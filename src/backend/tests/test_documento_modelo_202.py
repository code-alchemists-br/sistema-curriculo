"""Verifica identidade e estado persistido para completar o modelo da #202."""

import unittest
from dataclasses import replace
from datetime import datetime, timezone
from uuid import UUID

from backend.domain import Documento, DocumentoId, RegraDeDominioViolada, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.documento import (
    para_documento,
    para_registro,
)


class ModeloDocumento202TestCase(unittest.TestCase):
    """Compara estados e rejeições com valores fixos para proteger o agregado persistido."""

    def test_rejeita_identidades_nao_tipadas(self):
        """Constrói documentos com identidades inválidas para impedir proprietários sem contrato."""
        dados = dict(
            id=DocumentoId(UUID(int=1)),
            usuario_id=UsuarioId(UUID(int=2)),
            nome_arquivo="doc.pdf",
            tipo_arquivo="application/pdf",
            url_armazenamento="chave",
        )
        for campo in ("id", "usuario_id"):
            for valor in (None, UUID(int=3), "id"):
                with (
                    self.subTest(campo=campo, valor=valor),
                    self.assertRaises(RegraDeDominioViolada),
                ):
                    Documento(**(dados | {campo: valor}))

    def test_mapeamento_preserva_estado_de_exclusao(self):
        """Reconstrói registro excluído e ativo para impedir perda de estado entre camadas."""
        documento = Documento(
            DocumentoId(UUID(int=1)),
            UsuarioId(UUID(int=2)),
            "doc.pdf",
            "application/pdf",
            "chave",
        )
        registro = para_registro(documento)
        instante = datetime(2026, 10, 18, tzinfo=timezone.utc)
        registro.deleted_at = instante
        reconstruido = para_documento(registro)
        self.assertEqual(getattr(reconstruido, "deleted_at", None), instante)
        self.assertEqual(para_registro(reconstruido).deleted_at, instante)
        self.assertIsNone(documento.deleted_at)

    def test_rejeita_estado_exclusao_sem_instante_tipado(self):
        """Recusa carimbos não temporais via construtor para manter o estado de exclusão válido."""
        documento = Documento(
            DocumentoId(UUID(int=1)),
            UsuarioId(UUID(int=2)),
            "doc.pdf",
            "application/pdf",
            "chave",
        )
        self.assertTrue(hasattr(documento, "deleted_at"))
        with self.assertRaises(RegraDeDominioViolada):
            replace(documento, deleted_at="ontem")
