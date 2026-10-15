"""Expõe o cadastro autenticado de links profissionais por HTTP.

O módulo traduz DTOs HTTP para a entrada existente da Application e converte a
entidade resultante em uma resposta pública. Ele existe para disponibilizar o
cadastro sem revelar modelos de domínio ou aceitar o proprietário do cliente.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.application.cadastro_link_profissional import (
    CadastrarLinkProfissionalEntrada,
    LinkProfissionalJaCadastrado,
)
from backend.domain import LinkProfissional, RegraDeDominioViolada
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class CadastroLinkProfissionalRequisicao(BaseModel):
    """Representa os campos externos necessários para cadastrar um link profissional.

    O DTO valida a forma do JSON e mantém o dono fora do payload, deixando a
    regra de conteúdo para o domínio. Ele existe para separar o contrato HTTP
    do comando interno e impedir que o cliente escolha outro proprietário.
    """

    rotulo: str
    url: str


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class LinkProfissionalResposta(BaseModel):
    """Representa o link profissional público devolvido após seu cadastro.

    O DTO extrai valores primitivos da entidade validada, sem serializá-la
    diretamente. Ele existe para tornar o contrato HTTP independente da
    representação e dos value objects internos do domínio.
    """

    id: UUID
    usuario_id: UUID
    rotulo: str
    url: str


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class CadastroLinkProfissionalExecutor(Protocol):
    """Define o contrato de cadastro consumido pela fronteira HTTP.

    O protocolo recebe o comando tipado e devolve a entidade criada, sem
    revelar persistência à API. Ele existe para permitir injeção do caso de uso
    e teste isolado da tradução de transporte.
    """

    async def executar(
        self, entrada: CadastrarLinkProfissionalEntrada
    ) -> LinkProfissional:
        """Cadastra um link profissional para o proprietário autenticado.

        Implementações aplicam invariantes e persistência por contratos
        internos. O método existe para manter o handler HTTP independente do
        caso de uso concreto e de seus adapters.
        """


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def criar_router(
    cadastrar_link_profissional: CadastroLinkProfissionalExecutor | None,
) -> APIRouter:
    """Cria a rota protegida de criação de links profissionais.

    A fábrica registra um handler que obtém o proprietário do estado da
    requisição, converte o DTO e traduz falhas conhecidas em HTTP. Ela existe
    para manter o transporte fino e depender apenas do executor injetado.
    """
    router = APIRouter()

    @router.post(
        "/links-profissionais",
        response_model=LinkProfissionalResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def cadastrar(
        requisicao: CadastroLinkProfissionalRequisicao,
        request: Request,
    ) -> LinkProfissionalResposta:
        """Cadastra o link profissional para a identidade autenticada da requisição.

        O handler exige executor e UUID instalados pelo mecanismo existente,
        cria a entrada interna e apresenta erros de domínio ou duplicidade com
        códigos estáveis. Ele existe para preservar a propriedade do dado e a
        resposta pública do endpoint.
        """
        if cadastrar_link_profissional is None:
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
            link = await cadastrar_link_profissional.executar(
                CadastrarLinkProfissionalEntrada(
                    usuario_id=UsuarioId(usuario_id),
                    rotulo=requisicao.rotulo,
                    url=requisicao.url,
                )
            )
        except LinkProfissionalJaCadastrado as erro:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Link profissional já cadastrado para este usuário.",
            ) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(erro),
            ) from erro
        return LinkProfissionalResposta(
            id=link.id.valor,
            usuario_id=link.usuario_id.valor,
            rotulo=link.rotulo,
            url=link.url,
        )

    return router
