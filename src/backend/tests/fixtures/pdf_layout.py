"""Fornece dados e leitura nominal restrita para integração do gerador PDF.

Gera DTOs e PDFs sintéticos em memória e mede somente o subconjunto calibrado
na análise. Não é um renderizador genérico nem certifica tinta ou leitores.
"""

# Proveniência: decision-analysis prompts/backend/20261031-132242-regressao-pdf-corte-sobreposicao-v002.md#v002
from __future__ import annotations

import math
import re
from dataclasses import dataclass, replace
from io import BytesIO

from backend.application.documento_renderizado import (
    BlocoDocumento,
    CabecalhoDocumento,
    DocumentoCurriculoRenderizado,
    SecaoDocumento,
    montar_documento_renderizado,
)
from backend.application.previa_versao_curriculo import PreviaVersaoCurriculo
from backend.domain.secao_curriculo import SecaoCurriculo
from backend.tests.fixtures.curriculo_exportacao import (
    obter_curriculo_exportacao_fixture,
)

DEPENDENCIA_AUSENTE = None
try:
    from pypdf import PdfReader
    from pypdf.generic import ByteStringObject, ContentStream, TextStringObject
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfgen.canvas import Canvas
except ModuleNotFoundError as erro:
    if erro.name not in {"reportlab", "pypdf"}:
        raise
    DEPENDENCIA_AUSENTE = erro.name

# Oráculos literais aprovados; não importar medidas do renderizador.
LARGURA_A4 = 595.27559055
ALTURA_A4 = 841.88976378
ERRO_PAGINA = 0.05
MARGEM_CLASSICA = 56.69291339
MARGEM_COMPACTA = 42.51968504
FOLGA = 0.5
IDENTIDADE = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
FONTES = {"Helvetica", "Helvetica-Bold", "Helvetica-Oblique"}
OPERADORES = {
    b"cm": 6,
    b"q": 0,
    b"Q": 0,
    b"BT": 0,
    b"ET": 0,
    b"Tf": 2,
    b"TL": 1,
    b"Tm": 6,
    b"Tj": 1,
    b"T*": 0,
    b"rg": 3,
    b"Tw": 1,
}
TEXTOS_NORMAL = (
    "Pessoa Sintética",
    "pessoa@example.invalid",
    "https://example.invalid/perfil",
    "Formação acadêmica",
    "Tecnologia em Análise e Desenvolvimento de Sistemas",
    "Faculdade de Tecnologia de São Paulo (FATEC-SP) - Tecnólogo",
    "02/2023 - previsão 12/2025",
    "Situação: Em andamento",
    "Experiência profissional",
    "Estagiária de Desenvolvimento de Software",
    "Empresa de Soluções Tecnológicas Ltda",
    "01/2024 - atual",
    "Atuação no desenvolvimento de APIs RESTful utilizando Python e FastAPI, "
    "modelagem de banco de dados relacional e criação de suítes de testes "
    "automatizados para controle de qualidade de software.",
    "Projetos acadêmicos",
    "Sistema de Apoio Curricular Profissional",
    "Plataforma completa para centralização de perfil estudantil, assistência "
    "na redação de trajetórias acadêmicas e exportação automatizada de currículos.",
    "Tecnologias: Python, FastAPI, TypeScript, React, PostgreSQL, Nix",
    "Competências",
    "Python e Clean Architecture",
    "Técnica - Avançado",
    "FastAPI e APIs RESTful",
    "Técnica - Intermediário",
    "Idiomas",
    "Inglês",
    "Avançado",
    "Espanhol",
    "Intermediário",
)


@dataclass(frozen=True)
class CampoEsperado:
    """Descreve um campo usando literais e sentinelas para detectar perda e duplicação."""

    identificador: str
    marcador_inicio: str
    marcador_fim: str
    texto: str
    token_sem_quebra: str | None = None
    separador_antes: str = " "

    @property
    def marcado(self) -> str:
        """Envolve o literal em sentinelas distintas para comparar o campo completo."""
        return f"{self.marcador_inicio} {self.texto} {self.marcador_fim}"


