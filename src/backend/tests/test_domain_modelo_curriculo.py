"""Testa unitariamente os modelos de currículo e a recusa de modelo desconhecido."""

import unittest
from uuid import uuid4

# Proveniência: decision-analysis prompts/backend/20261017-140000-modelo-curriculo-edicao-versao-v001.md#v001
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
    """Verifica o vocabulário de modelos e a validação na edição da versão.

    Os testes exercitam a enumeração e ``editar_versao`` sem portas, banco ou
    framework. A classe existe para proteger no domínio a regra de que a edição
    só aceita modelos suportados.
    """

    def test_identificadores_dos_modelos_sao_estaveis(self) -> None:
        """Confirma os identificadores textuais de cada modelo.

        O teste compara o mapa completo, de modo que renomear um valor quebre o
        teste. Ele existe porque esses textos são gravados e expostos.
        """
        self.assertEqual(
            {modelo.name: modelo.value for modelo in ModeloCurriculo},
            {"CLASSICO": "classico", "COMPACTO": "compacto"},
        )

    def test_edicao_aceita_cada_modelo_suportado(self) -> None:
        """Confirma que a edição grava cada modelo suportado.

        O teste edita a versão com cada identificador e confere o modelo
        resultante. Ele existe para garantir o caminho de sucesso.
        """
        for modelo in ModeloCurriculo:
            with self.subTest(modelo=modelo.value):
                curriculo = _criar_curriculo()

                curriculo.editar_versao("Gestão de Projetos", modelo.value, True)

                self.assertEqual(curriculo.layout, modelo.value)

    def test_edicao_recusa_modelo_desconhecido_sem_alterar_a_versao(self) -> None:
        """Confirma que um modelo inexistente é recusado e nada é alterado.

        O teste tenta editar com modelos fora do vocabulário, inclusive variação
        de maiúsculas e texto vazio, e confere título, modelo e visibilidade
        intactos. Ele existe para que uma edição inválida não grave um modelo
        que o sistema não sabe apresentar.
        """
        for invalido in ("moderno", "Classico", "", "  "):
            with self.subTest(modelo=invalido):
                curriculo = _criar_curriculo("classico")

                with self.assertRaises(RegraDeDominioViolada):
                    curriculo.editar_versao("Gestão de Projetos", invalido, True)

                self.assertEqual(curriculo.titulo_versao, "Estágio em TI")
                self.assertEqual(curriculo.layout, "classico")
                self.assertFalse(curriculo.is_public)

    def test_versao_ja_existente_com_outro_modelo_continua_valida(self) -> None:
        """Confirma que a validação vale só para a edição, não para a leitura.

        O teste constrói uma versão com um modelo fora do vocabulário, como o
        que pode já estar gravado, e confere que ela é criada. Ele existe para
        que a nova regra não impeça carregar versões antigas do banco.
        """
        curriculo = _criar_curriculo("padrao")

        self.assertEqual(curriculo.layout, "padrao")
