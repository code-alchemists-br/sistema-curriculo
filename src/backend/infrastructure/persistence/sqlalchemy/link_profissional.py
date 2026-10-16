"""Mapeia links profissionais entre o domínio e as colunas SQLAlchemy externas.

O módulo conserva detalhes de tabela e chave técnica fora do domínio. Ele
existe para persistir links profissionais reutilizáveis sem permitir que modelos
ORM atravessem as fronteiras internas.
"""

from uuid import UUID

from sqlalchemy import ForeignKey, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.domain.itens_perfil import LinkProfissional
from backend.domain.value_objects import LinkProfissionalId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class LinkProfissionalRegistro(Base):
    """Representa um link profissional nas colunas relacionais da aplicação.

    O mapeamento armazena o rótulo descritivo, o endereço URL e a chave
    canônica url_normalizada calculada pelo domínio, com unicidade por usuário e
    URL normalizada. Ele existe para reforçar no banco a mesma identidade lógica
    usada pelo caso de uso.
    """

    __tablename__ = "links_profissionais"
    __table_args__ = (
        UniqueConstraint(
            "usuario_id",
            "url_normalizada",
            name="uq_links_profissionais_usuario_url_normalizada",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("usuarios.id", name="fk_links_profissionais_usuario_id_usuarios"),
        nullable=False,
    )
    rotulo: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    url_normalizada: Mapped[str] = mapped_column(Text, nullable=False)


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def para_registro(link: LinkProfissional) -> LinkProfissionalRegistro:
    """Converte um link profissional válido para seu registro persistível no SQLAlchemy.

    A função extrai identificadores e leva a chave canônica já calculada para o ORM.
    Ela existe para evitar que o banco defina política própria de normalização
    ou receba entidades de domínio.
    """
    return LinkProfissionalRegistro(
        id=link.id.valor,
        usuario_id=link.usuario_id.valor,
        rotulo=link.rotulo,
        url=link.url,
        url_normalizada=link.url_normalizada,
    )


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def para_link_profissional(registro: LinkProfissionalRegistro) -> LinkProfissional:
    """Reconstrói um link profissional de domínio a partir de um registro ORM persistido.

    A função recria value objects tipados, reexecutando as invariantes da
    entidade ao cruzar a fronteira. Ela existe para impedir que detalhes
    instrumentados do SQLAlchemy sejam usados nas camadas internas.
    """
    return LinkProfissional(
        id=LinkProfissionalId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        rotulo=registro.rotulo,
        url=registro.url,
    )