@dataclass(frozen=True)
class CasoPdfLayout:
    """Agrupa DTO e manifesto independente, usando tuplas para isolar cada geração."""

    documento: DocumentoCurriculoRenderizado
    esperado: tuple[CampoEsperado, ...]
    cenario: str


@dataclass(frozen=True)
class CaixaTexto:
    """Registra palavra e quatro cantos transformados para localizar violações nominais."""

    pagina: int
    ordem: int
    texto: str
    fonte: str
    tamanho: float
    cm: tuple[float, ...]
    tm: tuple[float, ...]
    cantos: tuple[tuple[float, float], ...]
    caixa: tuple[float, float, float, float]
    inicio_texto: int


@dataclass(frozen=True)
class RunPdf:
    """Conserva cada Tj em ordem de emissão para medir linhas sem agregar parágrafos."""

    pagina: int
    ordem: int
    texto: str
    palavras: tuple[CaixaTexto, ...]
    separador_antes: str = ""


@dataclass(frozen=True)
class PaginaPdf:
    """Guarda caixas efetivas da página para confrontar a área visível com o contrato."""

    numero: int
    mediabox: tuple[float, ...]
    cropbox: tuple[float, ...]
    rotacao: int
    unidade: float


@dataclass(frozen=True)
class GeometriaPdf:
    """Reúne páginas, runs e extração independente para auditar conteúdo e posições."""

    paginas: tuple[PaginaPdf, ...]
    runs: tuple[RunPdf, ...]
    texto_extraido: str

    @property
    def texto(self) -> str:
        """Une runs com quebras explícitas para preservar limites medidos pelo leitor."""
        return "".join(run.separador_antes + run.texto for run in self.runs)


@dataclass(frozen=True)
class ProblemaPdf:
    """Transporta evidência por página e caixa para explicar reprovações sem imagens."""

    tipo: str
    motivo: str
    pagina: int | None = None
    marcadores: tuple[str, ...] = ()
    caixa_a: CaixaTexto | None = None
    caixa_b: CaixaTexto | None = None
    profundidade_x: float | None = None
    profundidade_y: float | None = None
    invasoes: tuple[float, ...] = ()


@dataclass(frozen=True)
class RelatorioPdfLayout:
    """Distingue aprovação de reprovação com evidências para evitar falso verde textual."""

    geometria: GeometriaPdf
    problemas: tuple[ProblemaPdf, ...]

    @property
    def estado(self) -> str:
        """Deriva o estado da lista de defeitos para não esconder relatórios reprovados."""
        return "reprovado" if self.problemas else "aprovado"

    def resumo(self) -> str:
        """Resume os primeiros defeitos com suas caixas para tornar falhas investigáveis."""
        return (
            f"{self.estado}: {len(self.problemas)} problema(s): {self.problemas[:6]!r}"
        )


@dataclass(frozen=True)
class ControlePdfLayout:
    """Agrupa bytes, manifesto e categoria deliberada para provar sensibilidade real."""

    conteudo: bytes
    esperado: tuple[CampoEsperado, ...]
    tipo_esperado: str | None


class OraculoPdfNaoSuportado(AssertionError):
    """Interrompe medições não calibradas por exceção explícita para impedir aprovação indevida."""


def _recusar(condicao: bool, contexto: str) -> None:
    """Rejeita condições fora do subconjunto com contexto para não convertê-las em skips."""
    if not condicao:
        raise OraculoPdfNaoSuportado(f"oráculo não suporta {contexto}")


def _numeros(valores) -> tuple[float, ...]:
    """Valida operandos finitos convertendo números PDF para evitar caixas inválidas."""
    _recusar(
        all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in valores),
        f"operandos não numéricos {valores!r}",
    )
    numeros = tuple(float(v) for v in valores)
    _recusar(all(math.isfinite(v) for v in numeros), f"operandos não finitos {numeros}")
    return numeros


