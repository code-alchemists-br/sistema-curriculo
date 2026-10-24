"""Testa a rota de download do currículo exportado em DOCX."""

import io
import json
import unittest
from typing import Any
from uuid import UUID

from docx import Document

from backend.api.documentacao_openapi import TAG_EXPORTACAO_CURRICULO
from backend.api.download import cabecalho_de_download
from backend.api.exportacao_curriculo import (
    CAMINHO_EXPORTACAO_DOCX,
    MENSAGEM_FALHA_GERACAO,
)
from backend.api.factory import create_app
from backend.api.sessoes import COOKIE_SESSAO
from backend.application import (
    FORMATO_DOCX,
    CurriculoNaoEncontrado,
    ExportarCurriculo,
    ExportarCurriculoEntrada,
    FalhaGeracaoArquivoCurriculo,
    GerarPreviaVersaoCurriculoEntrada,
    PreviaVersaoCurriculo,
)
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.domain.value_objects import CurriculoId, UsuarioId
from backend.infrastructure.exportacao.renderizador_docx import (
    RenderizadorDocumentoCurriculoDocx,
)
from backend.tests.fixtures.curriculo_exportacao import (
    ID_CURRICULO_ESTAVEL,
    ID_USUARIO_ESTAVEL,
    obter_curriculo_exportacao_fixture,
)

CREDENCIAL_VALIDA = "credencial-sintetica-exportacao"
NOME_ARQUIVO = "curriculo-ana-carolina-da-silva-curriculo-de-estagio-engenharia-de-software.docx"
OUTRO_USUARIO = UUID("99999999-9999-4999-8999-999999999999")


