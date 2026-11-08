"""Verifica handler e bindings com doubles, sem servidor ou banco real.

Exercita a conversão da coleção, identidade e erros locais para proteger a
fronteira HTTP sem executar middleware, Application ou persistência.
"""

# Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
import inspect
import unittest
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID

from fastapi import HTTPException, Request

from backend.api.experiencia_profissional import criar_router
from backend.api.factory import create_app
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import ExperienciaProfissionalId, Periodo, UsuarioId


def obter_rota(executor):
    """Localiza o GET no router para testar seu handler diretamente.

    Inspeciona caminho e método sem iniciar contexto ASGI, permitindo verificar
    a tradução isolada do servidor e do mecanismo de sessão.
    """
    return next(
        rota for rota in criar_router(None, listar_experiencias=executor).routes
        if rota.path == "/experiencias-profissionais" and "GET" in rota.methods
    )


class ListagemExperienciasHandlerTestCase(unittest.IsolatedAsyncioTestCase):
    """Confere representação e entrada interna usando executor substituído.

    Emprega dados sintéticos e requisição double para observar a unidade de
    transporte sem integrar autenticação, regras de negócio ou armazenamento.
    """

    async def test_sete_campos_ordem_preservada_e_dono_somente_do_estado(self):
        """Injeta dados de cliente conflitantes e verifica DTOs e dono interno.

        Fornece uma sequência propositalmente fora da ordem de domínio para
        detectar reordenação no handler, mantendo o estado como única fonte do
        dono e os sete campos existentes como saída pública.
        """
        dono, alheio = UUID(int=101), UUID(int=202)
        experiencias = tuple(
            ExperienciaProfissional(
                id=ExperienciaProfissionalId(UUID(int=indice)),
                usuario_id=UsuarioId(dono),
                empresa="Empresa Local", cargo="Desenvolvedor",
                descricao="Desenvolvimento de aplicações.",
                periodo=Periodo(date(2024, 2, 1), fim),
            )
            for indice, fim in ((9, date(2025, 1, 1)), (3, None))
        )
        executor = Mock(executar=AsyncMock(return_value=experiencias))
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
                "empresa": "Empresa Local", "cargo": "Desenvolvedor",
                "descricao": "Desenvolvimento de aplicações.",
                "data_inicio": "2024-02-01",
                "data_fim": item.periodo.fim.isoformat() if item.periodo.fim else None,
            } for item in experiencias
        ]
        self.assertEqual(resposta.model_dump(mode="json"), {"experiencias": esperado})
        executor.executar.assert_awaited_once()
        self.assertEqual(executor.executar.call_args.args[0].usuario_id, UsuarioId(dono))
        request.json.assert_not_called()
        request.body.assert_not_called()

    async def test_vazio_devolve_envelope_vazio_com_status_200(self):
        """Confere resultado vazio e status local para evitar falso não encontrado.

        Substitui a consulta por tupla vazia e inspeciona resposta e declaração
        da rota, sem depender de uma requisição HTTP ou banco real.
        """
        rota = obter_rota(Mock(executar=AsyncMock(return_value=())))
        resposta = await rota.endpoint(Mock(state=SimpleNamespace(usuario_id=UUID(int=101))))
        self.assertEqual(rota.status_code, 200)
        self.assertEqual(resposta.model_dump(), {"experiencias": []})

    async def test_executor_ausente_responde_503_controlado(self):
        """Chama a unidade sem executor e confere sua tradução de indisponibilidade.

        Usa estado autenticado sintético para proteger a mensagem HTTP estável
        sem iniciar mecanismo de sessão ou persistência.
        """
        with self.assertRaises(HTTPException) as contexto:
            await obter_rota(None).endpoint(Mock(state=SimpleNamespace(usuario_id=UUID(int=101))))
        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Listagem indisponível.")

    async def test_identidade_ausente_ou_invalida_responde_401_sem_consulta(self):
        """Confere a defesa local por estados sintéticos e executor double.

        Verifica o erro e a ausência de chamadas para preservar o uso da função
        de identidade existente sem alterar ou testar middleware integrado.
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
        """Inspeciona a declaração local do GET sem iniciar a aplicação.

        Confere ausência de entradas e documentação de sessão, ordem e respostas
        para proteger o desenho do endpoint sem teste de contrato integrado.
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

    def test_factory_e_router_adicionam_leitura_no_fim_e_encaminham_executor(self):
        """Inspeciona assinaturas e binding com FastAPI e router substituídos.

        Verifica a posição dos novos parâmetros e a chamada do router para
        proteger consumidores posicionais sem criar contexto de aplicação.
        """
        self.assertEqual(list(inspect.signature(create_app).parameters)[-1], "listar_experiencias_profissionais")
        self.assertEqual(list(inspect.signature(criar_router).parameters)[-1], "listar_experiencias")
        executor = Mock()
        with (
            patch("backend.api.factory.FastAPI"),
            patch("backend.api.factory.criar_router_experiencia_profissional") as router,
        ):
            create_app(listar_experiencias_profissionais=executor)
        self.assertIs(router.call_args.kwargs["listar_experiencias"], executor)