def _ponto(x: float, y: float, matriz: tuple[float, ...]) -> tuple[float, float]:
    """Aplica uma matriz afim ao ponto para compor os quatro cantos nominais."""
    a, b, c, d, e, f = matriz
    return a * x + c * y + e, b * x + d * y + f


def _normalizar(texto: str, esperado: tuple[CampoEsperado, ...]) -> str:
    """Normaliza só espaços e quebras controladas para não apagar acentos ou pontuação."""
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    for campo in esperado:
        if campo.token_sem_quebra:
            token = campo.token_sem_quebra
            # Apenas as quebras conhecidas desse token; nunca eliminar espaços globais.
            padrao = "[\n]*".join(re.escape(c) for c in token)
            texto = re.sub(padrao, token, texto)
    return re.sub(r"[ \n]+", " ", texto).strip()


def _marcar_documento(documento, cenario, literais=None, token=None) -> CasoPdfLayout:
    """Marca campos e monta manifesto dos insumos para comparar toda a saída sem ler o PDF."""
    campos = []

    def marcar(valor, separador=" "):
        """Etiqueta um valor conhecido usando posição estável para detectar perdas por campo."""
        if valor is None or valor == "":
            return valor
        indice = len(campos)
        identificador = f"F{indice:03d}"
        literal = literais[indice] if literais is not None else valor
        if cenario == "P05" and valor == "Nota ✓ ok":
            literal = "Nota ? ok"
        campos.append(
            CampoEsperado(
                identificador,
                identificador + "I",
                identificador + "Z",
                literal,
                token if token and token in valor else None,
                separador,
            )
        )
        return f"{identificador}I {valor} {identificador}Z"

    c = documento.cabecalho
    nome = marcar(c.nome, "")
    email = marcar(c.email)
    telefones = tuple(marcar(t, " | ") for t in c.telefones)
    extras = [
        marcar(v, " | ") for v in (c.cidade, c.endereco, c.linkedin, c.curriculo_lattes)
    ]
    cabecalho = CabecalhoDocumento(
        nome, email, telefones, extras[1], extras[0], extras[2], extras[3]
    )
    secoes = []
    for secao in documento.secoes:
        titulo = marcar(secao.titulo)
        blocos = []
        for bloco in secao.blocos:
            blocos.append(
                BlocoDocumento(
                    marcar(bloco.titulo),
                    marcar(bloco.subtitulo),
                    marcar(bloco.periodo),
                    tuple(marcar(d) for d in bloco.detalhes),
                )
            )
        secoes.append(replace(secao, titulo=titulo, blocos=tuple(blocos)))
    if literais is not None:
        assert len(campos) == len(literais), "A fixture mudou a quantidade de campos"
    return CasoPdfLayout(
        replace(documento, cabecalho=cabecalho, secoes=tuple(secoes)),
        tuple(campos),
        cenario,
    )


