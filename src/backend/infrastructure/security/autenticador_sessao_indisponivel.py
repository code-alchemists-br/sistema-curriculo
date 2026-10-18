"""Define uma autenticação que rejeita sessões quando não há persistência.

O adapter implementa a porta de autenticação sem consultar armazenamento e
sempre considera o token inválido. Ele existe para manter a aplicação ASGI
segura enquanto a composição de produção não fornece um autenticador persistido.
"""

from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.domain.value_objects import UsuarioId


class AutenticadorSessaoIndisponivel(AutenticadorSessao):
    """Rejeita toda credencial quando não há consulta de sessão configurada.

    O método responde sempre com ``None`` sem consultar dependências externas.
    Ele existe como fallback seguro para impedir que a ausência de composição
    desative a proteção das rotas privadas.
    """

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Indica que nenhum token pode ser autenticado neste adapter.

        O valor recebido é deliberadamente ignorado porque não há persistência
        capaz de validar sessões. O método existe para manter o comportamento
        fechado até que a aplicação receba um autenticador funcional.
        """
        del token
        return None
