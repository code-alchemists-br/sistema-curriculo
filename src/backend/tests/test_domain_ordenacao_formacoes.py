"""Testa a ordenação estável de formações acadêmicas por situação e data."""

import unittest
from datetime import date
from uuid import UUID

from backend.domain import (
    FormacaoAcademica,
    FormacaoAcademicaId,
    NivelFormacaoAcademica,
    Periodo,
    StatusFormacaoAcademica,
    UsuarioId,
    ordenar_formacoes,
)

# Proveniência: decision-analysis prompts/backend/20261015-150000-ordenacao-formacoes-academicas-v001.md#v001

USUARIO_ID = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))


class OrdenacaoFormacoesTestCase(unittest.TestCase):
    """Verifica a regra de domínio que ordena formações para o currículo.

    Os cenários constroem entidades em memória com identificadores e datas
    fixos, sem relógio, banco ou framework. A classe existe para proteger a
    prioridade por situação, a ordem por data e o desempate estável.
    """

    def test_em_andamento_vem_antes_de_concluida_e_interrompida(self) -> None:
        """Prioriza a situação mesmo quando a data indicaria outra posição.

        A formação em andamento é a mais antiga das três e a interrompida a
        mais recente, mas o resultado segue em andamento, concluída e
        interrompida. O teste existe para garantir que a situação é o primeiro
        critério da ordenação.
        """
        em_andamento = _formacao(1, StatusFormacaoAcademica.EM_ANDAMENTO, date(2018, 1, 1))
        concluida = _formacao(
            2, StatusFormacaoAcademica.CONCLUIDO, date(2020, 1, 1), date(2022, 12, 1)
        )
        interrompida = _formacao(
            3, StatusFormacaoAcademica.INTERROMPIDO, date(2023, 1, 1), date(2024, 6, 1)
        )

        resultado = ordenar_formacoes([interrompida, concluida, em_andamento])

        self.assertEqual(resultado, (em_andamento, concluida, interrompida))

    def test_em_andamento_ordena_pela_data_de_inicio_mais_recente(self) -> None:
        """Ordena formações em andamento do início mais recente ao mais antigo.

        Uma das formações traz previsão de término posterior, que não deve
        alterar a ordem definida pelo início. O teste existe para fixar o
        início como referência das formações em andamento.
        """
        antiga = _formacao(
            1, StatusFormacaoAcademica.EM_ANDAMENTO, date(2021, 2, 1), date(2027, 12, 1)
        )
        recente = _formacao(2, StatusFormacaoAcademica.EM_ANDAMENTO, date(2024, 8, 1))

        resultado = ordenar_formacoes([antiga, recente])

        self.assertEqual(resultado, (recente, antiga))

    def test_concluidas_ordenam_pelo_termino_mais_recente(self) -> None:
        """Ordena concluídas do término mais recente ao mais antigo.

        A formação que começou antes terminou depois e por isso aparece
        primeiro. O teste existe para fixar o término como referência das
        formações concluídas.
        """
        termino_recente = _formacao(
            1, StatusFormacaoAcademica.CONCLUIDO, date(2015, 1, 1), date(2023, 12, 1)
        )
        termino_antigo = _formacao(
            2, StatusFormacaoAcademica.CONCLUIDO, date(2019, 1, 1), date(2021, 6, 1)
        )

        resultado = ordenar_formacoes([termino_antigo, termino_recente])

        self.assertEqual(resultado, (termino_recente, termino_antigo))

    def test_interrompida_sem_termino_usa_o_inicio_como_referencia(self) -> None:
        """Compara interrompidas pelo término ou, sem ele, pelo início.

        Uma interrompida sem término começou depois do término da outra e, por
        isso, vem primeiro. O teste existe para cobrir o período aberto aceito
        pelo domínio para formações interrompidas.
        """
        sem_termino = _formacao(3, StatusFormacaoAcademica.INTERROMPIDO, date(2024, 3, 1))
        com_termino = _formacao(
            4, StatusFormacaoAcademica.INTERROMPIDO, date(2020, 1, 1), date(2022, 1, 1)
        )

        resultado = ordenar_formacoes([com_termino, sem_termino])

        self.assertEqual(resultado, (sem_termino, com_termino))

    def test_mesmo_termino_desempata_pelo_inicio_mais_recente(self) -> None:
        """Usa o início mais recente quando situação e término coincidem.

        Duas concluídas terminam no mesmo dia; a que começou depois vem antes.
        O teste existe para proteger o critério intermediário de desempate.
        """
        inicio_antigo = _formacao(
            1, StatusFormacaoAcademica.CONCLUIDO, date(2018, 1, 1), date(2022, 12, 1)
        )
        inicio_recente = _formacao(
            2, StatusFormacaoAcademica.CONCLUIDO, date(2020, 1, 1), date(2022, 12, 1)
        )

        resultado = ordenar_formacoes([inicio_antigo, inicio_recente])

        self.assertEqual(resultado, (inicio_recente, inicio_antigo))

    def test_empate_total_e_desfeito_pelo_identificador_de_forma_estavel(self) -> None:
        """Mantém a mesma ordem para formações empatadas em qualquer entrada.

        Três formações com a mesma situação e as mesmas datas são ordenadas a
        partir de várias permutações da entrada, e todas produzem a sequência
        crescente por identificador. O teste existe para garantir que a ordem
        não depende da ordem de chegada dos itens.
        """
        primeira = _formacao(
            1, StatusFormacaoAcademica.CONCLUIDO, date(2019, 1, 1), date(2022, 12, 1)
        )
        segunda = _formacao(
            2, StatusFormacaoAcademica.CONCLUIDO, date(2019, 1, 1), date(2022, 12, 1)
        )
        terceira = _formacao(
            3, StatusFormacaoAcademica.CONCLUIDO, date(2019, 1, 1), date(2022, 12, 1)
        )
        esperado = (primeira, segunda, terceira)

        for entrada in (
            [primeira, segunda, terceira],
            [terceira, segunda, primeira],
            [segunda, terceira, primeira],
        ):
            with self.subTest(entrada=[formacao.id.valor.int for formacao in entrada]):
                self.assertEqual(ordenar_formacoes(entrada), esperado)

    def test_colecao_vazia_devolve_tupla_vazia(self) -> None:
        """Devolve tupla vazia quando não há formações a ordenar.

        A função aceita qualquer iterável e sempre devolve tupla imutável. O
        teste existe para cobrir o perfil sem formações cadastradas.
        """
        self.assertEqual(ordenar_formacoes([]), ())


def _formacao(
    numero: int,
    status: StatusFormacaoAcademica,
    inicio: date,
    fim: date | None = None,
) -> FormacaoAcademica:
    """Cria uma formação válida com identificador determinístico.

    A função deriva o UUID de um número inteiro e preenche os textos com
    valores fixos, variando apenas situação e período. Ela existe para que os
    cenários de ordenação controlem exatamente os critérios comparados.
    """
    return FormacaoAcademica(
        id=FormacaoAcademicaId(UUID(int=numero)),
        usuario_id=USUARIO_ID,
        instituicao="Fatec",
        curso=f"Curso {numero}",
        nivel=NivelFormacaoAcademica.TECNOLOGO,
        periodo=Periodo(inicio, fim),
        status=status,
    )
