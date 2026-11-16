"""Protege a composição de idiomas com doubles, sem conexão a banco.

Carrega a entrada ASGI isoladamente e observa os argumentos da factory para
impedir que uma rota implementada continue indisponível por falta de injeção.
"""

import importlib.util
import unittest
from unittest.mock import Mock, patch

from backend.application.cadastro_idioma import CadastrarIdioma
from backend.infrastructure.identificadores.geradores import GeradorIdiomaIdUuid4
from backend.infrastructure.persistence.sqlalchemy.executor_transacional import (
    ExecutorTransacionalSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_idioma import (
    RepositorioIdiomaSqlAlchemy,
)


class ComposicaoIdiomaTestCase(unittest.TestCase):
    """Confere o binding público da main usando mocks apenas nos limites externos."""

    def test_main_injeta_cadastro_transacional_somente_com_banco(self):
        """Avalia com e sem URL e observa a factory para preservar a política de indisponibilidade."""
        for url in ("", "postgresql+psycopg://localhost/teste"):
            with self.subTest(com_banco=bool(url)):
                spec = importlib.util.find_spec("backend.main")
                modulo = importlib.util.module_from_spec(spec)
                with (
                    patch.dict("os.environ", {"DATABASE_URL": url}),
                    patch("sqlalchemy.ext.asyncio.create_async_engine"),
                    patch("backend.api.factory.create_app") as criar_app,
                ):
                    spec.loader.exec_module(modulo)
                self.assertIn("cadastrar_idioma", criar_app.call_args.kwargs)
                executor = criar_app.call_args.kwargs["cadastrar_idioma"]
                if url:
                    self.assertIsInstance(executor, ExecutorTransacionalSqlAlchemy)
                    self.assertIs(executor._sessoes, modulo._sessoes_persistencia)
                    sessao = Mock()
                    caso = executor._montar_caso_de_uso(sessao)
                    self.assertIsInstance(caso, CadastrarIdioma)
                    self.assertIsInstance(
                        caso._repositorio, RepositorioIdiomaSqlAlchemy
                    )
                    self.assertIs(caso._repositorio._session, sessao)
                    self.assertIsInstance(caso._gerador_id, GeradorIdiomaIdUuid4)
                else:
                    self.assertIsNone(executor)
