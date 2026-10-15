"""Implementa a porta de formação acadêmica com SQLAlchemy assíncrono.

O adapter converte a entidade em registro, adiciona-o à sessão injetada e
aguarda o flush sem controlar commit. Ele existe para conectar Application à
persistência relacional mantendo a transação sob controle da composição.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports import RepositorioFormacaoAcademica
from backend.domain.itens_perfil import FormacaoAcademica
from backend.infrastructure.persistence.sqlalchemy.formacao_academica import (
    para_registro,
)


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
class RepositorioFormacaoAcademicaSqlAlchemy(RepositorioFormacaoAcademica):
    """Persiste formações na sessão assíncrona recebida.

    O adapter converte entidades para ORM e delega o envio à sessão sem fazer
    commit ou rollback. Ele existe para implementar a porta de cadastro sem
    introduzir detalhes SQLAlchemy no caso de uso.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Guarda a sessão que executará a persistência.

        A sessão é criada e administrada pela composição externa, não pelo
        repositório. O construtor existe para respeitar o ciclo de vida
        transacional definido fora deste adapter.
        """
        self._session = session

    async def salvar(self, formacao: FormacaoAcademica) -> None:
        """Adiciona a formação convertida e aguarda o envio das alterações.

        O método mapeia a entidade, adiciona o registro e chama ``flush`` sem
        finalizar a transação. Ele existe para atender a porta de persistência
        mantendo atomicidade no chamador.
        """
        self._session.add(para_registro(formacao))
        await self._session.flush()
