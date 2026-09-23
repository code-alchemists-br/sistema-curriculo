"""Testa unitariamente as operações de perfil e cadastro de formação."""

from datetime import date, datetime, timezone
import unittest
from uuid import uuid4

# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
from backend.application import (
    CadastrarFormacaoAcademica,
    CadastrarFormacaoAcademicaEntrada,
    EditarPerfil,
    EditarPerfilEntrada,
    EmailJaCadastrado,
    ExcluirPerfil,
    ExcluirPerfilEntrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)
from backend.domain import (
    Email,
    FormacaoAcademica,
    FormacaoAcademicaId,
    HashSenha,
    Nome,
    Periodo,
    Usuario,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001


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


# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
class RepositorioFormacaoAcademicaSpy:
    """Substitui a porta de formação e registra salvamentos solicitados.

    O double acumula entidades recebidas inteiramente em memória e não acessa
    banco, ORM ou rede. Ele existe para observar o efeito externo do caso de
    uso de cadastro sem transformar o teste unitário em teste de integração.
    """

    def __init__(self) -> None:
        """Inicia o histórico vazio de formações salvas pelo caso de uso.

        O construtor não configura recursos externos e mantém apenas uma lista
        controlada pelo teste. Ele existe para tornar observável cada solicitação
        de persistência feita pela orquestração.
        """
        self.formacoes_salvas: list[FormacaoAcademica] = []

    async def salvar(self, formacao: FormacaoAcademica) -> None:
        """Registra assincronamente a formação recebida sem persistência real.

        O método acrescenta a mesma entidade ao histórico em memória e não
        modifica seu conteúdo. Ele existe para simular a porta aguardável e
        permitir afirmar se o cadastro solicitou ou evitou o salvamento.
        """
        self.formacoes_salvas.append(formacao)


# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
class GeradorFormacaoAcademicaIdStub:
    """Substitui a geração de ID por valor fixo e conta suas utilizações.

    O double devolve sempre a identidade configurada e registra as chamadas,
    sem produzir aleatoriedade. Ele existe para verificar tanto a identidade da
    entidade criada quanto a ausência de geração nos fluxos interrompidos.
    """

    def __init__(self, formacao_id: FormacaoAcademicaId) -> None:
        """Armazena a identidade fixa e zera o contador de chamadas.

        O construtor recebe o value object pronto, sem criar UUID ou consultar
        serviço externo. Ele existe para preparar uma dependência totalmente
        determinística para os cenários de cadastro.
        """
        self._formacao_id = formacao_id
        self.chamadas = 0

    def gerar(self) -> FormacaoAcademicaId:
        """Devolve a identidade configurada e registra uma solicitação.

        O método incrementa o contador antes de retornar o mesmo value object,
        preservando a previsibilidade do teste. Ele existe para tornar visível
        quando o caso de uso efetivamente inicia a criação da entidade.
        """
        self.chamadas += 1
        return self._formacao_id


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


# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
class CadastrarFormacaoAcademicaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o cadastro de formação isolado de qualquer adapter externo.

    A classe usa spy de repositório, stub de gerador e perfil em memória para
    observar a sequência de decisões do caso de uso. Ela existe para proteger
    a associação com perfil ativo sem depender de banco, API ou ORM.
    """

    async def test_cadastra_formacao_para_perfil_ativo(self) -> None:
        """Confirma a criação e o salvamento da formação com dados recebidos.

        O teste fornece proprietário ativo, ID fixo e entrada válida, então
        compara a entidade retornada ao efeito observado pelo spy. Ele existe
        para proteger o caminho bem-sucedido da orquestração.
        """
        usuario = _criar_usuario()
        repositorio_usuario = RepositorioUsuarioSpy([usuario])
        repositorio_formacao = RepositorioFormacaoAcademicaSpy()
        formacao_id = FormacaoAcademicaId(uuid4())
        gerador = GeradorFormacaoAcademicaIdStub(formacao_id)
        entrada = _criar_entrada_formacao(usuario.id)

        resultado = await CadastrarFormacaoAcademica(
            repositorio_usuario, repositorio_formacao, gerador
        ).executar(entrada)

        self.assertEqual(resultado.id, formacao_id)
        self.assertEqual(resultado.usuario_id, usuario.id)
        self.assertEqual(resultado.instituicao, entrada.instituicao)
        self.assertEqual(resultado.curso, entrada.curso)
        self.assertEqual(resultado.nivel, entrada.nivel)
        self.assertEqual(resultado.periodo, entrada.periodo)
        self.assertEqual(resultado.status, entrada.status)
        self.assertEqual(repositorio_formacao.formacoes_salvas, [resultado])
        self.assertEqual(gerador.chamadas, 1)

    async def test_rejeita_perfil_inexistente_sem_gerar_ou_salvar_formacao(self) -> None:
        """Confirma que ausência do proprietário interrompe o cadastro cedo.

        O teste consulta um repositório sem usuário e observa a falha junto à
        ausência de chamadas ao gerador e ao spy. Ele existe para impedir que a
        Application crie ou persista formação órfã.
        """
        repositorio_usuario = RepositorioUsuarioSpy()
        repositorio_formacao = RepositorioFormacaoAcademicaSpy()
        gerador = GeradorFormacaoAcademicaIdStub(FormacaoAcademicaId(uuid4()))
        entrada = _criar_entrada_formacao(UsuarioId(uuid4()))

        with self.assertRaises(PerfilNaoEncontrado):
            await CadastrarFormacaoAcademica(
                repositorio_usuario, repositorio_formacao, gerador
            ).executar(entrada)

        self.assertEqual(gerador.chamadas, 0)
        self.assertEqual(repositorio_formacao.formacoes_salvas, [])

    async def test_rejeita_perfil_excluido_sem_gerar_ou_salvar_formacao(self) -> None:
        """Confirma que perfil excluído não recebe nova formação acadêmica.

        O teste fornece usuário removido e observa a falha antes de qualquer
        geração ou salvamento. Ele existe para preservar o ciclo de vida do
        perfil e impedir sua ampliação implícita após exclusão lógica.
        """
        usuario = _criar_usuario().excluir(_instante_exclusao())
        repositorio_usuario = RepositorioUsuarioSpy([usuario])
        repositorio_formacao = RepositorioFormacaoAcademicaSpy()
        gerador = GeradorFormacaoAcademicaIdStub(FormacaoAcademicaId(uuid4()))
        entrada = _criar_entrada_formacao(usuario.id)

        with self.assertRaises(PerfilExcluido):
            await CadastrarFormacaoAcademica(
                repositorio_usuario, repositorio_formacao, gerador
            ).executar(entrada)

        self.assertEqual(gerador.chamadas, 0)
        self.assertEqual(repositorio_formacao.formacoes_salvas, [])


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


# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
def _criar_entrada_formacao(
    usuario_id: UsuarioId,
) -> CadastrarFormacaoAcademicaEntrada:
    """Monta uma entrada válida e estável para cenários de cadastro.

    A função reúne textos e período em memória sem consultar gerador, relógio
    ou persistência. Ela existe para manter os testes focados nas decisões do
    caso de uso, variando somente o proprietário quando necessário.
    """
    return CadastrarFormacaoAcademicaEntrada(
        usuario_id=usuario_id,
        instituicao="FATEC",
        curso="Análise e Desenvolvimento de Sistemas",
        nivel="tecnologo",
        periodo=Periodo(date(2024, 2, 1)),
        status="em_andamento",
    )


def _instante_exclusao() -> datetime:
    """Fornece instante UTC fixo para comparar a exclusão lógica.

    A função retorna um valor estável sem consultar recurso externo. Ela existe
    para manter os testes determinísticos em qualquer data de execução.
    """
    return datetime(2026, 9, 20, tzinfo=timezone.utc)
