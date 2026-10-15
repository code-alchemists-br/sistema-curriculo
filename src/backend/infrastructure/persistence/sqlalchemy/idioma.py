"""Mapeia idiomas entre o domínio e as colunas SQLAlchemy externas.

O módulo conserva detalhes de tabela e chave técnica fora do domínio. Ele
existe para persistir idiomas reutilizáveis sem permitir que modelos ORM
atravessem as fronteiras internas.
"""

from uuid import UUID

from sqlalchemy import ForeignKey, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
from backend.domain.itens_perfil import Idioma
from backend.domain.value_objects import IdiomaId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class IdiomaRegistro(Base):
    """Representa um idioma nas colunas relacionais da aplicação.

    O mapeamento armazena os textos exibíveis e a chave canônica calculada pelo
    domínio, com unicidade por proprietário. Ele existe para reforçar no banco
    a mesma identidade lógica usada pelo caso de uso.
    """

    __tablename__ = "idiomas"
    __table_args__ = (
        UniqueConstraint(
            "usuario_id",
            "idioma_normalizado",
            name="uq_idiomas_usuario_idioma_normalizado",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("usuarios.id", name="fk_idiomas_usuario_id_usuarios"),
        nullable=False,
    )
    idioma: Mapped[str] = mapped_column(Text, nullable=False)
    idioma_normalizado: Mapped[str] = mapped_column(Text, nullable=False)
    nivel: Mapped[str] = mapped_column(Text, nullable=False)


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
def para_registro(idioma: Idioma) -> IdiomaRegistro:
    """Converte um idioma válido para seu registro persistível.

    A função extrai identificadores e leva a chave canônica já calculada para o
    ORM. Ela existe para evitar que o banco defina política própria de
    normalização ou receba entidades de domínio.
    """
    return IdiomaRegistro(
        id=idioma.id.valor,
        usuario_id=idioma.usuario_id.valor,
        idioma=idioma.idioma,
        idioma_normalizado=idioma.idioma_normalizado,
        nivel=idioma.nivel,
    )


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
def para_idioma(registro: IdiomaRegistro) -> Idioma:
    """Reconstrói um idioma de domínio a partir de um registro ORM.

    A função recria value objects tipados, reexecutando as invariantes da
    entidade ao cruzar a fronteira. Ela existe para impedir que detalhes
    instrumentados do SQLAlchemy sejam usados nas camadas internas.
    """
    return Idioma(
        id=IdiomaId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        idioma=registro.idioma,
        nivel=registro.nivel,
    )
