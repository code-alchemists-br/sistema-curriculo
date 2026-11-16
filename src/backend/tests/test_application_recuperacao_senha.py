"""Testa regras de solicitação e consumo de tokens de recuperação."""

import unittest
from datetime import datetime, timedelta, timezone
from uuid import UUID

from backend.application.recuperacao_senha import (
    EntradaRedefinicaoSenha,
    RedefinirSenha,
    SolicitarRecuperacaoSenha,
    TokenRecuperacaoGerado,
)
from backend.domain.usuario import Usuario
from backend.domain.value_objects import Email, HashSenha, Nome, UsuarioId

INSTANTE = datetime(2026, 11, 15, 12, tzinfo=timezone.utc)
ID_USUARIO = UsuarioId(UUID(int=1))
EMAIL = Email("ana@example.test")


class RelogioFixo:
    """Fornece instante previsível às regras temporais do fluxo."""

    def agora(self) -> datetime:
        """Devolve o instante fixo sem consultar relógio global.

        O valor permite validar validade e consumo de token deterministicamente.
        Ele existe para isolar o caso de uso do tempo real.
        """
        return INSTANTE


class GeradorTokenFalso:
    """Produz credencial e resumo determinísticos para os testes de aplicação."""

    def gerar(self) -> TokenRecuperacaoGerado:
        """Devolve valores de teste sem usar aleatoriedade criptográfica.

        A implementação mantém a correspondência entre segredo e resumo. Ela
        existe para que o teste confirme a orquestração sem depender do adapter.
        """
        return TokenRecuperacaoGerado("token-secreto", "a" * 64)

    def resumir(self, token: str) -> str:
        """Devolve o resumo estável esperado pelo cenário.

        O teste usa um único token conhecido para observar a consulta à porta.
        O método existe para substituir o algoritmo real de hashing.
        """
        return "a" * 64 if token == "token-secreto" else "b" * 64


class RepositorioUsuarioFalso:
    """Mantém usuário em memória para observar leituras e atualizações."""

    def __init__(self, usuario: Usuario | None) -> None:
        """Guarda estado inicial e prepara rastreamento de escrita.

        O repositório não acessa banco e permite simular ausência e conta ativa.
        Ele existe para verificar somente as regras da Application.
        """
        self.usuario = usuario
        self.atualizacoes: list[Usuario] = []

    async def obter_por_email(self, email: Email) -> Usuario | None:
        """Devolve a conta configurada somente quando o e-mail corresponde.

        A comparação usa o value object normalizado. Ela existe para representar
        a porta consultada pelo caso de solicitação.
        """
        return self.usuario if self.usuario and self.usuario.email == email else None

    async def obter_por_id(self, usuario_id: UsuarioId) -> Usuario | None:
        """Devolve a conta configurada para a identidade consultada.

        A comparação mantém a identidade tipada e não acessa armazenamento.
        Ela existe para acompanhar o fluxo de confirmação.
        """
        return self.usuario if self.usuario and self.usuario.id == usuario_id else None

    async def atualizar(self, usuario: Usuario) -> None:
        """Registra nova versão do agregado para a asserção do teste.

        A lista representa uma escrita confirmada pelo caso de uso. Ela existe
        para provar que somente tokens válidos alteram a credencial.
        """
        self.usuario = usuario
        self.atualizacoes.append(usuario)


class RepositorioTokensFalso:
    """Registra criação e consumo de token sem persistência externa."""

    def __init__(self, usuario_id: UsuarioId | None = ID_USUARIO) -> None:
        """Configura resultado de consumo e mantém registros observáveis.

        O repositório não consulta banco. Ele existe para testar decisões do
        caso de uso sem acoplar regras a SQLAlchemy.
        """
        self.usuario_id = usuario_id
        self.criacoes: list[tuple[UsuarioId, str, datetime, datetime]] = []
        self.consumos: list[tuple[str, datetime]] = []

    async def criar(self, usuario_id, resumo, criada_em, expira_em) -> bool:
        """Registra metadados e informa que a solicitação foi aceita.

        O método retém somente o resumo, reproduzindo a porta de persistência.
        Ele existe para validar prazo e proprietário.
        """
        self.criacoes.append((usuario_id, resumo, criada_em, expira_em))
        return True

    async def consumir(self, resumo: str, instante: datetime) -> UsuarioId | None:
        """Registra a consulta e devolve identidade ou ausência configurada.

        O resultado simula token válido ou inválido sem alterar banco. Ele
        existe para observar se o caso prossegue à troca da senha.
        """
        self.consumos.append((resumo, instante))
        return self.usuario_id


