"""Expõe solicitações públicas de recuperação e redefinição de senha."""

from typing import Protocol

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, Field

from backend.api.cadastro_acesso import DerivadorSenha
from backend.application.recuperacao_senha import (
    EntradaRedefinicaoSenha,
    EnviadorLinkRecuperacao,
    EnvioRecuperacaoSenha,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.value_objects import Email


class SolicitacaoRecuperacaoExecutor(Protocol):
    """Define a capacidade de emitir e entregar instruções de recuperação."""

    async def executar(self, email: Email) -> EnvioRecuperacaoSenha | None:
        """Processa solicitação e devolve envio privado para tarefa posterior.

        O retorno nunca é serializado e só é entregue ao serviço de e-mail em
        segundo plano. O método existe para manter a resposta sem enumeração.
        """


class RedefinicaoSenhaExecutor(Protocol):
    """Define a capacidade transacional de alterar senha com token válido."""

    async def executar(self, entrada: EntradaRedefinicaoSenha) -> bool:
        """Consome token e atualiza senha, retornando sucesso ou recusa uniforme.

        A implementação confirma o conjunto de gravações na mesma transação.
        O método existe para que a API traduza o resultado sem acessar ORM.
        """


class SolicitacaoRecuperacaoRequisicao(BaseModel):
    """Representa o e-mail informado para iniciar recuperação de conta.

    O DTO limita o tamanho antes de construir o value object de e-mail. Ele
    existe para validar o contrato HTTP sem consultar o cadastro.
    """

    email: str = Field(min_length=3, max_length=320)


class RedefinicaoSenhaRequisicao(BaseModel):
    """Representa token de recuperação e nova senha em texto temporário.

    O DTO aplica limites de transporte; a rota deriva a senha antes de invocar
    a Application. Ele existe para manter senha em claro fora de persistência.
    """

    token: str = Field(min_length=1, max_length=512)
    senha: str = Field(min_length=8, max_length=1024)


def criar_router(
    solicitar_recuperacao: SolicitacaoRecuperacaoExecutor | None,
    redefinir_senha: RedefinicaoSenhaExecutor | None,
    derivador_senha: DerivadorSenha | None,
    enviador_recuperacao: EnviadorLinkRecuperacao | None,
) -> APIRouter:
    """Cria rotas públicas a partir de executores injetados pela composição.

    A solicitação sempre devolve resposta genérica e a confirmação deriva a
    nova senha antes do caso de uso. Ela existe para expor recuperação sem
    acoplar handlers à persistência, ao SMTP ou ao algoritmo de senha.
    """
    router = APIRouter()

    @router.post("/recuperacoes-senha", status_code=status.HTTP_202_ACCEPTED)
    async def solicitar(
        requisicao: SolicitacaoRecuperacaoRequisicao,
        tarefas: BackgroundTasks,
    ) -> dict[str, str]:
        """Aceita pedido sem revelar se o e-mail tem conta registrada.

        Sempre responde com a mesma mensagem após a operação, inclusive para
        conta ausente ou envio limitado. A rota existe para evitar enumeração
        de usuários na solicitação pública.
        """
        if solicitar_recuperacao is None or enviador_recuperacao is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Recuperação de senha indisponível.",
            )
        try:
            email = Email(requisicao.email)
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Informe um e-mail válido.",
            ) from erro
        envio = await solicitar_recuperacao.executar(email)
        if envio is not None:
            tarefas.add_task(
                enviador_recuperacao.enviar, envio.email, envio.token
            )
        return {"mensagem": "Se houver uma conta associada, enviaremos instruções."}

    @router.post("/recuperacoes-senha/confirmacao", status_code=status.HTTP_204_NO_CONTENT)
    async def confirmar(requisicao: RedefinicaoSenhaRequisicao) -> None:
        """Consome token e troca credencial, recusando tokens inválidos uniformemente.

        A rota deriva a senha antes de chamar o executor e não cria sessão
        autenticada. Ela existe para concluir a recuperação sem permitir replay.
        """
        if redefinir_senha is None or derivador_senha is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Redefinição de senha indisponível.",
            )
        try:
            hash_senha = derivador_senha.derivar(requisicao.senha)
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A nova senha não atende aos requisitos.",
            ) from erro
        redefinida = await redefinir_senha.executar(
            EntradaRedefinicaoSenha(requisicao.token, hash_senha)
        )
        if not redefinida:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token de recuperação inválido ou expirado.",
            )

    return router
