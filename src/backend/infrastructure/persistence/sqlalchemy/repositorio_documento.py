"""Implementação do repositório de documentos complementares com SQLAlchemy assíncrono.

O módulo conecta as operações da porta RepositorioDocumento ao mecanismo relacional,
executando consultas com filtro de exclusão lógica (deleted_at IS NULL) e persistindo
atualizações na sessão assíncrona. Ele existe para satisfazer o contrato de
persistência sem vazar dependências de infraestrutura para o núcleo da aplicação.
"""

from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports import RepositorioDocumento
from backend.domain.itens_perfil import Documento
from backend.domain.value_objects import DocumentoId
from backend.infrastructure.persistence.sqlalchemy.documento import (
    DocumentoRegistro,
    para_documento,
    para_registro,
)


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
class RepositorioDocumentoSqlAlchemy(RepositorioDocumento):
    """Adaptador de persistência para documentos complementares usando SQLAlchemy.

    A classe executa queries e mutações na tabela 'documentos' utilizando a sessão
    injetada, aplicando soft-delete através da coluna deleted_at. Ela existe para
    cumprir a porta RepositorioDocumento mantendo a transação sob controle externo.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Inicializa o repositório com uma sessão SQLAlchemy assíncrona.

        O construtor armazena a sessão ativa recebida da composição da aplicação.
        Ele existe para delegar o ciclo de vida da transação ao chamador.
        """
        self._session = session

    async def obter_por_id(self, documento_id: DocumentoId) -> Documento | None:
        """Busca um documento ativo pelo seu identificador primário.

        O método seleciona o registro correspondente onde deleted_at seja nulo
        e o reconverte para a entidade de domínio Documento. Ele existe para prover
        leitura confiável antes de operações de modificação ou exclusão.
        """
        consulta = select(DocumentoRegistro).where(
            DocumentoRegistro.id == documento_id.valor,
            DocumentoRegistro.deleted_at.is_(None),
        )
        registro = await self._session.scalar(consulta)
        if registro is None:
            return None
        return para_documento(registro)

    async def excluir(self, documento: Documento) -> None:
        """Executa a exclusão lógica do documento na sessão assíncrona.

        O método emite um UPDATE preenchendo deleted_at com a data e hora UTC
        atual e realiza flush na sessão. Ele existe para efetivar a remoção lógica
        do documento em conformidade com o DER.
        """
        instrucao = (
            update(DocumentoRegistro)
            .where(
                DocumentoRegistro.id == documento.id.valor,
                DocumentoRegistro.deleted_at.is_(None),
            )
            .values(deleted_at=datetime.now(timezone.utc))
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(instrucao)
        await self._session.flush()

    async def salvar(self, documento: Documento) -> None:
        """Adiciona um novo documento à sessão e aguarda o envio das alterações.

        O método converte a entidade para registro ORM, adiciona na sessão
        e realiza o flush. Ele existe para viabilizar persistência de documentos.
        """
        registro = para_registro(documento)
        self._session.add(registro)
        await self._session.flush()
