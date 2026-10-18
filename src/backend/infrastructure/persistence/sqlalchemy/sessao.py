"""Mapeia metadados das sessões sem guardar tokens em texto claro."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.persistence.sqlalchemy.usuario import Base


class SessaoRegistro(Base):
    """Representa uma sessão autenticada persistida.

    A tabela associa usuário, hash único do token, validade e revogação. Ela
    existe para sustentar futuras consultas e revogações sem guardar o segredo.
    """

    __tablename__ = "sessoes"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("usuarios.id", name="fk_sessoes_usuario_id_usuarios"), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    criada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expira_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revogada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
