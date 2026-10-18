"""Expõe o cadastro autenticado de projetos acadêmicos por HTTP.

O módulo valida o JSON por DTO, obtém o proprietário da sessão e converte a
entidade em resposta explícita. Ele existe para oferecer o cadastro sem expor
o domínio nem aceitar a identidade do proprietário pelo cliente.
"""

from json import JSONDecodeError
from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationError,
    ValidationInfo,
    field_validator,
)

# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
from backend.application import CadastrarProjetoAcademicoEntrada
from backend.domain import (
    TAMANHO_MAXIMO_DESCRICAO_PROJETO,
    TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO,
    TAMANHO_MAXIMO_TITULO_PROJETO,
    TAMANHO_MINIMO_TEXTO_PROJETO,
    ProjetoAcademico,
    RegraDeDominioViolada,
    UsuarioId,
)


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class CadastroProjetoAcademicoExecutor(Protocol):
    """Define a capacidade interna de cadastrar projeto acadêmico.

    O contrato recebe entrada tipada e devolve a entidade criada, sem expor
    repositório ou detalhes de armazenamento. Ele existe para manter o handler
    independente da implementação do caso de uso.
    """

    async def executar(
        self, entrada: CadastrarProjetoAcademicoEntrada
    ) -> ProjetoAcademico:
        """Executa o cadastro e devolve o projeto persistido.

        A implementação aplica invariantes do Domain e persiste pela porta
        correspondente. O método existe para separar HTTP da Application.
        """


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class CadastroProjetoAcademicoRequisicao(BaseModel):
    """Representa os três textos aceitos no corpo do cadastro.

    O DTO ignora campos desconhecidos e verifica tipo e comprimento normalizado
    usando limites do Domain, preservando os textos originais para que a entidade
    faça a normalização autoritativa. Ele existe para validar a forma do JSON.
    """

    model_config = ConfigDict(extra="ignore")

    titulo: str
    descricao: str
    tecnologias: str

    @field_validator("titulo", "descricao", "tecnologias", mode="before")
    @classmethod
    def validar_formato_e_tamanho(
        cls, valor: object, info: ValidationInfo
    ) -> str:
        """Valida string e comprimento sem normalizar o valor recebido.

        O método rejeita tipos diferentes de texto e mede o valor após remover
        espaços apenas para comparação. Ele existe para manter o formato do
        request alinhado aos limites públicos sem duplicar a entidade.
        """
        if not isinstance(valor, str):
            raise ValueError("Campo de texto inválido.")

        limite_por_campo = {
            "titulo": TAMANHO_MAXIMO_TITULO_PROJETO,
            "descricao": TAMANHO_MAXIMO_DESCRICAO_PROJETO,
            "tecnologias": TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO,
        }
        tamanho = len(valor.strip())
        if not TAMANHO_MINIMO_TEXTO_PROJETO <= tamanho <= limite_por_campo[info.field_name]:
            raise ValueError("Tamanho de campo inválido.")
        return valor


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class ProjetoAcademicoResposta(BaseModel):
    """Define os campos públicos devolvidos ao criar um projeto.

    O DTO contém UUIDs e textos primitivos extraídos explicitamente da entidade.
    Ele existe para estabilizar o contrato HTTP sem serializar o objeto Domain.
    """

    id: UUID
    usuario_id: UUID
    titulo: str
    descricao: str
    tecnologias: str


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
def criar_router(
    cadastrar_projeto_academico: CadastroProjetoAcademicoExecutor | None,
) -> APIRouter:
    """Registra o endpoint de cadastro de projeto acadêmico.

    O handler lê JSON sem deixar erros de validação refletirem valores
    recebidos, deriva o proprietário de ``request.state`` e traduz falhas para
    HTTP. Ele existe para expor o caso de uso com propriedade segura.
    """
    router = APIRouter()

    @router.post(
        "/projetos-academicos",
        response_model=ProjetoAcademicoResposta,
        status_code=status.HTTP_201_CREATED,
        responses={422: {"description": "Dados do projeto acadêmico inválidos."}},
        openapi_extra={
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": CadastroProjetoAcademicoRequisicao.model_json_schema()
                    }
                },
            }
        },
    )
    async def cadastrar(request: Request) -> ProjetoAcademicoResposta:
        """Cadastra projeto para o usuário presente no estado da requisição.

        O endpoint exige executor e UUID autenticado, valida JSON pelo DTO e
        converte a entidade para resposta explícita. Ele existe para aceitar
        somente o proprietário validado pelo middleware.
        """
        if cadastrar_projeto_academico is None:
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
            requisicao = CadastroProjetoAcademicoRequisicao.model_validate(
                await request.json()
            )
        except (JSONDecodeError, UnicodeDecodeError, ValidationError) as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Dados do projeto acadêmico inválidos.",
            ) from erro

        entrada = CadastrarProjetoAcademicoEntrada(
            usuario_id=UsuarioId(usuario_id),
            titulo=requisicao.titulo,
            descricao=requisicao.descricao,
            tecnologias=requisicao.tecnologias,
        )
        try:
            projeto = await cadastrar_projeto_academico.executar(entrada)
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Os dados do projeto acadêmico violam as regras de cadastro.",
            ) from erro

        return ProjetoAcademicoResposta(
            id=projeto.id.valor,
            usuario_id=projeto.usuario_id.valor,
            titulo=projeto.titulo,
            descricao=projeto.descricao,
            tecnologias=projeto.tecnologias,
        )

    return router
