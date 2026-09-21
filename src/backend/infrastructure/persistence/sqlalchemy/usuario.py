"""Mapeia a conta em colunas externas para preservar o domínio imutável."""

from uuid import UUID

from sqlalchemy import Text, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.usuario import Usuario
from backend.domain.value_objects import Email, HashSenha, Nome, UsuarioId

# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001


class Base(DeclarativeBase):
    """Centraliza o registro ORM usando a base declarativa do SQLAlchemy.

    A metadata compartilhada reúne os modelos externos para que Alembic descubra
    as tabelas Code First sem instrumentar entidades de domínio.
    """


class UsuarioRegistro(Base):
    """Representa a conta persistida por colunas UUID e textuais não nulas.

    O modelo declara chave primária e unicidade de e-mail na infraestrutura,
    permitindo armazenar Usuario sem alterar sua imutabilidade ou value objects.
    """

    __tablename__ = "usuarios"
    __table_args__ = (UniqueConstraint("email", name="uq_usuarios_email"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    hash_senha: Mapped[str] = mapped_column(Text, nullable=False)


def para_registro(usuario: Usuario) -> UsuarioRegistro:
    """Converte o agregado em registro extraindo valores primitivos dos VOs.

    A conversão cria uma instância externa sem modificar o agregado, para que
    a sessão ORM persista UUID, nome, e-mail normalizado e hash já derivado.
    """
    return UsuarioRegistro(
        id=usuario.id.valor,
        nome=usuario.nome.valor,
        email=usuario.email.valor,
        hash_senha=usuario.hash_senha.valor,
    )


def para_usuario(registro: UsuarioRegistro) -> Usuario:
    """Converte o registro ORM recuperado em agregado imutável do domínio.

    A função recria os value objects a partir das colunas já persistidas, sem
    devolver o modelo instrumentado do ORM para as camadas internas. Ela existe
    para preservar a fronteira entre persistência SQLAlchemy e Application.
    """
    return Usuario(
        id=UsuarioId(registro.id),
        nome=Nome(registro.nome),
        email=Email(registro.email),
        hash_senha=HashSenha(registro.hash_senha),
    )
