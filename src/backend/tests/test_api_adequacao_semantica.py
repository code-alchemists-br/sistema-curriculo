"""Testa o adapter HTTP da solicitação de adequação semântica."""

import unittest
from uuid import UUID, uuid4

from fastapi import HTTPException
from starlette.requests import Request

from backend.api.adequacao_semantica import (
    ReferenciaAdequacaoRequisicao,
    SolicitarAdequacaoCurriculoVagaRequisicao,
    criar_router,
)
from backend.application import (
    GeracaoPropostaAdequacaoIndisponivel,
    SolicitarAdequacaoCurriculoVagaEntrada,
)
from backend.domain import (
    CurriculoId,
    ExperienciaProfissionalId,
    ModeloCurriculo,
    PropostaAdequacaoCurriculoVaga,
    RecomendacaoModeloCurriculo,
    ReferenciaCurriculo,
    SugestaoAdequacao,
    TipoSugestaoAdequacao,
)


def _request(usuario_id: UUID | None) -> Request:
    """Cria uma requisição sintética com principal opcional no estado.

    A função monta apenas o escopo necessário pelo handler e instala o UUID
    quando o cenário representa uma sessão válida. Ela existe para testar a
    borda HTTP sem iniciar servidor ou middleware real.
    """
    requisicao = Request({"type": "http", "method": "POST", "path": "/"})
    if usuario_id is not None:
        requisicao.state.usuario_id = usuario_id
    return requisicao


class SolicitarAdequacaoSpy:
    """Registra a entrada recebida e devolve uma proposta definida pelo teste.

    O double implementa somente o contrato da Application e não chama rede nem
    persistência. Ele existe para verificar que a API deriva a identidade e não
    aceita conteúdo profissional livre no corpo.
    """

    def __init__(self, proposta: PropostaAdequacaoCurriculoVaga) -> None:
        """Armazena a proposta controlada e inicia o histórico de chamadas.

        O construtor recebe uma proposta já válida do domínio e mantém uma lista
        inicialmente vazia. Ele existe para tornar observável a tradução do
        handler sem acoplar o teste ao caso de uso concreto.
        """
        self.proposta = proposta
        self.entradas: list[SolicitarAdequacaoCurriculoVagaEntrada] = []

    async def executar(
        self, entrada: SolicitarAdequacaoCurriculoVagaEntrada
    ) -> PropostaAdequacaoCurriculoVaga:
        """Registra a entrada e devolve a proposta previamente configurada.

        O método simula a execução assíncrona sem aplicar regras adicionais. Ele
        existe para isolar a responsabilidade de conversão do adapter HTTP.
        """
        self.entradas.append(entrada)
        return self.proposta


class IndisponivelExecutor:
    """Simula indisponibilidade da geração depois que a entrada é aceita.

    O double sempre levanta a exceção interna de indisponibilidade. Ele existe
    para garantir que o adapter não exponha detalhes do provedor externo.
    """

    async def executar(
        self, entrada: SolicitarAdequacaoCurriculoVagaEntrada
    ) -> PropostaAdequacaoCurriculoVaga:
        """Interrompe a solicitação com a falha abstrata da Application.

        O método ignora a entrada porque o cenário exercita apenas a tradução
        da exceção. Ele existe para verificar a resposta HTTP 503 estável.
        """
        raise GeracaoPropostaAdequacaoIndisponivel("falha externa")


# Proveniência: decision-analysis prompts/backend/20261105-181751-adequacao-semantica-gpt-nano-v005.md#v005
class RecomendarModeloSpy:
    """Registra a entrada e devolve recomendação controlada pelo cenário.

    O double cumpre somente a porta consumida pelo router, sem chamar IA ou
    persistência. Ele existe para verificar a tradução HTTP do fluxo paralelo.
    """

    def __init__(self, recomendacao: RecomendacaoModeloCurriculo) -> None:
        """Guarda a recomendação válida e inicia o histórico de chamadas.

        O construtor recebe um value object já validado para manter o teste
        focado no adapter HTTP. Ele existe para tornar a entrada observável.
        """
        self.recomendacao = recomendacao
        self.entradas: list[SolicitarAdequacaoCurriculoVagaEntrada] = []

    async def executar(
        self, entrada: SolicitarAdequacaoCurriculoVagaEntrada
    ) -> RecomendacaoModeloCurriculo:
        """Registra a entrada traduzida e retorna a recomendação configurada.

        O método não aplica o modelo nem consulta serviços externos. Ele existe
        para isolar a responsabilidade do handler em um teste unitário.
        """
        self.entradas.append(entrada)
        return self.recomendacao


