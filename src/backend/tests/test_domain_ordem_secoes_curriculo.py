"""Testa unitariamente a ordem explícita das seções no agregado de currículo."""

import unittest
from uuid import uuid4

# Proveniência: decision-analysis prompts/backend/20261017-180000-persistir-ordem-secoes-curriculo-v001.md#v001
from backend.domain import (
    ORDEM_PADRAO_SECOES,
    Curriculo,
    CurriculoId,
    RegraDeDominioViolada,
    SecaoCurriculo,
    UsuarioId,
)


def _criar_curriculo(**extras) -> Curriculo:
    """Cria uma versão de currículo válida, aceitando campos adicionais.

    A função monta o agregado sem acessar gerador, banco ou relógio e repassa
    os campos extras ao construtor. Ela existe para que cada teste controle a
    ordem das seções sem repetir o restante do cenário.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=UsuarioId(uuid4()),
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
        **extras,
    )


class OrdemSecoesCurriculoTestCase(unittest.TestCase):
    """Verifica a ordem explícita das seções mantida pelo agregado.

    Os testes exercitam a construção e ``definir_ordem_secoes`` sem portas,
    banco ou framework. A classe existe para proteger a regra de que a ordem
    contém cada seção suportada exatamente uma vez.
    """

    def test_versao_nova_nasce_com_a_ordem_padrao(self) -> None:
        """Confirma que, sem ordem informada, vale a ordem padrão.

        O teste cria a versão sem ordem explícita. Ele existe para que toda
        versão tenha uma ordem definida desde a criação.
        """
        self.assertEqual(_criar_curriculo().ordem_secoes, ORDEM_PADRAO_SECOES)

    def test_define_nova_ordem_valida(self) -> None:
        """Confirma que uma permutação completa das seções é aceita.

        O teste inverte a ordem padrão e confere a ordem resultante. Ele existe
        para garantir o caminho de sucesso da mudança de ordem.
        """
        curriculo = _criar_curriculo()
        invertida = tuple(reversed(ORDEM_PADRAO_SECOES))

        curriculo.definir_ordem_secoes(invertida)

        self.assertEqual(curriculo.ordem_secoes, invertida)

    def test_recusa_ordem_sem_alterar_a_ordem_atual(self) -> None:
        """Confirma que ordens incompletas, repetidas ou vazias são recusadas.

        O teste tenta definir ordens inválidas e confere que a ordem anterior é
        mantida. Ele existe para que uma ordem inválida não deixe o agregado
        parcialmente alterado.
        """
        invalidas = {
            "sem uma seção": ORDEM_PADRAO_SECOES[:-1],
            "com seção repetida": ORDEM_PADRAO_SECOES[:-1] + (ORDEM_PADRAO_SECOES[0],),
            "vazia": (),
        }
        for descricao, ordem in invalidas.items():
            with self.subTest(ordem=descricao):
                curriculo = _criar_curriculo()

                with self.assertRaises(RegraDeDominioViolada):
                    curriculo.definir_ordem_secoes(ordem)

                self.assertEqual(curriculo.ordem_secoes, ORDEM_PADRAO_SECOES)

    def test_construcao_recusa_ordem_invalida(self) -> None:
        """Confirma que o agregado não pode ser criado com ordem inválida.

        O teste constrói a versão com uma ordem incompleta. Ele existe para que
        dados lidos da persistência também passem pela mesma validação.
        """
        with self.assertRaises(RegraDeDominioViolada):
            _criar_curriculo(ordem_secoes=(SecaoCurriculo.IDIOMAS,))

    def test_mudar_a_ordem_nao_altera_titulo_nem_referencias(self) -> None:
        """Confirma que a ordem é independente do restante da versão.

        O teste muda a ordem e confere título, modelo, visibilidade e referências
        intactos. Ele existe para que a edição da ordem não tenha efeito
        colateral na composição da versão.
        """
        curriculo = _criar_curriculo()

        curriculo.definir_ordem_secoes(tuple(reversed(ORDEM_PADRAO_SECOES)))

        self.assertEqual(curriculo.titulo_versao, "Estágio em TI")
        self.assertEqual(curriculo.layout, "classico")
        self.assertFalse(curriculo.is_public)
        self.assertEqual(curriculo.referencias, frozenset())
