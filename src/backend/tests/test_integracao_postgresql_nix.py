"""Valida a disponibilidade do PostgreSQL efêmero no ambiente de integração."""

import os
import unittest

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


class PostgreSqlNixIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Confirma o contrato de conexão do PostgreSQL oferecido pelo shell Nix.

    O caso usa a URL temporária preparada pelo executor, conecta pelo driver
    assíncrono e consulta o banco criado para a execução. Ele existe para
    impedir que a CI sinalize integração verde sem disponibilizar um servidor
    PostgreSQL funcional para os testes que dependem dele.
    """

    async def test_conecta_ao_banco_temporario_exposto_pelo_executor(self) -> None:
        """Consulta o banco efêmero usando a URL fornecida pelo executor.

        O cenário cria uma engine assíncrona, verifica o nome do banco atual e
        sempre libera a conexão ao finalizar. Ele existe para validar servidor,
        socket e driver PostgreSQL juntos, antes dos cenários de persistência.
        """
        database_url = os.environ.get("DATABASE_URL")
        self.assertIsNotNone(database_url)
        assert database_url is not None
        engine = create_async_engine(database_url)
        self.addAsyncCleanup(engine.dispose)

        async with engine.connect() as connection:
            database_name = await connection.scalar(text("SELECT current_database()"))

        self.assertEqual(database_name, "sistema_curriculo_test")
