"""Implementa a porta de documento complementar com SQLAlchemy assíncrono.

O adapter persiste os metadados de documentos complementares utilizando a sessão
assíncrona do SQLAlchemy, convertendo entre a entidade de domínio e o registro ORM.
Ele existe para conectar a camada Application ao banco de dados relacional sem expor o ORM internamente.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports import RepositorioDocumento
from backend.domain.itens_perfil import Documento
from backend.domain.value_objects import DocumentoId
from backend.infrastructure.persistence.sqlalchemy.documento import (
    DocumentoRegistro,
    para_documento,
    para_registro,
)


# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
class RepositorioDocumentoSqlAlchemy(RepositorioDocumento):
    """Consulta e persiste documentos complementares usando uma sessão externa assíncrona.

    A implementação adiciona o modelo ORM à sessão, executa flush para materializar
    o registro e consulta documentos ativos desconsiderando os excluídos logicamente (deleted_at).
    Ela existe para atender o contrato da porta RepositorioDocumento.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Armazena a sessão que executará as operações de persistência.

        O construtor recebe a sessão gerenciada externamente pela composição ou middleware.
        Ele existe para manter o adapter subordinado ao ciclo de vida transacional.
        """
        self._session = session

    async def salvar(self, documento: Documento) -> None:
        """Adiciona o registro de documento à sessão e dispara flush.

        O método converte o documento de domínio para DocumentoRegistro e o registra
        na sessão assíncrona. Ele existe para efetivar a gravação dos metadados no banco.
        """
        registro = para_registro(documento)
        self._session.add(registro)
        await self._session.flush()

    async def obter_por_id(self, documento_id: DocumentoId) -> Documento | None:
        """Localiza um documento pelo seu identificador primário.

        O método pesquisa pelo ID desconsiderando registros com deleted_at preenchido.
        Ele existe para permitir recuperação e verificações de integridade.
        """
        consulta = select(DocumentoRegistro).where(
            DocumentoRegistro.id == documento_id.valor,
            DocumentoRegistro.deleted_at.is_(None),
        )
        resultado = await self._session.execute(consulta)
        registro = resultado.scalar_one_or_none()
        if registro is None:
            return None
        return para_documento(registro)
