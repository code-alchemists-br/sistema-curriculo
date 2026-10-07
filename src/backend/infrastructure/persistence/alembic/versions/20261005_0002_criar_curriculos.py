"""Cria a tabela de versões de currículo conforme o recorte Code First aprovado."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
revision = "20261005_0002"
down_revision = "20260916_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cria curriculos com UUID, proprietário obrigatório e dados da versão.

    A definição congelada nesta revisão reproduz o modelo atual para garantir
    instalações repetíveis mesmo quando a metadata da aplicação evoluir. A chave
    estrangeira aponta para usuarios, criada pela revisão anterior.
    """
    op.create_table(
        "curriculos",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("titulo_versao", sa.Text(), nullable=False),
        sa.Column("layout", sa.Text(), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"], name="fk_curriculos_usuario_id_usuarios"),
    )


def downgrade() -> None:
    """Remove curriculos via Alembic para reverter esta revisão.

    A operação descarta a tabela e seus dados, preservando usuarios; existe para
    permitir rollback explícito desta revisão apenas quando essa perda tiver
    sido autorizada.
    """
    op.drop_table("curriculos")