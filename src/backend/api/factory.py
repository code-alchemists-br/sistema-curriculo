"""Compõe a aplicação FastAPI e suas dependências de interface.

A fábrica registra routers a partir de capacidades recebidas da composição
externa, sem fazer a API abrir conexões ou conhecer persistência. Ela existe
para manter o ponto ASGI importável e permitir que ambientes escolham adapters.
"""

from fastapi import FastAPI

from backend.api.cadastro_acesso import (
    AcessoEstudanteExecutor,
    CadastroEstudanteExecutor,
    DerivadorSenha,
    criar_router,
)


def create_app(
    cadastrar_estudante: CadastroEstudanteExecutor | None = None,
    acessar_estudante: AcessoEstudanteExecutor | None = None,
    derivador_senha: DerivadorSenha | None = None,
) -> FastAPI:
    """Cria a aplicação HTTP e registra as rotas com dependências injetadas.

    A função instancia FastAPI e inclui o router de cadastro/acesso com os
    executores recebidos; ausências permanecem explícitas e são traduzidas pelo
    router em indisponibilidade. Ela existe para concentrar a composição na
    camada externa, mantendo Application e domínio livres do framework.
    """
    app = FastAPI()
    app.include_router(criar_router(cadastrar_estudante, acessar_estudante, derivador_senha))
    return app
