"""Testa unitariamente a regra de revisão de campos obrigatórios do currículo."""

import unittest
from dataclasses import replace

from backend.domain import (
    PendenciaRevisao,
    ResultadoRevisao,
    SecaoRevisao,
    SeveridadePendencia,
    revisar_curriculo,
)
from backend.tests.fixtures.curriculo_exportacao import (
    CurriculoExportacaoFixture,
    obter_curriculo_exportacao_fixture,
)

# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001


def _revisar(
    fixture: CurriculoExportacaoFixture,
    *,
    sem_contato: bool = False,
    sem_formacao: bool = False,
    sem_experiencia: bool = False,
    sem_projeto: bool = False,
    sem_competencia: bool = False,
    sem_idioma: bool = False,
) -> ResultadoRevisao:
    """Revisa o currículo da fixture, removendo as partes indicadas.

    A função parte do currículo completo da fixture e esvazia somente as seções
    pedidas, ou remove o contato do estudante, antes de chamar a regra. Ela
    existe para que cada teste provoque uma pendência específica sem repetir a
    montagem dos dados.
    """
    usuario = replace(fixture.usuario, dados_contato=None) if sem_contato else fixture.usuario
    return revisar_curriculo(
        usuario=usuario,
        formacoes=() if sem_formacao else (fixture.formacao_academica,),
        experiencias=() if sem_experiencia else (fixture.experiencia_profissional,),
        projetos=() if sem_projeto else (fixture.projeto_academico,),
        competencias=() if sem_competencia else fixture.competencias,
        idiomas=() if sem_idioma else fixture.idiomas,
    )


class RevisarCurriculoTestCase(unittest.TestCase):
    """Verifica a regra ``revisar_curriculo`` sobre o currículo da fixture.

    A classe usa o currículo completo da fixture e remove partes para observar
    cada pendência, a severidade, o veredito e a ordem. Ela existe para proteger
    a regra do que falta num currículo sem banco, rede ou framework.
    """

    def test_curriculo_completo_e_aprovado_sem_pendencias(self) -> None:
        """Confirma que um currículo completo não gera nenhuma pendência.

        O teste revisa a fixture inteira e observa a lista vazia e a aprovação.
        Ele existe para proteger o caso feliz da regra.
        """
        resultado = _revisar(obter_curriculo_exportacao_fixture())

        self.assertEqual(resultado.pendencias, ())
        self.assertTrue(resultado.aprovado)

    def test_contato_ausente_gera_erro_nos_dados_pessoais(self) -> None:
        """Confirma a pendência de contato quando o estudante não tem endereço e telefone.

        O teste remove os dados de contato e compara a única pendência com o
        esperado, além do veredito. Ele existe para proteger a regra de
        identificação.
        """
        resultado = _revisar(obter_curriculo_exportacao_fixture(), sem_contato=True)

        self.assertEqual(
            resultado.pendencias,
            (
                PendenciaRevisao(
                    codigo="CONTATO_AUSENTE",
                    secao=SecaoRevisao.DADOS_PESSOAIS,
                    mensagem="Informe o endereço e ao menos um telefone de contato.",
                    severidade=SeveridadePendencia.ERRO,
                ),
            ),
        )
        self.assertFalse(resultado.aprovado)

    def test_secao_obrigatoria_vazia_gera_um_erro_com_o_codigo_da_secao(self) -> None:
        """Confirma que formação, experiência e competência vazias geram erro.

        O teste esvazia cada seção obrigatória por vez e observa uma única
        pendência de erro, com o código e a seção esperados, e a reprovação. Ele
        existe para proteger as três seções obrigatórias.
        """
        casos = (
            ("sem_formacao", "FORMACAO_AUSENTE", SecaoRevisao.FORMACAO_ACADEMICA),
            ("sem_experiencia", "EXPERIENCIA_AUSENTE", SecaoRevisao.EXPERIENCIAS_PROFISSIONAIS),
            ("sem_competencia", "COMPETENCIA_AUSENTE", SecaoRevisao.COMPETENCIAS),
        )
        for ajuste, codigo, secao in casos:
            with self.subTest(ajuste=ajuste):
                resultado = _revisar(obter_curriculo_exportacao_fixture(), **{ajuste: True})

                self.assertEqual(
                    [(p.codigo, p.secao, p.severidade) for p in resultado.pendencias],
                    [(codigo, secao, SeveridadePendencia.ERRO)],
                )
                self.assertFalse(resultado.aprovado)

    def test_secao_opcional_vazia_gera_aviso_e_nao_reprova(self) -> None:
        """Confirma que projetos e idiomas vazios só recomendam, sem reprovar.

        O teste esvazia as duas seções opcionais e observa os dois avisos, em
        ordem de seção, e a aprovação. Ele existe para proteger a diferença entre
        erro e aviso.
        """
        resultado = _revisar(obter_curriculo_exportacao_fixture(), sem_projeto=True, sem_idioma=True)

        self.assertEqual(
            [(p.codigo, p.severidade) for p in resultado.pendencias],
            [
                ("PROJETO_AUSENTE", SeveridadePendencia.AVISO),
                ("IDIOMA_AUSENTE", SeveridadePendencia.AVISO),
            ],
        )
        self.assertTrue(resultado.aprovado)

    def test_ordena_erros_antes_de_avisos_e_pela_ordem_das_secoes(self) -> None:
        """Confirma a ordem das pendências quando tudo está faltando.

        O teste remove todas as partes e compara a sequência de códigos: erros
        primeiro, na ordem das seções, e depois os avisos. Ele existe para
        proteger o determinismo do resultado.
        """
        resultado = _revisar(
            obter_curriculo_exportacao_fixture(),
            sem_contato=True,
            sem_formacao=True,
            sem_experiencia=True,
            sem_projeto=True,
            sem_competencia=True,
            sem_idioma=True,
        )

        self.assertEqual(
            [pendencia.codigo for pendencia in resultado.pendencias],
            [
                "CONTATO_AUSENTE",
                "FORMACAO_AUSENTE",
                "EXPERIENCIA_AUSENTE",
                "COMPETENCIA_AUSENTE",
                "PROJETO_AUSENTE",
                "IDIOMA_AUSENTE",
            ],
        )

    def test_identificadores_de_secao_seguem_o_contrato_do_front_end(self) -> None:
        """Confirma os textos das seções, que o front-end já usa na validação.

        O teste compara o conjunto de valores com o esperado. Ele existe para que
        uma troca de texto não quebre o contrato com a interface.
        """
        self.assertEqual(
            {secao.value for secao in SecaoRevisao},
            {
                "dados-pessoais",
                "formacao-academica",
                "experiencias-profissionais",
                "competencias",
                "projetos-academicos",
                "idiomas",
            },
        )