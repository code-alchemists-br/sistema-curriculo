"""Cria a tabela de decisões do estudante sobre recomendações da revisão.

Revision ID: 20261023_0016
Revises: 20261017_0015
Create Date: 2026-10-23
"""

import sqlalchemy as sa
from alembic import op

revision = "20261023_0016"
down_revision = "20261017_0015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cria ``decisoes_recomendacao`` com uma decisão por versão e código.

    A chave primária é composta por versão e código, a decisão é texto não nulo
    e o instante tem fuso. A chave estrangeira para ``curriculos`` remove as
    decisões junto com a versão. Ela existe para persistir o que o estudante
    aceitou ou rejeitou.
    """
    op.create_table(
        "decisoes_recomendacao",
        sa.Column("curriculo_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("codigo", sa.Text(), nullable=False),
        sa.Column("decisao", sa.Text(), nullable=False),
        sa.Column("decidida_em", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["curriculo_id"],
            ["curriculos.id"],
            name="fk_decisoes_recomendacao_curriculo_id_curriculos",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("curriculo_id", "codigo"),
    )


def downgrade() -> None:
    """Remove a tabela de decisões sobre recomendações.

    A reversão descarta as decisões gravadas. Ela existe para permitir rollback
    explícito da alteração de schema.
    """
    op.drop_table("decisoes_recomendacao")
