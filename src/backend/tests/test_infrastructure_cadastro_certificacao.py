"""Verifica o executor transacional de certificação sem banco ou driver real.

Os testes substituem fábrica, contexto, repositório e caso de uso para observar
a fronteira de confirmação e falha. Eles existem para proteger o ciclo por
chamada sem confundir a delegação ao contexto com persistência PostgreSQL.
"""

# Proveniência: decision-analysis prompts/revisao/20261105-203823-auditoria-impacto-cursos-certificacoes-v002.md#v002

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, call, patch

from backend.application.cadastro_certificacao import (
    CadastrarCertificacaoEntrada,
    CertificacaoJaCadastrada,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.infrastructure.persistence.sqlalchemy.cadastro_certificacao import (
    CadastroCertificacaoSqlAlchemy,
)


class CadastroCertificacaoSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Isola as garantias transacionais externas do cadastro de certificação.

    A suíte controla os contextos assíncronos e substitui o núcleo por doubles
    para observar retorno, propagação e sessões independentes. Ela existe para
    impedir sucesso prematuro ou reutilização de sessão entre cadastros.
    """

    def setUp(self) -> None:
        """Prepara dependências isoladas do executor para cada cenário.

        O método instala patches locais do repositório e caso de uso e cria
        um contexto assíncrono sem I/O. Ele existe para testar somente o
        executor e restaurar as dependências automaticamente ao fim do teste.
        """
        self.sessoes = Mock()
        self.gerador = Mock()
        self.entrada = Mock(spec=CadastrarCertificacaoEntrada)
        self.entidade = Mock()
        self.sessao = Mock()
        self.transacao = MagicMock()
        self.transacao.__aenter__ = AsyncMock(return_value=self.sessao)
        self.transacao.__aexit__ = AsyncMock(return_value=False)
        self.sessoes.begin.return_value = self.transacao

        patch_repo = patch(
            "backend.infrastructure.persistence.sqlalchemy.cadastro_certificacao."
            "RepositorioCertificacaoSqlAlchemy"
        )
        self.criar_repositorio = patch_repo.start()
        self.addCleanup(patch_repo.stop)
        patch_caso = patch(
            "backend.infrastructure.persistence.sqlalchemy.cadastro_certificacao."
            "CadastrarCertificacao"
        )
        self.criar_caso = patch_caso.start()
        self.addCleanup(patch_caso.stop)
        self.caso = self.criar_caso.return_value
        self.caso.executar = AsyncMock(return_value=self.entidade)
        self.executor = CadastroCertificacaoSqlAlchemy(self.sessoes, self.gerador)

    def test_construtor_nao_abre_sessao_ou_transacao(self) -> None:
        """Mantém a construção do executor livre de abertura de recursos.

        O teste examina a fábrica injetada logo após construir o executor,
        sem executar cadastro. Ele existe para impedir que a composição
        retenha uma sessão global antes da primeira requisição.
        """
        self.sessoes.assert_not_called()
        self.sessoes.begin.assert_not_called()
        self.criar_repositorio.assert_not_called()

    async def test_delega_cadastro_e_sai_do_contexto_antes_do_retorno(self) -> None:
        """Devolve a entidade somente depois da saída transacional bem-sucedida.

        O teste controla a entrada e saída do contexto e confere a delegação
        da entrada ao caso de uso substituído. Ele existe para preservar a
        confirmação no adapter sem mover regras do núcleo para ele.
        """
        resultado = await self.executor.executar(self.entrada)

        self.assertIs(resultado, self.entidade)
        self.sessoes.begin.assert_called_once_with()
        self.criar_repositorio.assert_called_once_with(self.sessao)
        self.criar_caso.assert_called_once_with(
            self.criar_repositorio.return_value, self.gerador
        )
        self.caso.executar.assert_awaited_once_with(self.entrada)
        self.transacao.__aexit__.assert_awaited_once_with(None, None, None)

    async def test_aguarda_confirmacao_pendente_antes_de_entregar_sucesso(self) -> None:
        """Impede o chamador de receber sucesso enquanto a confirmação aguarda.

        O teste bloqueia a saída transacional com eventos, observa a tarefa
        ainda pendente e libera a confirmação. Ele existe para provar a
        ordem de retorno sem temporização arbitrária ou banco real.
        """
        confirmando = asyncio.Event()
        liberar = asyncio.Event()

        async def sair(*_argumentos: object) -> bool:
            """Simula confirmação pendente por eventos e permite a saída.

            O double sinaliza o início e aguarda liberação controlada para
            verificar que o executor não entrega sucesso antes do contexto.
            """
            confirmando.set()
            await liberar.wait()
            return False

        self.transacao.__aexit__.side_effect = sair
        tarefa = asyncio.create_task(self.executor.executar(self.entrada))
        try:
            await asyncio.wait_for(confirmando.wait(), timeout=2)
            self.assertFalse(tarefa.done())
        finally:
            liberar.set()
            resultado = await tarefa
        self.assertIs(resultado, self.entidade)

    async def test_encaminha_excecoes_ao_contexto_para_rollback(self) -> None:
        """Propaga falhas do cadastro ao contexto sem convertê-las em sucesso.

        O teste injeta duplicidade, regra inválida, falha inesperada e
        cancelamento e observa a exceção entregue à saída transacional. Ele
        existe para assegurar a delegação da reversão ao begin do SQLAlchemy.
        """
        for erro in (
            CertificacaoJaCadastrada("duplicado"),
            RegraDeDominioViolada("inválido"),
            RuntimeError("falha de escrita"),
            asyncio.CancelledError(),
        ):
            with self.subTest(tipo=type(erro).__name__):
                self.transacao.__aexit__.reset_mock()
                self.caso.executar.side_effect = erro

                with self.assertRaises(type(erro)) as falha:
                    await self.executor.executar(self.entrada)

                self.assertIs(falha.exception, erro)
                argumentos = self.transacao.__aexit__.await_args.args
                self.assertIs(argumentos[0], type(erro))
                self.assertIs(argumentos[1], erro)
                self.assertIsNotNone(argumentos[2])

    async def test_propaga_falha_de_commit_sem_devolver_entidade(self) -> None:
        """Recusa sucesso quando o contexto falha ao confirmar a transação.

        O teste faz o caso de uso terminar e a saída do contexto lançar uma
        falha de commit. Ele existe para impedir que a entidade já construída
        seja devolvida como cadastro confirmado após falha no banco.
        """
        erro = RuntimeError("falha no commit")
        self.transacao.__aexit__.side_effect = erro

        with self.assertRaises(RuntimeError) as falha:
            await self.executor.executar(self.entrada)

        self.assertIs(falha.exception, erro)
        self.caso.executar.assert_awaited_once_with(self.entrada)
        self.transacao.__aexit__.assert_awaited_once_with(None, None, None)

    async def test_cada_cadastro_recebe_sessao_independente(self) -> None:
        """Solicita outra transação e repositório para cada cadastro.

        O teste fornece duas sessões por contextos diferentes e executa o
        mesmo adapter duas vezes. Ele existe para impedir que o executor
        compartilhe estado transacional entre requisições.
        """
        outra_sessao = Mock()
        outra_transacao = MagicMock()
        outra_transacao.__aenter__ = AsyncMock(return_value=outra_sessao)
        outra_transacao.__aexit__ = AsyncMock(return_value=False)
        self.sessoes.begin.side_effect = [self.transacao, outra_transacao]

        await self.executor.executar(self.entrada)
        await self.executor.executar(self.entrada)

        self.assertEqual(self.sessoes.begin.call_count, 2)
        self.assertEqual(
            self.criar_repositorio.call_args_list,
            [call(self.sessao), call(outra_sessao)],
        )
        self.transacao.__aexit__.assert_awaited_once_with(None, None, None)
        outra_transacao.__aexit__.assert_awaited_once_with(None, None, None)
