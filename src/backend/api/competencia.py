"""Expõe o cadastro, listagem e exclusão autenticados de competências por HTTP.

O módulo traduz DTOs HTTP para a entrada existente da Application e converte as
entidades resultantes em respostas públicas. Ele existe para disponibilizar o
gerenciamento de competências sem revelar modelos de domínio ou aceitar o
proprietário diretamente do cliente.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from backend.application.cadastro_competencia import (
    CadastrarCompetenciaEntrada,
    CompetenciaJaCadastrada,
)
from backend.application.competencia import (
    CompetenciaNaoEncontrada,
    ExcluirCompetenciaEntrada,
    ListarCompetenciasEntrada,
)
from backend.domain import CategoriaCompetencia, Competencia, RegraDeDominioViolada
from backend.domain.value_objects import CompetenciaId, UsuarioId


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
    """Representa a competência pública devolvida após seu cadastro ou consulta.

    O DTO extrai valores primitivos da entidade validada, sem serializá-la
    diretamente. Ele existe para tornar o contrato HTTP independente da
    representação e dos value objects internos do domínio.
    """

    id: UUID
    usuario_id: UUID
    categoria: CategoriaCompetencia
    descricao: str
    nivel: str


class ListagemCompetenciasResposta(BaseModel):
    """Representa a coleção de competências cadastradas pelo estudante.

    O DTO reúne os itens em uma lista sob o atributo competencias para manter a
    resposta em formato de objeto estruturado. Ele existe para permitir evolução
    futura de contrato e serialização uniforme na interface pública.
    """

    competencias: list[CompetenciaResposta]


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


class ListagemCompetenciasExecutor(Protocol):
    """Define o contrato de consulta de competências consumido pela fronteira HTTP.

    O protocolo recebe a entrada com a identidade autenticada e retorna as
    competências do estudante. Ele existe para permitir a injeção do caso de
    uso e testes unitários isolados da camada web.
    """

    async def executar(
        self, entrada: ListarCompetenciasEntrada
    ) -> tuple[Competencia, ...]:
        """Consulta as competências do proprietário autenticado.

        Implementações aplicam a busca no repositório correspondente e retornam
        a coleção de entidades. O método existe para manter o handler desacoplado
        de detalhes de infraestrutura.
        """


class ExclusaoCompetenciaExecutor(Protocol):
    """Define o contrato de exclusão de competência consumido pela fronteira HTTP.

    O protocolo recebe o comando com os identificadores da competência e do
    usuário para executar a exclusão. Ele existe para permitir injeção do caso de
    uso de remoção e testes de fronteira independentes.
    """

    async def executar(self, entrada: ExcluirCompetenciaEntrada) -> None:
        """Exclui a competência do proprietário autenticado.

        Implementações validam posse e removem o registro no armazenamento. O
        método existe para manter o handler livre de dependências de persistência.
        """


def _usuario_autenticado(request: Request) -> UUID:
    """Obtém o UUID instalado pelo middleware de sessão ou responde 401.

    A função inspeciona request.state.usuario_id e rejeita ausências ou tipos
    inválidos. Ela existe para garantir que nenhuma operação de competência ocorra
    sem um identificador confiável provido pela autenticação.
    """
    usuario_id = getattr(request.state, "usuario_id", None)
    if not isinstance(usuario_id, UUID):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária.",
        )
    return usuario_id


def _para_resposta(competencia: Competencia) -> CompetenciaResposta:
    """Converte a entidade de domínio Competencia no DTO público de resposta.

    A função extrai identificadores primitivos e campos textuais da entidade
    sem serializá-la diretamente. Ela existe para manter a resposta HTTP
    desacoplada da representação e dos tipos internos do domínio.
    """
    return CompetenciaResposta(
        id=competencia.id.valor,
        usuario_id=competencia.usuario_id.valor,
        categoria=competencia.categoria,
        descricao=competencia.descricao,
        nivel=competencia.nivel,
    )


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def criar_router(
    cadastrar_competencia: CadastroCompetenciaExecutor | None = None,
    listar_competencias: ListagemCompetenciasExecutor | None = None,
    excluir_competencia: ExclusaoCompetenciaExecutor | None = None,
) -> APIRouter:
    """Cria as rotas protegidas de criação, listagem e exclusão de competências.

    A fábrica registra handlers que obtêm o proprietário autenticado do estado
    da requisição, convertem DTOs e traduzem exceções conhecidas em HTTP estável.
    Ela existe para manter o transporte fino e depender apenas dos executores injetados.
    """
    router = APIRouter()

    @router.get(
        "/competencias",
        response_model=ListagemCompetenciasResposta,
        status_code=status.HTTP_200_OK,
        summary="Listar competências do estudante autenticado",
        description=(
            "Requer cookie de sessão válido e lista todas as competências do "
            "estudante autenticado. Retorna 200 com array vazio se não houver registros."
        ),
        responses={
            200: {"description": "Coleção de competências do estudante."},
            401: {"description": "Autenticação necessária."},
            503: {"description": "Listagem indisponível."},
        },
    )
    async def listar(request: Request) -> ListagemCompetenciasResposta:
        """Apresenta a lista de competências pertencentes ao estudante autenticado.

        O handler valida o executor e a identidade da sessão, delega a busca ao
        caso de uso e projeta as entidades resultantes em DTOs de resposta. Ele
        existe para expor a leitura de competências protegendo a autoria dos dados.
        """
        if listar_competencias is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Listagem indisponível.",
            )
        usuario_id = _usuario_autenticado(request)
        competencias = await listar_competencias.executar(
            ListarCompetenciasEntrada(usuario_id=UsuarioId(usuario_id))
        )
        return ListagemCompetenciasResposta(
            competencias=[_para_resposta(comp) for comp in competencias]
        )

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
        usuario_id = _usuario_autenticado(request)
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
        return _para_resposta(competencia)

    @router.delete(
        "/competencias/{competencia_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Excluir competência do estudante autenticado",
        description=(
            "Remove a competência indicada pertencente ao estudante autenticado. "
            "Retorna 204 No Content em caso de sucesso ou 404 Not Found caso a "
            "competência não exista ou pertença a outro usuário."
        ),
        responses={
            204: {"description": "Competência excluída com sucesso."},
            401: {"description": "Autenticação necessária."},
            404: {"description": "Competência não encontrada."},
            503: {"description": "Exclusão indisponível."},
        },
    )
    async def excluir(competencia_id: UUID, request: Request) -> None:
        """Remove fisicamente a competência identificada na rota.

        O handler valida o executor e a identidade da sessão, invoca o caso de
        uso com os identificadores tipados e traduz falha de localização em 404.
        Ele existe para disponibilizar exclusão segura e reversibilidade sem
        vazar informações entre estudantes.
        """
        if excluir_competencia is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Exclusão indisponível.",
            )
        usuario_id = _usuario_autenticado(request)
        try:
            await excluir_competencia.executar(
                ExcluirCompetenciaEntrada(
                    competencia_id=CompetenciaId(competencia_id),
                    usuario_id=UsuarioId(usuario_id),
                )
            )
        except CompetenciaNaoEncontrada as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Competência não encontrada.",
            ) from erro

    return router
