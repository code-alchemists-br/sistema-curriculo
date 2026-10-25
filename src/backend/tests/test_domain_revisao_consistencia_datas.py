"""Testa a regra de consistência de datas de formação e experiência na revisão."""

import unittest
from dataclasses import replace
from datetime import date, timedelta

# Proveniência: decision-analysis prompts/backend/20261023-190000-consistencia-datas-revisao-v001.md#v001
from backend.domain import (
    Periodo,
    SecaoRevisao,
    SeveridadePendencia,
    StatusFormacaoAcademica,
    revisar_curriculo,
)
from backend.tests.fixtures.curriculo_exportacao import (
    CurriculoExportacaoFixture,
    obter_curriculo_exportacao_fixture,
)

HOJE = date(2026, 10, 23)
UM_DIA = timedelta(days=1)
INICIO_PASSADO = date(2020, 1, 1)


def _formacao(fixture: CurriculoExportacaoFixture, status, fim: date | None):
    """Cria uma formação a partir da fixture com situação e término informados.

    A função copia a formação da fixture trocando a situação e o período, sem
    alterar a fixture compartilhada. Ela existe para que cada teste controle só a
    situação e o término da formação.
    """
    return replace(
        fixture.formacao_academica,
        status=status,
        periodo=Periodo(inicio=INICIO_PASSADO, fim=fim),
    )


def _experiencia(fixture: CurriculoExportacaoFixture, inicio: date, fim: date | None = None):
    """Cria uma experiência a partir da fixture com início e término informados.

    A função copia a experiência da fixture trocando o período, sem alterar a
    fixture compartilhada. Ela existe para que cada teste controle só as datas da
    experiência.
    """
    return replace(
        fixture.experiencia_profissional, periodo=Periodo(inicio=inicio, fim=fim)
    )


def _revisar(fixture: CurriculoExportacaoFixture, formacoes, experiencias):
    """Revisa um currículo completo da fixture com as formações e experiências dadas.

    A função mantém contato (com cidade), projetos, competências e idiomas
    completos para que só a regra de datas possa gerar pendências. Ela existe para
    isolar a regra testada.
    """
    contato = replace(fixture.usuario.dados_contato, cidade="São Paulo")
    return revisar_curriculo(
        usuario=replace(fixture.usuario, dados_contato=contato),
        formacoes=tuple(formacoes),
        experiencias=tuple(experiencias),
        projetos=(fixture.projeto_academico,),
        competencias=fixture.competencias,
        idiomas=fixture.idiomas,
        hoje=HOJE,
    )


