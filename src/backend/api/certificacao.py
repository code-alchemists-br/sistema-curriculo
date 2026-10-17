"""Expõe o cadastro autenticado de certificações por HTTP.

O módulo traduz DTOs HTTP para a entrada existente da Application e converte a
entidade resultante em uma resposta pública. Ele existe para disponibilizar o
cadastro sem revelar modelos de domínio ou aceitar o proprietário do cliente.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, ValidationInfo, field_validator

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
from backend.application.cadastro_certificacao import (
    CadastrarCertificacaoEntrada,
    CertificacaoJaCadastrada,
)
from backend.domain import (
    Certificacao,
    RegraDeDominioViolada,
    normalizar_texto_certificacao,
)
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class CadastroCertificacaoRequisicao(BaseModel):
    """Representa os campos externos necessários para cadastrar uma certificação.

    O DTO exige os dois textos, rejeita tipos não textuais, caracteres de
    controle e tamanhos fora de 1 a 200 após aparar espaços externos, usando a
    mesma regra do domínio, e mantém o dono fora do payload. Ele existe para
    barrar requisições malformadas na fronteira HTTP, antes do caso de uso, e
    impedir que o cliente escolha outro proprietário.
    """

    nome: str
    organizacao_emissora: str

    @field_validator("nome", "organizacao_emissora", mode="before")
    @classmethod
    def validar_texto_certificacao(cls, valor: object, info: ValidationInfo) -> str:
        """Valida e apara um campo textual da requisição pela regra do domínio.

        O validador recebe o valor bruto, delega a checagem de tipo, controle e
        tamanho a ``normalizar_texto_certificacao`` e converte a falha em erro
        de validação do Pydantic. Ele existe para responder 422 na fronteira
        sem duplicar os limites definidos pela entidade.
        """
        campo = "nome" if info.field_name == "nome" else "organização emissora"
        try:
            return normalizar_texto_certificacao(valor, campo)  # type: ignore[arg-type]
        except RegraDeDominioViolada as erro:
            raise ValueError(str(erro)) from erro


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class CertificacaoResposta(BaseModel):
    """Representa a certificação pública devolvida após seu cadastro.

    O DTO extrai valores primitivos da entidade validada, sem serializá-la
    diretamente. Ele existe para tornar o contrato HTTP independente da
    representação e dos value objects internos do domínio.
    """

    id: UUID
    usuario_id: UUID
    nome: str
    organizacao_emissora: str


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class CadastroCertificacaoExecutor(Protocol):
    """Define o contrato de cadastro consumido pela fronteira HTTP.

    O protocolo recebe o comando tipado e devolve a entidade criada, sem
    revelar persistência à API. Ele existe para permitir injeção do caso de uso
    e teste isolado da tradução de transporte.
    """

    async def executar(
        self, entrada: CadastrarCertificacaoEntrada
    ) -> Certificacao:
        """Cadastra uma certificação para o proprietário autenticado.

        Implementações aplicam invariantes e persistência por contratos
        internos. O método existe para manter o handler HTTP independente do
        caso de uso concreto e de seus adapters.
        """


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
def criar_router(
    cadastrar_certificacao: CadastroCertificacaoExecutor | None,
) -> APIRouter:
    """Cria a rota protegida de criação de certificações.

    A fábrica registra um handler que obtém o proprietário do estado da
    requisição, converte o DTO e traduz falhas conhecidas em HTTP. Ela existe
    para manter o transporte fino e depender apenas do executor injetado.
    """
    router = APIRouter()

    @router.post(
        "/certificacoes",
        response_model=CertificacaoResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def cadastrar(
        requisicao: CadastroCertificacaoRequisicao,
        request: Request,
    ) -> CertificacaoResposta:
        """Cadastra a certificação para a identidade autenticada da requisição.

        O handler exige executor e UUID instalados pelo mecanismo existente,
        cria a entrada interna e apresenta duplicidade como 409 e violações de
        domínio como 422 com mensagem genérica, sem repetir o texto interno da
        regra. Ele existe para preservar a propriedade do dado e a resposta
        pública do endpoint.
        """
        if cadastrar_certificacao is None:
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
            certificacao = await cadastrar_certificacao.executar(
                CadastrarCertificacaoEntrada(
                    usuario_id=UsuarioId(usuario_id),
                    nome=requisicao.nome,
                    organizacao_emissora=requisicao.organizacao_emissora,
                )
            )
        except CertificacaoJaCadastrada as erro:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A certificação já está cadastrada.",
            ) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="A certificação informada viola as regras de cadastro.",
            ) from erro
        return CertificacaoResposta(
            id=certificacao.id.valor,
            usuario_id=certificacao.usuario_id.valor,
            nome=certificacao.nome,
            organizacao_emissora=certificacao.organizacao_emissora,
        )

    return router
