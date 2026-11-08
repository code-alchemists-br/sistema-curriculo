"""Acrescenta o marcador de exclusão de projetos sem alterar seleções ou checks."""

# Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
import sqlalchemy as sa
from alembic import op

revision = "20261108_0018"
down_revision = "20261101_0017_unificar_ramos"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Adiciona deleted_at anulável com fuso sem modificar dados existentes.

    Usa add_column com o mesmo DateTime de formação para permitir exclusão
    lógica mantendo projetos existentes ativos, sem índice ou alteração de CHECK.
    """
    op.add_column(
        "projetos_academicos",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Remove o marcador por operação Alembic para reverter o schema.

    Descarta somente a coluna e seus instantes de exclusão para permitir
    rollback explícito, preservando textos, checks e seleções de currículo.
    """
    op.drop_column("projetos_academicos", "deleted_at")
