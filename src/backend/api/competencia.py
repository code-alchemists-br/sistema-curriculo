"""Expõe o cadastro autenticado de competências por HTTP.

O módulo traduz DTOs HTTP para a entrada existente da Application e converte a
entidade resultante em uma resposta pública. Ele existe para disponibilizar o
cadastro sem revelar modelos de domínio ou aceitar o proprietário do cliente.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from backend.application.cadastro_competencia import (
    CadastrarCompetenciaEntrada,
    CompetenciaJaCadastrada,
)
from backend.domain import CategoriaCompetencia, Competencia, RegraDeDominioViolada
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class CadastroCompetenciaRequisicao(BaseModel):
    """Representa os campos externos necessários para criar uma competência.

    O DTO valida a forma do JSON e mantém o dono fora do payload, deixando a
    regra de conteúdo para o domínio. Ele existe para separar o contrato HTTP
    do comando interno e impedir que o cliente escolha outro proprietário.
    """

    categoria: CategoriaCompetencia
    descricao: str
    nivel: str


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class CompetenciaResposta(BaseModel):
    """Representa a competência pública devolvida após seu cadastro.

    O DTO extrai valores primitivos da entidade validada, sem serializá-la
    diretamente. Ele existe para tornar o contrato HTTP independente da
    representação e dos value objects internos do domínio.
    """

    id: UUID
    usuario_id: UUID
    categoria: CategoriaCompetencia
    descricao: str
    nivel: str


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class CadastroCompetenciaExecutor(Protocol):
    """Define o contrato de cadastro consumido pela fronteira HTTP.

    O protocolo recebe o comando tipado e devolve a entidade criada, sem
    revelar persistência à API. Ele existe para permitir injeção do caso de uso
    e teste isolado da tradução de transporte.
    """

    async def executar(self, entrada: CadastrarCompetenciaEntrada) -> Competencia:
        """Cadastra uma competência para o proprietário autenticado.

        Implementações aplicam invariantes e persistência por contratos
        internos. O método existe para manter o handler HTTP independente do
        caso de uso concreto e de seus adapters.
        """


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def criar_router(
    cadastrar_competencia: CadastroCompetenciaExecutor | None,
) -> APIRouter:
    """Cria a rota protegida de criação de competências.

    A fábrica registra um handler que obtém o proprietário do estado da
    requisição, converte o DTO e traduz falhas conhecidas em HTTP. Ela existe
    para manter o transporte fino e depender apenas do executor injetado.
    """
    router = APIRouter()

    @router.post(
        "/competencias",
        response_model=CompetenciaResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def cadastrar(
        requisicao: CadastroCompetenciaRequisicao,
        request: Request,
    ) -> CompetenciaResposta:
        """Cadastra a competência para a identidade autenticada da requisição.

        O handler exige executor e UUID instalados pelo mecanismo existente,
        cria a entrada interna e apresenta erros de domínio ou duplicidade com
        códigos estáveis. Ele existe para preservar a propriedade do dado e a
        resposta pública do endpoint.
        """
        if cadastrar_competencia is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cadastro indisponível.",
            )
        usuario_id = getattr(request.state, "usuario_id", None)
        if not isinstance(usuario_id, UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária.",
            )
        try:
            competencia = await cadastrar_competencia.executar(
                CadastrarCompetenciaEntrada(
                    usuario_id=UsuarioId(usuario_id),
                    categoria=requisicao.categoria,
                    descricao=requisicao.descricao,
                    nivel=requisicao.nivel,
                )
            )
        except CompetenciaJaCadastrada as erro:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A competência já está cadastrada.",
            ) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(erro),
            ) from erro
        return CompetenciaResposta(
            id=competencia.id.valor,
            usuario_id=competencia.usuario_id.valor,
            categoria=competencia.categoria,
            descricao=competencia.descricao,
            nivel=competencia.nivel,
        )

    return router
