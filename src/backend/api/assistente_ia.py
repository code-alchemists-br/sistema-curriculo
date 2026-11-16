"""Expõe as rotas do assistente de IA: revisão de um campo e recomendação de modelo.

O módulo converte as requisições em entradas dos casos de uso e traduz as
falhas em respostas HTTP. Ele existe para separar o transporte das regras da
revisão e da recomendação.
"""

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
    """Representa o JSON aceito para revisar um campo do formulário.

    Traz o campo, o texto do estudante, a pergunta exibida e dados já
    preenchidos do item (como cargo e empresa), com limites de tamanho para
    conter o custo da chamada à IA. Existe para validar a entrada na fronteira.
    """

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
    """Representa um dado extra que não fica no banco, como o objetivo do currículo.

    O par pergunta/resposta tem limites de tamanho e é convertido em
    ``InformacaoPerfil``. Existe para que a tela acrescente contexto à
    recomendação sem gravá-lo no perfil.
    """

    pergunta: str = Field(max_length=200, examples=["Carreira desejada"])
    resposta: str = Field(max_length=2000, examples=["Desenvolvimento Back-end (Júnior)"])


class RecomendacaoRequisicao(BaseModel):
    """Representa o JSON aceito para recomendar o modelo de currículo.

    Contém até dez dados extras somados ao perfil salvo. Existe para validar a
    entrada da recomendação na fronteira HTTP.
    """

    extras: list[InformacaoRequisicao] = Field(default_factory=list, max_length=10)


_RESPOSTAS = {
    401: {"description": "Sessão ausente ou inválida."},
    503: {"description": "Gemini não configurado ou indisponível."},
}


def criar_router(
    revisar_texto: RevisarTexto | None,
    recomendar_modelo: RecomendarModeloCurriculo | None,
) -> APIRouter:
    """Cria as rotas do assistente de IA, protegidas pela sessão.

    Registra ``POST /assistente/revisoes`` e ``POST /assistente/recomendacao-modelo``;
    sem caso de uso injetado, a rota responde indisponível (503). Existe para
    que a composição ligue o assistente sem que o router conheça o provedor.
    """
    router = APIRouter(prefix="/assistente")

    @router.post(
        "/revisoes",
        response_model=RevisaoTexto,
        summary="Avalia um campo do formulário e devolve 3 sugestões de texto",
        responses=_RESPOSTAS,
    )
    async def revisar(corpo: RevisaoRequisicao) -> RevisaoTexto:
        """Revisa o texto enviado e devolve veredito, motivo e sugestões.

        Não grava nada: o frontend salva o texto aprovado no cadastro do item.
        Falha do provedor vira 503. Existe para a revisão automática ao avançar.
        """
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
        """Recomenda um modelo para o estudante da sessão.

        Usa o usuário autenticado pelo middleware, responde 422 quando o perfil
        está vazio e 503 quando a IA falha. Existe para a recomendação exibida
        na seleção de modelo.
        """
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
