"""Testa a persistência e mapeamentos de Documento no SQLAlchemy e armazenamento local."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from backend.domain.itens_perfil import Documento
from backend.domain.value_objects import DocumentoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.documento import (
    DocumentoRegistro,
    para_documento,
    para_registro,
)
from backend.infrastructure.storage.armazenador_documentos_local import (
    ArmazenadorDocumentosLocal,
)


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class DocumentoInfraestruturaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica os mapeamentos ORM de documentos e o armazenamento em sistema de arquivos."""

    def test_conversao_bidirecional_documento_e_registro(self) -> None:
        """Confirma que a conversão entre entidade de domínio e DocumentoRegistro é simétrica."""
        doc_original = Documento(
            id=DocumentoId(uuid4()),
            usuario_id=UsuarioId(uuid4()),
            nome_arquivo="historico.pdf",
            tipo_arquivo="application/pdf",
            url_armazenamento="https://storage.local/historico.pdf",
        )

        registro = para_registro(doc_original)
        self.assertIsInstance(registro, DocumentoRegistro)
        self.assertEqual(registro.id, doc_original.id.valor)
        self.assertEqual(registro.usuario_id, doc_original.usuario_id.valor)
        self.assertEqual(registro.nome_arquivo, doc_original.nome_arquivo)
        self.assertEqual(registro.tipo_arquivo, doc_original.tipo_arquivo)
        self.assertEqual(registro.url_armazenamento, doc_original.url_armazenamento)

        doc_reconstruido = para_documento(registro)
        self.assertEqual(doc_reconstruido, doc_original)

    async def test_armazenador_local_grava_arquivo_em_disco(self) -> None:
        """Confirma que ArmazenadorDocumentosLocal persiste o conteúdo binário e gera URL."""
        with TemporaryDirectory() as temp_dir:
            armazenador = ArmazenadorDocumentosLocal(
                diretorio_base=temp_dir,
                url_prefixo="https://storage.local/arquivos",
            )
            conteudo = b"%PDF-1.4 arquivo binario teste"
            url = await armazenador.armazenar(
                conteudo=conteudo,
                nome_arquivo="certificado.pdf",
                tipo_arquivo="application/pdf",
            )

            self.assertTrue(url.startswith("https://storage.local/arquivos/"))
            self.assertRegex(url.rsplit("/", 1)[-1], r"^[a-f0-9]{32}$")

            # Confirma presença no diretório
            arquivos = list(Path(temp_dir).iterdir())
            self.assertEqual(len(arquivos), 1)
            self.assertEqual(arquivos[0].read_bytes(), conteudo)
