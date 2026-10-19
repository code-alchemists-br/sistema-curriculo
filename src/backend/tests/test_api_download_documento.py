"""Testa unitariamente a rota de download de documento complementar."""

import unittest
from uuid import UUID

from fastapi import HTTPException, status
from starlette.requests import Request

# Proveniência: decision-analysis prompts/backend/20261019-110000-download-documento-complementar-v001.md#v001
from backend.api.documento import criar_router
from backend.api.factory import create_app
from backend.application.download_documento import (
    BaixarDocumentoEntrada,
    ConteudoDocumento,
)
from backend.application.exclusao_documento import DocumentoNaoEncontrado
from backend.domain.value_objects import DocumentoId, UsuarioId

ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_DOCUMENTO = UUID("00000000-0000-0000-0000-0000000000d1")
BYTES_DO_ARQUIVO = b"%PDF-1.4 conteudo de teste"


class BaixarDocumentoStub:
    """Substituto de teste para o caso de uso ``BaixarDocumento``.

    A classe registra as entradas recebidas e devolve o arquivo configurado ou
    lança a falha configurada. Ela existe para dar controle determinístico aos
    testes da camada de API.
    """

    def __init__(
        self,
        arquivo: ConteudoDocumento | None = None,
        erro: Exception | None = None,
    ) -> None:
        """Guarda o arquivo a devolver, a falha opcional e o histórico de entradas.

        O construtor não acessa recursos externos. Ele existe para preparar o
        comportamento esperado em cada teste.
        """
        self.arquivo = arquivo
        self.erro = erro
        self.entradas: list[BaixarDocumentoEntrada] = []

    async def executar(self, entrada: BaixarDocumentoEntrada) -> ConteudoDocumento:
        """Registra a entrada e devolve o arquivo ou lança a falha configurada.

        O método simula a execução assíncrona do caso de uso. Ele existe para
        conferir se o handler enviou os parâmetros esperados.
        """
        self.entradas.append(entrada)
        if self.erro is not None:
            raise self.erro
        assert self.arquivo is not None
        return self.arquivo


