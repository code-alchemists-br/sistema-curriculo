"""Testa a geração PDF do currículo e seu conteúdo textual mínimo."""

import unittest
from dataclasses import replace
from io import BytesIO
from uuid import UUID

from pypdf import PdfReader

from backend.application import (
    BlocoDocumento,
    DocumentoCurriculoRenderizado,
    PreviaVersaoCurriculo,
    RenderizadorDocumentoCurriculo,
    SecaoDocumento,
    montar_documento_renderizado,
)
from backend.domain import Documento, DocumentoId
from backend.domain.secao_curriculo import SecaoCurriculo
from backend.infrastructure.exportacao.renderizador_docx import (
    RenderizadorDocumentoCurriculoDocx,
)
from backend.infrastructure.exportacao.renderizador_pdf import (
    RenderizadorDocumentoCurriculoPdf,
)
from backend.tests.fixtures.curriculo_exportacao import (
    obter_curriculo_exportacao_fixture,
)

URL_ARMAZENAMENTO = "armazenamento/interno/documento-privado.pdf"


def _documento_renderizado(com_documento: bool = False) -> DocumentoCurriculoRenderizado:
    """Monta o documento renderizado a partir da fixture estável de exportação.

    A função usa os itens da fixture como itens selecionados da versão e pode
    incluir um documento complementar com caminho sensível. Ela existe para que
    o PDF seja gerado do mesmo DTO usado pelo DOCX.
    """
    fixture = obter_curriculo_exportacao_fixture()
    documentos = ()
    if com_documento:
        documentos = (
            Documento(
                id=DocumentoId(UUID("88888888-8888-4888-8888-888888888888")),
                usuario_id=fixture.usuario.id,
                nome_arquivo="certificado-ingles.pdf",
                tipo_arquivo="application/pdf",
                url_armazenamento=URL_ARMAZENAMENTO,
            ),
        )
    previa = PreviaVersaoCurriculo(
        usuario=fixture.usuario,
        curriculo=fixture.curriculo,
        formacoes=(fixture.formacao_academica,),
        experiencias=(fixture.experiencia_profissional,),
        projetos=(fixture.projeto_academico,),
        competencias=fixture.competencias,
        idiomas=fixture.idiomas,
        documentos=documentos,
    )
    return montar_documento_renderizado(previa)


def _texto_do_pdf(conteudo: bytes) -> str:
    """Extrai o texto de todas as páginas do PDF, com espaços normalizados.

    A função abre os bytes com pypdf, como um leitor externo faria, e junta o
    texto em uma única linha. Ela existe para que os testes verifiquem o
    arquivo produzido, e não o código que o produziu.
    """
    leitor = PdfReader(BytesIO(conteudo))
    texto = " ".join(pagina.extract_text() or "" for pagina in leitor.pages)
    return " ".join(texto.split())


