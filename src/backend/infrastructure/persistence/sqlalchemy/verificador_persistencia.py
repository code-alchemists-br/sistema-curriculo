"""Adapta uma engine SQLAlchemy ao contrato de readiness da aplicação."""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


class VerificadorPersistenciaSqlalchemy:
    """Confirma conectividade com a persistência por uma consulta mínima.

    O adaptador executa `SELECT 1` usando a engine assíncrona injetada e deixa
    falhas de conexão subirem para a rota, que responde sem detalhes internos.
    Ele existe para ligar a porta de readiness da aplicação ao PostgreSQL.
    """

    def __init__(self, engine: AsyncEngine) -> None:
        """Recebe a engine assíncrona usada para verificar a persistência.

        A engine é criada pela composição externa e compartilhada com o ciclo
        de vida da aplicação. O construtor existe para manter o adaptador
        desacoplado de variáveis de ambiente e da criação de conexões.
        """
        self._engine = engine

    async def verificar(self) -> bool:
        """Executa uma consulta mínima e indica se o banco responde.

        O método abre uma conexão, executa `SELECT 1` e fecha a conexão pelo
        contexto assíncrono. Ele existe para impedir tráfego quando a
        persistência configurada não pode atender operações.
        """
        async with self._engine.connect() as conexao:
            resultado = await conexao.scalar(text("SELECT 1"))
        return resultado == 1
