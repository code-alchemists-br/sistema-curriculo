"""Define as portas para emissão e persistência de sessões de acesso."""

from datetime import datetime
from typing import Protocol

from backend.domain.value_objects import UsuarioId


class RepositorioSessao(Protocol):
    """Define a persistência de metadados de uma sessão sem segredo em claro.

    A porta recebe identidade, hash do token e instantes de validade. Ela existe
    para que o emissor de sessão possa persistir sessões sem depender de ORM.
    """

    async def salvar(
        self,
        usuario_id: UsuarioId,
        token_hash: str,
        criada_em: datetime,
        expira_em: datetime,
    ) -> None:
        """Persiste os metadados não secretos de uma sessão recém-criada.

        A implementação grava somente o resumo do token e sua validade. O
        método existe para permitir localizar e revogar a sessão futuramente.
        """


class CriadorSessao(Protocol):
    """Define a criação de uma credencial opaca para uma identidade autenticada.

    A implementação gera o segredo e persiste somente seu hash. Ela existe para
    separar a emissão de credenciais do transporte HTTP e do caso de uso.
    """

    async def criar(self, usuario_id: UsuarioId) -> str:
        """Cria uma sessão e devolve seu token em claro uma única vez.

        O método associa a sessão à identidade informada e retorna o segredo
        para que a API o transporte em cookie. Ele existe para concluir o login.
        """
