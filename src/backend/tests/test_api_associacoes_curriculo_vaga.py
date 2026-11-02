"""Testa unitariamente a fronteira HTTP da listagem de associações."""

import unittest
from uuid import UUID

from fastapi import HTTPException, Request
from fastapi.routing import APIRoute

# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
from backend.api.associacoes_curriculo_vaga import (
    CAMINHO_LISTAGEM_ASSOCIACOES,
    ListagemAssociacoesCurriculoVagaResposta,
    criar_router,
)
from backend.application.consulta_associacao_curriculo_vaga import (
    ListarAssociacoesCurriculoVagaEntrada,
)
from backend.domain.associacao_curriculo_vaga import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
)
from backend.domain.value_objects import CurriculoId, UsuarioId, VagaId


class ListagemAssociacoesExecutorStub:
    """Substitui o caso de uso e registra a entrada recebida pelo router.

    O stub devolve uma página pré-configurada sem I/O. Ele existe para isolar e
    verificar a tradução de identidade, paginação e dados da fronteira HTTP.
    """

    def __init__(self, resultado: tuple[AssociacaoCurriculoVaga, ...] = ()) -> None:
        """Armazena a página de teste e inicia o registro de chamadas.

        Toda configuração permanece em memória. Ela existe para observar
        exatamente a entrada enviada pelo handler ao caso de uso.
        """
        self.resultado = resultado
        self.entradas: list[ListarAssociacoesCurriculoVagaEntrada] = []

    async def executar(
        self, entrada: ListarAssociacoesCurriculoVagaEntrada
    ) -> tuple[AssociacaoCurriculoVaga, ...]:
        """Registra a entrada e devolve a página configurada.

        O método não acessa banco nem rede e preserva a ordem da tupla recebida.
        Ele existe para tornar observável a delegação feita pelo router.
        """
        self.entradas.append(entrada)
        return self.resultado


def _rota(executor: ListagemAssociacoesExecutorStub | None) -> APIRoute:
    """Localiza o handler GET da coleção de associações no router.

    A função constrói o router com o executor fornecido e retorna sua rota
    registrada, sem iniciar uma aplicação ou servidor. Ela existe para chamar
    isoladamente o adapter HTTP nos testes.
    """
    router = criar_router(executor)
    for rota in router.routes:
        if (
            isinstance(rota, APIRoute)
            and rota.path == CAMINHO_LISTAGEM_ASSOCIACOES
            and "GET" in rota.methods
        ):
            return rota
    raise AssertionError(f"Rota GET {CAMINHO_LISTAGEM_ASSOCIACOES} não encontrada.")


def _request(usuario_id: UUID | None) -> Request:
    """Monta uma requisição ASGI mínima com o principal opcional.

    O helper grava a identidade somente no estado da requisição, como faria o
    middleware de sessão. Ele existe para testar que o router não recebe
    identidade de cliente pela rota.
    """
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": CAMINHO_LISTAGEM_ASSOCIACOES,
            "headers": [],
        }
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


class ListagemAssociacoesCurriculoVagaRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP da listagem com o caso de uso substituído.

    Os testes chamam o endpoint diretamente e inspecionam sua rota declarada,
    sem servidor, banco ou autenticação externa. A classe existe para proteger
    o comportamento isolado do adapter HTTP.
    """

    async def test_mapeia_principal_pagina_e_classificacoes_sem_reordenar_associacoes(
        self,
    ) -> None:
        """Confirma o principal, a página e a serialização determinística.

        O cenário devolve duas associações em ordem conhecida, verifica os IDs,
        classificações ordenadas e a entrada encaminhada. Ele existe para
        proteger o contrato de saída e a identidade derivada da sessão.
        """
        usuario_id = UUID(int=1)
        primeira = AssociacaoCurriculoVaga(
            CurriculoId(UUID(int=10)),
            VagaId("vaga-a"),
            (
                ClassificacaoAssociacao.CANDIDATURA,
                ClassificacaoAssociacao.COMPATIBILIDADE,
            ),
        )
        segunda = AssociacaoCurriculoVaga(
            CurriculoId(UUID(int=20)),
            VagaId("vaga-b"),
            (ClassificacaoAssociacao.INTERESSE,),
        )
        executor = ListagemAssociacoesExecutorStub((primeira, segunda))
        rota = _rota(executor)

        resposta = await rota.endpoint(
            request=_request(usuario_id),
            offset=5,
            limit=3,
        )

        self.assertIsInstance(resposta, ListagemAssociacoesCurriculoVagaResposta)
        self.assertEqual(
            [
                (item.curriculo_id, item.vaga_id, item.classificacoes)
                for item in resposta.associacoes
            ],
            [
                (
                    UUID(int=10),
                    "vaga-a",
                    ["candidatura", "compatibilidade", "interesse"],
                ),
                (UUID(int=20), "vaga-b", ["interesse"]),
            ],
        )
        self.assertEqual(
            executor.entradas,
            [
                ListarAssociacoesCurriculoVagaEntrada(
                    UsuarioId(usuario_id),
                    offset=5,
                    limit=3,
                )
            ],
        )

    async def test_retorna_pagina_vazia_sem_executor_chamado_indevidamente(
        self,
    ) -> None:
        """Representa uma consulta válida sem associações como lista vazia.

        O executor substituto devolve uma tupla vazia e a resposta mantém a
        coleção vazia. O teste existe para fixar a representação do estado sem
        resultados sem fallback de erro.
        """
        executor = ListagemAssociacoesExecutorStub()

        resposta = await _rota(executor).endpoint(
            request=_request(UUID(int=2)),
            offset=0,
            limit=10,
        )

        self.assertEqual(resposta.associacoes, [])
        self.assertEqual(len(executor.entradas), 1)

    async def test_retorna_401_sem_identidade_autenticada(self) -> None:
        """Rejeita a chamada sem principal antes de consultar o executor.

        A requisição não contém `request.state.usuario_id`; o cenário confirma
        401 e nenhuma delegação. Ele existe para exigir identidade instalada
        pelo mecanismo de sessão existente.
        """
        executor = ListagemAssociacoesExecutorStub()

        with self.assertRaises(HTTPException) as contexto:
            await _rota(executor).endpoint(
                request=_request(None),
                offset=0,
                limit=10,
            )

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    async def test_retorna_503_quando_executor_ausente(self) -> None:
        """Sinaliza indisponibilidade sem produzir página de sucesso vazia.

        O cenário fornece principal válido, mas não compõe o executor. Ele
        existe para distinguir ausência de serviço de uma consulta vazia.
        """
        with self.assertRaises(HTTPException) as contexto:
            await _rota(None).endpoint(
                request=_request(UUID(int=3)),
                offset=0,
                limit=10,
            )

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_converte_parametros_invalidos_em_422(self) -> None:
        """Traduz as validações da entrada da Application para HTTP 422.

        Os cenários passam offset negativo e limit não positivo diretamente ao
        handler, verificando que nenhum deles chega ao executor. Ele existe
        para manter a fronteira coerente com a validação do caso de uso.
        """
        executor = ListagemAssociacoesExecutorStub()
        endpoint = _rota(executor).endpoint

        for offset, limit in ((-1, 10), (0, 0)):
            with self.subTest(offset=offset, limit=limit):
                with self.assertRaises(HTTPException) as contexto:
                    await endpoint(
                        request=_request(UUID(int=4)),
                        offset=offset,
                        limit=limit,
                    )

                self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(executor.entradas, [])

    def test_registra_rota_get_sem_identificador_de_estudante_na_url(self) -> None:
        """Confirma método, caminho e modelo de resposta declarados no router.

        O teste inspeciona a configuração da rota sem iniciar FastAPI. Ele
        existe para evitar que um ID controlado pelo cliente reapareça na URL e
        para manter a projeção tipada.
        """
        rota = _rota(None)

        self.assertEqual(rota.path, "/estudantes/atual/associacoes-curriculo-vaga")
        self.assertEqual(rota.methods, {"GET"})
        self.assertIs(rota.response_model, ListagemAssociacoesCurriculoVagaResposta)

    def test_exige_apenas_offset_e_limit_com_restricoes_de_paginacao(self) -> None:
        """Declara paginação obrigatória sem identidade controlada pelo cliente.

        O teste inspeciona os parâmetros de query registrados pelo FastAPI,
        verificando obrigatoriedade e limites estruturais sem subir servidor.
        Ele existe para fixar a configuração da fronteira HTTP.
        """
        parametros = {
            parametro.name: parametro
            for parametro in _rota(None).dependant.query_params
        }

        self.assertEqual(set(parametros), {"offset", "limit"})
        self.assertTrue(parametros["offset"].field_info.is_required())
        self.assertEqual(parametros["offset"].field_info.metadata[0].ge, 0)
        self.assertTrue(parametros["limit"].field_info.is_required())
        self.assertEqual(parametros["limit"].field_info.metadata[0].gt, 0)
