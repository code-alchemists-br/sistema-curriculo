"""Mapeia documentos complementares entre o domínio e as colunas SQLAlchemy externas.

O módulo conserva detalhes de tabela e chave técnica fora do domínio. Ele existe
para persistir os metadados de documentos complementares sem permitir que modelos
ORM atravessem as fronteiras internas da aplicação.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.itens_perfil import Documento
from backend.domain.value_objects import DocumentoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class DocumentoRegistro(Base):
    """Representa um documento complementar nas colunas relacionais da aplicação.

    O mapeamento armazena chave primária UUID, referência de proprietário (usuario_id),
    nome do arquivo, tipo MIME, URL de armazenamento gerada e carimbos de data/hora,
    incluindo deleted_at para suporte a exclusão lógica conforme o DER. Ele existe para
    materializar no banco a tabela DOCUMENTO.
    """

    __tablename__ = "documentos"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("usuarios.id", name="fk_documentos_usuario_id_usuarios"),
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


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
def para_registro(documento: Documento) -> DocumentoRegistro:
    """Converte um documento complementar de domínio para seu registro persistível no SQLAlchemy.

    A função extrai identificadores tipados e campos primitivos para o modelo ORM.
    Ela existe para evitar que o banco receba entidades de domínio diretamente.
    """
    return DocumentoRegistro(
        id=documento.id.valor,
        usuario_id=documento.usuario_id.valor,
        nome_arquivo=documento.nome_arquivo,
        tipo_arquivo=documento.tipo_arquivo,
        url_armazenamento=documento.url_armazenamento,
        deleted_at=documento.deleted_at,
    )


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
def para_documento(registro: DocumentoRegistro) -> Documento:
    """Reconstrói um documento complementar de domínio a partir de um registro ORM persistido.

    A função recria os value objects tipados, reexecutando as invariantes da
    entidade ao cruzar a fronteira para dentro. Ela existe para isolar o domínio
    de instâncias instrumentadas do SQLAlchemy.
    """
    return Documento(
        id=DocumentoId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        nome_arquivo=registro.nome_arquivo,
        tipo_arquivo=registro.tipo_arquivo,
        url_armazenamento=registro.url_armazenamento,
        deleted_at=registro.deleted_at,
    )
