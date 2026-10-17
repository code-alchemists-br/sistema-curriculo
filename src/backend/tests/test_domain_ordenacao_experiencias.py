"""Testa a ordenação estável de experiências profissionais por data de início."""

import unittest
from datetime import date
from uuid import UUID

from backend.domain import (
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    Periodo,
    UsuarioId,
    ordenar_experiencias,
)

# Proveniência: decision-analysis prompts/backend/20261016-140000-ordenacao-experiencias-profissionais-v001.md#v001

USUARIO_ID = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))


class OrdenacaoExperienciasTestCase(unittest.TestCase):
    """Verifica a regra de domínio que ordena experiências para o currículo.

    Os cenários constroem entidades em memória com identificadores e datas
    fixos, sem relógio, banco ou framework. A classe existe para proteger a
    ordem por início, o desempate pela experiência em andamento e o desempate
    estável por identificador.
    """

    def test_inicio_mais_recente_vem_primeiro(self) -> None:
        """Ordena experiências do início mais recente para o mais antigo.

        Três experiências com inícios diferentes chegam fora de ordem. O teste
        existe para fixar a data de início como critério principal.
        """
        antiga = _experiencia(1, date(2019, 3, 1), date(2020, 6, 1))
        intermediaria = _experiencia(2, date(2021, 5, 1), date(2022, 1, 1))
        recente = _experiencia(3, date(2024, 1, 15))

        resultado = ordenar_experiencias([intermediaria, antiga, recente])

        self.assertEqual(resultado, (recente, intermediaria, antiga))

    def test_termino_nao_altera_ordem_quando_inicios_diferem(self) -> None:
        """Mantém o início como critério mesmo para experiência em andamento.

        Uma experiência antiga ainda em andamento fica depois de uma recente já
        encerrada. O teste existe para garantir que o término só desempata
        inícios iguais.
        """
        antiga_em_andamento = _experiencia(1, date(2018, 1, 1))
        recente_encerrada = _experiencia(2, date(2023, 1, 1), date(2023, 12, 1))

        resultado = ordenar_experiencias([antiga_em_andamento, recente_encerrada])

        self.assertEqual(resultado, (recente_encerrada, antiga_em_andamento))

    def test_mesmo_inicio_coloca_experiencia_em_andamento_primeiro(self) -> None:
        """Desempata inícios iguais pela experiência sem término.

        Duas experiências começam no mesmo dia; a que ainda não terminou vem
        antes da encerrada, mesmo com identificador maior. O teste existe para
        proteger o primeiro critério de desempate definido pelo produto.
        """
        encerrada = _experiencia(1, date(2022, 2, 1), date(2023, 6, 1))
        em_andamento = _experiencia(2, date(2022, 2, 1))

        resultado = ordenar_experiencias([encerrada, em_andamento])

        self.assertEqual(resultado, (em_andamento, encerrada))

    def test_mesmo_inicio_encerradas_seguem_termino_mais_recente(self) -> None:
        """Desempata encerradas com o mesmo início pelo término mais recente.

        Duas experiências encerradas começam no mesmo dia; a que terminou
        depois vem antes, mesmo com identificador maior. O teste existe para
        proteger o critério intermediário de desempate.
        """
        termino_antigo = _experiencia(1, date(2022, 2, 1), date(2022, 8, 1))
        termino_recente = _experiencia(2, date(2022, 2, 1), date(2023, 6, 1))

        resultado = ordenar_experiencias([termino_antigo, termino_recente])

        self.assertEqual(resultado, (termino_recente, termino_antigo))

    def test_empate_total_e_desfeito_pelo_identificador_de_forma_estavel(self) -> None:
        """Mantém a mesma ordem para experiências empatadas em qualquer entrada.

        Três experiências em andamento com o mesmo início são ordenadas a partir
        de várias permutações da entrada, e todas produzem a sequência crescente
        por identificador. O teste existe para garantir que a ordem não depende
        da ordem de chegada dos itens.
        """
        primeira = _experiencia(1, date(2022, 2, 1))
        segunda = _experiencia(2, date(2022, 2, 1))
        terceira = _experiencia(3, date(2022, 2, 1))
        esperado = (primeira, segunda, terceira)

        for entrada in (
            [primeira, segunda, terceira],
            [terceira, segunda, primeira],
            [segunda, terceira, primeira],
        ):
            with self.subTest(entrada=[item.id.valor.int for item in entrada]):
                self.assertEqual(ordenar_experiencias(entrada), esperado)

    def test_colecao_vazia_devolve_tupla_vazia(self) -> None:
        """Devolve tupla vazia quando não há experiências a ordenar.

        A função aceita qualquer iterável e sempre devolve tupla imutável. O
        teste existe para cobrir o perfil sem experiências cadastradas.
        """
        self.assertEqual(ordenar_experiencias([]), ())


def _experiencia(
    numero: int, inicio: date, fim: date | None = None
) -> ExperienciaProfissional:
    """Cria uma experiência válida com identificador determinístico.

    A função deriva o UUID de um número inteiro e preenche os textos com
    valores fixos, variando apenas o período. Ela existe para que os cenários
    de ordenação controlem exatamente os critérios comparados.
    """
    return ExperienciaProfissional(
        id=ExperienciaProfissionalId(UUID(int=numero)),
        usuario_id=USUARIO_ID,
        empresa="Empresa",
        cargo=f"Cargo {numero}",
        descricao="Desenvolvimento de APIs.",
        periodo=Periodo(inicio, fim),
    )
