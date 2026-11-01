"""Integra gerador e leitor reais para proteger conteúdo e caixas nominais do PDF.

Os cenários finitos e seus controles medem somente o subconjunto da análise;
não certificam tinta, impressão, acessibilidade ou leitores específicos.
"""

# Proveniência: decision-analysis prompts/backend/20261031-132242-regressao-pdf-corte-sobreposicao-v002.md#v002
import unittest
from dataclasses import replace
from unittest.mock import patch

from backend.domain.modelo_curriculo import ModeloCurriculo
from backend.tests.fixtures.pdf_layout import (
    DEPENDENCIA_AUSENTE,
    OraculoPdfNaoSuportado,
    auditar_pdf_layout,
    criar_documento_pdf_layout,
    criar_pdf_controle_defeituoso,
)

if DEPENDENCIA_AUSENTE is None:
    from reportlab.pdfbase import pdfmetrics

    from backend.infrastructure.exportacao import renderizador_pdf


@unittest.skipIf(
    DEPENDENCIA_AUSENTE is not None,
    f"ambiente: {DEPENDENCIA_AUSENTE} ausente; executar nix develop .#tests "
    "--command env PYTHONPATH=src python -m unittest -v "
    "backend.tests.test_integracao_regressao_pdf_layout",
)
class RegressaoPdfLayoutIntegracaoTestCase(unittest.TestCase):
    """Audita PDFs reais com controles defeituosos para demonstrar proteção nominal sensível."""

    def setUp(self):
        """Cria gerador invariante por caso para isolar bytes e estado sem relógio ou rede."""
        self.renderizador = renderizador_pdf.RenderizadorDocumentoCurriculoPdf(
            invariante=True
        )

    def _gerar_e_auditar(self, caso):
        """Gera bytes do DTO e os relê com o auditor comum para exercitar a fronteira real."""
        conteudo = self.renderizador.renderizar(caso.documento)
        return conteudo, auditar_pdf_layout(
            conteudo, esperado=caso.esperado, modelo=caso.documento.modelo
        )

    def _aprovar(self, relatorio):
        """Exige relatório limpo com diagnóstico de caixas para impedir falso verde parcial."""
        self.assertEqual(relatorio.estado, "aprovado", relatorio.resumo())
        self.assertEqual(relatorio.problemas, ())

    def _reprovar(self, relatorio, tipo, *, motivo=None):
        """Exige a categoria deliberada e sua evidência para validar sensibilidade específica."""
        self.assertEqual(relatorio.estado, "reprovado", relatorio.resumo())
        encontrados = [
            p
            for p in relatorio.problemas
            if p.tipo == tipo and (motivo is None or p.motivo == motivo)
        ]
        self.assertTrue(encontrados, relatorio.resumo())
        if tipo in {"fora_area", "sobreposicao"}:
            for problema in encontrados:
                self.assertIsNotNone(problema.pagina)
                self.assertIsNotNone(problema.caixa_a)
                self.assertTrue(problema.marcadores)
        if tipo == "sobreposicao":
            for problema in encontrados:
                self.assertIsNotNone(problema.caixa_b)
                self.assertGreater(problema.profundidade_x, 0.5)
                self.assertGreater(problema.profundidade_y, 0.5)

    def _auditar_controle(self, tipo, variante="padrao", **kwargs):
        """Relê o Canvas sintético pelo mesmo auditor para comparar controles e geração real."""
        controle = criar_pdf_controle_defeituoso(tipo, variante=variante, **kwargs)
        # O controle de instrumento tem x=50: cabe na área compacta aprovada.
        modelo = "compacto" if tipo == "instrumento" else "classico"
        return auditar_pdf_layout(
            controle.conteudo, esperado=controle.esperado, modelo=modelo
        )

    def test_pdf_normal_respeita_area_e_preserva_conteudo(self):
        """P01 aprova a fixture sanitizada nos dois estilos para controlar falsos positivos."""
        for modelo in ("classico", "compacto"):
            with self.subTest(modelo=modelo):
                caso = criar_documento_pdf_layout("P01", modelo=modelo)
                _, relatorio = self._gerar_e_auditar(caso)
                self._aprovar(relatorio)

    def test_quarenta_blocos_preservam_todos_os_detalhes(self):
        """P02 confere cada campo de quarenta blocos em várias páginas para detectar perda parcial."""
        for modelo in ("classico", "compacto"):
            with self.subTest(modelo=modelo):
                caso = criar_documento_pdf_layout("P02", modelo=modelo)
                _, relatorio = self._gerar_e_auditar(caso)
                self._aprovar(relatorio)
                self.assertGreater(len(relatorio.geometria.paginas), 1)

    def test_texto_longo_e_url_sao_preservados(self):
        """P03 recompõe só tokens conhecidos em detalhe e contato para caracterizar quebras longas."""
        for modelo in ("classico", "compacto"):
            for comprimento in (512, 2048):
                for campo in ("D", "C"):
                    with self.subTest(
                        modelo=modelo, comprimento=comprimento, campo=campo
                    ):
                        caso = criar_documento_pdf_layout(
                            "P03",
                            modelo=modelo,
                            comprimento_token=comprimento,
                            campo_token=campo,
                        )
                        tokens = [
                            c.token_sem_quebra
                            for c in caso.esperado
                            if c.token_sem_quebra
                        ]
                        self.assertEqual(len(tokens), 1)
                        self.assertEqual(len(tokens[0]), comprimento)
                        _, relatorio = self._gerar_e_auditar(caso)
                        self._aprovar(relatorio)

    def test_bloco_maior_que_pagina_preserva_linhas(self):
        """P04 audita 120 detalhes de um bloco dividido para preservar texto sem exigir indivisibilidade."""
        for modelo in ("classico", "compacto"):
            with self.subTest(modelo=modelo):
                caso = criar_documento_pdf_layout("P04", modelo=modelo)
                _, relatorio = self._gerar_e_auditar(caso)
                self._aprovar(relatorio)
                self.assertGreater(len(relatorio.geometria.paginas), 1)

    def test_campos_opcionais_e_acentos_sao_caracterizados(self):
        """P05 verifica omissões e conversão cp1252 por literais para não confundir transformação com corte."""
        for modelo in ("classico", "compacto"):
            for subcaso in ("opcionais", "sem_secoes", "caracteres"):
                with self.subTest(modelo=modelo, subcaso=subcaso):
                    caso = criar_documento_pdf_layout(
                        "P05", modelo=modelo, subcaso=subcaso
                    )
                    _, relatorio = self._gerar_e_auditar(caso)
                    self._aprovar(relatorio)
                    self.assertNotIn("None", relatorio.geometria.texto)
                    if subcaso == "caracteres":
                        self.assertIn("Nota ? ok", relatorio.geometria.texto)
                        self.assertIn("Ação <REST> & ç", relatorio.geometria.texto)

    def test_catalogo_pdf_caracteriza_fallback(self):
        """P06 compara oito identificadores sobre o mesmo DTO para caracterizar apenas os dois estilos PDF."""
        modelos = {
            "classico",
            "compacto",
            "ats-simples",
            "criativo",
            "moderno",
            "academico",
            "primeiro-emprego",
        }
        self.assertEqual({m.value for m in ModeloCurriculo}, modelos)
        caso_classico = criar_documento_pdf_layout("P06")
        _, classico = self._gerar_e_auditar(caso_classico)
        self._aprovar(classico)
        for modelo in sorted(modelos | {"padrao_fatec"}):
            with self.subTest(modelo=modelo):
                caso = criar_documento_pdf_layout("P06", modelo=modelo)
                _, relatorio = self._gerar_e_auditar(caso)
                self._aprovar(relatorio)
                if modelo == "compacto":
                    self.assertNotEqual(
                        relatorio.geometria.runs, classico.geometria.runs
                    )
                else:
                    self.assertEqual(relatorio.geometria, classico.geometria)
                tamanhos = {
                    p.tamanho for r in relatorio.geometria.runs for p in r.palavras
                }
                self.assertIn(18 if modelo == "compacto" else 21, tamanhos)
                self.assertIn(9 if modelo == "compacto" else 10.5, tamanhos)

    def test_detector_rejeita_texto_fora_da_area(self):
        """N01 desloca texto extraível para fora dos limites para provar sensibilidade geométrica."""
        self._aprovar(self._auditar_controle("fora_area", "valido"))
        for variante in ("padrao", "mediabox"):
            with self.subTest(variante=variante):
                self._reprovar(
                    self._auditar_controle("fora_area", variante), "fora_area"
                )

    def test_detector_rejeita_sobreposicao(self):
        """N02 sobrepõe textos distintos, inclusive sob CTM, para provar que extração não mascara colisão."""
        self._aprovar(self._auditar_controle("sobreposicao", "valido"))
        for variante in ("padrao", "ctm"):
            with self.subTest(variante=variante):
                relatorio = self._auditar_controle("sobreposicao", variante)
                self._reprovar(relatorio, "sobreposicao")
                pares = [p for p in relatorio.problemas if p.tipo == "sobreposicao"]
                self.assertTrue(
                    any(set(p.marcadores) == {"F000", "F001"} for p in pares)
                )

    def test_detector_rejeita_texto_ausente(self):
        """N03 omite, duplica ou altera um campo conhecido para provar integridade textual integral."""
        self._aprovar(self._auditar_controle("conteudo_ausente", "valido"))
        for variante, motivo in (
            ("padrao", "ausente"),
            ("duplicado", "duplicado"),
            ("diferenca_textual", "diferenca_textual"),
        ):
            with self.subTest(variante=variante):
                self._reprovar(
                    self._auditar_controle("conteudo_ausente", variante),
                    "conteudo_ausente",
                    motivo=motivo,
                )

    def test_detector_valida_transformacoes_e_limites(self):
        """N04 calibra matrizes e fronteiras 0,49/0,51 com Canvas real para qualificar o instrumento."""
        relatorio = self._auditar_controle("instrumento", "valido")
        self._aprovar(relatorio)
        a, b = (r.palavras[0] for r in relatorio.geometria.runs)
        for medido, esperado in zip(a.cantos[0], (112.5, 213.137), strict=True):
            self.assertAlmostEqual(medido, esperado, places=4)
        for medido, esperado in zip(b.cantos[0], (50, 97.516), strict=True):
            self.assertAlmostEqual(medido, esperado, places=4)
        largura = pdfmetrics.stringWidth(a.texto, "Helvetica-Bold", 12) * 1.25
        self.assertAlmostEqual(a.cantos[1][0], 112.5 + largura, places=4)
        self.assertAlmostEqual(a.cantos[2][1], 221.462, places=4)
        self.assertAlmostEqual(a.cantos[3][0], 112.5, places=4)
        fragmentado = self._auditar_controle("instrumento", "ctm")
        self._aprovar(fragmentado)
        fragmento = next(
            p
            for r in fragmentado.geometria.runs
            for p in r.palavras
            if p.texto == "ROLE"
        )
        prefixo = "F000I Ação CONT"
        self.assertAlmostEqual(
            fragmento.caixa[0],
            112.5 + pdfmetrics.stringWidth(prefixo, "Helvetica-Bold", 12) * 1.25,
            places=4,
        )
        self.assertAlmostEqual(fragmento.caixa[1], 213.137, places=4)
        for dx in (0.49, 0.51):
            for dy in (0.49, 0.51):
                with self.subTest(dx=dx, dy=dy):
                    relatorio = self._auditar_controle(
                        "instrumento", "limiar", dx=dx, dy=dy
                    )
                    if dx == dy == 0.51:
                        self._reprovar(relatorio, "sobreposicao")
                    else:
                        self._aprovar(relatorio)
        for eixo in ("dx", "dy"):
            for sinal in (-1, 1):
                for invasao in (0.49, 0.51):
                    with self.subTest(eixo=eixo, sinal=sinal, invasao=invasao):
                        relatorio = self._auditar_controle(
                            "fora_area", "limiar", **{eixo: sinal * invasao}
                        )
                        if invasao == 0.51:
                            self._reprovar(relatorio, "fora_area")
                        else:
                            self._aprovar(relatorio)
        for variante in ("fonte", "rotacao", "clipping"):
            with self.subTest(variante=variante):
                with self.assertRaisesRegex(
                    OraculoPdfNaoSuportado, "oráculo não suporta"
                ):
                    self._auditar_controle("instrumento", variante)

    def test_detector_rejeita_regressao_real_de_margem(self):
        """N05 reduz a margem real por patch de escopo para provar detecção com área esperada fixa."""
        original = renderizador_pdf.ESTILOS_POR_MODELO.copy()
        for modelo, estilo in (
            ("classico", renderizador_pdf.ESTILO_CLASSICO),
            ("compacto", renderizador_pdf.ESTILO_COMPACTO),
        ):
            with self.subTest(modelo=modelo):
                caso = criar_documento_pdf_layout("P01", modelo=modelo)
                bytes_controle, controle = self._gerar_e_auditar(caso)
                self._aprovar(controle)
                with patch.dict(
                    renderizador_pdf.ESTILOS_POR_MODELO,
                    {modelo: replace(estilo, margem_cm=0.5)},
                ):
                    bytes_mutante, mutante = self._gerar_e_auditar(caso)
                self.assertNotEqual(bytes_controle, bytes_mutante)
                self._reprovar(mutante, "fora_area")
                self.assertEqual(renderizador_pdf.ESTILOS_POR_MODELO, original)
                restaurado, relatorio = self._gerar_e_auditar(caso)
                self._aprovar(relatorio)
                self.assertEqual(restaurado, bytes_controle)

    def test_detector_rejeita_leading_reduzido_em_memoria(self):
        """N06 reduz leading em estilos clonados para detectar colisões e verificar restauração sem disco."""
        original = renderizador_pdf._estilos

        def estilos_com_leading_reduzido(estilo):
            """Clona só o corpo a partir da função original para provocar colisão sem mudar produção."""
            estilos = original(estilo)
            estilos["corpo"] = estilos["corpo"].clone("corpo_mutante_teste", leading=1)
            return estilos

        for modelo in ("classico", "compacto"):
            with self.subTest(modelo=modelo):
                caso = criar_documento_pdf_layout("N06", modelo=modelo)
                bytes_controle, controle = self._gerar_e_auditar(caso)
                self._aprovar(controle)
                with patch.object(
                    renderizador_pdf,
                    "_estilos",
                    side_effect=estilos_com_leading_reduzido,
                ):
                    bytes_mutante, mutante = self._gerar_e_auditar(caso)
                self.assertNotEqual(bytes_controle, bytes_mutante)
                self._reprovar(mutante, "sobreposicao")
                self.assertIs(renderizador_pdf._estilos, original)
                restaurado, relatorio = self._gerar_e_auditar(caso)
                self._aprovar(relatorio)
                self.assertEqual(restaurado, bytes_controle)
