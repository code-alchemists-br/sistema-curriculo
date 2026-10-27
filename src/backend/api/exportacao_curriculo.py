"""Expõe o download do currículo exportado em DOCX e PDF por HTTP autenticado.

O módulo converte as identidades da rota em entrada da Application, invoca o
caso de uso de exportação do formato e devolve os bytes com tipo MIME e nome de
arquivo corretos, traduzindo ausência em 404 e falha de geração em 500. Ele
existe para atender aos UC07 e UC08 e ao CT-RF09-05 sem levar regras de conteúdo
à API.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response, status

from backend.api.download import cabecalhos_de_download
from backend.application.exportacao_curriculo import (
    FORMATO_DOCX,
    # Proveniência: decision-analysis prompts/backend/20261025-100000-rota-exportacao-pdf-v001.md#v001
    FORMATO_PDF,
    ArquivoCurriculoExportado,
    ExportarCurriculoEntrada,
    FalhaGeracaoArquivoCurriculo,
    FormatoExportacao,
)
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain.value_objects import CurriculoId, UsuarioId

CAMINHO_EXPORTACAO_DOCX = "/estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/docx"
# Proveniência: decision-analysis prompts/backend/20261025-100000-rota-exportacao-pdf-v001.md#v001
CAMINHO_EXPORTACAO_PDF = "/estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/pdf"
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


# Proveniência: decision-analysis prompts/backend/20261025-100000-rota-exportacao-pdf-v001.md#v001
def _registrar_download(
    router: APIRouter,
    caminho: str,
    executor: ExportacaoCurriculoExecutor | None,
    formato: FormatoExportacao,
    nome_do_formato: str,
) -> None:
    """Registra no router o GET de download de um formato de exportação.

    A função cria o handler do formato com o executor e o tipo MIME recebidos e
    o registra no caminho informado, de modo que DOCX e PDF compartilhem a mesma
    tradução de ausência, falha e autenticação. Ela existe para que cada formato
    novo seja só um caminho, um executor e um tipo, sem copiar o handler.
    """

    @router.get(
        caminho,
        response_class=Response,
        responses={
            200: {
                "description": f"Arquivo {nome_do_formato} do currículo.",
                "content": {formato.tipo_mime: {"schema": {"type": "string", "format": "binary"}}},
            },
            404: {"description": "Versão de currículo não encontrada."},
            500: {"description": MENSAGEM_FALHA_GERACAO},
            503: {"description": "Exportação indisponível."},
        },
    )
    async def exportar(usuario_id: UUID, curriculo_id: UUID, request: Request) -> Response:
        """Gera e devolve o arquivo da versão de currículo do estudante autenticado.

        O handler exige executor e principal da sessão, usa a identidade da
        sessão (o middleware já recusa outro estudante na URL), converte
        ausência em 404 e falha de geração em 500 com mensagem genérica, e
        responde com o tipo MIME do formato e ``Content-Disposition`` de anexo.
        Ele existe para que o navegador baixe um arquivo válido com nome legível.
        """
        if executor is None:
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
            arquivo = await executor.executar(
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


def criar_router(
    exportar_docx: ExportacaoCurriculoExecutor | None,
    # Proveniência: decision-analysis prompts/backend/20261025-100000-rota-exportacao-pdf-v001.md#v001
    exportar_pdf: ExportacaoCurriculoExecutor | None = None,
) -> APIRouter:
    """Cria as rotas de download do currículo em DOCX e em PDF.

    A função registra um GET autenticado por formato, que exige o principal da
    sessão, delega ao executor do formato e responde com o arquivo e cabeçalhos
    de download privados; um formato sem executor responde 503. Ela existe para
    compor a exportação na camada externa.
    """
    router = APIRouter()
    _registrar_download(router, CAMINHO_EXPORTACAO_DOCX, exportar_docx, FORMATO_DOCX, "DOCX")
    _registrar_download(router, CAMINHO_EXPORTACAO_PDF, exportar_pdf, FORMATO_PDF, "PDF")
    return router
