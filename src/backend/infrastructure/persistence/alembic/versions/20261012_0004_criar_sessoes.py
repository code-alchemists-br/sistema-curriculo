"""Cria armazenamento Code First para metadados de sessões autenticadas."""

import sqlalchemy as sa
from alembic import op

revision = "20261012_0004"
down_revision = "20261007_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cria tabela de sessões vinculada a usuários.

    A revisão persiste hash único e datas de validade/revogação, nunca o token
    em claro. Ela existe para armazenar sessões emitidas no login.
    """
    op.create_table(
        "sessoes",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("criada_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expira_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revogada_em", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["usuario_id"], ["usuarios.id"], name="fk_sessoes_usuario_id_usuarios"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash", name="uq_sessoes_token_hash"),
    )


def downgrade() -> None:
    """Remove a tabela de sessões em rollback explícito da revisão.

    A operação descarta registros de sessão, preservando as contas existentes.
    Ela existe para permitir reverter esta evolução isoladamente.
    """
    op.drop_table("sessoes")
