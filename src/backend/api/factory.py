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

# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
from backend.api.competencia import CadastroCompetenciaExecutor
from backend.api.competencia import criar_router as criar_router_competencia
from backend.api.dados_contato import (
    AtualizacaoDadosContatoExecutor,
)
from backend.api.dados_contato import (
    criar_router as criar_router_dados_contato,
)

# Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
from backend.api.exclusao_versao_curriculo import (
    ExclusaoVersaoCurriculoExecutor,
)
from backend.api.exclusao_versao_curriculo import (
    criar_router as criar_router_exclusao_versao_curriculo,
)
from backend.api.experiencia_profissional import (
    CadastroExperienciaProfissionalExecutor,
)
from backend.api.experiencia_profissional import (
    criar_router as criar_router_experiencia_profissional,
)

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
from backend.api.itens_versao_curriculo import (
    DesselecaoItemVersaoCurriculoExecutor,
    SelecaoItemVersaoCurriculoExecutor,
)
from backend.api.itens_versao_curriculo import (
    criar_router as criar_router_itens_versao_curriculo,
)

# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
from backend.api.listagem_versoes_curriculo import (
    ListagemVersoesCurriculoExecutor,
)
from backend.api.listagem_versoes_curriculo import (
    criar_router as criar_router_listagem_versoes_curriculo,
)
from backend.api.middleware_autenticacao import MiddlewareAutenticacaoSessao
from backend.api.perfil_estudante import (
    AtualizacaoPerfilCompletoExecutor,
    ConsultaPerfilExecutor,
    EdicaoPerfilExecutor,
    ExclusaoPerfilExecutor,
)
from backend.api.perfil_estudante import (
    criar_router as criar_router_perfil,
)

# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
from backend.api.previa_versao_curriculo import (
    PreviaVersaoCurriculoExecutor,
)
from backend.api.previa_versao_curriculo import (
    criar_router as criar_router_previa_versao_curriculo,
)
from backend.api.projeto_academico import (
    CadastroProjetoAcademicoExecutor,
)
from backend.api.projeto_academico import (
    criar_router as criar_router_projeto_academico,
)
from backend.api.sessoes import criar_router as criar_router_sessoes

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
from backend.api.versao_curriculo import (
    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    CriacaoVersaoCurriculoExecutor,
    EdicaoVersaoCurriculoExecutor,
)
from backend.api.versao_curriculo import (
    criar_router as criar_router_versao_curriculo,
)
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.application.sessoes import CriadorSessao, RevogadorSessao


def create_app(
    cadastrar_estudante: CadastroEstudanteExecutor | None = None,
    acessar_estudante: AcessoEstudanteExecutor | None = None,
    derivador_senha: DerivadorSenha | None = None,
    editar_perfil: EdicaoPerfilExecutor | None = None,
    excluir_perfil: ExclusaoPerfilExecutor | None = None,
    atualizar_dados_contato: AtualizacaoDadosContatoExecutor | None = None,
    cadastrar_projeto_academico: CadastroProjetoAcademicoExecutor | None = None,
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    cadastrar_competencia: CadastroCompetenciaExecutor | None = None,
    editar_versao_curriculo: EdicaoVersaoCurriculoExecutor | None = None,
    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    criar_versao_curriculo: CriacaoVersaoCurriculoExecutor | None = None,
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    selecionar_item_versao_curriculo: SelecaoItemVersaoCurriculoExecutor | None = None,
    desselecionar_item_versao_curriculo: DesselecaoItemVersaoCurriculoExecutor
    | None = None,
    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    listar_versoes_curriculo: ListagemVersoesCurriculoExecutor | None = None,
    criador_sessao: CriadorSessao | None = None,
    cadastrar_experiencia_profissional: CadastroExperienciaProfissionalExecutor
    | None = None,
    # Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
    gerar_previa_versao_curriculo: PreviaVersaoCurriculoExecutor | None = None,
    revogador_sessao: RevogadorSessao | None = None,
    autenticador_sessao: AutenticadorSessao | None = None,
    # Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
    excluir_versao_curriculo: ExclusaoVersaoCurriculoExecutor | None = None,
    atualizar_perfil_completo: AtualizacaoPerfilCompletoExecutor | None = None,
    consultar_perfil: ConsultaPerfilExecutor | None = None,
) -> FastAPI:
    """Cria a aplicação HTTP e registra as rotas com dependências injetadas.

    A função instancia FastAPI e inclui os routers de cadastro/acesso, perfil,
    dados completos de perfil, contato, projetos acadêmicos, competências, versões de currículo,
    seleção de itens, listagem, exclusão de versão, experiências profissionais
    e prévia com os executores recebidos; ausências permanecem explícitas e são
    traduzidas por cada router em indisponibilidade. Quando um autenticador é
    fornecido, instala o middleware que valida sessões nas rotas privadas. Ela
    existe para concentrar a composição na camada externa, mantendo Application
    e domínio livres do framework.
    """
    app = FastAPI()
    if autenticador_sessao is not None:
        app.add_middleware(
            MiddlewareAutenticacaoSessao, autenticador=autenticador_sessao
        )
    app.include_router(
        criar_router_cadastro_acesso(
            cadastrar_estudante, acessar_estudante, derivador_senha, criador_sessao
        )
    )
    app.include_router(
        criar_router_perfil(
            editar_perfil,
            excluir_perfil,
            atualizar_perfil_completo,
            consultar_perfil,
        )
    )
    app.include_router(criar_router_dados_contato(atualizar_dados_contato))
    app.include_router(criar_router_projeto_academico(cadastrar_projeto_academico))
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    app.include_router(criar_router_competencia(cadastrar_competencia))
    app.include_router(
        criar_router_versao_curriculo(editar_versao_curriculo, criar_versao_curriculo)
    )
    app.include_router(
        criar_router_itens_versao_curriculo(
            selecionar_item_versao_curriculo, desselecionar_item_versao_curriculo
        )
    )
    app.include_router(
        criar_router_listagem_versoes_curriculo(listar_versoes_curriculo)
    )
    app.include_router(
        criar_router_experiencia_profissional(cadastrar_experiencia_profissional)
    )
    app.include_router(
        criar_router_previa_versao_curriculo(gerar_previa_versao_curriculo)
    )
    app.include_router(criar_router_exclusao_versao_curriculo(excluir_versao_curriculo))
    app.include_router(criar_router_sessoes(revogador_sessao))
    return app
