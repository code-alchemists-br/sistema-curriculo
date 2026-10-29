"""Testa que um estudante não acessa nem exclui o documento de outro e que a exclusão vale."""

import unittest
from typing import Any
from uuid import UUID, uuid4

# Proveniência: decision-analysis prompts/backend/20261026-150000-testes-exclusao-logica-documento-v001.md#v001
from backend.api.factory import create_app
from backend.api.sessoes import COOKIE_SESSAO
from backend.application import BaixarDocumento, ExcluirDocumento
from backend.domain.itens_perfil import Documento
from backend.domain.value_objects import DocumentoId, UsuarioId
from backend.tests.test_integracao_crud_informacoes_complementares import (
    ID_ESTUDANTE_A,
    ID_ESTUDANTE_B,
    AutenticadorSessaoMultiUsuario,
    RepositorioDocumentoEmMemoriaComEstado,
)

TOKEN_A = "credencial-sintetica-estudante-a"
TOKEN_B = "credencial-sintetica-estudante-b"
URL_PRIVADA = "https://storage.local/documentos/" + "b" * 32
CONTEUDO = b"%PDF-1.4 historico do estudante A"


class ArmazenadorComLeituraFake:
    """Substitui o storage devolvendo o conteúdo configurado para a URL conhecida.

    O double guarda um dicionário de URL para bytes e devolve ``None`` para as
    demais. Ele existe para exercitar o download real sem sistema de arquivos.
    """

    def __init__(self, arquivos: dict[str, bytes]) -> None:
        """Guarda os arquivos disponíveis por URL de armazenamento.

        O construtor não acessa recursos externos. Ele existe para controlar o
        que existe fisicamente em cada cenário.
        """
        self._arquivos = arquivos

    async def armazenar(self, conteudo: bytes, nome_arquivo: str, tipo_arquivo: str) -> str:
        """Não é usado nestes cenários e falha se for chamado.

        O método existe para satisfazer a porta de storage; o teste só lê.
        """
        raise AssertionError("O armazenamento não deveria ser chamado neste teste.")

    async def ler(self, url_armazenamento: str) -> bytes | None:
        """Devolve os bytes da URL conhecida, ou ``None`` para as outras.

        O método consulta só o dicionário em memória. Ele existe para simular a
        leitura aguardável da porta de storage.
        """
        return self._arquivos.get(url_armazenamento)


def _cenario() -> tuple[object, RepositorioDocumentoEmMemoriaComEstado, UUID]:
    """Monta a aplicação com dois estudantes e um documento do estudante A.

    A função liga os casos de uso reais de exclusão e download ao repositório em
    memória e ao storage de teste, com autenticação de dois estudantes. Ela
    existe para exercitar sessão, autorização e roteamento reais, sem banco.
    """
    repositorio = RepositorioDocumentoEmMemoriaComEstado()
    documento = Documento(
        id=DocumentoId(uuid4()),
        usuario_id=UsuarioId(ID_ESTUDANTE_A),
        nome_arquivo="historico.pdf",
        tipo_arquivo="application/pdf",
        url_armazenamento=URL_PRIVADA,
    )
    repositorio.documentos[documento.id] = documento
    app = create_app(
        autenticador_sessao=AutenticadorSessaoMultiUsuario(
            {TOKEN_A: UsuarioId(ID_ESTUDANTE_A), TOKEN_B: UsuarioId(ID_ESTUDANTE_B)}
        ),
        excluir_documento=ExcluirDocumento(repositorio),
        baixar_documento=BaixarDocumento(
            repositorio, ArmazenadorComLeituraFake({URL_PRIVADA: CONTEUDO})
        ),
    )
    return app, repositorio, documento.id.valor


async def _chamar(app: object, metodo: str, caminho: str, token: str | None) -> tuple[int, bytes]:
    """Envia uma requisição à aplicação ASGI e devolve o status e o corpo.

    A função inclui o cookie de sessão do estudante quando há token. Ela existe
    para observar a resposta real emitida pelo FastAPI, sem servidor nem cliente
    externo.
    """
    cabecalhos = [(b"cookie", f"{COOKIE_SESSAO}={token}".encode())] if token else []
    escopo = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": metodo,
        "scheme": "http",
        "path": caminho,
        "raw_path": caminho.encode(),
        "query_string": b"",
        "headers": cabecalhos,
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }
    status_resposta = 0
    partes: list[bytes] = []

    async def receber() -> dict[str, object]:
        """Entrega uma requisição sem corpo."""
        return {"type": "http.request", "body": b"", "more_body": False}

    async def enviar(mensagem: dict[str, Any]) -> None:
        """Captura o status e os fragmentos do corpo da resposta."""
        nonlocal status_resposta
        if mensagem["type"] == "http.response.start":
            status_resposta = int(mensagem["status"])
        elif mensagem["type"] == "http.response.body":
            partes.append(mensagem.get("body", b""))

    await app(escopo, receber, enviar)  # type: ignore[operator]
    return status_resposta, b"".join(partes)


class IsolamentoDeDocumentoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o isolamento e a exclusão lógica do documento entre estudantes.

    Os cenários usam a aplicação com middleware de sessão e os casos de uso reais
    de download e exclusão. A classe existe para proteger o card F4.16: a
    exclusão vale para o dono e um estudante nunca acessa o documento de outro.
    """

    async def test_o_dono_baixa_o_proprio_documento(self) -> None:
        """Confirma que o dono recebe o arquivo do próprio documento.

        O teste baixa o documento com a sessão do dono. Ele existe como base de
        comparação para os cenários de recusa.
        """
        app, _, documento_id = _cenario()

        status, corpo = await _chamar(app, "GET", f"/documentos/{documento_id}", TOKEN_A)

        self.assertEqual((status, corpo), (200, CONTEUDO))

    async def test_outro_estudante_nao_baixa_o_documento_alheio(self) -> None:
        """Confirma que outro estudante recebe 404 e nenhum byte do arquivo.

        O teste baixa o documento do estudante A com a sessão do estudante B. Ele
        existe para que o acesso e a existência do documento não sejam revelados.
        """
        app, _, documento_id = _cenario()

        status, corpo = await _chamar(app, "GET", f"/documentos/{documento_id}", TOKEN_B)

        self.assertEqual(status, 404)
        self.assertNotIn(CONTEUDO, corpo)

    async def test_outro_estudante_nao_exclui_e_o_documento_segue_disponivel(self) -> None:
        """Confirma que a exclusão por outro estudante falha sem afetar o dono.

        O teste tenta excluir com a sessão de B e baixa com a sessão de A em
        seguida. Ele existe para que um estudante não remova dado alheio.
        """
        app, repositorio, documento_id = _cenario()

        status_exclusao, _ = await _chamar(app, "DELETE", f"/documentos/{documento_id}", TOKEN_B)
        status_download, corpo = await _chamar(app, "GET", f"/documentos/{documento_id}", TOKEN_A)

        self.assertEqual(status_exclusao, 404)
        self.assertEqual(repositorio.exclusoes, [])
        self.assertEqual((status_download, corpo), (200, CONTEUDO))

    async def test_depois_de_excluir_ninguem_baixa_o_documento(self) -> None:
        """Confirma que o documento excluído deixa de ser baixado, inclusive pelo dono.

        O teste exclui com a sessão do dono e tenta baixar com as duas sessões.
        Ele existe para provar que a exclusão lógica tem efeito.
        """
        app, repositorio, documento_id = _cenario()

        status_exclusao, _ = await _chamar(app, "DELETE", f"/documentos/{documento_id}", TOKEN_A)
        status_dono, _ = await _chamar(app, "GET", f"/documentos/{documento_id}", TOKEN_A)
        status_outro, _ = await _chamar(app, "GET", f"/documentos/{documento_id}", TOKEN_B)

        self.assertEqual(status_exclusao, 204)
        self.assertEqual(len(repositorio.exclusoes), 1)
        self.assertEqual((status_dono, status_outro), (404, 404))

    async def test_excluir_duas_vezes_responde_404_na_segunda(self) -> None:
        """Confirma que repetir a exclusão não encontra mais o documento.

        O teste exclui duas vezes com a sessão do dono. Ele existe para que a
        segunda tentativa não regrave nem revele estado.
        """
        app, repositorio, documento_id = _cenario()

        primeira, _ = await _chamar(app, "DELETE", f"/documentos/{documento_id}", TOKEN_A)
        segunda, _ = await _chamar(app, "DELETE", f"/documentos/{documento_id}", TOKEN_A)

        self.assertEqual((primeira, segunda), (204, 404))
        self.assertEqual(len(repositorio.exclusoes), 1)

    async def test_sem_sessao_nao_baixa_nem_exclui(self) -> None:
        """Confirma que, sem sessão, o download e a exclusão respondem 401.

        O teste omite o cookie nas duas operações. Ele existe para impedir acesso
        anônimo ao documento.
        """
        app, repositorio, documento_id = _cenario()

        status_download, _ = await _chamar(app, "GET", f"/documentos/{documento_id}", None)
        status_exclusao, _ = await _chamar(app, "DELETE", f"/documentos/{documento_id}", None)

        self.assertEqual((status_download, status_exclusao), (401, 401))
        self.assertEqual(repositorio.exclusoes, [])
