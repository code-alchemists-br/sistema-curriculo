"""Protege os bindings das operações de experiências com doubles locais.

Carrega a composição com dependências externas substituídas e isola o executor
para observar injeção e ciclo de sessão sem executar casos de uso reais.
"""

# Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
import importlib.util
import unittest
from unittest.mock import AsyncMock, Mock, patch

from backend.domain.value_objects import ExperienciaProfissionalId
from backend.infrastructure.identificadores.geradores import (
    GeradorExperienciaProfissionalIdUuid4,
)
from backend.infrastructure.persistence.sqlalchemy import (
    cadastro_experiencia_profissional as cadastro,
)
from backend.infrastructure.persistence.sqlalchemy import (
    listar_experiencias_profissionais as leitura,
)
from backend.infrastructure.persistence.sqlalchemy import (
    operacoes_experiencia_profissional as mutacoes,
)


class ComposicaoExperienciasTestCase(unittest.TestCase):
    """Confere o binding do módulo de entrada sem construir aplicação real.

    Substitui engine, fábrica de sessões e create_app para verificar somente a
    escolha de todas as operações de experiências, sem executar persistência.
    """

    def test_main_injeta_todas_as_operacoes_de_experiencias_quando_ha_sessoes(self):
        """Carrega main isoladamente com e sem URL e inspeciona create_app.

        Usa factories double para conferir o executor e sua fábrica de sessões
        sem rede, protegendo a disponibilidade do cadastro com banco configurado.
        """
        for url in ("", "postgresql+psycopg://localhost/teste"):
            with self.subTest(com_banco=bool(url)):
                spec = importlib.util.find_spec("backend.main")
                modulo = importlib.util.module_from_spec(spec)
                # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
                relogio = Mock()
                with (
                    patch("backend.infrastructure.persistence.sqlalchemy.operacoes_formacao_academica.RelogioUtc", return_value=relogio),
                    patch.dict("os.environ", {"DATABASE_URL": url}),
                    patch("sqlalchemy.ext.asyncio.create_async_engine"),
                    patch("sqlalchemy.ext.asyncio.async_sessionmaker"),
                    patch("backend.api.factory.create_app") as criar_app,
                ):
                    spec.loader.exec_module(modulo)
                argumentos = criar_app.call_args.kwargs
                executor = argumentos["listar_experiencias_profissionais"]
                if url:
                    self.assertIsInstance(executor, leitura.ListarExperienciasProfissionaisSqlAlchemy)
                    self.assertIs(executor._sessoes, modulo._sessoes_persistencia)
                else:
                    self.assertIsNone(executor)
                executor_cadastro = argumentos["cadastrar_experiencia_profissional"]
                if url:
                    self.assertIsInstance(executor_cadastro, cadastro.CadastroExperienciaProfissionalSqlAlchemy)
                    self.assertIs(executor_cadastro._sessoes, modulo._sessoes_persistencia)
                    # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
                    self.assertIs(executor_cadastro._relogio, relogio)
                    relogio.agora.assert_not_called()
                else:
                    self.assertIsNone(executor_cadastro)
                for operacao, classe in (
                    ("editar", mutacoes.EdicaoExperienciaProfissionalSqlAlchemy),
                    ("excluir", mutacoes.ExclusaoExperienciaProfissionalSqlAlchemy),
                ):
                    executor_mutacao = argumentos[f"{operacao}_experiencia_profissional"]
                    if url:
                        self.assertIsInstance(executor_mutacao, classe)
                        self.assertIs(executor_mutacao._sessoes, modulo._sessoes_persistencia)
                        # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
                        self.assertIs(executor_mutacao._relogio, relogio)
                    else:
                        self.assertIsNone(executor_mutacao)


class SessaoLeituraExperienciasTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica delegação e sessão por chamada substituindo todas as fronteiras.

    Usa contextos locais double para observar encerramento em sucesso e falha
    sem executar Application, ORM, engine, consulta SQL ou transação real.
    """

    async def test_leitura_usa_sessao_por_chamada_e_nao_confirma_mutacao(self):
        """Executa sucesso e falha com duas sessões double e caso substituído.

        Confere injeção do repositório e entrada, preservação do resultado e
        encerramento dos contextos sem begin ou commit para isolar recursos da
        leitura e permitir propagação de falhas ao chamador.
        """
        sessoes = Mock()
        contextos = [Mock(), Mock()]
        for contexto in contextos:
            contexto.__aenter__ = AsyncMock(return_value=Mock())
            contexto.__aexit__ = AsyncMock(return_value=False)
        sessoes.side_effect = contextos
        entrada, resultado = Mock(), Mock()
        executor = leitura.ListarExperienciasProfissionaisSqlAlchemy(sessoes)
        with (
            patch.object(leitura, "ListarExperienciasProfissionais") as caso,
            patch.object(leitura, "RepositorioExperienciaProfissionalSqlAlchemy") as repositorio,
        ):
            caso.return_value.executar = AsyncMock(return_value=resultado)
            self.assertIs(await executor.executar(entrada), resultado)
            caso.return_value.executar.assert_awaited_once_with(entrada)
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
                contexto.__aenter__.return_value.flush.assert_not_called()
        self.assertEqual(sessoes.call_count, 2)
        sessoes.begin.assert_not_called()
        self.assertIsNone(contextos[0].__aexit__.call_args.args[0])
        self.assertIs(contextos[1].__aexit__.call_args.args[0], ValueError)


class CadastroExperienciasTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o cadastro transacional com sessão e caso de uso substituídos.

    Confere identidade concreta e delegação isolada para impedir sucesso sem
    encerramento da transação ou dependência de banco nos testes unitários.
    """

    def test_gerador_produz_identidades_tipadas_uuid4(self):
        """Confere o tipo e versão das identidades usando o gerador de produção.

        Gera duas identidades e compara UUIDs para proteger a estratégia concreta
        exigida pelo cadastro sem consultar recursos externos.
        """
        gerador = GeradorExperienciaProfissionalIdUuid4()
        primeira, segunda = gerador.gerar(), gerador.gerar()
        self.assertIsInstance(primeira, ExperienciaProfissionalId)
        self.assertEqual(primeira.valor.version, 4)
        self.assertNotEqual(primeira, segunda)

    async def test_cadastro_delega_em_transacao_e_propaga_falhas_para_rollback(self):
        """Simula sucesso e falha para inspecionar a transação da requisição.

        Substitui sessão, repositório e caso para conferir injeção de dependências
        e que a exceção chega ao contexto begin, responsável por commit/rollback.
        """
        for falha in (False, True):
            with self.subTest(falha=falha):
                sessoes = Mock()
                contexto = sessoes.begin.return_value
                contexto.__aenter__ = AsyncMock(return_value=Mock())
                contexto.__aexit__ = AsyncMock(return_value=False)
                # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
                entrada, resultado, gerador, relogio = Mock(), Mock(), Mock(), Mock()
                with (
                    patch.object(cadastro, "CadastrarExperienciaProfissional") as caso,
                    patch.object(cadastro, "RepositorioExperienciaProfissionalSqlAlchemy") as repositorio,
                ):
                    caso.return_value.executar = AsyncMock(return_value=resultado)
                    executor = cadastro.CadastroExperienciaProfissionalSqlAlchemy(
                        # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
                        sessoes, gerador, relogio
                    )
                    if falha:
                        caso.return_value.executar.side_effect = ValueError("falha controlada")
                        with self.assertRaises(ValueError):
                            await executor.executar(entrada)
                    else:
                        self.assertIs(await executor.executar(entrada), resultado)
                    caso.return_value.executar.assert_awaited_once_with(entrada)
                    # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
                    caso.assert_called_once_with(repositorio.return_value, gerador, relogio)
                    repositorio.assert_called_once_with(contexto.__aenter__.return_value)
                sessoes.begin.assert_called_once_with()
                contexto.__aexit__.assert_awaited_once()
                self.assertIs(contexto.__aexit__.call_args.args[0], ValueError if falha else None)


class MutacoesExperienciasTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica transações de edição e exclusão com todas as portas substituídas.

    Observa delegação, relógio e encerramento para proteger persistência por
    requisição sem executar banco, regras de negócio ou relógio real.
    """

    async def test_edicao_e_exclusao_delegam_e_encerram_transacao_em_sucesso_e_falha(self):
        """Exercita cada executor com caso double em sucesso e exceção.

        Confere repositório, entrada e relógio recebidos, além da propagação da
        exceção ao contexto begin, para garantir a fronteira transacional.
        """
        relogio = Mock()
        for nome, classe, extras in (
            # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
            ("EditarExperienciaProfissional", mutacoes.EdicaoExperienciaProfissionalSqlAlchemy, (relogio,)),
            ("ExcluirExperienciaProfissional", mutacoes.ExclusaoExperienciaProfissionalSqlAlchemy, (relogio,)),
        ):
            for falha in (False, True):
                with self.subTest(caso=nome, falha=falha):
                    sessoes = Mock()
                    contexto = sessoes.begin.return_value
                    contexto.__aenter__ = AsyncMock(return_value=Mock())
                    contexto.__aexit__ = AsyncMock(return_value=False)
                    entrada, resultado = Mock(), Mock()
                    with (
                        patch.object(mutacoes, nome) as caso,
                        patch.object(mutacoes, "RepositorioExperienciaProfissionalSqlAlchemy") as repositorio,
                    ):
                        caso.return_value.executar = AsyncMock(return_value=resultado)
                        executor = classe(sessoes, *extras)
                        if falha:
                            caso.return_value.executar.side_effect = ValueError("falha controlada")
                            with self.assertRaises(ValueError):
                                await executor.executar(entrada)
                        else:
                            self.assertIs(await executor.executar(entrada), resultado)
                        caso.return_value.executar.assert_awaited_once_with(entrada)
                        caso.assert_called_once_with(repositorio.return_value, *extras)
                        repositorio.assert_called_once_with(contexto.__aenter__.return_value)
                    sessoes.begin.assert_called_once_with()
                    contexto.__aexit__.assert_awaited_once()
                    self.assertIs(contexto.__aexit__.call_args.args[0], ValueError if falha else None)
