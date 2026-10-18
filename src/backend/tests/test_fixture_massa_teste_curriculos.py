"""Garante que a massa JSON seja renderizável pelo contrato público de prévia."""

import unittest

from backend.api.previa_versao_curriculo import _para_resposta
from backend.tests.fixtures.massa_teste_curriculos import obter_curriculos_massa_teste


class MassaTesteCurriculosTestCase(unittest.TestCase):
    """Exercita entidades reais da massa no serializador usado pela API.

    A classe transforma cada registro JSON em entidades e usa o renderizador da
    rota de prévia para obter o payload público. Ela existe para impedir que os
    exemplos documentais divirjam do formato consumido pelo frontend.
    """

    def test_massa_constroi_entidades_e_gera_previas_publicas(self) -> None:
        """Confirma que os três perfis chegam ao payload de prévia oficial.

        O teste carrega a massa, monta o modelo de leitura e serializa-o pelo
        conversor da API, verificando campos e seções consumidos pela interface.
        Ele existe para proteger a compatibilidade ponta a ponta da massa.
        """
        curriculos = obter_curriculos_massa_teste()
        self.assertEqual(len(curriculos), 3)
        for fixture in curriculos:
            with self.subTest(titulo=fixture.curriculo.titulo_versao):
                resposta = _para_resposta(fixture.para_previa()).model_dump(mode="json")
                self.assertEqual(resposta["curriculo_id"], str(fixture.curriculo.id.valor))
                self.assertEqual(resposta["estudante"]["nome"], fixture.usuario.nome.valor)
                self.assertTrue(resposta["formacoes"])
                self.assertTrue(resposta["experiencias"])
                self.assertTrue(resposta["projetos"])
                self.assertTrue(resposta["competencias"])
                self.assertTrue(resposta["idiomas"])

