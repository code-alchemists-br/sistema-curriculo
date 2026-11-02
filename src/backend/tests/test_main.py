"""Verifica a composição de recursos da aplicação ASGI."""

import unittest
from unittest.mock import AsyncMock, Mock, patch

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.main import (
    _ciclo_vida_aplicacao,
    _configurar_cors,
    _criar_cadastrar_estudante,
    _criar_configuracao_cookie_sessao,
    _criar_engine_persistencia,
    _obter_origens_cors,
)


class ComposicaoAplicacaoTestCase(unittest.TestCase):
    """Protege a configuração da engine usada pela readiness."""

    def test_nao_cria_engine_sem_url_de_persistencia(self) -> None:
        """Mantém o probe ausente quando o ambiente não define DATABASE_URL.

        O teste chama a fábrica com valor ausente e confirma que nenhum engine
        é criado. Ele existe para que ambientes locais sem banco continuem
        iniciando com readiness fechada.
        """
        with patch("backend.main.create_async_engine") as criar_engine:
            resultado = _criar_engine_persistencia(None)

        self.assertIsNone(resultado)
        criar_engine.assert_not_called()

    def test_normaliza_url_postgresql_e_define_limite_de_conexao(self) -> None:
        """Usa Psycopg assíncrono e timeout ao criar a engine PostgreSQL.

        O teste substitui o construtor do SQLAlchemy e verifica URL e opções
        passadas pela composição. Ele existe para garantir compatibilidade com
        a estratégia assíncrona de persistência documentada.
        """
        engine = Mock()
        with patch(
            "backend.main.create_async_engine", return_value=engine
        ) as criar_engine:
            resultado = _criar_engine_persistencia(
                "postgresql://usuario:senha@localhost/curriculo"
            )

        self.assertIs(resultado, engine)
        url = criar_engine.call_args.args[0]
        self.assertEqual(url.drivername, "postgresql+psycopg")
        self.assertTrue(criar_engine.call_args.kwargs["pool_pre_ping"])
        self.assertEqual(
            criar_engine.call_args.kwargs["connect_args"],
            {"connect_timeout": 2},
        )

    def test_compoe_cadastro_transacional_somente_com_engine_de_persistencia(
        self,
    ) -> None:
        """Injeta sessão e gerador no adapter somente quando há banco configurado.

        O cenário substitui a fábrica SQLAlchemy e o adapter para conferir as
        dependências compostas sem abrir conexão. Ele existe para impedir que a
        aplicação executada volte a expor cadastro indisponível apesar de uma
        `DATABASE_URL` válida.
        """
        engine = Mock()
        gerador = Mock()
        sessoes = Mock()
        executor = Mock()

        with (
            patch("backend.main.async_sessionmaker", return_value=sessoes) as criar_sessoes,
            patch(
                "backend.main.CadastroEstudanteSqlAlchemy",
                return_value=executor,
            ) as criar_executor,
        ):
            resultado = _criar_cadastrar_estudante(engine, gerador)

        self.assertIs(resultado, executor)
        criar_sessoes.assert_called_once_with(engine, expire_on_commit=False)
        criar_executor.assert_called_once_with(sessoes, gerador)
        self.assertIsNone(_criar_cadastrar_estudante(None))

    def test_configura_cors_local_por_padrao_e_origens_explicitas_por_ambiente(
        self,
    ) -> None:
        """Restringe CORS ao Vite local ou à lista declarada pelo ambiente.

        O cenário lê os dois modos de configuração e inspeciona o middleware
        instalado em uma aplicação isolada. Ele existe para impedir que o
        frontend em outra porta seja bloqueado ou que CORS seja aberto a todas
        as origens por acidente.
        """
        self.assertEqual(
            _obter_origens_cors(None),
            ("http://127.0.0.1:5173", "http://localhost:5173"),
        )
        origens = _obter_origens_cors(
            " https://app.example.test, http://localhost:4173 ,,"
        )
        self.assertEqual(
            origens,
            ("https://app.example.test", "http://localhost:4173"),
        )

        aplicacao = FastAPI()
        _configurar_cors(aplicacao, origens)

        middleware = aplicacao.user_middleware[0]
        self.assertIs(middleware.cls, CORSMiddleware)
        self.assertEqual(middleware.kwargs["allow_origins"], list(origens))
        self.assertTrue(middleware.kwargs["allow_credentials"])

    def test_cookie_de_sessao_exige_https_salvo_em_desenvolvimento_explicito(self) -> None:
        """Mantém cookie Host seguro por padrão e libera HTTP apenas por opt-in.

        O cenário exercita valores ausente, inesperado e ``false`` sem alterar
        o ambiente do processo. Ele existe para evitar que desenvolvimento
        local torne produção insegura e para permitir testes HTTP deliberados.
        """
        self.assertTrue(_criar_configuracao_cookie_sessao(None).seguro)
        self.assertTrue(_criar_configuracao_cookie_sessao("qualquer").seguro)
        configuracao_local = _criar_configuracao_cookie_sessao("false")
        self.assertFalse(configuracao_local.seguro)
        self.assertEqual(configuracao_local.nome, "sessao")


class CicloVidaAplicacaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o encerramento de recursos externos da aplicação."""

    async def test_descarta_engine_ao_encerrar_lifespan(self) -> None:
        """Libera a engine ao fim do contexto ASGI.

        O teste injeta uma engine com `dispose` assíncrono e encerra o lifespan.
        Ele existe para evitar pools de conexão abertos após o shutdown.
        """
        engine = Mock()
        engine.dispose = AsyncMock()

        with patch("backend.main._engine_persistencia", engine):
            async with _ciclo_vida_aplicacao(Mock()):
                pass

        engine.dispose.assert_awaited_once()