class RevogadorSessoesFalso:
    """Registra revogações solicitadas pelo caso de redefinição."""

    def __init__(self) -> None:
        """Cria histórico vazio para confirmar efeitos do caso de uso."""
        self.revogacoes: list[tuple[UsuarioId, datetime]] = []

    async def revogar_todas(self, usuario_id: UsuarioId, instante: datetime) -> None:
        """Guarda usuário e instante recebidos sem acessar sessão persistida.

        A implementação funciona como spy. Ela existe para verificar que toda
        troca de senha invalida as sessões antigas.
        """
        self.revogacoes.append((usuario_id, instante))


def criar_usuario(*, excluido: bool = False) -> Usuario:
    """Cria agregado mínimo com credencial derivada para os cenários.

    O helper usa VOs reais e identidade determinística. Ele existe para evitar
    fixtures de infraestrutura nos testes de Application.
    """
    return Usuario(
        id=ID_USUARIO,
        nome=Nome("Ana"),
        email=EMAIL,
        hash_senha=HashSenha("hash-antigo"),
        deleted_at=INSTANTE if excluido else None,
    )


class SolicitacaoRecuperacaoSenhaTestCase(unittest.IsolatedAsyncioTestCase):
    """Confere criação limitada e resposta interna do caso de solicitação."""

    async def test_cria_token_de_quinze_minutos_para_conta_ativa(self) -> None:
        """Cria resumo persistido e devolve token somente ao adapter de e-mail."""
        usuarios = RepositorioUsuarioFalso(criar_usuario())
        tokens = RepositorioTokensFalso()
        caso = SolicitarRecuperacaoSenha(
            usuarios, tokens, GeradorTokenFalso(), RelogioFixo()
        )

        envio = await caso.executar(EMAIL)

        self.assertIsNotNone(envio)
        assert envio is not None
        self.assertEqual(envio.email, EMAIL)
        self.assertEqual(envio.token, "token-secreto")
        self.assertEqual(
            tokens.criacoes,
            [(ID_USUARIO, "a" * 64, INSTANTE, INSTANTE + timedelta(minutes=15))],
        )

    async def test_nao_cria_token_para_conta_ausente_ou_excluida(self) -> None:
        """Mantém ausências sem criação para não associar token a perfil inelegível."""
        for usuario in (None, criar_usuario(excluido=True)):
            with self.subTest(usuario_ausente=usuario is None):
                tokens = RepositorioTokensFalso()
                caso = SolicitarRecuperacaoSenha(
                    RepositorioUsuarioFalso(usuario),
                    tokens,
                    GeradorTokenFalso(),
                    RelogioFixo(),
                )
                self.assertIsNone(await caso.executar(EMAIL))
                self.assertEqual(tokens.criacoes, [])


class RedefinirSenhaTestCase(unittest.IsolatedAsyncioTestCase):
    """Confere troca de credencial e invalidação das sessões no mesmo fluxo."""

    async def test_token_valido_atualiza_conta_e_revoga_sessoes(self) -> None:
        """Aplica a senha derivada apenas após consumo bem-sucedido do token."""
        usuarios = RepositorioUsuarioFalso(criar_usuario())
        tokens = RepositorioTokensFalso()
        sessoes = RevogadorSessoesFalso()
        caso = RedefinirSenha(
            usuarios, tokens, sessoes, GeradorTokenFalso(), RelogioFixo()
        )

        resultado = await caso.executar(
            EntradaRedefinicaoSenha("token-secreto", HashSenha("hash-novo"))
        )

        self.assertTrue(resultado)
        self.assertEqual(tokens.consumos, [("a" * 64, INSTANTE)])
        self.assertEqual(usuarios.usuario.hash_senha, HashSenha("hash-novo"))
        self.assertEqual(sessoes.revogacoes, [(ID_USUARIO, INSTANTE)])

    async def test_token_invalido_nao_altera_credencial_ou_sessoes(self) -> None:
        """Interrompe o fluxo antes de qualquer efeito quando o token não existe."""
        usuarios = RepositorioUsuarioFalso(criar_usuario())
        tokens = RepositorioTokensFalso(usuario_id=None)
        sessoes = RevogadorSessoesFalso()
        caso = RedefinirSenha(
            usuarios, tokens, sessoes, GeradorTokenFalso(), RelogioFixo()
        )

        resultado = await caso.executar(
            EntradaRedefinicaoSenha("token-secreto", HashSenha("hash-novo"))
        )

        self.assertFalse(resultado)
        self.assertEqual(usuarios.atualizacoes, [])
        self.assertEqual(sessoes.revogacoes, [])
