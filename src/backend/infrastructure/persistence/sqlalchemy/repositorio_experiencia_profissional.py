"""Implementa a porta de experiência profissional com SQLAlchemy assíncrono.

O adapter converte a entidade para seu modelo externo e de volta, consulta,
atualiza e marca exclusão lógica por identidade e proprietário e aguarda o envio
das instruções sem controlar commit. Ele existe para persistir cadastro, edição
e exclusão usando o ciclo transacional da composição externa.
"""

from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports import RepositorioExperienciaProfissional
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import ExperienciaProfissionalId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.experiencia_profissional import (
    ExperienciaProfissionalRegistro,
    para_experiencia,
    para_registro,
)


class RepositorioExperienciaProfissionalSqlAlchemy(RepositorioExperienciaProfissional):
    """Persiste e consulta experiências profissionais na sessão assíncrona recebida.

    O adapter traduz entidade e modelo ORM, executa consultas e atualizações
    filtradas por ID e proprietário, desconsidera experiências excluídas nas
    operações ativas e chama ``flush``; commit e rollback continuam sob
    responsabilidade da composição. Ele existe para implementar a porta interna
    sem introduzir SQLAlchemy no caso de uso.
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

    async def obter_por_id_e_usuario(
        self, experiencia_id: ExperienciaProfissionalId, usuario_id: UsuarioId
    ) -> ExperienciaProfissional | None:
        """Obtém a experiência ativa somente se ID e proprietário coincidirem.

        A consulta filtra os dois identificadores e a ausência de exclusão na
        mesma instrução e converte o registro encontrado para a entidade de
        domínio. Ela existe para ocultar experiências alheias ou removidas e
        manter o ORM dentro do adapter.
        """
        consulta = select(ExperienciaProfissionalRegistro).where(
            ExperienciaProfissionalRegistro.id == experiencia_id.valor,
            ExperienciaProfissionalRegistro.usuario_id == usuario_id.valor,
            ExperienciaProfissionalRegistro.deleted_at.is_(None),
        )
        registro = await self._session.scalar(consulta)
        if registro is None:
            return None
        return para_experiencia(registro)

    async def obter_por_id_e_usuario_incluindo_excluidas(
        self, experiencia_id: ExperienciaProfissionalId, usuario_id: UsuarioId
    ) -> ExperienciaProfissional | None:
        """Obtém a experiência própria, ativa ou excluída, por ID e proprietário.

        A consulta filtra somente identidade e dono, sem restringir o marcador
        de exclusão, e reconstrói a entidade com seu ``deleted_at``. Ela existe
        para tornar a exclusão idempotente sem revelar itens de terceiros.
        """
        consulta = select(ExperienciaProfissionalRegistro).where(
            ExperienciaProfissionalRegistro.id == experiencia_id.valor,
            ExperienciaProfissionalRegistro.usuario_id == usuario_id.valor,
        )
        registro = await self._session.scalar(consulta)
        if registro is None:
            return None
        return para_experiencia(registro)

    async def atualizar(self, experiencia: ExperienciaProfissional) -> bool:
        """Atualiza condicionalmente os campos editáveis de uma experiência ativa.

        Um UPDATE atômico confere ID, proprietário e ausência de exclusão, grava
        empresa, cargo, descrição e datas, sincroniza objetos carregados e faz
        ``flush`` sem commit. O booleano permite à Application traduzir
        ausência, exclusão ou concorrência como experiência não encontrada.
        """
        instrucao = (
            update(ExperienciaProfissionalRegistro)
            .where(
                ExperienciaProfissionalRegistro.id == experiencia.id.valor,
                ExperienciaProfissionalRegistro.usuario_id == experiencia.usuario_id.valor,
                ExperienciaProfissionalRegistro.deleted_at.is_(None),
            )
            .values(
                empresa=experiencia.empresa,
                cargo=experiencia.cargo,
                descricao=experiencia.descricao,
                data_inicio=experiencia.periodo.inicio,
                data_fim=experiencia.periodo.fim,
            )
            .execution_options(synchronize_session="fetch")
        )
        resultado = await self._session.execute(instrucao)
        await self._session.flush()
        return resultado.rowcount == 1

    async def marcar_excluida(
        self,
        experiencia_id: ExperienciaProfissionalId,
        usuario_id: UsuarioId,
        deleted_at: datetime,
    ) -> bool:
        """Marca como excluída somente uma experiência ativa do proprietário.

        Um UPDATE condicional exige ID, dono e ``deleted_at`` nulo, grava apenas
        o instante recebido e faz ``flush`` sem commit; repetições não alteram
        linha alguma. O booleano permite à Application distinguir a primeira
        exclusão de uma disputa concorrente.
        """
        instrucao = (
            update(ExperienciaProfissionalRegistro)
            .where(
                ExperienciaProfissionalRegistro.id == experiencia_id.valor,
                ExperienciaProfissionalRegistro.usuario_id == usuario_id.valor,
                ExperienciaProfissionalRegistro.deleted_at.is_(None),
            )
            .values(deleted_at=deleted_at)
            .execution_options(synchronize_session="fetch")
        )
        resultado = await self._session.execute(instrucao)
        await self._session.flush()
        return resultado.rowcount == 1