def _proposta(referencia: ReferenciaCurriculo) -> PropostaAdequacaoCurriculoVaga:
    """Constrói uma proposta mínima e revisável para os cenários HTTP.

    A função relaciona uma sugestão ao item escolhido e fornece metadados de
    política estáveis. Ela existe para os testes verificarem o presenter sem
    depender de geração real por IA.
    """
    return PropostaAdequacaoCurriculoVaga(
        curriculo_id=CurriculoId(uuid4()),
        modelo="gpt-5-nano",
        versao_politica="1",
        referencias_utilizadas=(referencia,),
        sugestoes=(
            SugestaoAdequacao(
                codigo="EXPERIENCIA_1",
                tipo=TipoSugestaoAdequacao.EXPERIENCIA,
                referencia_item=referencia,
                texto_sugerido="Desenvolvi APIs REST em Python.",
                justificativa="Evidencia experiência relevante.",
            ),
        ),
    )


class AdequacaoSemanticaApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução do contrato HTTP sem servidor ou provedor externo.

    Os cenários invocam diretamente o endpoint registrado no router com doubles
    de Application. A classe existe para preservar sessão, minimização do corpo
    e falhas públicas estáveis na fronteira de entrada.
    """

    async def test_deriva_usuario_da_sessao_e_apresenta_proposta_revisavel(
        self,
    ) -> None:
        """Converte rota e DTO no comando e devolve somente a proposta pública.

        O cenário usa referências de experiência e um campo extra ignorado,
        conferindo que a identidade vem do estado da requisição. Ele existe para
        impedir que o contrato aceite proprietário ou currículo livre no JSON.
        """
        usuario_id = uuid4()
        curriculo_id = uuid4()
        referencia_id = uuid4()
        referencia = ReferenciaCurriculo(ExperienciaProfissionalId(referencia_id))
        executor = SolicitarAdequacaoSpy(_proposta(referencia))
        endpoint = criar_router(executor).routes[0].endpoint
        requisicao = SolicitarAdequacaoCurriculoVagaRequisicao.model_validate(
            {
                "cargo_alvo": "Desenvolvedora Backend",
                "descricao_vaga": "Experiência com Python.",
                "referencias_selecionadas": [
                    {"tipo": "experiencia", "id": str(referencia_id)}
                ],
                "consentimento_explicito": True,
                "usuario_id": str(uuid4()),
            }
        )

        resposta = await endpoint(curriculo_id, requisicao, _request(usuario_id))

        self.assertEqual(len(executor.entradas), 1)
        entrada = executor.entradas[0]
        self.assertEqual(entrada.usuario_id.valor, usuario_id)
        self.assertEqual(entrada.curriculo_id.valor, curriculo_id)
        self.assertEqual(entrada.referencias_selecionadas, (referencia,))
        self.assertEqual(resposta.modelo, "gpt-5-nano")
        self.assertEqual(resposta.referencias_utilizadas[0].tipo, "experiencia")
        self.assertEqual(resposta.referencias_utilizadas[0].id, referencia_id)
        self.assertEqual(resposta.sugestoes[0].referencia_item.id, referencia_id)

    async def test_recusa_sem_principal_antes_de_executar_caso_de_uso(self) -> None:
        """Exige autenticação antes de converter ou executar a solicitação.

        O cenário não instala UUID no estado e espera 401 sem usar o spy. Ele
        existe para impedir que o cliente escolha ou omita a identidade do dono.
        """
        referencia = ReferenciaCurriculo(ExperienciaProfissionalId(uuid4()))
        executor = SolicitarAdequacaoSpy(_proposta(referencia))
        endpoint = criar_router(executor).routes[0].endpoint
        corpo = SolicitarAdequacaoCurriculoVagaRequisicao(
            cargo_alvo="Desenvolvedora",
            referencias_selecionadas=[
                ReferenciaAdequacaoRequisicao(
                    tipo="experiencia", id=referencia.item_id.valor
                )
            ],
            consentimento_explicito=True,
        )

        with self.assertRaises(HTTPException) as contexto:
            await endpoint(uuid4(), corpo, _request(None))

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    async def test_oculta_falha_do_gerador_como_indisponibilidade(self) -> None:
        """Traduz a falha interna do provedor para uma resposta 503 genérica.

        O cenário usa um executor que representa falha já abstraída na camada
        interna e confere o texto público. Ele existe para evitar vazamento de
        credenciais, payloads ou detalhes de transporte da OpenAI.
        """
        referencia_id = uuid4()
        endpoint = criar_router(IndisponivelExecutor()).routes[0].endpoint
        corpo = SolicitarAdequacaoCurriculoVagaRequisicao(
            cargo_alvo="Desenvolvedora",
            referencias_selecionadas=[
                ReferenciaAdequacaoRequisicao(tipo="experiencia", id=referencia_id)
            ],
            consentimento_explicito=True,
        )

        with self.assertRaises(HTTPException) as contexto:
            await endpoint(uuid4(), corpo, _request(uuid4()))

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Adequação semântica indisponível.")


# Proveniência: decision-analysis prompts/backend/20261105-181751-adequacao-semantica-gpt-nano-v005.md#v005
class RecomendacaoModeloCurriculoApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a borda HTTP da recomendação de modelo revisável.

    Os cenários chamam o endpoint registrado com doubles da Application. A
    classe existe para garantir uso do DTO comum sem introduzir aplicação de
    layout, servidor real ou provedor externo.
    """

    async def test_reutiliza_dto_e_apresenta_recomendacao_sem_aplica_la(self) -> None:
        """Deriva a sessão, reutiliza referências e expõe somente a sugestão.

        O cenário chama a segunda rota do router e verifica a entrada recebida.
        Ele existe para preservar consentimento prévio e decisão posterior na UI.
        """
        usuario_id = uuid4()
        curriculo_id = uuid4()
        referencia_id = uuid4()
        executor = RecomendarModeloSpy(
            RecomendacaoModeloCurriculo(
                modelo_recomendado=ModeloCurriculo.MODERNO,
                justificativa="Organiza melhor competências técnicas recentes.",
            )
        )
        endpoint = criar_router(None, executor).routes[1].endpoint
        corpo = SolicitarAdequacaoCurriculoVagaRequisicao(
            cargo_alvo="Desenvolvedora Backend",
            descricao_vaga="Experiência com Python.",
            referencias_selecionadas=[
                ReferenciaAdequacaoRequisicao(tipo="experiencia", id=referencia_id)
            ],
            consentimento_explicito=True,
        )

        resposta = await endpoint(curriculo_id, corpo, _request(usuario_id))

        self.assertEqual(len(executor.entradas), 1)
        self.assertEqual(executor.entradas[0].usuario_id.valor, usuario_id)
        self.assertEqual(executor.entradas[0].curriculo_id.valor, curriculo_id)
        self.assertTrue(executor.entradas[0].consentimento_explicito)
        self.assertEqual(resposta.modelo_recomendado, "moderno")
        self.assertEqual(
            resposta.justificativa,
            "Organiza melhor competências técnicas recentes.",
        )

    async def test_explica_indisponibilidade_quando_executor_nao_foi_composto(
        self,
    ) -> None:
        """Retorna 503 estável quando a capacidade de IA não foi injetada.

        O cenário mantém a aplicação inicializável sem credenciais de provedor.
        Ele existe para que ausência de composição não cause erro interno HTTP.
        """
        endpoint = criar_router(None).routes[1].endpoint
        corpo = SolicitarAdequacaoCurriculoVagaRequisicao(
            cargo_alvo="Desenvolvedora Backend",
            referencias_selecionadas=[],
            consentimento_explicito=True,
        )

        with self.assertRaises(HTTPException) as contexto:
            await endpoint(uuid4(), corpo, _request(uuid4()))

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(
            contexto.exception.detail,
            "Recomendação de modelo indisponível.",
        )
