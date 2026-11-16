"""Cria armazenamento de tokens para recuperação de senha."""

import sqlalchemy as sa
from alembic import op

revision = "20261115_0019"
down_revision = "20261108_0018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cria tabela com resumo único, vínculo de usuário e validade temporal.

    Registra somente o hash do token e indexa a conta para substituir tokens
    anteriores e aplicar contenção de envios. A migration existe para dar
    suporte relacional e reversível ao novo fluxo.
    """
    op.create_table(
        "tokens_recuperacao_senha",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("criada_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expira_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("usada_em", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            name="fk_tokens_recuperacao_usuario_id_usuarios",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uq_tokens_recuperacao_senha_hash",
        "tokens_recuperacao_senha",
        ["token_hash"],
        unique=True,
    )
    op.create_index(
        "ix_tokens_recuperacao_senha_usuario",
        "tokens_recuperacao_senha",
        ["usuario_id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove os índices e a tabela de tokens de recuperação.

    Descarta somente dados temporários de redefinição. A operação existe para
    permitir rollback explícito da migration.
    """
    op.drop_index("ix_tokens_recuperacao_senha_usuario", table_name="tokens_recuperacao_senha")
    op.drop_index("uq_tokens_recuperacao_senha_hash", table_name="tokens_recuperacao_senha")
    op.drop_table("tokens_recuperacao_senha")
