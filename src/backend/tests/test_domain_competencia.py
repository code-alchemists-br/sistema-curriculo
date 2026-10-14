"""Testa invariantes e normalização da entidade de competência."""

import unittest
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
from backend.domain import (
    CategoriaCompetencia,
    Competencia,
    CompetenciaId,
    RegraDeDominioViolada,
    UsuarioId,
)


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class CompetenciaTestCase(unittest.TestCase):
    """Verifica a validade e a chave lógica de competências em memória.

    A suíte constrói entidades apenas com value objects e compara a política de
    normalização, sem acessar framework ou recursos externos. Ela existe para
    proteger as invariantes que antecedem o cadastro e a deduplicação.
    """

    def test_apara_descricao_e_expoe_chave_sem_caixa_ou_espacos(self) -> None:
        """Produz chave igual para variações de caixa e espaços entre termos.

        O cenário constrói uma competência com contorno e tabulação e compara a
        chave com a forma canônica esperada. Ele existe para garantir a política
        de duplicidade aprovada antes que a Application consulte a porta.
        """
        competencia = self._criar_competencia(descricao="  Power\t  BI  ")

        self.assertEqual(competencia.descricao, "Power\t  BI")
        self.assertEqual(competencia.descricao_normalizada, "power bi")

    def test_rejeita_descricao_sem_termos_apos_normalizacao(self) -> None:
        """Impede entidade sem descrição mesmo quando recebe somente espaços.

        O cenário entrega espaços, tabulação e quebra de linha à entidade e
        exige a falha de domínio. Ele existe para impedir que uma chave vazia
        alcance o caso de uso ou a persistência.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_competencia(descricao=" \t\n ")

    def test_rejeita_nivel_vazio(self) -> None:
        """Impede competência cujo nível não possui texto significativo.

        O cenário fornece nível composto apenas por espaços e exige a invariante
        de domínio. Ele existe para assegurar que toda competência criada possa
        informar sua proficiência ao currículo.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_competencia(nivel="  ")

    def test_rejeita_categoria_fora_do_vocabulario(self) -> None:
        """Impede que texto arbitrário seja usado como categoria da competência.

        O cenário ignora a tipagem estática e fornece uma string para verificar
        a defesa de execução da entidade. Ele existe para manter o vocabulário
        de categorias íntegro mesmo fora de uma fronteira validada.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_competencia(categoria="outra")  # type: ignore[arg-type]

    def _criar_competencia(
        self,
        descricao: str = "Python",
        nivel: str = "Avançado",
        categoria: CategoriaCompetencia = CategoriaCompetencia.TECNICA,
    ) -> Competencia:
        """Constrói competência com identidades determinísticas para os testes.

        O auxiliar fornece dados válidos por padrão e permite variar uma regra
        de cada vez. Ele existe para deixar os cenários focados na invariante ou
        normalização que desejam observar.
        """
        return Competencia(
            id=CompetenciaId(UUID("50000000-0000-0000-0000-000000000001")),
            usuario_id=UsuarioId(UUID("50000000-0000-0000-0000-000000000002")),
            categoria=categoria,
            descricao=descricao,
            nivel=nivel,
        )
