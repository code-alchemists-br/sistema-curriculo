"""Implementa inserção de sessões com SQLAlchemy."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.sessoes import RepositorioSessao
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.sessao import SessaoRegistro


class RepositorioSessaoSqlAlchemy(RepositorioSessao):
    """Insere metadados de sessão em uma AsyncSession externa.

    O adapter converte a identidade tipada e aguarda o flush sem executar
    commit. Ele existe para manter persistência e ORM fora do caso de uso.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Retém a sessão ORM cujo ciclo transacional pertence à composição.

        O construtor não abre conexão e permite substituir a sessão em testes.
        Ele existe para manter transações sob responsabilidade externa.
        """
        self._session = session

    async def salvar(
        self,
        usuario_id: UsuarioId,
        token_hash: str,
        criada_em: datetime,
        expira_em: datetime,
    ) -> None:
        """Adiciona a sessão com UUID novo e hash do token.

        O método cria uma linha sem token em claro e aguarda o flush, deixando
        commit e rollback para o chamador. Ele existe para tornar a sessão
        disponível à persistência antes de o login enviar o cookie.
        """
        self._session.add(
            SessaoRegistro(
                id=uuid4(),
                usuario_id=usuario_id.valor,
                token_hash=token_hash,
                criada_em=criada_em,
                expira_em=expira_em,
                revogada_em=None,
            )
        )
        await self._session.flush()

    async def revogar_por_hash(self, token_hash: str, revogada_em: datetime) -> None:
        """Registra revogação somente para sessão ainda ativa do hash informado.

        A atualização condicional evita reescrever a data da primeira
        revogação e não altera sessões de outros tokens. Ela existe para
        garantir logout idempotente no armazenamento.
        """
        comando = (
            update(SessaoRegistro)
            .where(SessaoRegistro.token_hash == token_hash, SessaoRegistro.revogada_em.is_(None))
            .values(revogada_em=revogada_em)
        )
        await self._session.execute(comando)
        await self._session.flush()
