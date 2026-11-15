"""Protege a consulta de proprietário de item, sem banco real."""

import unittest
from typing import Any, cast
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.value_objects import (
    CompetenciaId,
    FormacaoAcademicaId,
    ReferenciaCurriculo,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.consulta_proprietario_item import (
    ConsultaProprietarioItemSqlAlchemy,
)

ITEM = UUID("00000000-0000-4000-8000-0000000000a1")
DONO = UUID("00000000-0000-4000-8000-0000000000b1")


class SessaoFalsa:
    """Simula a sessão devolvendo um valor fixo e guardando a consulta recebida.

    A classe registra o SQL compilado e devolve o proprietário configurado. Ela
    existe para verificar a tabela escolhida e o resultado sem abrir conexão.
    """

    def __init__(self, resultado: UUID | None) -> None:
        """Guarda o valor a devolver e prepara o registro da consulta."""
        self.resultado = resultado
        self.sql: str = ""

    async def scalar(self, consulta: Any) -> UUID | None:
        """Registra o SQL recebido e devolve o resultado configurado."""
        self.sql = str(consulta)
        return self.resultado


class ConsultaProprietarioItemTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica tabela escolhida, devolução do dono e filtro de exclusão lógica.

    A classe usa sessão falsa para observar a consulta gerada. Ela existe para
    proteger a regra de propriedade usada ao selecionar itens de uma versão.
    """

    async def test_devolve_o_dono_quando_o_item_existe(self) -> None:
        """Devolve ``UsuarioId`` do proprietário e consulta a tabela da formação.

        Ele existe para provar a escolha da tabela pelo tipo do identificador e
        a conversão do resultado para o value object.
        """
        sessao = SessaoFalsa(DONO)
        consulta = ConsultaProprietarioItemSqlAlchemy(cast(AsyncSession, sessao))

        dono = await consulta.obter_proprietario(
            ReferenciaCurriculo(FormacaoAcademicaId(ITEM))
        )

        self.assertEqual(dono, UsuarioId(DONO))
        self.assertIn("formacoes_academicas", sessao.sql)
        self.assertIn("deleted_at IS NULL", sessao.sql)

    async def test_devolve_none_quando_o_item_nao_existe(self) -> None:
        """Devolve ``None`` se a tabela não tem o item (ou ele foi excluído).

        Ele existe para que a seleção recuse itens ausentes.
        """
        sessao = SessaoFalsa(None)
        consulta = ConsultaProprietarioItemSqlAlchemy(cast(AsyncSession, sessao))

        dono = await consulta.obter_proprietario(
            ReferenciaCurriculo(CompetenciaId(ITEM))
        )

        self.assertIsNone(dono)
        self.assertIn("competencias", sessao.sql)
        self.assertNotIn("deleted_at", sessao.sql)