class ConsistenciaDeDatasTestCase(unittest.TestCase):
    """Verifica a regra de consistência de datas da revisão do currículo.

    Os testes variam situação e datas de formações e experiências em torno de
    ``HOJE`` e observam as pendências, sem banco, rede ou relógio do sistema. A
    classe existe para proteger os limites da regra, inclusive a tolerância de um
    dia para o fuso horário.
    """

    def setUp(self) -> None:
        """Obtém a fixture de exportação usada como ponto de partida.

        O método cria a fixture determinística antes de cada teste. Ele existe
        para que os testes não compartilhem estado entre si.
        """
        self.fixture = obter_curriculo_exportacao_fixture()
        # A formação da fixture termina em 2025 e estaria "atrasada" em HOJE; esta,
        # em andamento e sem término, é neutra para a regra de datas.
        self.formacao_neutra = _formacao(
            self.fixture, StatusFormacaoAcademica.EM_ANDAMENTO, None
        )

    def _codigos(self, formacoes, experiencias) -> list[str]:
        """Devolve os códigos das pendências da revisão dos itens informados.

        O método revisa e extrai só os códigos. Ele existe para que os testes
        comparem de forma curta o que a regra apontou.
        """
        return [p.codigo for p in _revisar(self.fixture, formacoes, experiencias).pendencias]

    def test_datas_coerentes_nao_geram_pendencia(self) -> None:
        """Confirma que um currículo com datas coerentes não recebe pendência.

        O teste usa formação em andamento sem término, formação concluída no
        passado e experiência atual. Ele existe para proteger o caso feliz.
        """
        formacoes = (
            _formacao(self.fixture, StatusFormacaoAcademica.EM_ANDAMENTO, None),
            _formacao(self.fixture, StatusFormacaoAcademica.CONCLUIDO, date(2024, 12, 1)),
        )

        self.assertEqual(
            self._codigos(formacoes, (_experiencia(self.fixture, date(2025, 1, 1)),)), []
        )

    def test_formacao_concluida_com_fim_no_futuro_gera_erro(self) -> None:
        """Confirma o erro para formação concluída que termina depois de hoje.

        O teste usa um término dois dias à frente e confere código, seção,
        severidade e a reprovação. Ele existe porque não se conclui no futuro.
        """
        formacao = _formacao(
            self.fixture, StatusFormacaoAcademica.CONCLUIDO, HOJE + 2 * UM_DIA
        )

        resultado = _revisar(self.fixture, (formacao,), (self.fixture.experiencia_profissional,))

        self.assertEqual(
            [(p.codigo, p.secao, p.severidade) for p in resultado.pendencias],
            [
                (
                    "FORMACAO_CONCLUIDA_COM_FIM_FUTURO",
                    SecaoRevisao.FORMACAO_ACADEMICA,
                    SeveridadePendencia.ERRO,
                )
            ],
        )
        self.assertFalse(resultado.aprovado)

    def test_formacao_em_andamento_com_fim_passado_gera_aviso(self) -> None:
        """Confirma o aviso para formação em andamento cujo término já passou.

        O teste usa um término dois dias atrás e confere o aviso e a aprovação.
        Ele existe para sugerir a atualização da situação sem reprovar.
        """
        formacao = _formacao(
            self.fixture, StatusFormacaoAcademica.EM_ANDAMENTO, HOJE - 2 * UM_DIA
        )

        resultado = _revisar(self.fixture, (formacao,), (self.fixture.experiencia_profissional,))

        self.assertEqual(
            [(p.codigo, p.severidade) for p in resultado.pendencias],
            [("FORMACAO_EM_ANDAMENTO_COM_FIM_PASSADO", SeveridadePendencia.AVISO)],
        )
        self.assertTrue(resultado.aprovado)

    def test_experiencia_que_comeca_no_futuro_gera_erro(self) -> None:
        """Confirma o erro para experiência cujo início é depois de hoje.

        O teste usa um início dois dias à frente. Ele existe porque ninguém
        trabalhou em um período que ainda não começou.
        """
        experiencia = _experiencia(self.fixture, HOJE + 2 * UM_DIA)

        resultado = _revisar(self.fixture, (self.formacao_neutra,), (experiencia,))

        self.assertEqual(
            [(p.codigo, p.secao, p.severidade) for p in resultado.pendencias],
            [
                (
                    "EXPERIENCIA_INICIO_FUTURO",
                    SecaoRevisao.EXPERIENCIAS_PROFISSIONAIS,
                    SeveridadePendencia.ERRO,
                )
            ],
        )
        self.assertFalse(resultado.aprovado)

    def test_limites_respeitam_a_tolerancia_de_um_dia_de_fuso(self) -> None:
        """Confirma que um dia de diferença não gera pendência, mas dois geram.

        O teste usa os limites exatos de ontem e de amanhã para cada regra. Ele
        existe para que a diferença de fuso horário não produza falso alarme à
        noite, e para fixar onde a regra passa a valer.
        """
        concluida = StatusFormacaoAcademica.CONCLUIDO
        andamento = StatusFormacaoAcademica.EM_ANDAMENTO
        casos = (
            ("concluída termina amanhã", _formacao(self.fixture, concluida, HOJE + UM_DIA), None, []),
            ("concluída termina em 2 dias", _formacao(self.fixture, concluida, HOJE + 2 * UM_DIA), None, ["FORMACAO_CONCLUIDA_COM_FIM_FUTURO"]),
            ("andamento terminou ontem", _formacao(self.fixture, andamento, HOJE - UM_DIA), None, []),
            ("andamento terminou há 2 dias", _formacao(self.fixture, andamento, HOJE - 2 * UM_DIA), None, ["FORMACAO_EM_ANDAMENTO_COM_FIM_PASSADO"]),
            ("experiência começa amanhã", None, _experiencia(self.fixture, HOJE + UM_DIA), []),
            ("experiência começa em 2 dias", None, _experiencia(self.fixture, HOJE + 2 * UM_DIA), ["EXPERIENCIA_INICIO_FUTURO"]),
        )
        for descricao, formacao, experiencia, esperado in casos:
            with self.subTest(caso=descricao):
                formacoes = (formacao or self.formacao_neutra,)
                experiencias = (experiencia or self.fixture.experiencia_profissional,)

                self.assertEqual(self._codigos(formacoes, experiencias), esperado)

    def test_situacoes_sem_regra_de_data_nao_geram_pendencia(self) -> None:
        """Confirma que formação interrompida e términos previstos não são apontados.

        O teste usa formação interrompida com término no passado e no futuro, e
        formação em andamento com término previsto à frente. Ele existe porque
        esses casos são legítimos.
        """
        formacoes = (
            _formacao(self.fixture, StatusFormacaoAcademica.INTERROMPIDO, HOJE - 100 * UM_DIA),
            _formacao(self.fixture, StatusFormacaoAcademica.INTERROMPIDO, HOJE + 100 * UM_DIA),
            _formacao(self.fixture, StatusFormacaoAcademica.EM_ANDAMENTO, HOJE + 100 * UM_DIA),
        )
        experiencias = (_experiencia(self.fixture, date(2025, 1, 1), HOJE + 100 * UM_DIA),)

        self.assertEqual(self._codigos(formacoes, experiencias), [])

    def test_varios_itens_com_o_mesmo_problema_geram_uma_so_pendencia(self) -> None:
        """Confirma que o mesmo problema em vários itens vira uma única pendência.

        O teste usa duas formações concluídas no futuro e duas experiências no
        futuro. Ele existe para manter um código por tipo de problema.
        """
        futuro = HOJE + 10 * UM_DIA
        formacoes = (
            _formacao(self.fixture, StatusFormacaoAcademica.CONCLUIDO, futuro),
            _formacao(self.fixture, StatusFormacaoAcademica.CONCLUIDO, futuro + UM_DIA),
        )
        experiencias = (_experiencia(self.fixture, futuro), _experiencia(self.fixture, futuro))

        self.assertEqual(
            self._codigos(formacoes, experiencias),
            ["FORMACAO_CONCLUIDA_COM_FIM_FUTURO", "EXPERIENCIA_INICIO_FUTURO"],
        )

    def test_erros_vem_antes_dos_avisos_na_ordem_das_secoes(self) -> None:
        """Confirma a ordem quando erros e aviso de datas aparecem juntos.

        O teste combina formação concluída no futuro, formação em andamento com
        término passado e experiência no futuro. Ele existe para provar a ordem
        por severidade e seção.
        """
        formacoes = (
            _formacao(self.fixture, StatusFormacaoAcademica.CONCLUIDO, HOJE + 10 * UM_DIA),
            _formacao(self.fixture, StatusFormacaoAcademica.EM_ANDAMENTO, HOJE - 10 * UM_DIA),
        )
        experiencias = (_experiencia(self.fixture, HOJE + 10 * UM_DIA),)

        self.assertEqual(
            self._codigos(formacoes, experiencias),
            [
                "FORMACAO_CONCLUIDA_COM_FIM_FUTURO",
                "EXPERIENCIA_INICIO_FUTURO",
                "FORMACAO_EM_ANDAMENTO_COM_FIM_PASSADO",
            ],
        )
