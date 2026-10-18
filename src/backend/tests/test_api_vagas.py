"""Testa unitariamente a fronteira HTTP de consulta de vagas externas.

O módulo valida o endpoint GET /vagas isolado por dublês em memória, assegurando
a serialização adequada dos resultados, a preservação de filtros no estado vazio ([F7.5]),
a sanitização de erros sem vazamento de detalhes internos ([F7.6]) e o registro da rota.
Ele existe para garantir o contrato e a segurança da API na camada de interface.
"""

from __future__ import annotations

import unittest
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

# Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
from backend.api.factory import create_app
from backend.api.vagas import criar_router
from backend.application.consulta_vagas import (
    ConsultarVagasEntrada,
    ErroIntegracaoVagas,
    RespostaInvalidaVagas,
    TimeoutIntegracaoVagas,
)
from backend.application.ports import VagaExternaDto

ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
class ConsultaVagasStub:
    """Dublê em memória para simular o caso de uso de consulta de vagas.

    A classe armazena as entradas recebidas e devolve uma coleção pré-configurada
    ou lança exceções controladas. Ela existe para isolar os testes do endpoint
    sem acoplamento a rede, banco ou serviços externos.
    """

    def __init__(
        self,
        resultado: list[VagaExternaDto] | None = None,
        excecao: Exception | None = None,
    ) -> None:
        """Inicializa o dublê com resultados esperados ou exceção a ser lançada.

        O construtor armazena o resultado determinístico e prepara o histórico de chamadas.
        Ele existe para permitir a configuração de cenários de teste na unidade de interface.
        """
        self.resultado = resultado if resultado is not None else []
        self.excecao = excecao
        self.entradas: list[ConsultarVagasEntrada] = []

    async def executar(self, entrada: ConsultarVagasEntrada) -> list[VagaExternaDto]:
        """Registra a entrada recebida e retorna o resultado ou dispara a exceção.

        O método simula a invocação assíncrona do caso de uso da camada de aplicação.
        Ele existe para fornecer respostas controladas ao handler HTTP em teste.
        """
        self.entradas.append(entrada)
        if self.excecao is not None:
            raise self.excecao
        return self.resultado


# Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
def _rota(router: APIRouter) -> Any:
    """Extrai o handler assíncrono do endpoint GET /vagas configurado no router.

    A função varre a lista de rotas do APIRouter e retorna o callable associado.
    Ela existe para permitir testes unitários diretos na função de fronteira.
    """
    for rota in router.routes:
        if getattr(rota, "path", None) == "/vagas" and "GET" in getattr(
            rota, "methods", set()
        ):
            return rota.endpoint
    raise AssertionError("Rota GET /vagas não encontrada no router.")


# Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
def _request(usuario_id: UUID | None) -> Request:
    """Constrói uma requisição HTTP simulada contendo o principal opcional no estado.

    A função instancia uma Request com escopo ASGI mínimo e atribui o identificador
    de usuário simulado. Ela existe para testar a validação de autenticação do handler.
    """
    request = Request(
        {"type": "http", "method": "GET", "path": "/vagas", "headers": []}
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


# Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
class ApiVagasTestCase(unittest.IsolatedAsyncioTestCase):
    """Suíte de testes unitários para a fronteira HTTP de busca de vagas externas.

    A classe verifica o comportamento da API para buscas com resultados, estado vazio,
    erros de integração e controle de acesso. Ela existe para blindar o contrato da API.
    """

    async def test_retorna_200_com_vagas_quando_busca_encontra_resultados(
        self,
    ) -> None:
        """Verifica a resposta 200 OK contendo os DTOs serializados de vagas encontradas.

        O cenário simula uma consulta com termo e filtros com retorno positivo do executor.
        Ele existe para validar o mapeamento e a contagem total de vagas na interface.
        """
        vagas_exemplo = [
            VagaExternaDto(
                id="vaga-101",
                titulo="Desenvolvedor Python Júnior",
                empresa="Tech Soluções",
                descricao="Atuação em backend e APIs.",
                requisitos=("Python", "FastAPI", "SQL"),
                localizacao="São Paulo - SP",
                modalidade="HIBRIDO",
                url_candidatura="https://vagas.exemplo.com/101",
            ),
            VagaExternaDto(
                id="vaga-102",
                titulo="Estágio em Engenharia de Software",
                empresa="Inova Lab",
                descricao="Auxílio em desenvolvimento web.",
                requisitos=("Git", "Lógica de Programação"),
                localizacao=None,
                modalidade="REMOTO",
                url_candidatura=None,
            ),
        ]
        executor = ConsultaVagasStub(resultado=vagas_exemplo)
        listar_vagas = _rota(criar_router(executor))

        resposta = await listar_vagas(
            request=_request(ID_USUARIO),
            termo="python",
            localizacao="São Paulo - SP",
            modalidade="HIBRIDO",
        )

        self.assertEqual(resposta.termo, "python")
        self.assertEqual(
            resposta.filtros,
            {"localizacao": "São Paulo - SP", "modalidade": "HIBRIDO"},
        )
        self.assertEqual(resposta.total, 2)
        self.assertEqual(len(resposta.vagas), 2)
        self.assertEqual(resposta.vagas[0].id, "vaga-101")
        self.assertEqual(resposta.vagas[0].titulo, "Desenvolvedor Python Júnior")
        self.assertEqual(resposta.vagas[0].requisitos, ["Python", "FastAPI", "SQL"])
        self.assertEqual(resposta.vagas[1].id, "vaga-102")
        self.assertIsNone(resposta.vagas[1].localizacao)
        self.assertIsNone(resposta.vagas[1].url_candidatura)

        self.assertEqual(len(executor.entradas), 1)
        self.assertEqual(executor.entradas[0].termo, "python")
        self.assertEqual(
            executor.entradas[0].filtros,
            {"localizacao": "São Paulo - SP", "modalidade": "HIBRIDO"},
        )

    async def test_retorna_200_com_estado_vazio_preservando_termo_e_filtros(
        self,
    ) -> None:
        """Verifica a exposição do estado vazio preservando termo e filtros ([F7.5]).

        O cenário simula busca sem resultados no serviço externo e confirma que
        o endpoint responde 200 OK com total zero e ecoa fielmente os critérios do estudante.
        Ele existe para satisfazer a sub-issue #241.
        """
        executor = ConsultaVagasStub(resultado=[])
        listar_vagas = _rota(criar_router(executor))

        resposta = await listar_vagas(
            request=_request(ID_USUARIO),
            termo="rust",
            localizacao="Remoto",
            modalidade="REMOTO",
        )

        self.assertEqual(resposta.termo, "rust")
        self.assertEqual(
            resposta.filtros,
            {"localizacao": "Remoto", "modalidade": "REMOTO"},
        )
        self.assertEqual(resposta.total, 0)
        self.assertEqual(resposta.vagas, [])
        self.assertEqual(len(executor.entradas), 1)
        self.assertEqual(executor.entradas[0].termo, "rust")

    async def test_retorna_504_em_timeout_sem_detalhes_internos(self) -> None:
        """Verifica que esgotamento de tempo limite retorna 504 limpo ([F7.6]).

        O cenário injeta TimeoutIntegracaoVagas com mensagem técnica interna e
        assegura que a resposta HTTP contenha mensagem estável sem vazar detalhes.
        Ele existe para satisfazer a sub-issue #242.
        """
        excecao_interna = TimeoutIntegracaoVagas(
            mensagem="Timeout no socket tcp://10.0.0.5:8000 após 5000ms",
            termo="dev",
            filtros={"modalidade": "REMOTO"},
        )
        executor = ConsultaVagasStub(excecao=excecao_interna)
        listar_vagas = _rota(criar_router(executor))

        with self.assertRaises(HTTPException) as contexto:
            await listar_vagas(
                request=_request(ID_USUARIO),
                termo="dev",
                localizacao=None,
                modalidade="REMOTO",
            )

        self.assertEqual(contexto.exception.status_code, 504)
        self.assertEqual(
            contexto.exception.detail,
            "Tempo limite esgotado ao consultar vagas externas. Tente novamente mais tarde.",
        )
        self.assertNotIn("tcp://10.0.0.5", contexto.exception.detail)
        self.assertNotIn("5000ms", contexto.exception.detail)

    async def test_retorna_502_em_resposta_invalida_sem_detalhes_internos(self) -> None:
        """Verifica que resposta corrompida retorna 502 Bad Gateway limpo ([F7.6]).

        O cenário injeta RespostaInvalidaVagas com detalhes de quebra de schema
        e confirma que o cliente recebe mensagem genérica segura.
        Ele existe para satisfazer a sub-issue #242.
        """
        excecao_invalida = RespostaInvalidaVagas(
            mensagem="JSONDecodeError na linha 42 coluna 15: chave 'id' ausente",
            termo="dados",
            filtros={},
        )
        executor = ConsultaVagasStub(excecao=excecao_invalida)
        listar_vagas = _rota(criar_router(executor))

        with self.assertRaises(HTTPException) as contexto:
            await listar_vagas(
                request=_request(ID_USUARIO),
                termo="dados",
                localizacao=None,
                modalidade=None,
            )

        self.assertEqual(contexto.exception.status_code, 502)
        self.assertEqual(
            contexto.exception.detail,
            "Não foi possível obter dados válidos do serviço de vagas no momento.",
        )
        self.assertNotIn("JSONDecodeError", contexto.exception.detail)
        self.assertNotIn("linha 42", contexto.exception.detail)

    async def test_retorna_502_em_erro_generico_integracao(self) -> None:
        """Verifica que falha genérica de integração retorna 502 Bad Gateway sanitizado ([F7.6]).

        O cenário simula ErroIntegracaoVagas e valida a tradução para HTTP 502 seguro.
        Ele existe para assegurar que nenhuma falha de infraestrutura externa vaze.
        """
        excecao_generica = ErroIntegracaoVagas(
            mensagem="ConnectionRefusedError: Host g2-api.intranet inacessível",
            termo="cloud",
            filtros={},
        )
        executor = ConsultaVagasStub(excecao=excecao_generica)
        listar_vagas = _rota(criar_router(executor))

        with self.assertRaises(HTTPException) as contexto:
            await listar_vagas(
                request=_request(ID_USUARIO),
                termo="cloud",
                localizacao=None,
                modalidade=None,
            )

        self.assertEqual(contexto.exception.status_code, 502)
        self.assertEqual(
            contexto.exception.detail,
            "Não foi possível obter dados válidos do serviço de vagas no momento.",
        )
        self.assertNotIn("ConnectionRefusedError", contexto.exception.detail)
        self.assertNotIn("g2-api.intranet", contexto.exception.detail)

    async def test_retorna_503_quando_executor_nao_configurado(self) -> None:
        """Verifica retorno 503 quando o executor de vagas não estiver presente.

        O cenário instancia o router com None e tenta listar vagas.
        Ele existe para sinalizar indisponibilidade controlada da dependência.
        """
        listar_vagas = _rota(criar_router(None))

        with self.assertRaises(HTTPException) as contexto:
            await listar_vagas(
                request=_request(ID_USUARIO),
                termo="python",
                localizacao=None,
                modalidade=None,
            )

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Consulta de vagas indisponível.")

    async def test_rejeita_requisicao_sem_autenticacao(self) -> None:
        """Verifica retorno 401 quando a requisição não contém principal autenticado.

        O cenário omite o estado de sessão e verifica a recusa imediata sem chamar o executor.
        Ele existe para proteger a rota contra acessos anônimos.
        """
        executor = ConsultaVagasStub()
        listar_vagas = _rota(criar_router(executor))

        with self.assertRaises(HTTPException) as contexto:
            await listar_vagas(
                request=_request(None),
                termo="python",
                localizacao=None,
                modalidade=None,
            )

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(contexto.exception.detail, "Autenticação necessária.")
        self.assertEqual(executor.entradas, [])

    def test_fabrica_registra_rota_de_vagas(self) -> None:
        """Verifica que a aplicação ASGI registra a rota /vagas no contrato OpenAPI.

        O teste cria o app via create_app e inspeciona o schema OpenAPI gerado.
        Ele existe para garantir que a rota está devidamente exposta na aplicação.
        """
        app = create_app()
        schema = app.openapi()

        self.assertIn("/vagas", schema["paths"])
        operacao_get = schema["paths"]["/vagas"]["get"]
        self.assertIn("Vagas", operacao_get["tags"])
        self.assertEqual(operacao_get["summary"], "Listar Vagas")
