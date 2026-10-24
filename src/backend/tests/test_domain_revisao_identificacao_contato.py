"""Testa a regra de completude de identificação e contato na revisão do currículo."""

import unittest
from dataclasses import replace

# Proveniência: decision-analysis prompts/backend/20261023-100000-completude-identificacao-contato-v001.md#v001
from backend.domain import (
    PendenciaRevisao,
    SecaoRevisao,
    SeveridadePendencia,
    Usuario,
    revisar_curriculo,
)
from backend.tests.fixtures.curriculo_exportacao import (
    CurriculoExportacaoFixture,
    obter_curriculo_exportacao_fixture,
)


def _usuario_com_contato(
    fixture: CurriculoExportacaoFixture, **alteracoes
) -> Usuario:
    """Devolve o estudante da fixture com o contato alterado conforme pedido.

    A função copia o contato da fixture aplicando as alterações informadas (por
    exemplo, cidade ou links), sem mudar a fixture compartilhada. Ela existe para
    que cada teste controle exatamente quais campos de contato estão preenchidos.
    """
    contato = replace(fixture.usuario.dados_contato, **alteracoes)
    return replace(fixture.usuario, dados_contato=contato)


def _revisar(fixture: CurriculoExportacaoFixture, usuario: Usuario):
    """Revisa o currículo completo da fixture com o estudante informado.

    A função mantém todas as seções preenchidas para que somente a identificação
    e o contato possam gerar pendências. Ela existe para isolar a regra testada.
    """
    return revisar_curriculo(
        usuario=usuario,
        formacoes=(fixture.formacao_academica,),
        experiencias=(fixture.experiencia_profissional,),
        projetos=(fixture.projeto_academico,),
        competencias=fixture.competencias,
        idiomas=fixture.idiomas,
    )


class IdentificacaoEContatoTestCase(unittest.TestCase):
    """Verifica a regra de completude da identificação e do contato.

    Os testes variam cidade, links e contato do estudante da fixture e observam as
    pendências geradas. A classe existe para proteger a diferença entre erro (sem
    contato) e aviso (cidade ou links ausentes).
    """

    def test_contato_completo_nao_gera_pendencia(self) -> None:
        """Confirma que cidade e links preenchidos não geram pendência.

        O teste revisa o estudante com cidade, LinkedIn e Lattes. Ele existe para
        proteger o caso feliz da regra.
        """
        fixture = obter_curriculo_exportacao_fixture()

        resultado = _revisar(fixture, _usuario_com_contato(fixture, cidade="São Paulo"))

        self.assertEqual(resultado.pendencias, ())
        self.assertTrue(resultado.aprovado)

    def test_cidade_ausente_gera_apenas_aviso(self) -> None:
        """Confirma que a falta da cidade é um aviso e não reprova.

        O teste revisa o estudante sem cidade e observa a pendência, a severidade
        e a aprovação. Ele existe para que a cidade seja uma recomendação.
        """
        fixture = obter_curriculo_exportacao_fixture()

        resultado = _revisar(fixture, _usuario_com_contato(fixture, cidade=None))

        self.assertEqual(
            resultado.pendencias,
            (
                PendenciaRevisao(
                    codigo="CIDADE_AUSENTE",
                    secao=SecaoRevisao.DADOS_PESSOAIS,
                    mensagem="Considere informar a cidade onde você mora.",
                    severidade=SeveridadePendencia.AVISO,
                ),
            ),
        )
        self.assertTrue(resultado.aprovado)

    def test_sem_linkedin_e_sem_lattes_gera_aviso_de_link(self) -> None:
        """Confirma que a ausência dos dois links gera um aviso único.

        O teste remove LinkedIn e Lattes e observa uma só pendência de aviso. Ele
        existe para que o aviso valha para o conjunto dos links profissionais.
        """
        fixture = obter_curriculo_exportacao_fixture()
        usuario = _usuario_com_contato(
            fixture, cidade="São Paulo", linkedin=None, curriculo_lattes=None
        )

        resultado = _revisar(fixture, usuario)

        self.assertEqual(
            [(p.codigo, p.severidade) for p in resultado.pendencias],
            [("LINK_PROFISSIONAL_AUSENTE", SeveridadePendencia.AVISO)],
        )
        self.assertTrue(resultado.aprovado)

    def test_basta_um_dos_links_para_nao_gerar_aviso(self) -> None:
        """Confirma que um único link profissional já satisfaz a recomendação.

        O teste mantém só o Lattes e depois só o LinkedIn. Ele existe para que o
        estudante não seja cobrado pelos dois.
        """
        fixture = obter_curriculo_exportacao_fixture()
        for ajuste in ({"linkedin": None}, {"curriculo_lattes": None}):
            with self.subTest(ajuste=ajuste):
                usuario = _usuario_com_contato(fixture, cidade="São Paulo", **ajuste)

                self.assertEqual(_revisar(fixture, usuario).pendencias, ())

    def test_avisos_de_contato_vem_ordenados_pelo_codigo(self) -> None:
        """Confirma a ordem dos avisos quando faltam a cidade e os links.

        O teste remove cidade e links e observa a sequência dos códigos. Ele
        existe para que a lista seja sempre a mesma.
        """
        fixture = obter_curriculo_exportacao_fixture()
        usuario = _usuario_com_contato(
            fixture, cidade=None, linkedin=None, curriculo_lattes=None
        )

        resultado = _revisar(fixture, usuario)

        self.assertEqual(
            [p.codigo for p in resultado.pendencias],
            ["CIDADE_AUSENTE", "LINK_PROFISSIONAL_AUSENTE"],
        )

    def test_sem_contato_gera_so_o_erro_de_contato(self) -> None:
        """Confirma que, sem contato, só o erro é gerado, sem os avisos de detalhe.

        O teste remove o contato e observa a pendência única de erro. Ele existe
        para que o estudante não receba avisos sobre campos de um contato que nem
        existe.
        """
        fixture = obter_curriculo_exportacao_fixture()

        resultado = _revisar(fixture, replace(fixture.usuario, dados_contato=None))

        self.assertEqual(
            [(p.codigo, p.severidade) for p in resultado.pendencias],
            [("CONTATO_AUSENTE", SeveridadePendencia.ERRO)],
        )
        self.assertFalse(resultado.aprovado)
