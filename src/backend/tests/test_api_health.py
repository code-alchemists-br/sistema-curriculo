"""Testa unitariamente os endpoints de health check e readiness check."""

import json
import unittest

from fastapi import HTTPException

from backend.api.factory import create_app
from backend.api.health import (
    HealthResposta,
    ReadyResposta,
    VerificadorConectividadePersistencia,
    criar_router,
)
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.domain.value_objects import UsuarioId

# Proveniência: decision-analysis prompts/backend/20261014-175641-health-readiness-checks-v001.md#v001


class VerificadorConectividadeStub(VerificadorConectividadePersistencia):
    """Substitui a verificação de persistência com comportamento configurável.

    O double permite simular resposta operacional positiva, falha de conexão ou
    lançamento de exceções durante a verificação de prontidão. Ele existe para
    exercitar o comportamento do endpoint /ready sem acessar bancos de dados reais.
    """

    def __init__(
        self, operacional: bool = True, erro: Exception | None = None
    ) -> None:
        """Configura o resultado booleano ou a exceção simulada pelo verificador.

        O construtor armazena o estado desejado para ser retornado na chamada
        assíncrona subsequente. Ele existe para parametrizar cenários de teste unitário.
        """
        self._operacional = operacional
        self._erro = erro
        self.chamadas = 0

    async def checar_conectividade(self) -> bool:
        """Devolve o estado pré-configurado ou levanta o erro programado.

        O método contabiliza as invocações e reproduz a resposta simulada sem I/O.
        Ele existe para validar o tratamento de erros do handler de prontidão.
        """
        self.chamadas += 1
        if self._erro is not None:
            raise self._erro
        return self._operacional


