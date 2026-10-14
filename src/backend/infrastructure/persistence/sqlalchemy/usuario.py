"""Mapeia a conta em colunas externas para preservar o domínio imutável."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, DateTime, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.usuario import Usuario
from backend.domain.value_objects import (
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    Cidade,
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
    """Representa conta e contato em colunas Code First opcionais ou obrigatórias.

    O modelo declara chave, credenciais, exclusão lógica e campos de contato
    com campos pessoais opcionais para perfis anteriores à coleta. Ele existe
    para persistir os valores necessários à consulta sem alterar o domínio.
    """

    __tablename__ = "usuarios"
    __table_args__ = (UniqueConstraint("email", name="uq_usuarios_email"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    hash_senha: Mapped[str] = mapped_column(Text, nullable=False)
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    endereco: Mapped[str | None] = mapped_column(Text, nullable=True)
    telefones: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    cidade: Mapped[str | None] = mapped_column(Text, nullable=True)
    linkedin: Mapped[str | None] = mapped_column(Text, nullable=True)
    curriculo_lattes: Mapped[str | None] = mapped_column(Text, nullable=True)


def para_registro(usuario: Usuario) -> UsuarioRegistro:
    """Converte o agregado em registro extraindo valores primitivos dos VOs.

    A conversão cria uma instância externa sem modificar o agregado, para que
    a sessão ORM persista identidade, estado de exclusão e dados de contato
    como valores primitivos separados do modelo de domínio.
    """
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    contato = usuario.dados_contato
    return UsuarioRegistro(
        id=usuario.id.valor,
        nome=usuario.nome.valor,
        email=usuario.email.valor,
        hash_senha=usuario.hash_senha.valor,
        deleted_at=usuario.deleted_at,
        endereco=contato.endereco.valor if contato is not None else None,
        telefones=(
            [telefone.valor for telefone in contato.telefones]
            if contato is not None
            else None
        ),
        cidade=(
            contato.cidade.valor
            if contato is not None and contato.cidade is not None
            else None
        ),
        linkedin=contato.linkedin if contato is not None else None,
        curriculo_lattes=contato.curriculo_lattes if contato is not None else None,
    )


def para_usuario(registro: UsuarioRegistro) -> Usuario:
    """Converte o registro ORM recuperado em agregado imutável do domínio.

    A função recria value objects, dados de contato e estado de exclusão a
    partir das colunas persistidas, sem devolver o modelo instrumentado do ORM.
    Ela existe para preservar a fronteira entre persistência e Application.
    """
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    dados_contato = None
    if registro.endereco is not None or registro.telefones is not None:
        dados_contato = DadosContato(
            endereco=Endereco(registro.endereco or ""),
            telefones=tuple(Telefone(valor) for valor in (registro.telefones or [])),
            linkedin=registro.linkedin,
            curriculo_lattes=registro.curriculo_lattes,
            cidade=Cidade(registro.cidade) if registro.cidade is not None else None,
        )
    return Usuario(
        id=UsuarioId(registro.id),
        nome=Nome(registro.nome),
        email=Email(registro.email),
        hash_senha=HashSenha(registro.hash_senha),
        deleted_at=registro.deleted_at,
        dados_contato=dados_contato,
    )
