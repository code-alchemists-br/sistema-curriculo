"""Expõe a consulta autenticada de vagas externas por HTTP.

O módulo define os DTOs de resposta, o protocolo do executor e a rota HTTP de
busca de oportunidades. Ele existe para conectar a interface web à camada de
aplicação, garantindo a preservação de filtros no estado vazio e a resposta
segura em situações de erro de integração sem vazar detalhes internos ao cliente.
"""

from __future__ import annotations

from typing import Any, Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request, status
from pydantic import BaseModel

# Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
from backend.application.consulta_vagas import (
    ConsultarVagasEntrada,
    ErroIntegracaoVagas,
    RespostaInvalidaVagas,
    TimeoutIntegracaoVagas,
)
from backend.application.ports import VagaExternaDto


# Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
class VagaResposta(BaseModel):
    """Representa uma oportunidade de vaga exposta publicamente na interface HTTP.

    O DTO serializa os dados essenciais e complementares de uma vaga externa de
    forma amigável ao cliente. Ele existe para desacoplar a representação HTTP
    dos DTOs internos da camada de aplicação e dos contratos externos.
    """

    id: str
    titulo: str
    empresa: str
    descricao: str
    requisitos: list[str]
    localizacao: str | None = None
    modalidade: str | None = None
    url_candidatura: str | None = None


# Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
class ResultadoBuscaVagasResposta(BaseModel):
    """Representa o resultado consolidado da pesquisa de vagas na interface HTTP.

    O DTO agrupa o termo consultado, o dicionário de filtros utilizados, a contagem
    total e a lista de vagas encontradas. Ele existe para satisfazer o requisito
    de estado vazio ([F7.5]), permitindo ao estudante visualizar seus critérios e ajustá-los.
    """

    termo: str
    filtros: dict[str, Any]
    total: int
    vagas: list[VagaResposta]


# Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
class ConsultaVagasExecutor(Protocol):
    """Define o contrato da consulta de vagas consumido pela fronteira HTTP.

    O protocolo recebe os critérios de busca tipados e devolve a coleção de vagas
    obtida pela camada de aplicação. Ele existe para viabilizar injeção de dependência
    e testes unitários isolados de transporte sem depender de implementação concreta.
    """

    async def executar(self, entrada: ConsultarVagasEntrada) -> list[VagaExternaDto]:
        """Executa a pesquisa de vagas a partir dos parâmetros informados.

        O método orquestra a obtenção de vagas na camada interna e devolve a lista
        de DTOs correspondente. Ele existe para separar a fronteira HTTP da orquestração.
        """
        ...


# Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
def criar_router(
    consultar_vagas: ConsultaVagasExecutor | None,
) -> APIRouter:
    """Cria o router HTTP para consulta e listagem de vagas de emprego.

    A fábrica registra o endpoint GET /vagas com validação de autenticação,
    preservação de critérios de pesquisa no estado vazio e tratamento resiliente
    de erros de integração externa. Ela existe para compor a interface HTTP mantendo
    o isolamento em relação ao framework.
    """
    router = APIRouter()

    @router.get(
        "/vagas",
        response_model=ResultadoBuscaVagasResposta,
        status_code=status.HTTP_200_OK,
    )
    async def listar_vagas(
        request: Request,
        termo: str = Query(
            default="",
            description="Termo de pesquisa por cargo, empresa ou palavra-chave.",
        ),
        localizacao: str | None = Query(
            default=None,
            description="Filtro opcional por cidade, estado ou modelo geográfico.",
        ),
        modalidade: str | None = Query(
            default=None,
            description="Filtro opcional por modalidade de trabalho (ex: REMOTO, HIBRIDO, PRESENCIAL).",
        ),
    ) -> ResultadoBuscaVagasResposta:
        """Realiza a consulta de oportunidades de vagas para o estudante autenticado.

        O handler valida a sessão do usuário, compõe a entrada da aplicação com o
        termo e os filtros recebidos, invoca o executor e formata a resposta. Em caso
        de lista vazia, retorna 200 OK preservando os filtros; em caso de falha externa,
        retorna erros HTTP controlados (504/502) sem vazar detalhes técnicos internos.
        Ele existe para expor o serviço de busca de vagas com integridade e segurança.
        """
        if consultar_vagas is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Consulta de vagas indisponível.",
            )

        usuario_id = getattr(request.state, "usuario_id", None)
        if not isinstance(usuario_id, UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária.",
            )

        filtros: dict[str, Any] = {}
        if localizacao is not None:
            filtros["localizacao"] = localizacao
        if modalidade is not None:
            filtros["modalidade"] = modalidade

        entrada = ConsultarVagasEntrada(termo=termo, filtros=filtros)

        try:
            vagas_externas = await consultar_vagas.executar(entrada)
        except TimeoutIntegracaoVagas as erro:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Tempo limite esgotado ao consultar vagas externas. Tente novamente mais tarde.",
            ) from erro
        except (RespostaInvalidaVagas, ErroIntegracaoVagas) as erro:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Não foi possível obter dados válidos do serviço de vagas no momento.",
            ) from erro

        vagas_resposta = [
            VagaResposta(
                id=vaga.id,
                titulo=vaga.titulo,
                empresa=vaga.empresa,
                descricao=vaga.descricao,
                requisitos=list(vaga.requisitos),
                localizacao=vaga.localizacao,
                modalidade=vaga.modalidade,
                url_candidatura=vaga.url_candidatura,
            )
            for vaga in vagas_externas
        ]

        return ResultadoBuscaVagasResposta(
            termo=termo,
            filtros=filtros,
            total=len(vagas_resposta),
            vagas=vagas_resposta,
        )

    return router
