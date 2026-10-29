"""Testa unitariamente os modelos de currículo e a recusa de modelo desconhecido."""

import unittest
from uuid import uuid4

from backend.domain import (
    Curriculo,
    CurriculoId,
    ModeloCurriculo,
    RegraDeDominioViolada,
    UsuarioId,
)


def _criar_curriculo(layout: str = "classico") -> Curriculo:
    """Cria uma versão de currículo válida com o modelo informado.

    A função monta o agregado sem acessar gerador, banco ou relógio. Ela existe
    para que cada teste controle o modelo inicial sem repetir o cenário.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=UsuarioId(uuid4()),
        titulo_versao="Estágio em TI",
        layout=layout,
        is_public=False,
    )


class ModeloCurriculoTestCase(unittest.TestCase):
    """Verifica o vocabulário de modelos e a validação na edição da versão."""

    def test_identificadores_dos_modelos_sao_estaveis(self) -> None:
        """Confirma o mapa completo dos identificadores públicos dos modelos."""
        self.assertEqual(
            {modelo.name: modelo.value for modelo in ModeloCurriculo},
            {
                "CLASSICO": "classico",
                "COMPACTO": "compacto",
                "ATS_SIMPLES": "ats-simples",
                "CRIATIVO": "criativo",
                "MODERNO": "moderno",
                "ACADEMICO": "academico",
                "PRIMEIRO_EMPREGO": "primeiro-emprego",
            },
        )

    def test_edicao_aceita_cada_modelo_suportado(self) -> None:
        """Confirma que a edição grava cada modelo suportado como texto simples."""
        for modelo in ModeloCurriculo:
            with self.subTest(modelo=modelo.value):
                curriculo = _criar_curriculo()

                curriculo.editar_versao("Gestão de Projetos", modelo.value, True)

                self.assertEqual(curriculo.layout, modelo.value)

    def test_edicao_recusa_modelo_desconhecido_sem_alterar_a_versao(self) -> None:
        """Confirma que uma edição com modelo inexistente não muda a versão."""
        for invalido in ("inexistente", "Classico", "", "  "):
            with self.subTest(modelo=invalido):
                curriculo = _criar_curriculo("classico")

                with self.assertRaises(RegraDeDominioViolada):
                    curriculo.editar_versao("Gestão de Projetos", invalido, True)

                self.assertEqual(curriculo.titulo_versao, "Estágio em TI")
                self.assertEqual(curriculo.layout, "classico")
                self.assertFalse(curriculo.is_public)

    def test_versao_ja_existente_com_outro_modelo_continua_valida(self) -> None:
        """Confirma que a leitura continua aceitando layout histórico não catalogado."""
        curriculo = _criar_curriculo("padrao")

        self.assertEqual(curriculo.layout, "padrao")
