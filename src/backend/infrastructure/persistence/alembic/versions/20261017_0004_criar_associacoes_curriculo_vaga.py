"""Cria associação currículo-vaga e classificações com identidade composta."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
revision = "20261017_0004"
down_revision = "20261007_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cria as tabelas relacionais com chaves compostas e referência ao currículo.

    A migration cria primeiro a associação, identificada pelo par currículo-vaga,
    e depois suas classificações, cuja PK inclui o mesmo par e o valor textual.
    Ela existe para impor unicidade e persistir todas as classificações sem ID
    técnico de associação.
    """
    op.create_table(
        "associacoes_curriculo_vaga",
        sa.Column("curriculo_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("vaga_id", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "curriculo_id",
            "vaga_id",
            name="pk_associacoes_curriculo_vaga",
        ),
        sa.ForeignKeyConstraint(
            ["curriculo_id"],
            ["curriculos.id"],
            name="fk_associacoes_curriculo_vaga_curriculo_id_curriculos",
        ),
    )
    op.create_table(
        "classificacoes_associacao_curriculo_vaga",
        sa.Column("curriculo_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("vaga_id", sa.Text(), nullable=False),
        sa.Column("classificacao", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "curriculo_id",
            "vaga_id",
            "classificacao",
            name="pk_classificacoes_associacao_curriculo_vaga",
        ),
        sa.ForeignKeyConstraint(
            ["curriculo_id", "vaga_id"],
            [
                "associacoes_curriculo_vaga.curriculo_id",
                "associacoes_curriculo_vaga.vaga_id",
            ],
            name="fk_classificacoes_associacao_assoc_curriculo_vaga",
            ondelete="CASCADE",
        ),
    )


def downgrade() -> None:
    """Remove classificações e associação na ordem segura das chaves estrangeiras.

    A operação descarta as duas tabelas criadas por esta revisão e preserva
    currículos. Ela existe para permitir rollback explícito da migration.
    """
    op.drop_table("classificacoes_associacao_curriculo_vaga")
    op.drop_table("associacoes_curriculo_vaga")
