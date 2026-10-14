"""Emite, valida e revoga sessões opacas usando persistência SQLAlchemy.

O adapter gera tokens aleatórios, guarda somente SHA-256 e consulta a tabela em
cada validação. Ele existe para fornecer identidade autenticada revogável sem
dependência de provedor externo.
"""

from datetime import datetime, timedelta, timezone
import hashlib
import secrets
from typing import Callable
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.infrastructure.persistence.sqlalchemy.sessao import SessaoRegistro


class SessoesSqlAlchemy:
    """Implementa o ciclo de sessões próprias sobre sessões ORM injetadas.

    Cada operação abre uma unidade curta de persistência e a validação rejeita
    hash inexistente, expirado ou revogado. O adapter existe para centralizar o
    ciclo de vida da credencial fora do domínio e dos handlers.
    """

    def __init__(self, fabrica: async_sessionmaker[AsyncSession], agora: Callable[[], datetime] | None = None) -> None:
        """Recebe fábrica ORM e relógio substituível para operação/testes.

        O construtor não abre conexão; o relógio padrão é UTC. Ele existe para
        manter transações curtas e permitir testes determinísticos de expiração.
        """
        self._fabrica = fabrica
        self._agora = agora or (lambda: datetime.now(timezone.utc))

    @staticmethod
    def _hash(token: str) -> str:
        """Calcula digest SHA-256 do token recebido sem armazená-lo em claro.

        A saída hexadecimal tem tamanho fixo para a coluna única. O método
        existe para comparar a credencial recebida com a persistida.
        """
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    async def criar(self, usuario_id: UUID) -> tuple[str, datetime]:
        """Cria token opaco e persiste somente seu hash por oito horas.

        O token tem 256 bits aleatórios e o registro recebe timestamps UTC com
        expiração absoluta. O método existe para iniciar sessão após login válido.
        """
        token = secrets.token_urlsafe(32)
        agora = self._agora()
        expira = agora + timedelta(hours=8)
        async with self._fabrica() as sessao:
            sessao.add(SessaoRegistro(id=uuid4(), usuario_id=usuario_id, token_hash=self._hash(token), criada_em=agora, expira_em=expira))
            await sessao.commit()
        return token, expira

    async def usuario_da_sessao(self, token: str | None) -> UUID | None:
        """Resolve proprietário somente para token ativo e não expirado.

        O valor recebido é convertido a digest antes da consulta e estados
        revogados/expirados são negados. O método existe para derivar principal
        confiável exclusivamente do cookie validado pelo servidor.
        """
        if not token:
            return None
        async with self._fabrica() as sessao:
            registro = await sessao.scalar(select(SessaoRegistro).where(SessaoRegistro.token_hash == self._hash(token)))
            if registro is None or registro.revogada_em is not None or registro.expira_em <= self._agora():
                return None
            return registro.usuario_id

    async def revogar(self, token: str | None) -> None:
        """Revoga a sessão identificada pelo token, ignorando token ausente.

        Atualiza somente registro ainda ativo e confirma a transação. O método
        existe para invalidar imediatamente a credencial no logout.
        """
        if not token:
            return
        async with self._fabrica() as sessao:
            registro = await sessao.scalar(select(SessaoRegistro).where(SessaoRegistro.token_hash == self._hash(token)))
            if registro is not None and registro.revogada_em is None:
                registro.revogada_em = self._agora()
                await sessao.commit()
