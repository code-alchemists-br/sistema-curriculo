"""Implementa a porta de projetos acadêmicos com SQLAlchemy assíncrono.

O adapter converte a entidade, adiciona o modelo à sessão e aguarda o flush sem
controlar commit. Ele existe para conectar Application à persistência e deixar
o ciclo transacional sob responsabilidade da composição.
"""

# Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
from backend.application.ports import RepositorioProjetoAcademico
from backend.domain import ProjetoAcademico, ProjetoAcademicoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.projeto_academico import (
    ProjetoAcademicoRegistro,
    para_projeto_academico,
    para_registro,
)


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class RepositorioProjetoAcademicoSQLAlchemy(RepositorioProjetoAcademico):
    """Consulta e persiste projetos na sessão assíncrona recebida.

    O adapter implementa ``salvar`` convertendo para ORM, adicionando e fazendo
    flush, lê por ID e dono e usa UPDATE condicional para edição e exclusão,
    sem executar commit ou regras de negócio. Ele existe para satisfazer
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

    # Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
    async def obter_por_id_e_usuario(
        self, projeto_id: ProjetoAcademicoId, usuario_id: UsuarioId
    ) -> ProjetoAcademico | None:
        """Lê projeto próprio ativo filtrando ID, dono e marcador nulo.

        Converte somente registro encontrado para entidade, para confundir
        ausente, alheio e excluído sem expor o ORM à Application.
        """
        registro = await self._session.scalar(select(ProjetoAcademicoRegistro).where(
            ProjetoAcademicoRegistro.id == projeto_id.valor,
            ProjetoAcademicoRegistro.usuario_id == usuario_id.valor,
            ProjetoAcademicoRegistro.deleted_at.is_(None),
        ))
        return para_projeto_academico(registro) if registro is not None else None

    # Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
    async def obter_por_id_e_usuario_incluindo_excluidas(
        self, projeto_id: ProjetoAcademicoId, usuario_id: UsuarioId
    ) -> ProjetoAcademico | None:
        """Lê projeto próprio inclusive excluído por ID e proprietário.

        Omite o filtro temporal e converte o registro encontrado para permitir
        repetição idempotente sem revelar existência de projetos alheios.
        """
        registro = await self._session.scalar(select(ProjetoAcademicoRegistro).where(
            ProjetoAcademicoRegistro.id == projeto_id.valor,
            ProjetoAcademicoRegistro.usuario_id == usuario_id.valor,
        ))
        return para_projeto_academico(registro) if registro is not None else None

    # Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
    async def atualizar(self, projeto: ProjetoAcademico) -> bool:
        """Atualiza os três textos somente no registro próprio ainda ativo.

        Usa UPDATE por ID, dono e marcador nulo, faz flush sem commit e devolve
        rowcount igual a um, para não ressuscitar exclusão concorrente.
        """
        instrucao = update(ProjetoAcademicoRegistro).where(
            ProjetoAcademicoRegistro.id == projeto.id.valor,
            ProjetoAcademicoRegistro.usuario_id == projeto.usuario_id.valor,
            ProjetoAcademicoRegistro.deleted_at.is_(None),
        ).values(
            titulo=projeto.titulo, descricao=projeto.descricao,
            tecnologias=projeto.tecnologias,
        ).execution_options(synchronize_session="fetch")
        resultado = await self._session.execute(instrucao)
        await self._session.flush()
        return resultado.rowcount == 1

    # Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
    async def marcar_excluida(
        self, projeto_id: ProjetoAcademicoId, usuario_id: UsuarioId, deleted_at: datetime
    ) -> bool:
        """Marca o projeto próprio ativo sem tocar nas seleções de currículo.

        Usa UPDATE condicional com flush sem commit e informa se alterou uma
        linha para preservar o primeiro instante e permitir releitura na disputa.
        """
        instrucao = update(ProjetoAcademicoRegistro).where(
            ProjetoAcademicoRegistro.id == projeto_id.valor,
            ProjetoAcademicoRegistro.usuario_id == usuario_id.valor,
            ProjetoAcademicoRegistro.deleted_at.is_(None),
        ).values(deleted_at=deleted_at).execution_options(synchronize_session="fetch")
        resultado = await self._session.execute(instrucao)
        await self._session.flush()
        return resultado.rowcount == 1
