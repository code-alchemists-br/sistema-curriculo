"""Caracteriza a composição ASGI exportada sem conectar a banco externo.

Executa a aplicação original em processo isolado e reserva o fluxo autenticado
ausente como ignorado por produto, distinguindo fallback de autenticação real.
"""

# Proveniência: decision-analysis prompts/backend/20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md#v001

import asyncio
import json
import os
import sys
import unittest

from backend.api.middleware_autenticacao import MiddlewareAutenticacaoSessao
from backend.infrastructure.security.autenticador_sessao_indisponivel import (
    AutenticadorSessaoIndisponivel,
)
from backend.tests.fixtures.credenciais_sessao import (
    RAIZ,
    SENHA_SINTETICA,
    USUARIO_A,
    solicitar_asgi,
    token_sintetico,
)


async def caracterizar_em_processo_isolado() -> dict:
    """Importa a app original sem DATABASE_URL e reúne observações redigidas.

    Remove a variável antes do import, usa lifespan e restaura o ambiente em
    finally para caracterizar o fallback sem overrides, banco externo ou token
    aceito artificialmente. Retorna somente status e comparações booleanas.
    """
    database_anterior = os.environ.pop("DATABASE_URL", None)
    try:
        from backend.main import app

        middleware = [
            item for item in app.user_middleware
            if item.cls is MiddlewareAutenticacaoSessao
        ]
        observacoes = {
            "middleware_unico": len(middleware) == 1,
            "autenticador_fechado": len(middleware) == 1 and isinstance(
                middleware[0].kwargs.get("autenticador"), AutenticadorSessaoIndisponivel
            ),
            "sem_overrides": not app.dependency_overrides,
            "sem_database_url": "DATABASE_URL" not in os.environ,
            "operacoes": {},
        }
        token = token_sintetico(701)
        async with app.router.lifespan_context(app):
            for rotulo, metodo, caminho, parametros, detalhe in (
                ("login", "POST", "/acessos", {
                    "dados": {"email": "a@example.test", "senha": SENHA_SINTETICA},
                }, "Acesso indisponível."),
                ("logout-com-cookie", "DELETE", "/sessao/atual", {"token": token}, "Sessões indisponíveis."),
                ("logout-sem-cookie", "DELETE", "/sessao/atual", {}, None),
                ("rota-privada", "GET", f"/estudantes/{USUARIO_A}", {"token": token}, "Sessão ausente ou inválida."),
            ):
                resposta = await solicitar_asgi(app, metodo, caminho, **parametros)
                dados = {
                    "status": resposta.status,
                    "corpo_correto": resposta.corpo == b"" if detalhe is None else (
                        resposta.json() == {"detail": detalhe}
                    ),
                    "sem_set_cookie": not resposta.cabecalhos("set-cookie"),
                }
                if rotulo == "logout-sem-cookie":
                    cookie = resposta.cookie_sessao()
                    dados["cookie_removido"] = (
                        cookie.value == "" and cookie["max-age"] == "0"
                        and cookie["path"] == "/" and cookie["secure"] is True
                        and cookie["httponly"] is True and cookie["samesite"].lower() == "lax"
                        and cookie["domain"] == ""
                    )
                observacoes["operacoes"][rotulo] = dados
        return observacoes
    finally:
        if database_anterior is None:
            os.environ.pop("DATABASE_URL", None)
        else:
            os.environ["DATABASE_URL"] = database_anterior


class ComposicaoCredenciaisSessaoIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Distingue caracterização do fallback de um fluxo produtivo não composto.

    Isola a importação em subprocesso do mesmo interpretador com ambiente
    filtrado, inclusive se main já estiver carregado com engine no processo pai.
    """

    async def test_C01_composicao_exportada_caracteriza_fallback(self) -> None:
        """C01 caracteriza o fallback atual, não certifica login em produção.

        Exercita main.app original sem overrides em processo sem DATABASE_URL.
        Não certifica autenticação persistida; precisa ser atualizado quando a
        composição for completada. O ambiente do pai permanece intacto e o do
        filho é restaurado no cleanup, sem imprimir cookies ou credenciais.
        """
        database_anterior = os.environ.get("DATABASE_URL")
        ambiente = {
            chave: os.environ[chave]
            for chave in ("PATH", "TMPDIR", "LANG", "LC_ALL")
            if chave in os.environ
        }
        ambiente.update(PYTHONPATH="src", PYTHONDONTWRITEBYTECODE="1")
        processo = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "backend.tests.test_integracao_composicao_credenciais_sessao",
            "--caracterizar-composicao", cwd=RAIZ, env=ambiente,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        try:
            saida, _ = await asyncio.wait_for(processo.communicate(), timeout=60)
        except BaseException:
            if processo.returncode is None:
                processo.kill()
            await processo.wait()
            raise
        self.assertEqual(processo.returncode, 0, "Processo C01 falhou; saída sensível [REDACTED]")
        try:
            observacoes = json.loads(saida)
        except (ValueError, UnicodeError):
            self.fail("Evidência C01 não é JSON válido [REDACTED]")
        with self.subTest(operacao="middleware original", identidade="sem-principal"):
            self.assertTrue(observacoes["middleware_unico"])
            self.assertTrue(observacoes["autenticador_fechado"])
            self.assertTrue(observacoes["sem_overrides"])
            self.assertTrue(observacoes["sem_database_url"])
            self.assertTrue(os.environ.get("DATABASE_URL") == database_anterior, "Ambiente do pai alterado [REDACTED]")
        for rotulo, esperado in (
            ("login", 503), ("logout-com-cookie", 503),
            ("logout-sem-cookie", 204), ("rota-privada", 401),
        ):
            with self.subTest(operacao=rotulo, identidade="não-autenticada"):
                observacao = observacoes["operacoes"][rotulo]
                self.assertEqual(observacao["status"], esperado)
                self.assertTrue(observacao["corpo_correto"])
                if rotulo == "logout-sem-cookie":
                    self.assertTrue(observacao["cookie_removido"])
                else:
                    self.assertTrue(observacao["sem_set_cookie"])

    @unittest.skip("produção não compõe login, criador, revogador nem autenticador persistido")
    async def test_C02_fluxo_autenticado_ignorado_por_produto(self) -> None:
        """C02 registra ignorado-produto, não indisponibilidade do ambiente.

        Reserva a jornada até existir composição produtiva real, sem fabricar
        token aceito, endpoint, override ou expectedFailure para obter aprovação.
        """
        self.fail("C02 exige composição produtiva real antes de retirar o skip")


if __name__ == "__main__":
    if sys.argv[1:] == ["--caracterizar-composicao"]:
        print(json.dumps(asyncio.run(caracterizar_em_processo_isolado())))
    else:
        unittest.main()