class AutenticadorSessaoFake(AutenticadorSessao):
    """Substitui o serviço de autenticação para testes de rotas com middleware.

    O double não consulta banco e rejeita qualquer token para garantir que
    rotas públicas funcionem mesmo sem credenciais válidas. Ele existe para
    comprovar que /health e /ready dispensam autenticação.
    """

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Retorna None para simular qualquer tentativa sem sessão válida.

        O método não faz I/O e sempre rejeita o token recebido. Ele existe para
        garantir que requisições públicas funcionem mesmo quando não autenticadas.
        """
        return None


def _obter_endpoint(router, caminho: str, metodo: str):
    """Localiza a função de endpoint associada a uma rota registrada.

    A função percorre as rotas do APIRouter para recuperar a corrotina correspondente
    ao método e caminho informados. Ela existe para permitir chamadas unitárias diretas
    sem inicializar o servidor ASGI.
    """
    for rota in router.routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota.endpoint
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


async def _requisitar_asgi(app, metodo: str, caminho: str) -> tuple[int, dict]:
    """Executa uma requisição ASGI em memória na aplicação e extrai status e JSON.

    A função monta o escopo ASGI, despacha a mensagem diretamente na aplicação
    e captura os buffers de resposta. Ela existe para exercitar middlewares e roteamento
    completos sem abrir sockets de rede.
    """
    escopo = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": metodo,
        "scheme": "http",
        "path": caminho,
        "raw_path": caminho.encode(),
        "query_string": b"",
        "headers": [(b"host", b"testserver")],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }
    status_code = 0
    corpo_bytes: list[bytes] = []

    async def receber() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def enviar(mensagem: dict) -> None:
        nonlocal status_code
        if mensagem["type"] == "http.response.start":
            status_code = mensagem["status"]
        elif mensagem["type"] == "http.response.body":
            corpo_bytes.append(mensagem.get("body", b""))

    await app(escopo, receber, enviar)
    corpo = json.loads(b"".join(corpo_bytes).decode("utf-8")) if corpo_bytes else {}
    return status_code, corpo


class ApiHealthTestCase(unittest.IsolatedAsyncioTestCase):
    """Agrupa os testes unitários das rotas /health e /ready."""

    async def test_health_retorna_200_com_status_ok_sem_dados_sensiveis(self) -> None:
        """Confirma que /health responde 200 OK e exatamente {'status': 'ok'}.

        O teste invoca diretamente o endpoint de liveness e inspeciona o DTO
        gerado para garantir conformidade com a política de sigilo de ambiente.
        """
        router = criar_router()
        endpoint = _obter_endpoint(router, "/health", "GET")

        resposta = await endpoint()

        self.assertIsInstance(resposta, HealthResposta)
        self.assertEqual(resposta.status, "ok")
        self.assertEqual(resposta.model_dump(), {"status": "ok"})

    async def test_ready_retorna_200_quando_persistencia_conectada(self) -> None:
        """Confirma que /ready responde 200 OK quando o verificador retorna True.

        O teste injeta um stub de conectividade operacional e valida a confirmação
        de prontidão retornada pelo handler.
        """
        verificador = VerificadorConectividadeStub(operacional=True)
        router = criar_router(verificador)
        endpoint = _obter_endpoint(router, "/ready", "GET")

        resposta = await endpoint()

        self.assertIsInstance(resposta, ReadyResposta)
        self.assertEqual(resposta.status, "ready")
        self.assertEqual(verificador.chamadas, 1)

    async def test_ready_lanca_503_quando_persistencia_inoperante(self) -> None:
        """Confirma 503 Service Unavailable quando o verificador reporta False.

        O teste simula resposta de falha do banco e verifica se o handler converte
        em HTTPException 503 com mensagem clara e segura.
        """
        verificador = VerificadorConectividadeStub(operacional=False)
        router = criar_router(verificador)
        endpoint = _obter_endpoint(router, "/ready", "GET")

        with self.assertRaises(HTTPException) as contexto:
            await endpoint()

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Persistência indisponível.")
        self.assertEqual(verificador.chamadas, 1)

    async def test_ready_lanca_503_quando_persistencia_levanta_excecao(self) -> None:
        """Confirma 503 Service Unavailable quando o verificador gera exceção de I/O.

        O teste programa o stub para lançar RuntimeError e confirma que a exceção
        é tratada pelo router sem vazar stack trace para o chamador.
        """
        verificador = VerificadorConectividadeStub(erro=RuntimeError("Timeout no banco"))
        router = criar_router(verificador)
        endpoint = _obter_endpoint(router, "/ready", "GET")

        with self.assertRaises(HTTPException) as contexto:
            await endpoint()

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Persistência indisponível.")
        self.assertEqual(verificador.chamadas, 1)

    async def test_ready_lanca_503_quando_verificador_nao_fornecido(self) -> None:
        """Confirma 503 Service Unavailable quando o verificador for None.

        O teste cria o router sem fornecer capacidade de checagem e verifica a
        indisponibilidade explícita de prontidão.
        """
        router = criar_router(verificador_conectividade=None)
        endpoint = _obter_endpoint(router, "/ready", "GET")

        with self.assertRaises(HTTPException) as contexto:
            await endpoint()

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Persistência indisponível.")

    async def test_health_e_ready_sao_rotas_publicas_liberadas_pelo_middleware(
        self,
    ) -> None:
        """Confirma que /health e /ready respondem 200 via ASGI mesmo sem sessão ativa.

        O teste instancia a aplicação completa com MiddlewareAutenticacaoSessao
        e valida que requisições anônimas para as sondas não sofrem bloqueio 401.
        """
        verificador = VerificadorConectividadeStub(operacional=True)
        autenticador = AutenticadorSessaoFake()
        app = create_app(
            autenticador_sessao=autenticador,
            verificador_conectividade=verificador,
        )

        status_health, corpo_health = await _requisitar_asgi(app, "GET", "/health")
        status_ready, corpo_ready = await _requisitar_asgi(app, "GET", "/ready")

        self.assertEqual(status_health, 200)
        self.assertEqual(corpo_health, {"status": "ok"})
        self.assertEqual(status_ready, 200)
        self.assertEqual(corpo_ready, {"status": "ready"})


if __name__ == "__main__":
    unittest.main()
