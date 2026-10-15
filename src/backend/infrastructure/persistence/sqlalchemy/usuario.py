"""Mapeia a conta em colunas externas para preservar o domínio imutável."""

from uuid import UUID

from sqlalchemy import JSON, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.usuario import Usuario
from backend.domain.value_objects import (
    DadosContato,
    Email,
    Endereco,
    HashSenha,
    Nome,
    Telefone,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001


class Base(DeclarativeBase):
    """Centraliza o registro ORM usando a base declarativa do SQLAlchemy.

    A metadata compartilhada reúne os modelos externos para que Alembic descubra
    as tabelas Code First sem instrumentar entidades de domínio.
    """


class UsuarioRegistro(Base):
    """Representa conta e dados de contato em colunas externas do usuário.

    O modelo declara chave primária, e-mail único e contato anulável para
    preservar contas legadas sem contato. Ele existe para armazenar o agregado
    do domínio em formato relacional sem instrumentá-lo com ORM.
    """

    __tablename__ = "usuarios"
    __table_args__ = (UniqueConstraint("email", name="uq_usuarios_email"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    hash_senha: Mapped[str] = mapped_column(Text, nullable=False)
    endereco: Mapped[str | None] = mapped_column(Text, nullable=True)
    cidade: Mapped[str | None] = mapped_column(Text, nullable=True)
    telefones: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    linkedin: Mapped[str | None] = mapped_column(Text, nullable=True)
    curriculo_lattes: Mapped[str | None] = mapped_column(Text, nullable=True)


def para_registro(usuario: Usuario) -> UsuarioRegistro:
    """Converte o agregado em registro extraindo valores primitivos dos VOs.

    A conversão cria uma instância externa sem modificar o agregado, para que
    a sessão ORM persista identidade, credencial derivada e todos os campos de
    contato serializados como valores primitivos.
    """
    contato = usuario.dados_contato
    return UsuarioRegistro(
        id=usuario.id.valor,
        nome=usuario.nome.valor,
        email=usuario.email.valor,
        hash_senha=usuario.hash_senha.valor,
        endereco=contato.endereco.valor if contato is not None else None,
        cidade=contato.cidade if contato is not None else None,
        telefones=(
            [telefone.valor for telefone in contato.telefones]
            if contato is not None
            else None
        ),
        linkedin=contato.linkedin if contato is not None else None,
        curriculo_lattes=contato.curriculo_lattes if contato is not None else None,
    )


def para_usuario(registro: UsuarioRegistro) -> Usuario:
    """Converte o registro ORM recuperado em agregado imutável do domínio.

    A função recria os value objects a partir das colunas já persistidas e
    compõe contato quando endereço e telefones existem, sem devolver o modelo
    ORM às camadas internas. Ela existe para preservar o limite entre
    persistência SQLAlchemy e Application.
    """
    contato = None
    if registro.endereco is not None and registro.telefones is not None:
        contato = DadosContato(
            endereco=Endereco(registro.endereco),
            telefones=tuple(Telefone(telefone) for telefone in registro.telefones),
            linkedin=registro.linkedin,
            curriculo_lattes=registro.curriculo_lattes,
            cidade=registro.cidade,
        )
    return Usuario(
        id=UsuarioId(registro.id),
        nome=Nome(registro.nome),
        email=Email(registro.email),
        hash_senha=HashSenha(registro.hash_senha),
        dados_contato=contato,
    )
