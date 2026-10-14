"""Cria a tabela de formações acadêmicas com vocabulários e período controlados."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
revision = "20261014_0007"
down_revision = "20261014_0006"
branch_labels = None
depends_on = None


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
def upgrade() -> None:
    """Cria a tabela e suas constraints relacionais portáveis.

    A migration armazena enums como texto e limita instituição/curso com
    VARCHAR e CHECKs, além de restringir vocabulário e coerência temporal. Ela
    existe para materializar o contrato do modelo em PostgreSQL e SQLite.
    """
    op.create_table(
        "formacoes_academicas",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("instituicao", sa.String(length=200), nullable=False),
        sa.Column("curso", sa.String(length=200), nullable=False),
        sa.Column("nivel", sa.Text(), nullable=False),
        sa.Column("data_inicio", sa.Date(), nullable=False),
        sa.Column("data_fim", sa.Date(), nullable=True),
        sa.Column("status", sa.Text(), nullable=False),
        sa.CheckConstraint(
            "length(trim(instituicao)) BETWEEN 1 AND 200",
            name="ck_formacoes_instituicao_tamanho",
        ),
        sa.CheckConstraint(
            "length(trim(curso)) BETWEEN 1 AND 200",
            name="ck_formacoes_curso_tamanho",
        ),
        sa.CheckConstraint(
            "nivel IN ('ensino_fundamental', 'ensino_medio', 'tecnico', "
            "'tecnologo', 'graduacao', 'especializacao', 'mestrado', 'doutorado')",
            name="ck_formacoes_nivel_valido",
        ),
        sa.CheckConstraint(
            "status IN ('em_andamento', 'concluido', 'interrompido')",
            name="ck_formacoes_status_valido",
        ),
        sa.CheckConstraint(
            "(status = 'em_andamento' AND "
            "(data_fim IS NULL OR data_fim >= data_inicio)) OR "
            "(status = 'concluido' AND data_fim IS NOT NULL AND "
            "data_fim >= data_inicio) OR "
            "(status = 'interrompido' AND "
            "(data_fim IS NULL OR data_fim >= data_inicio))",
            name="ck_formacoes_status_periodo_coerente",
        ),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            name="fk_formacoes_usuario_id_usuarios",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
def downgrade() -> None:
    """Remove a tabela criada por esta evolução de schema.

    A operação descarta formações acadêmicas e mantém tabelas anteriores
    intactas. Ela existe para permitir rollback explícito desta migration.
    """
    op.drop_table("formacoes_academicas")
