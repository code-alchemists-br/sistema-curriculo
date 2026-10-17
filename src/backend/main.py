"""Compõe a aplicação ASGI, a readiness de persistência e o logging.

O módulo cria uma engine assíncrona quando `DATABASE_URL` está configurada,
injeta um verificador SQL mínimo e encerra a engine no shutdown. Sem essa
variável, readiness permanece indisponível. Ele existe para concentrar a
composição de infraestrutura fora das camadas internas.
"""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from backend.api.factory import create_app
from backend.application.saude import VerificadorPersistencia
from backend.configuracao_logging import configurar_logging
from backend.infrastructure.persistence.sqlalchemy.verificador_persistencia import (
    VerificadorPersistenciaSqlalchemy,
)
from backend.infrastructure.security.autenticador_sessao_indisponivel import (
    AutenticadorSessaoIndisponivel,
)

configurar_logging()


def _criar_engine_persistencia(database_url: str | None) -> AsyncEngine | None:
    """Cria a engine PostgreSQL assíncrona quando há URL de persistência.

    A função normaliza URLs PostgreSQL sem driver para `postgresql+psycopg`,
    ativa verificação de conexão e limita o tempo de conexão. Ela existe para
    fornecer à aplicação uma dependência real para o probe de readiness.
    """
    if not database_url:
        return None

    url = make_url(database_url)
    if url.drivername == "postgresql":
        url = url.set(drivername="postgresql+psycopg")
    return create_async_engine(
        url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 2},
    )


_engine_persistencia = _criar_engine_persistencia(
    os.environ.get("DATABASE_URL")
)
_verificador_persistencia: VerificadorPersistencia | None = (
    VerificadorPersistenciaSqlalchemy(_engine_persistencia)
    if _engine_persistencia is not None
    else None
)


@asynccontextmanager
async def _ciclo_vida_aplicacao(_aplicacao: FastAPI) -> AsyncIterator[None]:
    """Libera recursos da engine quando o processo ASGI é encerrado.

    O contexto mantém os recursos disponíveis durante a execução e descarta a
    engine assíncrona ao sair. Ele existe para evitar conexões ou pools abertos
    após o encerramento da aplicação.
    """
    try:
        yield
    finally:
        if _engine_persistencia is not None:
            await _engine_persistencia.dispose()

# Proveniência: decision-analysis prompts/backend/20260913-fundamentos-fastapi-v001.md#v001
app = create_app(
    autenticador_sessao=AutenticadorSessaoIndisponivel(),
    verificador_persistencia=_verificador_persistencia,
    lifespan=_ciclo_vida_aplicacao,
)
