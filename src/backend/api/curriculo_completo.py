"""Rotas para o frontend ler e salvar o currículo do estudante logado."""

from typing import Any

from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel, Field, TypeAdapter, ValidationError

from backend.application.curriculo_completo import (
    ITEM_POR_SECAO,
    CurriculoCompleto,
    CurriculoNaoEncontrado,
    DadosRepetidos,
    GerenciarCurriculoCompleto,
    SecaoCurriculo,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.modelo_curriculo import ModeloCurriculo


class SecaoRequisicao(BaseModel):
    """Lista completa da seção; substitui o que estava salvo."""

    itens: list[dict[str, Any]] = Field(default_factory=list, max_length=50)
    curriculo_lattes: str | None = Field(
        default=None, description="Só usado na seção de formações."
    )


class ModeloRequisicao(BaseModel):
    """Modelo visual escolhido para o currículo."""

    modelo: ModeloCurriculo


def criar_router_curriculo_completo(
    gerenciar: GerenciarCurriculoCompleto | None,
) -> APIRouter:
    """Cria as rotas de leitura e gravação do currículo completo.

    - O que faz: expõe a leitura de tudo o que foi salvo, a troca de uma seção
      inteira e a gravação do modelo visual.
    - Como faz: usa o usuário da sessão (``request.state.usuario_id``), valida
      os itens com o modelo da seção e traduz falhas em 404, 409, 422 e 503.
    - Qual finalidade atende: o frontend salva cada etapa no banco sem duplicar
      e mostra o currículo a partir do banco.
    """
    router = APIRouter(prefix="/estudantes/me/curriculo")

    def _disponivel() -> GerenciarCurriculoCompleto:
        if gerenciar is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Banco de dados indisponível.")
        return gerenciar

    @router.get("", response_model=CurriculoCompleto, summary="Lê o currículo salvo do estudante logado")
    async def consultar(request: Request) -> CurriculoCompleto:
        try:
            return await _disponivel().consultar(request.state.usuario_id)
        except CurriculoNaoEncontrado as erro:
            raise HTTPException(status.HTTP_404_NOT_FOUND, str(erro)) from erro

    @router.put(
        "/modelo",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Salva o modelo visual escolhido",
    )
    async def salvar_modelo(request: Request, corpo: ModeloRequisicao) -> Response:
        await _disponivel().salvar_modelo(request.state.usuario_id, corpo.modelo)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.put(
        "/{secao}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Substitui todos os itens de uma seção pela lista enviada",
    )
    async def substituir(request: Request, secao: SecaoCurriculo, corpo: SecaoRequisicao) -> Response:
        servico = _disponivel()
        try:
            itens = TypeAdapter(list[ITEM_POR_SECAO[secao]]).validate_python(corpo.itens)
        except ValidationError as erro:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                [{"loc": e["loc"], "msg": e["msg"]} for e in erro.errors()],
            ) from erro
        try:
            await servico.substituir_secao(
                request.state.usuario_id, secao, itens, corpo.curriculo_lattes
            )
        except RegraDeDominioViolada as erro:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(erro)) from erro
        except DadosRepetidos as erro:
            raise HTTPException(status.HTTP_409_CONFLICT, str(erro)) from erro
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
