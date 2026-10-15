"""Cria armazenamento Code First para cursos complementares de estudantes."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
revision = "20261015_0011"
down_revision = "20261015_0010"
branch_labels = None
depends_on = None


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
def upgrade() -> None:
    """Cria a tabela de cursos e sua unicidade lógica composta.

    A migration materializa as colunas do modelo ORM, a referência ao usuário
    e o índice único da chave canônica composta (usuário, nome e instituição
    normalizados). Ela existe para fazer o banco reforçar a duplicidade tratada
    pela Application inclusive em requisições concorrentes.
    """
    op.create_table(
        "cursos",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("nome", sa.Text(), nullable=False),
        sa.Column("nome_normalizado", sa.Text(), nullable=False),
        sa.Column("instituicao", sa.Text(), nullable=False),
        sa.Column("instituicao_normalizada", sa.Text(), nullable=False),
        sa.Column("carga_horaria", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["usuario_id"], ["usuarios.id"], name="fk_cursos_usuario_id_usuarios"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "usuario_id",
            "nome_normalizado",
            "instituicao_normalizada",
            name="uq_cursos_usuario_nome_instituicao_normalizados",
        ),
    )


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
def downgrade() -> None:
    """Remove a tabela de cursos em um rollback explícito.

    A reversão descarta somente os registros introduzidos por esta evolução e
    preserva as tabelas anteriores. Ela existe para permitir retorno controlado
    quando a remoção desses dados tiver sido aprovada.
    """
    op.drop_table("cursos")
