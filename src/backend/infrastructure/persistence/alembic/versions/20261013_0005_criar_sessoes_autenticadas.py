"""Cria armazenamento server-side para sessões opacas revogáveis."""

import sqlalchemy as sa
from alembic import op

revision = "20261013_0005"
down_revision = "20261013_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cria tabela de sessão com digest único e vínculo à conta.

    O schema guarda datas absolutas e revogação, sem coluna para token bruto.
    A migration existe para habilitar validação e logout server-side.
    """
    op.create_table(
        "sessoes_autenticadas",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("usuario_id", sa.Uuid(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("criada_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expira_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revogada_em", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index("ix_sessoes_autenticadas_usuario_id", "sessoes_autenticadas", ["usuario_id"])


def downgrade() -> None:
    """Remove índice e tabela de sessões desta revisão.

    A reversão descarta sessões existentes, invalidando suas credenciais. Ela
    existe para permitir rollback explícito do schema.
    """
    op.drop_index("ix_sessoes_autenticadas_usuario_id", table_name="sessoes_autenticadas")
    op.drop_table("sessoes_autenticadas")
