"""Testa a rota de download do currículo exportado em PDF."""

import json
import unittest
from io import BytesIO
from uuid import UUID

from pypdf import PdfReader

# Proveniência: decision-analysis prompts/backend/20261025-100000-rota-exportacao-pdf-v001.md#v001
from backend.api.documentacao_openapi import TAG_EXPORTACAO_CURRICULO
from backend.api.exportacao_curriculo import (
    CAMINHO_EXPORTACAO_DOCX,
    CAMINHO_EXPORTACAO_PDF,
    MENSAGEM_FALHA_GERACAO,
)
from backend.api.factory import create_app
from backend.application import (
    FORMATO_PDF,
    ExportarCurriculo,
    GerarPreviaVersaoCurriculoEntrada,
)
from backend.domain.value_objects import CurriculoId
from backend.infrastructure.exportacao.renderizador_pdf import (
    RenderizadorDocumentoCurriculoPdf,
)
from backend.tests.fixtures.curriculo_exportacao import (
    ID_CURRICULO_ESTAVEL,
    ID_USUARIO_ESTAVEL,
)
from backend.tests.test_api_exportacao_curriculo import (
    OUTRO_USUARIO,
    AutenticadorSessaoStub,
    ExportacaoFalhaStub,
    GeradorPreviaStub,
    _baixar,
)

NOME_ARQUIVO = "curriculo-ana-carolina-da-silva-curriculo-de-estagio-engenharia-de-software.pdf"


def _caminho(usuario_id: UUID, curriculo_id: UUID) -> str:
    """Monta o caminho da exportação PDF para os identificadores informados.

    A função preenche o modelo de rota publicado. Ela existe para evitar
    divergência entre o teste e o caminho registrado.
    """
    return CAMINHO_EXPORTACAO_PDF.format(usuario_id=usuario_id, curriculo_id=curriculo_id)


def _app(executor: object | None):
    """Compõe a aplicação com middleware de sessão e o executor de PDF informado.

    A fábrica real recebe o autenticador sintético e o executor de exportação
    em PDF. Ela existe para exercitar autenticação, roteamento e resposta reais.
    """
    return create_app(
        autenticador_sessao=AutenticadorSessaoStub(),
        exportar_curriculo_pdf=executor,  # type: ignore[arg-type]
    )


def _exportacao_real() -> ExportarCurriculo:
    """Monta o caso de uso real com o gerador PDF real e prévia simulada.

    A função combina a prévia da fixture com ``RenderizadorDocumentoCurriculoPdf``.
    Ela existe para validar o arquivo realmente entregue pela rota.
    """
    return ExportarCurriculo(GeradorPreviaStub(), RenderizadorDocumentoCurriculoPdf(), FORMATO_PDF)


class ExportacaoPdfRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o contrato HTTP do download PDF do currículo.

    Os cenários cobrem sucesso com arquivo válido, cabeçalhos, propriedade,
    falha de geração, autenticação, indisponibilidade e convivência com o DOCX.
    A classe existe para proteger o UC07 e os casos CT-RF09-01 e CT-RF15-01.
    """

    async def test_baixa_pdf_valido_com_tipo_mime_e_nome_corretos(self) -> None:
        """Entrega o PDF da versão com MIME, nome e proteções de download.

        O teste abre o corpo com pypdf e confere os cabeçalhos. Ele existe para
        garantir que o navegador baixe um arquivo legível.
        """
        status, cabecalhos, corpo = await _baixar(
            _app(_exportacao_real()), _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor)
        )

        self.assertEqual(status, 200)
        self.assertEqual(cabecalhos["content-type"], "application/pdf")
        disposicao = cabecalhos["content-disposition"]
        self.assertTrue(disposicao.startswith("attachment"))
        self.assertIn(f'filename="{NOME_ARQUIVO}"', disposicao)
        self.assertIn(f"filename*=UTF-8''{NOME_ARQUIVO}", disposicao)
        self.assertEqual(cabecalhos["x-content-type-options"], "nosniff")
        self.assertEqual(cabecalhos["cache-control"], "private, no-store")
        self.assertTrue(corpo.startswith(b"%PDF"))
        texto = " ".join(pagina.extract_text() for pagina in PdfReader(BytesIO(corpo)).pages)
        self.assertIn("Ana Carolina da Silva", texto)

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
        """Responde 503 quando a exportação em PDF não foi composta.

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
        exportacao = ExportarCurriculo(previa, RenderizadorDocumentoCurriculoPdf(), FORMATO_PDF)

        await _baixar(_app(exportacao), _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor))

        self.assertEqual(
            previa.entradas,
            [GerarPreviaVersaoCurriculoEntrada(ID_USUARIO_ESTAVEL, CurriculoId(ID_CURRICULO_ESTAVEL.valor))],
        )

    async def test_pdf_e_docx_sao_independentes(self) -> None:
        """Confirma que compor só o PDF não habilita o DOCX.

        O teste monta a aplicação apenas com o executor do PDF e pede o DOCX. Ele
        existe para que cada formato dependa só do seu próprio executor.
        """
        status, _, _ = await _baixar(
            _app(_exportacao_real()),
            CAMINHO_EXPORTACAO_DOCX.format(
                usuario_id=ID_USUARIO_ESTAVEL.valor, curriculo_id=ID_CURRICULO_ESTAVEL.valor
            ),
        )

        self.assertEqual(status, 503)


class ContratoOpenApiExportacaoPdfTestCase(unittest.TestCase):
    """Verifica a documentação OpenAPI da exportação PDF.

    O teste lê o schema gerado pela aplicação. A classe existe para que o
    Swagger mostre o tipo binário e as respostas de erro da rota.
    """

    def test_documenta_rota_com_tag_e_respostas(self) -> None:
        """Documenta a rota com a tag de exportação e o conteúdo PDF.

        O teste confere tag, respostas e tipo de conteúdo do 200. Ele existe
        para manter o contrato publicado fiel ao handler.
        """
        operacao = create_app().openapi()["paths"][CAMINHO_EXPORTACAO_PDF]["get"]

        self.assertEqual(operacao["tags"], [TAG_EXPORTACAO_CURRICULO])
        self.assertTrue({"200", "404", "500", "503"} <= set(operacao["responses"]))
        self.assertIn(FORMATO_PDF.tipo_mime, operacao["responses"]["200"]["content"])
