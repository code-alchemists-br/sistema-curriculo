"""Testa as regras de domínio e invariantes de Documento e metadados."""

import unittest
from uuid import uuid4

from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import (
    TAMANHO_MAXIMO_NOME_ARQUIVO,
    TIPOS_ARQUIVO_PERMITIDOS,
    Documento,
    validar_nome_arquivo,
    validar_tipo_arquivo,
)
from backend.domain.value_objects import DocumentoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class DocumentoDominioTestCase(unittest.TestCase):
    """Verifica a integridade e validações de segurança da entidade Documento.

    A classe avalia tipos de arquivo aceitos, limites de tamanho, rejeição de
    caracteres perigosos e invariantes de construção. Ela existe para garantir que
    apenas metadados válidos e seguros componham o domínio.
    """

    def setUp(self) -> None:
        """Configura dados básicos para os testes de domínio de documento."""
        self.usuario_id = UsuarioId(uuid4())
        self.documento_id = DocumentoId(uuid4())

    def test_cria_documento_com_dados_validos(self) -> None:
        """Confirma que a entidade Documento é criada corretamente com dados válidos."""
        doc = Documento(
            id=self.documento_id,
            usuario_id=self.usuario_id,
            nome_arquivo="certificado_python.pdf",
            tipo_arquivo="application/pdf",
            url_armazenamento="https://storage.local/docs/certificado_python.pdf",
        )
        self.assertEqual(doc.id, self.documento_id)
        self.assertEqual(doc.usuario_id, self.usuario_id)
        self.assertEqual(doc.nome_arquivo, "certificado_python.pdf")
        self.assertEqual(doc.tipo_arquivo, "application/pdf")
        self.assertEqual(
            doc.url_armazenamento,
            "https://storage.local/docs/certificado_python.pdf",
        )

    def test_aceita_tipos_de_arquivo_permitidos(self) -> None:
        """Confirma que PDF, PNG e JPEG são aceitos na validação."""
        for tipo in TIPOS_ARQUIVO_PERMITIDOS:
            self.assertEqual(validar_tipo_arquivo(tipo), tipo)

    def test_rejeita_tipo_de_arquivo_nao_permitido(self) -> None:
        """Confirma que extensões ou MIME types executáveis são rejeitados."""
        tipos_invalidos = [
            "application/x-sh",
            "application/x-msdownload",
            "text/html",
            "video/mp4",
            "exe",
        ]
        for tipo in tipos_invalidos:
            with self.assertRaises(RegraDeDominioViolada):
                validar_tipo_arquivo(tipo)

    def test_rejeita_nome_de_arquivo_vazio_ou_com_caracteres_de_controle(self) -> None:
        """Confirma que nomes vazios ou com controle disparam RegraDeDominioViolada."""
        nomes_invalidos = ["", "   ", "doc\x00.pdf", "doc\n.pdf"]
        for nome in nomes_invalidos:
            with self.assertRaises(RegraDeDominioViolada):
                validar_nome_arquivo(nome)

    def test_rejeita_nome_com_tentativa_de_path_traversal(self) -> None:
        """Confirma que barras e sequências '..' são rejeitadas para evitar Path Traversal."""
        nomes_perigosos = [
            "../doc.pdf",
            "../../etc/passwd",
            "subpasta/doc.pdf",
            "subpasta\\doc.pdf",
        ]
        for nome in nomes_perigosos:
            with self.assertRaises(RegraDeDominioViolada):
                validar_nome_arquivo(nome)

    def test_rejeita_nome_de_arquivo_muito_longo(self) -> None:
        """Confirma que nomes acima do tamanho máximo são rejeitados."""
        nome_longo = "a" * (TAMANHO_MAXIMO_NOME_ARQUIVO + 1) + ".pdf"
        with self.assertRaises(RegraDeDominioViolada):
            validar_nome_arquivo(nome_longo)

    def test_rejeita_url_armazenamento_vazia(self) -> None:
        """Confirma que a URL de armazenamento não pode ser vazia."""
        with self.assertRaises(RegraDeDominioViolada):
            Documento(
                id=self.documento_id,
                usuario_id=self.usuario_id,
                nome_arquivo="doc.pdf",
                tipo_arquivo="application/pdf",
                url_armazenamento="   ",
            )
