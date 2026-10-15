"""Expõe os casos de uso internos da aplicação de currículos.

O pacote organiza a orquestração entre agregados do domínio e portas internas,
sem importar API, ORM ou adaptadores concretos. Ele existe para preservar as
dependências apontadas para dentro e permitir que interfaces externas componham
os casos de uso posteriormente.
"""

# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
from backend.application.acesso_estudante import (
    AcessarEstudante,
    AcessarEstudanteEntrada,
    CredenciaisInvalidas,
)

# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
from backend.application.cadastro_competencia import (
    CadastrarCompetencia,
    CadastrarCompetenciaEntrada,
    CompetenciaJaCadastrada,
)
from backend.application.cadastro_estudante import (
    CadastrarEstudante,
    CadastrarEstudanteEntrada,
    EmailJaCadastrado,
)

# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from backend.application.cadastro_experiencia_profissional import (
    CadastrarExperienciaProfissional,
    CadastrarExperienciaProfissionalEntrada,
)

# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
from backend.application.cadastro_projeto_academico import (
    CadastrarProjetoAcademico,
    CadastrarProjetoAcademicoEntrada,
)

# Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
from backend.application.dados_contato import (
    AtualizarDadosContato,
    AtualizarDadosContatoEntrada,
)

# Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
from backend.application.exclusao_versao_curriculo import (
    ExcluirVersaoCurriculo,
    ExcluirVersaoCurriculoEntrada,
)

# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
from backend.application.listagem_versoes_curriculo import (
    ListarVersoesCurriculo,
    ListarVersoesCurriculoEntrada,
)

# Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
from backend.application.perfil_estudante import (
    CadastrarFormacaoAcademica,
    CadastrarFormacaoAcademicaEntrada,
    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    EditarFormacaoAcademica,
    EditarFormacaoAcademicaEntrada,
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    ConsultarPerfilEstudante,
    ConsultarPerfilEstudanteEntrada,
    EditarPerfil,
    EditarPerfilEntrada,
    ExcluirPerfil,
    ExcluirPerfilEntrada,
    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    FormacaoAcademicaNaoEncontrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)

# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
from backend.application.ports import (
    # Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
    ConsultaItemPerfil,
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    ConsultaProprietarioItem,
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    GeradorCompetenciaId,
    GeradorCurriculoId,
    GeradorExperienciaProfissionalId,
    GeradorFormacaoAcademicaId,
    GeradorProjetoAcademicoId,
    GeradorUsuarioId,
    Relogio,
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    RepositorioCompetencia,
    RepositorioCurriculo,
    RepositorioExperienciaProfissional,
    RepositorioFormacaoAcademica,
    RepositorioProjetoAcademico,
    RepositorioUsuario,
    VerificadorSenha,
)

# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
from backend.application.previa_versao_curriculo import (
    GerarPreviaVersaoCurriculo,
    GerarPreviaVersaoCurriculoEntrada,
    PreviaVersaoCurriculo,
)

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
from backend.application.selecao_itens_versao_curriculo import (
    DesselecionarItemVersaoCurriculo,
    DesselecionarItemVersaoCurriculoEntrada,
    ItemNaoEncontrado,
    SelecionarItemVersaoCurriculo,
    SelecionarItemVersaoCurriculoEntrada,
)

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
from backend.application.versao_curriculo import (
    CriarVersaoCurriculo,
    CriarVersaoCurriculoEntrada,
    CurriculoNaoEncontrado,
    EditarVersaoCurriculo,
    EditarVersaoCurriculoEntrada,
)

__all__ = [
    "CadastrarEstudante",
    "CadastrarEstudanteEntrada",
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    "CadastrarCompetencia",
    "CadastrarCompetenciaEntrada",
    "CompetenciaJaCadastrada",
    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    "CadastrarExperienciaProfissional",
    "CadastrarExperienciaProfissionalEntrada",
    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    "CadastrarProjetoAcademico",
    "CadastrarProjetoAcademicoEntrada",
    "AcessarEstudante",
    "AcessarEstudanteEntrada",
    # Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
    "AtualizarDadosContato",
    "AtualizarDadosContatoEntrada",
    "CredenciaisInvalidas",
    "EmailJaCadastrado",
    # Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
    "CadastrarFormacaoAcademica",
    "CadastrarFormacaoAcademicaEntrada",
    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    "EditarFormacaoAcademica",
    "EditarFormacaoAcademicaEntrada",
    "FormacaoAcademicaNaoEncontrada",
    "ConsultarPerfilEstudante",
    "ConsultarPerfilEstudanteEntrada",
    # Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001
    "EditarPerfil",
    "EditarPerfilEntrada",
    "ExcluirPerfil",
    "ExcluirPerfilEntrada",
    "GeradorFormacaoAcademicaId",
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    "GeradorCompetenciaId",
    "GeradorUsuarioId",
    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    "GeradorExperienciaProfissionalId",
    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    "GeradorProjetoAcademicoId",
    "PerfilExcluido",
    "PerfilNaoEncontrado",
    "Relogio",
    "RepositorioFormacaoAcademica",
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    "RepositorioCompetencia",
    "RepositorioUsuario",
    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    "RepositorioExperienciaProfissional",
    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    "RepositorioProjetoAcademico",
    "VerificadorSenha",
    # Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
    "CurriculoNaoEncontrado",
    "EditarVersaoCurriculo",
    "EditarVersaoCurriculoEntrada",
    "RepositorioCurriculo",
    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    "CriarVersaoCurriculo",
    "CriarVersaoCurriculoEntrada",
    "GeradorCurriculoId",
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    "ConsultaProprietarioItem",
    "DesselecionarItemVersaoCurriculo",
    "DesselecionarItemVersaoCurriculoEntrada",
    "ItemNaoEncontrado",
    "SelecionarItemVersaoCurriculo",
    "SelecionarItemVersaoCurriculoEntrada",
    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    "ListarVersoesCurriculo",
    "ListarVersoesCurriculoEntrada",
    # Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
    "ExcluirVersaoCurriculo",
    "ExcluirVersaoCurriculoEntrada",
    # Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
    "ConsultaItemPerfil",
    "GerarPreviaVersaoCurriculo",
    "GerarPreviaVersaoCurriculoEntrada",
    "PreviaVersaoCurriculo",
]
