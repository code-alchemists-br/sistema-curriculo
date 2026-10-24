"""Testa o repositório de decisões sobre recomendações com sessão substituída."""

import unittest
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
from backend.domain import CurriculoId, DecisaoEstudante, DecisaoRecomendacao
from backend.infrastructure.persistence.sqlalchemy.decisao_recomendacao import (
    DecisaoRecomendacaoRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_decisao_recomendacao import (
    RepositorioDecisaoRecomendacaoSqlAlchemy,
)

INSTANTE = datetime(2026, 10, 23, 12, 0, tzinfo=UTC)
OUTRO_INSTANTE = datetime(2026, 10, 24, 8, 30, tzinfo=UTC)


def _sessao() -> MagicMock:
    """Cria uma sessão assíncrona substituída, sem banco.

    A função devolve um mock com a interface de ``AsyncSession`` e as chamadas
    assíncronas aguardáveis. Ela existe para observar o que o repositório pede à
    sessão sem I/O.
    """
    sessao = MagicMock(spec=AsyncSession)
    sessao.get = AsyncMock(return_value=None)
    sessao.flush = AsyncMock()
    sessao.scalars = AsyncMock()
    return sessao


class RepositorioDecisaoRecomendacaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a gravação e a listagem de decisões pelo adapter SQLAlchemy.

    A sessão é substituída por doubles, e os testes observam as chamadas e os
    resultados. A classe existe para proteger a regra de uma decisão por versão e
    código e a ordem estável da listagem.
    """

    async def test_salva_decisao_nova_adicionando_o_registro_e_aguardando_flush(
        self,
    ) -> None:
        """Confirma que, sem decisão anterior, o registro novo é adicionado.

        O teste usa uma sessão que não encontra o par e confere o registro
        adicionado e o flush. Ele existe para o caminho de inserção.
        """
        sessao = _sessao()
        curriculo_id = CurriculoId(uuid4())
        decisao = DecisaoRecomendacao(
            curriculo_id, "PROJETO_AUSENTE", DecisaoEstudante.REJEITADA, INSTANTE
        )

        await RepositorioDecisaoRecomendacaoSqlAlchemy(sessao).salvar(decisao)

        sessao.get.assert_awaited_once_with(
            DecisaoRecomendacaoRegistro, (curriculo_id.valor, "PROJETO_AUSENTE")
        )
        sessao.add.assert_called_once()
        registro = sessao.add.call_args.args[0]
        self.assertEqual(
            (registro.curriculo_id, registro.codigo, registro.decisao, registro.decidida_em),
            (curriculo_id.valor, "PROJETO_AUSENTE", "rejeitada", INSTANTE),
        )
        sessao.flush.assert_awaited_once()

    async def test_decidir_de_novo_atualiza_o_registro_existente(self) -> None:
        """Confirma que uma nova decisão do mesmo par substitui a anterior.

        O teste usa uma sessão que encontra o registro e confere que ele foi
        atualizado, sem novo ``add``. Ele existe para que haja uma só decisão
        por versão e código.
        """
        existente = SimpleNamespace(
            decisao="rejeitada", decidida_em=INSTANTE
        )
        sessao = _sessao()
        sessao.get = AsyncMock(return_value=existente)
        decisao = DecisaoRecomendacao(
            CurriculoId(uuid4()), "PROJETO_AUSENTE", DecisaoEstudante.ACEITA, OUTRO_INSTANTE
        )

        await RepositorioDecisaoRecomendacaoSqlAlchemy(sessao).salvar(decisao)

        self.assertEqual(existente.decisao, "aceita")
        self.assertEqual(existente.decidida_em, OUTRO_INSTANTE)
        sessao.add.assert_not_called()
        sessao.flush.assert_awaited_once()

    async def test_lista_as_decisoes_da_versao_em_ordem_do_codigo(self) -> None:
        """Confirma a consulta filtrada e ordenada e a conversão para o domínio.

        O teste devolve dois registros pela sessão e confere as decisões, além do
        SQL gerado. Ele existe para proteger o filtro por versão e a ordem estável.
        """
        curriculo_id = CurriculoId(uuid4())
        registros = [
            SimpleNamespace(
                curriculo_id=curriculo_id.valor,
                codigo=codigo,
                decisao=decisao,
                decidida_em=INSTANTE,
            )
            for codigo, decisao in (("IDIOMA_AUSENTE", "aceita"), ("PROJETO_AUSENTE", "rejeitada"))
        ]
        sessao = _sessao()
        sessao.scalars = AsyncMock(return_value=MagicMock(all=MagicMock(return_value=registros)))

        resultado = await RepositorioDecisaoRecomendacaoSqlAlchemy(sessao).listar_por_curriculo(
            curriculo_id
        )

        self.assertEqual(
            [(d.codigo, d.decisao) for d in resultado],
            [
                ("IDIOMA_AUSENTE", DecisaoEstudante.ACEITA),
                ("PROJETO_AUSENTE", DecisaoEstudante.REJEITADA),
            ],
        )
        consulta = sessao.scalars.await_args.args[0]
        sql = str(consulta)
        self.assertIn("decisoes_recomendacao.curriculo_id", sql)
        self.assertIn("ORDER BY decisoes_recomendacao.codigo", sql)
        self.assertIn(curriculo_id.valor, set(consulta.compile().params.values()))

    async def test_lista_vazia_quando_nao_ha_decisoes(self) -> None:
        """Confirma que uma versão sem decisões devolve uma tupla vazia.

        O teste faz a sessão devolver nenhum registro. Ele existe para o caso de
        uma revisão ainda sem nenhuma escolha do estudante.
        """
        sessao = _sessao()
        sessao.scalars = AsyncMock(return_value=MagicMock(all=MagicMock(return_value=[])))

        resultado = await RepositorioDecisaoRecomendacaoSqlAlchemy(sessao).listar_por_curriculo(
            CurriculoId(uuid4())
        )

        self.assertEqual(resultado, ())
