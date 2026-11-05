"""Testa a política determinística de recomendação de modelos de currículo."""

import unittest

from backend.domain import (
    ModeloCurriculo,
    ObjetivoCurriculo,
    PoliticaRecomendacaoModeloCurriculo,
    RecomendacaoModeloCurriculo,
)

# Proveniência: decision-analysis prompts/backend/20261102-235645-adequacao-semantica-gpt-nano-v003.md#v003


class PoliticaRecomendacaoModeloCurriculoTestCase(unittest.TestCase):
    """Verifica o mapeamento documentado e a explicabilidade da orientação.

    Os cenários exercitam a política pura, sem adaptadores, persistência ou
    relógio. A classe existe para impedir que um objetivo seja mapeado para um
    modelo diferente da tabela aprovada pelo produto.
    """

    def test_recomenda_modelo_documentado_para_cada_objetivo(self) -> None:
        """Reproduz a tabela de objetivo para modelo inicial da documentação.

        O cenário percorre todas as categorias fechadas e verifica o modelo e
        uma justificativa não vazia. Ele existe para manter a recomendação
        determinística, explicável e independente de inteligência artificial.
        """
        politica = PoliticaRecomendacaoModeloCurriculo()
        esperados = {
            ObjetivoCurriculo.PRIMEIRO_EMPREGO: ModeloCurriculo.PRIMEIRO_EMPREGO,
            ObjetivoCurriculo.TECNOLOGIA: ModeloCurriculo.MODERNO,
            ObjetivoCurriculo.ADMINISTRATIVO_CORPORATIVO: ModeloCurriculo.ATS_SIMPLES,
            ObjetivoCurriculo.CRIATIVO_DESIGN: ModeloCurriculo.CRIATIVO,
            ObjetivoCurriculo.ACADEMICO_PESQUISADOR: ModeloCurriculo.ACADEMICO,
            ObjetivoCurriculo.OUTRO: ModeloCurriculo.MODERNO,
        }

        for objetivo, modelo_esperado in esperados.items():
            with self.subTest(objetivo=objetivo.value):
                recomendacao = politica.recomendar(objetivo)

                self.assertEqual(recomendacao.modelo_recomendado, modelo_esperado)
                self.assertTrue(recomendacao.justificativa.strip())

    def test_explicita_profissional_classico_como_alternativa_administrativa(self) -> None:
        """Mantém a alternativa documental na justificativa do caso administrativo.

        O cenário confere que ATS simples permanece a recomendação inicial e
        que a explicação preserva a possibilidade de escolher o clássico. Ele
        existe para orientar sem restringir a autonomia sobre o layout final.
        """
        recomendacao = PoliticaRecomendacaoModeloCurriculo().recomendar(
            ObjetivoCurriculo.ADMINISTRATIVO_CORPORATIVO
        )

        self.assertEqual(recomendacao.modelo_recomendado, ModeloCurriculo.ATS_SIMPLES)
        self.assertIn("Profissional clássico", recomendacao.justificativa)

    def test_recusa_objetivo_ou_resultado_sem_tipo_de_dominio_valido(self) -> None:
        """Protege o vocabulário e a explicação usados pela recomendação.

        O cenário tenta usar texto solto como objetivo e dados vazios no
        resultado. Ele existe para impedir orientação opaca ou valores fora da
        política aprovada de alcançarem a Application.
        """
        politica = PoliticaRecomendacaoModeloCurriculo()

        with self.assertRaises(ValueError):
            politica.recomendar("tecnologia")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            RecomendacaoModeloCurriculo(  # type: ignore[arg-type]
                modelo_recomendado="moderno", justificativa="Recomendado."
            )
        with self.assertRaises(ValueError):
            RecomendacaoModeloCurriculo(
                modelo_recomendado=ModeloCurriculo.MODERNO, justificativa=" "
            )
