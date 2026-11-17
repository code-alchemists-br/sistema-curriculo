"""Protege a revogação transacional de sessão no logout, sem banco real."""

import hashlib
import unittest
from typing import Any, cast

from sqlalchemy.ext.asyncio import async_sessionmaker

from backend.infrastructure.persistence.sqlalchemy.acesso_estudante import (
    RevogadorSessaoSqlAlchemy,
)

TOKEN = "token-de-teste"


class SessaoFalsa:
    """Simula a sessão SQLAlchemy registrando o comando de revogação.

    A classe guarda o SQL compilado com seus parâmetros e conta as descargas.
    Ela existe para observar o hash e a tabela atingidos sem abrir conexão.
    """

    def __init__(self) -> None:
        """Prepara o registro dos comandos executados."""
        self.comandos: list[Any] = []
        self.descargas = 0

    async def execute(self, comando: Any) -> None:
        """Guarda o comando recebido."""
        self.comandos.append(comando)

    async def flush(self) -> None:
        """Conta a descarga solicitada pelo repositório."""
        self.descargas += 1


class SessoesFalsas:
    """Simula a fábrica de sessões registrando confirmação e reversão.

    A classe devolve a si mesma em ``begin`` e anota, na saída do contexto, se
    houve confirmação ou reversão. Ela existe para provar que o logout roda em
    uma transação confirmada.
    """

    def __init__(self) -> None:
        """Cria a sessão falsa e zera os indicadores de transação."""
        self.sessao = SessaoFalsa()
        self.confirmou = False
        self.reverteu = False

    def begin(self) -> "SessoesFalsas":
        """Devolve o próprio objeto como contexto transacional."""
        return self

    async def __aenter__(self) -> SessaoFalsa:
        """Entrega a sessão falsa ao adapter."""
        return self.sessao

    async def __aexit__(self, tipo: object, valor: object, retorno: object) -> bool:
        """Registra confirmação sem exceção e reversão com exceção."""
        if tipo is None:
            self.confirmou = True
        else:
            self.reverteu = True
        return False


class RevogadorSessaoSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a revogação por hash dentro de uma transação confirmada.

    A classe usa fábrica e sessão falsas para observar o comando emitido. Ela
    existe para proteger o logout que invalida a sessão no banco.
    """

    async def test_revoga_pelo_hash_do_token_e_confirma_a_transacao(self) -> None:
        """Emite uma atualização na tabela de sessões e confirma a transação.

        Ele existe para provar que o segredo em claro não chega ao banco, só o
        resumo SHA-256, e que a escrita é confirmada.
        """
        sessoes = SessoesFalsas()
        revogador = RevogadorSessaoSqlAlchemy(
            cast(async_sessionmaker, sessoes)  # type: ignore[type-arg]
        )

        await revogador.revogar(TOKEN)

        self.assertTrue(sessoes.confirmou)
        self.assertFalse(sessoes.reverteu)
        self.assertEqual(len(sessoes.sessao.comandos), 1)
        comando = sessoes.sessao.comandos[0]
        valores = comando.compile().params
        hash_esperado = hashlib.sha256(TOKEN.encode("utf-8")).hexdigest()
        self.assertIn(hash_esperado, valores.values())
        self.assertNotIn(TOKEN, valores.values())
        self.assertIn("UPDATE", str(comando))
