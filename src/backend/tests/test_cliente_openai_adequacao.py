"""Testa unitariamente o adaptador da OpenAI para adequação semântica."""

import json
import unittest
from uuid import uuid4

from backend.application.adequacao_semantica import ContextoAdequacaoCurriculoVaga
from backend.application.politica_limites_contexto_ia import LimitesContextoIa
from backend.domain import (
    CurriculoId,
    ExperienciaProfissionalId,
    ItemSelecionadoAdequacao,
    ReferenciaCurriculo,
)
from backend.infrastructure.integrations.cliente_openai_adequacao import (
    ClienteOpenAiAdequacaoHttp,
    ClienteOpenAiRecomendacaoModeloHttp,
    RespostaOpenAiAdequacaoInvalida,
    mapear_resposta_openai_para_recomendacao,
    mapear_resposta_openai_para_sugestoes,
    montar_requisicao_openai,
    montar_requisicao_openai_recomendacao,
)

# Proveniência: decision-analysis prompts/backend/20261020-163820-adequacao-semantica-gpt-nano-v001.md#v001


def _contexto() -> ContextoAdequacaoCurriculoVaga:
    """Cria um contexto mínimo autorizado para os cenários do adaptador.

    A função usa referências e limites tipados em memória. Ela existe para que
    os testes controlem o payload sem consultar Application, rede ou banco.
    """
    referencia = ReferenciaCurriculo(ExperienciaProfissionalId(uuid4()))
    return ContextoAdequacaoCurriculoVaga(
        curriculo_id=CurriculoId(uuid4()),
        cargo_alvo="Desenvolvedora Backend",
        descricao_vaga="Experiência com Python e APIs.",
        itens_selecionados=(
            ItemSelecionadoAdequacao(
                referencia=referencia,
                conteudo="Empresa: Tech\nCargo: Desenvolvedora\nDescrição: APIs REST",
            ),
        ),
        modelo="gpt-5-nano",
        versao_politica="1",
        limites=LimitesContextoIa(
            limites_campos={"cargo": 120}, orcamento_total_caracteres=1000
        ),
    )


def _envelope_sucesso(referencia: ReferenciaCurriculo) -> bytes:
    """Monta uma resposta Responses com uma sugestão referenciada válida.

    A função serializa a forma externa esperada pelo adaptador. Ela existe para
    testar desserialização sem qualquer chamada real ao provedor.
    """
    return json.dumps(
        {
            "output": [
                {
                    "type": "message",
                    "content": [
                        {
                            "type": "output_text",
                            "text": json.dumps(
                                {
                                    "sugestoes": [
                                        {
                                            "codigo": "EXPERIENCIA_1",
                                            "tipo": "experiencia",
                                            "referencia_item": {
                                                "tipo": "experiencia",
                                                "id": str(referencia.item_id.valor),
                                            },
                                            "texto_sugerido": "Desenvolvi APIs REST em Python.",
                                            "justificativa": "Evidencia a experiência solicitada.",
                                        }
                                    ]
                                },
                                ensure_ascii=False,
                            ),
                        }
                    ],
                }
            ]
        },
        ensure_ascii=False,
    ).encode()


# Proveniência: decision-analysis prompts/backend/20261105-181751-adequacao-semantica-gpt-nano-v005.md#v005
def _envelope_recomendacao() -> bytes:
    """Monta uma resposta Responses com recomendação de modelo válida.

    A função serializa a forma mínima aceita pelo gateway de recomendação. Ela
    existe para testar a desserialização sem rede, SDK ou credencial real.
    """
    return json.dumps(
        {
            "output": [
                {
                    "type": "message",
                    "content": [
                        {
                            "type": "output_text",
                            "text": json.dumps(
                                {
                                    "modelo_recomendado": "moderno",
                                    "justificativa": "Destaca competências técnicas recentes.",
                                },
                                ensure_ascii=False,
                            ),
                        }
                    ],
                }
            ]
        },
        ensure_ascii=False,
    ).encode()


class ClienteOpenAiAdequacaoHttpTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica serialização, delegação HTTP e mapeamento sem rede real.

    Os testes substituem o executor HTTP por funções locais e exercitam somente
    o adaptador. A classe existe para preservar a fronteira externa sem iniciar
    servidor, SDK, banco ou processo adicional.
    """

    def test_monta_payload_sem_identidade_do_curriculo_ou_campos_vedados(self) -> None:
        """Mantém no payload somente vaga e conteúdo profissional autorizado.

        O cenário inspeciona a mensagem de usuário e o schema estruturado. Ele
        existe para impedir que metadados internos ou dados pessoais sejam
        introduzidos na serialização do adaptador.
        """
        contexto = _contexto()

        requisicao = montar_requisicao_openai(contexto)

        dados_usuario = json.loads(requisicao["input"][1]["content"][0]["text"])
        self.assertEqual(requisicao["model"], "gpt-5-nano")
        self.assertNotIn("curriculo_id", dados_usuario)
        self.assertNotIn("telefone", dados_usuario)
        self.assertEqual(
            dados_usuario["itens_selecionados"][0]["referencia"]["tipo"], "experiencia"
        )
        self.assertEqual(requisicao["text"]["format"]["type"], "json_schema")

    async def test_envia_corpo_para_executor_e_mapeia_sugestao(self) -> None:
        """Traduz o contexto em POST lógico e devolve sugestão de domínio.

        O cenário usa executor em memória para inspecionar URL, corpo e chave,
        recebendo um envelope sintético. Ele existe para testar delegação sem
        abrir conexão ou usar credencial real.
        """
        contexto = _contexto()
        chamadas: list[tuple[str, bytes, str]] = []

        def executor(url: str, corpo: bytes, chave: str) -> bytes:
            """Registra a requisição e devolve resposta Responses sintética.

            A função atua como transporte falso sem rede. Ela existe para tornar
            observável a tradução feita pelo cliente HTTP.
            """
            chamadas.append((url, corpo, chave))
            return _envelope_sucesso(contexto.itens_selecionados[0].referencia)

        cliente = ClienteOpenAiAdequacaoHttp(
            api_key="chave-de-teste",
            url_responses="https://openai.test/v1/responses",
            executor_http=executor,
        )

        sugestoes = await cliente.gerar(contexto)

        self.assertEqual(len(chamadas), 1)
        self.assertEqual(chamadas[0][0], "https://openai.test/v1/responses")
        self.assertEqual(chamadas[0][2], "chave-de-teste")
        self.assertEqual(
            sugestoes[0].referencia_item, contexto.itens_selecionados[0].referencia
        )
        self.assertEqual(sugestoes[0].codigo, "EXPERIENCIA_1")

    def test_recusa_envelope_sem_texto_estruturado(self) -> None:
        """Recusa resposta do provedor que não contém texto de saída válido.

        O cenário fornece envelope sem conteúdo final. Ele existe para impedir
        que uma estrutura externa incompleta atravesse o adaptador como proposta.
        """
        with self.assertRaises(RespostaOpenAiAdequacaoInvalida):
            mapear_resposta_openai_para_sugestoes({"output": []})


# Proveniência: decision-analysis prompts/backend/20261105-181751-adequacao-semantica-gpt-nano-v005.md#v005
class ClienteOpenAiRecomendacaoModeloHttpTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o gateway de recomendação sem iniciar conexão externa.

    Os cenários usam transporte em memória e o mesmo contexto da adequação. A
    classe existe para preservar minimização de dados e validação do catálogo.
    """

    def test_monta_payload_sem_identificador_de_curriculo_ou_referencias(self) -> None:
        """Envia apenas vaga e conteúdo profissional autorizado ao provedor.

        O cenário inspeciona dados de usuário e schema com enum do catálogo. Ele
        existe para impedir que a recomendação transporte IDs internos ou aceite
        modelos que não pertencem ao domínio.
        """
        requisicao = montar_requisicao_openai_recomendacao(_contexto())

        dados_usuario = json.loads(requisicao["input"][1]["content"][0]["text"])

        self.assertNotIn("curriculo_id", dados_usuario)
        self.assertEqual(
            dados_usuario["itens_selecionados"][0],
            {"conteudo": "Empresa: Tech\nCargo: Desenvolvedora\nDescrição: APIs REST"},
        )
        self.assertNotIn("referencia", dados_usuario["itens_selecionados"][0])
        self.assertIn(
            "moderno",
            requisicao["text"]["format"]["schema"]["properties"]["modelo_recomendado"][
                "enum"
            ],
        )

    async def test_envia_corpo_e_devolve_recomendacao_validada(self) -> None:
        """Traduz o contexto e mapeia a resposta no value object de domínio.

        O cenário captura URL, corpo e chave no transporte falso. Ele existe
        para garantir a implementação concreta da porta sem acesso à rede.
        """
        chamadas: list[tuple[str, bytes, str]] = []

        def executor(url: str, corpo: bytes, chave: str) -> bytes:
            """Registra a chamada externa e devolve envelope sintético.

            A função substitui o transporte bloqueante durante o teste. Ela
            existe para tornar a serialização e a autenticação observáveis.
            """
            chamadas.append((url, corpo, chave))
            return _envelope_recomendacao()

        cliente = ClienteOpenAiRecomendacaoModeloHttp(
            api_key="chave-de-teste",
            url_responses="https://openai.test/v1/responses",
            executor_http=executor,
        )

        recomendacao = await cliente.gerar(_contexto())

        self.assertEqual(len(chamadas), 1)
        self.assertEqual(chamadas[0][0], "https://openai.test/v1/responses")
        self.assertEqual(chamadas[0][2], "chave-de-teste")
        self.assertEqual(recomendacao.modelo_recomendado.value, "moderno")
        self.assertEqual(
            recomendacao.justificativa,
            "Destaca competências técnicas recentes.",
        )

    def test_recusa_modelo_fora_do_catalogo(self) -> None:
        """Recusa JSON estruturado cujo modelo não pertence ao domínio.

        O cenário usa um envelope formalmente completo, mas com enum inválido.
        Ele existe para impedir que texto inventado pelo provedor chegue à UI.
        """
        resposta = {
            "output": [
                {
                    "content": [
                        {
                            "type": "output_text",
                            "text": json.dumps(
                                {
                                    "modelo_recomendado": "inexistente",
                                    "justificativa": "Teste.",
                                }
                            ),
                        }
                    ]
                }
            ]
        }

        with self.assertRaises(RespostaOpenAiAdequacaoInvalida):
            mapear_resposta_openai_para_recomendacao(resposta)
