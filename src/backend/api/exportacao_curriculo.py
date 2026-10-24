"""Expõe o download do currículo exportado em DOCX por HTTP autenticado.

O módulo converte as identidades da rota em entrada da Application, invoca o
caso de uso de exportação e devolve os bytes com tipo MIME e nome de arquivo
corretos, traduzindo ausência em 404 e falha de geração em 500. Ele existe para
atender ao UC08 e ao CT-RF09-05 sem levar regras de conteúdo à API.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response, status

from backend.api.download import cabecalhos_de_download
from backend.application.exportacao_curriculo import (
    FORMATO_DOCX,
    ArquivoCurriculoExportado,
    ExportarCurriculoEntrada,
    FalhaGeracaoArquivoCurriculo,
)
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain.value_objects import CurriculoId, UsuarioId

CAMINHO_EXPORTACAO_DOCX = "/estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/docx"
MENSAGEM_FALHA_GERACAO = "Não foi possível gerar o arquivo. Tente novamente."


class ExportacaoCurriculoExecutor(Protocol):
    """Define a exportação de currículo consumida pela fronteira HTTP.

    O contrato recebe a entrada tipada e devolve o arquivo pronto, sem expor
    prévia, documento renderizado ou biblioteca de formato. Ele existe para
    permitir injeção do caso de uso e testes isolados da rota.
    """

    async def executar(self, entrada: ExportarCurriculoEntrada) -> ArquivoCurriculoExportado:
        """Exporta a versão do estudante e devolve bytes, nome e tipo MIME.

        A implementação garante a propriedade da versão e a validade do arquivo.
        O método existe para que o handler apenas monte a resposta HTTP.
        """


def criar_router(exportar_docx: ExportacaoCurriculoExecutor | None) -> APIRouter:
    """Cria a rota de download do currículo em DOCX.

    A função registra um GET autenticado que exige o principal da sessão,
    delega ao executor e responde com o arquivo e cabeçalhos de download
    privados. Ela existe para compor a exportação na camada externa.
    """
    router = APIRouter()

    @router.get(
        CAMINHO_EXPORTACAO_DOCX,
        response_class=Response,
        responses={
            200: {
                "description": "Arquivo DOCX do currículo.",
                "content": {FORMATO_DOCX.tipo_mime: {"schema": {"type": "string", "format": "binary"}}},
            },
            404: {"description": "Versão de currículo não encontrada."},
            500: {"description": MENSAGEM_FALHA_GERACAO},
            503: {"description": "Exportação indisponível."},
        },
    )
    async def exportar(usuario_id: UUID, curriculo_id: UUID, request: Request) -> Response:
        """Gera e devolve o DOCX da versão de currículo do estudante autenticado.

        O handler exige executor e principal da sessão, usa a identidade da
        sessão (o middleware já recusa outro estudante na URL), converte
        ausência em 404 e falha de geração em 500 com mensagem genérica, e
        responde com o tipo MIME do DOCX e ``Content-Disposition`` de anexo.
        Ele existe para que o navegador baixe um arquivo válido com nome legível.
        """
        if exportar_docx is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Exportação indisponível.",
            )
        principal = getattr(request.state, "usuario_id", None)
        if not isinstance(principal, UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária.",
            )
        try:
            arquivo = await exportar_docx.executar(
                ExportarCurriculoEntrada(
                    usuario_id=UsuarioId(principal),
                    curriculo_id=CurriculoId(curriculo_id),
                )
            )
        except CurriculoNaoEncontrado as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Versão de currículo não encontrada.",
            ) from erro
        except FalhaGeracaoArquivoCurriculo as erro:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=MENSAGEM_FALHA_GERACAO,
            ) from erro
        return Response(
            content=arquivo.conteudo,
            media_type=arquivo.tipo_mime,
            headers=cabecalhos_de_download(arquivo.nome_arquivo, "curriculo"),
        )

    return router
