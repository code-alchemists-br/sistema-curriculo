"""Testa a política de gravação pura e a reconstrução estrutural de legados.

Usa datas e textos sintéticos para conferir a mesma regra em criação e edição,
sem relógio, ORM, transporte ou recursos externos.
"""

# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
import unittest
from datetime import date, datetime, timedelta, timezone
from uuid import UUID

from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import (
    TAMANHO_MAXIMO_CARGO_EXPERIENCIA,
    TAMANHO_MAXIMO_DESCRICAO_EXPERIENCIA,
    TAMANHO_MAXIMO_EMPRESA_EXPERIENCIA,
    TAMANHO_MINIMO_TEXTO_EXPERIENCIA,
    ExperienciaProfissional,
)
from backend.domain.value_objects import ExperienciaProfissionalId, Periodo, UsuarioId

HOJE = date(2026, 11, 7)
LIMITES = {
    "empresa": TAMANHO_MAXIMO_EMPRESA_EXPERIENCIA,
    "cargo": TAMANHO_MAXIMO_CARGO_EXPERIENCIA,
    "descricao": TAMANHO_MAXIMO_DESCRICAO_EXPERIENCIA,
}


def dados_experiencia(**alteracoes):
    """Monta dados estruturais fixos e substitui os campos do cenário.

    Usa IDs e período determinísticos para comparar fábrica e edição sem gerar
    identidades ou consultar tempo durante os testes de regra de domínio.
    """
    dados = {
        "id": ExperienciaProfissionalId(UUID(int=1)),
        "usuario_id": UsuarioId(UUID(int=2)),
        "empresa": "Empresa Local", "cargo": "Desenvolvedor",
        "descricao": "Desenvolvimento de aplicações.",
        "periodo": Periodo(HOJE - timedelta(days=1), HOJE),
    }
    return {**dados, **alteracoes}


def gravar(modo, **alteracoes):
    """Exercita um caminho público de gravação com hoje explícito e fixo.

    Alterna fábrica e edição de entidade estrutural para exigir a mesma política
    compartilhada sem duplicar sua implementação ou aplicar relógio a legados.
    """
    dados = dados_experiencia(**alteracoes)
    if modo == "criar":
        return ExperienciaProfissional.criar_para_gravacao(**dados, hoje=HOJE)
    original = ExperienciaProfissional(**dados_experiencia())
    return original.editar(
        empresa=dados["empresa"], cargo=dados["cargo"], descricao=dados["descricao"],
        periodo=dados["periodo"], hoje=HOJE,
    )


