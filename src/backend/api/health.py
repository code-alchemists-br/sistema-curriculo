"""Expõe rotas e contratos de sondagem de integridade e prontidão do backend.

O módulo disponibiliza os endpoints HTTP de liveness (/health) e readiness (/ready)
para que orquestradores externos verifiquem se a aplicação está ativa e se a camada
de persistência está acessível. Ele existe para atender às necessidades operacionais
de monitoramento sem acoplar a API a tecnologias concretas de banco de dados e sem
expor credenciais, configurações ou dados sensíveis do ambiente.
"""

from typing import Protocol

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

# Proveniência: decision-analysis prompts/backend/20261014-175641-health-readiness-checks-v001.md#v001


class VerificadorConectividadePersistencia(Protocol):
    """Define a capacidade assíncrona de checar a conectividade da persistência.

    O protocolo estabelece o contrato assíncrono aguardado pelo endpoint de prontidão,
    retornando um booleano indicativo do estado operacional do armazenamento. Ele existe
    para permitir que o router valide a persistência sem acoplar a camada de API a
    drivers de banco de dados ou sessões concretas de ORM.
    """

    async def checar_conectividade(self) -> bool:
        """Verifica assincronamente se a camada de armazenamento está acessível.

        A implementação concreta realiza uma sondagem de baixo custo no armazenamento
        e reporta o resultado sem levantar exceções não tratadas. O método existe para
        fornecer uma resposta binária e segura sobre a disponibilidade da persistência.
        """


class HealthResposta(BaseModel):
    """Representa a resposta pública da sonda de integridade do processo.

    O DTO serializa o estado básico de vida da aplicação com um indicador textual
    estático sem incluir detalhes de ambiente, variáveis ou versões de pacotes.
    Ele existe para garantir que a verificação de liveness cumpra a política de não
    exposição de informações sensíveis.
    """

    status: str = "ok"


class ReadyResposta(BaseModel):
    """Representa a resposta pública da sonda de prontidão da aplicação.

    O DTO serializa a confirmação de que os recursos essenciais estão operacionais
    e prontos para receber tráfego sem expor topologia interna ou nomes de bancos.
    Ele existe para manter o contrato de readiness estável e seguro para orquestradores.
    """

    status: str = "ready"


def criar_router(
    verificador_conectividade: VerificadorConectividadePersistencia | None = None,
) -> APIRouter:
    """Cria e configura o roteador FastAPI para os endpoints operacionais de sondagem.

    A função instancia um APIRouter e registra os handlers HTTP de /health e /ready,
    injetando a dependência de verificação de persistência e tratando ausência ou falhas
    com códigos de status padronizados. Ela existe para desacoplar a criação das rotas
    de monitoramento da composição da aplicação ASGI e facilitar testes com doubles.
    """
    router = APIRouter()

    @router.get("/health", response_model=HealthResposta, status_code=status.HTTP_200_OK)
    async def checar_health() -> HealthResposta:
        """Responde à verificação de liveness do processo web.

        O handler retorna confirmação imediata de que a aplicação está em execução
        e aceitando conexões HTTP, sem consultar dependências externas. Ele existe para
        fornecer uma resposta rápida e sem efeitos colaterais para sondas de orquestração.
        """
        return HealthResposta(status="ok")

    @router.get("/ready", response_model=ReadyResposta, status_code=status.HTTP_200_OK)
    async def checar_ready() -> ReadyResposta:
        """Responde à verificação de prontidão para atendimento a requisições completas.

        O handler consulta a capacidade injetada de persistência e devolve 200 OK quando
        o armazenamento responde adequadamente, ou converte indisponibilidade em 503
        Service Unavailable. Ele existe para impedir que tráfego de produção seja direcionado
        a instâncias com banco de dados inacessível.
        """
        if verificador_conectividade is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Persistência indisponível.",
            )

        try:
            conectado = await verificador_conectividade.checar_conectividade()
        except Exception as erro:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Persistência indisponível.",
            ) from erro

        if not conectado:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Persistência indisponível.",
            )

        return ReadyResposta(status="ready")

    return router
