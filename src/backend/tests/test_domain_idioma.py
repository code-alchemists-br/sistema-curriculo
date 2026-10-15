"""Testa invariantes e normalização da entidade de idioma."""

import unittest
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
from backend.domain import (
    Idioma,
    IdiomaId,
    RegraDeDominioViolada,
    UsuarioId,
    normalizar_idioma,
)


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class IdiomaTestCase(unittest.TestCase):
    """Verifica a validade e a chave lógica de idiomas em memória.

    A suíte constrói entidades apenas com value objects e compara a política de
    normalização, sem acessar framework ou recursos externos. Ela existe para
    proteger as invariantes que antecedem o cadastro e a deduplicação.
    """

    def test_apara_idioma_e_expoe_chave_sem_caixa_ou_espacos(self) -> None:
        """Produz chave igual para variações de caixa e espaços entre termos.

        O cenário constrói um idioma com contorno e múltiplos espaços internos e
        compara a chave com a forma canônica esperada. Ele existe para garantir a
        política de duplicidade aprovada antes que a Application consulte a porta.
        """
        idioma = self._criar_idioma(idioma="  Inglês\t  Instrumental  ")

        self.assertEqual(idioma.idioma, "Inglês\t  Instrumental")
        self.assertEqual(idioma.idioma_normalizado, "inglês instrumental")

    def test_rejeita_idioma_sem_termos_apos_normalizacao(self) -> None:
        """Impede entidade sem idioma mesmo quando recebe somente espaços.

        O cenário entrega espaços, tabulação e quebra de linha à entidade e
        exige a falha de domínio. Ele existe para impedir que uma chave vazia
        alcance o caso de uso ou a persistência.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_idioma(idioma=" \t\n ")

    def test_rejeita_idioma_nao_textual(self) -> None:
        """Impede que tipos não textuais sejam fornecidos como idioma.

        O cenário ignora tipagem estática e passa um número para verificar a
        defesa em tempo de execução da normalização. Ele existe para manter a
        consistência do domínio contra dados corrompidos.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_idioma(idioma=123)  # type: ignore[arg-type]

    def test_rejeita_nivel_vazio(self) -> None:
        """Impede idioma cujo nível não possui texto significativo.

        O cenário fornece nível composto apenas por espaços e exige a invariante
        de domínio. Ele existe para assegurar que todo idioma criado possa
        informar sua proficiência ao currículo.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_idioma(nivel="   ")

    def test_normalizar_idioma_diretamente(self) -> None:
        """Valida o comportamento isolado da função pura de normalização.

        O cenário invoca a função utilitária com termos espaçados em caixa alta e
        compara com a forma canônica colapsada em minúsculas. Ele existe para
        garantir que outras camadas possam obter a mesma chave sem instanciar a
        entidade completa.
        """
        resultado = normalizar_idioma("  FRANCÊS   AVANÇADO  ")
        self.assertEqual(resultado, "francês avançado")

    def _criar_idioma(
        self,
        idioma: str = "Inglês",
        nivel: str = "Intermediário",
    ) -> Idioma:
        """Constrói idioma com identidades determinísticas para os testes.

        O auxiliar fornece dados válidos por padrão e permite variar uma regra
        de cada vez. Ele existe para deixar os cenários focados na invariante ou
        normalização que desejam observar.
        """
        return Idioma(
            id=IdiomaId(UUID("60000000-0000-0000-0000-000000000001")),
            usuario_id=UsuarioId(UUID("60000000-0000-0000-0000-000000000002")),
            idioma=idioma,
            nivel=nivel,
        )
