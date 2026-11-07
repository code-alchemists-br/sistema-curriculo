"""Protege o relógio do sistema usado pela exclusão lógica."""

import unittest
from datetime import timedelta

from backend.infrastructure.relogio import RelogioSistema


class RelogioSistemaTestCase(unittest.TestCase):
    """Verifica que o relógio do sistema devolve instantes com fuso UTC.

    A classe chama o adapter real e confere propriedades que valem para qualquer
    instante. Ela existe para garantir que o domínio nunca receba data sem fuso.
    """

    def test_agora_devolve_instante_com_fuso_utc(self) -> None:
        """Confirma que o instante devolvido informa fuso e é UTC.

        Obtém o instante e verifica a presença de ``tzinfo`` e o deslocamento
        zero. Ele existe para proteger a regra de exclusão que recusa instantes
        sem fuso.
        """
        instante = RelogioSistema().agora()

        self.assertIsNotNone(instante.tzinfo)
        self.assertEqual(instante.utcoffset(), timedelta(0))
