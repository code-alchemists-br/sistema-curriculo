"""Testa unitariamente as seções do currículo e a ordem padrão de apresentação."""

import unittest

# Proveniência: decision-analysis prompts/backend/20261017-100000-secoes-curriculo-ordem-padrao-v001.md#v001
from backend.domain import ORDEM_PADRAO_SECOES, SecaoCurriculo, SecaoRevisao


class SecaoCurriculoTestCase(unittest.TestCase):
    """Verifica o vocabulário de seções e a ordem padrão do currículo.

    Os testes comparam identificadores, ordem, cobertura e conversão a partir de
    texto, sem dependências externas. A classe existe para proteger o contrato
    de seções que persistência, consulta e exportação compartilham.
    """

    def test_identificadores_das_secoes_sao_estaveis(self) -> None:
        """Confirma os identificadores textuais de cada seção.

        O teste compara o mapa completo, de modo que renomear um valor quebre o
        teste. Ele existe porque esses textos serão persistidos e expostos.
        """
        self.assertEqual(
            {secao.name: secao.value for secao in SecaoCurriculo},
            {
                "DADOS_PESSOAIS": "dados-pessoais",
                "FORMACAO_ACADEMICA": "formacao-academica",
                "EXPERIENCIAS_PROFISSIONAIS": "experiencias-profissionais",
                "PROJETOS_ACADEMICOS": "projetos-academicos",
                "COMPETENCIAS": "competencias",
                "IDIOMAS": "idiomas",
                "DOCUMENTOS_COMPLEMENTARES": "documentos-complementares",
            },
        )

    def test_ordem_padrao_segue_a_sequencia_definida(self) -> None:
        """Confirma a ordem padrão de apresentação das seções.

        O teste compara a sequência exata. Ele existe para que qualquer mudança
        na ordem padrão seja uma decisão consciente e revisada.
        """
        self.assertEqual(
            ORDEM_PADRAO_SECOES,
            (
                SecaoCurriculo.DADOS_PESSOAIS,
                SecaoCurriculo.FORMACAO_ACADEMICA,
                SecaoCurriculo.EXPERIENCIAS_PROFISSIONAIS,
                SecaoCurriculo.PROJETOS_ACADEMICOS,
                SecaoCurriculo.COMPETENCIAS,
                SecaoCurriculo.IDIOMAS,
                SecaoCurriculo.DOCUMENTOS_COMPLEMENTARES,
            ),
        )

    def test_ordem_padrao_cobre_cada_secao_uma_unica_vez(self) -> None:
        """Confirma que a ordem padrão não omite nem repete seção.

        O teste compara o tamanho da tupla com o conjunto de seções e com o
        total da enumeração. Ele existe para que uma seção nova adicionada ao
        Enum sem entrar na ordem padrão seja detectada imediatamente.
        """
        self.assertEqual(len(ORDEM_PADRAO_SECOES), len(set(ORDEM_PADRAO_SECOES)))
        self.assertEqual(set(ORDEM_PADRAO_SECOES), set(SecaoCurriculo))

    def test_ordem_padrao_e_imutavel(self) -> None:
        """Confirma que a ordem padrão é uma tupla e não pode ser alterada.

        O teste verifica o tipo da coleção. Ele existe para impedir que um
        consumidor reordene a sequência compartilhada por engano.
        """
        self.assertIsInstance(ORDEM_PADRAO_SECOES, tuple)

    def test_secao_e_reconhecida_a_partir_do_identificador(self) -> None:
        """Confirma a conversão de um identificador textual na seção.

        O teste constrói a seção pelo valor e compara com o texto. Ele existe
        para que dados lidos de banco ou de requisição sejam reconhecidos.
        """
        self.assertIs(SecaoCurriculo("idiomas"), SecaoCurriculo.IDIOMAS)
        self.assertEqual(SecaoCurriculo.IDIOMAS, "idiomas")

    def test_identificador_desconhecido_e_rejeitado(self) -> None:
        """Confirma que um identificador fora do vocabulário é recusado.

        O teste tenta criar uma seção inexistente. Ele existe para garantir que
        o vocabulário é fechado e não aceita texto livre.
        """
        with self.assertRaises(ValueError):
            SecaoCurriculo("hobbies")

    def test_secoes_da_revisao_pertencem_ao_vocabulario_do_curriculo(self) -> None:
        """Confirma que toda seção da revisão existe também no currículo.

        O teste compara os identificadores das duas enumerações. Ele existe para
        que a revisão e o currículo não divirjam em silêncio.
        """
        self.assertLessEqual(
            {secao.value for secao in SecaoRevisao},
            {secao.value for secao in SecaoCurriculo},
        )
