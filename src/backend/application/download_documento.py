"""Caso de uso de download de documento complementar de estudante.

O módulo orquestra a verificação de propriedade e a leitura do conteúdo do
documento, devolvendo somente nome, tipo e bytes, sem a localização de
armazenamento, e tratando de forma uniforme o documento inexistente, excluído ou
de outro estudante. Ele existe para que o download seja autorizado fora do
transporte HTTP e do provedor de storage.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261019-110000-download-documento-complementar-v001.md#v001
from backend.application.exclusao_documento import DocumentoNaoEncontrado
from backend.application.ports import ArmazenadorDocumentos, RepositorioDocumento
from backend.domain.value_objects import DocumentoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261019-110000-download-documento-complementar-v001.md#v001
@dataclass(frozen=True, slots=True)
class BaixarDocumentoEntrada:
    """Encapsula os parâmetros tipados necessários para baixar um documento.

    O DTO transporta o identificador do estudante autenticado e o do documento
    pedido. Ele existe para estabelecer uma fronteira limpa entre a camada de
    transporte e a lógica de aplicação.
    """

    usuario_id: UsuarioId
    documento_id: DocumentoId


# Proveniência: decision-analysis prompts/backend/20261019-110000-download-documento-complementar-v001.md#v001
@dataclass(frozen=True, slots=True)
class ConteudoDocumento:
    """Representa o arquivo a ser entregue ao estudante, sem a localização física.

    O modelo guarda o nome, o tipo MIME e os bytes do documento e deliberadamente
    não inclui a URL de armazenamento. Ele existe para que a interface devolva o
    arquivo sem revelar o caminho em que ele está guardado.
    """

    nome_arquivo: str
    tipo_arquivo: str
    conteudo: bytes


# Proveniência: decision-analysis prompts/backend/20261019-110000-download-documento-complementar-v001.md#v001
class BaixarDocumento:
    """Entrega o conteúdo de um documento complementar do próprio estudante.

    O caso busca o documento, recusa o que não existe, está excluído ou pertence
    a outro estudante, lê o arquivo pela porta de storage e devolve nome, tipo e
    bytes. Ele existe para garantir que somente o dono baixe seu documento e que
    a localização de armazenamento nunca saia da Application.
    """

    # Proveniência: decision-analysis prompts/backend/20261019-110000-download-documento-complementar-v001.md#v001
    def __init__(
        self,
        repositorio_documento: RepositorioDocumento,
        armazenador: ArmazenadorDocumentos,
    ) -> None:
        """Recebe as portas usadas para consultar o documento e ler o arquivo.

        O construtor armazena somente abstrações internas, que podem ser
        substituídas por doubles. Ele existe para manter a orquestração
        independente da infraestrutura.
        """
        self._repositorio = repositorio_documento
        self._armazenador = armazenador

    # Proveniência: decision-analysis prompts/backend/20261019-110000-download-documento-complementar-v001.md#v001
    async def executar(self, entrada: BaixarDocumentoEntrada) -> ConteudoDocumento:
        """Valida a propriedade do documento e devolve o arquivo para download.

        O método trata documento ausente, excluído ou de outro estudante como a
        mesma falha, antes de tocar no storage, e também falha do mesmo modo
        quando o arquivo físico não existe. Ele existe para impedir a enumeração
        de documentos alheios e o vazamento da localização de armazenamento.
        """
        documento = await self._repositorio.obter_por_id(entrada.documento_id)
        if (
            documento is None
            or documento.deleted_at is not None
            or documento.usuario_id != entrada.usuario_id
        ):
            raise DocumentoNaoEncontrado("Documento não encontrado.")

        conteudo = await self._armazenador.ler(documento.url_armazenamento)
        if conteudo is None:
            raise DocumentoNaoEncontrado("Documento não encontrado.")

        return ConteudoDocumento(
            nome_arquivo=documento.nome_arquivo,
            tipo_arquivo=documento.tipo_arquivo,
            conteudo=conteudo,
        )
