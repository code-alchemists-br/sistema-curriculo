"""Exercita disco temporário para verificar isolamento e configuração do adapter #204."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from backend.infrastructure.storage.armazenador_documentos_local import (
    ArmazenadorDocumentosLocal,
)


class ArmazenamentoLocal204TestCase(unittest.IsolatedAsyncioTestCase):
    """Grava arquivos reais em diretórios isolados para verificar o contrato do storage."""

    async def test_nome_fisico_independe_do_nome_enviado(self):
        """Usa nomes longos e caminhos hostis para impedir que metadados decidam o destino físico."""
        with TemporaryDirectory() as raiz:
            destino = Path(raiz) / "privado"
            storage = ArmazenadorDocumentosLocal(destino, "local://documentos")
            for nome in ("á" * 250 + ".pdf", "../../escape.pdf", "C:\\escape.pdf"):
                with self.subTest(nome=nome):
                    referencia = await storage.armazenar(
                        b"conteudo", nome, "application/pdf"
                    )
                    chave = referencia.removeprefix("local://documentos/")
                    self.assertRegex(chave, r"^[a-f0-9]{32}$")
                    self.assertEqual((destino / chave).read_bytes(), b"conteudo")
            self.assertEqual(len(list(destino.iterdir())), 3)
            self.assertEqual(list(Path(raiz).iterdir()), [destino])

    async def test_mesmo_nome_nao_sobrescreve_e_diretorios_sao_independentes(self):
        """Compara conteúdos após gravações repetidas para preservar arquivos e configuração local."""
        with TemporaryDirectory() as raiz:
            a = ArmazenadorDocumentosLocal(Path(raiz) / "a", "local://a")
            b = ArmazenadorDocumentosLocal(Path(raiz) / "b", "local://b")
            refs = [
                await a.armazenar(dado, "doc.pdf", "application/pdf")
                for dado in (b"a", b"b")
            ]
            await b.armazenar(b"c", "doc.pdf", "application/pdf")
            self.assertNotEqual(*refs)
            self.assertEqual(
                sorted(p.read_bytes() for p in (Path(raiz) / "a").iterdir()),
                [b"a", b"b"],
            )
            self.assertEqual(
                [p.read_bytes() for p in (Path(raiz) / "b").iterdir()], [b"c"]
            )
