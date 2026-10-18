"""Implementa o armazenamento de documentos em sistema de arquivos local ou simulado.

O módulo implementa a porta ArmazenadorDocumentos gravando os bytes em disco
(ou gerando uma URI de armazenamento segura baseada em diretório configurável),
utilizando operações assíncronas encapsuladas via asyncio.to_thread para não bloquear
o loop de eventos. Ele existe para atender a porta de storage em ambientes de desenvolvimento e teste.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from uuid import uuid4

from backend.application.ports import ArmazenadorDocumentos


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class ArmazenadorDocumentosLocal(ArmazenadorDocumentos):
    """Armazena arquivos em um diretório local do sistema de arquivos.

    A classe gera um nome único de arquivo para prevenir colisões e grava o
    conteúdo em disco em uma thread delegada pelo asyncio.to_thread. Ela existe
    para fornecer uma implementação funcional e isolada de armazenamento físico.
    """

    def __init__(
        self,
        diretorio_base: Path | str = "/tmp/sistema_curriculo_documentos",
        url_prefixo: str = "https://storage.local/documentos",
    ) -> None:
        """Inicializa o armazenador com o diretório base e prefixo de URL configurados.

        O construtor converte o caminho recebido em um Path absoluto e armazena o
        prefixo de URL base. Ele existe para permitir que ambientes configurem o local de gravação.
        """
        self._diretorio_base = Path(diretorio_base)
        self._url_prefixo = url_prefixo.rstrip("/")

    def _gravar_arquivo_sincrono(self, conteudo: bytes, nome_arquivo: str) -> str:
        """Executa a gravação do arquivo em disco de forma síncrona.

        O método cria o diretório de destino se não existir, gera um prefixo UUID único
        para o arquivo para evitar sobrescrita e grava os bytes. Ele existe para ser
        executado via worker em thread.
        """
        self._diretorio_base.mkdir(parents=True, exist_ok=True)
        nome_unico = f"{uuid4().hex}_{nome_arquivo}"
        caminho_destino = self._diretorio_base / nome_unico
        caminho_destino.write_bytes(conteudo)
        return f"{self._url_prefixo}/{nome_unico}"

    async def armazenar(
        self,
        conteudo: bytes,
        nome_arquivo: str,
        tipo_arquivo: str,
    ) -> str:
        """Persiste os bytes no sistema de arquivos local de forma não bloqueante.

        O método delega a escrita do arquivo para uma thread assíncrona e devolve
        a URL/caminho resultante. Ele existe para satisfazer a porta ArmazenadorDocumentos.
        """
        return await asyncio.to_thread(
            self._gravar_arquivo_sincrono, conteudo, nome_arquivo
        )
