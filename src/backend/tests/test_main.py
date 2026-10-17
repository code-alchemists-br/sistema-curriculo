"""Verifica a composição de recursos da aplicação ASGI."""

import unittest
from unittest.mock import AsyncMock, Mock, patch

from backend.main import _ciclo_vida_aplicacao, _criar_engine_persistencia


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
