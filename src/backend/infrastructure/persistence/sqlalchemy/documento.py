"""Mapeamento objeto-relacional para documentos complementares de estudantes.

O módulo define o modelo DocumentoRegistro compatível com a tabela 'documentos'
do banco de dados relacional e funções puras de conversão bidirecional entre
o registro do ORM e a entidade Documento do domínio. Ele existe para isolar
detalhes do SQLAlchemy da lógica de negócio.
"""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.itens_perfil import Documento
from backend.domain.value_objects import DocumentoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
class DocumentoRegistro(Base):
    """Representa a tabela relacional 'documentos' mapeada via SQLAlchemy.

    A classe declara as colunas correspondentes à modelagem do DER, incluindo
    identificador UUID, chave estrangeira para o usuário e data de exclusão lógica
    (deleted_at). Ela existe para servir de base às consultas e persistência do ORM.
    """

    __tablename__ = "documentos"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )
    nome_arquivo: Mapped[str] = mapped_column(Text, nullable=False)
    tipo_arquivo: Mapped[str] = mapped_column(Text, nullable=False)
    url_armazenamento: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
def para_registro(documento: Documento) -> DocumentoRegistro:
    """Converte a entidade de domínio Documento para o registro ORM DocumentoRegistro.

    A função extrai valores primitivos e UUIDs dos value objects da entidade e instancia
    o modelo SQLAlchemy. Ela existe para desacoplar a camada de persistência da representação do domínio.
    """
    return DocumentoRegistro(
        id=documento.id.valor,
        usuario_id=documento.usuario_id.valor,
        nome_arquivo=documento.nome_arquivo,
        tipo_arquivo=documento.tipo_arquivo,
        url_armazenamento=documento.url_armazenamento,
    )


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
def para_documento(registro: DocumentoRegistro) -> Documento:
    """Reconstrói a entidade Documento a partir do registro ORM persistido.

    A função instancia os value objects DocumentoId e UsuarioId e monta a entidade
    com os campos armazenados no banco. Ela existe para garantir que a aplicação
    receba apenas objetos válidos do domínio ao consultar o repositório.
    """
    return Documento(
        id=DocumentoId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        nome_arquivo=registro.nome_arquivo,
        tipo_arquivo=registro.tipo_arquivo,
        url_armazenamento=registro.url_armazenamento,
    )
