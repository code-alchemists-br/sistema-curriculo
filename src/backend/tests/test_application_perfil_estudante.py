"""Testa unitariamente os casos de uso de edição e exclusão do perfil."""

from datetime import datetime, timezone
import unittest
from uuid import uuid4

from backend.application import (
    EditarPerfil,
    EditarPerfilEntrada,
    EmailJaCadastrado,
    ExcluirPerfil,
    ExcluirPerfilEntrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)
from backend.domain import Email, HashSenha, Nome, Usuario, UsuarioId

# Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001


class RepositorioUsuarioSpy:
    """Substitui a porta de usuário e registra atualizações solicitadas.

    O double consulta agregados em memória por ID ou e-mail e acumula os novos
    estados recebidos. Ele existe para testar a orquestração assíncrona sem ORM,
    banco, rede ou adapter produtivo.
    """

    def __init__(self, usuarios: list[Usuario] | None = None) -> None:
        """Prepara índices em memória e um histórico vazio de atualizações.

        O construtor copia os usuários fornecidos em dicionários por identidade
        e por e-mail. Ele existe para controlar ausência, propriedade do e-mail
        e estado excluído em cada cenário.
        """
        existentes = usuarios or []
        self._por_id = {usuario.id: usuario for usuario in existentes}
        self._por_email = {usuario.email: usuario for usuario in existentes}
        self.usuarios_atualizados: list[Usuario] = []

    async def obter_por_id(self, usuario_id: UsuarioId) -> Usuario | None:
        """Devolve por coroutine o usuário associado ao ID informado.

        O método consulta somente o dicionário controlado pelo teste e não faz
        I/O. Ele existe para simular a leitura aguardável exigida pelos casos.
        """
        return self._por_id.get(usuario_id)

    async def obter_por_email(self, email: Email) -> Usuario | None:
        """Devolve por coroutine o eventual proprietário do e-mail.

        O método usa o índice em memória, permitindo distinguir ausência, mesmo
        usuário e outro usuário. Ele existe para simular a regra de unicidade.
        """
        return self._por_email.get(email)

    async def atualizar(self, usuario: Usuario) -> None:
        """Registra por coroutine o novo estado solicitado pela Application.

        O método acumula o agregado sem persistir ou iniciar transação. Ele
        existe para tornar observável se e quando houve efeito de atualização.
        """
        self.usuarios_atualizados.append(usuario)


class RelogioStub:
    """Substitui o relógio por um instante fixo e conta suas consultas.

    O double devolve um valor configurado sem acessar o relógio do sistema. Ele
    existe para verificar o instante e evitar consulta temporal em repetição
    idempotente da exclusão.
    """

    def __init__(self, instante: datetime) -> None:
        """Armazena o instante fixo e inicia o contador de chamadas.

        O construtor não normaliza nem consulta tempo externo. Ele existe para
        preparar uma fonte temporal completamente controlada pelo teste.
        """
        self._instante = instante
        self.chamadas = 0

    def agora(self) -> datetime:
        """Devolve o instante preparado e registra uma consulta temporal.

        O método incrementa o contador antes de retornar o valor fixo. Ele existe
        para comprovar que somente a primeira exclusão precisa obter tempo.
        """
        self.chamadas += 1
        return self._instante


class EditarPerfilTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``EditarPerfil``.

    A classe substitui todas as portas por estado em memória e observa falhas e
    atualizações. Ela existe para testar a unidade Application sem qualquer
    adapter, framework ou infraestrutura.
    """

    async def test_edita_perfil_quando_email_nao_possui_outro_dono(self) -> None:
        """Confirma a edição e atualização quando o novo e-mail está livre.

        O teste fornece um perfil ativo e um e-mail ausente no índice, então
        compara estado retornado e efeito observado. Ele existe para proteger o
        caminho válido da orquestração.
        """
        usuario = _criar_usuario()
        repositorio = RepositorioUsuarioSpy([usuario])
        entrada = EditarPerfilEntrada(
            usuario.id, Nome("Ana Souza"), Email("ana.souza@example.com")
        )

        resultado = await EditarPerfil(repositorio).executar(entrada)

        self.assertEqual(resultado.nome, entrada.nome)
        self.assertEqual(resultado.email, entrada.email)
        self.assertEqual(resultado.id, usuario.id)
        self.assertEqual(resultado.hash_senha, usuario.hash_senha)
        self.assertEqual(repositorio.usuarios_atualizados, [resultado])

    async def test_aceita_manter_email_pertencente_ao_proprio_perfil(self) -> None:
        """Confirma que o próprio e-mail não é interpretado como duplicidade.

        O teste mantém o endereço indexado para o mesmo ID e observa a edição do
        nome. Ele existe para comparar propriedade, e não apenas existência.
        """
        usuario = _criar_usuario()
        repositorio = RepositorioUsuarioSpy([usuario])
        entrada = EditarPerfilEntrada(usuario.id, Nome("Ana Souza"), usuario.email)

        resultado = await EditarPerfil(repositorio).executar(entrada)

        self.assertEqual(resultado.email, usuario.email)
        self.assertEqual(repositorio.usuarios_atualizados, [resultado])

    async def test_rejeita_email_pertencente_a_outro_usuario(self) -> None:
        """Confirma que outro proprietário interrompe a edição sem atualização.

        O teste indexa o e-mail desejado sob ID distinto e observa a falha de
        duplicidade. Ele existe para preservar a unicidade no fluxo de edição.
        """
        usuario = _criar_usuario()
        outro = _criar_usuario(email="ocupado@example.com")
        repositorio = RepositorioUsuarioSpy([usuario, outro])
        entrada = EditarPerfilEntrada(usuario.id, Nome("Ana Souza"), outro.email)

        with self.assertRaises(EmailJaCadastrado):
            await EditarPerfil(repositorio).executar(entrada)

        self.assertEqual(repositorio.usuarios_atualizados, [])

    async def test_rejeita_perfil_inexistente_sem_atualizacao(self) -> None:
        """Confirma que ausência interrompe o fluxo antes das demais decisões.

        O teste usa repositório vazio e observa a falha e o histórico sem efeito.
        Ele existe para impedir criação implícita durante uma edição.
        """
        repositorio = RepositorioUsuarioSpy()
        entrada = EditarPerfilEntrada(
            UsuarioId(uuid4()), Nome("Ana Souza"), Email("ana@example.com")
        )

        with self.assertRaises(PerfilNaoEncontrado):
            await EditarPerfil(repositorio).executar(entrada)

        self.assertEqual(repositorio.usuarios_atualizados, [])

    async def test_rejeita_edicao_de_perfil_excluido(self) -> None:
        """Confirma que um estado excluído não pode ser atualizado ou reativado.

        O teste fornece agregado já excluído e observa a falha antes de efeitos.
        Ele existe para preservar a transição de ciclo de vida do perfil.
        """
        usuario = _criar_usuario().excluir(_instante_exclusao())
        repositorio = RepositorioUsuarioSpy([usuario])
        entrada = EditarPerfilEntrada(usuario.id, Nome("Ana Souza"), usuario.email)

        with self.assertRaises(PerfilExcluido):
            await EditarPerfil(repositorio).executar(entrada)

        self.assertEqual(repositorio.usuarios_atualizados, [])


class ExcluirPerfilTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``ExcluirPerfil``.

    A classe substitui repositório e relógio e observa atualização, instante e
    repetição. Ela existe para testar a exclusão lógica isoladamente de banco,
    API, autenticação e purga física.
    """

    async def test_exclui_perfil_ativo_com_instante_do_relogio(self) -> None:
        """Confirma a primeira transição e sua solicitação de atualização.

        O teste fornece usuário ativo e relógio fixo, então compara o instante e
        as interações dos doubles. Ele existe para proteger o caminho válido.
        """
        usuario = _criar_usuario()
        repositorio = RepositorioUsuarioSpy([usuario])
        relogio = RelogioStub(_instante_exclusao())

        resultado = await ExcluirPerfil(repositorio, relogio).executar(
            ExcluirPerfilEntrada(usuario.id)
        )

        self.assertTrue(resultado.excluido)
        self.assertEqual(resultado.deleted_at, _instante_exclusao())
        self.assertEqual(repositorio.usuarios_atualizados, [resultado])
        self.assertEqual(relogio.chamadas, 1)

    async def test_repeticao_de_exclusao_nao_altera_instante_nem_atualiza(self) -> None:
        """Confirma que perfil já excluído retorna sem novo efeito externo.

        O teste fornece estado removido e exige ausência de relógio e atualização.
        Ele existe para tornar retries seguros e preservar o primeiro instante.
        """
        usuario = _criar_usuario().excluir(_instante_exclusao())
        repositorio = RepositorioUsuarioSpy([usuario])
        relogio = RelogioStub(datetime(2026, 9, 21, tzinfo=timezone.utc))

        resultado = await ExcluirPerfil(repositorio, relogio).executar(
            ExcluirPerfilEntrada(usuario.id)
        )

        self.assertIs(resultado, usuario)
        self.assertEqual(resultado.deleted_at, _instante_exclusao())
        self.assertEqual(repositorio.usuarios_atualizados, [])
        self.assertEqual(relogio.chamadas, 0)

    async def test_rejeita_perfil_inexistente_sem_relogio_ou_atualizacao(self) -> None:
        """Confirma que ausência interrompe exclusão antes de qualquer efeito.

        O teste usa repositório vazio e observa falha, relógio intocado e nenhum
        agregado atualizado. Ele existe para impedir tombstone sem proprietário.
        """
        repositorio = RepositorioUsuarioSpy()
        relogio = RelogioStub(_instante_exclusao())

        with self.assertRaises(PerfilNaoEncontrado):
            await ExcluirPerfil(repositorio, relogio).executar(
                ExcluirPerfilEntrada(UsuarioId(uuid4()))
            )

        self.assertEqual(repositorio.usuarios_atualizados, [])
        self.assertEqual(relogio.chamadas, 0)


def _criar_usuario(email: str = "ana@example.com") -> Usuario:
    """Cria perfil ativo com dados válidos para os casos de uso.

    A função monta um agregado sem acessar gerador, banco ou relógio e permite
    variar somente o e-mail relevante ao cenário. Ela existe para reduzir
    repetição mantendo cada teste focado na decisão de fluxo.
    """
    return Usuario(
        id=UsuarioId(uuid4()),
        nome=Nome("Ana Silva"),
        email=Email(email),
        hash_senha=HashSenha("hash-ja-derivado"),
    )


def _instante_exclusao() -> datetime:
    """Fornece instante UTC fixo para comparar a exclusão lógica.

    A função retorna um valor estável sem consultar recurso externo. Ela existe
    para manter os testes determinísticos em qualquer data de execução.
    """
    return datetime(2026, 9, 20, tzinfo=timezone.utc)
