"""Cria a tabela de seleção de itens por versão de currículo conforme o recorte Code First aprovado."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
revision = "20261007_0003"
down_revision = "20261005_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cria curriculo_itens com chave primária composta e chave para curriculos.

    A definição congelada nesta revisão reproduz o modelo atual para garantir
    instalações repetíveis mesmo quando a metadata da aplicação evoluir. A chave
    estrangeira aponta para curriculos, criada pela revisão anterior, e não há
    chave para os itens, cujas tabelas ainda não existem.
    """
    op.create_table(
        "curriculo_itens",
        sa.Column("curriculo_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("tipo", sa.Text(), nullable=False),
        sa.Column("item_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("curriculo_id", "tipo", "item_id"),
        sa.ForeignKeyConstraint(
            ["curriculo_id"],
            ["curriculos.id"],
            name="fk_curriculo_itens_curriculo_id_curriculos",
        ),
    )


def downgrade() -> None:
    """Remove curriculo_itens via Alembic para reverter esta revisão.

    A operação descarta a tabela e as seleções nela gravadas, preservando
    curriculos; existe para permitir rollback explícito desta revisão apenas
    quando essa perda tiver sido autorizada.
    """
    op.drop_table("curriculo_itens")
