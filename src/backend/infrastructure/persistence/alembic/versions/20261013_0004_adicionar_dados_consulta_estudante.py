"""Adiciona os dados de perfil necessários à consulta pessoal do estudante."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
revision = "20261013_0004"
down_revision = "20261014_0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Acrescenta contato e exclusão lógica sem invalidar contas existentes.

    A revisão acrescenta a data de exclusão lógica, enquanto as colunas de
    contato são criadas pela revisão 20261014_0007. Ela existe para completar
    a consulta sem duplicar alterações de schema já integradas.
    """
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    op.add_column(
        "usuarios",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Remove as colunas introduzidas nesta revisão Alembic.

    As operações descartam os respectivos valores de perfil, e existem para
    permitir reversão explícita da alteração de schema versionada.
    """
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    op.drop_column("usuarios", "deleted_at")
