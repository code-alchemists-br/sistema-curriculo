"""Mapeia solicitações de redefinição sem armazenar tokens em claro."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.persistence.sqlalchemy.usuario import Base


class TokenRecuperacaoSenhaRegistro(Base):
    """Representa token temporário associado a uma conta.

    O mapeamento persiste somente SHA-256, expiração e estado de uso, com
    vínculo obrigatório à conta. Ele existe para suportar consumo único e
    auditoria mínima sem guardar a credencial enviada por e-mail.
    """

    __tablename__ = "tokens_recuperacao_senha"
    __table_args__ = (
        Index("uq_tokens_recuperacao_senha_hash", "token_hash", unique=True),
        Index("ix_tokens_recuperacao_senha_usuario", "usuario_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("usuarios.id", name="fk_tokens_recuperacao_usuario_id_usuarios", ondelete="CASCADE"),
        nullable=False,
    )
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    criada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expira_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    usada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
