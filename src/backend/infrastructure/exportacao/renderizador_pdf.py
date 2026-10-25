"""Gera o arquivo PDF do currículo a partir do documento renderizado.

O módulo implementa a porta ``RenderizadorDocumentoCurriculo`` com o ReportLab
(Platypus), desenhando cabeçalho, seções e blocos na ordem recebida, com
quebra automática de linhas e páginas e variação de tamanho entre os modelos
clássico e compacto. Ele existe para atender ao UC07 e ao CT-RF09-01 sem que a
Application conheça a biblioteca de geração de PDF.
"""

from dataclasses import dataclass
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from backend.application.documento_renderizado import (
    BlocoDocumento,
    CabecalhoDocumento,
    DocumentoCurriculoRenderizado,
)

IDIOMA_DOCUMENTO = "pt-BR"
SEPARADOR_CONTATOS = " | "
CODIFICACAO_FONTES_PADRAO = "cp1252"
COR_TITULOS = colors.HexColor("#1F3A5F")


@dataclass(frozen=True, slots=True)
class EstiloModelo:
    """Agrupa as medidas visuais de um modelo de currículo no PDF.

    O DTO guarda tamanho da fonte base, espaçamento após cada bloco e margem
    da página. Ele existe para que os modelos mudem apenas a aparência,
    mantendo exatamente o mesmo texto.
    """

    tamanho_fonte: float
    espaco_bloco: float
    margem_cm: float


ESTILO_CLASSICO = EstiloModelo(tamanho_fonte=10.5, espaco_bloco=6, margem_cm=2.0)
ESTILO_COMPACTO = EstiloModelo(tamanho_fonte=9, espaco_bloco=3, margem_cm=1.5)
ESTILOS_POR_MODELO = {"compacto": ESTILO_COMPACTO}


class RenderizadorDocumentoCurriculoPdf:
    """Desenha o documento renderizado do currículo em um arquivo PDF.

    O renderizador monta parágrafos do Platypus com o nome em destaque, os
    contatos em uma linha, o título de cada seção e os blocos com título em
    negrito, subtítulo e período em itálico e detalhes; mantém cada bloco
    inteiro na mesma página quando possível e não decide conteúdo. Ele existe
    para implementar a porta de renderização no formato PDF.
    """

    def __init__(self, invariante: bool = False) -> None:
        """Define se o PDF deve ser gerado de forma byte a byte reprodutível.

        Com ``invariante`` verdadeiro, o ReportLab fixa datas e identificadores
        internos do arquivo. O construtor existe para permitir testes e caches
        determinísticos sem mudar o conteúdo visível.
        """
        self._invariante = invariante

    def renderizar(self, documento: DocumentoCurriculoRenderizado) -> bytes:
        """Gera o PDF do currículo e devolve os bytes do arquivo.

        O método escolhe as medidas do modelo, cria o documento A4 com título da
        versão e idioma pt-BR e sem autor, escreve cabeçalho e seções na ordem
        do DTO e salva em memória. Ele existe para entregar à exportação um
        arquivo pronto para download.
        """
        estilo = ESTILOS_POR_MODELO.get(documento.modelo, ESTILO_CLASSICO)
        estilos = _estilos(estilo)
        saida = BytesIO()
        margem = estilo.margem_cm * cm
        pdf = SimpleDocTemplate(
            saida,
            pagesize=A4,
            leftMargin=margem,
            rightMargin=margem,
            topMargin=margem,
            bottomMargin=margem,
            title=documento.titulo_versao,
            author="",
            subject="",
            creator="",
            keywords="",
            lang=IDIOMA_DOCUMENTO,
            invariant=1 if self._invariante else 0,
        )
        historia: list[Flowable] = _cabecalho(documento.cabecalho, estilos)
        for secao in documento.secoes:
            blocos = [_bloco(bloco, estilos) for bloco in secao.blocos]
            primeiro = blocos[0] if blocos else []
            historia.append(
                KeepTogether([Paragraph(_texto(secao.titulo), estilos["secao"]), *primeiro])
            )
            historia.extend(KeepTogether(bloco) for bloco in blocos[1:])
        pdf.build(historia)
        return saida.getvalue()


