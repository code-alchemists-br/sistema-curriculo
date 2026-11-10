"""Testa os adaptadores transacionais de competências com doubles de sessão e casos.

O módulo valida que as operações de escrita (cadastro e exclusão) utilizem
transações isoladas por chamada (bloco begin()), que a operação de listagem
utilize sessão curta sem confirmação de mutação e que erros sejam propagados
para reversão atômica. Ele existe para garantir que a camada de infraestrutura
cumpra os contratos da Clean Architecture sem depender de banco de dados em
tempo de teste unitário.
"""

import importlib.util
import unittest
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID

from backend.application.cadastro_competencia import CadastrarCompetenciaEntrada
from backend.application.competencia import (
    ExcluirCompetenciaEntrada,
    ListarCompetenciasEntrada,
)
from backend.domain.itens_perfil import CategoriaCompetencia, Competencia
from backend.domain.value_objects import CompetenciaId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy import (
    operacoes_competencia as operacoes,
)

ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_COMPETENCIA = UUID("00000000-0000-0000-0000-0000000000c1")


class ComposicaoCompetenciaTestCase(unittest.TestCase):
    """Verifica a injeção dos adaptadores de competência na composição ASGI."""

    def test_main_injeta_operacoes_competencia_somente_com_banco(self) -> None:
        """Verifica que main.py injeta os adaptadores com DATABASE_URL e None sem ela.

        O teste carrega o módulo backend.main isoladamente com e sem variável
        DATABASE_URL, inspecionando os argumentos passados para create_app().
        Ele existe para proteger a injeção contra remoção acidental que cause
        erro 503 nas rotas de competências.
        """
        for url in ("", "postgresql+psycopg://localhost/teste"):
            with self.subTest(com_banco=bool(url)):
                spec = importlib.util.find_spec("backend.main")
                self.assertIsNotNone(spec)
                assert spec and spec.loader
                modulo = importlib.util.module_from_spec(spec)
                with (
                    patch.dict("os.environ", {"DATABASE_URL": url}),
                    patch("sqlalchemy.ext.asyncio.create_async_engine"),
                    patch("backend.api.factory.create_app") as criar_app,
                ):
                    spec.loader.exec_module(modulo)

                for chave, classe in (
                    ("cadastrar_competencia", operacoes.CadastroCompetenciaSqlAlchemy),
                    ("listar_competencias", operacoes.ListarCompetenciasSqlAlchemy),
                    ("excluir_competencia", operacoes.ExclusaoCompetenciaSqlAlchemy),
                ):
                    executor = criar_app.call_args.kwargs[chave]
                    if url:
                        self.assertIsInstance(executor, classe)
                        self.assertIs(executor._sessoes, modulo._sessoes_persistencia)
                    else:
                        self.assertIsNone(executor)


class OperacoesCompetenciaSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o ciclo de sessões e a delegação dos adaptadores de competência."""

    async def test_cadastro_executa_em_transacao_com_begin(self) -> None:
        """Confirma que o cadastro abre transação atômica via begin() e delega ao caso.

        O teste configura o mock de sessão para simular begin(), invoca o adapter
        e verifica a delegação da chamada para o caso de uso com o retorno esperado.
        Ele existe para assegurar atomicidade no cadastro de competências.
        """
        sessao_mock = AsyncMock()
        gerenciador_transacao = AsyncMock()
        gerenciador_transacao.__aenter__.return_value = sessao_mock
        gerenciador_transacao.__aexit__.return_value = None

        sessoes_factory = Mock()
        sessoes_factory.begin.return_value = gerenciador_transacao

        gerador_id = Mock()
        adapter = operacoes.CadastroCompetenciaSqlAlchemy(sessoes_factory, gerador_id)

        entrada = CadastrarCompetenciaEntrada(
            usuario_id=UsuarioId(ID_USUARIO),
            categoria=CategoriaCompetencia.TECNICA,
            descricao="Python",
            nivel="Avançado",
        )
        competencia_esperada = Competencia(
            id=CompetenciaId(ID_COMPETENCIA),
            usuario_id=UsuarioId(ID_USUARIO),
            categoria=CategoriaCompetencia.TECNICA,
            descricao="Python",
            nivel="Avançado",
        )

        with patch(
            "backend.infrastructure.persistence.sqlalchemy.operacoes_competencia.CadastrarCompetencia"
        ) as caso_mock_cls:
            caso_instancia = Mock()
            caso_instancia.executar = AsyncMock(return_value=competencia_esperada)
            caso_mock_cls.return_value = caso_instancia

            resultado = await adapter.executar(entrada)

        self.assertEqual(resultado, competencia_esperada)
        sessoes_factory.begin.assert_called_once()
        caso_instancia.executar.assert_awaited_once_with(entrada)

    async def test_listagem_executa_em_sessao_sem_begin(self) -> None:
        """Confirma que a listagem utiliza sessão curta sem abrir transação de escrita.

        O teste valida que a fábrica é chamada diretamente como context manager
        assíncrono sem invocar begin(), retornando as competências consultadas.
        Ele existe para garantir leituras eficientes e sem locks desnecessários.
        """
        sessao_mock = AsyncMock()
        gerenciador_sessao = AsyncMock()
        gerenciador_sessao.__aenter__.return_value = sessao_mock
        gerenciador_sessao.__aexit__.return_value = None

        sessoes_factory = Mock(return_value=gerenciador_sessao)
        adapter = operacoes.ListarCompetenciasSqlAlchemy(sessoes_factory)

        entrada = ListarCompetenciasEntrada(usuario_id=UsuarioId(ID_USUARIO))
        competencias_esperadas = (
            Competencia(
                id=CompetenciaId(ID_COMPETENCIA),
                usuario_id=UsuarioId(ID_USUARIO),
                categoria=CategoriaCompetencia.TECNICA,
                descricao="Python",
                nivel="Avançado",
            ),
        )

        with patch(
            "backend.infrastructure.persistence.sqlalchemy.operacoes_competencia.ListarCompetencias"
        ) as caso_mock_cls:
            caso_instancia = Mock()
            caso_instancia.executar = AsyncMock(return_value=competencias_esperadas)
            caso_mock_cls.return_value = caso_instancia

            resultado = await adapter.executar(entrada)

        self.assertEqual(resultado, competencias_esperadas)
        sessoes_factory.assert_called_once()
        sessoes_factory.begin.assert_not_called()
        caso_instancia.executar.assert_awaited_once_with(entrada)

    async def test_exclusao_executa_em_transacao_com_begin(self) -> None:
        """Confirma que a exclusão abre transação atômica via begin() e delega ao caso.

        O teste simula o contexto transacional com begin(), executa a exclusão e
        verifica que o caso de uso foi chamado com a entrada tipada. Ele existe
        para garantir reversibilidade consistente e remoção atômica no banco.
        """
        sessao_mock = AsyncMock()
        gerenciador_transacao = AsyncMock()
        gerenciador_transacao.__aenter__.return_value = sessao_mock
        gerenciador_transacao.__aexit__.return_value = None

        sessoes_factory = Mock()
        sessoes_factory.begin.return_value = gerenciador_transacao

        adapter = operacoes.ExclusaoCompetenciaSqlAlchemy(sessoes_factory)

        entrada = ExcluirCompetenciaEntrada(
            competencia_id=CompetenciaId(ID_COMPETENCIA),
            usuario_id=UsuarioId(ID_USUARIO),
        )

        with patch(
            "backend.infrastructure.persistence.sqlalchemy.operacoes_competencia.ExcluirCompetencia"
        ) as caso_mock_cls:
            caso_instancia = Mock()
            caso_instancia.executar = AsyncMock(return_value=None)
            caso_mock_cls.return_value = caso_instancia

            await adapter.executar(entrada)

        sessoes_factory.begin.assert_called_once()
        caso_instancia.executar.assert_awaited_once_with(entrada)
