"""Protege o executor transacional genérico, sem banco real."""

import unittest
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.infrastructure.persistence.sqlalchemy.executor_transacional import (
    ExecutorTransacionalSqlAlchemy,
    criar_executor_transacional,
)


class SessoesFalsas:
    """Simula a fábrica de sessões registrando confirmação e reversão.

    A classe devolve a si mesma em ``begin`` e anota, na saída do contexto, se
    houve confirmação ou reversão. Ela existe para observar o comportamento
    transacional sem abrir conexão.
    """

    def __init__(self) -> None:
        """Cria a sessão sentinela e zera os indicadores de transação."""
        self.sessao = object()
        self.confirmou = False
        self.reverteu = False

    def begin(self) -> "SessoesFalsas":
        """Devolve o próprio objeto como contexto transacional."""
        return self

    async def __aenter__(self) -> object:
        """Entrega a sessão sentinela ao executor."""
        return self.sessao

    async def __aexit__(self, tipo: object, valor: object, retorno: object) -> bool:
        """Registra confirmação sem exceção e reversão com exceção."""
        if tipo is None:
            self.confirmou = True
        else:
            self.reverteu = True
        return False


class CasoDeUsoFalso:
    """Simula um caso de uso que devolve a entrada dobrada ou falha.

    A classe guarda a sessão recebida e a entrada executada. Ela existe para
    provar que o executor monta o caso com a sessão e delega a execução.
    """

    def __init__(self, sessao: object, falhar: bool = False) -> None:
        """Guarda a sessão recebida e se deve falhar ao executar."""
        self.sessao = sessao
        self.falhar = falhar
        self.entradas: list[int] = []

    async def executar(self, entrada: int) -> int:
        """Registra a entrada e devolve o dobro, ou levanta erro se configurado."""
        self.entradas.append(entrada)
        if self.falhar:
            raise ValueError("falha simulada")
        return entrada * 2


class ExecutorTransacionalTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a delegação e o controle de transação do executor genérico.

    A classe usa fábrica e caso de uso falsos para observar sessão, resultado e
    confirmação. Ela existe para proteger o mecanismo compartilhado por todas as
    rotas ligadas ao banco.
    """

    async def test_monta_caso_com_a_sessao_devolve_resultado_e_confirma(self) -> None:
        """Entrega a sessão ao caso, devolve o resultado e confirma a transação.

        Executa com entrada 21 e confere resultado 42, sessão repassada e
        confirmação sem reversão. Ele existe para provar o caminho de sucesso.
        """
        sessoes = SessoesFalsas()
        montados: list[CasoDeUsoFalso] = []

        def montar(sessao: AsyncSession) -> CasoDeUsoFalso:
            caso = CasoDeUsoFalso(sessao)
            montados.append(caso)
            return caso

        executor = ExecutorTransacionalSqlAlchemy(
            cast(async_sessionmaker[AsyncSession], sessoes), montar
        )

        resultado = await executor.executar(21)

        self.assertEqual(resultado, 42)
        self.assertIs(montados[0].sessao, sessoes.sessao)
        self.assertTrue(sessoes.confirmou)
        self.assertFalse(sessoes.reverteu)

    async def test_propaga_excecao_e_reverte_a_transacao(self) -> None:
        """Propaga a falha do caso e sinaliza reversão em vez de confirmação.

        Faz o caso falhar e confere a exceção e os indicadores. Ele existe para
        garantir que erro de negócio nunca deixe dados confirmados.
        """
        sessoes = SessoesFalsas()
        executor = ExecutorTransacionalSqlAlchemy(
            cast(async_sessionmaker[AsyncSession], sessoes),
            lambda sessao: CasoDeUsoFalso(sessao, falhar=True),
        )

        with self.assertRaises(ValueError):
            await executor.executar(1)

        self.assertTrue(sessoes.reverteu)
        self.assertFalse(sessoes.confirmou)

    def test_sem_sessoes_nao_cria_executor(self) -> None:
        """Devolve ``None`` quando não há persistência configurada.

        Chama a função de criação sem fábrica de sessões. Ele existe para manter
        a rota indisponível (503) quando o banco não está configurado.
        """
        self.assertIsNone(
            criar_executor_transacional(None, lambda sessao: CasoDeUsoFalso(sessao))
        )
