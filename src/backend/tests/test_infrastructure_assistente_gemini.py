"""Testa os adaptadores do Gemini sem chamar a API real."""

import unittest
from types import SimpleNamespace

from google.genai import errors

from backend.application.recomendacao_modelo import (
    InformacaoPerfil,
    RecomendacaoModelo,
    RecomendadorModeloIndisponivel,
)
from backend.application.revisao_texto import (
    AvaliacaoIa,
    CampoRevisavel,
    RevisorTextoIndisponivel,
    SituacaoTexto,
)
from backend.domain.modelo_curriculo import ModeloCurriculo
from backend.infrastructure.integrations.assistente_gemini import (
    INSTRUCAO_RECOMENDACAO,
    INSTRUCAO_REVISAO,
    RecomendadorModeloAusente,
    RecomendadorModeloGemini,
    RevisorTextoAusente,
    RevisorTextoGemini,
)


class ClienteFalso:
    """Imita ``client.aio.models.generate_content`` do SDK google-genai.

    Guarda os argumentos de cada chamada e devolve a resposta configurada ou
    lança o erro configurado. Existe para testar os adaptadores sem rede.
    """

    def __init__(self, parsed=None, erro: Exception | None = None) -> None:
        """Configura a resposta (``parsed``) ou o erro e o histórico de chamadas.

        Existe para que cada teste simule um comportamento do Gemini.
        """
        self.chamadas: list[dict] = []
        self._parsed = parsed
        self._erro = erro
        self.aio = SimpleNamespace(models=SimpleNamespace(generate_content=self._gerar))

    async def _gerar(self, **argumentos):
        """Registra a chamada e devolve a resposta ou lança o erro.

        Existe para substituir a chamada de rede do SDK.
        """
        self.chamadas.append(argumentos)
        if self._erro:
            raise self._erro
        return SimpleNamespace(parsed=self._parsed)


def _erro_api() -> errors.APIError:
    """Cria um ``APIError`` do SDK como o devolvido em falhas do Gemini.

    Existe para simular indisponibilidade do provedor.
    """
    return errors.APIError(503, {"error": {"message": "indisponível", "status": "UNAVAILABLE"}})


class RevisorTextoGeminiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a montagem da chamada de revisão e o tratamento de falhas.

    Existe para garantir prompt, esquema JSON e tradução de erros do provedor.
    """

    async def test_monta_a_mensagem_e_pede_saida_tipada(self) -> None:
        """Envia campo, pergunta, contexto e texto com o esquema ``AvaliacaoIa``.

        Existe para proteger o formato combinado com as instruções de revisão.
        """
        avaliacao = AvaliacaoIa(situacao=SituacaoTexto.VALIDO, motivo="Ok.", sugestoes=["a"])
        cliente = ClienteFalso(parsed=avaliacao)

        resultado = await RevisorTextoGemini("chave", "modelo-x", cliente=cliente).avaliar(
            CampoRevisavel.DESCRICAO_EXPERIENCIA, "O que fazia?", "Fiz APIs.", {"cargo": "Dev"}
        )

        self.assertIs(resultado, avaliacao)
        chamada = cliente.chamadas[0]
        self.assertEqual(chamada["model"], "modelo-x")
        self.assertEqual(
            chamada["contents"],
            "Campo: descricao_experiencia\nPergunta: O que fazia?\n"
            "Contexto - cargo: Dev\nTexto do estudante: Fiz APIs.",
        )
        self.assertEqual(chamada["config"].system_instruction, INSTRUCAO_REVISAO)
        self.assertIs(chamada["config"].response_schema, AvaliacaoIa)

    async def test_falha_ou_resposta_invalida_viram_indisponivel(self) -> None:
        """Traduz erro do SDK e resposta fora do esquema em ``RevisorTextoIndisponivel``.

        Existe para que a API responda 503 nesses casos.
        """
        for cliente in (ClienteFalso(erro=_erro_api()), ClienteFalso(parsed=None)):
            with self.subTest(cliente=cliente):
                with self.assertRaises(RevisorTextoIndisponivel):
                    await RevisorTextoGemini("chave", cliente=cliente).avaliar(
                        CampoRevisavel.OUTRO, None, "texto", {}
                    )


class RecomendadorModeloGeminiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a montagem da chamada de recomendação e o tratamento de falhas.

    Existe para garantir prompt, esquema JSON e tradução de erros do provedor.
    """

    async def test_envia_perfil_em_linhas_e_pede_saida_tipada(self) -> None:
        """Envia uma linha por informação com o esquema ``RecomendacaoModelo``.

        Existe para proteger o formato combinado com as instruções.
        """
        recomendacao = RecomendacaoModelo(
            modelo=ModeloCurriculo.ACADEMICO, motivo="Pesquisa.", alternativa=None
        )
        cliente = ClienteFalso(parsed=recomendacao)

        resultado = await RecomendadorModeloGemini("chave", cliente=cliente).recomendar(
            [InformacaoPerfil("Formação", "Mestrado"), InformacaoPerfil("Objetivo", "Pesquisa")]
        )

        self.assertIs(resultado, recomendacao)
        chamada = cliente.chamadas[0]
        self.assertEqual(chamada["contents"], "Formação: Mestrado\nObjetivo: Pesquisa")
        self.assertEqual(chamada["config"].system_instruction, INSTRUCAO_RECOMENDACAO)
        self.assertIs(chamada["config"].response_schema, RecomendacaoModelo)

    async def test_falha_vira_indisponivel(self) -> None:
        """Traduz erro do SDK e resposta inválida em ``RecomendadorModeloIndisponivel``.

        Existe para que a API responda 503 nesses casos.
        """
        for cliente in (ClienteFalso(erro=_erro_api()), ClienteFalso(parsed="texto solto")):
            with self.subTest(cliente=cliente):
                with self.assertRaises(RecomendadorModeloIndisponivel):
                    await RecomendadorModeloGemini("chave", cliente=cliente).recomendar(
                        [InformacaoPerfil("Formação", "ADS")]
                    )


class AdaptadoresAusentesTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica os adaptadores usados quando não há chave do Gemini.

    Existe para garantir que a ausência de IA vire indisponibilidade clara.
    """

    async def test_ausentes_sempre_indisponiveis(self) -> None:
        """Lançam as exceções de indisponível sem chamar nenhum serviço.

        Existe para que a API suba e responda 503 sem a chave.
        """
        with self.assertRaises(RevisorTextoIndisponivel):
            await RevisorTextoAusente().avaliar(CampoRevisavel.OUTRO, None, "x", {})
        with self.assertRaises(RecomendadorModeloIndisponivel):
            await RecomendadorModeloAusente().recomendar([])


if __name__ == "__main__":
    unittest.main()
