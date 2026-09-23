"""Define entidades reutilizáveis que compõem o perfil profissional do usuário.

As entidades mantêm identidade própria e proprietário explícito, sem conhecer
ORM, tabelas ou APIs. Elas existem para separar os itens reutilizáveis das
transições da conta e permitir seu crescimento coeso fora de um módulo genérico.
"""

from __future__ import annotations

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.value_objects import (
    CompetenciaId,
    DocumentoId,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    IdiomaId,
    Periodo,
    ProjetoAcademicoId,
    UsuarioId,
)


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
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


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
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

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def __post_init__(self) -> None:
        """Garante que a experiência profissional contenha os textos essenciais.

        A validação percorre empresa, cargo e descrição, removendo espaços para
        identificar valores ausentes antes que a entidade possa ser usada. Ela
        existe para impedir que o currículo mantenha experiências sem a
        informação mínima necessária para sua apresentação profissional.
        """
        for campo, valor in (
            ("empresa", self.empresa),
            ("cargo", self.cargo),
            ("descrição", self.descricao),
        ):
            if not isinstance(valor, str) or not valor.strip():
                raise RegraDeDominioViolada(
                    f"A experiência profissional exige {campo} preenchido."
                )


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
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

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    def __post_init__(self) -> None:
        """Garante que o projeto acadêmico contenha os textos essenciais.

        A validação percorre título, descrição e tecnologias, removendo espaços
        para identificar valores ausentes antes que a entidade seja utilizada.
        Ela existe para impedir que o perfil mantenha projetos sem informação
        mínima para apresentação em currículos.
        """
        for campo, valor in (
            ("título", self.titulo),
            ("descrição", self.descricao),
            ("tecnologias", self.tecnologias),
        ):
            if not isinstance(valor, str) or not valor.strip():
                raise RegraDeDominioViolada(
                    f"O projeto acadêmico exige {campo} preenchido."
                )


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
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


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
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


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
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
