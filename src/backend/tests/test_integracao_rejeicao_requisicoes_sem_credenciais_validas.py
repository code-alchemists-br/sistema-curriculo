"""Registra a lacuna de autenticação da listagem real de currículos.

Os casos são um relatório de lacuna de RF13, não cobertura de mecanismo
integrado. A composição ASGI atual não declara autenticação e retorna HTTP 503
quando o executor de listagem não está configurado.
"""

import json
import unittest

from backend.main import app

# Proveniência: decision-analysis prompts/backend/20261011-102943-rejeicao-requisicoes-sem-credenciais-validas-v004.md#v004
_CAMINHO_LISTAGEM_CURRICULOS = "/estudantes/00000000-0000-4000-8000-000000000001/curriculos"
_CAMPOS_PRIVADOS_CURRICULO = {"versoes", "titulo_versao", "layout", "is_public", "total_itens"}


class RejeicaoSemCredenciaisValidasTestCase(unittest.IsolatedAsyncioTestCase):
    """Exercita a listagem real e registra os estados de RF13 ainda ausentes.

    Os métodos chamam a interface ASGI sem overrides, marcando ausência/cookie
    inválido como falhas esperadas estritas e estados não validáveis como skips.
    A classe existe para tornar a lacuna observável sem simular autenticação.
    """

    async def _solicitar_app_asgi(self, cookie: str | None) -> tuple[int, object]:
        """Envia GET diretamente à app ASGI e decodifica status e JSON.

        O helper fornece scope HTTP, corpo vazio e coleciona eventos em memória,
        sem abrir socket nem importar um cliente externo. Ele existe para testar
        o roteamento real sem exigir httpx ou httpx2.
        """
        cabecalhos = [(b"host", b"testserver")]
        if cookie is not None:
            cabecalhos.append((b"cookie", cookie.encode("ascii")))

        escopo: dict[str, object] = {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.3"},
            "http_version": "1.1",
            "method": "GET",
            "scheme": "http",
            "path": _CAMINHO_LISTAGEM_CURRICULOS,
            "raw_path": _CAMINHO_LISTAGEM_CURRICULOS.encode("ascii"),
            "query_string": b"",
            "root_path": "",
            "headers": cabecalhos,
            "client": ("testclient", 50000),
            "server": ("testserver", 80),
            "state": {},
        }
        eventos_resposta: list[dict[str, object]] = []
        requisicao_entregue = False

        async def receber() -> dict[str, object]:
            """Entrega o GET vazio uma vez e sinaliza disconnect em seguida.

            A sequência fornece os eventos de entrada mínimos exigidos pelo
            protocolo ASGI. Ela existe para que a aplicação real possa completar
            a resposta dentro do harness em memória.
            """
            nonlocal requisicao_entregue
            if requisicao_entregue:
                return {"type": "http.disconnect"}
            requisicao_entregue = True
            return {"type": "http.request", "body": b"", "more_body": False}

        async def enviar(evento: dict[str, object]) -> None:
            """Armazena um evento de resposta emitido pela aplicação ASGI.

            Os eventos permanecem em memória para que o helper leia o status e
            o corpo HTTP reais. A função existe para substituir somente o
            transporte de rede, não o app ou suas rotas.
            """
            eventos_resposta.append(evento)

        await app(escopo, receber, enviar)  # type: ignore[arg-type]
        inicio = next(evento for evento in eventos_resposta if evento.get("type") == "http.response.start")
        partes_corpo = [
            evento.get("body", b"")
            for evento in eventos_resposta
            if evento.get("type") == "http.response.body" and isinstance(evento.get("body", b""), bytes)
        ]
        corpo = json.loads(b"".join(partes_corpo))
        return int(inicio["status"]), corpo

    async def _assert_requisicao_rejeitada(self, cookie: str | None) -> None:
        """Aplica o oráculo 401/sem dados ao resultado da rota real.

        O helper inspeciona status e campos do DTO de currículo e avalia ambas
        as condições antes de falhar. Ele existe para reaproveitar o mesmo
        oráculo nos quatro estados de credenciais sem criar endpoints auxiliares.
        """
        status, corpo = await self._solicitar_app_asgi(cookie)
        if isinstance(corpo, dict):
            campos_encontrados = _CAMPOS_PRIVADOS_CURRICULO.intersection(corpo)
        elif corpo:
            campos_encontrados = set(_CAMPOS_PRIVADOS_CURRICULO)
        else:
            campos_encontrados = set()

        status_correto = status == 401
        corpo_sem_dados_privados = not campos_encontrados
        self.assertTrue(
            status_correto and corpo_sem_dados_privados,
            "Esperava HTTP 401 sem campos privados de currículo; "
            f"recebeu status={status}, campos={sorted(campos_encontrados)}",
        )

    @unittest.expectedFailure
    async def test_sem_cookie(self) -> None:
        """RF13 não implementada: ausência de cookie deve retornar 401 sem dados.

        O teste faz GET à app ASGI real sem cabeçalho Cookie. expectedFailure
        produz falha esperada e uma aprovação inesperada falha a suíte, mantendo
        o comportamento estrito equivalente ao xfail solicitado.
        """
        await self._assert_requisicao_rejeitada(cookie=None)

    @unittest.expectedFailure
    async def test_cookie_invalido(self) -> None:
        """RF13 não implementada: cookie inválido deve retornar 401 sem dados.

        O teste envia um valor sintético à app real sem afirmar que seu nome seja
        o cookie definitivo. expectedFailure falha a suíte se o oráculo passar
        inesperadamente, mantendo estrita a expectativa de lacuna.
        """
        await self._assert_requisicao_rejeitada(cookie="sessao=credencial-invalida")

    @unittest.skip("validador de sessão não existe")
    async def test_sessao_expirada(self) -> None:
        """Reserva o estado expirado enquanto não existe validador de sessão.

        O método conserva o mesmo oráculo para quando a API puder reconhecer a
        expiração. O skip registra a limitação sem simular comportamento ausente.
        """
        await self._assert_requisicao_rejeitada(cookie="sessao=credencial-expirada")

    @unittest.skip("validador de sessão não existe")
    async def test_sessao_revogada(self) -> None:
        """Reserva o estado revogado enquanto não existe validador de sessão.

        O método conserva o mesmo oráculo para quando a API puder reconhecer a
        revogação. O skip registra a limitação sem simular comportamento ausente.
        """
        await self._assert_requisicao_rejeitada(cookie="sessao=credencial-revogada")
