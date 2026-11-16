"""Rotas do assistente de IA: revisão de um campo e recomendação de modelo."""

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field

from backend.application.recomendacao_modelo import (
    InformacaoPerfil,
    RecomendacaoModelo,
    RecomendadorModeloIndisponivel,
    RecomendarModeloCurriculo,
)
from backend.application.revisao_texto import (
    CampoRevisavel,
    RevisaoTexto,
    RevisarTexto,
    RevisorTextoIndisponivel,
)


class RevisaoRequisicao(BaseModel):
    """Campo, pergunta exibida, texto do estudante e dados já preenchidos do item."""

    campo: CampoRevisavel
    texto: str = Field(max_length=2000, examples=["eu fazia umas api la no estagio kkk"])
    pergunta: str | None = Field(
        default=None, max_length=300, examples=["O que você fazia nessa experiência?"]
    )
    contexto: dict[str, str] = Field(
        default_factory=dict,
        max_length=10,
        examples=[{"cargo": "Estagiária de Back-end", "empresa": "TechNova"}],
    )


class InformacaoRequisicao(BaseModel):
    """Dado que não fica no banco, como a carreira desejada ou o objetivo."""

    pergunta: str = Field(max_length=200, examples=["Carreira desejada"])
    resposta: str = Field(max_length=2000, examples=["Desenvolvimento Back-end (Júnior)"])


class RecomendacaoRequisicao(BaseModel):
    """Dados extras somados ao perfil salvo na hora de recomendar o modelo."""

    extras: list[InformacaoRequisicao] = Field(default_factory=list, max_length=10)


_RESPOSTAS = {
    401: {"description": "Sessão ausente ou inválida."},
    503: {"description": "Gemini não configurado ou indisponível."},
}


def criar_router(
    revisar_texto: RevisarTexto | None,
    recomendar_modelo: RecomendarModeloCurriculo | None,
) -> APIRouter:
    """Cria as rotas protegidas por sessão do assistente de IA."""
    router = APIRouter(prefix="/assistente")

    @router.post(
        "/revisoes",
        response_model=RevisaoTexto,
        summary="Avalia um campo do formulário e devolve 3 sugestões de texto",
        responses=_RESPOSTAS,
    )
    async def revisar(corpo: RevisaoRequisicao) -> RevisaoTexto:
        """Não grava nada: o frontend salva o texto aprovado no cadastro do item."""
        if revisar_texto is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Revisão indisponível.")
        try:
            return await revisar_texto.executar(
                corpo.campo, corpo.texto, corpo.pergunta, corpo.contexto
            )
        except RevisorTextoIndisponivel as erro:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(erro)) from erro

    @router.post(
        "/recomendacao-modelo",
        response_model=RecomendacaoModelo,
        summary="Recomenda o modelo de currículo que combina com o perfil salvo",
        responses={**_RESPOSTAS, 422: {"description": "Perfil ainda vazio."}},
    )
    async def recomendar(corpo: RecomendacaoRequisicao, request: Request) -> RecomendacaoModelo:
        """Lê o perfil do estudante logado e devolve um dos modelos do sistema."""
        if recomendar_modelo is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Recomendação indisponível.")
        extras = [InformacaoPerfil(e.pergunta, e.resposta) for e in corpo.extras]
        try:
            return await recomendar_modelo.executar(request.state.usuario_id, extras)
        except ValueError as erro:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(erro)) from erro
        except RecomendadorModeloIndisponivel as erro:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(erro)) from erro

    return router
