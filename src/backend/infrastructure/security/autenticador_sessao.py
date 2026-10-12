"""Valida tokens de sessão contra os metadados persistidos."""

import hashlib
from datetime import datetime, timezone

from backend.application.autenticacao_sessao import (
    AutenticadorSessao,
    ConsultaSessaoAtiva,
)
from backend.domain.value_objects import UsuarioId


class AutenticadorSessaoPersistida(AutenticadorSessao):
    """Adapta um token opaco à consulta de sessão ativa.

    O adapter calcula SHA-256 e consulta somente metadados não secretos no
    repositório. Ele existe para rejeitar sessões desconhecidas, expiradas ou
    revogadas em cada requisição autenticada.
    """

    def __init__(self, consulta: ConsultaSessaoAtiva) -> None:
        """Recebe a porta que consulta sessões ativas.

        A dependência abstrai a persistência e permite substitutos determinísticos.
        Ela existe para manter hashing e acesso ao armazenamento desacoplados.
        """
        self._consulta = consulta

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Resume o token e devolve a identidade se a sessão continuar ativa.

        O método usa SHA-256 e um instante UTC atual; o segredo em claro nunca
        chega ao repositório. Ele existe para validar cookies de sessão.
        """
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        return await self._consulta.obter_usuario_ativo(token_hash, datetime.now(timezone.utc))
