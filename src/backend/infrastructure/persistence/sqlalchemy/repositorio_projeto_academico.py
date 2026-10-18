"""Implementa a porta de projetos acadêmicos com SQLAlchemy assíncrono.

O adapter converte a entidade, adiciona o modelo à sessão e aguarda o flush sem
controlar commit. Ele existe para conectar Application à persistência e deixar
o ciclo transacional sob responsabilidade da composição.
"""

from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
from backend.application.ports import RepositorioProjetoAcademico
from backend.domain import ProjetoAcademico
from backend.infrastructure.persistence.sqlalchemy.projeto_academico import (
    para_registro,
)


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class RepositorioProjetoAcademicoSQLAlchemy(RepositorioProjetoAcademico):
    """Persiste projetos acadêmicos na sessão assíncrona recebida.

    O adapter implementa ``salvar`` convertendo para ORM, adicionando e fazendo
    flush, sem executar commit ou regras de negócio. Ele existe para satisfazer
    a porta da Application sobre armazenamento relacional.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Guarda a sessão que executará a gravação.

        A sessão é criada e administrada externamente; o construtor conserva a
        dependência recebida para respeitar o ciclo transacional da aplicação.
        """
        self._session = session

    async def salvar(self, projeto: ProjetoAcademico) -> None:
        """Adiciona o projeto convertido e aguarda o flush da sessão.

        O método mapeia a entidade, chama ``add`` e aguarda ``flush`` sem
        finalizar a transação. Ele existe para implementar a porta de gravação
        mantendo atomicidade no chamador.
        """
        self._session.add(para_registro(projeto))
        await self._session.flush()
