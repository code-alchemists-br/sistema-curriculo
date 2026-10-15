"""Testa a atualização integral do agregado de perfil na Application."""

import unittest
from datetime import datetime, timezone
from uuid import uuid4

from backend.application import (
    AtualizarPerfilCompleto,
    AtualizarPerfilCompletoEntrada,
    EmailJaCadastrado,
    PerfilExcluido,
    PerfilNaoEncontrado,
)
from backend.domain import (
    DadosContato,
    Email,
    Endereco,
    HashSenha,
    Nome,
    Telefone,
    Usuario,
    UsuarioId,
)


class RepositorioUsuarioSpy:
    """Mantém perfis em memória e registra pedidos de persistência.

    O double implementa as consultas necessárias ao caso de uso sem I/O e
    conserva estado atualizado para as asserções. Ele existe para testar
    unicidade e atualização atômica sem depender de adapter ou banco.
    """

    def __init__(self, usuarios: tuple[Usuario, ...]) -> None:
        """Indexa os perfis fornecidos por ID e e-mail.

        O construtor cria índices independentes para consultas do caso de uso
        e inicia o histórico de atualizações. Ele existe para preparar estado
        determinístico por cenário.
        """
        self._por_id = {usuario.id: usuario for usuario in usuarios}
        self._por_email = {usuario.email: usuario for usuario in usuarios}
        self.atualizados: list[Usuario] = []

    async def obter_por_id(self, usuario_id: UsuarioId) -> Usuario | None:
        """Busca no índice local o agregado associado à identidade tipada.

        O método não realiza I/O e devolve ausência quando o UUID não existe.
        Ele existe para simular a consulta de proprietário exigida pela porta.
        """
        return self._por_id.get(usuario_id)

    async def obter_por_email(self, email: Email) -> Usuario | None:
        """Consulta no índice em memória o proprietário de um e-mail.

        A operação retorna `None` quando o valor está livre. Ela existe para
        reproduzir a verificação de unicidade do caso de uso sem banco.
        """
        return self._por_email.get(email)

    async def atualizar(self, usuario: Usuario) -> None:
        """Registra a gravação e atualiza ambos os índices em memória.

        O método mantém o estado posterior e adiciona o agregado ao histórico.
        Ele existe para observar uma persistência integral única no teste.
        """
        self.atualizados.append(usuario)
        self._por_id[usuario.id] = usuario
        self._por_email[usuario.email] = usuario


def _criar_usuario(email: str = "ana@example.com") -> Usuario:
    """Cria um agregado ativo e válido para os cenários unitários.

    A função constrói valores de domínio sem relógio, banco ou gerador. Ela
    existe para manter os testes focados na coordenação da atualização.
    """
    return Usuario(
        id=UsuarioId(uuid4()),
        nome=Nome("Ana Silva"),
        email=Email(email),
        hash_senha=HashSenha("hash-que-nao-deve-mudar"),
    )


def _entrada(usuario_id: UsuarioId, email: str = "ana.nova@example.com") -> AtualizarPerfilCompletoEntrada:
    """Monta valores válidos para substituir todos os campos editáveis.

    A entrada usa novo nome, e-mail e contato profissional já validados pelo
    domínio. Ela existe para reutilizar o mesmo cenário base nos testes.
    """
    return AtualizarPerfilCompletoEntrada(
        usuario_id=usuario_id,
        nome=Nome("Ana Souza"),
        email=Email(email),
        dados_contato=DadosContato(
            endereco=Endereco("Av. Central, 300"),
            telefones=(Telefone("11988887777"),),
            linkedin="https://linkedin.com/in/ana-souza",
            curriculo_lattes="http://lattes.cnpq.br/123",
            cidade="São Paulo",
        ),
    )


class AtualizarPerfilCompletoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica validação, composição e persistência do perfil integral.

    Os cenários usam um repositório em memória para cobrir sucesso e bloqueios
    antes da gravação. A classe existe para proteger as regras da Application
    sem depender de transporte ou banco.
    """

    async def test_atualiza_todos_os_campos_em_uma_persistencia(self) -> None:
        """Persiste identidade e contato juntos preservando credenciais.

        O teste executa o caso real contra um repositório em memória e compara
        o estado completo e o número de gravações. Ele existe para garantir
        atualização integral sem estado parcialmente salvo.
        """
        usuario = _criar_usuario()
        repositorio = RepositorioUsuarioSpy((usuario,))
        entrada = _entrada(usuario.id)

        resultado = await AtualizarPerfilCompleto(repositorio).executar(entrada)

        self.assertEqual(resultado.nome, entrada.nome)
        self.assertEqual(resultado.email, entrada.email)
        self.assertEqual(resultado.dados_contato, entrada.dados_contato)
        self.assertEqual(resultado.hash_senha, usuario.hash_senha)
        self.assertEqual(repositorio.atualizados, [resultado])

    async def test_email_de_outro_perfil_nao_persiste_nenhum_campo(self) -> None:
        """Rejeita e-mail ocupado antes de alterar qualquer campo do perfil.

        O repositório contém outro usuário dono do e-mail solicitado. O teste
        existe para garantir que a validação anteceda a única persistência.
        """
        usuario = _criar_usuario()
        outro = _criar_usuario("ocupado@example.com")
        repositorio = RepositorioUsuarioSpy((usuario, outro))
        entrada = _entrada(usuario.id, outro.email.valor)

        with self.assertRaises(EmailJaCadastrado):
            await AtualizarPerfilCompleto(repositorio).executar(entrada)

        self.assertEqual(repositorio.atualizados, [])

    async def test_perfil_inexistente_nao_persiste(self) -> None:
        """Rejeita identidade ausente sem criar perfil durante uma edição.

        O repositório vazio representa um UUID desconhecido. O teste existe
        para impedir que a intenção de atualização vire cadastro implícito.
        """
        repositorio = RepositorioUsuarioSpy(())

        with self.assertRaises(PerfilNaoEncontrado):
            await AtualizarPerfilCompleto(repositorio).executar(
                _entrada(UsuarioId(uuid4()))
            )

        self.assertEqual(repositorio.atualizados, [])

    async def test_perfil_excluido_nao_persiste(self) -> None:
        """Impede que a atualização integral reative um perfil excluído.

        O cenário fornece um agregado marcado como removido e inspeciona a
        ausência de gravação. Ele existe para preservar o ciclo de vida.
        """
        usuario = _criar_usuario().excluir(datetime(2026, 10, 14, tzinfo=timezone.utc))
        repositorio = RepositorioUsuarioSpy((usuario,))

        with self.assertRaises(PerfilExcluido):
            await AtualizarPerfilCompleto(repositorio).executar(_entrada(usuario.id))

        self.assertEqual(repositorio.atualizados, [])