class RenderizadorPdfTestCase(unittest.TestCase):
    """Verifica o arquivo PDF gerado a partir do documento renderizado.

    Os cenários geram o arquivo em memória e o leem de volta, sem disco, banco
    ou rede. A classe existe para cobrir o conteúdo textual mínimo do UC07 e a
    correspondência com a visualização (CT-RF09-01 e CT-RF09-03).
    """

    def setUp(self) -> None:
        """Gera o PDF padrão e extrai seu texto.

        O setup guarda o documento, os bytes e o texto extraído. Ele existe
        para reduzir repetição entre os cenários.
        """
        self.documento = _documento_renderizado()
        self.conteudo = RenderizadorDocumentoCurriculoPdf().renderizar(self.documento)
        self.texto = _texto_do_pdf(self.conteudo)

    def test_implementa_a_porta_e_gera_um_pdf_valido(self) -> None:
        """Gera bytes de um PDF que abre e tem ao menos uma página.

        O teste usa o renderizador como a porta, confere a assinatura do PDF e
        abre o arquivo. Ele existe para garantir que nunca seja entregue um
        arquivo inválido (CT-RF09-05).
        """
        renderizador: RenderizadorDocumentoCurriculo = RenderizadorDocumentoCurriculoPdf()

        conteudo = renderizador.renderizar(self.documento)

        self.assertTrue(conteudo.startswith(b"%PDF-"))
        self.assertGreaterEqual(len(PdfReader(BytesIO(conteudo)).pages), 1)

    def test_cabecalho_tem_nome_e_contatos(self) -> None:
        """Mostra o nome do estudante e os contatos informados.

        O teste procura nome, e-mail, telefones e links no texto extraído. Ele
        existe para que o PDF comece pela mesma identificação da prévia.
        """
        for esperado in (
            "Ana Carolina da Silva",
            "ana.silva@fatec.sp.gov.br",
            "(11) 98765-4321",
            "(11) 3322-1100",
            "https://linkedin.com/in/estudante-fatec",
        ):
            self.assertIn(esperado, self.texto)
        self.assertTrue(self.texto.startswith("Ana Carolina da Silva"))

    def test_secoes_e_blocos_aparecem_na_ordem_do_documento(self) -> None:
        """Escreve seções e títulos de blocos na mesma ordem do DTO.

        O teste localiza cada título no texto extraído e confere que as posições
        são crescentes. Ele existe para que o PDF siga a ordem da versão e coloque
        cada item na seção certa.
        """
        esperados = []
        for secao in self.documento.secoes:
            esperados.append(secao.titulo)
            esperados.extend(bloco.titulo for bloco in secao.blocos)

        posicoes = [self.texto.index(titulo) for titulo in esperados]

        self.assertEqual(posicoes, sorted(posicoes))

    def test_textos_minimos_de_periodo_e_detalhes(self) -> None:
        """Inclui períodos, subtítulos e detalhes dos itens.

        O teste procura textos característicos da fixture no PDF. Ele existe
        para cobrir o conteúdo textual mínimo pedido pelo card.
        """
        for esperado in (
            "01/2024 - atual",
            "02/2023 - previsão 12/2025",
            "Situação: Em andamento",
            "Empresa de Soluções Tecnológicas Ltda",
            "Técnica - Avançado",
            "Inglês",
        ):
            self.assertIn(esperado, self.texto)
        self.assertIn("Tecnologias: Python, FastAPI, TypeScript", self.texto)

    def test_mesmo_conteudo_do_docx(self) -> None:
        """Mostra os mesmos títulos de seção e de bloco que o DOCX gerado do DTO.

        O teste gera o DOCX do mesmo documento e confere que todos os seus
        títulos aparecem no PDF. Ele existe para que os dois formatos exportem o
        mesmo currículo (CT-RF09-03).
        """
        from docx import Document

        docx = Document(BytesIO(RenderizadorDocumentoCurriculoDocx().renderizar(self.documento)))
        titulos_docx = [
            paragrafo.text for paragrafo in docx.paragraphs
            if paragrafo.style.name in {"Title", "Heading 1"}
        ]

        for titulo in titulos_docx:
            self.assertIn(titulo, self.texto)

    def test_modelos_classico_e_compacto_geram_o_mesmo_texto(self) -> None:
        """Muda apenas a aparência entre os modelos, nunca o conteúdo.

        O teste gera o PDF nos modelos clássico e compacto e compara o texto
        extraído. Ele existe para que trocar de modelo não altere o currículo.
        """
        classico = RenderizadorDocumentoCurriculoPdf().renderizar(
            replace(self.documento, modelo="classico")
        )
        compacto = RenderizadorDocumentoCurriculoPdf().renderizar(
            replace(self.documento, modelo="compacto")
        )

        self.assertEqual(_texto_do_pdf(classico), _texto_do_pdf(compacto))
        self.assertNotEqual(classico, compacto)

    def test_metadados_e_conteudo_sem_dados_internos(self) -> None:
        """Mantém fora do arquivo IDs, hash e armazenamento, e sem autor.

        O teste gera o PDF com um documento complementar e procura dados
        internos no texto e nos metadados, além de conferir o título. Ele existe
        para que o arquivo exportado não revele dados internos.
        """
        conteudo = RenderizadorDocumentoCurriculoPdf().renderizar(
            _documento_renderizado(com_documento=True)
        )
        texto = _texto_do_pdf(conteudo)
        metadados = PdfReader(BytesIO(conteudo)).metadata
        fixture = obter_curriculo_exportacao_fixture()

        self.assertIn("certificado-ingles.pdf", texto)
        for proibido in (
            URL_ARMAZENAMENTO,
            fixture.usuario.hash_senha.valor,
            str(fixture.usuario.id.valor),
        ):
            self.assertNotIn(proibido, texto)
            self.assertNotIn(proibido, str(dict(metadados)))
        self.assertEqual(metadados.title, self.documento.titulo_versao)
        self.assertFalse(metadados.author)

    def test_textos_com_marcacao_e_caracteres_especiais_nao_quebram_o_pdf(self) -> None:
        """Escapa marcação e substitui caracteres que a fonte não desenha.

        O teste usa um bloco com ``<``, ``&`` e um caractere fora da página de
        código das fontes padrão. Ele existe para que nenhum texto do estudante
        impeça a geração do arquivo ou vire quadrado preto.
        """
        documento = replace(
            self.documento,
            secoes=(
                SecaoDocumento(
                    secao=SecaoCurriculo.PROJETOS_ACADEMICOS,
                    titulo="Projetos acadêmicos",
                    blocos=(BlocoDocumento(titulo="API <REST> & Testes", detalhes=("Nota ✓ ok",)),),
                ),
            ),
        )

        texto = _texto_do_pdf(RenderizadorDocumentoCurriculoPdf().renderizar(documento))

        self.assertIn("API <REST> & Testes", texto)
        self.assertIn("Nota ? ok", texto)

    def test_muitos_itens_quebram_em_varias_paginas_sem_perder_texto(self) -> None:
        """Distribui um currículo longo em várias páginas sem perder blocos.

        O teste cria uma seção com muitos blocos e confere que o PDF tem mais de
        uma página e todos os títulos. Ele existe para cobrir a quebra de página
        automática, base do RNF07.
        """
        blocos = tuple(
            BlocoDocumento(titulo=f"Experiência {numero:02d}", detalhes=("Atividade " * 30,))
            for numero in range(40)
        )
        documento = replace(
            self.documento,
            secoes=(
                SecaoDocumento(
                    secao=SecaoCurriculo.EXPERIENCIAS_PROFISSIONAIS,
                    titulo="Experiência profissional",
                    blocos=blocos,
                ),
            ),
        )

        conteudo = RenderizadorDocumentoCurriculoPdf().renderizar(documento)

        self.assertGreater(len(PdfReader(BytesIO(conteudo)).pages), 1)
        texto = _texto_do_pdf(conteudo)
        for bloco in blocos:
            self.assertIn(bloco.titulo, texto)

    def test_modo_invariante_gera_bytes_identicos(self) -> None:
        """Produz exatamente o mesmo arquivo para o mesmo documento.

        O teste gera o PDF duas vezes com o modo invariante ativo. Ele existe
        para permitir comparações e caches determinísticos.
        """
        renderizador = RenderizadorDocumentoCurriculoPdf(invariante=True)

        self.assertEqual(
            renderizador.renderizar(self.documento), renderizador.renderizar(self.documento)
        )

    def test_documento_sem_secoes_gera_somente_o_cabecalho(self) -> None:
        """Gera um PDF válido apenas com nome e contatos.

        O teste remove todas as seções do documento. Ele existe para que uma
        versão sem itens selecionados ainda produza um arquivo coerente.
        """
        texto = _texto_do_pdf(
            RenderizadorDocumentoCurriculoPdf().renderizar(replace(self.documento, secoes=()))
        )

        self.assertIn("Ana Carolina da Silva", texto)
        self.assertNotIn("Formação acadêmica", texto)
