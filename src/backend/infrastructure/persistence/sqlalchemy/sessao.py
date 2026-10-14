"""Mapeia sessões autenticadas para armazenamento revogável server-side.

O modelo mantém somente o digest do token e seu ciclo de vida ligado à conta.
Ele existe para que a API valide e revogue credenciais sem persistir tokens
reutilizáveis em claro.
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.persistence.sqlalchemy.usuario import Base


class SessaoRegistro(Base):
    """Representa uma sessão opaca persistida e revogável.

    A tabela guarda hash único, proprietário, criação, expiração e revogação.
    Ela existe para resolver o principal autenticado em cada requisição.
    """

    __tablename__ = "sessoes_autenticadas"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    criada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expira_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revogada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
