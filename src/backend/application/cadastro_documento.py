"""Orquestra o cadastro e armazenamento assíncrono de documentos complementares.

O módulo define o DTO de entrada tipado e o caso de uso ArmazenarDocumento,
responsável por validar o tamanho do payload binário, delegar a gravação física ao
ArmazenadorDocumentos, construir a entidade de domínio e persisti-la pelo RepositorioDocumento.
Ele existe para que a aplicação realize o upload sem acoplamento a tecnologias de armazenamento.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass

from backend.application.ports import (
    ArmazenadorDocumentos,
    GeradorDocumentoId,
    RepositorioDocumento,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import (
    TAMANHO_MAXIMO_DOCUMENTO_BYTES,
    Documento,
    validar_nome_arquivo,
    validar_tipo_arquivo,
)
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
@dataclass(frozen=True, slots=True)
class ArmazenarDocumentoEntrada:
    """Encapsula os dados necessários para cadastrar e armazenar um documento complementar.

    A estrutura imutável transporta a identidade do usuário autenticado, os metadados
    do arquivo e seu conteúdo codificado em Base64. Ela existe para desacoplar a camada
    Application de formulários multipart ou protocolos de transporte HTTP.
    """

    usuario_id: UsuarioId
    nome_arquivo: str
    tipo_arquivo: str
    conteudo_base64: str


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class ArmazenarDocumento:
    """Coordena o fluxo de validação, armazenamento e persistência de documentos.

    O caso de uso decodifica o Base64, valida o limite máximo de tamanho de arquivo,
    invoca o armazenamento assíncrono do conteúdo binário, cria a entidade de domínio
    com sua nova identidade tipada e persiste o registro no repositório. Ele existe para
    centralizar as regras de aplicação ligadas ao upload de documentos complementares.
    """

    def __init__(
        self,
        repositorio_documento: RepositorioDocumento,
        gerador_documento_id: GeradorDocumentoId,
        armazenador_documentos: ArmazenadorDocumentos,
    ) -> None:
        """Injeta as portas necessárias para persistência, identificação e storage de documentos.

        O construtor armazena as dependências abstratas do núcleo, permitindo a substituição
        por fakes/doubles em testes unitários isolados. Ele existe para preservar a inversão
        de dependência no caso de uso.
        """
        self._repositorio = repositorio_documento
        self._gerador_id = gerador_documento_id
        self._armazenador = armazenador_documentos

    async def executar(self, entrada: ArmazenarDocumentoEntrada) -> Documento:
        """Processa o upload do documento e persiste seus metadados.

        O método valida nome e MIME antes do storage, decodifica Base64 e rejeita payloads vazios ou maiores
        que o limite permitido (10 MB), envia os bytes para o armazenador configurado,
        gera um novo DocumentoId e salva a entidade no repositório. Ele existe para fornecer
        armazenamento validado e registro no perfil. Não há transação distribuída:
        falhas de persistência após a gravação ainda podem deixar arquivos órfãos.
        """
        nome_arquivo = validar_nome_arquivo(entrada.nome_arquivo)
        tipo_arquivo = validar_tipo_arquivo(entrada.tipo_arquivo)
        if not entrada.conteudo_base64 or not entrada.conteudo_base64.strip():
            raise RegraDeDominioViolada("O conteúdo do documento não pode ser vazio.")

        try:
            conteudo_bytes = base64.b64decode(entrada.conteudo_base64, validate=True)
        except Exception as erro:
            raise RegraDeDominioViolada(
                "O conteúdo do documento deve ser uma string Base64 válida."
            ) from erro

        if not conteudo_bytes:
            raise RegraDeDominioViolada("O conteúdo do documento não pode ser vazio.")

        if len(conteudo_bytes) > TAMANHO_MAXIMO_DOCUMENTO_BYTES:
            raise RegraDeDominioViolada(
                f"O tamanho do arquivo excede o limite máximo permitido de {TAMANHO_MAXIMO_DOCUMENTO_BYTES // (1024 * 1024)} MB."
            )

        url_armazenamento = await self._armazenador.armazenar(
            conteudo=conteudo_bytes,
            nome_arquivo=nome_arquivo,
            tipo_arquivo=tipo_arquivo,
        )

        documento_id = self._gerador_id.gerar()
        documento = Documento(
            id=documento_id,
            usuario_id=entrada.usuario_id,
            nome_arquivo=entrada.nome_arquivo,
            tipo_arquivo=entrada.tipo_arquivo,
            url_armazenamento=url_armazenamento,
        )

        await self._repositorio.salvar(documento)
        return documento
