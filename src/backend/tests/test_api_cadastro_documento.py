"""Testa unitariamente a fronteira HTTP de cadastro e armazenamento de documentos complementares."""

import unittest
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from starlette.requests import Request

from backend.api.documento import CadastroDocumentoRequisicao, criar_router
from backend.api.factory import create_app
from backend.application.cadastro_documento import ArmazenarDocumentoEntrada
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import Documento
from backend.domain.value_objects import DocumentoId, UsuarioId

ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_DOCUMENTO = UUID("00000000-0000-0000-0000-0000000000d1")


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class CadastroDocumentoStub:
    """Substitui o caso de uso por comportamento determinístico em memória."""

    def __init__(self, erro_dominio: str | None = None) -> None:
        self.erro_dominio = erro_dominio
        self.entradas: list[ArmazenarDocumentoEntrada] = []

    async def executar(self, entrada: ArmazenarDocumentoEntrada) -> Documento:
        self.entradas.append(entrada)
        if self.erro_dominio is not None:
            raise RegraDeDominioViolada(self.erro_dominio)
        return Documento(
            id=DocumentoId(ID_DOCUMENTO),
            usuario_id=entrada.usuario_id,
            nome_arquivo=entrada.nome_arquivo,
            tipo_arquivo=entrada.tipo_arquivo,
            url_armazenamento=f"https://storage.fake/{entrada.nome_arquivo}",
        )


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
def _rota(router: APIRouter) -> Any:
    """Obtém o endpoint POST de documentos diretamente da tabela de rotas."""
    for rota in router.routes:
        if getattr(rota, "path", None) == "/documentos" and "POST" in getattr(
            rota, "methods", set()
        ):
            return rota.endpoint
    raise AssertionError("Rota POST /documentos não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
def _request(usuario_id: UUID | None) -> Request:
    """Constrói uma requisição mínima com o principal opcional no estado."""
    request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/documentos",
            "headers": [],
        }
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class CadastroDocumentoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução entre transporte HTTP e executor de armazenamento de documento."""

    async def test_vincula_o_documento_ao_principal_autenticado(self) -> None:
        """Confirma que o documento é criado com o UUID do usuário autenticado."""
        executor = CadastroDocumentoStub()
        cadastrar = _rota(criar_router(executor))

        resposta = await cadastrar(
            CadastroDocumentoRequisicao(
                nome_arquivo="diploma.pdf",
                tipo_arquivo="application/pdf",
                conteudo_base64="dGVzdGU=",
            ),
            _request(ID_USUARIO),
        )

        self.assertEqual(resposta.id, ID_DOCUMENTO)
        self.assertEqual(resposta.usuario_id, ID_USUARIO)
        self.assertEqual(resposta.nome_arquivo, "diploma.pdf")
        self.assertEqual(resposta.tipo_arquivo, "application/pdf")
        self.assertEqual(resposta.url_armazenamento, "https://storage.fake/diploma.pdf")
        self.assertEqual(len(executor.entradas), 1)
        self.assertEqual(executor.entradas[0].usuario_id, UsuarioId(ID_USUARIO))

    async def test_retorna_503_quando_executor_nao_fornecido(self) -> None:
        """Confirma que ausência de executor gera 503 Service Unavailable."""
        cadastrar = _rota(criar_router(None))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroDocumentoRequisicao(
                    nome_arquivo="diploma.pdf",
                    tipo_arquivo="application/pdf",
                    conteudo_base64="dGVzdGU=",
                ),
                _request(ID_USUARIO),
            )
        self.assertEqual(
            contexto.exception.status_code, status.HTTP_503_SERVICE_UNAVAILABLE
        )
        self.assertEqual(contexto.exception.detail, "Cadastro indisponível.")

    async def test_retorna_401_quando_usuario_nao_autenticado(self) -> None:
        """Confirma que requisição sem sessão válida no state gera 401 Unauthorized."""
        executor = CadastroDocumentoStub()
        cadastrar = _rota(criar_router(executor))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroDocumentoRequisicao(
                    nome_arquivo="diploma.pdf",
                    tipo_arquivo="application/pdf",
                    conteudo_base64="dGVzdGU=",
                ),
                _request(None),
            )
        self.assertEqual(contexto.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(contexto.exception.detail, "Autenticação necessária.")

    async def test_retorna_422_quando_regra_de_dominio_violada(self) -> None:
        """Confirma que falha de domínio é traduzida para 422 Unprocessable Content."""
        executor = CadastroDocumentoStub(erro_dominio="Tipo de arquivo não permitido.")
        cadastrar = _rota(criar_router(executor))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroDocumentoRequisicao(
                    nome_arquivo="script.sh",
                    tipo_arquivo="application/x-sh",
                    conteudo_base64="dGVzdGU=",
                ),
                _request(ID_USUARIO),
            )
        self.assertEqual(
            contexto.exception.status_code,
            status.HTTP_422_UNPROCESSABLE_CONTENT,
        )
        self.assertEqual(contexto.exception.detail, "Tipo de arquivo não permitido.")

    def test_fabrica_registra_rota_de_documento(self) -> None:
        """Confirma que create_app registra a rota /documentos."""
        app = create_app()
        self.assertIn("/documentos", app.openapi()["paths"])
