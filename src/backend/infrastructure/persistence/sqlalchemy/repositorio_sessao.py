"""Implementa inserção de sessões com SQLAlchemy."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.autenticacao_sessao import ConsultaSessaoAtiva
from backend.application.sessoes import RepositorioSessao
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.sessao import SessaoRegistro
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro


class RepositorioSessaoSqlAlchemy(RepositorioSessao, ConsultaSessaoAtiva):
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

    async def obter_usuario_ativo(self, token_hash: str, instante: datetime) -> UsuarioId | None:
        """Busca a identidade de sessão não revogada, válida e de perfil ativo.

        A consulta filtra pelo resumo, expiração e ausência de revogação e faz
        junção com o usuário para descartar perfis com ``deleted_at``, sem
        materializar os registros inteiros. Ela existe para autenticar
        requisições usando o estado persistido e para que a exclusão lógica do
        perfil invalide imediatamente todas as suas sessões.
        """
        comando = (
            select(SessaoRegistro.usuario_id)
            .join(UsuarioRegistro, UsuarioRegistro.id == SessaoRegistro.usuario_id)
            .where(
                SessaoRegistro.token_hash == token_hash,
                SessaoRegistro.expira_em > instante,
                SessaoRegistro.revogada_em.is_(None),
                UsuarioRegistro.deleted_at.is_(None),
            )
        )
        resultado = await self._session.execute(comando)
        usuario_id = resultado.scalar_one_or_none()
        return UsuarioId(usuario_id) if usuario_id is not None else None

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
