"""Testa unitariamente a rota HTTP de listagem de versões de currículo."""

import unittest
from uuid import uuid4

from fastapi import HTTPException

from backend.api.factory import create_app
from backend.api.listagem_versoes_curriculo import (
    ListagemVersoesCurriculoResposta,
    criar_router,
)
from backend.application import ListarVersoesCurriculoEntrada
from backend.domain import (
    Curriculo,
    CurriculoId,
    IdiomaId,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001

CAMINHO_LISTAGEM = "/estudantes/{usuario_id}/curriculos"


class ListagemExecutorDouble:
    """Substitui o caso de uso de listagem e registra as entradas recebidas.

    O double devolve as versões pré-configuradas, sem tocar portas, banco ou
    domínio de verdade. Ele existe para testar a tradução HTTP da rota
    isoladamente da orquestração da Application.
    """

    def __init__(self, resultado: tuple[Curriculo, ...] = ()) -> None:
        """Guarda o resultado configurado e inicia o histórico de chamadas.

        O construtor não acessa recursos externos. Ele existe para permitir que
        cada teste configure as versões que o caso de uso devolveria.
        """
        self._resultado = resultado
        self.entradas: list[ListarVersoesCurriculoEntrada] = []

    async def executar(self, entrada: ListarVersoesCurriculoEntrada) -> tuple[Curriculo, ...]:
        """Registra a entrada recebida e devolve o resultado configurado.

        O método aguarda de forma trivial, sem I/O real. Ele existe para tornar
        observável o que o handler HTTP enviou ao caso de uso.
        """
        self.entradas.append(entrada)
        return self._resultado


def _rota(executor: ListagemExecutorDouble | None):
    """Localiza a rota GET de listagem para inspeção e chamada direta em teste.

    A função cria o router com o executor dado e varre suas rotas por caminho e
    método HTTP, devolvendo o objeto da rota, que expõe o endpoint e a
    configuração declarada. Ela existe para exercitar o handler sem iniciar
    servidor ASGI ou cliente HTTP real.
    """
    for rota in criar_router(executor).routes:
        if rota.path == CAMINHO_LISTAGEM and "GET" in rota.methods:
            return rota
    raise AssertionError(f"Rota GET {CAMINHO_LISTAGEM} não encontrada.")


def _criar_curriculo(
    usuario_id: UsuarioId,
    titulo: str,
    layout: str = "classico",
    is_public: bool = False,
    referencias: tuple[ReferenciaCurriculo, ...] = (),
) -> Curriculo:
    """Cria uma versão válida do usuário com os dados e a seleção informados.

    A função gera uma identidade nova, constrói o agregado e inclui as
    referências recebidas. Ela existe para montar versões distintas mantendo
    cada teste focado na tradução HTTP.
    """
    curriculo = Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id,
        titulo_versao=titulo,
        layout=layout,
        is_public=is_public,
    )
    for referencia in referencias:
        curriculo.incluir_referencia(referencia)
    return curriculo


class ListagemVersoesCurriculoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP da listagem de versões pela rota GET.

    A classe substitui o caso de uso por um double e observa o que a rota envia
    e devolve. Ela existe para testar a unidade de interface isoladamente da
    Application e da infraestrutura.
    """

    async def test_devolve_o_resumo_publico_na_ordem_recebida_e_envia_a_entrada_correta(self) -> None:
        """Confirma os campos do resumo, a contagem de itens e a entrada enviada.

        O teste configura duas versões, uma com dois itens selecionados e outra
        sem itens, chama o handler e compara a resposta, que deve preservar a
        ordem recebida, e a entrada registrada no double. Ele existe para
        proteger o contrato da listagem.
        """
        usuario_id = UsuarioId(uuid4())
        primeira = _criar_curriculo(
            usuario_id,
            "Estágio em TI",
            referencias=(
                ReferenciaCurriculo(ProjetoAcademicoId(uuid4())),
                ReferenciaCurriculo(IdiomaId(uuid4())),
            ),
        )
        segunda = _criar_curriculo(usuario_id, "Gestão", layout="moderno", is_public=True)
        executor = ListagemExecutorDouble((primeira, segunda))
        listar = _rota(executor).endpoint

        resposta = await listar(usuario_id=usuario_id.valor)

        self.assertIsInstance(resposta, ListagemVersoesCurriculoResposta)
        self.assertEqual([versao.id for versao in resposta.versoes], [primeira.id.valor, segunda.id.valor])
        self.assertEqual(
            [(versao.titulo_versao, versao.layout, versao.is_public, versao.total_itens) for versao in resposta.versoes],
            [("Estágio em TI", "classico", False, 2), ("Gestão", "moderno", True, 0)],
        )
        self.assertEqual(executor.entradas, [ListarVersoesCurriculoEntrada(usuario_id)])

    async def test_resposta_nao_expoe_proprietario_nem_referencias(self) -> None:
        """Confirma que a resposta traz somente os campos públicos do resumo.

        O teste serializa a resposta de uma versão com itens e procura o
        identificador do estudante e os dos itens, além de enumerar os campos do
        resumo. Ele existe para proteger a minimização de dados da fronteira.
        """
        usuario_id = UsuarioId(uuid4())
        projeto_id = ProjetoAcademicoId(uuid4())
        curriculo = _criar_curriculo(usuario_id, "Estágio em TI", referencias=(ReferenciaCurriculo(projeto_id),))
        listar = _rota(ListagemExecutorDouble((curriculo,))).endpoint

        resposta = await listar(usuario_id=usuario_id.valor)

        texto = resposta.model_dump_json()
        self.assertNotIn(str(usuario_id.valor), texto)
        self.assertNotIn(str(projeto_id.valor), texto)
        self.assertEqual(
            set(resposta.versoes[0].model_dump().keys()),
            {"id", "titulo_versao", "layout", "is_public", "total_itens"},
        )

    async def test_estudante_sem_versoes_recebe_lista_vazia(self) -> None:
        """Confirma que a ausência de versões resulta em lista vazia, e não em erro.

        O teste configura o double sem versões e observa a lista vazia na
        resposta. Ele existe para proteger o caso do estudante que ainda não
        criou nenhuma versão.
        """
        listar = _rota(ListagemExecutorDouble(())).endpoint

        resposta = await listar(usuario_id=uuid4())

        self.assertEqual(resposta.versoes, [])

    async def test_declara_modelo_de_resposta_publico(self) -> None:
        """Confirma o modelo de resposta declarado na rota registrada.

        O teste inspeciona a configuração da rota, já que a chamada direta ao
        handler não passa pela camada que aplica o modelo. Ele existe para
        proteger o contrato HTTP da listagem.
        """
        rota = _rota(None)

        self.assertIs(rota.response_model, ListagemVersoesCurriculoResposta)

    async def test_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum caso de uso de listagem foi injetado.

        O teste chama o handler sem executor e observa a indisponibilidade
        explícita antes de qualquer outra decisão.
        """
        listar = _rota(None).endpoint

        with self.assertRaises(HTTPException) as contexto:
            await listar(usuario_id=uuid4())

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_fabrica_registra_a_listagem_junto_da_criacao_no_mesmo_caminho(self) -> None:
        """Confirma que a fábrica expõe GET e POST no caminho das versões.

        O teste monta a aplicação com o executor de listagem e lê, no esquema
        OpenAPI, os métodos documentados para o caminho, sem iniciar servidor. O
        esquema é usado porque o FastAPI agrupa os routers incluídos em objetos
        internos, o que torna instável inspecionar a lista de rotas. Ele existe
        para garantir que o novo router esteja ligado e não oculte a rota de
        criação.
        """
        app = create_app(listar_versoes_curriculo=ListagemExecutorDouble(()))

        metodos = set(app.openapi()["paths"][CAMINHO_LISTAGEM])

        self.assertTrue({"get", "post"} <= metodos)
