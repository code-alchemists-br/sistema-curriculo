"""Protege a leitura de item do perfil por tipo, sem banco real."""

import unittest
from typing import Any, cast
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.value_objects import (
    CompetenciaId,
    FormacaoAcademicaId,
    ReferenciaCurriculo,
)
from backend.infrastructure.persistence.sqlalchemy.competencia import (
    CompetenciaRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.consulta_item_perfil import (
    ConsultaItemPerfilSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.formacao_academica import (
    FormacaoAcademicaRegistro,
)

ITEM = UUID("00000000-0000-4000-8000-0000000000a1")


class SessaoFalsa:
    """Simula a sessão devolvendo um registro fixo e guardando a chamada.

    A classe registra o modelo e a chave pedidos a ``get`` e devolve o valor
    configurado. Ela existe para verificar a tabela escolhida sem abrir conexão.
    """

    def __init__(self, resultado: object | None) -> None:
        """Guarda o valor a devolver e prepara o registro da chamada."""
        self.resultado = resultado
        self.chamada: tuple[Any, Any] | None = None

    async def get(self, modelo: Any, chave: Any) -> object | None:
        """Registra o modelo e a chave recebidos e devolve o resultado."""
        self.chamada = (modelo, chave)
        return self.resultado


class ConsultaItemPerfilTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a escolha do modelo pelo tipo e a ausência do item.

    A classe usa sessão falsa para observar o modelo e a chave consultados. Ela
    existe para proteger a leitura usada pela prévia e pela revisão.
    """

    async def test_consulta_o_modelo_do_tipo_e_a_chave_do_item(self) -> None:
        """Pede à sessão o modelo da formação com a chave do identificador.

        Ele existe para provar que o tipo do identificador decide a tabela.
        """
        sessao = SessaoFalsa(None)
        consulta = ConsultaItemPerfilSqlAlchemy(cast(AsyncSession, sessao))

        await consulta.obter_item(ReferenciaCurriculo(FormacaoAcademicaId(ITEM)))

        self.assertEqual(sessao.chamada, (FormacaoAcademicaRegistro, ITEM))

    async def test_devolve_none_quando_o_registro_nao_existe(self) -> None:
        """Devolve ``None`` se a tabela não tem o item.

        Ele existe para que a prévia descarte referências sem item.
        """
        sessao = SessaoFalsa(None)
        consulta = ConsultaItemPerfilSqlAlchemy(cast(AsyncSession, sessao))

        item = await consulta.obter_item(ReferenciaCurriculo(CompetenciaId(ITEM)))

        self.assertIsNone(item)
        self.assertEqual(sessao.chamada, (CompetenciaRegistro, ITEM))
