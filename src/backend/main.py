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
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.api.factory import create_app
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.application.ports import GeradorUsuarioId, VerificadorSenha
from backend.application.saude import VerificadorPersistencia
from backend.application.sessoes import CriadorSessao
from backend.configuracao_logging import configurar_logging
from backend.infrastructure.identificadores.geradores import GeradorUsuarioIdUuid4
from backend.infrastructure.persistence.sqlalchemy.acesso_estudante import (
    AcessarEstudanteSqlAlchemy,
    AutenticadorSessaoSqlAlchemy,
    CriadorSessaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.cadastro_estudante import (
    CadastroEstudanteSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.verificador_persistencia import (
    VerificadorPersistenciaSqlalchemy,
)
from backend.infrastructure.security.autenticador_sessao_indisponivel import (
    AutenticadorSessaoIndisponivel,
)
from backend.infrastructure.security.senhas import DerivadorSenhaScrypt

configurar_logging()

ORIGENS_CORS_DESENVOLVIMENTO = (
    "http://127.0.0.1:5173",
    "http://localhost:5173",
)


def _obter_origens_cors(valor_configurado: str | None) -> tuple[str, ...]:
    """Define as origens permitidas para chamadas HTTP feitas pelo navegador.

    A função usa as duas origens locais do Vite quando a variável não foi
    definida e, quando foi, divide sua lista separada por vírgulas removendo
    espaços e valores vazios. Ela existe para liberar o desenvolvimento local
    sem tornar CORS aberto e permitir que cada ambiente publique suas origens.
    """
    if not valor_configurado:
        return ORIGENS_CORS_DESENVOLVIMENTO
    return tuple(
        origem.strip()
        for origem in valor_configurado.split(",")
        if origem.strip()
    )


def _configurar_cors(aplicacao: FastAPI, origens: tuple[str, ...]) -> None:
    """Instala a política CORS que protege e permite o frontend configurado.

    A função registra middleware com credenciais, métodos e cabeçalhos usados
    pela API, restringindo as origens à lista recebida. Ela existe para que o
    navegador possa chamar a API de outra porta sem expor a aplicação a todas
    as origens ou duplicar configuração nos controllers.
    """
    aplicacao.add_middleware(
        CORSMiddleware,
        allow_origins=list(origens),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type"],
    )


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


def _criar_cadastrar_estudante(
    engine: AsyncEngine | None,
    gerador_usuario_id: GeradorUsuarioId | None = None,
) -> CadastroEstudanteSqlAlchemy | None:
    """Compõe o executor transacional de cadastro quando há persistência.

    A função cria uma fábrica de sessões assíncronas e combina o adapter de
    transação com o gerador de UUID da infraestrutura; sem engine, mantém a
    ausência explícita tratada pela API. Ela existe para habilitar o cadastro
    real sem introduzir dependências de banco no controller ou na Application.
    """
    if engine is None:
        return None
    sessoes = async_sessionmaker(engine, expire_on_commit=False)
    return CadastroEstudanteSqlAlchemy(
        sessoes,
        gerador_usuario_id or GeradorUsuarioIdUuid4(),
    )


def _criar_sessoes_persistencia(
    engine: AsyncEngine | None,
) -> async_sessionmaker[AsyncSession] | None:
    """Cria a fábrica de sessões reutilizada pelos fluxos de acesso e sessão.

    A função vincula sessões assíncronas à engine disponível sem abrir conexão;
    na ausência de banco, devolve ausência explícita. Ela existe para que login
    e autenticação compartilhem uma configuração de persistência, não sessões.
    """
    if engine is None:
        return None
    return async_sessionmaker(engine, expire_on_commit=False)


def _criar_acessar_estudante(
    sessoes: async_sessionmaker[AsyncSession] | None,
    verificador_senha: VerificadorSenha,
) -> AcessarEstudanteSqlAlchemy | None:
    """Compõe o executor de login somente quando existe persistência configurada.

    A função conecta a fábrica de sessões ao adapter de acesso e mantém a
    indisponibilidade explícita sem banco. Ela existe para não expor um login
    aparentemente funcional quando as credenciais não podem ser consultadas.
    """
    return AcessarEstudanteSqlAlchemy(sessoes, verificador_senha) if sessoes else None


def _criar_criador_sessao(
    sessoes: async_sessionmaker[AsyncSession] | None,
) -> CriadorSessao | None:
    """Compõe a emissão persistida de sessão quando há banco disponível.

    A função entrega a fábrica de sessões ao adapter transacional ou devolve
    ausência para a API traduzir em indisponibilidade. Ela existe para impedir
    que login emita cookie sem armazenar sua sessão correspondente.
    """
    return CriadorSessaoSqlAlchemy(sessoes) if sessoes else None


def _criar_autenticador_sessao(
    sessoes: async_sessionmaker[AsyncSession] | None,
) -> AutenticadorSessao:
    """Escolhe o autenticador persistido ou a implementação indisponível.

    A função cria o adapter que consulta sessões por requisição quando há banco
    e preserva a negação explícita nos ambientes sem persistência. Ela existe
    para manter a proteção das rotas coerente com a capacidade de login.
    """
    return (
        AutenticadorSessaoSqlAlchemy(sessoes)
        if sessoes
        else AutenticadorSessaoIndisponivel()
    )


_engine_persistencia = _criar_engine_persistencia(
    os.environ.get("DATABASE_URL")
)
_verificador_persistencia: VerificadorPersistencia | None = (
    VerificadorPersistenciaSqlalchemy(_engine_persistencia)
    if _engine_persistencia is not None
    else None
)
_cadastrar_estudante = _criar_cadastrar_estudante(_engine_persistencia)
_sessoes_persistencia = _criar_sessoes_persistencia(_engine_persistencia)
_derivador_senha = DerivadorSenhaScrypt()
_acessar_estudante = _criar_acessar_estudante(
    _sessoes_persistencia,
    _derivador_senha,
)
_criador_sessao = _criar_criador_sessao(_sessoes_persistencia)
_autenticador_sessao = _criar_autenticador_sessao(_sessoes_persistencia)


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
    cadastrar_estudante=_cadastrar_estudante,
    acessar_estudante=_acessar_estudante,
    criador_sessao=_criador_sessao,
    derivador_senha=_derivador_senha,
    autenticador_sessao=_autenticador_sessao,
    verificador_persistencia=_verificador_persistencia,
    lifespan=_ciclo_vida_aplicacao,
)
_configurar_cors(app, _obter_origens_cors(os.environ.get("CORS_ALLOWED_ORIGINS")))
