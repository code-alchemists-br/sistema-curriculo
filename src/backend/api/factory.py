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
    criar_router as criar_router_cadastro_acesso,
)
from backend.api.perfil_estudante import (
    EdicaoPerfilExecutor,
    ExclusaoPerfilExecutor,
    criar_router as criar_router_perfil,
)


def create_app(
    cadastrar_estudante: CadastroEstudanteExecutor | None = None,
    acessar_estudante: AcessoEstudanteExecutor | None = None,
    derivador_senha: DerivadorSenha | None = None,
    editar_perfil: EdicaoPerfilExecutor | None = None,
    excluir_perfil: ExclusaoPerfilExecutor | None = None,
) -> FastAPI:
    """Cria a aplicação HTTP e registra as rotas com dependências injetadas.

    A função instancia FastAPI e inclui os routers de cadastro/acesso e de
    perfil com os executores recebidos; ausências permanecem explícitas e são
    traduzidas por cada router em indisponibilidade. Ela existe para
    concentrar a composição na camada externa, mantendo Application e domínio
    livres do framework.
    """
    app = FastAPI()
    app.include_router(criar_router_cadastro_acesso(cadastrar_estudante, acessar_estudante, derivador_senha))
    app.include_router(criar_router_perfil(editar_perfil, excluir_perfil))
    return app