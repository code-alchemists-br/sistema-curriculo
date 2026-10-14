"""Implementa a porta de experiência profissional com SQLAlchemy assíncrono.

O adapter converte a entidade para seu modelo externo, adiciona à sessão e
aguarda o envio da instrução sem controlar commit. Ele existe para persistir o
cadastro usando o ciclo transacional da composição externa.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports import RepositorioExperienciaProfissional
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.infrastructure.persistence.sqlalchemy.experiencia_profissional import (
    para_registro,
)


class RepositorioExperienciaProfissionalSqlAlchemy(RepositorioExperienciaProfissional):
    """Persiste experiências profissionais na sessão assíncrona recebida.

    O adapter traduz a entidade para o modelo ORM, adiciona e executa ``flush``;
    commit e rollback continuam sob responsabilidade da composição. Ele existe
    para implementar a porta interna sem introduzir SQLAlchemy no caso de uso.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Armazena a sessão recebida para delegar as operações de persistência.

        A sessão é injetada e não é criada pelo adapter, permitindo que a
        composição controle seu ciclo de vida e a transação da requisição.
        """
        self._session = session

    async def salvar(self, experiencia: ExperienciaProfissional) -> None:
        """Adiciona a experiência e aguarda o envio das alterações ao banco.

        O método mapeia a entidade, adiciona o registro e chama ``flush`` sem
        finalizar a transação. Ele existe para atender a porta de persistência
        do caso de uso mantendo atomicidade no chamador.
        """
        self._session.add(para_registro(experiencia))
        await self._session.flush()
