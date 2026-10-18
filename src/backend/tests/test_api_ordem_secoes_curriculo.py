"""Protege o contrato HTTP mínimo da atualização da ordem das seções."""

import unittest

from backend.api.factory import create_app


CAMINHO = "/estudantes/{usuario_id}/curriculos/{curriculo_id}/ordem-secoes"
NOME_REQUISICAO = "AtualizarOrdemSecoesCurriculoRequisicao"


class OrdemSecoesCurriculoContratoTestCase(unittest.TestCase):
    """Confere o endpoint e o schema público de reordenação de seções.

    A classe gera o OpenAPI da fábrica sem iniciar servidor ou banco e compara
    somente elementos estáveis do contrato. Ela existe para evitar que o corpo
    mínimo da operação ganhe campos acidentalmente.
    """

    def test_atualizacao_expoe_put_sem_corpo_de_resposta(self) -> None:
        """Confirma caminho, método, status e referência ao payload mínimo.

        O teste lê a operação gerada pela aplicação e exige o status 204 e o
        schema próprio de requisição. Ele existe para manter explícita a
        atualização sem resposta e separada da edição completa da versão.
        """
        operacao = create_app().openapi()["paths"][CAMINHO]["put"]

        self.assertIn("204", operacao["responses"])
        self.assertEqual(
            operacao["requestBody"]["content"]["application/json"]["schema"]["$ref"],
            f"#/components/schemas/{NOME_REQUISICAO}",
        )

    def test_payload_contem_exclusivamente_a_ordem_com_todas_as_secoes_validas(self) -> None:
        """Confirma que o payload obrigatório tem somente a lista de seções.

        O teste verifica o schema de requisição, incluindo enumeração, tamanho
        mínimo e recusa de propriedades extras. Ele existe para impedir que a
        reordenação passe a exigir ou aceitar dados alheios à sua intenção.
        """
        schema = create_app().openapi()["components"]["schemas"][NOME_REQUISICAO]

        self.assertEqual(schema["required"], ["ordem_secoes"])
        self.assertEqual(set(schema["properties"]), {"ordem_secoes"})
        self.assertFalse(schema["additionalProperties"])
        ordem_secoes = schema["properties"]["ordem_secoes"]
        self.assertEqual((ordem_secoes["minItems"], ordem_secoes["maxItems"]), (7, 7))
        itens = ordem_secoes["items"]
        self.assertEqual(
            itens["$ref"], "#/components/schemas/SecaoCurriculo"
        )
        self.assertEqual(
            set(create_app().openapi()["components"]["schemas"]["SecaoCurriculo"]["enum"]),
            {
                "dados-pessoais",
                "formacao-academica",
                "experiencias-profissionais",
                "projetos-academicos",
                "competencias",
                "idiomas",
                "documentos-complementares",
            },
        )


if __name__ == "__main__":
    unittest.main()
