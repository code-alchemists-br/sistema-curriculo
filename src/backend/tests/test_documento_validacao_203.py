"""Observa efeitos por portas substituídas para provar validação anterior ao storage."""

import base64
import unittest
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from backend.application.cadastro_documento import (
    ArmazenarDocumento,
    ArmazenarDocumentoEntrada,
)
from backend.application.ports import (
    ArmazenadorDocumentos,
    GeradorDocumentoId,
    RepositorioDocumento,
)
from backend.domain import DocumentoId, RegraDeDominioViolada, UsuarioId
from backend.domain.itens_perfil import TAMANHO_MAXIMO_DOCUMENTO_BYTES


class ValidacaoDocumento203TestCase(unittest.IsolatedAsyncioTestCase):
    """Inspeciona efeitos com doubles tipados para impedir arquivos rejeitados em disco."""

    async def test_metadados_invalidos_nao_chegam_ao_armazenamento(self):
        """Envia tipo e nome inválidos ao caso de uso para provar ausência de escrita."""
        for nome, tipo in (
            ("doc.exe", "application/x-msdownload"),
            ("../doc.pdf", "application/pdf"),
        ):
            with self.subTest(nome=nome, tipo=tipo):
                storage = AsyncMock(spec=ArmazenadorDocumentos)
                storage.armazenar.return_value = "chave"
                repo = AsyncMock(spec=RepositorioDocumento)
                gerador = Mock(spec=GeradorDocumentoId)
                gerador.gerar.return_value = DocumentoId(UUID(int=1))
                caso = ArmazenarDocumento(repo, gerador, storage)
                with self.assertRaises(RegraDeDominioViolada):
                    await caso.executar(
                        ArmazenarDocumentoEntrada(
                            UsuarioId(UUID(int=2)), nome, tipo, "WA=="
                        )
                    )
                storage.armazenar.assert_not_awaited()
                repo.salvar.assert_not_awaited()

    async def test_limite_inclusivo_e_rejeicoes_sem_efeitos(self):
        """Exercita limite exato, excesso e Base64 inválido para preservar o contrato de tamanho."""
        for tamanho in (
            TAMANHO_MAXIMO_DOCUMENTO_BYTES,
            TAMANHO_MAXIMO_DOCUMENTO_BYTES + 1,
            0,
            -1,
        ):
            with self.subTest(tamanho=tamanho):
                storage = AsyncMock(spec=ArmazenadorDocumentos)
                storage.armazenar.return_value = "chave"
                repo = AsyncMock(spec=RepositorioDocumento)
                gerador = Mock(spec=GeradorDocumentoId)
                gerador.gerar.return_value = DocumentoId(UUID(int=1))
                caso = ArmazenarDocumento(repo, gerador, storage)
                conteudo = (
                    base64.b64encode(b"X" * max(0, tamanho)).decode()
                    if tamanho >= 0
                    else "!"
                )
                entrada = ArmazenarDocumentoEntrada(
                    UsuarioId(UUID(int=2)), "doc.pdf", "application/pdf", conteudo
                )
                if tamanho == TAMANHO_MAXIMO_DOCUMENTO_BYTES:
                    await caso.executar(entrada)
                    storage.armazenar.assert_awaited_once()
                    repo.salvar.assert_awaited_once()
                else:
                    with self.assertRaises(RegraDeDominioViolada):
                        await caso.executar(entrada)
                    storage.armazenar.assert_not_awaited()
                    repo.salvar.assert_not_awaited()
