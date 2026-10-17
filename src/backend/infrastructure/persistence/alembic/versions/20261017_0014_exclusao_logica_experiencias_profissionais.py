"""Adiciona exclusão lógica às experiências profissionais.

Revision ID: 20261017_0014
Revises: 20261016_0013
Create Date: 2026-10-17
"""

import sqlalchemy as sa
from alembic import op

revision = "20261017_0014"
down_revision = "20261016_0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Adiciona timestamp anulável de exclusão sem alterar dados existentes.

    A coluna registra o instante original da exclusão lógica e mantém as
    experiências atuais ativas, com valor nulo, nos dialetos suportados. Ela
    existe para permitir remover experiências do perfil sem purga física.
    """
    op.add_column(
        "experiencias_profissionais",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Remove a marca de exclusão lógica das experiências.

    A reversão remove a coluna e descarta os instantes de exclusão registrados.
    Ela existe para permitir rollback explícito da alteração de schema.
    """
    op.drop_column("experiencias_profissionais", "deleted_at")
