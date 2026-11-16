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

    def __init__(
        self,
        parsed=None,
        erro: Exception | None = None,
        falhas_antes: list[Exception] | None = None,
    ) -> None:
        """Configura a resposta (``parsed``), o erro fixo e falhas iniciais.

        ``erro`` é lançado em toda chamada; ``falhas_antes`` são lançadas uma
        por chamada, na ordem, antes de a resposta ser devolvida. Existe para
        que cada teste simule um comportamento do Gemini, inclusive falhas
        passageiras seguidas de sucesso.
        """
        self.chamadas: list[dict] = []
        self._parsed = parsed
        self._erro = erro
        self._falhas_antes = list(falhas_antes or [])
        self.aio = SimpleNamespace(models=SimpleNamespace(generate_content=self._gerar))

    async def _gerar(self, **argumentos):
        """Registra a chamada e devolve a resposta ou lança o erro.

        Existe para substituir a chamada de rede do SDK.
        """
        self.chamadas.append(argumentos)
        if self._erro:
            raise self._erro
        if self._falhas_antes:
            raise self._falhas_antes.pop(0)
        return SimpleNamespace(parsed=self._parsed)


class EsperaFalsa:
    """Registra as pausas pedidas entre tentativas sem esperar de verdade.

    Existe para testar as novas tentativas sem deixar os testes lentos e sem
    depender do relógio.
    """

    def __init__(self) -> None:
        """Começa sem nenhuma pausa registrada.

        Existe para cada teste conferir só as pausas que provocou.
        """
        self.pausas: list[float] = []

    async def __call__(self, segundos: float) -> None:
        """Guarda a duração pedida e retorna na hora.

        Existe para substituir ``asyncio.sleep`` nos adaptadores.
        """
        self.pausas.append(segundos)


def _erro_api(codigo: int = 503) -> errors.APIError:
    """Cria um ``APIError`` do SDK como o devolvido em falhas do Gemini.

    Usa 503 (sobrecarga) por padrão. Existe para simular indisponibilidade ou
    outros erros do provedor.
    """
    return errors.APIError(codigo, {"error": {"message": "falha", "status": "UNAVAILABLE"}})


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
                    await RevisorTextoGemini(
                        "chave", cliente=cliente, esperar=EsperaFalsa()
                    ).avaliar(CampoRevisavel.OUTRO, None, "texto", {})

    async def test_tenta_de_novo_quando_o_gemini_esta_sobrecarregado(self) -> None:
        """Repete após 503 e 429 e devolve a revisão da tentativa que deu certo.

        Existe porque o Gemini recusa chamadas isoladas por sobrecarga, e a
        revisão do estudante não deve ser pulada por uma falha momentânea.
        """
        avaliacao = AvaliacaoIa(situacao=SituacaoTexto.VALIDO, motivo="Ok.", sugestoes=["a"])
        cliente = ClienteFalso(parsed=avaliacao, falhas_antes=[_erro_api(503), _erro_api(429)])
        espera = EsperaFalsa()

        resultado = await RevisorTextoGemini("chave", cliente=cliente, esperar=espera).avaliar(
            CampoRevisavel.OUTRO, None, "texto", {}
        )

        self.assertIs(resultado, avaliacao)
        self.assertEqual(len(cliente.chamadas), 3)
        self.assertEqual(espera.pausas, [0.5, 1.5])

    async def test_desiste_apos_tres_tentativas_e_nao_repete_erro_definitivo(self) -> None:
        """Faz no máximo 3 chamadas em falha passageira e 1 em erro definitivo.

        Um 503 persistente vira indisponível depois da terceira tentativa; um
        400 (pedido inválido) não é repetido. Existe para limitar o tempo de
        espera do estudante e não gastar cota com chamadas que não vão passar.
        """
        for codigo, chamadas_esperadas in ((503, 3), (400, 1)):
            with self.subTest(codigo=codigo):
                cliente = ClienteFalso(erro=_erro_api(codigo))
                with self.assertRaises(RevisorTextoIndisponivel):
                    await RevisorTextoGemini(
                        "chave", cliente=cliente, esperar=EsperaFalsa()
                    ).avaliar(CampoRevisavel.OUTRO, None, "texto", {})
                self.assertEqual(len(cliente.chamadas), chamadas_esperadas)


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
                    await RecomendadorModeloGemini(
                        "chave", cliente=cliente, esperar=EsperaFalsa()
                    ).recomendar([InformacaoPerfil("Formação", "ADS")])

    async def test_tenta_de_novo_quando_o_gemini_esta_sobrecarregado(self) -> None:
        """Repete após um 503 e devolve a recomendação da segunda tentativa.

        Existe para que a recomendação não falhe por sobrecarga momentânea.
        """
        recomendacao = RecomendacaoModelo(
            modelo=ModeloCurriculo.MODERNO, motivo="Tecnologia.", alternativa=None
        )
        cliente = ClienteFalso(parsed=recomendacao, falhas_antes=[_erro_api(503)])

        resultado = await RecomendadorModeloGemini(
            "chave", cliente=cliente, esperar=EsperaFalsa()
        ).recomendar([InformacaoPerfil("Formação", "ADS")])

        self.assertIs(resultado, recomendacao)
        self.assertEqual(len(cliente.chamadas), 2)


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
