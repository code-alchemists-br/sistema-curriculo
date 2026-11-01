"""Valida a disponibilidade do PostgreSQL efêmero no ambiente de integração."""

import os
import unittest

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from backend.tests.fixtures.credenciais_sessao import solicitar_asgi


@unittest.skipUnless(
    os.environ.get("DATABASE_URL"),
    "Requer DATABASE_URL fornecida pelo executor de integração PostgreSQL.",
)
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

    async def test_aplicacao_composta_cadastra_conta_e_recusa_email_duplicado(
        self,
    ) -> None:
        """Exercita o cadastro da aplicação real contra PostgreSQL migrado.

        O cenário importa a aplicação somente após o executor definir a URL,
        envia duas requisições HTTP ASGI pela rota pública e repete o e-mail.
        Ele existe para impedir que o cadastro volte a receber dependências
        ausentes ou responda sucesso sem persistir a conta.
        """
        from backend.main import app

        dados = {
            "nome": "Ana Integração",
            "email": "ana.integracao@example.test",
            "senha": "Senha-Integracao-123",
        }
        primeira = await solicitar_asgi(app, "POST", "/estudantes", dados=dados)
        repetida = await solicitar_asgi(app, "POST", "/estudantes", dados=dados)

        self.assertEqual(primeira.status, 201)
        self.assertEqual(repetida.status, 409)
