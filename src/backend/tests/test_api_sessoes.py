"""Verifica o encerramento HTTP da sessão atual."""

import unittest

from fastapi import APIRouter, HTTPException, Response

from backend.api.factory import create_app
from backend.api.sessoes import COOKIE_SESSAO, criar_router
from backend.application.sessoes import RevogadorSessao


class RevogadorSessaoStub(RevogadorSessao):
    """Registra os tokens encaminhados pelo handler sem tocar no banco.

    O double guarda chamadas em memória. Ele existe para isolar a tradução
    HTTP do adapter de persistência.
    """

    def __init__(self) -> None:
        """Prepara histórico vazio de tokens revogados.

        Nenhum recurso externo é aberto. O construtor existe para tornar
        observável a dependência usada pelo teste.
        """
        self.tokens: list[str] = []

    async def revogar(self, token: str) -> None:
        """Registra o token apresentado ao handler sem persistir ou resumir.

        O método simula a porta de aplicação e mantém chamadas observáveis.
        Ele existe para conferir a delegação HTTP usando estado local.
        """
        self.tokens.append(token)


def _handler(revogador_sessao: RevogadorSessaoStub | None):
    """Localiza o handler DELETE sem iniciar servidor ASGI.

    A função procura a rota no router isolado e devolve sua função endpoint.
    Ela existe para testar respostas e delegação sem rede.
    """
    router: APIRouter = criar_router(revogador_sessao)
    for rota in router.routes:
        if rota.path == "/sessao/atual" and "DELETE" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota DELETE /sessao/atual não encontrada.")


class SessaoAtualRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Protege a revogação do token do cookie e a limpeza da sessão no cliente."""

    async def test_revoga_o_cookie_atual_e_envia_instrucao_de_remocao_segura(
        self,
    ) -> None:
        """Delega o token recebido e remove o cookie com atributos seguros.

        O handler recebe uma resposta em memória e um revogador double. O teste
        existe para proteger logout sem afetar outras sessões do estudante.
        """
        revogador = RevogadorSessaoStub()
        resposta = Response()

        resultado = await _handler(revogador)(resposta, "token-atual")

        cookie = resposta.headers["set-cookie"]
        self.assertIsNone(resultado)
        self.assertEqual(revogador.tokens, ["token-atual"])
        self.assertIn(f"{COOKIE_SESSAO}=", cookie)
        self.assertIn("Max-Age=0", cookie)
        self.assertIn("Path=/", cookie)
        self.assertIn("Secure", cookie)
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=lax", cookie)

    async def test_cookie_ausente_limpa_cliente_sem_chamar_revogador(self) -> None:
        """Mantém logout idempotente quando o navegador já não envia cookie.

        A rota recebe token ausente e ainda remove o cookie local. O teste
        existe para permitir repetição segura da operação de logout.
        """
        revogador = RevogadorSessaoStub()
        resposta = Response()

        await _handler(revogador)(resposta, None)

        self.assertEqual(revogador.tokens, [])
        self.assertIn("Max-Age=0", resposta.headers["set-cookie"])

    async def test_cookie_presente_sem_revogador_retorna_indisponibilidade(
        self,
    ) -> None:
        """Não confirma logout quando a persistência de revogação não existe.

        A rota devolve 503 antes de limpar o cookie, evitando sinalizar sucesso
        sem invalidar a credencial no servidor.
        """
        resposta = Response()

        with self.assertRaises(HTTPException) as contexto:
            await _handler(None)(resposta, "token-atual")

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertNotIn("set-cookie", resposta.headers)

    async def test_fabrica_registra_rota_de_logout(self) -> None:
        """Confirma que a composição expõe o método de logout no OpenAPI.

        A fábrica monta a aplicação sem iniciar servidor nem banco. O teste
        existe para impedir que o router fique fora da API pública.
        """
        app = create_app(revogador_sessao=RevogadorSessaoStub())

        operacao = app.openapi()["paths"]["/sessao/atual"]["delete"]

        self.assertEqual(
            operacao["responses"]["204"]["description"], "Successful Response"
        )
