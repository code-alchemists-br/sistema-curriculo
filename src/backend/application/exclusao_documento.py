"""Caso de uso para exclusão de documento complementar de estudante.

O módulo orquestra a validação de propriedade e exclusão segura do documento,
assegurando tratamento uniforme e sem vazamento de existência de recursos alheios.
Ele existe para implementar as regras de negócio de exclusão de documentos
isoladas de transporte HTTP e tecnologia de banco de dados.
"""

from dataclasses import dataclass

from backend.application.ports import RepositorioDocumento
from backend.domain.value_objects import DocumentoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
class DocumentoNaoEncontrado(LookupError):
    """Indica que o documento solicitado não foi encontrado ou não pertence ao usuário.

    A exceção herda de LookupError e é disparada indistintamente para ausência
    de registro ou divergência de titularidade. Ela existe para prevenir ataques
    de enumeração de recursos (IDOR) e manter mensagens consistentes de erro.
    """


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
@dataclass(frozen=True, slots=True)
class ExcluirDocumentoEntrada:
    """Encapsula os parâmetros tipados necessários para excluir um documento.

    O DTO transporta o identificador do estudante autenticado e o identificador
    único do documento alvo. Ele existe para estabelecer uma fronteira limpa
    entre a camada de interface/transporte e a lógica de aplicação.
    """

    usuario_id: UsuarioId
    documento_id: DocumentoId


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
class ExcluirDocumento:
    """Orquestra a validação de posse e a exclusão de documento complementar.

    O interactor busca o documento na porta de persistência, verifica a
    correspondência do proprietário com a sessão autenticada e delega a exclusão.
    Ele existe para centralizar o fluxo de exclusão de documentos segundo
    os princípios da Clean Architecture.
    """

    def __init__(self, repositorio_documento: RepositorioDocumento) -> None:
        """Inicializa o caso de uso com a porta de repositório de documentos.

        O construtor armazena a dependência abstrata recebida por injeção.
        Ele existe para permitir que a persistência seja substituída por doubles
        em testes unitários determinísticos.
        """
        self._repositorio = repositorio_documento

    async def executar(self, entrada: ExcluirDocumentoEntrada) -> None:
        """Executa a verificação e exclusão do documento complementar.

        O método obtém o documento pelo ID informado na entrada, valida se o
        proprietário confere com o usuário autenticado e, em caso afirmativo,
        chama a exclusão no repositório. Ele existe para garantir que estudantes
        só possam excluir documentos de sua titularidade e sinalizar erro caso contrário.
        """
        documento = await self._repositorio.obter_por_id(entrada.documento_id)
        if documento is None or documento.usuario_id != entrada.usuario_id:
            raise DocumentoNaoEncontrado("Documento não encontrado.")

        await self._repositorio.excluir(documento)
