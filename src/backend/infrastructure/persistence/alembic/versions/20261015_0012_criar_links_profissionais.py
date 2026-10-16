"""Cria armazenamento Code First para links profissionais de estudantes."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
revision = "20261015_0012"
down_revision = "20261015_0011"
branch_labels = None
depends_on = None


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def upgrade() -> None:
    """Cria a tabela de links profissionais e sua unicidade lógica por usuário e URL.

    A migration materializa as colunas do modelo ORM, a referência ao usuário
    e a restrição única da chave canônica (usuário e url_normalizada).
    Ela existe para fazer o banco reforçar a duplicidade tratada pela Application
    inclusive em requisições concorrentes.
    """
    op.create_table(
        "links_profissionais",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("rotulo", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("url_normalizada", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            name="fk_links_profissionais_usuario_id_usuarios",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "usuario_id",
            "url_normalizada",
            name="uq_links_profissionais_usuario_url_normalizada",
        ),
    )


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def downgrade() -> None:
    """Remove a tabela de links profissionais em um rollback explícito.

    A reversão descarta somente os registros introduzidos por esta evolução e
    preserva as tabelas anteriores. Ela existe para permitir retorno controlado
    quando a remoção desses dados tiver sido aprovada.
    """
    op.drop_table("links_profissionais")
