"""Testa as regras de domínio da adequação semântica de currículo a vaga."""

import unittest
from uuid import uuid4

from backend.domain import (
    AcaoAdequacaoSemantica,
    CompetenciaId,
    CurriculoId,
    ExperienciaProfissionalId,
    ItemSelecionadoAdequacao,
    ReferenciaCurriculo,
    RegraDeDominioViolada,
    SolicitacaoAdequacaoCurriculoVaga,
    SugestaoAdequacao,
    TipoSugestaoAdequacao,
)


def _item_experiencia() -> ItemSelecionadoAdequacao:
    """Cria uma experiência selecionada válida para os cenários de teste.

    A função monta uma referência tipada e um conteúdo profissional mínimo. Ela
    existe para que cada teste altere somente a invariante que deseja observar.
    """
    return ItemSelecionadoAdequacao(
        referencia=ReferenciaCurriculo(ExperienciaProfissionalId(uuid4())),
        conteudo="Desenvolvimento de interfaces em React e integração com APIs.",
    )


def _solicitacao(**alteracoes) -> SolicitacaoAdequacaoCurriculoVaga:
    """Cria uma solicitação consentida e válida, aceitando alterações pontuais.

    A função concentra dados profissionais fictícios e sobrescreve apenas os
    campos indicados. Ela existe para manter cada cenário de teste pequeno e
    explícito sobre a regra que está exercitando.
    """
    campos = {
        "curriculo_id": CurriculoId(uuid4()),
        "cargo_alvo": "Desenvolvedora Frontend",
        "descricao_vaga": "Buscamos experiência com React e APIs REST.",
        "itens_selecionados": (_item_experiencia(),),
        "consentimento_explicito": True,
    }
    campos.update(alteracoes)
    return SolicitacaoAdequacaoCurriculoVaga(**campos)


class SolicitacaoAdequacaoCurriculoVagaTestCase(unittest.TestCase):
    """Verifica consentimento, seleção e revisão de propostas da adequação.

    Os cenários usam somente value objects e não acessam SDK, rede, JSON ou
    persistência. A classe existe para impedir envio não autorizado e sugestões
    sobre conteúdo não selecionado antes das camadas externas serem adicionadas.
    """

    def test_cria_solicitacao_consentida_para_a_vaga_com_itens_rastreaveis(self) -> None:
        """Mantém a ação, a seleção e a vaga informada na intenção válida.

        O cenário cria a solicitação padrão e confere os valores derivados. Ele
        existe para garantir que o domínio represente a intenção do estudante
        antes de qualquer gerador externo ser chamado.
        """
        solicitacao = _solicitacao()

        self.assertEqual(
            solicitacao.acao, AcaoAdequacaoSemantica.ADEQUAR_CURRICULO_VAGA
        )
        self.assertEqual(len(solicitacao.referencias_selecionadas), 1)
        self.assertEqual(solicitacao.cargo_alvo, "Desenvolvedora Frontend")

    def test_recusa_sem_consentimento_sem_selecao_ou_referencia_repetida(self) -> None:
        """Impede intenções que violam consentimento ou controle da seleção.

        O cenário tenta construir três pedidos inválidos. Ele existe para que a
        futura Application não consiga alcançar o provedor sem autorização e
        sem um conjunto profissional inequívoco de itens.
        """
        item = _item_experiencia()
        for alteracoes in (
            {"consentimento_explicito": False},
            {"itens_selecionados": ()},
            {"itens_selecionados": (item, item)},
        ):
            with self.subTest(alteracoes=alteracoes):
                with self.assertRaises(RegraDeDominioViolada):
                    _solicitacao(**alteracoes)

    def test_cria_proposta_sem_mutar_solicitacao_e_registra_itens_utilizados(self) -> None:
        """Cria uma proposta revisável ligada exclusivamente ao item autorizado.

        O cenário envia uma sugestão de experiência para a referência escolhida
        e confere a proposta resultante. Ele existe para garantir que o retorno
        do gerador seja apenas uma proposta, não uma alteração do currículo ou
        da seleção original.
        """
        solicitacao = _solicitacao()
        referencia = solicitacao.itens_selecionados[0].referencia
        sugestao = SugestaoAdequacao(
            codigo="EXPERIENCIA_1",
            tipo=TipoSugestaoAdequacao.EXPERIENCIA,
            referencia_item=referencia,
            texto_sugerido="Desenvolvi interfaces React integradas a APIs REST.",
            justificativa="Destaca as competências pedidas pela vaga.",
        )

        proposta = solicitacao.criar_proposta(
            modelo="gpt-5.4-nano",
            versao_politica="1",
            sugestoes=(sugestao,),
        )

        self.assertEqual(proposta.referencias_utilizadas, (referencia,))
        self.assertEqual(proposta.sugestoes, (sugestao,))
        self.assertEqual(solicitacao.itens_selecionados[0].referencia, referencia)

    def test_recusa_proposta_para_item_nao_autorizado_e_codigos_duplicados(self) -> None:
        """Bloqueia sugestões fora da seleção e propostas ambíguas.

        O cenário aponta uma sugestão para competência não selecionada e depois
        repete um código em duas sugestões globais. Ele existe para preservar a
        autorização granular e a revisão individual pelo estudante.
        """
        solicitacao = _solicitacao()
        sugestao_nao_autorizada = SugestaoAdequacao(
            codigo="COMPETENCIA_1",
            tipo=TipoSugestaoAdequacao.COMPETENCIA,
            referencia_item=ReferenciaCurriculo(CompetenciaId(uuid4())),
            texto_sugerido="React avançado",
            justificativa="Palavra-chave relevante para a vaga.",
        )

        with self.assertRaises(RegraDeDominioViolada):
            solicitacao.criar_proposta(
                modelo="gpt-5.4-nano",
                versao_politica="1",
                sugestoes=(sugestao_nao_autorizada,),
            )

        sugestao_global = SugestaoAdequacao(
            codigo="PALAVRAS_CHAVE",
            tipo=TipoSugestaoAdequacao.PALAVRAS_CHAVE,
            referencia_item=None,
            texto_sugerido="React, APIs REST",
            justificativa="Termos encontrados na vaga.",
        )
        with self.assertRaises(RegraDeDominioViolada):
            solicitacao.criar_proposta(
                modelo="gpt-5.4-nano",
                versao_politica="1",
                sugestoes=(sugestao_global, sugestao_global),
            )