def criar_documento_pdf_layout(
    cenario: str,
    *,
    modelo: str = "classico",
    comprimento_token: int | None = None,
    campo_token: str | None = None,
    subcaso: str | None = None,
) -> CasoPdfLayout:
    """Constrói os cenários finitos aprovados com DTOs sintéticos para integrar gerador e leitor."""
    if cenario not in {"P01", "P02", "P03", "P04", "P05", "P06", "N06"}:
        raise ValueError(cenario)
    cabecalho = CabecalhoDocumento(
        "Pessoa Sintética",
        "pessoa@example.invalid",
        linkedin="https://example.invalid/perfil",
    )
    documento = DocumentoCurriculoRenderizado(
        "Regressão PDF sintética", modelo, "curriculo-sintetico", cabecalho, ()
    )
    token = None
    literais = None
    secao = SecaoCurriculo.PROJETOS_ACADEMICOS
    titulo = "Projetos acadêmicos"
    blocos = (
        BlocoDocumento(
            "Modelo sintético", "Subtítulo sintético", detalhes=("Conteúdo de modelo",)
        ),
    )
    if cenario == "P01":
        f = obter_curriculo_exportacao_fixture()
        previa = PreviaVersaoCurriculo(
            usuario=f.usuario,
            curriculo=f.curriculo,
            formacoes=(f.formacao_academica,),
            experiencias=(f.experiencia_profissional,),
            projetos=(f.projeto_academico,),
            competencias=f.competencias,
            idiomas=f.idiomas,
            documentos=(),
        )
        documento = replace(
            montar_documento_renderizado(previa),
            modelo=modelo,
            cabecalho=cabecalho,
            titulo_versao=documento.titulo_versao,
            nome_arquivo_base=documento.nome_arquivo_base,
        )
        literais = TEXTOS_NORMAL
    elif cenario == "P02":
        secao, titulo = (
            SecaoCurriculo.EXPERIENCIAS_PROFISSIONAIS,
            "Experiência profissional",
        )
        blocos = tuple(
            BlocoDocumento(
                f"Bloco {i:02d}",
                f"Subtítulo {i:02d}",
                "01/2024 - 12/2024",
                (" ".join(f"V{i:02d}_{j:02d}" for j in range(30)),),
            )
            for i in range(40)
        )
    elif cenario == "P03":
        if comprimento_token not in {512, 2048} or campo_token not in {"C", "D"}:
            raise ValueError("P03 exige comprimento 512/2048 e campo C/D")
        inicio = f"I{campo_token}{comprimento_token:04d}"
        fim = f"F{campo_token}{comprimento_token:04d}"
        token = inicio + "X" * (comprimento_token - len(inicio) - len(fim)) + fim
        blocos = (
            BlocoDocumento(
                "Bloco token",
                detalhes=(token if campo_token == "D" else "Detalhe curto",),
            ),
        )
        if campo_token == "C":
            documento = replace(
                documento,
                cabecalho=replace(
                    cabecalho, linkedin="https://example.invalid/" + token
                ),
            )
    elif cenario == "P04":
        blocos = (
            BlocoDocumento(
                "Bloco extenso",
                "Subtítulo sintético",
                "01/2024 - 12/2024",
                tuple(f"D{j:03d} Ação sintética FIM{j:03d}" for j in range(120)),
            ),
        )
    elif cenario == "P05":
        if subcaso not in {"opcionais", "sem_secoes", "caracteres"}:
            raise ValueError("Subcaso P05 desconhecido")
        documento = replace(documento, cabecalho=replace(cabecalho, linkedin=None))
        blocos = (BlocoDocumento("Opcional"),)
        if subcaso == "caracteres":
            blocos = (BlocoDocumento("Ação <REST> & ç", detalhes=("Nota ✓ ok",)),)
    elif cenario == "N06":
        blocos = (
            BlocoDocumento(
                "Bloco leading", detalhes=(" ".join(f"L{i:03d}" for i in range(120)),)
            ),
        )
    if cenario != "P01":
        secoes = (
            ()
            if cenario == "P05" and subcaso == "sem_secoes"
            else (SecaoDocumento(secao, titulo, blocos),)
        )
        documento = replace(documento, secoes=secoes)
    return _marcar_documento(documento, cenario, literais, token)


def _fontes_pagina(pagina, numero):
    """Resolve fontes WinAnsi permitidas por recurso para medir sem fontes do sistema."""
    recursos = pagina["/Resources"]
    _recusar(
        not (set(recursos) - {"/Font", "/ProcSet"}),
        f"recurso página {numero}: {tuple(recursos)}",
    )
    _recusar(
        not pagina.get("/Annots") and not pagina.get("/Group"),
        f"anotações/grupo página {numero}",
    )
    fontes = {}
    _recusar("/Font" in recursos, f"fontes ausentes página {numero}")
    for chave, referencia in recursos["/Font"].items():
        f = referencia.get_object()
        nome = str(f.get("/BaseFont", "")).lstrip("/")
        _recusar(
            nome in FONTES
            and f.get("/Subtype") == "/Type1"
            and f.get("/Encoding") == "/WinAnsiEncoding"
            and not (set(f) - {"/Type", "/Subtype", "/BaseFont", "/Encoding", "/Name"}),
            f"fonte página {numero}: {dict(f)!r}",
        )
        fontes[str(chave)] = nome
    return fontes


