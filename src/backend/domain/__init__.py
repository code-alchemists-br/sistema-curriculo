"""Expõe o núcleo de domínio independente da aplicação de currículos.

O módulo reúne a API pública de entidades, agregados e value objects sem
importar frameworks, persistência ou transporte. Ele existe para que camadas
internas possam trabalhar com regras de negócio estáveis e para que adapters
futuros dependam do domínio, e não o contrário.
"""

# Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
from backend.domain.associacao_curriculo_vaga import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
)

# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
from backend.domain.curriculo import Curriculo
from backend.domain.exceptions import RegraDeDominioViolada

# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.itens_perfil import (
    TAMANHO_MAXIMO_TEXTO_FORMACAO,
    TAMANHO_MINIMO_TEXTO_FORMACAO,
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    CategoriaCompetencia,
    Competencia,
    Documento,
    ExperienciaProfissional,
    FormacaoAcademica,
    Idioma,
    # Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
    NivelFormacaoAcademica,
    ProjetoAcademico,
    StatusFormacaoAcademica,
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    normalizar_idioma,
)

# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
from backend.domain.revisao_curriculo import (
    PendenciaRevisao,
    ResultadoRevisao,
    SecaoRevisao,
    SeveridadePendencia,
    revisar_curriculo,
)

# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.usuario import Usuario
from backend.domain.value_objects import (
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    Cidade,
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
    # Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
    VagaId,
)

__all__ = [
    # Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
    "AssociacaoCurriculoVaga",
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    "CategoriaCompetencia",
    "ClassificacaoAssociacao",
    "Competencia",
    "CompetenciaId",
    "Curriculo",
    "CurriculoId",
    "Cidade",
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
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    "normalizar_idioma",
    # Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
    "NivelFormacaoAcademica",
    "Periodo",
    "ProjetoAcademico",
    "ProjetoAcademicoId",
    "ReferenciaCurriculo",
    "RegraDeDominioViolada",
    "StatusFormacaoAcademica",
    "TAMANHO_MAXIMO_TEXTO_FORMACAO",
    "TAMANHO_MINIMO_TEXTO_FORMACAO",
    "Telefone",
    "Usuario",
    "UsuarioId",
    # Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
    "VagaId",
    # Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
    "PendenciaRevisao",
    "ResultadoRevisao",
    "SecaoRevisao",
    "SeveridadePendencia",
    "revisar_curriculo",
]
