"""Expõe o núcleo de domínio independente da aplicação de currículos.

O módulo reúne a API pública de entidades, agregados e value objects sem
importar frameworks, persistência ou transporte. Ele existe para que camadas
internas possam trabalhar com regras de negócio estáveis e para que adapters
futuros dependam do domínio, e não o contrário.
"""

# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
from backend.domain.curriculo import Curriculo
# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.itens_perfil import (
    Competencia,
    Documento,
    ExperienciaProfissional,
    FormacaoAcademica,
    Idioma,
    ProjetoAcademico,
)
# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.usuario import Usuario
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.value_objects import (
    CompetenciaId,
    CurriculoId,
    # Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
    DadosContato,
    DocumentoId,
    Email,
    # Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
    Endereco,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    HashSenha,
    IdiomaId,
    Nome,
    Periodo,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    # Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
    Telefone,
    UsuarioId,
)

__all__ = [
    "Competencia",
    "CompetenciaId",
    "Curriculo",
    "CurriculoId",
    "DadosContato",
    "Documento",
    "DocumentoId",
    "Email",
    "Endereco",
    "ExperienciaProfissional",
    "ExperienciaProfissionalId",
    "FormacaoAcademica",
    "FormacaoAcademicaId",
    "HashSenha",
    "Idioma",
    "IdiomaId",
    "Nome",
    "Periodo",
    "ProjetoAcademico",
    "ProjetoAcademicoId",
    "ReferenciaCurriculo",
    "RegraDeDominioViolada",
    "Telefone",
    "Usuario",
    "UsuarioId",
]