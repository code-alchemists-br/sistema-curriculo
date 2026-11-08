"""Protege a ligação do Uvicorn e o ciclo transacional sem banco ou rede.

Usa doubles nos limites externos para verificar injeção, propagação de falhas
e encerramento das transações que tornam os endpoints persistentes.
"""

import importlib.util
import unittest
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID

from backend.infrastructure.identificadores.geradores import (
    GeradorFormacaoAcademicaIdUuid4,
)
from backend.infrastructure.persistence.sqlalchemy import (
    operacoes_formacao_academica as operacoes,
)


class ComposicaoFormacaoTestCase(unittest.TestCase):
    """Carrega o módulo de entrada isolado para conferir seus bindings reais."""

    def test_main_injeta_operacoes_somente_com_banco(self):
        """Avalia main com e sem URL usando mocks para proteger a ligação HTTP."""
        for url in ("", "postgresql+psycopg://localhost/teste"):
            with self.subTest(com_banco=bool(url)):
                spec = importlib.util.find_spec("backend.main")
                modulo = importlib.util.module_from_spec(spec)
                with (
                    patch.dict("os.environ", {"DATABASE_URL": url}),
                    patch("sqlalchemy.ext.asyncio.create_async_engine"),
                    patch("backend.api.factory.create_app") as criar_app,
                ):
                    spec.loader.exec_module(modulo)
                for nome, classe in (
                    ("cadastrar", operacoes.CadastroFormacaoAcademicaSqlAlchemy),
                    ("editar", operacoes.EdicaoFormacaoAcademicaSqlAlchemy),
                    ("excluir", operacoes.ExclusaoFormacaoAcademicaSqlAlchemy),
                    # Proveniência: decision-analysis prompts/backend/20261107-171028-listar-formacoes-academicas-v001.md#v001
                    ("listar", operacoes.ListarFormacoesAcademicasSqlAlchemy),
                ):
                    # Proveniência: decision-analysis prompts/backend/20261107-171028-listar-formacoes-academicas-v001.md#v001
                    chave = "listar_formacoes_academicas" if nome == "listar" else f"{nome}_formacao_academica"
                    executor = criar_app.call_args.kwargs[chave]
                    if url:
                        self.assertIsInstance(executor, classe)
                        self.assertIs(executor._sessoes, modulo._sessoes_persistencia)
                    else:
                        self.assertIsNone(executor)

    def test_gerador_entrega_uuid4_e_relogio_entrega_utc(self):
        """Confere tipos e fuso das fontes reais para identidades e exclusões."""
        identidade = GeradorFormacaoAcademicaIdUuid4().gerar()
        self.assertIsInstance(identidade.valor, UUID)
        self.assertEqual(identidade.valor.version, 4)
        self.assertEqual(operacoes.RelogioUtc().agora().utcoffset().total_seconds(), 0)


class TransacoesFormacaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica transações e delegação com doubles determinísticos dos casos."""

    # Proveniência: decision-analysis prompts/backend/20261107-171028-listar-formacoes-academicas-v001.md#v001
    async def test_leitura_usa_sessao_curta_delega_e_nao_confirma_mutacao(self):
        """Isola o executor de leitura substituindo sessões, caso e repositório.

        Verifica duas chamadas e o encerramento em sucesso e falha para impedir
        sessão global ou commit de mutação sem executar Application ou banco.
        """
        sessoes = Mock()
        contextos = [Mock(), Mock()]
        for contexto in contextos:
            contexto.__aenter__ = AsyncMock(return_value=Mock())
            contexto.__aexit__ = AsyncMock(return_value=False)
        sessoes.side_effect = contextos
        entrada, resultado = Mock(), Mock()
        executor = operacoes.ListarFormacoesAcademicasSqlAlchemy(sessoes)
        with (
            patch.object(operacoes, "ListarFormacoesAcademicas") as caso,
            patch.object(operacoes, "RepositorioFormacaoAcademicaSqlAlchemy") as repositorio,
        ):
            caso.return_value.executar = AsyncMock(return_value=resultado)
            self.assertIs(await executor.executar(entrada), resultado)
            caso.return_value.executar.side_effect = ValueError("falha controlada")
            with self.assertRaises(ValueError):
                await executor.executar(entrada)
            self.assertEqual(caso.return_value.executar.await_count, 2)
            caso.return_value.executar.assert_awaited_with(entrada)
            caso.assert_called_with(repositorio.return_value)
            self.assertEqual(repositorio.call_count, 2)
            for chamada, contexto in zip(repositorio.call_args_list, contextos, strict=True):
                self.assertIs(chamada.args[0], contexto.__aenter__.return_value)
                contexto.__aexit__.assert_awaited_once()
                contexto.__aenter__.return_value.commit.assert_not_called()
        self.assertEqual(sessoes.call_count, 2)
        sessoes.begin.assert_not_called()
        self.assertIsNone(contextos[0].__aexit__.call_args.args[0])
        self.assertIs(contextos[1].__aexit__.call_args.args[0], ValueError)

    async def test_operacoes_delegam_e_encerram_transacao_no_sucesso_e_na_falha(self):
        """Exercita os três executores e falhas para proteger commit e rollback.

        Inspeciona o contexto begin e as portas recebidas pelos casos, garantindo
        que exceções cheguem ao contexto transacional e ao chamador.
        """
        for nome, classe, extras in (
            ("CadastrarFormacaoAcademica", operacoes.CadastroFormacaoAcademicaSqlAlchemy, (Mock(),)),
            ("EditarFormacaoAcademica", operacoes.EdicaoFormacaoAcademicaSqlAlchemy, ()),
            ("ExcluirFormacaoAcademica", operacoes.ExclusaoFormacaoAcademicaSqlAlchemy, (Mock(),)),
        ):
            for falha in (False, True):
                with self.subTest(caso=nome, falha=falha):
                    sessoes = Mock()
                    contexto = sessoes.begin.return_value
                    contexto.__aenter__ = AsyncMock(return_value=Mock())
                    contexto.__aexit__ = AsyncMock(return_value=False)
                    entrada, resultado = Mock(), Mock()
                    with patch.object(operacoes, nome) as caso:
                        executar = AsyncMock(return_value=resultado)
                        caso.return_value.executar = executar
                        if falha:
                            executar.side_effect = ValueError("falha controlada")
                            with self.assertRaises(ValueError):
                                await classe(sessoes, *extras).executar(entrada)
                        else:
                            self.assertIs(await classe(sessoes, *extras).executar(entrada), resultado)
                        executar.assert_awaited_once_with(entrada)
                        portas = caso.call_args.args
                        repositorio = portas[1] if nome.startswith("Cadastrar") else portas[0]
                        self.assertIs(repositorio._session, contexto.__aenter__.return_value)
                    sessoes.begin.assert_called_once_with()
                    contexto.__aexit__.assert_awaited_once()
                    self.assertIs(contexto.__aexit__.call_args.args[0], ValueError if falha else None)
