"""Testa a proposta tipada e revisável de recomendação de modelo."""

import unittest

from backend.domain import ModeloCurriculo, RecomendacaoModeloCurriculo

# Proveniência: decision-analysis prompts/backend/20261105-181751-adequacao-semantica-gpt-nano-v005.md#v005


class RecomendacaoModeloCurriculoTestCase(unittest.TestCase):
    """Verifica os invariantes da sugestão de modelo sem gerador externo.

    Os cenários constroem somente o value object e rejeitam valores fora do
    catálogo ou sem justificativa. A classe existe para impedir que a IA
    atravesse a fronteira interna com uma recomendação opaca ou inválida.
    """

    def test_aceita_modelo_do_catalogo_com_justificativa(self) -> None:
        """Mantém proposta válida como orientação não vinculante.

        O cenário instancia modelo reconhecido e explicação não vazia. Ele
        existe para garantir que a saída tipada preserve a sugestão revisável.
        """
        recomendacao = RecomendacaoModeloCurriculo(
            ModeloCurriculo.MODERNO, "Valoriza projetos e competências selecionados."
        )

        self.assertEqual(recomendacao.modelo_recomendado, ModeloCurriculo.MODERNO)

    def test_recusa_modelo_ou_justificativa_invalidos(self) -> None:
        """Bloqueia resposta externa sem catálogo ou explicação legível.

        O cenário tenta criar propostas com texto solto e explicação vazia. Ele
        existe para garantir que o adaptador futuro tenha resultado verificável.
        """
        with self.assertRaises(ValueError):
            RecomendacaoModeloCurriculo("moderno", "Orientação.")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            RecomendacaoModeloCurriculo(ModeloCurriculo.MODERNO, " ")
