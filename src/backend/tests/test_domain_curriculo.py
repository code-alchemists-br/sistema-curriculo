"""Testa invariantes unitárias do aggregate root de currículo."""

import unittest
from uuid import uuid4

from backend.domain import (
    CompetenciaId,
    Curriculo,
    CurriculoId,
    FormacaoAcademicaId,
    ReferenciaCurriculo,
    RegraDeDominioViolada,
    UsuarioId,
)


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
class CurriculoTestCase(unittest.TestCase):
    """Verifica a composição local de um currículo sem consultar outros agregados.

    A classe exerce o aggregate root exclusivamente com IDs e referências em
    memória. Ela existe para assegurar que inclusão, remoção e duplicidade sejam
    protegidas pelo próprio currículo antes de qualquer caso de uso ou repositório.
    """

    def test_curriculo_expoe_referencias_sem_permitir_alteracao_externa(self) -> None:
        """Confirma que a coleção pública é imutável e reflete inclusões válidas.

        O teste inclui uma referência por meio do método do agregado e verifica
        que a visão retornada é um ``frozenset``. Ele existe para impedir que um
        consumidor altere a composição sem passar pelas invariantes do currículo.
        """
        curriculo = _criar_curriculo()
        referencia = ReferenciaCurriculo(FormacaoAcademicaId(uuid4()))

        curriculo.incluir_referencia(referencia)

        self.assertEqual(curriculo.referencias, frozenset({referencia}))

    def test_curriculo_rejeita_referencia_duplicada(self) -> None:
        """Confirma que o mesmo item não pode ser incluído duas vezes.

        O teste repete a inclusão de uma referência tipada e espera a falha de
        domínio. Ele existe para preservar a consistência local das associações
        do currículo sem depender de tabela de junção ou banco de dados.
        """
        curriculo = _criar_curriculo()
        referencia = ReferenciaCurriculo(CompetenciaId(uuid4()))
        curriculo.incluir_referencia(referencia)

        with self.assertRaises(RegraDeDominioViolada):
            curriculo.incluir_referencia(referencia)

    def test_curriculo_rejeita_remocao_de_referencia_ausente(self) -> None:
        """Confirma que remover item não incluído é uma transição inválida.

        O teste pede a remoção de uma referência inexistente e espera a falha de
        domínio. Ele existe para tornar explícitas as mudanças de composição do
        agregado e evitar estados silenciosamente inconsistentes.
        """
        curriculo = _criar_curriculo()

        with self.assertRaises(RegraDeDominioViolada):
            curriculo.remover_referencia(ReferenciaCurriculo(CompetenciaId(uuid4())))


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
def _criar_curriculo() -> Curriculo:
    """Cria um currículo válido para manter os testes focados na regra exercitada.

    A função gera identificadores em memória e fornece os campos mínimos do
    aggregate root. Ela existe para evitar repetição de preparação nos testes sem
    introduzir fixture externa, banco ou dependência de framework.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=UsuarioId(uuid4()),
        titulo_versao="Currículo principal",
        layout="padrao",
        is_public=False,
    )
