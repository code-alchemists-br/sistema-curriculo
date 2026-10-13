"""Define as portas para autenticar sessões persistidas."""

from datetime import datetime
from typing import Protocol

from backend.domain.value_objects import UsuarioId


class ConsultaSessaoAtiva(Protocol):
    """Define a consulta da identidade associada a uma sessão válida.

    A implementação procura por resumo de token e instante de referência,
    considerando validade e revogação. Ela existe para consultar persistência
    sem expor ORM à camada de segurança.
    """

    async def obter_usuario_ativo(self, token_hash: str, instante: datetime) -> UsuarioId | None:
        """Retorna a identidade somente se a sessão estiver ativa no instante.

        A consulta exclui sessões expiradas ou revogadas e devolve `None` para
        tokens desconhecidos. Ela existe para fornecer uma decisão de sessão.
        """


class AutenticadorSessao(Protocol):
    """Define a validação de um token de sessão apresentado à API.

    A implementação resume a credencial e consulta uma porta de sessões ativas.
    Ela existe para separar a autenticação do transporte HTTP e do ORM.
    """

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Retorna o estudante autenticado ou `None` para credencial inválida.

        A consulta considera sessão persistida, expiração e revogação. Ela
        existe para dar à API uma identidade confiável para cada requisição.
        """
