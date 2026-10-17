"""Verifica o health check agregado exposto pela API."""

import asyncio
import json
import unittest

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.api.factory import create_app
from backend.api.middleware_autenticacao import ROTAS_PUBLICAS
from backend.api.saude import criar_router
from backend.application.saude import VerificadorSaude
from backend.infrastructure.security.autenticador_sessao_indisponivel import (
    AutenticadorSessaoIndisponivel,
)


class VerificadorSaudeStub(VerificadorSaude):
    """Simula a disponibilidade de uma dependência sem acesso externo.

    O double retorna um resultado ou lança uma exceção configurada. Ele existe
    para exercitar o health check sem abrir conexões com serviços reais.
    """

    def __init__(
        self, resultado: bool = True, erro: Exception | None = None
    ) -> None:
        """Armazena resultado e falha opcionais para os cenários de teste.

        A configuração permanece em memória. O construtor existe para permitir
        testar dependências saudáveis e indisponíveis de forma determinística.
        """
        self.resultado = resultado
        self.erro = erro

    async def verificar(self) -> bool:
        """Devolve o resultado configurado ou simula falha do probe.

        O método retorna o booleano definido no double ou lança a exceção
        configurada. Ele existe para observar como a rota agrega cada probe.
        """
        if self.erro is not None:
            raise self.erro
        return self.resultado


class VerificadorTravado(VerificadorSaude):
    """Simula uma dependência que não conclui seu probe de disponibilidade.

    O método aguarda um evento sem sinalização para exceder o timeout da rota.
    A classe existe para provar que o monitor recebe indisponibilidade em vez
    de aguardar indefinidamente.
    """

    async def verificar(self) -> bool:
        """Aguarda indefinidamente para acionar o limite do health check.

        A espera usa um evento sem sinalização. Ela existe para simular uma
        dependência travada sem iniciar tarefas externas.
        """
        await asyncio.Event().wait()
        return True


def _handler(verificadores: tuple[VerificadorSaude, ...] = ()):
    """Localiza o handler de saúde sem iniciar servidor ou cliente HTTP.

    A função procura `/health` no router isolado e devolve seu endpoint. Ela
    existe para testar status e corpo diretamente, sem rede ou dependências reais.
    """
    router: APIRouter = criar_router(verificadores)
    for rota in router.routes:
        if rota.path == "/health" and "GET" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota GET /health não encontrada.")


class HealthCheckApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Protege a resposta agregada e privada do endpoint de saúde.

    Os testes chamam o handler com verificadores em memória e inspecionam a
    composição OpenAPI. A classe existe para garantir monitoramento sem expor
    detalhes das dependências nem exigir sessão de usuário.
    """

    async def test_retorna_ok_quando_todos_os_verificadores_estao_saudaveis(
        self,
    ) -> None:
        """Agrega probes saudáveis em uma resposta mínima sem dados de serviço.

        Dois verificadores locais retornam `True`; a resposta contém somente o
        estado agregado. O teste existe para permitir monitoramento seguro.
        """
        verificadores = (VerificadorSaudeStub(), VerificadorSaudeStub())

        resposta: JSONResponse = await _handler(verificadores)()

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(json.loads(resposta.body), {"status": "ok"})

    async def test_sem_verificadores_confirma_somente_disponibilidade_da_api(
        self,
    ) -> None:
        """Mantém a rota útil na composição sem dependências externas injetadas.

        O router executa zero probes e devolve o estado da própria API. O teste
        existe para deixar explícito o comportamento da composição atual.
        """
        resposta: JSONResponse = await _handler()()

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(json.loads(resposta.body), {"status": "ok"})

    async def test_retorna_503_sem_identificar_dependencia_indisponivel(self) -> None:
        """Sinaliza indisponibilidade sem informar qual probe falhou.

        Um verificador falso representa a dependência fora do ar. A resposta
        contém apenas o estado geral; o teste existe para evitar vazamento de
        nomes ou topologia dos serviços.
        """
        resposta: JSONResponse = await _handler(
            (VerificadorSaudeStub(resultado=False),)
        )()

        self.assertEqual(resposta.status_code, 503)
        self.assertEqual(json.loads(resposta.body), {"status": "indisponivel"})

    async def test_sanitiza_excecao_de_verificador(self) -> None:
        """Converte erro interno em estado genérico sem mensagem sensível.

        O probe lança uma exceção contendo detalhe confidencial. A API responde
        somente o estado de indisponibilidade para monitores externos.
        """
        resposta: JSONResponse = await _handler(
            (VerificadorSaudeStub(erro=RuntimeError("senha-secreta")),)
        )()

        corpo = resposta.body.decode("utf-8")
        self.assertEqual(resposta.status_code, 503)
        self.assertEqual(json.loads(corpo), {"status": "indisponivel"})
        self.assertNotIn("senha-secreta", corpo)

    async def test_timeout_do_verificador_retorna_503(self) -> None:
        """Limita o tempo de resposta quando um probe não termina.

        O verificador aguarda além do limite configurado pela rota. O teste
        existe para que um serviço travado não mantenha o monitor pendente.
        """
        resposta: JSONResponse = await _handler((VerificadorTravado(),))()

        self.assertEqual(resposta.status_code, 503)
        self.assertEqual(json.loads(resposta.body), {"status": "indisponivel"})

    async def test_rota_e_publica_e_documentada_mesmo_com_autenticacao(self) -> None:
        """Mantém health check acessível e sem exigência de cookie de sessão.

        A aplicação é composta com autenticação ativa e schema OpenAPI gerado.
        O teste existe para permitir que sistemas de monitoramento consultem a
        saúde antes de haver uma sessão de usuário.
        """
        app = create_app(autenticador_sessao=AutenticadorSessaoIndisponivel())
        operacao = app.openapi()["paths"]["/health"]["get"]

        self.assertIn(("GET", "/health"), ROTAS_PUBLICAS)
        self.assertNotIn("security", operacao)
