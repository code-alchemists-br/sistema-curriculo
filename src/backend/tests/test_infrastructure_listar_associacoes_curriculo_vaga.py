"""Testa unitariamente a composição SQLAlchemy da consulta de associações."""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
from backend.application.consulta_associacao_curriculo_vaga import (
    ListarAssociacoesCurriculoVagaEntrada,
)
from backend.domain.associacao_curriculo_vaga import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
)
from backend.domain.value_objects import CurriculoId, UsuarioId, VagaId
from backend.infrastructure.persistence.sqlalchemy.listar_associacoes_curriculo_vaga import (
    ListarAssociacoesCurriculoVagaSqlAlchemy,
)


class ListarAssociacoesCurriculoVagaSqlAlchemyTestCase(
    unittest.IsolatedAsyncioTestCase
):
    """Verifica delegação e lifecycle sem abrir banco ou executar ORM real.

    O teste substitui sessão, repositório e caso de uso por doubles e verifica
    abertura e encerramento do contexto. A classe existe para proteger o adapter
    de composição externa isoladamente.
    """

    async def test_abre_sessao_curta_e_delega_entrada_e_resultado(self) -> None:
        """Cria o repository na sessão ativa e fecha a sessão após delegar.

        O cenário substitui o caso de uso e a porta de persistência, confirma os
        argumentos e devolve agregados pré-configurados. Ele existe para
        garantir composição correta sem I/O ou dependência de ORM.
        """
        usuario_id = UsuarioId(UUID(int=101))
        entrada = ListarAssociacoesCurriculoVagaEntrada(
            usuario_id=usuario_id,
            offset=20,
            limit=5,
        )
        resultado = (
            AssociacaoCurriculoVaga(
                CurriculoId(UUID(int=201)),
                VagaId("vaga-1"),
                (ClassificacaoAssociacao.INTERESSE,),
            ),
        )
        sessao = object()
        contexto_sessao = MagicMock()
        contexto_sessao.__aenter__ = AsyncMock(return_value=sessao)
        contexto_sessao.__aexit__ = AsyncMock(return_value=False)
        sessoes = MagicMock(return_value=contexto_sessao)

        with (
            patch(
                "backend.infrastructure.persistence.sqlalchemy."
                "listar_associacoes_curriculo_vaga."
                "RepositorioAssociacaoCurriculoVagaSqlAlchemy"
            ) as repositorio,
            patch(
                "backend.infrastructure.persistence.sqlalchemy."
                "listar_associacoes_curriculo_vaga."
                "ListarAssociacoesCurriculoVaga"
            ) as caso_de_uso,
        ):
            caso_de_uso.return_value.executar = AsyncMock(return_value=resultado)

            resposta = await ListarAssociacoesCurriculoVagaSqlAlchemy(sessoes).executar(
                entrada
            )

        self.assertEqual(resposta, resultado)
        sessoes.assert_called_once_with()
        contexto_sessao.__aenter__.assert_awaited_once_with()
        contexto_sessao.__aexit__.assert_awaited_once()
        repositorio.assert_called_once_with(sessao)
        caso_de_uso.assert_called_once_with(repositorio.return_value)
        caso_de_uso.return_value.executar.assert_awaited_once_with(entrada)
