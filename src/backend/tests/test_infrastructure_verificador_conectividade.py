"""Testa unitariamente a verificação de conectividade SQLAlchemy."""

import unittest

from backend.infrastructure.persistence.sqlalchemy.verificador_conectividade import (
    VerificadorConectividadePersistenciaSqlAlchemy,
)

# Proveniência: decision-analysis prompts/backend/20261014-175641-health-readiness-checks-v001.md#v001


class AsyncSessionSpy:
    """Substitui a AsyncSession do SQLAlchemy para testes da sonda de conectividade.

    O double intercepta a execução de queries SQL e permite simular sucesso ou
    lançamento de falha de conexão sem abrir sockets com banco de dados real. Ele
    existe para isolar os testes do adaptador de persistência.
    """

    def __init__(self, falhar: bool = False) -> None:
        """Armazena a política de sucesso ou falha para as chamadas de execute.

        O construtor registra se a sessão simulada deve prosseguir normalmente ou
        levantar erro operacional. Ele existe para parametrizar cenários de persistência.
        """
        self.falhar = falhar
        self.consultas: list[str] = []

    async def execute(self, statement, *args, **kwargs):
        """Registra a consulta SQL submetida e devolve resultado ou levanta exceção.

        O método simula a corrotina execute da AsyncSession sem dependência de I/O.
        Ele existe para validar se a instrução enviada corresponde ao teste esperado.
        """
        self.consultas.append(str(statement))
        if self.falhar:
            raise RuntimeError("Falha de conexão com o banco de dados")
        return None


class VerificadorConectividadeSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica unitariamente o comportamento do adaptador de prontidão com SQLAlchemy."""

    async def test_checar_conectividade_retorna_true_quando_query_tem_sucesso(
        self,
    ) -> None:
        """Confirma retorno True e execução de query leve quando a sessão responde.

        O teste submete a verificação de conectividade a uma sessão saudável e
        confirma que o resultado é verdadeiro e que 'SELECT 1' foi executado.
        """
        sessao = AsyncSessionSpy(falhar=False)
        verificador = VerificadorConectividadePersistenciaSqlAlchemy(sessao)  # type: ignore

        conectado = await verificador.checar_conectividade()

        self.assertTrue(conectado)
        self.assertEqual(len(sessao.consultas), 1)
        self.assertIn("SELECT 1", sessao.consultas[0])

    async def test_checar_conectividade_retorna_false_quando_query_lanca_excecao(
        self,
    ) -> None:
        """Confirma retorno False sem vazamento de exceção quando o banco falha.

        O teste simula indisponibilidade de banco de dados e valida que o adaptador
        captura a falha de persistência e reporta False de forma segura.
        """
        sessao = AsyncSessionSpy(falhar=True)
        verificador = VerificadorConectividadePersistenciaSqlAlchemy(sessao)  # type: ignore

        conectado = await verificador.checar_conectividade()

        self.assertFalse(conectado)
        self.assertEqual(len(sessao.consultas), 1)


if __name__ == "__main__":
    unittest.main()
