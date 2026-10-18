"""Implementa a porta de formação acadêmica com SQLAlchemy assíncrono.

O adapter converte a entidade em registro, adiciona-o à sessão injetada e
aguarda o flush sem controlar commit. Ele existe para conectar Application à
persistência relacional mantendo a transação sob controle da composição.
"""

# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports import RepositorioFormacaoAcademica
from backend.domain.itens_perfil import FormacaoAcademica
from backend.domain.value_objects import FormacaoAcademicaId, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
from backend.infrastructure.persistence.sqlalchemy.formacao_academica import (
    FormacaoAcademicaRegistro,
    para_formacao_academica,
    para_registro,
)


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
class RepositorioFormacaoAcademicaSqlAlchemy(RepositorioFormacaoAcademica):
    """Consulta e persiste formações na sessão assíncrona recebida.

    O adapter filtra consultas por identidade e proprietário, reconstrói
    entidades de domínio e altera registros mapeados sem controlar commit ou
    rollback. Ele existe para implementar a porta sem introduzir SQLAlchemy na
    Application.
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

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    async def obter_por_id_e_usuario(
        self, formacao_id: FormacaoAcademicaId, usuario_id: UsuarioId
    ) -> FormacaoAcademica | None:
        """Obtém a formação somente se os dois identificadores coincidirem.

        A consulta filtra ID e usuário na mesma instrução e converte o registro
        encontrado para a entidade de domínio. Ela existe para ocultar a
        existência de formações alheias e manter o ORM dentro do adapter.
        """
        consulta = select(FormacaoAcademicaRegistro).where(
            FormacaoAcademicaRegistro.id == formacao_id.valor,
            FormacaoAcademicaRegistro.usuario_id == usuario_id.valor,
            FormacaoAcademicaRegistro.deleted_at.is_(None),
        )
        registro = await self._session.scalar(consulta)
        if registro is None:
            return None
        return para_formacao_academica(registro)

    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    async def obter_por_id_e_usuario_incluindo_excluidas(
        self, formacao_id: FormacaoAcademicaId, usuario_id: UsuarioId
    ) -> FormacaoAcademica | None:
        """Obtém formação ativa ou excluída após conferir identidade e dono.

        A consulta restringe simultaneamente ID e usuário sem filtro de exclusão,
        permitindo à operação de exclusão repetir-se sem revelar registros alheios.
        """
        consulta = select(FormacaoAcademicaRegistro).where(
            FormacaoAcademicaRegistro.id == formacao_id.valor,
            FormacaoAcademicaRegistro.usuario_id == usuario_id.valor,
        )
        registro = await self._session.scalar(consulta)
        if registro is None:
            return None
        return para_formacao_academica(registro)

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    async def atualizar(self, formacao: FormacaoAcademica) -> bool:
        """Atualiza condicionalmente os seis campos de uma formação ativa.

        Um UPDATE atômico confere ID, proprietário e estado ativo, sincroniza
        objetos carregados e faz flush sem commit. O booleano permite à
        Application traduzir concorrência ou ausência como não encontrada.
        """
        instrucao = (
            update(FormacaoAcademicaRegistro)
            .where(
                FormacaoAcademicaRegistro.id == formacao.id.valor,
                FormacaoAcademicaRegistro.usuario_id == formacao.usuario_id.valor,
                FormacaoAcademicaRegistro.deleted_at.is_(None),
            )
            .values(
                instituicao=formacao.instituicao,
                curso=formacao.curso,
                nivel=formacao.nivel.value,
                data_inicio=formacao.periodo.inicio,
                data_fim=formacao.periodo.fim,
                status=formacao.status.value,
            )
            .execution_options(synchronize_session="fetch")
        )
        resultado = await self._session.execute(instrucao)
        await self._session.flush()
        return resultado.rowcount == 1

    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    async def marcar_excluida(
        self,
        formacao_id: FormacaoAcademicaId,
        usuario_id: UsuarioId,
        deleted_at: datetime,
    ) -> bool:
        """Marca como excluída somente uma formação ativa do proprietário.

        O UPDATE condicional preserva o primeiro instante em concorrências,
        sincroniza identidades ORM e faz flush sem controlar o commit externo.
        """
        instrucao = (
            update(FormacaoAcademicaRegistro)
            .where(
                FormacaoAcademicaRegistro.id == formacao_id.valor,
                FormacaoAcademicaRegistro.usuario_id == usuario_id.valor,
                FormacaoAcademicaRegistro.deleted_at.is_(None),
            )
            .values(deleted_at=deleted_at)
            .execution_options(synchronize_session="fetch")
        )
        resultado = await self._session.execute(instrucao)
        await self._session.flush()
        return resultado.rowcount == 1
