"""Une os ramos de migrations independentes do schema relacional.

Revision ID: 20261101_0017_unificar_ramos
Revises: 20261023_0016, 20261015_0012_projetos, 20261017_0004
Create Date: 2026-11-01

Esta migration não altera tabelas. Ela registra no Alembic que as evoluções de
documentos, projetos acadêmicos e associações currículo-vaga devem coexistir
antes das próximas alterações lineares do schema.
"""

from typing import Sequence, Union


revision: str = "20261101_0017_unificar_ramos"
down_revision: Union[str, Sequence[str], None] = (
    "20261023_0016",
    "20261015_0012_projetos",
    "20261017_0004",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Registra a convergência das linhas independentes de evolução do schema.

    A operação não executa DDL porque as três heads já materializam suas tabelas
    próprias. Ela existe para permitir que upgrades futuros tenham uma única
    predecessora, sem repetir ou omitir nenhuma estrutura já versionada.
    """


def downgrade() -> None:
    """Restaura as três heads quando um rollback atravessa a merge migration.

    A operação também não executa DDL porque somente remove a relação de merge
    no histórico. Ela existe para preservar a reversibilidade do grafo sem
    alterar os schemas criados pelas migrations predecessoras.
    """