class AutenticadorSessaoStub(AutenticadorSessao):
    """Autentica somente a credencial sintética do estudante da fixture.

    O double devolve o estudante estável para o token conhecido e ``None`` para
    os demais. Ele existe para exercitar o middleware real sem banco de sessões.
    """

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Devolve o estudante da fixture apenas para a credencial conhecida.

        O método compara o token sem consultar serviços. Ele existe para que o
        dono da exportação venha da sessão autenticada.
        """
        return ID_USUARIO_ESTAVEL if token == CREDENCIAL_VALIDA else None


class GeradorPreviaStub:
    """Devolve a prévia da fixture somente para a versão do estudante.

    O double registra as entradas e levanta ``CurriculoNaoEncontrado`` para
    qualquer outro par usuário/versão. Ele existe para usar o caso de uso real
    de exportação sem persistência.
    """

    def __init__(self) -> None:
        """Inicia o histórico de entradas recebidas.

        O construtor mantém apenas estado em memória. Ele existe para conferir a
        identidade repassada pela rota.
        """
        self.entradas: list[GerarPreviaVersaoCurriculoEntrada] = []

    async def executar(self, entrada: GerarPreviaVersaoCurriculoEntrada) -> PreviaVersaoCurriculo:
        """Registra a entrada e devolve a prévia ou sinaliza versão ausente.

        O método aceita apenas o estudante e a versão estáveis. Ele existe para
        simular a verificação de propriedade do caso de uso de prévia.
        """
        self.entradas.append(entrada)
        if (entrada.usuario_id, entrada.curriculo_id) != (ID_USUARIO_ESTAVEL, ID_CURRICULO_ESTAVEL):
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")
        fixture = obter_curriculo_exportacao_fixture()
        return PreviaVersaoCurriculo(
            usuario=fixture.usuario,
            curriculo=fixture.curriculo,
            formacoes=(fixture.formacao_academica,),
            experiencias=(fixture.experiencia_profissional,),
            projetos=(fixture.projeto_academico,),
            competencias=fixture.competencias,
            idiomas=fixture.idiomas,
            documentos=(),
        )


class ExportacaoFalhaStub:
    """Simula a exportação que não consegue gerar o arquivo.

    O double sempre levanta ``FalhaGeracaoArquivoCurriculo``. Ele existe para
    verificar a resposta 500 genérica da rota.
    """

    async def executar(self, entrada: ExportarCurriculoEntrada) -> None:
        """Levanta a falha de geração para qualquer entrada.

        O método ignora a entrada. Ele existe para reproduzir erro interno do
        gerador sem depender da biblioteca DOCX.
        """
        raise FalhaGeracaoArquivoCurriculo("detalhe interno que não deve vazar")


def _caminho(usuario_id: UUID, curriculo_id: UUID) -> str:
    """Monta o caminho da exportação DOCX para os identificadores informados.

    A função preenche o modelo de rota publicado. Ela existe para evitar
    divergência entre o teste e o caminho registrado.
    """
    return CAMINHO_EXPORTACAO_DOCX.format(usuario_id=usuario_id, curriculo_id=curriculo_id)


async def _baixar(
    app: object, caminho: str, autenticado: bool = True
) -> tuple[int, dict[str, str], bytes]:
    """Envia um GET diretamente à aplicação ASGI e coleta a resposta.

    A função inclui o cookie de sessão sintético quando pedido e devolve status,
    cabeçalhos em minúsculas e corpo. Ela existe para observar a resposta real
    emitida pelo FastAPI, sem servidor nem cliente externo.
    """
    cabecalhos = [(b"cookie", f"{COOKIE_SESSAO}={CREDENCIAL_VALIDA}".encode())] if autenticado else []
    escopo = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": caminho,
        "raw_path": caminho.encode(),
        "query_string": b"",
        "headers": cabecalhos,
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }
    status_resposta = 0
    cabecalhos_resposta: dict[str, str] = {}
    partes: list[bytes] = []

    async def receber() -> dict[str, object]:
        """Entrega uma requisição sem corpo."""
        return {"type": "http.request", "body": b"", "more_body": False}

    async def enviar(mensagem: dict[str, Any]) -> None:
        """Captura status, cabeçalhos e fragmentos do corpo da resposta."""
        nonlocal status_resposta
        if mensagem["type"] == "http.response.start":
            status_resposta = int(mensagem["status"])
            for nome, valor in mensagem.get("headers", []):
                cabecalhos_resposta[nome.decode("latin-1").lower()] = valor.decode("latin-1")
        elif mensagem["type"] == "http.response.body":
            partes.append(mensagem.get("body", b""))

    await app(escopo, receber, enviar)  # type: ignore[operator]
    return status_resposta, cabecalhos_resposta, b"".join(partes)


def _app(executor: object | None):
    """Compõe a aplicação com middleware de sessão e o executor informado.

    A fábrica real recebe o autenticador sintético e o executor de exportação.
    Ela existe para exercitar autenticação, roteamento e resposta reais.
    """
    return create_app(
        autenticador_sessao=AutenticadorSessaoStub(),
        exportar_curriculo_docx=executor,  # type: ignore[arg-type]
    )


def _exportacao_real() -> ExportarCurriculo:
    """Monta o caso de uso real com o gerador DOCX real e prévia simulada.

    A função combina a prévia da fixture com ``RenderizadorDocumentoCurriculoDocx``.
    Ela existe para validar o arquivo realmente entregue pela rota.
    """
    return ExportarCurriculo(GeradorPreviaStub(), RenderizadorDocumentoCurriculoDocx(), FORMATO_DOCX)


class ExportacaoDocxRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o contrato HTTP do download DOCX do currículo.

    Os cenários cobrem sucesso com arquivo válido, cabeçalhos, propriedade,
    falha de geração, autenticação e indisponibilidade. A classe existe para
    proteger o UC08 e os casos CT-RF09-05 e CT-RF15-01.
    """

    async def test_baixa_docx_valido_com_tipo_mime_e_nome_corretos(self) -> None:
        """Entrega o DOCX da versão com MIME, nome e proteções de download.

        O teste abre o corpo com python-docx e confere os cabeçalhos. Ele
        existe para garantir que o navegador baixe um arquivo legível.
        """
        status, cabecalhos, corpo = await _baixar(
            _app(_exportacao_real()), _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor)
        )

        self.assertEqual(status, 200)
        self.assertEqual(cabecalhos["content-type"], FORMATO_DOCX.tipo_mime)
        disposicao = cabecalhos["content-disposition"]
        self.assertTrue(disposicao.startswith("attachment"))
        self.assertIn(f'filename="{NOME_ARQUIVO}"', disposicao)
        self.assertIn(f"filename*=UTF-8''{NOME_ARQUIVO}", disposicao)
        self.assertEqual(cabecalhos["x-content-type-options"], "nosniff")
        self.assertEqual(cabecalhos["cache-control"], "private, no-store")
        textos = [paragrafo.text for paragrafo in Document(io.BytesIO(corpo)).paragraphs]
        self.assertIn("Ana Carolina da Silva", textos)

    async def test_versao_inexistente_ou_alheia_responde_404(self) -> None:
        """Responde 404 uniforme quando a versão não pertence ao estudante.

        O teste pede uma versão que a prévia não reconhece. Ele existe para não
        revelar a existência de versões de outros estudantes.
        """
        status, _, corpo = await _baixar(
            _app(_exportacao_real()), _caminho(ID_USUARIO_ESTAVEL.valor, OUTRO_USUARIO)
        )

        self.assertEqual(status, 404)
        self.assertEqual(json.loads(corpo), {"detail": "Versão de currículo não encontrada."})

    async def test_outro_estudante_na_url_e_recusado_pelo_middleware(self) -> None:
        """Recusa a exportação quando a URL aponta para outro estudante.

        O middleware compara o identificador da rota com a sessão. O teste
        existe para impedir exportar currículos de terceiros (CT-RF15-01).
        """
        status, _, _ = await _baixar(
            _app(_exportacao_real()), _caminho(OUTRO_USUARIO, ID_CURRICULO_ESTAVEL.valor)
        )

        self.assertEqual(status, 403)

    async def test_falha_de_geracao_responde_500_generico(self) -> None:
        """Responde 500 com mensagem genérica quando o arquivo não é gerado.

        O teste confere que o detalhe interno não vaza. Ele existe para cumprir
        o CT-RF09-05 sem expor erros da biblioteca.
        """
        status, _, corpo = await _baixar(
            _app(ExportacaoFalhaStub()), _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor)
        )

        self.assertEqual(status, 500)
        self.assertEqual(json.loads(corpo), {"detail": MENSAGEM_FALHA_GERACAO})

    async def test_sem_sessao_responde_401(self) -> None:
        """Exige sessão autenticada para exportar.

        O teste omite o cookie de sessão. Ele existe para impedir download
        anônimo de currículos.
        """
        status, _, _ = await _baixar(
            _app(_exportacao_real()),
            _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor),
            autenticado=False,
        )

        self.assertEqual(status, 401)

    async def test_sem_executor_responde_503(self) -> None:
        """Responde 503 quando a exportação não foi composta.

        O teste monta a aplicação sem executor. Ele existe para sinalizar
        indisponibilidade em vez de erro interno.
        """
        status, _, corpo = await _baixar(
            _app(None), _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor)
        )

        self.assertEqual(status, 503)
        self.assertEqual(json.loads(corpo), {"detail": "Exportação indisponível."})

    async def test_usa_a_identidade_da_sessao(self) -> None:
        """Repassa ao caso de uso o estudante da sessão e a versão da URL.

        O teste inspeciona a entrada recebida pela prévia. Ele existe para que a
        propriedade seja verificada com a identidade autenticada.
        """
        previa = GeradorPreviaStub()
        exportacao = ExportarCurriculo(previa, RenderizadorDocumentoCurriculoDocx(), FORMATO_DOCX)

        await _baixar(_app(exportacao), _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor))

        self.assertEqual(
            previa.entradas,
            [GerarPreviaVersaoCurriculoEntrada(ID_USUARIO_ESTAVEL, CurriculoId(ID_CURRICULO_ESTAVEL.valor))],
        )


