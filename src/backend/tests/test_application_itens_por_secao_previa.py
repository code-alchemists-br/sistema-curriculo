"""Testa unitariamente a projeção dos itens da prévia por seção, na ordem padrão."""

import unittest
from dataclasses import replace

from backend.application.previa_versao_curriculo import PreviaVersaoCurriculo
from backend.domain import SecaoCurriculo

# Proveniência: decision-analysis prompts/backend/20261017-160000-itens-por-secao-previa-versao-curriculo-v001.md#v001
from backend.tests.fixtures.curriculo_exportacao import (
    obter_curriculo_exportacao_fixture,
)


def _criar_previa() -> PreviaVersaoCurriculo:
    """Monta uma prévia completa a partir da fixture de exportação.

    A função reúne o estudante, a versão e um item ou mais de cada seção com
    dados determinísticos, sem acessar portas, banco ou relógio. Ela existe para
    que cada teste parta de uma prévia válida e altere só o que importa.
    """
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


class ItensPorSecaoPreviaTestCase(unittest.TestCase):
    """Verifica a projeção dos itens selecionados por seção na ordem padrão.

    Os testes constroem a prévia diretamente e conferem as seções devolvidas por
    ``itens_por_secao``, sem portas ou framework. A classe existe para proteger a
    regra de que só as seções com itens aparecem, na ordem padrão.
    """

    def test_devolve_as_secoes_preenchidas_na_ordem_padrao(self) -> None:
        """Confirma a sequência de seções devolvida para uma prévia completa.

        O teste lê só os identificadores das seções. Ele existe para garantir que
        a ordem siga a ordem padrão e que os dados pessoais não apareçam como
        seção de itens.
        """
        previa = _criar_previa()

        self.assertEqual(
            [secao for secao, _ in previa.itens_por_secao()],
            [
                SecaoCurriculo.FORMACAO_ACADEMICA,
                SecaoCurriculo.EXPERIENCIAS_PROFISSIONAIS,
                SecaoCurriculo.PROJETOS_ACADEMICOS,
                SecaoCurriculo.COMPETENCIAS,
                SecaoCurriculo.IDIOMAS,
            ],
        )

    def test_cada_secao_traz_os_itens_selecionados_da_previa(self) -> None:
        """Confirma que cada seção contém exatamente os itens da prévia.

        O teste compara o conteúdo de cada seção com a tupla correspondente. Ele
        existe para que a projeção não acrescente, omita nem reordene itens.
        """
        previa = _criar_previa()

        self.assertEqual(
            dict(previa.itens_por_secao()),
            {
                SecaoCurriculo.FORMACAO_ACADEMICA: previa.formacoes,
                SecaoCurriculo.EXPERIENCIAS_PROFISSIONAIS: previa.experiencias,
                SecaoCurriculo.PROJETOS_ACADEMICOS: previa.projetos,
                SecaoCurriculo.COMPETENCIAS: previa.competencias,
                SecaoCurriculo.IDIOMAS: previa.idiomas,
            },
        )

    def test_omite_secao_sem_itens_selecionados(self) -> None:
        """Confirma que uma seção sem itens não aparece na projeção.

        O teste esvazia idiomas e projetos e confere que as duas seções somem
        sem alterar a ordem das demais. Ele existe para que o documento final
        não receba títulos de seção vazios.
        """
        previa = replace(_criar_previa(), idiomas=(), projetos=())

        self.assertEqual(
            [secao for secao, _ in previa.itens_por_secao()],
            [
                SecaoCurriculo.FORMACAO_ACADEMICA,
                SecaoCurriculo.EXPERIENCIAS_PROFISSIONAIS,
                SecaoCurriculo.COMPETENCIAS,
            ],
        )

    def test_previa_sem_itens_devolve_projecao_vazia(self) -> None:
        """Confirma que uma prévia sem itens devolve uma tupla vazia.

        O teste esvazia todas as seções de itens. Ele existe para que uma versão
        recém-criada, ainda sem seleção, não produza seção alguma.
        """
        previa = replace(
            _criar_previa(),
            formacoes=(),
            experiencias=(),
            projetos=(),
            competencias=(),
            idiomas=(),
        )

        self.assertEqual(previa.itens_por_secao(), ())
