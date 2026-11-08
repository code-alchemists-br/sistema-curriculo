"""Verifica handler e bindings isolados com doubles, sem servidor ou banco.

Exercita DTOs, ordem e identidade para proteger a tradução da consulta própria
sem executar middleware, Application ou persistência real.
"""

# Proveniência: decision-analysis prompts/backend/20261107-171028-listar-formacoes-academicas-v001.md#v001
import inspect
import unittest
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID

from fastapi import HTTPException, Request

from backend.api.factory import create_app
from backend.api.formacao_academica import criar_router
from backend.domain.itens_perfil import (
    FormacaoAcademica,
    NivelFormacaoAcademica,
    StatusFormacaoAcademica,
)
from backend.domain.value_objects import FormacaoAcademicaId, Periodo, UsuarioId


def obter_rota(executor):
    """Localiza o GET por caminho e método para testar somente seu handler.

    Inspeciona o router sem iniciar contexto ASGI, permitindo observar a unidade
    de transporte isolada do servidor e do mecanismo de autenticação.
    """
    return next(
        rota for rota in criar_router(None, listar_formacoes=executor).routes
        if rota.path == "/formacoes-academicas" and "GET" in rota.methods
    )


class ListagemFormacoesHandlerTestCase(unittest.IsolatedAsyncioTestCase):
    """Confere tradução e metadados com executor e requisição substituídos.

    Usa dados sintéticos para observar ordem, identidade e falhas sem executar
    casos de uso reais ou uma jornada integrada da API.
    """

    async def test_oito_campos_ordem_preservada_e_dono_somente_do_estado(self):
        """Fornece canais de cliente conflitantes e confere a entrada interna.

        O Request double contém outro dono em query, caminho e corpo, enquanto
        o executor recebe o estado; DTOs preservam sequência e os oito campos
        públicos para impedir reordenação ou exposição de detalhes internos.
        """
        dono, alheio = UUID(int=101), UUID(int=202)
        formacoes = tuple(
            FormacaoAcademica(
                id=FormacaoAcademicaId(UUID(int=indice)),
                usuario_id=UsuarioId(dono),
                instituicao="Universidade Local",
                curso="Computação",
                nivel=NivelFormacaoAcademica.GRADUACAO,
                periodo=Periodo(date(2024, 2, 1), None),
                status=StatusFormacaoAcademica.EM_ANDAMENTO,
            ) for indice in (9, 3)
        )
        executor = Mock(executar=AsyncMock(return_value=formacoes))
        request = Mock(spec=Request)
        request.state = SimpleNamespace(usuario_id=dono)
        request.query_params = {"usuario_id": str(alheio)}
        request.path_params = {"usuario_id": str(alheio)}
        request.json = AsyncMock(return_value={"usuario_id": str(alheio)})
        request.body = AsyncMock(return_value=b'{"usuario_id":"alheio"}')

        resposta = await obter_rota(executor).endpoint(request)

        esperado = [
            {
                "id": str(item.id.valor), "usuario_id": str(dono),
                "instituicao": "Universidade Local", "curso": "Computação",
                "nivel": "graduacao", "data_inicio": "2024-02-01",
                "data_fim": None, "status": "em_andamento",
            } for item in formacoes
        ]
        self.assertEqual(resposta.model_dump(mode="json"), {"formacoes": esperado})
        executor.executar.assert_awaited_once()
        self.assertEqual(executor.executar.call_args.args[0].usuario_id, UsuarioId(dono))
        request.json.assert_not_called()
        request.body.assert_not_called()

    async def test_vazio_devolve_envelope_vazio_com_status_200(self):
        """Confere DTO vazio e status na declaração da rota sem executar HTTP.

        Substitui a consulta por tupla vazia para proteger a representação da
        ausência de itens como sucesso, sem depender do banco ou do servidor.
        """
        executor = Mock(executar=AsyncMock(return_value=()))
        rota = obter_rota(executor)
        resposta = await rota.endpoint(Mock(state=SimpleNamespace(usuario_id=UUID(int=101))))
        self.assertEqual(rota.status_code, 200)
        self.assertEqual(resposta.model_dump(), {"formacoes": []})

    async def test_executor_ausente_responde_503_controlado(self):
        """Chama o handler sem executor e inspeciona sua exceção HTTP.

        Usa estado autenticado sintético para garantir a mensagem pública de
        indisponibilidade sem depender do mecanismo de sessão ou persistência.
        """
        with self.assertRaises(HTTPException) as contexto:
            await obter_rota(None).endpoint(Mock(state=SimpleNamespace(usuario_id=UUID(int=101))))
        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Listagem indisponível.")

    async def test_identidade_ausente_ou_invalida_nao_consulta(self):
        """Verifica estados inválidos com doubles para proteger a defesa local.

        Inspeciona 401 e ausência de consulta para manter o tratamento dos
        handlers existentes sem integrar a política de autenticação.
        """
        for estado in (SimpleNamespace(), SimpleNamespace(usuario_id="invalido")):
            with self.subTest(estado=vars(estado)):
                executor = Mock(executar=AsyncMock())
                with self.assertRaises(HTTPException) as contexto:
                    await obter_rota(executor).endpoint(Mock(state=estado))
                self.assertEqual(contexto.exception.status_code, 401)
                self.assertEqual(contexto.exception.detail, "Autenticação necessária.")
                executor.executar.assert_not_called()

    def test_metadados_sem_entradas_e_com_respostas_documentadas(self):
        """Inspeciona metadados locais sem iniciar aplicação ou gerar contrato.

        Confere assinatura, entradas e descrição para preservar a declaração
        do GET sem parâmetros e sua documentação de sessão e ordenação.
        """
        rota = obter_rota(Mock())
        self.assertEqual(list(inspect.signature(rota.endpoint).parameters), ["request"])
        self.assertFalse(rota.dependant.query_params)
        self.assertFalse(rota.dependant.path_params)
        self.assertFalse(rota.dependant.body_params)
        self.assertEqual(set(rota.responses), {200, 401, 503})
        self.assertTrue(rota.summary)
        self.assertIn("cookie de sessão", rota.description)
        self.assertIn("ordem do domínio", rota.description)
        self.assertIn("sem corpo, parâmetros ou paginação", rota.description)

    def test_factory_adiciona_parametro_no_fim_e_encaminha_executor(self):
        """Confere binding substituindo FastAPI e o router para evitar contexto.

        Inspeciona assinatura e chamada do router para proteger consumidores
        posicionais da factory e a passagem do executor de leitura ao GET.
        """
        # Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
        self.assertEqual(list(inspect.signature(create_app).parameters)[-2:], [
            "listar_formacoes_academicas", "listar_experiencias_profissionais"
        ])
        executor = Mock()
        with (
            patch("backend.api.factory.FastAPI"),
            patch("backend.api.factory.criar_router_formacao_academica") as router,
        ):
            create_app(listar_formacoes_academicas=executor)
        self.assertIs(router.call_args.kwargs["listar_formacoes"], executor)