def _caixas_palavras(texto, numero, ordem, fonte, tamanho, tw, cm, tm, inicio):
    """Mede palavras com avanços de fonte e Tw para transformar seus quatro cantos."""
    asc, desc = pdfmetrics.getAscentDescent(fonte, tamanho)
    palavras = []
    for match in re.finditer(r"[^ ]+", texto):
        prefixo = texto[: match.start()]
        x = pdfmetrics.stringWidth(prefixo, fonte, tamanho) + tw * prefixo.count(" ")
        largura = pdfmetrics.stringWidth(match[0], fonte, tamanho)
        cantos = tuple(
            _ponto(*_ponto(px, py, tm), cm)
            for px, py in ((x, desc), (x + largura, desc), (x + largura, asc), (x, asc))
        )
        caixa = (
            min(p[0] for p in cantos),
            min(p[1] for p in cantos),
            max(p[0] for p in cantos),
            max(p[1] for p in cantos),
        )
        palavras.append(
            CaixaTexto(
                numero,
                ordem,
                match[0],
                fonte,
                tamanho,
                cm,
                tm,
                cantos,
                caixa,
                inicio + match.start(),
            )
        )
    return tuple(palavras)


def extrair_geometria_pdf(conteudo: bytes) -> GeometriaPdf:
    """Extrai cada Tj do subconjunto calibrado para preservar linhas e medir caixas nominais."""
    leitor = PdfReader(BytesIO(conteudo))
    _recusar(bool(leitor.pages), "PDF sem páginas")
    paginas, runs, textos = [], [], []
    inicio_texto = 0
    for numero, pagina in enumerate(leitor.pages, 1):
        media, crop = _numeros(pagina.mediabox), _numeros(pagina.cropbox)
        rotacao, unidade = pagina.rotation, float(pagina.get("/UserUnit", 1))
        _recusar(
            rotacao == 0 and unidade == 1 and media[:2] == (0, 0),
            f"rotação/unidade/origem página {numero}: {rotacao}, {unidade}, {media}",
        )
        _recusar(
            crop[2] > crop[0] and crop[3] > crop[1], f"CropBox página {numero}: {crop}"
        )
        fontes = _fontes_pagina(pagina, numero)
        operacoes = ContentStream(pagina.get_contents(), leitor).operations
        for args, op in operacoes:
            _recusar(
                op in OPERADORES and len(args) == OPERADORES[op],
                f"operador página {numero}: {op!r} {args!r}",
            )
            if op not in {b"Tj", b"Tf"}:
                _numeros(args)
        estado = {"fonte": None, "tamanho": 0.0, "tw": 0.0}
        pilha = []
        dentro_texto = posicionado = False
        cursor = 0.0
        nova_linha = True
        quantidade_tj = 0

        def antes(op, args, matriz_cm, matriz_tm):
            """Fotografa estado antes de cada Tj para não atribuir caixas a callbacks agregados."""
            nonlocal \
                dentro_texto, \
                posicionado, \
                inicio_texto, \
                quantidade_tj, \
                cursor, \
                nova_linha
            contexto = f"página {numero}, operador {op!r}, operandos {args!r}"
            if op == b"q":
                _recusar(not dentro_texto, contexto)
                pilha.append(estado.copy())
            elif op == b"Q":
                _recusar(bool(pilha) and not dentro_texto, contexto)
                estado.update(pilha.pop())
            elif op == b"BT":
                _recusar(not dentro_texto, contexto)
                dentro_texto, posicionado = True, False
                cursor, nova_linha = 0.0, True
            elif op == b"ET":
                _recusar(dentro_texto, contexto)
                dentro_texto = False
            elif op == b"Tf":
                (tamanho,) = _numeros(args[1:])
                _recusar(
                    dentro_texto and str(args[0]) in fontes and tamanho > 0, contexto
                )
                estado.update(fonte=fontes[str(args[0])], tamanho=tamanho)
            elif op == b"Tw":
                _recusar(dentro_texto, contexto)
                estado["tw"] = float(args[0])
            elif op == b"TL":
                _recusar(dentro_texto, contexto)
            elif op == b"Tm":
                _recusar(
                    dentro_texto and _numeros(args)[:4] == IDENTIDADE[:4], contexto
                )
                posicionado = True
                cursor, nova_linha = 0.0, True
            elif op == b"T*":
                _recusar(dentro_texto and posicionado, contexto)
                posicionado = True
                cursor, nova_linha = 0.0, True
            elif op == b"cm":
                a, b, c, d, _, _ = _numeros(args)
                _recusar(not dentro_texto and b == c == 0 and a > 0 and d > 0, contexto)
            elif op == b"Tj":
                _recusar(
                    dentro_texto and posicionado and estado["fonte"] is not None,
                    contexto + " sem posição/fonte validada",
                )
                _recusar(
                    isinstance(args[0], (TextStringObject, ByteStringObject)), contexto
                )
                bruto = (
                    args[0].get_original_bytes()
                    if isinstance(args[0], TextStringObject)
                    else bytes(args[0])
                )
                texto = bruto.decode("cp1252")
                _recusar(not any(c in texto for c in "\t\r\n"), contexto)
                cm, tm = _numeros(matriz_cm), _numeros(matriz_tm)
                _recusar(
                    cm[1] == cm[2] == 0
                    and cm[0] > 0
                    and cm[3] > 0
                    and tm[:4] == IDENTIDADE[:4],
                    contexto + " matriz não calibrada",
                )
                # Tj avança o cursor PDF, mas o callback de pypdf conserva Tm.
                # Somar somente os avanços Type1/WinAnsi/Tw já medidos na linha.
                tm = (*tm[:4], tm[4] + cursor, tm[5])
                separador = "\n" if nova_linha and runs else ""
                inicio_texto += len(separador)
                palavras = _caixas_palavras(
                    texto,
                    numero,
                    len(runs),
                    estado["fonte"],
                    estado["tamanho"],
                    estado["tw"],
                    cm,
                    tm,
                    inicio_texto,
                )
                runs.append(RunPdf(numero, len(runs), texto, palavras, separador))
                inicio_texto += len(texto)
                quantidade_tj += 1
                cursor += pdfmetrics.stringWidth(
                    texto, estado["fonte"], estado["tamanho"]
                ) + estado["tw"] * texto.count(" ")
                nova_linha = False

        textos.append(pagina.extract_text(visitor_operand_before=antes))
        _recusar(
            not pilha and not dentro_texto, f"estado não balanceado página {numero}"
        )
        _recusar(
            quantidade_tj == sum(op == b"Tj" for _, op in operacoes),
            f"Tj não representado página {numero}",
        )
        paginas.append(PaginaPdf(numero, media, crop, rotacao, unidade))
    return GeometriaPdf(tuple(paginas), tuple(runs), "\n".join(textos))


