"""Cria armazenamento Code First para idiomas de estudantes."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
revision = "20261015_0009"
down_revision = "20261014_0008"
branch_labels = None
depends_on = None


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
def upgrade() -> None:
    """Cria a tabela de idiomas e sua unicidade lógica.

    A migration materializa as colunas do modelo ORM, a referência ao usuário
    e o índice único da chave canônica. Ela existe para fazer o banco reforçar
    a duplicidade tratada pela Application inclusive em requisições concorrentes.
    """
    op.create_table(
        "idiomas",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("idioma", sa.Text(), nullable=False),
        sa.Column("idioma_normalizado", sa.Text(), nullable=False),
        sa.Column("nivel", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["usuario_id"], ["usuarios.id"], name="fk_idiomas_usuario_id_usuarios"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "usuario_id",
            "idioma_normalizado",
            name="uq_idiomas_usuario_idioma_normalizado",
        ),
    )


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
def downgrade() -> None:
    """Remove a tabela de idiomas em um rollback explícito.

    A reversão descarta somente os registros introduzidos por esta evolução e
    preserva as tabelas anteriores. Ela existe para permitir retorno controlado
    quando a remoção desses dados tiver sido aprovada.
    """
    op.drop_table("idiomas")
