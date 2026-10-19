"""Verifica a regra de domínio candidatura implica interesse."""

import unittest
from uuid import uuid4

from backend.domain import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
    CurriculoId,
    RegraDeDominioViolada,
    VagaId,
)


# Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
class AssociacaoCurriculoVagaTestCase(unittest.TestCase):
    """Testa classificações da associação sem depender de camadas externas.

    Os cenários constroem o agregado em memória e exercitam inclusão de
    classificações. A classe existe para verificar a regra candidatura implica
    interesse e impedir que mutações públicas produzam estado inválido.
    """

    def test_interesse_isolado_permanece_sem_outras_classificacoes(self) -> None:
        """Confirma que interesse sozinho permanece como a única classificação.

        O teste constrói a associação somente com interesse e compara a visão
        pública com esse conjunto. Ele existe para evitar que a normalização
        acrescente classificações que o estudante não selecionou.
        """
        associacao = _criar_associacao(ClassificacaoAssociacao.INTERESSE)

        self.assertEqual(
            associacao.classificacoes,
            frozenset({ClassificacaoAssociacao.INTERESSE}),
        )

    def test_criar_com_candidatura_inclui_interesse(self) -> None:
        """Confirma que a construção com candidatura também registra interesse.

        O teste fornece somente candidatura à criação e verifica o conjunto
        normalizado. Ele existe para garantir a invariante desde o primeiro
        estado observável da associação.
        """
        associacao = _criar_associacao(ClassificacaoAssociacao.CANDIDATURA)

        self.assertEqual(
            associacao.classificacoes,
            frozenset(
                {
                    ClassificacaoAssociacao.CANDIDATURA,
                    ClassificacaoAssociacao.INTERESSE,
                }
            ),
        )

    def test_adicionar_candidatura_com_interesse_existente_nao_duplica(self) -> None:
        """Confirma que incluir candidatura mantém uma única ocorrência de interesse.

        O teste cria uma associação com interesse, adiciona candidatura e
        compara seu conjunto de classificações. Ele existe para assegurar que
        a inclusão é idempotente em relação ao interesse já presente.
        """
        associacao = _criar_associacao(ClassificacaoAssociacao.INTERESSE)

        associacao.adicionar_classificacao(ClassificacaoAssociacao.CANDIDATURA)

        self.assertEqual(
            associacao.classificacoes,
            frozenset(
                {
                    ClassificacaoAssociacao.CANDIDATURA,
                    ClassificacaoAssociacao.INTERESSE,
                }
            ),
        )

    def test_adicionar_classificacao_existente_e_idempotente(self) -> None:
        """Confirma que adicionar novamente não muda o estado do agregado.

        O teste adiciona interesse a uma associação que já o possui e verifica
        o sinal de mudança e o conjunto final. Ele existe para distinguir no-op
        de alteração persistível.
        """
        associacao = _criar_associacao(ClassificacaoAssociacao.INTERESSE)

        alterada = associacao.adicionar_classificacao(ClassificacaoAssociacao.INTERESSE)

        self.assertFalse(alterada)
        self.assertEqual(
            associacao.classificacoes,
            frozenset({ClassificacaoAssociacao.INTERESSE}),
        )

    def test_adicionar_candidatura_preserva_compatibilidade(self) -> None:
        """Confirma que a inclusão de candidatura não remove compatibilidade.

        O teste parte de compatibilidade, adiciona candidatura e verifica as
        três classificações previstas. Ele existe para preservar o estado
        previamente escolhido ao aplicar a invariante.
        """
        associacao = _criar_associacao(ClassificacaoAssociacao.COMPATIBILIDADE)

        associacao.adicionar_classificacao(ClassificacaoAssociacao.CANDIDATURA)

        self.assertEqual(
            associacao.classificacoes,
            frozenset(
                {
                    ClassificacaoAssociacao.CANDIDATURA,
                    ClassificacaoAssociacao.INTERESSE,
                    ClassificacaoAssociacao.COMPATIBILIDADE,
                }
            ),
        )

    def test_operacoes_publicas_nao_produzem_candidatura_sem_interesse(self) -> None:
        """Verifica a invariante após construção e inclusão de candidatura.

        O teste observa as associações criadas diretamente com candidatura ou
        atualizadas pelas inclusões públicas permitidas. Ele existe para cobrir
        todos os caminhos da #131 que podem produzir candidatura.
        """
        associacoes = (
            _criar_associacao(ClassificacaoAssociacao.CANDIDATURA),
            _criar_associacao(ClassificacaoAssociacao.INTERESSE),
            _criar_associacao(ClassificacaoAssociacao.COMPATIBILIDADE),
        )
        associacoes[1].adicionar_classificacao(ClassificacaoAssociacao.CANDIDATURA)
        associacoes[2].adicionar_classificacao(ClassificacaoAssociacao.CANDIDATURA)

        for associacao in associacoes:
            with self.subTest(classificacoes=associacao.classificacoes):
                if ClassificacaoAssociacao.CANDIDATURA in associacao.classificacoes:
                    self.assertIn(
                        ClassificacaoAssociacao.INTERESSE,
                        associacao.classificacoes,
                    )

    def test_visao_de_classificacoes_nao_pode_ser_alterada_externamente(self) -> None:
        """Confirma que consumidores não alteram o estado por meio da leitura.

        O teste obtém as classificações expostas pelo agregado e verifica que
        não oferecem uma operação de adição. Ele existe para impedir que a
        invariante seja contornada fora dos métodos do domínio.
        """
        associacao = _criar_associacao(ClassificacaoAssociacao.INTERESSE)

        with self.assertRaises(AttributeError):
            associacao.classificacoes.add(ClassificacaoAssociacao.CANDIDATURA)

    def test_associacao_rejeita_construcao_sem_classificacoes(self) -> None:
        """Confirma que uma associação não nasce sem classificação alguma.

        O teste fornece um conjunto vazio e espera uma violação de domínio. Ele
        existe para preservar o mínimo definido para uma associação sem
        introduzir qualquer regra de persistência ou remoção.
        """
        with self.assertRaises(RegraDeDominioViolada):
            AssociacaoCurriculoVaga(
                curriculo_id=CurriculoId(uuid4()),
                vaga_id=VagaId("vaga-1"),
                classificacoes=(),
            )

    def test_remover_classificacao_ausente_e_idempotente(self) -> None:
        """Confirma que remover item ausente deixa a associação inalterada.

        O teste remove candidatura de uma associação somente com interesse e
        verifica que nenhuma mudança foi produzida. Ele existe para permitir
        retries sem efeitos ou falhas artificiais.
        """
        associacao = _criar_associacao(ClassificacaoAssociacao.INTERESSE)

        alterada = associacao.remover_classificacao(ClassificacaoAssociacao.CANDIDATURA)

        self.assertFalse(alterada)
        self.assertEqual(
            associacao.classificacoes,
            frozenset({ClassificacaoAssociacao.INTERESSE}),
        )

    def test_remover_candidatura_preserva_interesse(self) -> None:
        """Confirma que retirar candidatura mantém interesse no agregado.

        O teste parte da combinação normalizada, remove somente candidatura e
        compara o conjunto restante. Ele existe para proteger a dependência de
        candidatura em cada transição.
        """
        associacao = _criar_associacao(ClassificacaoAssociacao.CANDIDATURA)

        alterada = associacao.remover_classificacao(ClassificacaoAssociacao.CANDIDATURA)

        self.assertTrue(alterada)
        self.assertEqual(
            associacao.classificacoes,
            frozenset({ClassificacaoAssociacao.INTERESSE}),
        )

    def test_remover_interesse_com_candidatura_rejeita_sem_alterar_estado(
        self,
    ) -> None:
        """Rejeita retirar interesse enquanto candidatura permanece.

        O teste captura o estado, tenta remover interesse e verifica a exceção e
        a ausência de mutação. Ele existe para manter a invariante após falha.
        """
        associacao = _criar_associacao(ClassificacaoAssociacao.CANDIDATURA)
        estado_original = associacao.classificacoes

        with self.assertRaises(RegraDeDominioViolada):
            associacao.remover_classificacao(ClassificacaoAssociacao.INTERESSE)

        self.assertEqual(associacao.classificacoes, estado_original)

    def test_remover_ultima_classificacao_rejeita_sem_alterar_estado(self) -> None:
        """Impede que uma associação válida passe a não ter classificações.

        O teste tenta retirar o único interesse e confirma falha sem mutação.
        Ele existe para manter o agregado não vazio durante toda sua vida útil.
        """
        associacao = _criar_associacao(ClassificacaoAssociacao.INTERESSE)

        with self.assertRaises(RegraDeDominioViolada):
            associacao.remover_classificacao(ClassificacaoAssociacao.INTERESSE)

        self.assertEqual(
            associacao.classificacoes,
            frozenset({ClassificacaoAssociacao.INTERESSE}),
        )

    def test_classificacoes_reconhecidas_sao_as_previstas_nos_requisitos(self) -> None:
        """Confirma que o domínio expõe somente os três rótulos aprovados.

        O teste compara os valores do enum com o vocabulário do requisito. Ele
        existe para impedir que a regra introduza classificações não aprovadas.
        """
        self.assertEqual(
            {classificacao.value for classificacao in ClassificacaoAssociacao},
            {"interesse", "compatibilidade", "candidatura"},
        )

    def test_associacao_preserva_identificadores_tipados(self) -> None:
        """Confirma que a associação mantém as identidades recebidas.

        O teste constrói a associação com objetos de identidade previamente
        tipados e verifica que a entidade os conserva. Ele existe para evitar
        conversões ou mistura de identidades no modelo mínimo.
        """
        curriculo_id = CurriculoId(uuid4())
        vaga_id = VagaId("vaga-externa-1")
        associacao = AssociacaoCurriculoVaga(
            curriculo_id=curriculo_id,
            vaga_id=vaga_id,
            classificacoes=(ClassificacaoAssociacao.INTERESSE,),
        )

        self.assertIs(associacao.curriculo_id, curriculo_id)
        self.assertIs(associacao.vaga_id, vaga_id)


# Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
def _criar_associacao(
    classificacao: ClassificacaoAssociacao,
) -> AssociacaoCurriculoVaga:
    """Cria associação válida para manter cada teste focado no comportamento.

    A função usa identificadores tipados em memória e uma única classificação
    inicial. Ela existe para compartilhar preparação sem banco, rede ou fixture
    externa.
    """
    return AssociacaoCurriculoVaga(
        curriculo_id=CurriculoId(uuid4()),
        vaga_id=VagaId("vaga-1"),
        classificacoes=(classificacao,),
    )
