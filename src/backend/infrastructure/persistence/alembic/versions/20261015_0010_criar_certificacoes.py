"""Cria armazenamento Code First para certificações de estudantes."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
revision = "20261015_0010"
down_revision = ("20261014_0009", "20261015_0009")
branch_labels = None
depends_on = None


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
def upgrade() -> None:
    """Cria a tabela de certificações e sua unicidade composta lógica.

    A migration materializa as colunas do modelo ORM, a referência ao usuário
    e o índice único da chave canônica (usuário, nome e emissor normalizados).
    Ela existe para fazer o banco reforçar a duplicidade tratada pela Application
    inclusive em requisições concorrentes.
    """
    op.create_table(
        "certificacoes",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("nome", sa.Text(), nullable=False),
        sa.Column("nome_normalizado", sa.Text(), nullable=False),
        sa.Column("organizacao_emissora", sa.Text(), nullable=False),
        sa.Column("organizacao_emissora_normalizada", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            name="fk_certificacoes_usuario_id_usuarios",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "usuario_id",
            "nome_normalizado",
            "organizacao_emissora_normalizada",
            name="uq_certificacoes_usuario_nome_emissor_normalizados",
        ),
    )


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
def downgrade() -> None:
    """Remove a tabela de certificações em um rollback explícito.

    A reversão descarta somente os registros introduzidos por esta evolução e
    preserva as tabelas anteriores. Ela existe para permitir retorno controlado
    quando a remoção desses dados tiver sido aprovada.
    """
    op.drop_table("certificacoes")
