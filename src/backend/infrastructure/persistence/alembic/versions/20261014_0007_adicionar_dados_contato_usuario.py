"""Adiciona contato opcional à conta sem invalidar usuários existentes."""

import sqlalchemy as sa
from alembic import op

revision = "20261014_0007"
down_revision = "20261014_0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cria colunas opcionais para endereço, cidade, telefones e links.

    Todos os campos aceitam nulo para preservar contas já cadastradas que
    ainda não informaram contato. A operação existe para armazenar os campos
    completos do perfil pela metadata Code First atualizada.
    """
    op.add_column("usuarios", sa.Column("endereco", sa.Text(), nullable=True))
    op.add_column("usuarios", sa.Column("cidade", sa.Text(), nullable=True))
    op.add_column("usuarios", sa.Column("telefones", sa.JSON(), nullable=True))
    op.add_column("usuarios", sa.Column("linkedin", sa.Text(), nullable=True))
    op.add_column(
        "usuarios", sa.Column("curriculo_lattes", sa.Text(), nullable=True)
    )


def downgrade() -> None:
    """Remove as colunas adicionadas pela revisão em ordem inversa.

    A operação reverte a ampliação do perfil e descarta os dados de contato
    gravados nessas colunas. Ela existe para permitir rollback explícito da
    revisão conforme o fluxo de migrations do backend.
    """
    op.drop_column("usuarios", "curriculo_lattes")
    op.drop_column("usuarios", "linkedin")
    op.drop_column("usuarios", "telefones")
    op.drop_column("usuarios", "cidade")
    op.drop_column("usuarios", "endereco")