class CabecalhoDownloadTestCase(unittest.TestCase):
    """Verifica o ``Content-Disposition`` compartilhado pelos downloads.

    Os cenários usam nomes com acento e caracteres especiais. A classe existe
    para que o cabeçalho nunca quebre fora do ASCII.
    """

    def test_nome_com_acento_tem_alternativa_ascii_e_utf8(self) -> None:
        """Gera ``filename`` ASCII e ``filename*`` codificado em UTF-8.

        O teste confere as duas formas do nome. Ele existe para manter o nome
        legível em navegadores antigos e modernos (RFC 6266).
        """
        cabecalho = cabecalho_de_download("Currículo João.docx")

        self.assertTrue(cabecalho.startswith("attachment"))
        cabecalho.encode("latin-1")
        self.assertIn("filename*=UTF-8''Curr%C3%ADculo%20Jo%C3%A3o.docx", cabecalho)
        nome_ascii = cabecalho.split('filename="')[1].split('"')[0]
        self.assertTrue(nome_ascii.isascii())
        self.assertTrue(nome_ascii.endswith(".docx"))


class ContratoOpenApiExportacaoTestCase(unittest.TestCase):
    """Verifica a documentação OpenAPI da exportação DOCX.

    O teste lê o schema gerado pela aplicação. A classe existe para que o
    Swagger mostre o tipo binário e as respostas de erro da rota.
    """

    def test_documenta_rota_com_tag_e_respostas(self) -> None:
        """Documenta a rota com a tag de exportação e o conteúdo DOCX.

        O teste confere tag, respostas e tipo de conteúdo do 200. Ele existe
        para manter o contrato publicado fiel ao handler.
        """
        operacao = create_app().openapi()["paths"][CAMINHO_EXPORTACAO_DOCX]["get"]

        self.assertEqual(operacao["tags"], [TAG_EXPORTACAO_CURRICULO])
        self.assertTrue({"200", "404", "500", "503"} <= set(operacao["responses"]))
        self.assertIn(FORMATO_DOCX.tipo_mime, operacao["responses"]["200"]["content"])
