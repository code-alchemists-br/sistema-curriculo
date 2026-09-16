"""Configura migrations Alembic sem iniciar a aplicação HTTP.

O ambiente importa a metadata central, exige ``DATABASE_URL`` e adapta a conexão
assíncrona para as operações síncronas internas do Alembic. Ele existe para
executar migrations Code First de forma reprodutível e independente da API.
"""

import asyncio
import os

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from backend.infrastructure.persistence.sqlalchemy.metadata import metadata


# Proveniência: decision-analysis prompts/backend/20260916-estrutura-alembic-code-first-v001.md#v001
config = context.config
target_metadata = metadata


def _database_url() -> str:
    """Obtém a URL operacional obrigatória para a migration.

    A função lê exclusivamente ``DATABASE_URL`` e rejeita ausência para impedir
    que uma migration use configuração versionada ou inferida. Ela existe para
    manter credenciais e destinos fora do repositório.
    """
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL deve ser definida para executar Alembic.")
    return database_url


def run_migrations_offline() -> None:
    """Configura geração SQL sem abrir conexão de banco.

    A função usa a URL operacional e a metadata explícita para produzir SQL de
    migration offline. Ela existe para suportar fluxos controlados sem iniciar a
    aplicação ou criar tabelas automaticamente.
    """
    context.configure(url=_database_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Executa migrations usando uma conexão adaptada pelo Alembic.

    A função configura a metadata e roda a transação na conexão recebida do
    engine assíncrono. Ela existe para separar a ponte síncrona do Alembic da
    criação operacional do engine.
    """
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Abre engine assíncrono temporário e aplica migrations.

    A função cria o engine somente para o comando Alembic, usa ``run_sync`` para
    executar sua ponte interna e o descarta ao final. Ela existe para manter a
    migration compatível com Psycopg assíncrono sem criar engine da aplicação.
    """
    config.set_main_option("sqlalchemy.url", _database_url())
    connectable = async_engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