def _request(usuario_id: UUID | None) -> Request:
    """Cria uma requisição mínima com o usuário autenticado, quando informado.

    A função instancia o ``Request`` do Starlette e injeta ``usuario_id`` em
    ``request.state``. Ela existe para testar a camada HTTP sem cliente real.
    """
    request = Request(
        {"type": "http", "method": "GET", "path": f"/documentos/{ID_DOCUMENTO}", "headers": []}
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


def _endpoint(executor: BaixarDocumentoStub | None):
    """Localiza o endpoint GET do router de documentos.

    A função percorre as rotas de ``criar_router`` e devolve o handler do
    download. Ela existe para chamar a função direto, sem servidor ASGI.
    """
    router = criar_router(baixar_documento=executor)
    for rota in router.routes:
        if getattr(rota, "path", None) == "/documentos/{documento_id}" and "GET" in getattr(
            rota, "methods", set()
        ):
            return rota.endpoint
    raise AssertionError("Rota GET /documentos/{documento_id} não encontrada.")


class DownloadDocumentoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP do download de documentos complementares.

    Os testes cobrem sucesso, cabeçalhos, autenticação, 404 uniforme, 503 e o
    registro da rota. A classe existe para proteger o contrato do download.
    """

    async def test_devolve_o_arquivo_com_tipo_e_cabecalhos_de_download(self) -> None:
        """Confirma corpo, tipo e cabeçalhos da resposta de sucesso.

        O teste chama o handler com o usuário autenticado e confere os bytes, o
        tipo, o ``Content-Disposition`` e as proteções de cache e sniffing. Ele
        existe para garantir que o navegador baixe o arquivo corretamente.
        """
        executor = BaixarDocumentoStub(
            ConteudoDocumento("rg.pdf", "application/pdf", BYTES_DO_ARQUIVO)
        )

        resposta = await _endpoint(executor)(
            documento_id=ID_DOCUMENTO, request=_request(ID_USUARIO)
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.body, BYTES_DO_ARQUIVO)
        self.assertEqual(resposta.media_type, "application/pdf")
        self.assertIn('filename="rg.pdf"', resposta.headers["content-disposition"])
        self.assertTrue(resposta.headers["content-disposition"].startswith("attachment"))
        self.assertEqual(resposta.headers["x-content-type-options"], "nosniff")
        self.assertEqual(resposta.headers["cache-control"], "private, no-store")
        self.assertEqual(
            executor.entradas,
            [
                BaixarDocumentoEntrada(
                    usuario_id=UsuarioId(ID_USUARIO),
                    documento_id=DocumentoId(ID_DOCUMENTO),
                )
            ],
        )

    async def test_nome_com_acento_vai_codificado_no_cabecalho(self) -> None:
        """Confirma a codificação de nomes com acento no ``Content-Disposition``.

        O teste baixa um arquivo com acento e confere o nome UTF-8 codificado e
        a alternativa ASCII. Ele existe para que o cabeçalho HTTP nunca quebre
        com caracteres fora do ASCII.
        """
        executor = BaixarDocumentoStub(
            ConteudoDocumento("Currículo.pdf", "application/pdf", BYTES_DO_ARQUIVO)
        )

        resposta = await _endpoint(executor)(
            documento_id=ID_DOCUMENTO, request=_request(ID_USUARIO)
        )

        cabecalho = resposta.headers["content-disposition"]
        self.assertIn("filename*=UTF-8''Curr%C3%ADculo.pdf", cabecalho)
        self.assertIn('filename="Currculo.pdf"', cabecalho)

    async def test_retorna_401_sem_usuario_autenticado(self) -> None:
        """Confirma que a falta de sessão responde 401 sem chamar o caso de uso.

        O teste chama o handler sem usuário na requisição. Ele existe para que o
        download exija autenticação.
        """
        executor = BaixarDocumentoStub()

        with self.assertRaises(HTTPException) as contexto:
            await _endpoint(executor)(documento_id=ID_DOCUMENTO, request=_request(None))

        self.assertEqual(contexto.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(executor.entradas, [])

    async def test_retorna_404_uniforme_quando_nao_encontrado(self) -> None:
        """Confirma que documento ausente, excluído ou alheio responde 404.

        O teste faz o caso de uso lançar ``DocumentoNaoEncontrado`` e confere o
        status e a mensagem genérica. Ele existe para impedir a enumeração de
        documentos.
        """
        executor = BaixarDocumentoStub(erro=DocumentoNaoEncontrado("x"))

        with self.assertRaises(HTTPException) as contexto:
            await _endpoint(executor)(
                documento_id=ID_DOCUMENTO, request=_request(ID_USUARIO)
            )

        self.assertEqual(contexto.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(contexto.exception.detail, "Documento não encontrado.")

    async def test_retorna_503_quando_o_executor_nao_foi_injetado(self) -> None:
        """Confirma que a ausência do executor responde 503.

        O teste cria o router sem executor. Ele existe para que a composição
        incompleta falhe de forma explícita.
        """
        with self.assertRaises(HTTPException) as contexto:
            await _endpoint(None)(documento_id=ID_DOCUMENTO, request=_request(ID_USUARIO))

        self.assertEqual(
            contexto.exception.status_code, status.HTTP_503_SERVICE_UNAVAILABLE
        )

    def test_fabrica_registra_o_download_ao_lado_da_exclusao(self) -> None:
        """Confirma que a aplicação publica o download em ``/documentos/{id}``.

        O teste lê as rotas do OpenAPI gerado. Ele existe para garantir que o
        executor chega ao router pela fábrica.
        """
        caminhos = create_app().openapi()["paths"]

        self.assertIn("get", caminhos["/documentos/{documento_id}"])
        self.assertIn("delete", caminhos["/documentos/{documento_id}"])
