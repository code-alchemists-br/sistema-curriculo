"""Testa unitariamente a rota HTTP de revisão de campos obrigatórios."""

import unittest
from uuid import uuid4

from fastapi import HTTPException

from backend.api.factory import create_app
from backend.api.revisao_versao_curriculo import (
    RevisaoVersaoCurriculoResposta,
    criar_router,
)
from backend.application import CurriculoNaoEncontrado, RevisarVersaoCurriculoEntrada
from backend.domain import (
    CurriculoId,
    PendenciaRevisao,
    ResultadoRevisao,
    SecaoRevisao,
    SeveridadePendencia,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001

CAMINHO_REVISAO = "/estudantes/{usuario_id}/curriculos/{curriculo_id}/revisao"

PENDENCIA_ERRO = PendenciaRevisao(
    codigo="CONTATO_AUSENTE",
    secao=SecaoRevisao.DADOS_PESSOAIS,
    mensagem="Informe o endereço e ao menos um telefone de contato.",
    severidade=SeveridadePendencia.ERRO,
)
PENDENCIA_AVISO = PendenciaRevisao(
    codigo="PROJETO_AUSENTE",
    secao=SecaoRevisao.PROJETOS_ACADEMICOS,
    mensagem="Considere incluir um projeto acadêmico na versão.",
    severidade=SeveridadePendencia.AVISO,
)


class RevisaoExecutorDouble:
    """Substitui o caso de uso de revisão e registra as entradas recebidas.

    O double devolve o resultado ou levanta o erro pré-configurado, sem tocar
    portas, banco ou domínio de verdade. Ele existe para testar a tradução HTTP
    da rota isoladamente da orquestração da Application.
    """

    def __init__(
        self,
        resultado: ResultadoRevisao | None = None,
        erro: Exception | None = None,
    ) -> None:
        """Guarda o comportamento configurado e inicia o histórico de chamadas.

        O construtor não acessa recursos externos. Ele existe para permitir que
        cada teste configure sucesso ou falha de forma explícita.
        """
        self._resultado = resultado
        self._erro = erro
        self.entradas: list[RevisarVersaoCurriculoEntrada] = []

    async def executar(self, entrada: RevisarVersaoCurriculoEntrada) -> ResultadoRevisao:
        """Registra a entrada recebida e devolve o resultado ou levanta o erro.

        O método aguarda de forma trivial, sem I/O real. Ele existe para tornar
        observável o que o handler HTTP enviou ao caso de uso.
        """
        self.entradas.append(entrada)
        if self._erro is not None:
            raise self._erro
        if self._resultado is None:
            raise AssertionError("O double não recebeu resultado nem erro configurado.")
        return self._resultado


def _rota(executor: RevisaoExecutorDouble | None):
    """Localiza a rota GET de revisão para inspeção e chamada direta em teste.

    A função cria o router com o executor dado e varre suas rotas por caminho e
    método HTTP, devolvendo o objeto da rota, que expõe o endpoint e a
    configuração declarada. Ela existe para exercitar o handler sem iniciar
    servidor ASGI ou cliente HTTP real.
    """
    for rota in criar_router(executor).routes:
        if rota.path == CAMINHO_REVISAO and "GET" in rota.methods:
            return rota
    raise AssertionError(f"Rota GET {CAMINHO_REVISAO} não encontrada.")


class RevisaoVersaoCurriculoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP da revisão de campos obrigatórios pela rota GET.

    A classe substitui o caso de uso por um double e observa o que a rota envia
    e devolve. Ela existe para testar a unidade de interface isoladamente da
    Application e da infraestrutura.
    """

    async def test_devolve_o_veredito_e_as_pendencias_e_envia_a_entrada_correta(self) -> None:
        """Confirma o veredito, as pendências em texto e a entrada enviada.

        O teste configura um resultado com um erro e um aviso, chama o handler e
        compara a resposta pública e a entrada registrada. Ele existe para
        proteger o contrato da revisão.
        """
        usuario_id, curriculo_id = uuid4(), uuid4()
        executor = RevisaoExecutorDouble(
            resultado=ResultadoRevisao(pendencias=(PENDENCIA_ERRO, PENDENCIA_AVISO))
        )
        revisar = _rota(executor).endpoint

        resposta = await revisar(usuario_id=usuario_id, curriculo_id=curriculo_id)

        self.assertIsInstance(resposta, RevisaoVersaoCurriculoResposta)
        self.assertFalse(resposta.aprovado)
        self.assertEqual(
            [
                (p.codigo, p.secao, p.mensagem, p.severidade)
                for p in resposta.pendencias
            ],
            [
                (
                    "CONTATO_AUSENTE",
                    "dados-pessoais",
                    "Informe o endereço e ao menos um telefone de contato.",
                    "erro",
                ),
                (
                    "PROJETO_AUSENTE",
                    "projetos-academicos",
                    "Considere incluir um projeto acadêmico na versão.",
                    "aviso",
                ),
            ],
        )
        self.assertEqual(
            executor.entradas,
            [RevisarVersaoCurriculoEntrada(UsuarioId(usuario_id), CurriculoId(curriculo_id))],
        )

    async def test_aviso_nao_reprova_e_curriculo_completo_devolve_lista_vazia(self) -> None:
        """Confirma que só aviso aprova e que sem pendências a lista vem vazia.

        O teste cobre um resultado só com aviso e outro sem pendências e observa
        o veredito e a lista de cada um. Ele existe para proteger a diferença
        entre erro e aviso na resposta.
        """
        so_aviso = _rota(
            RevisaoExecutorDouble(resultado=ResultadoRevisao(pendencias=(PENDENCIA_AVISO,)))
        ).endpoint
        completo = _rota(
            RevisaoExecutorDouble(resultado=ResultadoRevisao(pendencias=()))
        ).endpoint

        resposta_aviso = await so_aviso(usuario_id=uuid4(), curriculo_id=uuid4())
        resposta_completo = await completo(usuario_id=uuid4(), curriculo_id=uuid4())

        self.assertTrue(resposta_aviso.aprovado)
        self.assertEqual([p.codigo for p in resposta_aviso.pendencias], ["PROJETO_AUSENTE"])
        self.assertTrue(resposta_completo.aprovado)
        self.assertEqual(resposta_completo.pendencias, [])

    async def test_declara_modelo_de_resposta_publico(self) -> None:
        """Confirma o modelo de resposta declarado na rota registrada.

        O teste inspeciona a configuração da rota, já que a chamada direta ao
        handler não passa pela camada que aplica o modelo. Ele existe para
        proteger o contrato HTTP da revisão.
        """
        rota = _rota(None)

        self.assertIs(rota.response_model, RevisaoVersaoCurriculoResposta)

    async def test_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum caso de uso de revisão foi injetado.

        O teste chama o handler sem executor e observa a indisponibilidade
        explícita antes de qualquer outra decisão.
        """
        revisar = _rota(None).endpoint

        with self.assertRaises(HTTPException) as contexto:
            await revisar(usuario_id=uuid4(), curriculo_id=uuid4())

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_ausencia_ou_propriedade_alheia_vira_404(self) -> None:
        """Confirma 404 quando o caso de uso sinaliza versão não encontrada.

        O teste configura o double para a falha de não encontrado e observa a
        tradução HTTP preservando a mensagem. Ele existe para proteger a negação
        sem revelar a diferença entre ausência e propriedade alheia.
        """
        erro = CurriculoNaoEncontrado("Versão de currículo não encontrada.")
        revisar = _rota(RevisaoExecutorDouble(erro=erro)).endpoint

        with self.assertRaises(HTTPException) as contexto:
            await revisar(usuario_id=uuid4(), curriculo_id=uuid4())

        self.assertEqual(contexto.exception.status_code, 404)
        self.assertEqual(contexto.exception.detail, str(erro))

    async def test_fabrica_registra_a_revisao_no_caminho_da_versao(self) -> None:
        """Confirma que a fábrica expõe o GET de revisão no caminho esperado.

        O teste monta a aplicação com o executor de revisão e lê, no esquema
        OpenAPI, os métodos documentados para o caminho, sem iniciar servidor. Ele
        existe para garantir que o novo router esteja ligado na fábrica.
        """
        app = create_app(revisar_versao_curriculo=RevisaoExecutorDouble())

        metodos = set(app.openapi()["paths"][CAMINHO_REVISAO])

        self.assertIn("get", metodos)