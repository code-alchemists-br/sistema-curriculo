"""Expõe o núcleo de domínio independente da aplicação de currículos.

O módulo reúne a API pública de entidades, agregados e value objects sem
importar frameworks, persistência ou transporte. Ele existe para que camadas
internas possam trabalhar com regras de negócio estáveis e para que adapters
futuros dependam do domínio, e não o contrário.
"""

# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
from backend.domain.curriculo import Curriculo
from backend.domain.entities import (
    Competencia,
    Documento,
    ExperienciaProfissional,
    FormacaoAcademica,
    Idioma,
    ProjetoAcademico,
    Usuario,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.value_objects import (
    CompetenciaId,
    CurriculoId,
    DocumentoId,
    Email,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    HashSenha,
    IdiomaId,
    Nome,
    Periodo,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    UsuarioId,
)

__all__ = [
    "Competencia",
    "CompetenciaId",
    "Curriculo",
    "CurriculoId",
    "Documento",
    "DocumentoId",
    "Email",
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
    "Usuario",
    "UsuarioId",
]