def _estilos(estilo: EstiloModelo) -> dict[str, ParagraphStyle]:
    """Cria os estilos de parágrafo do currículo para o modelo informado.

    A função deriva tamanhos e espaçamentos da fonte base do modelo, usando
    Helvetica e cores neutras. Ela existe para concentrar a aparência do PDF
    em um único lugar.
    """
    base = estilo.tamanho_fonte
    corpo = ParagraphStyle(
        "corpo", fontName="Helvetica", fontSize=base, leading=base * 1.3, spaceAfter=1
    )
    return {
        "nome": ParagraphStyle(
            "nome", parent=corpo, fontName="Helvetica-Bold", fontSize=base * 2,
            leading=base * 2.4, textColor=COR_TITULOS, spaceAfter=4,
        ),
        "contatos": ParagraphStyle("contatos", parent=corpo, spaceAfter=base),
        "secao": ParagraphStyle(
            "secao", parent=corpo, fontName="Helvetica-Bold", fontSize=base * 1.35,
            leading=base * 1.7, textColor=COR_TITULOS, spaceBefore=base * 0.8,
            spaceAfter=3,
        ),
        "titulo_bloco": ParagraphStyle("titulo_bloco", parent=corpo, fontName="Helvetica-Bold"),
        "destaque": ParagraphStyle("destaque", parent=corpo, fontName="Helvetica-Oblique"),
        "corpo": corpo,
        "espaco": ParagraphStyle("espaco", parent=corpo, spaceAfter=estilo.espaco_bloco),
    }


def _cabecalho(
    cabecalho: CabecalhoDocumento, estilos: dict[str, ParagraphStyle]
) -> list[Flowable]:
    """Monta o nome do estudante e a linha de contatos preenchidos.

    A função junta, separados por barra vertical, apenas os contatos
    informados. Ela existe para que o topo do PDF corresponda à identificação
    mostrada na prévia.
    """
    contatos = [
        cabecalho.email,
        *cabecalho.telefones,
        cabecalho.cidade,
        cabecalho.endereco,
        cabecalho.linkedin,
        cabecalho.curriculo_lattes,
    ]
    return [
        Paragraph(_texto(cabecalho.nome), estilos["nome"]),
        Paragraph(
            _texto(SEPARADOR_CONTATOS.join(item for item in contatos if item)),
            estilos["contatos"],
        ),
    ]


def _bloco(bloco: BlocoDocumento, estilos: dict[str, ParagraphStyle]) -> list[Flowable]:
    """Converte um bloco em parágrafos de título, subtítulo, período e detalhes.

    A função cria um parágrafo por informação presente e termina com um espaço
    proporcional ao modelo. Ela existe para que todo tipo de item apareça de
    forma uniforme no PDF.
    """
    paragrafos: list[Flowable] = [Paragraph(_texto(bloco.titulo), estilos["titulo_bloco"])]
    for texto in (bloco.subtitulo, bloco.periodo):
        if texto:
            paragrafos.append(Paragraph(_texto(texto), estilos["destaque"]))
    paragrafos.extend(Paragraph(_texto(detalhe), estilos["corpo"]) for detalhe in bloco.detalhes)
    paragrafos.append(Spacer(1, estilos["espaco"].spaceAfter))
    return paragrafos


def _texto(valor: str) -> str:
    """Prepara um texto do estudante para um parágrafo do ReportLab.

    A função troca por "?" os caracteres que as fontes padrão do PDF não
    conseguem desenhar (fora da página de código cp1252) e escapa ``<``, ``>`` e
    ``&``, que o ReportLab interpretaria como marcação. Ela existe para que
    nenhum texto vire quadrado preto nem quebre a geração do arquivo.
    """
    representavel = valor.encode(CODIFICACAO_FONTES_PADRAO, "replace").decode(
        CODIFICACAO_FONTES_PADRAO
    )
    return escape(representavel)