def _identificar(palavra, texto, esperado):
    """Relaciona fragmentos às sentinelas do campo para diagnosticar até linhas sem marcador."""
    for campo in esperado:
        inicio = texto.find(campo.marcador_inicio)
        fim = texto.find(campo.marcador_fim, max(0, inicio))
        if inicio >= 0 and inicio <= palavra.inicio_texto < fim + len(
            campo.marcador_fim
        ):
            return campo.identificador
    return f"run{palavra.ordem}"


def _limite_inferior(palavra: CaixaTexto) -> float:
    """Ordena pela borda inferior para limitar pares ativos sem mudar a ordem textual."""
    return palavra.caixa[1]


def auditar_pdf_layout(
    conteudo: bytes, *, esperado: tuple[CampoEsperado, ...], modelo: str
) -> RelatorioPdfLayout:
    """Compara manifesto, área e interseções usando o leitor real para auditar o PDF produzido."""
    geometria = extrair_geometria_pdf(conteudo)
    texto = geometria.texto
    problemas = []
    for campo in esperado:
        contagens = (
            texto.count(campo.marcador_inicio),
            texto.count(campo.marcador_fim),
        )
        if contagens != (1, 1):
            problemas.append(
                ProblemaPdf(
                    "conteudo_ausente",
                    "duplicado" if max(contagens) > 1 else "ausente",
                    marcadores=(campo.identificador,),
                )
            )
    literal = "".join(c.separador_antes + c.marcado for c in esperado)
    normal = _normalizar(texto, esperado)
    if normal != _normalizar(literal, esperado):
        problemas.append(ProblemaPdf("conteudo_ausente", "diferenca_textual"))
    if normal != _normalizar(geometria.texto_extraido, esperado):
        problemas.append(ProblemaPdf("conteudo_ausente", "leitura_textual_divergente"))
    margem = MARGEM_COMPACTA if modelo == "compacto" else MARGEM_CLASSICA
    for pagina in geometria.paginas:
        media, crop = pagina.mediabox, pagina.cropbox
        if (
            abs(media[2] - LARGURA_A4) > ERRO_PAGINA
            or abs(media[3] - ALTURA_A4) > ERRO_PAGINA
        ):
            problemas.append(
                ProblemaPdf("fora_area", "dimensoes_pagina", pagina.numero)
            )
        area = (
            max(margem, media[0], crop[0]),
            max(margem, media[1], crop[1]),
            min(LARGURA_A4 - margem, media[2], crop[2]),
            min(ALTURA_A4 - margem, media[3], crop[3]),
        )
        palavras = [
            p
            for run in geometria.runs
            if run.pagina == pagina.numero
            for p in run.palavras
        ]
        for palavra in palavras:
            x0, y0, x1, y1 = palavra.caixa
            invasoes = (area[0] - x0, area[1] - y0, x1 - area[2], y1 - area[3])
            if max(invasoes) > FOLGA:
                problemas.append(
                    ProblemaPdf(
                        "fora_area",
                        "caixa_fora_da_area",
                        pagina.numero,
                        (_identificar(palavra, texto, esperado),),
                        palavra,
                        invasoes=invasoes,
                    )
                )
        ativos = []
        for palavra in sorted(palavras, key=_limite_inferior):
            ativos = [p for p in ativos if p.caixa[3] - palavra.caixa[1] > FOLGA]
            for anterior in ativos:
                a, b = anterior.caixa, palavra.caixa
                dx = min(a[2], b[2]) - max(a[0], b[0])
                dy = min(a[3], b[3]) - max(a[1], b[1])
                if dx > FOLGA and dy > FOLGA:
                    problemas.append(
                        ProblemaPdf(
                            "sobreposicao",
                            "caixas_interceptadas",
                            pagina.numero,
                            (
                                _identificar(anterior, texto, esperado),
                                _identificar(palavra, texto, esperado),
                            ),
                            anterior,
                            palavra,
                            dx,
                            dy,
                        )
                    )
            ativos.append(palavra)
    return RelatorioPdfLayout(geometria, tuple(problemas))


