"""Emite credenciais aleatórias para sessões autenticadas."""

import base64
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from backend.application.sessoes import (
    CriadorSessao,
    RepositorioSessao,
    RevogadorSessao,
)
from backend.domain.value_objects import UsuarioId


class CriadorSessaoSeguro(CriadorSessao):
    """Gera token opaco de 256 bits e persiste somente seu resumo SHA-256.

    O adapter usa bytes criptograficamente aleatórios, codifica-os em Base64
    URL-safe sem padding e grava a validade de oito horas. Ele existe para
    emitir credenciais sem manter um token reutilizável no banco.
    """

    _DURACAO = timedelta(hours=8)

    def __init__(self, repositorio: RepositorioSessao) -> None:
        """Recebe a porta que armazenará os metadados não secretos da sessão.

        A persistência é injetada para permitir doubles e manter o emissor
        independente de ORM. Ela existe para associar cada token a uma conta.
        """
        self._repositorio = repositorio

    async def criar(self, usuario_id: UsuarioId) -> str:
        """Gera token, persiste hash e datas UTC e devolve o segredo uma vez.

        O token é construído com 32 bytes aleatórios; somente seu SHA-256 é
        salvo. O método existe para concluir login com sessão opaca limitada.
        """
        token = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("ascii")
        criada_em = datetime.now(timezone.utc)
        await self._repositorio.salvar(
            usuario_id=usuario_id,
            token_hash=hashlib.sha256(token.encode("ascii")).hexdigest(),
            criada_em=criada_em,
            expira_em=criada_em + self._DURACAO,
        )
        return token


class RevogadorSessaoSeguro(RevogadorSessao):
    """Revoga uma sessão procurando o hash do token recebido.

    O adapter calcula SHA-256 e delega a atualização condicional do registro;
    o segredo em claro nunca chega ao repositório. Ele existe para invalidar
    somente a sessão apresentada no logout.
    """

    def __init__(self, repositorio: RepositorioSessao) -> None:
        """Recebe a porta usada para marcar sessões como revogadas.

        A dependência permite substituir armazenamento em testes e mantém o
        adapter independente de ORM. Ela existe para separar hashing de SQL.
        """
        self._repositorio = repositorio

    async def revogar(self, token: str) -> None:
        """Resume o token e grava o instante UTC da revogação.

        O método calcula SHA-256 do valor apresentado e delega a atualização
        condicional ao repositório. Ele existe para encerrar a sessão sem
        persistir nem registrar novamente o segredo.
        """
        await self._repositorio.revogar_por_hash(
            hashlib.sha256(token.encode("utf-8")).hexdigest(), datetime.now(timezone.utc)
        )
