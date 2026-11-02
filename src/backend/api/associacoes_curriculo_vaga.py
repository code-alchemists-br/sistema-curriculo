"""Expõe a listagem paginada de associações próprias por HTTP.

O módulo valida os parâmetros de página, obtém o principal da sessão na
requisição e projeta os agregados em DTOs mínimos. Ele existe para conectar a
API ao caso de uso de listagem sem expor entidades de domínio.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import BaseModel

# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
from backend.application.consulta_associacao_curriculo_vaga import (
    ListarAssociacoesCurriculoVagaEntrada,
)
from backend.domain.associacao_curriculo_vaga import AssociacaoCurriculoVaga
from backend.domain.value_objects import UsuarioId

# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
CAMINHO_LISTAGEM_ASSOCIACOES = "/estudantes/atual/associacoes-curriculo-vaga"


# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
class ListagemAssociacoesCurriculoVagaExecutor(Protocol):
    """Define o caso de uso de listagem consumido pelo router.

    O contrato recebe parâmetros de proprietário e página e devolve agregados
    já filtrados pelo repositório. Ele existe para manter o adapter HTTP
    testável sem depender da composição SQLAlchemy.
    """

    async def executar(
        self, entrada: ListarAssociacoesCurriculoVagaEntrada
    ) -> tuple[AssociacaoCurriculoVaga, ...]:
        """Executa a consulta de associações na camada de aplicação.

        A implementação delega ao caso de uso existente e devolve a página em
        ordem determinística. O método existe para separar HTTP da orquestração.
        """
        ...


# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
class AssociacaoCurriculoVagaItemResposta(BaseModel):
    """Representa os campos existentes de uma associação na resposta HTTP.

    O DTO serializa os IDs do currículo e da vaga e os valores das classificações,
    sem expor o agregado ou inventar detalhes externos. Ele existe para manter
    explícita a projeção pública mínima da associação.
    """

    curriculo_id: UUID
    vaga_id: str
    classificacoes: list[str]


# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
class ListagemAssociacoesCurriculoVagaResposta(BaseModel):
    """Agrupa a página de associações devolvida pela API.

    O DTO envolve os itens em `associacoes` sem acrescentar total ou navegação
    não calculados pelo caso de uso. Ele existe para padronizar o corpo da
    listagem exposta ao cliente.
    """

    associacoes: list[AssociacaoCurriculoVagaItemResposta]


# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
def criar_router(
    listar_associacoes: ListagemAssociacoesCurriculoVagaExecutor | None,
) -> APIRouter:
    """Cria o endpoint de listagem associado à sessão autenticada.

    A função registra a rota privada com parâmetros de página obrigatórios,
    converte o principal instalado no request state e projeta o resultado em
    DTOs. Ela existe para expor a consulta da #243 sem aceitar identidade do
    cliente nem levar HTTP à Application.
    """
    router = APIRouter()

    @router.get(
        CAMINHO_LISTAGEM_ASSOCIACOES,
        response_model=ListagemAssociacoesCurriculoVagaResposta,
        status_code=status.HTTP_200_OK,
    )
    async def listar(
        request: Request,
        offset: int = Query(ge=0),
        limit: int = Query(gt=0),
    ) -> ListagemAssociacoesCurriculoVagaResposta:
        """Retorna uma página das associações do estudante autenticado.

        O handler exige o principal da sessão, valida a entrada do caso de uso,
        delega a consulta e ordena as classificações para serialização
        determinística, preservando a ordem dos agregados. Ele existe para
        apresentar a listagem com identidade confiável e erros HTTP explícitos.
        """
        usuario_id = getattr(request.state, "usuario_id", None)
        if not isinstance(usuario_id, UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária.",
            )
        if listar_associacoes is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Listagem de associações indisponível.",
            )

        try:
            entrada = ListarAssociacoesCurriculoVagaEntrada(
                usuario_id=UsuarioId(usuario_id),
                offset=offset,
                limit=limit,
            )
        except ValueError as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(erro),
            ) from erro

        associacoes = await listar_associacoes.executar(entrada)
        return ListagemAssociacoesCurriculoVagaResposta(
            associacoes=[
                AssociacaoCurriculoVagaItemResposta(
                    curriculo_id=associacao.curriculo_id.valor,
                    vaga_id=associacao.vaga_id.valor,
                    classificacoes=sorted(
                        classificacao.value
                        for classificacao in associacao.classificacoes
                    ),
                )
                for associacao in associacoes
            ]
        )

    return router
