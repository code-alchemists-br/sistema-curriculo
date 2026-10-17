"""Verifica o adaptador SQLAlchemy da porta de readiness."""

import unittest
from unittest.mock import AsyncMock, Mock

from backend.infrastructure.persistence.sqlalchemy.verificador_persistencia import (
    VerificadorPersistenciaSqlalchemy,
)


class VerificadorPersistenciaSqlalchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Testa a consulta mínima do adaptador sem abrir conexões reais."""

    async def test_retorna_true_quando_a_consulta_de_conectividade_responde(self) -> None:
        """Confirma sucesso quando o banco devolve o resultado esperado.

        O cenário substitui engine e conexão por doubles e verifica o retorno de
        `SELECT 1`. Ele existe para proteger o contrato usado pela rota ready.
        """
        engine, conexao = _engine_com_resultado(1)

        resultado = await VerificadorPersistenciaSqlalchemy(engine).verificar()

        self.assertTrue(resultado)
        conexao.scalar.assert_awaited_once()
        self.assertEqual(str(conexao.scalar.await_args.args[0]), "SELECT 1")

    async def test_retorna_false_quando_a_consulta_nao_confirma_conexao(self) -> None:
        """Não declara disponibilidade quando a consulta não retorna 1.

        O double devolve um valor inesperado sem levantar exceção. O cenário
        existe para garantir que readiness só aceite a resposta definida pelo
        adaptador como sucesso.
        """
        engine, _ = _engine_com_resultado(0)

        resultado = await VerificadorPersistenciaSqlalchemy(engine).verificar()

        self.assertFalse(resultado)


def _engine_com_resultado(resultado: int) -> tuple[Mock, Mock]:
    """Cria doubles de engine e conexão assíncronas para os testes.

    A função monta um gerenciador de contexto assíncrono com `scalar` controlado
    e devolve ambos para asserções. Ela existe para testar o adapter sem rede ou
    banco de dados externos.
    """
    conexao = Mock()
    conexao.scalar = AsyncMock(return_value=resultado)
    contexto = AsyncMock()
    contexto.__aenter__.return_value = conexao
    engine = Mock()
    engine.connect.return_value = contexto
    return engine, conexao
