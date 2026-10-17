"""Testes unitários para a rota de exclusão de documento complementar."""

import unittest
from uuid import UUID

from fastapi import HTTPException, status
from starlette.requests import Request

from backend.api.documento import criar_router
from backend.api.factory import create_app
from backend.application.exclusao_documento import (
    DocumentoNaoEncontrado,
    ExcluirDocumentoEntrada,
)
from backend.domain.value_objects import DocumentoId, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_DOCUMENTO = UUID("00000000-0000-0000-0000-0000000000d1")


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
class ExcluirDocumentoStub:
    """Substituto de teste para o caso de uso ExcluirDocumento.

    A classe registra chamadas recebidas e permite simular sucesso ou falha
    configurável sem acoplar a infraestrutura ou banco de dados. Ela existe
    para fornecer controle determinístico aos testes da camada API.
    """

    def __init__(self, erro: Exception | None = None) -> None:
        """Inicializa o stub com falha opcional a ser lançada.

        O construtor armazena a exceção a ser simulada e cria a lista de chamadas.
        Ele existe para preparar o comportamento esperado em cada teste.
        """
        self.erro = erro
        self.entradas: list[ExcluirDocumentoEntrada] = []

    async def executar(self, entrada: ExcluirDocumentoEntrada) -> None:
        """Registra a entrada e lança erro ou conclui com sucesso.

        O método simula a execução assíncrona do caso de uso.
        Ele existe para validar se o handler enviou os parâmetros esperados.
        """
        self.entradas.append(entrada)
        if self.erro is not None:
            raise self.erro


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
def _request(usuario_id: UUID | None) -> Request:
    """Cria uma requisição mínima mockada para simulação do endpoint.

    A função instancia um objeto Request do Starlette injetando o usuario_id
    em request.state quando fornecido. Ela existe para testar a camada HTTP isoladamente.
    """
    request = Request(
        {
            "type": "http",
            "method": "DELETE",
            "path": f"/documentos/{ID_DOCUMENTO}",
            "headers": [],
        }
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
def _obter_endpoint_exclusao(executor: ExcluirDocumentoStub | None):
    """Localiza o endpoint DELETE do router de documentos.

    A função itera sobre as rotas registradas em criar_router e retorna o handler correspondente.
    Ela existe para permitir a chamada direta da função sem necessidade de cliente HTTP externo.
    """
    router = criar_router(excluir_documento=executor)
    for rota in router.routes:
        if getattr(
            rota, "path", None
        ) == "/documentos/{documento_id}" and "DELETE" in getattr(
            rota, "methods", set()
        ):
            return getattr(rota, "endpoint", None)
    return None


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
class TestApiExclusaoDocumento(unittest.IsolatedAsyncioTestCase):
    """Testes unitários dos endpoints HTTP de exclusão de documentos complementares.

    A classe verifica a conversão de parâmetros, tratamento de 204 No Content,
    autenticação necessária (401), recurso não encontrado (404) e indisponibilidade (503).
    Ela existe para assegurar a conformidade dos contratos da API.
    """

    async def test_exclusao_retorna_204_quando_sucesso(self) -> None:
        """Verifica que requisição válida e autenticada exclui o documento com 204.

        O teste invoca o endpoint com stub de sucesso e valida que o handler
        executa sem retornar corpo e que o caso de uso recebeu as identidades certas.
        Ele existe para garantir o comportamento padrão da rota DELETE.
        """
        stub = ExcluirDocumentoStub()
        endpoint = _obter_endpoint_exclusao(stub)
        self.assertIsNotNone(endpoint)

        requisicao = _request(ID_USUARIO)
        resposta = await endpoint(ID_DOCUMENTO, requisicao)  # type: ignore[misc]

        self.assertIsNone(resposta)
        self.assertEqual(len(stub.entradas), 1)
        self.assertEqual(stub.entradas[0].usuario_id, UsuarioId(ID_USUARIO))
        self.assertEqual(stub.entradas[0].documento_id, DocumentoId(ID_DOCUMENTO))

    async def test_retorna_401_quando_nao_autenticado(self) -> None:
        """Verifica que requisição sem sessão autenticada é rejeitada com 401.

        O teste envia requisição sem usuario_id em request.state e espera HTTPException 401.
        Ele existe para validar o controle de acesso e autenticação da rota.
        """
        stub = ExcluirDocumentoStub()
        endpoint = _obter_endpoint_exclusao(stub)
        requisicao = _request(None)

        with self.assertRaises(HTTPException) as ctx:
            await endpoint(ID_DOCUMENTO, requisicao)  # type: ignore[misc]

        self.assertEqual(ctx.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(ctx.exception.detail, "Autenticação necessária.")
        self.assertEqual(len(stub.entradas), 0)

    async def test_retorna_404_quando_documento_nao_encontrado(self) -> None:
        """Verifica que DocumentoNaoEncontrado é convertido em HTTP 404 uniforme.

        O teste configura o stub para lançar DocumentoNaoEncontrado e confirma a
        geração da resposta 404 Not Found com detalhe consistente. Ele existe para
        garantir conformidade com a política contra IDOR.
        """
        stub = ExcluirDocumentoStub(
            erro=DocumentoNaoEncontrado("Documento não encontrado.")
        )
        endpoint = _obter_endpoint_exclusao(stub)
        requisicao = _request(ID_USUARIO)

        with self.assertRaises(HTTPException) as ctx:
            await endpoint(ID_DOCUMENTO, requisicao)  # type: ignore[misc]

        self.assertEqual(ctx.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ctx.exception.detail, "Documento não encontrado.")

    async def test_retorna_503_quando_executor_nao_injetado(self) -> None:
        """Verifica que a ausência do executor resulta em 503 Service Unavailable.

        O teste cria o router com executor None e confirma o status 503.
        Ele existe para garantir estabilidade em falhas de composição.
        """
        endpoint = _obter_endpoint_exclusao(None)
        requisicao = _request(ID_USUARIO)

        with self.assertRaises(HTTPException) as ctx:
            await endpoint(ID_DOCUMENTO, requisicao)  # type: ignore[misc]

        self.assertEqual(ctx.exception.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(ctx.exception.detail, "Exclusão indisponível.")

    def test_fabrica_registra_rota_de_documento(self) -> None:
        """Verifica que create_app registra a rota de exclusão de documentos.

        O teste cria a aplicação via create_app e busca a rota DELETE /documentos/{documento_id}.
        Ele existe para garantir a integração correta do router na fábrica ASGI.
        """
        stub = ExcluirDocumentoStub()
        app = create_app(excluir_documento=stub)

        caminhos = app.openapi()["paths"]
        self.assertIn("/documentos/{documento_id}", caminhos)
        self.assertIn("delete", caminhos["/documentos/{documento_id}"])
        self.assertEqual(
            caminhos["/documentos/{documento_id}"]["delete"]["responses"]["204"][
                "description"
            ],
            "Successful Response",
        )


if __name__ == "__main__":
    unittest.main()
