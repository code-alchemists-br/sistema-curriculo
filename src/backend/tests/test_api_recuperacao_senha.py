"""Testa contratos HTTP públicos de recuperação e redefinição de senha."""

import unittest

from fastapi import BackgroundTasks, HTTPException

from backend.api.recuperacao_senha import (
    RedefinicaoSenhaRequisicao,
    SolicitacaoRecuperacaoRequisicao,
    criar_router,
)
from backend.application.recuperacao_senha import (
    EntradaRedefinicaoSenha,
    EnvioRecuperacaoSenha,
)
from backend.domain.value_objects import Email, HashSenha


class SolicitadorFalso:
    """Devolve resultado configurado sem consultar armazenamento."""

    def __init__(self, envio: EnvioRecuperacaoSenha | None) -> None:
        """Guarda resposta do executor e registra e-mail recebido."""
        self.envio = envio
        self.emails: list[Email] = []

    async def executar(self, email: Email) -> EnvioRecuperacaoSenha | None:
        """Registra e-mail e devolve resultado interno determinístico."""
        self.emails.append(email)
        return self.envio


class EnviadorFalso:
    """Registra mensagens que a rota agenda depois da resposta."""

    def __init__(self) -> None:
        """Cria histórico vazio de mensagens enviadas."""
        self.envios: list[tuple[Email, str]] = []

    async def enviar(self, email: Email, token: str) -> None:
        """Guarda conteúdo recebido para confirmar agendamento da tarefa."""
        self.envios.append((email, token))


class RedefinidorFalso:
    """Registra entradas de redefinição e devolve resultado configurado."""

    def __init__(self, resultado: bool) -> None:
        """Configura o retorno do executor e inicia histórico vazio."""
        self.resultado = resultado
        self.entradas: list[EntradaRedefinicaoSenha] = []

    async def executar(self, entrada: EntradaRedefinicaoSenha) -> bool:
        """Registra a entrada já derivada e devolve o resultado de teste."""
        self.entradas.append(entrada)
        return self.resultado


class DerivadorFalso:
    """Representa derivação de senha na fronteira HTTP."""

    def derivar(self, senha: str) -> HashSenha:
        """Devolve hash sintético sem expor senha ao caso de uso."""
        return HashSenha(f"derivado:{senha}")


class ApiRecuperacaoSenhaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica não enumeração, agendamento e consumo do contrato HTTP."""

    async def test_solicitacao_agenda_email_sem_devolver_token(self) -> None:
        """Retorna mensagem genérica e agenda envio fora da resposta serializada."""
        email = Email("ana@example.test")
        solicitador = SolicitadorFalso(EnvioRecuperacaoSenha(email, "segredo"))
        enviador = EnviadorFalso()
        router = criar_router(solicitador, RedefinidorFalso(True), DerivadorFalso(), enviador)
        tarefa = BackgroundTasks()

        resposta = await router.routes[0].endpoint(
            SolicitacaoRecuperacaoRequisicao(email=email.valor), tarefa
        )

        self.assertEqual(
            resposta,
            {"mensagem": "Se houver uma conta associada, enviaremos instruções."},
        )
        self.assertEqual(solicitador.emails, [email])
        self.assertEqual(len(tarefa.tasks), 1)
        self.assertEqual(enviador.envios, [])
        await tarefa()
        self.assertEqual(enviador.envios, [(email, "segredo")])

    async def test_solicitacao_sem_conta_usa_a_mesma_resposta(self) -> None:
        """Preserva mensagem pública genérica quando não existe conta elegível."""
        solicitador = SolicitadorFalso(None)
        router = criar_router(solicitador, RedefinidorFalso(True), DerivadorFalso(), EnviadorFalso())

        resposta = await router.routes[0].endpoint(
            SolicitacaoRecuperacaoRequisicao(email="ana@example.test"),
            BackgroundTasks(),
        )

        self.assertEqual(
            resposta,
            {"mensagem": "Se houver uma conta associada, enviaremos instruções."},
        )

    async def test_redefinicao_deriva_senha_e_retorna_sem_corpo(self) -> None:
        """Passa somente hash ao executor e conclui sem criar conteúdo de resposta."""
        redefinidor = RedefinidorFalso(True)
        router = criar_router(SolicitadorFalso(None), redefinidor, DerivadorFalso(), EnviadorFalso())

        resposta = await router.routes[1].endpoint(
            RedefinicaoSenhaRequisicao(token="token", senha="nova-senha-123")
        )

        self.assertIsNone(resposta)
        self.assertEqual(redefinidor.entradas[0].token, "token")
        self.assertEqual(redefinidor.entradas[0].hash_senha, HashSenha("derivado:nova-senha-123"))

    async def test_token_recusado_recebe_erro_uniforme(self) -> None:
        """Traduz falha do token sem revelar ausência, expiração ou replay."""
        router = criar_router(SolicitadorFalso(None), RedefinidorFalso(False), DerivadorFalso(), EnviadorFalso())

        with self.assertRaises(HTTPException) as erro:
            await router.routes[1].endpoint(
                RedefinicaoSenhaRequisicao(token="invalido", senha="nova-senha-123")
            )

        self.assertEqual(erro.exception.status_code, 400)
        self.assertEqual(erro.exception.detail, "Token de recuperação inválido ou expirado.")

    async def test_servico_ausente_responde_indisponibilidade(self) -> None:
        """Não simula sucesso quando banco ou envio não foram compostos."""
        router = criar_router(None, None, None, None)

        with self.assertRaises(HTTPException) as erro:
            await router.routes[0].endpoint(
                SolicitacaoRecuperacaoRequisicao(email="ana@example.test"),
                BackgroundTasks(),
            )

        self.assertEqual(erro.exception.status_code, 503)
