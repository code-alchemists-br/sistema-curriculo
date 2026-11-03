"""Testa o adaptador transacional do cadastro de estudante."""

import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch

from backend.application.cadastro_estudante import CadastrarEstudanteEntrada
from backend.infrastructure.persistence.sqlalchemy.cadastro_estudante import (
    CadastroEstudanteSqlAlchemy,
)


class CadastroEstudanteSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Garante o limite transacional externo do caso de uso de cadastro.

    Os cenários substituem sessão, repositório e caso de uso por doubles para
    observar somente a composição do adapter. A classe existe para evitar que
    a aplicação execute cadastro com sessão global ou sem confirmação atômica.
    """

    async def test_executa_caso_de_uso_em_sessao_transacional_por_requisicao(
        self,
    ) -> None:
        """Abre transação, monta as dependências e devolve o usuário persistido.

        O cenário configura o contexto assíncrono de uma fábrica de sessões e
        confirma a delegação da entrada ao caso de uso. Ele existe para provar
        que a infraestrutura controla a transação sem mover regra de negócio
        para o adapter.
        """
        sessao = Mock()
        transacao = MagicMock()
        transacao.__aenter__ = AsyncMock(return_value=sessao)
        transacao.__aexit__ = AsyncMock(return_value=False)
        sessoes = Mock()
        sessoes.begin.return_value = transacao
        gerador = Mock()
        entrada = Mock(spec=CadastrarEstudanteEntrada)
        usuario = Mock()
        repositorio = Mock()
        caso_de_uso = Mock()
        caso_de_uso.executar = AsyncMock(return_value=usuario)

        with (
            patch(
                "backend.infrastructure.persistence.sqlalchemy.cadastro_estudante.RepositorioUsuarioSqlAlchemy",
                return_value=repositorio,
            ) as criar_repositorio,
            patch(
                "backend.infrastructure.persistence.sqlalchemy.cadastro_estudante.CadastrarEstudante",
                return_value=caso_de_uso,
            ) as criar_caso_de_uso,
        ):
            adapter = CadastroEstudanteSqlAlchemy(sessoes, gerador)
            resultado = await adapter.executar(entrada)

        self.assertIs(resultado, usuario)
        sessoes.begin.assert_called_once_with()
        criar_repositorio.assert_called_once_with(sessao)
        criar_caso_de_uso.assert_called_once_with(repositorio, gerador)
        caso_de_uso.executar.assert_awaited_once_with(entrada)
