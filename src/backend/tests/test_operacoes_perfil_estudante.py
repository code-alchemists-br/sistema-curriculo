"""Testa os adaptadores transacionais de perfil com doubles de sessão e casos.

O módulo valida que as operações de escrita (atualização integral, edição e
exclusão) utilizem transações isoladas por chamada (bloco begin()), que as
operações de leitura utilizem sessões curtas sem confirmação de mutação e que
erros sejam propagados para reversão atômica. Ele existe para garantir que a
camada de infraestrutura cumpra os contratos da Clean Architecture sem depender
de banco de dados em tempo de teste unitário.
"""

import importlib.util
import unittest
from unittest.mock import AsyncMock, Mock, patch

from backend.infrastructure.persistence.sqlalchemy import (
    operacoes_perfil_estudante as operacoes,
)


class ComposicaoPerfilTestCase(unittest.TestCase):
    """Verifica a injeção dos adaptadores de perfil na composição ASGI."""

    def test_main_injeta_operacoes_perfil_somente_com_banco(self) -> None:
        """Verifica que main.py injeta os adaptadores com DATABASE_URL e None sem ela.

        Como faz: carrega o módulo backend.main isoladamente com e sem variável
        DATABASE_URL, inspecionando os kwargs passados para create_app().
        Qual finalidade atende: protege a injeção em produção contra remoção
        acidental e regressões que reintroduzam erro 503.
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
                    (
                        "atualizar_perfil_completo",
                        operacoes.AtualizarPerfilCompletoSqlAlchemy,
                    ),
                    ("consultar_perfil", operacoes.ConsultarPerfilSqlAlchemy),
                    ("editar_perfil", operacoes.EdicaoPerfilSqlAlchemy),
                    ("excluir_perfil", operacoes.ExclusaoPerfilSqlAlchemy),
                ):
                    executor = criar_app.call_args.kwargs[chave]
                    if url:
                        self.assertIsInstance(executor, classe)
                        self.assertIs(executor._sessoes, modulo._sessoes_persistencia)
                    else:
                        self.assertIsNone(executor)


class OperacoesPerfilEstudanteTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica isolamento transacional e delegação dos adaptadores de perfil.

    A suíte testa o ciclo de vida das sessões SQLAlchemy e a injeção dos
    repositórios nos casos de uso reais correspondentes.
    """

    async def test_atualizar_perfil_completo_executa_em_begin_e_propaga_resultado(
        self,
    ) -> None:
        """Verifica que a atualização completa executa dentro de begin transacional.

        Como faz: substitui o criador de sessões e o caso de uso por mocks,
        executando o adapter e inspecionando a entrada no bloco begin().
        Qual finalidade atende: garante atomicidade e durabilidade da gravação
        de dados pessoais sem persistência parcial.
        """
        sessoes = Mock()
        contexto = sessoes.begin.return_value
        contexto.__aenter__ = AsyncMock(return_value=Mock())
        contexto.__aexit__ = AsyncMock(return_value=False)
        entrada = Mock()
        resultado_esperado = Mock()

        executor = operacoes.AtualizarPerfilCompletoSqlAlchemy(sessoes)
        with patch.object(operacoes, "AtualizarPerfilCompleto") as caso_mock:
            caso_mock.return_value.executar = AsyncMock(return_value=resultado_esperado)
            resultado = await executor.executar(entrada)

            self.assertIs(resultado, resultado_esperado)
            sessoes.begin.assert_called_once_with()
            contexto.__aenter__.assert_awaited_once()
            contexto.__aexit__.assert_awaited_once()
            caso_mock.return_value.executar.assert_awaited_once_with(entrada)
            self.assertIs(contexto.__aexit__.call_args.args[0], None)

    async def test_atualizar_perfil_completo_propaga_excecao_para_rollback(
        self,
    ) -> None:
        """Verifica que exceções no caso de uso são propagadas ao contexto begin.

        Como faz: configura o caso de uso para lançar ValueError e valida a
        passagem do tipo de erro aos argumentos de saída do contexto assíncrono.
        Qual finalidade atende: protege o banco de dados contra confirmações
        indevidas quando uma regra de negócio ou integridade é violada.
        """
        sessoes = Mock()
        contexto = sessoes.begin.return_value
        contexto.__aenter__ = AsyncMock(return_value=Mock())
        contexto.__aexit__ = AsyncMock(return_value=False)
        entrada = Mock()

        executor = operacoes.AtualizarPerfilCompletoSqlAlchemy(sessoes)
        with patch.object(operacoes, "AtualizarPerfilCompleto") as caso_mock:
            caso_mock.return_value.executar = AsyncMock(
                side_effect=ValueError("falha controlada")
            )
            with self.assertRaises(ValueError):
                await executor.executar(entrada)

            sessoes.begin.assert_called_once_with()
            self.assertIs(contexto.__aexit__.call_args.args[0], ValueError)

    async def test_consultar_perfil_utiliza_sessao_curta_sem_begin(self) -> None:
        """Verifica que a consulta de perfil abre sessão de leitura sem bloco begin.

        Como faz: configura sessão mockada com enter/exit e valida que begin()
        nunca é acionado pelo adaptador ConsultarPerfilSqlAlchemy.
        Qual finalidade atende: evita bloqueios ou commits desnecessários em
        operações puras de leitura de perfil.
        """
        sessoes = Mock()
        contexto = Mock()
        contexto.__aenter__ = AsyncMock(return_value=Mock())
        contexto.__aexit__ = AsyncMock(return_value=False)
        sessoes.return_value = contexto
        entrada = Mock()
        resultado_esperado = Mock()

        executor = operacoes.ConsultarPerfilSqlAlchemy(sessoes)
        with patch.object(operacoes, "ConsultarPerfilEstudante") as caso_mock:
            caso_mock.return_value.executar = AsyncMock(return_value=resultado_esperado)
            resultado = await executor.executar(entrada)

            self.assertIs(resultado, resultado_esperado)
            sessoes.assert_called_once_with()
            sessoes.begin.assert_not_called()
            contexto.__aenter__.assert_awaited_once()
            contexto.__aexit__.assert_awaited_once()
            caso_mock.return_value.executar.assert_awaited_once_with(entrada)
            self.assertIs(contexto.__aexit__.call_args.args[0], None)

    async def test_edicao_perfil_executa_em_begin(self) -> None:
        """Verifica que a edição de perfil abre transação com begin.

        Como faz: executa EdicaoPerfilSqlAlchemy e verifica o acionamento do
        método begin() e do caso de uso EditarPerfil.
        Qual finalidade atende: garante atomicidade para edições parciais.
        """
        sessoes = Mock()
        contexto = sessoes.begin.return_value
        contexto.__aenter__ = AsyncMock(return_value=Mock())
        contexto.__aexit__ = AsyncMock(return_value=False)
        entrada = Mock()
        resultado_esperado = Mock()

        executor = operacoes.EdicaoPerfilSqlAlchemy(sessoes)
        with patch.object(operacoes, "EditarPerfil") as caso_mock:
            caso_mock.return_value.executar = AsyncMock(return_value=resultado_esperado)
            resultado = await executor.executar(entrada)

            self.assertIs(resultado, resultado_esperado)
            sessoes.begin.assert_called_once_with()
            caso_mock.return_value.executar.assert_awaited_once_with(entrada)

    async def test_exclusao_perfil_executa_em_begin_com_relogio(self) -> None:
        """Verifica que a exclusão lógica usa transação e injeta relógio.

        Como faz: invoca ExclusaoPerfilSqlAlchemy repassando relógio mockado
        e valida a passagem do relógio ao caso de uso ExcluirPerfil.
        Qual finalidade atende: assegura que o instante de exclusão lógica seja
        registrado sob transação e de maneira determinística.
        """
        sessoes = Mock()
        contexto = sessoes.begin.return_value
        contexto.__aenter__ = AsyncMock(return_value=Mock())
        contexto.__aexit__ = AsyncMock(return_value=False)
        relogio = Mock()
        entrada = Mock()
        resultado_esperado = Mock()

        executor = operacoes.ExclusaoPerfilSqlAlchemy(sessoes, relogio)
        with patch.object(operacoes, "ExcluirPerfil") as caso_mock:
            caso_mock.return_value.executar = AsyncMock(return_value=resultado_esperado)
            resultado = await executor.executar(entrada)

            self.assertIs(resultado, resultado_esperado)
            sessoes.begin.assert_called_once_with()
            caso_mock.assert_called_once()
            self.assertIs(caso_mock.call_args.args[1], relogio)
            caso_mock.return_value.executar.assert_awaited_once_with(entrada)
