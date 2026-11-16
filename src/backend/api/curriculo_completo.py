"""Expõe as rotas para o frontend ler e salvar o currículo do estudante logado.

O módulo valida a entrada por seção, chama os casos de uso do currículo
completo e traduz falhas em respostas HTTP. Ele existe para separar o
transporte das regras de substituição das seções.
"""

from typing import Any

from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel, Field, TypeAdapter, ValidationError

from backend.application.curriculo_completo import (
    ITEM_POR_SECAO,
    CurriculoCompleto,
    CurriculoNaoEncontrado,
    DadosRepetidos,
    GerenciarCurriculoCompleto,
    SecaoSubstituivel,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.modelo_curriculo import ModeloCurriculo


class SecaoRequisicao(BaseModel):
    """Representa a lista completa de uma seção, que substitui o que estava salvo.

    Os itens chegam como objetos genéricos (até 50) e são validados contra o
    modelo da seção na rota; ``curriculo_lattes`` só vale para formações.
    Existe para que uma única rota atenda todas as seções substituíveis.
    """

    itens: list[dict[str, Any]] = Field(default_factory=list, max_length=50)
    curriculo_lattes: str | None = Field(
        default=None, description="Só usado na seção de formações."
    )


class ModeloRequisicao(BaseModel):
    """Representa o modelo visual escolhido para o currículo.

    O valor é validado contra o catálogo de modelos do domínio. Existe para
    persistir a escolha feita na tela de seleção de modelo.
    """

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
        """Devolve o caso de uso ou responde 503 quando não há banco.

        Existe para que todas as rotas tratem a ausência de persistência igual.
        """
        if gerenciar is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Banco de dados indisponível.")
        return gerenciar

    @router.get("", response_model=CurriculoCompleto, summary="Lê o currículo salvo do estudante logado")
    async def consultar(request: Request) -> CurriculoCompleto:
        """Lê o currículo salvo do estudante da sessão.

        Responde 404 quando a conta não existe mais. Existe para o frontend
        preencher as telas a partir do banco.
        """
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
        """Salva o modelo visual escolhido pelo estudante da sessão.

        Responde 204 sem corpo em caso de sucesso. Existe para persistir a
        escolha da tela de seleção de modelo.
        """
        await _disponivel().salvar_modelo(request.state.usuario_id, corpo.modelo)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.put(
        "/{secao}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Substitui todos os itens de uma seção pela lista enviada",
    )
    async def substituir(
        request: Request, secao: SecaoSubstituivel, corpo: SecaoRequisicao
    ) -> Response:
        """Substitui todos os itens de uma seção pela lista enviada.

        Valida os itens contra o modelo da seção (422 com os campos inválidos),
        aplica as regras do domínio (422) e recusa itens repetidos (409).
        Responde 204 em caso de sucesso. Existe para salvar uma etapa do
        currículo sem duplicar registros.
        """
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
