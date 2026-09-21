"""Expõe os casos de uso internos da aplicação de currículos.

O pacote organiza a orquestração entre agregados do domínio e portas internas,
sem importar API, ORM ou adaptadores concretos. Ele existe para preservar as
dependências apontadas para dentro e permitir que interfaces externas componham
os casos de uso posteriormente.
"""

# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
from backend.application.cadastro_estudante import (
    CadastrarEstudante,
    CadastrarEstudanteEntrada,
    EmailJaCadastrado,
)
from backend.application.acesso_estudante import (
    AcessarEstudante,
    AcessarEstudanteEntrada,
    CredenciaisInvalidas,
)
from backend.application.ports import (
    GeradorUsuarioId,
    Relogio,
    RepositorioUsuario,
    VerificadorSenha,
)
# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from backend.application.ports import (
    GeradorExperienciaProfissionalId,
    RepositorioExperienciaProfissional,
)

# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from backend.application.cadastro_experiencia_profissional import (
    CadastrarExperienciaProfissional,
    CadastrarExperienciaProfissionalEntrada,
)

# Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001
from backend.application.perfil_estudante import (
    EditarPerfil,
    EditarPerfilEntrada,
    ExcluirPerfil,
    ExcluirPerfilEntrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)

__all__ = [
    "CadastrarEstudante",
    "CadastrarEstudanteEntrada",
    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    "CadastrarExperienciaProfissional",
    "CadastrarExperienciaProfissionalEntrada",
    "AcessarEstudante",
    "AcessarEstudanteEntrada",
    "CredenciaisInvalidas",
    "EmailJaCadastrado",
    # Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001
    "EditarPerfil",
    "EditarPerfilEntrada",
    "ExcluirPerfil",
    "ExcluirPerfilEntrada",
    "GeradorUsuarioId",
    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    "GeradorExperienciaProfissionalId",
    "PerfilExcluido",
    "PerfilNaoEncontrado",
    "Relogio",
    "RepositorioUsuario",
    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    "RepositorioExperienciaProfissional",
    "VerificadorSenha",
]
