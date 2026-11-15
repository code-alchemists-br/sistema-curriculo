"""Verifica composição de projetos com engine, framework e casos doubles.

Carrega main isolado e exercita executores transacionais sem banco, rede,
servidor ou contexto FastAPI para proteger a ligação dos quatro fluxos.
"""

# Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
import importlib.util
import inspect
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, Mock, patch

from backend.api import factory
from backend.infrastructure.persistence.sqlalchemy import (
    operacoes_projeto_academico as operacoes,
)


class ComposicaoProjetoTestCase(TestCase):
    """Verifica bindings locais substituindo criação de engine e aplicação.

    Executa somente composição e observa argumentos para conferir executores
    com e sem fábrica de sessões, sem abrir conexões ou iniciar framework.
    """

    def test_main_injeta_quatro_executores_somente_com_sessoes(self):
        """Carrega main com banco configurado e ausente usando doubles externos.

        Confere classes e fábrica compartilhada por configuração para garantir
        que main.app receba capacidades concretas ou indisponibilidade explícita.
        """
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
                self.assertIs(modulo.app, criar_app.return_value)
                for nome, classe in (
                    ("cadastrar", operacoes.CadastroProjetoAcademicoSqlAlchemy),
                    ("consultar", operacoes.ConsultaProjetoAcademicoSqlAlchemy),
                    ("editar", operacoes.EdicaoProjetoAcademicoSqlAlchemy),
                    ("excluir", operacoes.ExclusaoProjetoAcademicoSqlAlchemy),
                ):
                    executor = criar_app.call_args.kwargs[f"{nome}_projeto_academico"]
                    if url:
                        self.assertIsInstance(executor, classe)
                        self.assertIs(executor._sessoes, modulo._sessoes_persistencia)
                        if nome == "excluir":
                            self.assertIsInstance(executor._relogio, modulo.RelogioUtc)
                    else:
                        self.assertIsNone(executor)

    def test_factory_encaminha_executores_e_preserva_parametros_posicionais(self):
        """Isola factory com FastAPI e router doubles para verificar os bindings.

        Compara a cauda da assinatura e argumentos do router para impedir
        deslocamento de chamadas posicionais e perda da injeção das operações.
        """
        nomes = list(inspect.signature(factory.create_app).parameters)
        self.assertEqual(nomes[-3:], ["consultar_projeto_academico",
                                    "editar_projeto_academico", "excluir_projeto_academico"])
        consulta, edicao, exclusao = Mock(), Mock(), Mock()
        with (
            patch.object(factory, "FastAPI"),
            patch.object(factory, "configurar_documentacao"),
            patch.object(factory, "criar_router_projeto_academico") as router,
        ):
            app = factory.create_app(consultar_projeto_academico=consulta,
                                     editar_projeto_academico=edicao,
                                     excluir_projeto_academico=exclusao)
            self.assertEqual(router.call_args.kwargs, {
                "consultar_projeto_academico": consulta,
                "editar_projeto_academico": edicao,
                "excluir_projeto_academico": exclusao,
            })
            self.assertTrue(any(c.args[0] is router.return_value
                                for c in app.include_router.call_args_list))


class ExecutoresProjetoTestCase(IsolatedAsyncioTestCase):
    """Isola executores de sessão com casos e repositório substituídos.

    Observa contextos em sucesso e falha para garantir sessão por chamada,
    propagação de exceções e fronteira transacional sem executar Application.
    """

    async def test_contextos_e_delegacao_no_sucesso_e_falha(self):
        """Exerce quatro executores com contextos assíncronos doubles.

        Verifica uso de begin só nas escritas, injeção de portas e encerramento
        em ambos os resultados para proteger commit ou rollback do chamador.
        """
        for nome, classe, extras, leitura in (
            ("CadastrarProjetoAcademico", operacoes.CadastroProjetoAcademicoSqlAlchemy, (Mock(),), False),
            ("ConsultarProjetoAcademico", operacoes.ConsultaProjetoAcademicoSqlAlchemy, (), True),
            ("EditarProjetoAcademico", operacoes.EdicaoProjetoAcademicoSqlAlchemy, (), False),
            ("ExcluirProjetoAcademico", operacoes.ExclusaoProjetoAcademicoSqlAlchemy, (Mock(),), False),
        ):
            for falha in (False, True):
                with self.subTest(caso=nome, falha=falha):
                    sessoes = Mock()
                    contexto = sessoes.return_value if leitura else sessoes.begin.return_value
                    contexto.__aenter__ = AsyncMock(return_value=Mock())
                    contexto.__aexit__ = AsyncMock(return_value=False)
                    entrada, resultado = Mock(), Mock()
                    with (
                        patch.object(operacoes, nome) as caso,
                        patch.object(operacoes, "RepositorioProjetoAcademicoSQLAlchemy") as repositorio,
                    ):
                        caso.return_value.executar = AsyncMock(return_value=resultado)
                        if falha:
                            caso.return_value.executar.side_effect = ValueError("falha controlada")
                            with self.assertRaises(ValueError):
                                await classe(sessoes, *extras).executar(entrada)
                        else:
                            self.assertIs(await classe(sessoes, *extras).executar(entrada), resultado)
                        caso.return_value.executar.assert_awaited_once_with(entrada)
                        caso.assert_called_once_with(repositorio.return_value, *extras)
                        repositorio.assert_called_once_with(contexto.__aenter__.return_value)
                    contexto.__aexit__.assert_awaited_once()
                    self.assertIs(contexto.__aexit__.call_args.args[0], ValueError if falha else None)
                    if leitura:
                        sessoes.assert_called_once_with()
                        sessoes.begin.assert_not_called()
                    else:
                        sessoes.begin.assert_called_once_with()
                    contexto.__aenter__.return_value.commit.assert_not_called()