def criar_pdf_controle_defeituoso(
    tipo: str,
    *,
    variante: str = "padrao",
    dx: float | None = None,
    dy: float | None = None,
) -> ControlePdfLayout:
    """Desenha controles Canvas com posições conhecidas para exercitar o auditor real.

    No limite externo, um único dx/dy informa a invasão: positivo indica
    esquerda/inferior; negativo, direita/superior. Os outros casos conservam
    dados e áreas para isolar o defeito deliberado sem duplicar o auditor.
    """
    if tipo not in {"fora_area", "sobreposicao", "conteudo_ausente", "instrumento"}:
        raise ValueError(tipo)
    variantes = {
        "valido",
        "padrao",
        "mediabox",
        "ctm",
        "duplicado",
        "diferenca_textual",
        "limiar",
        "fonte",
        "rotacao",
        "clipping",
    }
    if variante not in variantes:
        raise ValueError(variante)
    palavras = ("ALFA", "OMEGA")
    if tipo == "instrumento":
        palavras = ("M", "N") if variante == "limiar" else ("Ação CONTROLE", "ITÁLICO")
    campos = tuple(
        CampoEsperado(
            f"F{i:03d}",
            f"F{i:03d}I",
            f"F{i:03d}Z",
            t,
            separador_antes="" if i == 0 else " ",
        )
        for i, t in enumerate(palavras)
    )
    saida = BytesIO()
    canvas = Canvas(saida, pagesize=(LARGURA_A4, ALTURA_A4), invariant=1)
    canvas.setFont("Helvetica", 12)
    primeiro, segundo = campos[0].marcado, campos[1].marcado
    x0, y0, x1, y1 = 100.0, 200.0, 100.0, 160.0
    defeito = None if variante == "valido" else tipo
    if tipo == "fora_area" and variante != "valido":
        x0 = -10 if variante == "mediabox" else MARGEM_CLASSICA - 10
        if variante == "limiar":
            x0 = 100.0
            if (dx is None) == (dy is None):
                raise ValueError("O limite externo exige exatamente um eixo")
            asc, desc = pdfmetrics.getAscentDescent("Helvetica", 12)
            if dx is not None:
                x0 = (
                    MARGEM_CLASSICA - dx
                    if dx >= 0
                    else LARGURA_A4
                    - MARGEM_CLASSICA
                    - dx
                    - pdfmetrics.stringWidth(primeiro, "Helvetica", 12)
                )
            else:
                y0 = (
                    MARGEM_CLASSICA - dy - desc
                    if dy >= 0
                    else ALTURA_A4 - MARGEM_CLASSICA - dy - asc
                )
    elif tipo == "sobreposicao":
        y1 = 180 if variante == "valido" else y0
        if variante == "ctm":
            canvas.translate(20, 30)
    elif tipo == "instrumento":
        defeito = None
        if variante == "limiar":
            if dx is None or dy is None:
                raise ValueError("O controle de interseção exige dx/dy")
            x1 = x0 + pdfmetrics.stringWidth(primeiro, "Helvetica", 12) - dx
            y1 = y0 + 11.1 - dy
        else:
            canvas.saveState()
            canvas.translate(100, 200)
            canvas.scale(1.25, 0.75)
            canvas.setFont("Helvetica-Bold", 12)
            if variante == "ctm":
                corte = primeiro.index("CONTROLE") + 4
                objeto = canvas.beginText(10, 20)
                objeto.setFont("Helvetica-Bold", 12)
                objeto.textOut(primeiro[:corte])
                objeto.textOut(primeiro[corte:])
                canvas.drawText(objeto)
            else:
                canvas.drawString(10, 20, primeiro)
            canvas.restoreState()
            canvas.setFont("Helvetica-Oblique", 12)
            x1, y1 = 50, 100
            primeiro = ""
        if variante == "fonte":
            canvas.setFont("Times-Roman", 12)
        elif variante == "rotacao":
            canvas.rotate(15)
        elif variante == "clipping":
            caminho = canvas.beginPath()
            caminho.rect(0, 0, 500, 700)
            canvas.clipPath(caminho, stroke=0, fill=0)
    if primeiro:
        canvas.drawString(x0, y0, primeiro)
    if tipo != "conteudo_ausente" or variante in {
        "valido",
        "duplicado",
        "diferenca_textual",
    }:
        canvas.drawString(
            x1,
            y1,
            segundo.replace("OMEGA", "OMEGA!")
            if variante == "diferenca_textual"
            else segundo,
        )
    if variante == "duplicado":
        canvas.drawString(100, 120, segundo)
    canvas.save()
    return ControlePdfLayout(saida.getvalue(), campos, defeito)
