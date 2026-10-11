"""Registra a lacuna de autenticação da listagem real de currículos.

Os casos são um relatório de lacuna de RF13, não cobertura de mecanismo
integrado. Na composição ASGI atual, a ausência de executor gera HTTP 503.
"""

import unittest

from fastapi.testclient import TestClient

from backend.main import app


# Proveniência: decision-analysis prompts/backend/20261011-102943-rejeicao-requisicoes-sem-credenciais-validas-v004.md#v004
_CAMINHO_LISTAGEM_CURRICULOS = "/estudantes/00000000-0000-4000-8000-000000000001/curriculos"
_CAMPOS_PRIVADOS_CURRICULO = {"versoes", "titulo_versao", "layout", "is_public", "total_itens"}


class RejeicaoSemCredenciaisValidasTestCase(unittest.TestCase):
    """Exercita a listagem real e registra os estados de RF13 ainda ausentes.

    Os métodos usam TestClient sem overrides, marcando ausência/cookie inválido
    como falhas esperadas estritas e sessões sem validador como skips. A classe
    existe para deixar a lacuna observável sem simular autenticação de produto.
    """

    def _assert_requisicao_rejeitada(self, cookie: str | None) -> None:
        """Verifica o status e o corpo observáveis da requisição à listagem.

        O helper chama a app ASGI real via TestClient, inspeciona status e campos
        privados previstos pelo DTO da rota e centraliza o oráculo HTTP dos
        quatro casos para que cada estado tenha exatamente as mesmas asserções.
        """
        cabecalhos = {} if cookie is None else {"Cookie": cookie}
        with TestClient(app) as cliente:
            resposta = cliente.get(_CAMINHO_LISTAGEM_CURRICULOS, headers=cabecalhos)

        corpo = resposta.json()
        if isinstance(corpo, dict):
            campos_encontrados = _CAMPOS_PRIVADOS_CURRICULO.intersection(corpo)
        elif corpo:
            campos_encontrados = set(_CAMPOS_PRIVADOS_CURRICULO)
        else:
            campos_encontrados = set()

        status_correto = resposta.status_code == 401
        corpo_sem_dados_privados = not campos_encontrados
        self.assertTrue(
            status_correto and corpo_sem_dados_privados,
            "Esperava HTTP 401 sem campos privados de currículo; "
            f"recebeu status={resposta.status_code}, "
            f"campos={sorted(campos_encontrados)}",
        )

    @unittest.expectedFailure
    def test_sem_cookie(self) -> None:
        """RF13 não implementada: ausência de cookie deve retornar 401 sem dados.

        O teste envia uma requisição sem cabeçalho Cookie e aplica as asserções
        do oráculo da listagem real. expectedFailure do unittest falha a suíte se
        o caso passar inesperadamente, funcionando como xfail estrito.
        """
        self._assert_requisicao_rejeitada(cookie=None)

    @unittest.expectedFailure
    def test_cookie_invalido(self) -> None:
        """RF13 não implementada: cookie inválido deve retornar 401 sem dados.

        O teste envia um valor sintético inválido sem alegar que seu nome seja o
        cookie definitivo. expectedFailure do unittest falha a suíte se o caso
        passar inesperadamente, funcionando como xfail estrito.
        """
        self._assert_requisicao_rejeitada(cookie="sessao=credencial-invalida")

    @unittest.skip("validador de sessão não existe")
    def test_sessao_expirada(self) -> None:
        """Reserva o estado expirado até existir um validador de sessão.

        O teste envia um cookie sintético à rota real e conserva o mesmo oráculo
        401/sem dados para futura ativação. O skip informa a lacuna atual sem
        simular comportamento que o backend ainda não implementa.
        """
        self._assert_requisicao_rejeitada(cookie="sessao=credencial-expirada")

    @unittest.skip("validador de sessão não existe")
    def test_sessao_revogada(self) -> None:
        """Reserva o estado revogado até existir um validador de sessão.

        O teste envia um cookie sintético à rota real e conserva o mesmo oráculo
        401/sem dados para futura ativação. O skip informa a lacuna atual sem
        simular comportamento que o backend ainda não implementa.
        """
        self._assert_requisicao_rejeitada(cookie="sessao=credencial-revogada")
