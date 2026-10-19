"""Testa a leitura do armazenador local de documentos, com diretório temporário."""

import tempfile
import unittest
from pathlib import Path

# Proveniência: decision-analysis prompts/backend/20261019-110000-download-documento-complementar-v001.md#v001
from backend.infrastructure.storage.armazenador_documentos_local import (
    ArmazenadorDocumentosLocal,
)

PREFIXO = "https://storage.local/documentos"


class LeituraArmazenadorLocalTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a leitura de arquivos pelo ``ArmazenadorDocumentosLocal``.

    Os testes usam um diretório temporário e conferem leitura, ausência e
    localizações maliciosas. A classe existe para proteger a regra de que só se
    lê o que o próprio armazenador gravou, dentro do diretório base.
    """

    def setUp(self) -> None:
        """Cria o diretório temporário e o armazenador que o usa como base.

        O método prepara um diretório isolado por teste e garante sua remoção.
        Ele existe para que nenhum teste toque o disco fora da área temporária.
        """
        self._temporario = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporario.cleanup)
        self.base = Path(self._temporario.name) / "documentos"
        self.armazenador = ArmazenadorDocumentosLocal(self.base, PREFIXO)

    async def test_le_de_volta_o_que_foi_armazenado(self) -> None:
        """Confirma que o conteúdo gravado é devolvido pela mesma localização.

        O teste grava um arquivo e o lê pela URL devolvida. Ele existe para
        garantir o ciclo completo de gravação e leitura.
        """
        url = await self.armazenador.armazenar(b"conteudo", "rg.pdf", "application/pdf")

        self.assertEqual(await self.armazenador.ler(url), b"conteudo")

    async def test_devolve_none_para_arquivo_inexistente(self) -> None:
        """Confirma que uma chave válida sem arquivo devolve ``None``.

        O teste lê uma chave bem formada que nunca foi gravada. Ele existe para
        que a falta do arquivo não vire exceção.
        """
        self.base.mkdir(parents=True)

        self.assertIsNone(await self.armazenador.ler(f"{PREFIXO}/{'0' * 32}"))

    async def test_devolve_none_para_localizacao_de_outro_prefixo(self) -> None:
        """Confirma que uma URL fora do prefixo configurado não é lida.

        O teste lê uma localização de outro host. Ele existe para que só
        localizações geradas por este armazenador sejam aceitas.
        """
        self.assertIsNone(
            await self.armazenador.ler(f"https://outro.exemplo/documentos/{'a' * 32}")
        )

    async def test_recusa_navegacao_de_diretorio_e_chaves_mal_formadas(self) -> None:
        """Confirma que ``..``, barras e chaves fora do padrão não leem arquivo algum.

        O teste cria um arquivo secreto fora do diretório base e tenta alcançá-lo
        por localizações maliciosas. Ele existe para impedir leitura fora da
        área de armazenamento.
        """
        self.base.mkdir(parents=True)
        (self.base.parent / "segredo").write_bytes(b"segredo")
        tentativas = (
            f"{PREFIXO}/../segredo",
            f"{PREFIXO}/..%2Fsegredo",
            f"{PREFIXO}/{'a' * 31}",
            f"{PREFIXO}/{'A' * 32}",
            f"{PREFIXO}/{'a' * 32}/extra",
            f"{PREFIXO}/",
            PREFIXO,
        )

        for url in tentativas:
            with self.subTest(url=url):
                self.assertIsNone(await self.armazenador.ler(url))
