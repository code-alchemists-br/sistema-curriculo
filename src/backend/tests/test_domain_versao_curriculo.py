"""Testa unitariamente a edição de versão no agregado de currículo."""

import unittest
from uuid import uuid4

from backend.domain import (
    Curriculo,
    CurriculoId,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    RegraDeDominioViolada,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001


class VersaoCurriculoDomainTestCase(unittest.TestCase):
    """Verifica a edição de título, layout e visibilidade do ``Curriculo``.

    A classe exerce somente o domínio com value objects em memória, sem portas
    ou recursos externos. Ela existe para proteger identidade, proprietário,
    referências e atomicidade da edição.
    """

    def test_edita_versao_preservando_identidade_proprietario_e_referencias(self) -> None:
        """Confirma que os três dados mudam e o restante do agregado permanece.

        O teste inclui uma referência antes de editar e compara identidade,
        proprietário e referências depois da transição. Ele existe para garantir
        que a edição não afete a composição nem a posse da versão.
        """
        curriculo = _criar_curriculo()
        referencia = ReferenciaCurriculo(ProjetoAcademicoId(uuid4()))
        curriculo.incluir_referencia(referencia)
        identidade = curriculo.id
        proprietario = curriculo.usuario_id

        curriculo.editar_versao("Gestão de Projetos", "moderno", True)

        self.assertEqual(curriculo.titulo_versao, "Gestão de Projetos")
        self.assertEqual(curriculo.layout, "moderno")
        self.assertTrue(curriculo.is_public)
        self.assertEqual(curriculo.id, identidade)
        self.assertEqual(curriculo.usuario_id, proprietario)
        self.assertEqual(curriculo.referencias, frozenset({referencia}))

    def test_rejeita_titulo_em_branco_sem_alterar_o_agregado(self) -> None:
        """Confirma que título formado só por espaços é recusado sem efeito.

        O teste tenta editar com título em branco e compara o estado depois da
        falha. Ele existe para impedir uma versão anônima por meio da edição.
        """
        curriculo = _criar_curriculo()

        with self.assertRaises(RegraDeDominioViolada):
            curriculo.editar_versao("   ", "moderno", True)

        _confirmar_estado_original(self, curriculo)

    def test_rejeita_visibilidade_nao_booleana_sem_alterar_nenhum_campo(self) -> None:
        """Confirma que uma edição parcialmente válida não modifica o agregado.

        O teste envia título e layout válidos com visibilidade inválida e exige
        que nenhum dos campos tenha sido alterado. Ele existe para provar que a
        validação ocorre antes de qualquer atribuição.
        """
        curriculo = _criar_curriculo()

        with self.assertRaises(RegraDeDominioViolada):
            curriculo.editar_versao("Gestão de Projetos", "moderno", "sim")  # type: ignore[arg-type]

        _confirmar_estado_original(self, curriculo)


def _criar_curriculo() -> Curriculo:
    """Cria uma versão de currículo válida e independente de I/O.

    A função reúne value objects determinísticos, exceto pelas identidades sem
    significado externo. Ela existe para reduzir repetição e manter os testes
    concentrados na transição de edição.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=UsuarioId(uuid4()),
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


def _confirmar_estado_original(teste: unittest.TestCase, curriculo: Curriculo) -> None:
    """Afirma que título, layout e visibilidade mantêm os valores de ``_criar_curriculo``.

    A função compara os três campos editáveis com os valores iniciais. Ela
    existe para evitar repetir as mesmas asserções nos cenários de falha.
    """
    teste.assertEqual(curriculo.titulo_versao, "Estágio em TI")
    teste.assertEqual(curriculo.layout, "classico")
    teste.assertFalse(curriculo.is_public)
