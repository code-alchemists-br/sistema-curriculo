"""Protege o adapter de geração de identidade de currículo, sem recursos externos."""

import unittest
from unittest.mock import patch
from uuid import UUID

from backend.domain import CurriculoId
from backend.infrastructure.identificadores.geradores import GeradorCurriculoIdUuid4

# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001

GERADOR = "backend.infrastructure.identificadores.geradores"
PRIMEIRO = UUID("00000000-0000-4000-8000-000000000001")
SEGUNDO = UUID("00000000-0000-4000-8000-000000000002")


class GeradorCurriculoIdUuid4TestCase(unittest.TestCase):
    """Verifica a tradução do gerador de UUID para ``CurriculoId``.

    A classe substitui o gerador de UUID por valores fixos para observar a
    delegação, e confere uma propriedade determinística do valor real. Ela
    existe para proteger o contrato da porta de identidade de currículo.
    """

    def test_devolve_curriculo_id_com_o_uuid_gerado_a_cada_chamada(self) -> None:
        """Confirma que cada chamada delega ao gerador e embrulha o resultado.

        Faz o gerador de UUID devolver dois valores conhecidos e compara os
        value objects retornados. Ele existe para provar que o adapter não
        reutiliza identidades entre chamadas.
        """
        with patch(f"{GERADOR}.uuid4", side_effect=[PRIMEIRO, SEGUNDO]) as uuid4_mock:
            primeiro = GeradorCurriculoIdUuid4().gerar()
            segundo = GeradorCurriculoIdUuid4().gerar()

        self.assertEqual(primeiro, CurriculoId(PRIMEIRO))
        self.assertEqual(segundo, CurriculoId(SEGUNDO))
        self.assertEqual(uuid4_mock.call_count, 2)

    def test_gera_value_object_com_uuid_versao_4(self) -> None:
        """Confirma o tipo e a versão do identificador produzido sem substituições.

        Chama o adapter com o gerador real e verifica que o resultado é um
        ``CurriculoId`` cujo valor é um UUID versão 4. A propriedade verificada
        vale para qualquer valor sorteado, mantendo o teste determinístico.
        """
        identificador = GeradorCurriculoIdUuid4().gerar()

        self.assertIsInstance(identificador, CurriculoId)
        self.assertIsInstance(identificador.valor, UUID)
        self.assertEqual(identificador.valor.version, 4)
