"""Adiciona os dados de perfil necessários à consulta pessoal do estudante."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
revision = "20261013_0004"
down_revision = "20261007_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Acrescenta contato e exclusão lógica sem invalidar contas existentes.

    Todas as novas colunas são anuláveis para preservar registros anteriores
    sem contato/cidade; telefones são armazenados como JSON. A revisão existe
    para tornar os campos explícitos e recuperáveis pelo ORM Code First.
    """
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    op.add_column(
        "usuarios",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column("usuarios", sa.Column("endereco", sa.Text(), nullable=True))
    op.add_column("usuarios", sa.Column("telefones", sa.JSON(), nullable=True))
    op.add_column("usuarios", sa.Column("cidade", sa.Text(), nullable=True))
    op.add_column("usuarios", sa.Column("linkedin", sa.Text(), nullable=True))
    op.add_column("usuarios", sa.Column("curriculo_lattes", sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove as colunas introduzidas nesta revisão Alembic.

    As operações descartam os respectivos valores de perfil, e existem para
    permitir reversão explícita da alteração de schema versionada.
    """
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    op.drop_column("usuarios", "curriculo_lattes")
    op.drop_column("usuarios", "linkedin")
    op.drop_column("usuarios", "cidade")
    op.drop_column("usuarios", "telefones")
    op.drop_column("usuarios", "endereco")
    op.drop_column("usuarios", "deleted_at")
