"""Testa unitariamente a regra de domínio de propriedade da referência do currículo."""

import unittest
from uuid import uuid4

# Proveniência: decision-analysis prompts/backend/20261017-120000-propriedade-referencia-curriculo-v001.md#v001
from backend.domain import (
    Curriculo,
    CurriculoId,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    ReferenciaDeOutroProprietario,
    RegraDeDominioViolada,
    UsuarioId,
)


def _criar_curriculo(usuario_id: UsuarioId) -> Curriculo:
    """Cria uma versão de currículo válida pertencente ao usuário informado.

    A função monta o agregado sem acessar gerador, banco ou relógio. Ela existe
    para que cada teste controle quem é o dono da versão sem repetir o cenário.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id,
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


def _criar_referencia() -> ReferenciaCurriculo:
    """Cria uma referência válida a um projeto acadêmico com identidade nova.

    A função escolhe um tipo de item apenas para compor o cenário. Ela existe
    para reduzir repetição nos testes que não dependem do tipo do item.
    """
    return ReferenciaCurriculo(ProjetoAcademicoId(uuid4()))


class PropriedadeReferenciaCurriculoTestCase(unittest.TestCase):
    """Verifica a regra de que a versão só reúne itens do próprio estudante.

    Os testes exercitam ``incluir_referencia_do_proprietario`` com proprietários
    informados diretamente, sem portas, banco ou framework. A classe existe para
    proteger no domínio a invariante de propriedade da seleção.
    """

    def test_inclui_item_do_proprio_dono_do_curriculo(self) -> None:
        """Confirma que o item do dono entra na composição da versão.

        O teste informa como proprietário o mesmo usuário do agregado e confere
        a referência incluída. Ele existe para garantir o caminho de sucesso.
        """
        dono = UsuarioId(uuid4())
        curriculo = _criar_curriculo(dono)
        referencia = _criar_referencia()

        curriculo.incluir_referencia_do_proprietario(referencia, dono)

        self.assertEqual(curriculo.referencias, frozenset({referencia}))

    def test_recusa_item_de_outro_proprietario_sem_alterar_a_versao(self) -> None:
        """Confirma que o item de outro estudante é recusado e nada é incluído.

        O teste informa um proprietário diferente do dono e confere a falha
        específica e a composição inalterada. Ele existe para impedir que dado
        alheio entre numa versão e seja exposto na exportação.
        """
        curriculo = _criar_curriculo(UsuarioId(uuid4()))

        with self.assertRaises(ReferenciaDeOutroProprietario):
            curriculo.incluir_referencia_do_proprietario(
                _criar_referencia(), UsuarioId(uuid4())
            )

        self.assertEqual(curriculo.referencias, frozenset())

    def test_recusa_por_propriedade_e_uma_regra_de_dominio(self) -> None:
        """Confirma que a recusa por propriedade é uma violação de domínio.

        O teste captura a falha pelo tipo geral das regras de domínio. Ele
        existe para que consumidores que já tratam essa família de falhas
        continuem funcionando.
        """
        curriculo = _criar_curriculo(UsuarioId(uuid4()))

        with self.assertRaises(RegraDeDominioViolada):
            curriculo.incluir_referencia_do_proprietario(
                _criar_referencia(), UsuarioId(uuid4())
            )

    def test_propriedade_e_verificada_antes_da_duplicidade(self) -> None:
        """Confirma que o item alheio é recusado por propriedade, não duplicidade.

        O teste inclui a referência pelo dono e tenta repeti-la com outro
        proprietário. Ele existe para que a falha por propriedade prevaleça e a
        duplicidade de um item alheio não seja revelada.
        """
        dono = UsuarioId(uuid4())
        curriculo = _criar_curriculo(dono)
        referencia = _criar_referencia()
        curriculo.incluir_referencia_do_proprietario(referencia, dono)

        with self.assertRaises(ReferenciaDeOutroProprietario):
            curriculo.incluir_referencia_do_proprietario(
                referencia, UsuarioId(uuid4())
            )

    def test_duplicidade_do_dono_nao_e_falha_de_propriedade(self) -> None:
        """Confirma que repetir um item do dono continua sendo duplicidade.

        O teste repete a inclusão com o proprietário correto e exige que a falha
        não seja a de propriedade. Ele existe para manter as duas regras
        distinguíveis por quem orquestra a seleção.
        """
        dono = UsuarioId(uuid4())
        curriculo = _criar_curriculo(dono)
        referencia = _criar_referencia()
        curriculo.incluir_referencia_do_proprietario(referencia, dono)

        with self.assertRaises(RegraDeDominioViolada) as contexto:
            curriculo.incluir_referencia_do_proprietario(referencia, dono)

        self.assertNotIsInstance(
            contexto.exception, ReferenciaDeOutroProprietario
        )
