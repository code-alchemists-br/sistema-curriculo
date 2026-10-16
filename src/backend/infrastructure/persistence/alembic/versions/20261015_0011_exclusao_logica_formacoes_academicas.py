"""Adiciona exclusão lógica às formações acadêmicas.

Revision ID: 20261015_0011
Revises: 20261015_0010
Create Date: 2026-10-15

Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261015_0011"
down_revision: Union[str, Sequence[str], None] = "20261015_0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Adiciona timestamp anulável sem alterar constraints ou seleções.

    A coluna permite marcar exclusão lógica com o instante original e mantém
    compatibilidade com os dialetos PostgreSQL e SQLite suportados.
    """
    op.add_column(
        "formacoes_academicas",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Remove a marca de exclusão lógica.

    A reversão remove a coluna e descarta os instantes de exclusão registrados.
    Ela existe para permitir rollback explícito da alteração de schema.
    """
    op.drop_column("formacoes_academicas", "deleted_at")
