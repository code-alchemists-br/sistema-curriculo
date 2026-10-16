"""Expõe o cadastro e armazenamento autenticado de documentos complementares por HTTP.

O módulo traduz o DTO da requisição HTTP para a entrada tipada da Application,
invoca o executor injetado e converte a entidade resultante em resposta pública com status 201.
Ele existe para disponibilizar o upload de documentos preservando o isolamento do domínio.
"""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from backend.application.cadastro_documento import ArmazenarDocumentoEntrada
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import Documento
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class CadastroDocumentoRequisicao(BaseModel):
    """Representa o corpo JSON da requisição de cadastro e armazenamento de documento.

    O DTO transporta o nome do arquivo, seu tipo MIME e o conteúdo binário codificado
    em Base64. Ele existe para possibilitar o envio de arquivos sem dependências multipart.
    """

    nome_arquivo: str
    tipo_arquivo: str
    conteudo_base64: str


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class DocumentoResposta(BaseModel):
    """Representa a estrutura de resposta pública devolvida após o armazenamento do documento.

    O DTO extrai os valores primitivos da entidade criada, incluindo a URL de acesso
    gerada no storage. Ele existe para desacoplar a resposta HTTP dos tipos internos de domínio.
    """

    id: UUID
    usuario_id: UUID
    nome_arquivo: str
    tipo_arquivo: str
    url_armazenamento: str


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class CadastroDocumentoExecutor(Protocol):
    """Define o contrato de execução do armazenamento de documentos consumido pela API.

    O protocolo recebe o comando tipado e devolve o Documento criado sem expor
    persistência ou storage à camada HTTP. Ele existe para viabilizar injeção de dependência e testes.
    """

    async def executar(self, entrada: ArmazenarDocumentoEntrada) -> Documento:
        """Executa a validação, upload e persistência do documento complementar.

        A implementação aplica as regras de negócio e salva o arquivo e seus metadados.
        O método existe para manter o router independente do caso de uso concreto.
        """
        ...


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
def criar_router(
    armazenar_documento: CadastroDocumentoExecutor | None,
) -> APIRouter:
    """Cria a rota POST protegida por sessão para upload de documentos complementares.

    A fábrica registra o endpoint /documentos obtendo o usuário autenticado de request.state,
    traduz violações de domínio em 422 Unprocessable Content e devolve o documento com 201 Created.
    Ela existe para isolar a infraestrutura HTTP da lógica de aplicação.
    """
    router = APIRouter()

    @router.post(
        "/documentos",
        response_model=DocumentoResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def cadastrar(
        requisicao: CadastroDocumentoRequisicao,
        request: Request,
    ) -> DocumentoResposta:
        """Cadastra e armazena o documento complementar para o usuário autenticado.

        O handler valida a presença do executor e a identidade do usuário na sessão,
        repassa os dados para o caso de uso e traduz regras de negócio violadas em 422.
        Ele existe para prover o ponto de entrada HTTP para armazenamento de documentos.
        """
        if armazenar_documento is None:
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
            documento = await armazenar_documento.executar(
                ArmazenarDocumentoEntrada(
                    usuario_id=UsuarioId(usuario_id),
                    nome_arquivo=requisicao.nome_arquivo,
                    tipo_arquivo=requisicao.tipo_arquivo,
                    conteudo_base64=requisicao.conteudo_base64,
                )
            )
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(erro),
            ) from erro
        return DocumentoResposta(
            id=documento.id.valor,
            usuario_id=documento.usuario_id.valor,
            nome_arquivo=documento.nome_arquivo,
            tipo_arquivo=documento.tipo_arquivo,
            url_armazenamento=documento.url_armazenamento,
        )

    return router
