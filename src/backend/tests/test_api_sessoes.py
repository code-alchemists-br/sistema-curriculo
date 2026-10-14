"""Testa emissão e encerramento de sessão na fronteira HTTP."""

import unittest
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, FastAPI, HTTPException, Response

from backend.api.cadastro_acesso import AcessoEstudanteRequisicao, criar_router, obter_principal
from backend.application import AcessarEstudanteEntrada
from backend.domain import Email, HashSenha, Nome, Usuario, UsuarioId
from backend.infrastructure.security.sessoes import SessoesSqlAlchemy


class AcessoExecutorStub:
    """Devolve identidade autenticada sem consultar banco ou senha real.

    O double registra a entrada e existe para isolar a emissão de sessão do
    caso de uso de validação de credenciais.
    """

    def __init__(self, usuario: Usuario) -> None:
        """Guarda a conta que representa credenciais válidas no cenário."""
        self.usuario = usuario
        self.entradas: list[AcessarEstudanteEntrada] = []

    async def executar(self, entrada: AcessarEstudanteEntrada) -> Usuario:
        """Registra a tentativa e devolve o agregado autenticado configurado."""
        self.entradas.append(entrada)
        return self.usuario


class SessoesStub:
    """Simula gerenciamento de sessão e registra operações solicitadas.

    Os métodos retornam valores estáveis sem persistência. O double existe para
    verificar que a API cria, resolve e revoga sessões através do contrato.
    """

    def __init__(self) -> None:
        """Inicializa histórico vazio e token previsível para as asserções."""
        self.criacoes: list[object] = []
        self.revogacoes: list[str | None] = []

    async def criar(self, usuario_id):
        """Registra proprietário e devolve token de teste com prazo futuro."""
        self.criacoes.append(usuario_id)
        return "token-de-teste", datetime(2030, 1, 1, tzinfo=timezone.utc)

    async def usuario_da_sessao(self, token):
        """Retorna a conta sintética somente para o token conhecido."""
        return self.criacoes[0] if token == "token-de-teste" and self.criacoes else None

    async def revogar(self, token):
        """Registra a credencial que a API solicitou invalidar."""
        self.revogacoes.append(token)


def _endpoint(router: APIRouter, caminho: str, metodo: str):
    """Localiza handler registrado para chamada isolada sem servidor HTTP."""
    for rota in router.routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota.endpoint
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


class SessaoApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica cookie de login e revogação pelo endpoint de logout."""

    async def test_login_emite_cookie_seguro_sem_payload_de_token(self) -> None:
        """Confirma flags do cookie e associação ao usuário autenticado."""
        usuario = Usuario(UsuarioId(uuid4()), Nome("Ana Silva"), Email("ana@example.com"), HashSenha("hash"))
        sessoes = SessoesStub()
        router = criar_router(None, AcessoExecutorStub(usuario), sessoes=sessoes)

        resposta = await _endpoint(router, "/acessos", "POST")(AcessoEstudanteRequisicao(email="ana@example.com", senha="senha-correta"))

        cookie = resposta.headers["set-cookie"]
        self.assertIn("sistema_curriculo_sessao=token-de-teste", cookie)
        self.assertIn("httponly", cookie.lower())
        self.assertIn("secure", cookie.lower())
        self.assertIn("samesite=lax", cookie.lower())
        self.assertEqual(sessoes.criacoes, [usuario.id.valor])
        self.assertEqual(resposta.body, b"")

    async def test_logout_revoga_cookie_atual_e_o_remove(self) -> None:
        """Confirma que logout usa o cookie e ordena sua remoção."""
        from starlette.requests import Request

        sessoes = SessoesStub()
        router = criar_router(None, None, sessoes=sessoes)
        request = Request({"type": "http", "headers": [(b"cookie", b"sistema_curriculo_sessao=token-de-teste")]})
        response = Response()

        await _endpoint(router, "/sessoes/logout", "POST")(request, response)

        self.assertEqual(sessoes.revogacoes, ["token-de-teste"])
        self.assertIn("max-age=0", response.headers["set-cookie"].lower())

    async def test_persistencia_usa_digest_sem_reter_token_bruto(self) -> None:
        """Confirma digest SHA-256 estável e de tamanho fixo para armazenamento."""
        digest = SessoesSqlAlchemy._hash("segredo-de-sessao")

        self.assertEqual(len(digest), 64)
        self.assertNotEqual(digest, "segredo-de-sessao")
        self.assertEqual(digest, SessoesSqlAlchemy._hash("segredo-de-sessao"))

    async def test_principal_e_derivado_do_cookie_validado(self) -> None:
        """Resolve o usuário pelo cookie com o gerenciador da composição."""
        from starlette.requests import Request

        sessoes = SessoesStub()
        usuario_id = uuid4()
        sessoes.criacoes.append(usuario_id)
        app = FastAPI()
        app.state.sessoes = sessoes
        request = Request({"type": "http", "app": app, "headers": [(b"cookie", b"sistema_curriculo_sessao=token-de-teste")]})

        self.assertEqual(await obter_principal(request), usuario_id)

    async def test_principal_rejeita_token_ausente(self) -> None:
        """Responde 401 quando a requisição não traz sessão validável."""
        from starlette.requests import Request

        app = FastAPI()
        app.state.sessoes = SessoesStub()
        request = Request({"type": "http", "app": app, "headers": []})

        with self.assertRaises(HTTPException) as erro:
            await obter_principal(request)

        self.assertEqual(erro.exception.status_code, 401)
