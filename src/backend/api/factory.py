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
)
from backend.api.cadastro_acesso import (
    criar_router as criar_router_cadastro_acesso,
)
from backend.api.dados_contato import (
    AtualizacaoDadosContatoExecutor,
)
from backend.api.dados_contato import (
    criar_router as criar_router_dados_contato,
)
from backend.api.perfil_estudante import (
    EdicaoPerfilExecutor,
    ExclusaoPerfilExecutor,
)
from backend.api.perfil_estudante import (
    criar_router as criar_router_perfil,
)
from backend.api.projeto_academico import (
    CadastroProjetoAcademicoExecutor,
)
from backend.api.projeto_academico import (
    criar_router as criar_router_projeto_academico,
)

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
from backend.api.versao_curriculo import (
    EdicaoVersaoCurriculoExecutor,
)
from backend.api.versao_curriculo import (
    criar_router as criar_router_versao_curriculo,
)


def create_app(
    cadastrar_estudante: CadastroEstudanteExecutor | None = None,
    acessar_estudante: AcessoEstudanteExecutor | None = None,
    derivador_senha: DerivadorSenha | None = None,
    editar_perfil: EdicaoPerfilExecutor | None = None,
    excluir_perfil: ExclusaoPerfilExecutor | None = None,
    atualizar_dados_contato: AtualizacaoDadosContatoExecutor | None = None,
    cadastrar_projeto_academico: CadastroProjetoAcademicoExecutor | None = None,
    editar_versao_curriculo: EdicaoVersaoCurriculoExecutor | None = None,
) -> FastAPI:
    """Cria a aplicação HTTP e registra as rotas com dependências injetadas.

    A função instancia FastAPI e inclui os routers de cadastro/acesso, perfil,
    dados de contato, projetos acadêmicos e versões de currículo com os
    executores recebidos; ausências permanecem explícitas e são traduzidas por
    cada router em indisponibilidade. Ela existe para concentrar a composição
    na camada externa, mantendo Application e domínio livres do framework.
    """
    app = FastAPI()
    app.include_router(criar_router_cadastro_acesso(cadastrar_estudante, acessar_estudante, derivador_senha))
    app.include_router(criar_router_perfil(editar_perfil, excluir_perfil))
    app.include_router(criar_router_dados_contato(atualizar_dados_contato))
    app.include_router(criar_router_projeto_academico(cadastrar_projeto_academico))
    app.include_router(criar_router_versao_curriculo(editar_versao_curriculo))
    return app