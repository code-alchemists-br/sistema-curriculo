"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
"""

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    """Aplica a revisão usando operações Alembic para evoluir o schema.

    As operações abaixo devem ser revisadas para documentar a mudança específica
    e garantir que a evolução Code First corresponda à decisão aprovada.
    """
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Reverte a revisão com operações Alembic para recuperar o schema anterior.

    Revise as operações abaixo e documente possíveis perdas de dados antes de
    autorizar a reversão em um ambiente persistente.
    """
    ${downgrades if downgrades else "pass"}
