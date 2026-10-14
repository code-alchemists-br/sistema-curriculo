"""Unifica a evolução dos dados pessoais e dos recursos adicionados em dev."""

revision = "20261014_0007"
down_revision = ("20261013_0004", "20261014_0006")
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Reconcilia dois históricos de schema sem repetir operações.

    Os pais já criam os dados pessoais e os recursos existentes em dev; esta
    revisão não altera tabelas. Ela existe para garantir um único head Alembic.
    """


def downgrade() -> None:
    """Permite recuar o marcador de merge sem remover dados dos pais.

    A revisão não executa DDL, então o downgrade também não altera tabelas.
    Ela existe para manter o grafo de migrations reversível.
    """
