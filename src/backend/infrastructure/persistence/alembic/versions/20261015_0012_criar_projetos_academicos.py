"""Cria armazenamento Code First para projetos acadêmicos de estudantes."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
revision = "20261015_0012"
down_revision = "20261015_0011"
branch_labels = None
depends_on = None


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
def upgrade() -> None:
    """Cria a tabela de projetos, sua FK e limites de texto.

    A migration adiciona somente `projetos_academicos`, com três checks de
    comprimento e uma referência ao proprietário. Ela existe para versionar o
    armazenamento inicial sem alterar estruturas anteriores.
    """
    op.create_table(
        "projetos_academicos",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("titulo", sa.String(length=200), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("tecnologias", sa.String(length=300), nullable=False),
        sa.CheckConstraint(
            "length(trim(titulo)) BETWEEN 1 AND 200",
            name="ck_projetos_academicos_titulo_tamanho",
        ),
        sa.CheckConstraint(
            "length(trim(descricao)) BETWEEN 1 AND 2000",
            name="ck_projetos_academicos_descricao_tamanho",
        ),
        sa.CheckConstraint(
            "length(trim(tecnologias)) BETWEEN 1 AND 300",
            name="ck_projetos_academicos_tecnologias_tamanho",
        ),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            name="fk_projetos_academicos_usuario_id_usuarios",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
def downgrade() -> None:
    """Remove a tabela adicionada por esta revisão.

    A operação descarta somente projetos acadêmicos, sem tocar nas demais
    tabelas. Ela existe para permitir rollback explícito desta evolução.
    """
    op.drop_table("projetos_academicos")
