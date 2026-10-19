"""Testa unitariamente o caso de uso de download de documento complementar."""

import unittest
from dataclasses import fields, replace
from datetime import UTC, datetime
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261019-110000-download-documento-complementar-v001.md#v001
from backend.application.download_documento import (
    BaixarDocumento,
    BaixarDocumentoEntrada,
    ConteudoDocumento,
)
from backend.application.exclusao_documento import DocumentoNaoEncontrado
from backend.domain.itens_perfil import Documento
from backend.domain.value_objects import DocumentoId, UsuarioId

ID_DONO = UUID("00000000-0000-0000-0000-000000000001")
ID_OUTRO = UUID("00000000-0000-0000-0000-000000000002")
ID_DOCUMENTO = UUID("00000000-0000-0000-0000-0000000000d1")
URL_PRIVADA = "https://storage.local/documentos/" + "a" * 32
BYTES_DO_ARQUIVO = b"%PDF-1.4 conteudo de teste"


def _criar_documento(**alteracoes) -> Documento:
    """Cria um documento complementar válido pertencente ao dono de referência.

    A função monta a entidade sem acessar storage ou banco e aceita alterações
    pontuais. Ela existe para que cada teste altere só o aspecto que interessa.
    """
    documento = Documento(
        id=DocumentoId(ID_DOCUMENTO),
        usuario_id=UsuarioId(ID_DONO),
        nome_arquivo="rg.pdf",
        tipo_arquivo="application/pdf",
        url_armazenamento=URL_PRIVADA,
    )
    return replace(documento, **alteracoes) if alteracoes else documento


class RepositorioDocumentoStub:
    """Substitui a porta de documentos e registra as consultas recebidas.

    O stub devolve o documento configurado e guarda cada identificador pedido.
    Ele existe para controlar a existência do documento e provar quando o
    storage não deveria ser consultado.
    """

    def __init__(self, documento: Documento | None) -> None:
        """Guarda o documento a devolver e inicia o histórico de consultas.

        O construtor não acessa recursos externos. Ele existe para que cada teste
        defina se o documento existe e quem é o dono.
        """
        self._documento = documento
        self.consultas: list[DocumentoId] = []

    async def obter_por_id(self, documento_id: DocumentoId) -> Documento | None:
        """Devolve por coroutine o documento configurado, registrando a consulta.

        O método não faz I/O. Ele existe para simular a leitura aguardável da
        porta de repositório.
        """
        self.consultas.append(documento_id)
        return self._documento


class ArmazenadorStub:
    """Substitui a porta de storage e registra as leituras solicitadas.

    O stub devolve os bytes configurados e guarda cada localização lida. Ele
    existe para provar que o arquivo só é lido depois da autorização.
    """

    def __init__(self, conteudo: bytes | None) -> None:
        """Guarda o conteúdo a devolver e inicia o histórico de leituras.

        O construtor não acessa recursos externos. Ele existe para que cada teste
        defina se o arquivo físico existe.
        """
        self._conteudo = conteudo
        self.leituras: list[str] = []

    async def ler(self, url_armazenamento: str) -> bytes | None:
        """Devolve por coroutine o conteúdo configurado, registrando a leitura.

        O método não faz I/O. Ele existe para simular a leitura aguardável da
        porta de storage.
        """
        self.leituras.append(url_armazenamento)
        return self._conteudo


def _entrada(usuario_id: UUID = ID_DONO) -> BaixarDocumentoEntrada:
    """Cria a entrada do caso de uso para o usuário e o documento de referência.

    A função monta o DTO tipado com o documento fixo e o usuário informado. Ela
    existe para reduzir repetição nos testes.
    """
    return BaixarDocumentoEntrada(
        usuario_id=UsuarioId(usuario_id), documento_id=DocumentoId(ID_DOCUMENTO)
    )


class BaixarDocumentoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica as decisões de fluxo do caso de uso ``BaixarDocumento``.

    Os testes substituem as duas portas por doubles e conferem o resultado e as
    consultas feitas. A classe existe para proteger a regra de que só o dono
    baixa o documento e de que a localização de armazenamento não sai daqui.
    """

    async def test_devolve_nome_tipo_e_bytes_do_documento_do_dono(self) -> None:
        """Confirma que o dono recebe o arquivo com nome, tipo e conteúdo.

        O teste executa o caso com o dono e confere o resultado e a localização
        lida no storage. Ele existe para garantir o caminho de sucesso.
        """
        armazenador = ArmazenadorStub(BYTES_DO_ARQUIVO)
        caso = BaixarDocumento(RepositorioDocumentoStub(_criar_documento()), armazenador)

        resultado = await caso.executar(_entrada())

        self.assertEqual(
            resultado,
            ConteudoDocumento("rg.pdf", "application/pdf", BYTES_DO_ARQUIVO),
        )
        self.assertEqual(armazenador.leituras, [URL_PRIVADA])

    async def test_resultado_nao_expoe_a_localizacao_de_armazenamento(self) -> None:
        """Confirma que o resultado não carrega a URL de armazenamento.

        O teste inspeciona os campos do resultado e os valores devolvidos. Ele
        existe para impedir que o caminho do storage chegue à camada de API.
        """
        caso = BaixarDocumento(
            RepositorioDocumentoStub(_criar_documento()), ArmazenadorStub(BYTES_DO_ARQUIVO)
        )

        resultado = await caso.executar(_entrada())

        self.assertEqual(
            [campo.name for campo in fields(ConteudoDocumento)],
            ["nome_arquivo", "tipo_arquivo", "conteudo"],
        )
        self.assertNotIn(URL_PRIVADA, repr(resultado))

    async def test_recusa_documento_inexistente_sem_ler_o_storage(self) -> None:
        """Confirma que documento ausente falha sem consultar o storage.

        O teste executa o caso com um repositório vazio. Ele existe para que o
        storage só seja tocado depois da autorização.
        """
        armazenador = ArmazenadorStub(BYTES_DO_ARQUIVO)
        caso = BaixarDocumento(RepositorioDocumentoStub(None), armazenador)

        with self.assertRaises(DocumentoNaoEncontrado):
            await caso.executar(_entrada())

        self.assertEqual(armazenador.leituras, [])

    async def test_recusa_documento_de_outro_estudante_sem_ler_o_storage(self) -> None:
        """Confirma que o documento de outro estudante falha como inexistente.

        O teste executa o caso com um usuário diferente do dono. Ele existe para
        impedir o acesso e a enumeração de documentos alheios.
        """
        armazenador = ArmazenadorStub(BYTES_DO_ARQUIVO)
        caso = BaixarDocumento(RepositorioDocumentoStub(_criar_documento()), armazenador)

        with self.assertRaises(DocumentoNaoEncontrado):
            await caso.executar(_entrada(ID_OUTRO))

        self.assertEqual(armazenador.leituras, [])

    async def test_recusa_documento_excluido_sem_ler_o_storage(self) -> None:
        """Confirma que documento com exclusão lógica não pode ser baixado.

        O teste usa um documento com ``deleted_at`` preenchido. Ele existe para
        que a exclusão lógica também valha para o download, mesmo que o
        repositório devolva o registro.
        """
        excluido = _criar_documento(deleted_at=datetime(2026, 10, 19, tzinfo=UTC))
        armazenador = ArmazenadorStub(BYTES_DO_ARQUIVO)
        caso = BaixarDocumento(RepositorioDocumentoStub(excluido), armazenador)

        with self.assertRaises(DocumentoNaoEncontrado):
            await caso.executar(_entrada())

        self.assertEqual(armazenador.leituras, [])

    async def test_recusa_quando_o_arquivo_fisico_nao_existe(self) -> None:
        """Confirma que arquivo ausente no storage falha como não encontrado.

        O teste usa um storage que devolve ``None``. Ele existe para que a falta
        do arquivo não vire erro interno nem revele detalhes do storage.
        """
        caso = BaixarDocumento(
            RepositorioDocumentoStub(_criar_documento()), ArmazenadorStub(None)
        )

        with self.assertRaises(DocumentoNaoEncontrado):
            await caso.executar(_entrada())
