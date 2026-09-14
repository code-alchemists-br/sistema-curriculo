"""Define entidades de conta e itens reutilizáveis do perfil profissional.

As entidades preservam identidade e proprietário explícitos, mas não conhecem
ORM, tabelas ou APIs. Elas existem para representar os dados que um usuário pode
reutilizar entre versões independentes de currículo.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.domain.value_objects import (
    CompetenciaId,
    DocumentoId,
    Email,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    HashSenha,
    IdiomaId,
    Nome,
    Periodo,
    ProjetoAcademicoId,
    UsuarioId,
)


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class Usuario:
    """Representa o aggregate root da conta e identidade do usuário.

    A entidade reúne uma identidade tipada, nome, e-mail e hash de senha já
    derivado, todos validados por value objects. Ela existe como proprietário
    conceitual de currículos e itens de perfil, sem acoplar autenticação, sessão
    ou recuperação de senha à primeira fatia de domínio.
    """

    id: UsuarioId
    nome: Nome
    email: Email
    hash_senha: HashSenha


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class FormacaoAcademica:
    """Representa uma formação acadêmica reutilizável pertencente a um usuário.

    A entidade combina sua identidade, proprietário e informações descritivas
    com um ``Periodo`` validado. Ela existe para que uma formação possa aparecer
    em mais de uma versão de currículo sem se tornar parte interna de um agregado
    de currículo.
    """

    id: FormacaoAcademicaId
    usuario_id: UsuarioId
    instituicao: str
    curso: str
    nivel: str
    periodo: Periodo
    status: str


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class ExperienciaProfissional:
    """Representa uma experiência profissional reutilizável do usuário.

    A entidade mantém identidade, proprietário, descrição profissional e um
    intervalo cronologicamente válido. Ela existe para preservar a experiência
    como item independente que currículos distintos podem referenciar.
    """

    id: ExperienciaProfissionalId
    usuario_id: UsuarioId
    empresa: str
    cargo: str
    descricao: str
    periodo: Periodo


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class ProjetoAcademico:
    """Representa um projeto acadêmico reutilizável pertencente a um usuário.

    A entidade agrupa identidade, proprietário e os textos descritos no DER sem
    impor vocabulário para tecnologias. Ela existe para permitir que projetos
    sejam selecionados em diferentes versões de currículo.
    """

    id: ProjetoAcademicoId
    usuario_id: UsuarioId
    titulo: str
    descricao: str
    tecnologias: str


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class Competencia:
    """Representa uma competência reutilizável pertencente a um usuário.

    A entidade identifica a competência e registra sua descrição e nível como
    textos, pois o vocabulário de níveis ainda não foi especificado. Ela existe
    para que o perfil seja independente de uma versão particular de currículo.
    """

    id: CompetenciaId
    usuario_id: UsuarioId
    descricao: str
    nivel: str


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class Idioma:
    """Representa um idioma e nível reutilizáveis pertencentes a um usuário.

    A entidade mantém a identidade e proprietário tipados e conserva o nível
    como texto enquanto não houver vocabulário aprovado. Ela existe para que o
    mesmo idioma possa compor mais de uma versão de currículo.
    """

    id: IdiomaId
    usuario_id: UsuarioId
    idioma: str
    nivel: str


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class Documento:
    """Representa metadados de um documento reutilizável do usuário.

    A entidade guarda identidade, proprietário e metadados descritos no DER sem
    abrir arquivo ou acessar armazenamento. Ela existe para que currículos
    referenciem documentos sem depender de adaptadores de upload ou arquivos.
    """

    id: DocumentoId
    usuario_id: UsuarioId
    nome_arquivo: str
    tipo_arquivo: str
    url_armazenamento: str