class GravacaoExperienciaTestCase(unittest.TestCase):
    """Verifica as duas transições e os limites como regras puras de domínio.

    Parametriza datas e textos nos caminhos públicos para detectar divergência
    entre cadastro e edição e proteger a compatibilidade da reconstrução.
    """

    def test_constantes_especificas_refletem_limites_aprovados(self):
        """Compara as constantes com os valores aprovados para evitar deriva.

        Confere números explícitos sem depender da implementação da política,
        protegendo o contrato de 1–200, 1–200 e 1–5.000 caracteres.
        """
        self.assertEqual(TAMANHO_MINIMO_TEXTO_EXPERIENCIA, 1)
        self.assertEqual(LIMITES, {"empresa": 200, "cargo": 200, "descricao": 5000})

    def test_ontem_hoje_e_amanha_em_ambas_as_datas(self):
        """Exercita ontem, hoje e amanhã em início e fim nas duas transições.

        Mantém cronologia válida ao variar uma data e verifica rejeição somente
        do futuro para impedir tolerância indevida e inclusão de relógio real.
        """
        for modo in ("criar", "editar"):
            for campo in ("inicio", "fim"):
                for deslocamento in (-1, 0, 1):
                    with self.subTest(modo=modo, campo=campo, dias=deslocamento):
                        data = HOJE + timedelta(days=deslocamento)
                        periodo = Periodo(data, None) if campo == "inicio" else Periodo(HOJE - timedelta(days=2), data)
                        if deslocamento > 0:
                            with self.assertRaises(RegraDeDominioViolada):
                                gravar(modo, periodo=periodo)
                        else:
                            self.assertEqual(gravar(modo, periodo=periodo).periodo, periodo)

    def test_termino_nulo_datas_iguais_e_cronologia_preservada(self):
        """Confere término nulo e datas iguais usando Periodo sem regra global nova.

        Verifica a cronologia já existente e a aceitação no dia atual para
        preservar a representação de experiência em andamento e períodos curtos.
        """
        for modo in ("criar", "editar"):
            for periodo in (Periodo(HOJE), Periodo(HOJE, HOJE)):
                with self.subTest(modo=modo, periodo=periodo):
                    self.assertEqual(gravar(modo, periodo=periodo).periodo, periodo)
        with self.assertRaises(RegraDeDominioViolada):
            Periodo(HOJE, HOJE - timedelta(days=1))

    def test_textos_no_minimo_e_maximo_sao_normalizados_sem_truncamento(self):
        """Confere limites inclusivos após strip nos três campos e dois caminhos.

        Usa Unicode com mais bytes que caracteres e espaços externos para
        garantir medição por len e retorno do texto normalizado integralmente.
        """
        for modo in ("criar", "editar"):
            for campo, maximo in LIMITES.items():
                for tamanho in (1, maximo):
                    with self.subTest(modo=modo, campo=campo, tamanho=tamanho):
                        texto = "é" * tamanho
                        resultado = gravar(modo, **{campo: f" \t{texto}\n "})
                        self.assertEqual(getattr(resultado, campo), texto)

    def test_textos_vazios_brancos_e_maximo_mais_um_sao_rejeitados(self):
        """Recusa valores vazios ou acima do máximo nos dois caminhos de gravação.

        Testa cada campo separadamente, inclusive espaços periféricos em excesso,
        para garantir que a política rejeite em vez de truncar os valores.
        """
        for modo in ("criar", "editar"):
            for campo, maximo in LIMITES.items():
                for texto in ("", " \t\n ", "a" * (maximo + 1), " " + "a" * (maximo + 1) + " "):
                    with self.subTest(modo=modo, campo=campo, tamanho=len(texto)):
                        with self.assertRaises(RegraDeDominioViolada):
                            gravar(modo, **{campo: texto})

    def test_unicode_composto_e_descricao_multilinha_preservam_conteudo_interno(self):
        """Mede pontos de código e preserva espaços internos, linhas e emoji.

        Exercita composição Unicode no limite e além dele para documentar len,
        mantendo a descrição multilinha sem normalização interna ou truncamento.
        """
        descricao = "Primeira  linha\nSegunda\tlinha 👩🏽‍💻"
        for modo in ("criar", "editar"):
            resultado = gravar(modo, empresa=" " + "e\u0301" * 100 + " ", descricao="\n" + descricao + "\n")
            self.assertEqual(len(resultado.empresa), 200)
            self.assertEqual(resultado.descricao, descricao)
            with self.assertRaises(RegraDeDominioViolada):
                gravar(modo, cargo="e\u0301" * 101)

    def test_reconstrucao_estrutural_preserva_legados_e_permite_correcao(self):
        """Reconstrói legado com textos longos e datas futuras sem política nova.

        Confere preservação literal, exclusão e posterior edição válida para
        impedir que a compatibilidade de leitura dependa dos limites atuais.
        """
        dados = dados_experiencia(
            empresa=" " + "e" * 201 + " ", cargo="c" * 201,
            descricao="d" * 5001, periodo=Periodo(date(2100, 1, 1), date(2101, 1, 1)),
        )
        legado = ExperienciaProfissional(**dados)
        self.assertEqual(legado.empresa, dados["empresa"])
        self.assertEqual(legado.periodo, dados["periodo"])
        excluida = legado.excluir(datetime(2026, 11, 7, tzinfo=timezone.utc))
        self.assertEqual(excluida.descricao, dados["descricao"])
        corrigida = legado.editar(
            empresa=" Empresa ", cargo=" Cargo ", descricao=" Descrição ",
            periodo=Periodo(HOJE), hoje=HOJE,
        )
        self.assertEqual((corrigida.empresa, corrigida.cargo, corrigida.descricao), ("Empresa", "Cargo", "Descrição"))
        self.assertEqual((corrigida.id, corrigida.usuario_id), (legado.id, legado.usuario_id))
        self.assertEqual(legado.descricao, dados["descricao"])

    def test_edicao_invalida_nao_muta_parcialmente_entidade(self):
        """Falha na edição imutável e compara todos os atributos da entidade.

        Propõe textos válidos e uma data futura, verificando após a exceção que
        nenhuma parte da versão anterior foi alterada antes da validação total.
        """
        original = ExperienciaProfissional(**dados_experiencia())
        estado = dados_experiencia()
        with self.assertRaises(RegraDeDominioViolada):
            original.editar(
                empresa=" Nova Empresa ", cargo="Novo Cargo", descricao="Nova descrição",
                periodo=Periodo(HOJE + timedelta(days=1)), hoje=HOJE,
            )
        for campo, valor in estado.items():
            self.assertEqual(getattr(original, campo), valor)
