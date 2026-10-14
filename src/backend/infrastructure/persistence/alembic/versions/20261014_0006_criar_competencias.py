"""Cria armazenamento Code First para competências de estudantes."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
revision = "20261014_0006"
down_revision = "20261012_0005"
branch_labels = None
depends_on = None


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def upgrade() -> None:
    """Cria a tabela de competências e sua unicidade lógica.

    A migration materializa as colunas do modelo ORM, a referência ao usuário
    e o índice único da chave canônica. Ela existe para fazer o banco reforçar
    a duplicidade tratada pela Application inclusive em requisições concorrentes.
    """
    op.create_table(
        "competencias",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("categoria", sa.String(length=32), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("descricao_normalizada", sa.Text(), nullable=False),
        sa.Column("nivel", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["usuario_id"], ["usuarios.id"], name="fk_competencias_usuario_id_usuarios"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "usuario_id",
            "categoria",
            "descricao_normalizada",
            name="uq_competencias_usuario_categoria_descricao_normalizada",
        ),
    )


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def downgrade() -> None:
    """Remove a tabela de competências em um rollback explícito.

    A reversão descarta somente os registros introduzidos por esta evolução e
    preserva as tabelas anteriores. Ela existe para permitir retorno controlado
    quando a remoção desses dados tiver sido aprovada.
    """
    op.drop_table("competencias")
