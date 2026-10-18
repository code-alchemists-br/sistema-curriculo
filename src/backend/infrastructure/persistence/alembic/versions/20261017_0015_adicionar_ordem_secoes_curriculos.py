"""Adiciona a ordem explícita das seções às versões de currículo.

Revision ID: 20261017_0015
Revises: 20261017_0014
Create Date: 2026-10-17
"""

import sqlalchemy as sa
from alembic import op

revision = "20261017_0015"
down_revision = "20261017_0014"
branch_labels = None
depends_on = None

# Ordem padrão congelada na migration: versões já existentes passam a ter a
# ordem explícita igual à ordem padrão vigente quando a coluna foi criada.
ORDEM_SECOES_PADRAO = (
    "dados-pessoais,formacao-academica,experiencias-profissionais,"
    "projetos-academicos,competencias,idiomas,documentos-complementares"
)


def upgrade() -> None:
    """Adiciona a coluna de ordem das seções preenchida com a ordem padrão.

    A coluna é de texto não nulo, com valor padrão no servidor, de modo que as
    versões existentes recebem a ordem padrão sem uma etapa de preenchimento. Ela
    existe para persistir a ordem explícita de apresentação das seções.
    """
    op.add_column(
        "curriculos",
        sa.Column(
            "ordem_secoes",
            sa.Text(),
            nullable=False,
            server_default=ORDEM_SECOES_PADRAO,
        ),
    )


def downgrade() -> None:
    """Remove a coluna de ordem das seções das versões de currículo.

    A reversão remove a coluna e descarta as ordens personalizadas gravadas. Ela
    existe para permitir rollback explícito da alteração de schema.
    """
    op.drop_column("curriculos", "ordem_secoes")
