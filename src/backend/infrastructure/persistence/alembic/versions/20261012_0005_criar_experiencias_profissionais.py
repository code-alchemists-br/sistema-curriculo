"""Cria armazenamento Code First para experiências profissionais."""

import sqlalchemy as sa
from alembic import op

revision = "20261012_0005"
down_revision = "20261012_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cria a tabela de experiências profissionais associadas ao estudante.

    A tabela referencia a conta proprietária e preserva as colunas definidas no
    modelo ORM. Ela existe para habilitar persistência Code First do cadastro de
    experiências sem duplicar o mecanismo de sessões já existente.
    """
    op.create_table(
        "experiencias_profissionais",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("empresa", sa.Text(), nullable=False),
        sa.Column("cargo", sa.Text(), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("data_inicio", sa.Date(), nullable=False),
        sa.Column("data_fim", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["usuario_id"], ["usuarios.id"], name="fk_experiencias_usuario_id_usuarios"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Remove a tabela de experiências profissionais em um rollback.

    A reversão descarta somente as experiências persistidas, preservando
    usuários e sessões. Ela existe para permitir rollback explícito desta
    evolução de schema quando a perda desses dados for aceita.
    """
    op.drop_table("experiencias_profissionais")
