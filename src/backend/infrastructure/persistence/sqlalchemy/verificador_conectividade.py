"""Implementa a verificação de conectividade com a persistência via SQLAlchemy."""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.health import VerificadorConectividadePersistencia

# Proveniência: decision-analysis prompts/backend/20261014-175641-health-readiness-checks-v001.md#v001


class VerificadorConectividadePersistenciaSqlAlchemy(
    VerificadorConectividadePersistencia
):
    """Executa sondagem assíncrona leve no banco relacional via AsyncSession.

    A classe submete uma instrução simples ('SELECT 1') ao banco de dados por meio da
    sessão assíncrona do SQLAlchemy e captura qualquer falha de conexão, retornando
    um status booleano seguro. Ela existe para fornecer a implementação concreta do
    contrato de readiness sem expor detalhes de banco à camada de API.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Armazena a sessão SQLAlchemy para execução de consultas de teste.

        O construtor recebe uma AsyncSession previamente configurada sem abrir transações
        explícitas ou executar I/O no momento da inicialização. Ele existe para permitir
        injeção de dependência e controle do ciclo de vida da conexão pela composição externa.
        """
        self._session = session

    async def checar_conectividade(self) -> bool:
        """Executa a query de teste assíncrona e reporta a integridade da conexão.

        O método despacha uma consulta SQL mínima via 'session.execute(text("SELECT 1"))',
        retornando True se a resposta for obtida ou False diante de qualquer exceção de
        rede, autenticação ou travamento no banco. Ele existe para confirmar de modo rápido
        e seguro que a persistência está operacional antes de liberar tráfego.
        """
        try:
            await self._session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
