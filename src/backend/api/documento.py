"""Módulo de roteamento HTTP para documentos complementares do estudante.

O módulo define as rotas protegidas da API para documentos complementares,
gerenciando a extração do usuário autenticado a partir de request.state e
traduzindo exceções de negócio em códigos de resposta HTTP padronizados.
Ele existe para expor a gestão de documentos de forma segura e desacoplada.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status

from backend.application.exclusao_documento import (
    DocumentoNaoEncontrado,
    ExcluirDocumentoEntrada,
)
from backend.domain.value_objects import DocumentoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
class ExclusaoDocumentoExecutor(Protocol):
    """Protocolo de execução para o caso de uso de exclusão de documentos.

    A interface define o método executar assíncrono recebendo o DTO de entrada.
    Ela existe para que a rota HTTP dependa de uma abstração de caso de uso
    testável com mocks e doubles.
    """

    async def executar(self, entrada: ExcluirDocumentoEntrada) -> None:
        """Executa a validação e exclusão do documento complementar.

        O método recebe a entrada tipada com as identidades do usuário e documento.
        Ele existe para delegar o fluxo de negócio ao caso de uso correspondente.
        """
        ...


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
def criar_router(
    excluir_documento: ExclusaoDocumentoExecutor | None = None,
) -> APIRouter:
    """Cria e configura o roteador FastAPI para operações com documentos complementares.

    A função instancia o APIRouter e registra os endpoints protegidos, injetando
    os executores de casos de uso necessários. Ela existe para compor as rotas de documentos
    na fábrica central da aplicação.
    """
    router = APIRouter()

    # Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
    @router.delete(
        "/documentos/{documento_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def excluir(
        documento_id: UUID,
        request: Request,
    ) -> None:
        """Exclui documento complementar vinculado à sessão do estudante autenticado.

        O endpoint extrai o usuario_id validado de request.state, invoca o caso de uso
        e retorna 204 No Content sem corpo de resposta. Ele trata 503 para executor ausente,
        401 para requisições não autenticadas e 404 uniforme para documentos inexistentes
        ou de outros usuários. Ele existe para permitir a exclusão segura de documentos via HTTP.
        """
        if excluir_documento is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Exclusão indisponível.",
            )

        usuario_id = getattr(request.state, "usuario_id", None)
        if not isinstance(usuario_id, UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária.",
            )

        try:
            entrada = ExcluirDocumentoEntrada(
                usuario_id=UsuarioId(usuario_id),
                documento_id=DocumentoId(documento_id),
            )
            await excluir_documento.executar(entrada)
        except DocumentoNaoEncontrado as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Documento não encontrado.",
            ) from erro

    return router
