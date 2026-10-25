"""Testa unitariamente a decisão do estudante sobre uma recomendação."""

import unittest
from datetime import UTC, datetime, timedelta, timezone
from uuid import uuid4

# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
from backend.domain import (
    CurriculoId,
    DecisaoEstudante,
    DecisaoRecomendacao,
    RegraDeDominioViolada,
)

INSTANTE = datetime(2026, 10, 23, 12, 0, tzinfo=UTC)


def _criar(**alteracoes) -> DecisaoRecomendacao:
    """Cria uma decisão válida, aceitando alterações pontuais nos campos.

    A função monta a decisão com valores determinísticos e sobrescreve só o que
    o teste pedir. Ela existe para que cada teste destaque um único campo.
    """
    campos = {
        "curriculo_id": CurriculoId(uuid4()),
        "codigo": "PROJETO_AUSENTE",
        "decisao": DecisaoEstudante.REJEITADA,
        "decidida_em": INSTANTE,
    }
    campos.update(alteracoes)
    return DecisaoRecomendacao(**campos)


class DecisaoRecomendacaoTestCase(unittest.TestCase):
    """Verifica a validação do value object ``DecisaoRecomendacao``.

    Os testes constroem decisões válidas e inválidas sem portas, banco ou
    framework. A classe existe para proteger a regra de que só uma decisão
    completa, com instante com fuso, pode ser persistida.
    """

    def test_identificadores_das_decisoes_sao_estaveis(self) -> None:
        """Confirma os valores textuais das duas decisões possíveis.

        O teste compara o mapa completo. Ele existe porque esses textos serão
        gravados no banco e expostos pela API.
        """
        self.assertEqual(
            {decisao.name: decisao.value for decisao in DecisaoEstudante},
            {"ACEITA": "aceita", "REJEITADA": "rejeitada"},
        )

    def test_cria_decisao_valida_para_cada_tipo_de_decisao(self) -> None:
        """Confirma que aceitar e rejeitar produzem decisões válidas.

        O teste cria uma decisão de cada tipo e confere os campos. Ele existe
        para garantir o caminho de sucesso.
        """
        for escolha in DecisaoEstudante:
            with self.subTest(decisao=escolha.value):
                decisao = _criar(decisao=escolha)

                self.assertEqual(decisao.decisao, escolha)
                self.assertEqual(decisao.codigo, "PROJETO_AUSENTE")
                self.assertEqual(decisao.decidida_em, INSTANTE)

    def test_aceita_instante_com_qualquer_fuso(self) -> None:
        """Confirma que o instante pode ter um fuso diferente de UTC.

        O teste usa o fuso de Brasília. Ele existe para que a regra exija fuso,
        mas não imponha UTC ao domínio.
        """
        brasilia = timezone(timedelta(hours=-3))

        decisao = _criar(decidida_em=datetime(2026, 10, 23, 9, 0, tzinfo=brasilia))

        self.assertEqual(decisao.decidida_em.utcoffset(), timedelta(hours=-3))

    def test_recusa_instante_sem_fuso_ou_que_nao_e_data(self) -> None:
        """Confirma que o instante sem fuso e valores que não são data são recusados.

        O teste tenta construir com um instante ingênuo e com um texto. Ele existe
        para que a data técnica seja sempre inequívoca.
        """
        for invalido in (datetime(2026, 10, 23, 12, 0), "2026-10-23T12:00:00Z"):
            with self.subTest(instante=repr(invalido)):
                with self.assertRaises(RegraDeDominioViolada):
                    _criar(decidida_em=invalido)

    def test_recusa_codigo_fora_do_padrao(self) -> None:
        """Confirma que códigos vazios, em minúsculas ou com símbolos são recusados.

        O teste tenta vários códigos inválidos. Ele existe para manter os códigos
        no mesmo formato dos que a revisão produz.
        """
        for invalido in ("", "  ", "projeto_ausente", "PROJETO AUSENTE", "1_PROJETO", "PROJETO-AUSENTE"):
            with self.subTest(codigo=invalido):
                with self.assertRaises(RegraDeDominioViolada):
                    _criar(codigo=invalido)

    def test_recusa_decisao_que_nao_e_da_enumeracao(self) -> None:
        """Confirma que um texto solto não vale como decisão.

        O teste passa o texto "aceita" no lugar da enumeração. Ele existe para
        que o vocabulário da decisão seja fechado.
        """
        with self.assertRaises(RegraDeDominioViolada):
            _criar(decisao="aceita")

    def test_recusa_versao_que_nao_e_identidade_tipada(self) -> None:
        """Confirma que a versão deve ser um ``CurriculoId``.

        O teste passa um UUID puro. Ele existe para manter a identidade tipada
        em todo o domínio.
        """
        with self.assertRaises(RegraDeDominioViolada):
            _criar(curriculo_id=uuid4())

    def test_decisao_e_imutavel_e_comparada_pelo_valor(self) -> None:
        """Confirma que a decisão é um value object imutável.

        O teste compara duas decisões iguais e tenta alterar um campo. Ele existe
        para que a escolha do estudante não mude depois de criada.
        """
        curriculo_id = CurriculoId(uuid4())
        primeira = _criar(curriculo_id=curriculo_id)
        segunda = _criar(curriculo_id=curriculo_id)

        self.assertEqual(primeira, segunda)
        with self.assertRaises(AttributeError):
            primeira.codigo = "OUTRO"  # type: ignore[misc]
