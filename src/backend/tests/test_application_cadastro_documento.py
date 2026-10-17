"""Testa o caso de uso ArmazenarDocumento e suas validações de aplicação."""

import base64
import unittest
from uuid import uuid4

from backend.application.cadastro_documento import (
    ArmazenarDocumento,
    ArmazenarDocumentoEntrada,
)
from backend.application.ports import (
    ArmazenadorDocumentos,
    GeradorDocumentoId,
    RepositorioDocumento,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import TAMANHO_MAXIMO_DOCUMENTO_BYTES, Documento
from backend.domain.value_objects import DocumentoId, UsuarioId


# Doubles em memória para testes unitários isolados
# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class GeradorDocumentoIdFake(GeradorDocumentoId):
    """Gera IDs determinísticos para documentos em testes."""

    def __init__(self, id_fixo: DocumentoId | None = None) -> None:
        self.proximo_id = id_fixo or DocumentoId(uuid4())

    def gerar(self) -> DocumentoId:
        return self.proximo_id


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class RepositorioDocumentoEmMemoria(RepositorioDocumento):
    """Simula a persistência de documentos em memória."""

    def __init__(self) -> None:
        self.documentos: dict[DocumentoId, Documento] = {}

    async def salvar(self, documento: Documento) -> None:
        self.documentos[documento.id] = documento

    async def obter_por_id(self, documento_id: DocumentoId) -> Documento | None:
        return self.documentos.get(documento_id)


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class ArmazenadorDocumentosFake(ArmazenadorDocumentos):
    """Simula o armazenamento de arquivos binários em memória."""

    def __init__(self) -> None:
        self.arquivos_salvos: list[dict[str, object]] = []

    async def armazenar(
        self,
        conteudo: bytes,
        nome_arquivo: str,
        tipo_arquivo: str,
    ) -> str:
        self.arquivos_salvos.append(
            {
                "conteudo": conteudo,
                "nome_arquivo": nome_arquivo,
                "tipo_arquivo": tipo_arquivo,
            }
        )
        return f"https://storage.fake/{nome_arquivo}"


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class ArmazenarDocumentoCasoDeUsoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a orquestração do caso de uso ArmazenarDocumento.

    A classe avalia o fluxo de decodificação Base64, validação de tamanho, gravação
    no storage e persistência no repositório. Ela existe para testar a camada Application.
    """

    def setUp(self) -> None:
        self.usuario_id = UsuarioId(uuid4())
        self.documento_id = DocumentoId(uuid4())
        self.repositorio = RepositorioDocumentoEmMemoria()
        self.gerador_id = GeradorDocumentoIdFake(self.documento_id)
        self.armazenador = ArmazenadorDocumentosFake()
        self.caso_de_uso = ArmazenarDocumento(
            repositorio_documento=self.repositorio,
            gerador_documento_id=self.gerador_id,
            armazenador_documentos=self.armazenador,
        )

    async def test_armazena_documento_com_sucesso(self) -> None:
        """Confirma que o caso de uso decodifica o base64, salva no storage e persiste."""
        conteudo_original = b"%PDF-1.4 conteudo de teste"
        b64 = base64.b64encode(conteudo_original).decode("ascii")

        entrada = ArmazenarDocumentoEntrada(
            usuario_id=self.usuario_id,
            nome_arquivo="comprovante.pdf",
            tipo_arquivo="application/pdf",
            conteudo_base64=b64,
        )

        doc = await self.caso_de_uso.executar(entrada)

        self.assertEqual(doc.id, self.documento_id)
        self.assertEqual(doc.usuario_id, self.usuario_id)
        self.assertEqual(doc.nome_arquivo, "comprovante.pdf")
        self.assertEqual(doc.url_armazenamento, "https://storage.fake/comprovante.pdf")

        # Verifica gravação no repositório
        salvo = await self.repositorio.obter_por_id(self.documento_id)
        self.assertIsNotNone(salvo)
        self.assertEqual(salvo, doc)

        # Verifica gravação no storage
        self.assertEqual(len(self.armazenador.arquivos_salvos), 1)
        self.assertEqual(
            self.armazenador.arquivos_salvos[0]["conteudo"], conteudo_original
        )

    async def test_rejeita_base64_invalido(self) -> None:
        """Confirma que strings não-Base64 disparam RegraDeDominioViolada."""
        entrada = ArmazenarDocumentoEntrada(
            usuario_id=self.usuario_id,
            nome_arquivo="teste.pdf",
            tipo_arquivo="application/pdf",
            conteudo_base64="conteudo-invalido-nao-base64!!",
        )
        with self.assertRaises(RegraDeDominioViolada):
            await self.caso_de_uso.executar(entrada)

    async def test_rejeita_conteudo_vazio(self) -> None:
        """Confirma que conteúdo vazio ou base64 de string vazia é rejeitado."""
        entrada = ArmazenarDocumentoEntrada(
            usuario_id=self.usuario_id,
            nome_arquivo="teste.pdf",
            tipo_arquivo="application/pdf",
            conteudo_base64="   ",
        )
        with self.assertRaises(RegraDeDominioViolada):
            await self.caso_de_uso.executar(entrada)

    async def test_rejeita_arquivo_acima_do_tamanho_maximo(self) -> None:
        """Confirma que arquivos com tamanho superior a 10 MB são rejeitados."""
        conteudo_gigante = b"X" * (TAMANHO_MAXIMO_DOCUMENTO_BYTES + 1)
        b64_gigante = base64.b64encode(conteudo_gigante).decode("ascii")

        entrada = ArmazenarDocumentoEntrada(
            usuario_id=self.usuario_id,
            nome_arquivo="gigante.pdf",
            tipo_arquivo="application/pdf",
            conteudo_base64=b64_gigante,
        )

        with self.assertRaises(RegraDeDominioViolada) as contexto:
            await self.caso_de_uso.executar(entrada)
        self.assertIn("excede o limite", str(contexto.exception))
