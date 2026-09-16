"""Cria a primeira tabela de contas conforme o recorte Code First aprovado."""

from alembic import op
import sqlalchemy as sa

# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001
revision = "20260916_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cria usuarios com UUID e e-mail único usando operações Alembic.

    A definição congelada nesta revisão reproduz o modelo inicial para garantir
    instalações repetíveis mesmo quando a metadata da aplicação evoluir.
    """
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("nome", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("hash_senha", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_usuarios_email"),
    )


def downgrade() -> None:
    """Remove usuarios via Alembic para reverter a instalação inicial.

    A operação descarta a tabela e seus dados; existe para permitir rollback
    explícito desta revisão apenas quando essa perda tiver sido autorizada.
    """
    op.drop_table("usuarios")
