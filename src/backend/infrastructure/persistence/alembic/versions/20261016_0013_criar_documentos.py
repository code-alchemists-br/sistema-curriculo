"""Cria armazenamento Code First para documentos complementares de estudantes."""

import sqlalchemy as sa
from alembic import op

# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
revision = "20261016_0013"
down_revision = "20261015_0012"
branch_labels = None
depends_on = None


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
def upgrade() -> None:
    """Cria a tabela de documentos complementares e suas chaves estrangeiras.

    A migration materializa as colunas do modelo ORM DocumentoRegistro, a referência
    ao usuário proprietário (FK) e os carimbos de auditoria/exclusão lógica (deleted_at).
    Ela existe para persistir documentos complementares de forma consistente com o DER.
    """
    op.create_table(
        "documentos",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("usuario_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("nome_arquivo", sa.Text(), nullable=False),
        sa.Column("tipo_arquivo", sa.Text(), nullable=False),
        sa.Column("url_armazenamento", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
            name="fk_documentos_usuario_id_usuarios",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_documentos_usuario_id",
        "documentos",
        ["usuario_id"],
        unique=False,
    )


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
def downgrade() -> None:
    """Remove a tabela de documentos complementares em rollback explícito.

    A operação remove a tabela e índices criados por esta evolução, sem afetar
    outras entidades. Ela existe para permitir reversão controlada da estrutura de dados.
    """
    op.drop_index("ix_documentos_usuario_id", table_name="documentos")
    op.drop_table("documentos")
