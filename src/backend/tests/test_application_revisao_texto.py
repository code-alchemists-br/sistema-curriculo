"""Testa as regras do caso de uso de revisão de texto com IA."""

import unittest

from backend.application.revisao_texto import (
    AvaliacaoIa,
    CampoRevisavel,
    RevisarTexto,
    SituacaoTexto,
)


class RevisorFalso:
    """Substitui o provedor de IA por uma avaliação fixa em memória.

    O double guarda as chamadas recebidas e devolve a avaliação configurada,
    sem rede. Ele existe para testar as regras do caso de uso isoladamente.
    """

    def __init__(self, avaliacao: AvaliacaoIa) -> None:
        """Guarda a avaliação a devolver e prepara o histórico de chamadas.

        Existe para que cada teste escolha a resposta simulada da IA.
        """
        self.avaliacao = avaliacao
        self.chamadas: list[tuple] = []

    async def avaliar(self, campo, pergunta, texto, contexto) -> AvaliacaoIa:
        """Registra a chamada e devolve a avaliação configurada.

        Existe para que os testes confiram o que o caso de uso enviou à IA.
        """
        self.chamadas.append((campo, pergunta, texto, contexto))
        return self.avaliacao


class RevisarTextoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica as regras aplicadas pelo caso de uso ``RevisarTexto``.

    Usa um revisor falso para isolar o provedor de IA. Existe para garantir
    bloqueio de texto vazio, limite de sugestões e a decisão de manter o texto.
    """

    async def test_texto_vazio_e_invalido_sem_chamar_a_ia(self) -> None:
        """Recusa texto só com espaços sem consultar o provedor.

        Existe para não gastar chamadas de IA com campos vazios.
        """
        revisor = RevisorFalso(AvaliacaoIa(situacao=SituacaoTexto.VALIDO, motivo="", sugestoes=[]))

        resultado = await RevisarTexto(revisor).executar(CampoRevisavel.DESCRICAO_PROJETO, "   ")

        self.assertEqual(resultado.situacao, SituacaoTexto.INVALIDO)
        self.assertFalse(resultado.pode_manter_texto)
        self.assertEqual(revisor.chamadas, [])

    async def test_limpa_e_limita_as_sugestoes_a_tres(self) -> None:
        """Descarta sugestões vazias, tira espaços e mantém no máximo três.

        Existe para que a tela sempre receba sugestões utilizáveis.
        """
        revisor = RevisorFalso(
            AvaliacaoIa(
                situacao=SituacaoTexto.MELHORADO,
                motivo="Pode melhorar.",
                sugestoes=[" a ", "", "b", "c", "d"],
            )
        )

        resultado = await RevisarTexto(revisor).executar(
            CampoRevisavel.DESCRICAO_EXPERIENCIA, " texto ", "Pergunta?", {"cargo": "Dev"}
        )

        self.assertEqual(resultado.sugestoes, ["a", "b", "c"])
        self.assertTrue(resultado.pode_manter_texto)
        self.assertEqual(
            revisor.chamadas,
            [(CampoRevisavel.DESCRICAO_EXPERIENCIA, "Pergunta?", "texto", {"cargo": "Dev"})],
        )

    async def test_texto_invalido_nao_pode_ser_mantido(self) -> None:
        """Marca ``pode_manter_texto`` falso quando a IA julga o texto inválido.

        Existe para que o frontend bloqueie o avanço só nesse caso.
        """
        revisor = RevisorFalso(
            AvaliacaoIa(situacao=SituacaoTexto.INVALIDO, motivo="Vago.", sugestoes=["modelo"])
        )

        resultado = await RevisarTexto(revisor).executar(CampoRevisavel.OUTRO, "fazia coisas")

        self.assertEqual(resultado.situacao, SituacaoTexto.INVALIDO)
        self.assertFalse(resultado.pode_manter_texto)
        self.assertEqual(revisor.chamadas[0][3], {})


if __name__ == "__main__":
    unittest.main()
