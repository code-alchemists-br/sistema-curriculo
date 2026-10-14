"""Mapeia competências entre o domínio e as colunas SQLAlchemy externas.

O módulo conserva detalhes de tabela, enumeração e chave técnica fora do
domínio. Ele existe para persistir competências reutilizáveis sem permitir que
modelos ORM atravessem as fronteiras internas.
"""

from uuid import UUID

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.itens_perfil import CategoriaCompetencia, Competencia
from backend.domain.value_objects import CompetenciaId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class CompetenciaRegistro(Base):
    """Representa uma competência nas colunas relacionais da aplicação.

    O mapeamento armazena a categoria, os textos exibíveis e a chave canônica
    calculada pelo domínio, com unicidade por proprietário. Ele existe para
    reforçar no banco a mesma identidade lógica usada pelo caso de uso.
    """

    __tablename__ = "competencias"
    __table_args__ = (
        UniqueConstraint(
            "usuario_id",
            "categoria",
            "descricao_normalizada",
            name="uq_competencias_usuario_categoria_descricao_normalizada",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("usuarios.id", name="fk_competencias_usuario_id_usuarios"),
        nullable=False,
    )
    categoria: Mapped[str] = mapped_column(String(32), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    descricao_normalizada: Mapped[str] = mapped_column(Text, nullable=False)
    nivel: Mapped[str] = mapped_column(Text, nullable=False)


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def para_registro(competencia: Competencia) -> CompetenciaRegistro:
    """Converte uma competência válida para seu registro persistível.

    A função extrai identificadores, serializa a categoria controlada e leva a
    chave canônica já calculada para o ORM. Ela existe para evitar que o banco
    defina política própria de normalização ou receba entidades de domínio.
    """
    return CompetenciaRegistro(
        id=competencia.id.valor,
        usuario_id=competencia.usuario_id.valor,
        categoria=competencia.categoria.value,
        descricao=competencia.descricao,
        descricao_normalizada=competencia.descricao_normalizada,
        nivel=competencia.nivel,
    )


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def para_competencia(registro: CompetenciaRegistro) -> Competencia:
    """Reconstrói uma competência de domínio a partir de um registro ORM.

    A função recria value objects e categoria tipada, reexecutando as
    invariantes da entidade ao cruzar a fronteira. Ela existe para impedir que
    detalhes instrumentados do SQLAlchemy sejam usados nas camadas internas.
    """
    return Competencia(
        id=CompetenciaId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        categoria=CategoriaCompetencia(registro.categoria),
        descricao=registro.descricao,
        nivel=registro.nivel,
    )
