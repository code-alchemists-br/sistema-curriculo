"""Testes unitários para o caso de uso de exclusão de documento complementar."""

import unittest
from uuid import uuid4

from backend.application import (
    DocumentoNaoEncontrado,
    ExcluirDocumento,
    ExcluirDocumentoEntrada,
    RepositorioDocumento,
)
from backend.domain import Documento, DocumentoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
class RepositorioDocumentoEmMemoria(RepositorioDocumento):
    """Substituto em memória para a porta de persistência de documentos.

    A classe armazena documentos em um dicionário indexado pelo DocumentoId,
    registrando operações sem I/O real. Ela existe para permitir testes unitários
    rápidos, isolados e determinísticos do caso de uso de exclusão.
    """

    def __init__(self, documentos: list[Documento] | None = None) -> None:
        """Inicializa o repositório em memória com documentos opcionais.

        O construtor popula o dicionário interno com a lista fornecida.
        Ele existe para preparar o estado inicial necessário aos cenários de teste.
        """
        self._documentos: dict[DocumentoId, Documento] = {
            doc.id: doc for doc in (documentos or [])
        }
        self.exclusoes: list[Documento] = []

    async def obter_por_id(self, documento_id: DocumentoId) -> Documento | None:
        """Retorna o documento correspondente ao ID ou None se ausente.

        O método consulta o dicionário em memória sem latência de banco de dados.
        Ele existe para simular a leitura assíncrona do repositório real.
        """
        return self._documentos.get(documento_id)

    async def excluir(self, documento: Documento) -> None:
        """Remove o documento do dicionário e registra na lista de exclusões.

        O método descarta o item pelo ID e adiciona a entidade em self.exclusoes.
        Ele existe para simular a exclusão e permitir asserções no teste.
        """
        self.exclusoes.append(documento)
        self._documentos.pop(documento.id, None)

    async def salvar(self, documento: Documento) -> None:
        """Adiciona ou atualiza o documento no dicionário em memória.

        O método persiste o item em memória. Ele existe para satisfazer
        o contrato completo da porta RepositorioDocumento.
        """
        self._documentos[documento.id] = documento


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
class TestApplicationExclusaoDocumento(unittest.IsolatedAsyncioTestCase):
    """Testes unitários para o fluxo de orquestração de ExcluirDocumento.

    A classe valida os cenários de sucesso, documento inexistente e bloqueio de
    exclusão de documento alheio (proteção IDOR). Ela existe para garantir a conformidade
    da lógica de aplicação com as regras e requisitos arquiteturais.
    """

    def setUp(self) -> None:
        """Prepara identificadores e entidades de apoio para os testes.

        O método cria instâncias isoladas de IDs para usuário e documentos.
        Ele existe para assegurar independência total entre os métodos de teste.
        """
        self.usuario_id = UsuarioId(uuid4())
        self.outro_usuario_id = UsuarioId(uuid4())
        self.documento_id = DocumentoId(uuid4())
        self.documento = Documento(
            id=self.documento_id,
            usuario_id=self.usuario_id,
            nome_arquivo="historico_escolar.pdf",
            tipo_arquivo="application/pdf",
            url_armazenamento="https://storage.local/docs/historico.pdf",
        )

    async def test_exclui_documento_com_sucesso_quando_proprietario_valido(
        self,
    ) -> None:
        """Verifica a exclusão bem-sucedida de um documento pelo próprio titular.

        O teste inicializa o repositório com o documento, executa o caso de uso
        e valida que o documento foi excluído e não mais retornado na consulta.
        Ele existe para validar o caminho feliz da funcionalidade.
        """
        repo = RepositorioDocumentoEmMemoria([self.documento])
        caso_de_uso = ExcluirDocumento(repo)
        entrada = ExcluirDocumentoEntrada(
            usuario_id=self.usuario_id, documento_id=self.documento_id
        )

        await caso_de_uso.executar(entrada)

        self.assertIn(self.documento, repo.exclusoes)
        doc_consultado = await repo.obter_por_id(self.documento_id)
        self.assertIsNone(doc_consultado)

    async def test_lanca_documento_nao_encontrado_quando_inexistente(
        self,
    ) -> None:
        """Verifica que documento inexistente resulta em DocumentoNaoEncontrado.

        O teste executa a exclusão em um repositório vazio e confirma a exceção,
        assegurando que nenhuma exclusão foi disparada. Ele existe para evitar
        operações espúrias em IDs inválidos.
        """
        repo = RepositorioDocumentoEmMemoria()
        caso_de_uso = ExcluirDocumento(repo)
        entrada = ExcluirDocumentoEntrada(
            usuario_id=self.usuario_id, documento_id=self.documento_id
        )

        with self.assertRaises(DocumentoNaoEncontrado) as ctx:
            await caso_de_uso.executar(entrada)

        self.assertEqual(str(ctx.exception), "Documento não encontrado.")
        self.assertEqual(len(repo.exclusoes), 0)

    async def test_lanca_documento_nao_encontrado_quando_pertence_a_outro_usuario(
        self,
    ) -> None:
        """Verifica proteção IDOR quando o documento pertence a outro estudante.

        O teste cadastra um documento vinculado a outro_usuario_id e tenta excluí-lo
        com a identidade de self.usuario_id. O teste assegura que DocumentoNaoEncontrado
        é lançado de forma indistinguível e o documento original permanece intacto.
        Ele existe para garantir segurança estrita contra enumeração ou deleção indevida.
        """
        doc_alheio = Documento(
            id=self.documento_id,
            usuario_id=self.outro_usuario_id,
            nome_arquivo="certificado_privado.pdf",
            tipo_arquivo="application/pdf",
            url_armazenamento="https://storage.local/docs/privado.pdf",
        )
        repo = RepositorioDocumentoEmMemoria([doc_alheio])
        caso_de_uso = ExcluirDocumento(repo)
        entrada = ExcluirDocumentoEntrada(
            usuario_id=self.usuario_id, documento_id=self.documento_id
        )

        with self.assertRaises(DocumentoNaoEncontrado) as ctx:
            await caso_de_uso.executar(entrada)

        self.assertEqual(str(ctx.exception), "Documento não encontrado.")
        self.assertEqual(len(repo.exclusoes), 0)
        doc_preservado = await repo.obter_por_id(self.documento_id)
        self.assertEqual(doc_preservado, doc_alheio)


if __name__ == "__main__":
    unittest.main()
