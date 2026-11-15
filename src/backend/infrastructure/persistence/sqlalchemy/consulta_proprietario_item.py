"""Descobre o proprietário de um item do perfil consultando o banco.

O módulo implementa a porta ``ConsultaProprietarioItem`` usada pela seleção de
itens de uma versão do currículo. Ele existe para que a Application recuse
itens inexistentes ou de outro estudante sem conhecer as tabelas de cada tipo.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports import ConsultaProprietarioItem
from backend.domain.value_objects import (
    CompetenciaId,
    DocumentoId,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    IdiomaId,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.competencia import (
    CompetenciaRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.documento import DocumentoRegistro
from backend.infrastructure.persistence.sqlalchemy.experiencia_profissional import (
    ExperienciaProfissionalRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.formacao_academica import (
    FormacaoAcademicaRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.idioma import IdiomaRegistro
from backend.infrastructure.persistence.sqlalchemy.projeto_academico import (
    ProjetoAcademicoRegistro,
)

_REGISTRO_POR_TIPO_DE_ID = {
    FormacaoAcademicaId: FormacaoAcademicaRegistro,
    ExperienciaProfissionalId: ExperienciaProfissionalRegistro,
    ProjetoAcademicoId: ProjetoAcademicoRegistro,
    CompetenciaId: CompetenciaRegistro,
    IdiomaId: IdiomaRegistro,
    DocumentoId: DocumentoRegistro,
}


class ConsultaProprietarioItemSqlAlchemy(ConsultaProprietarioItem):
    """Consulta o dono de um item do perfil na tabela do seu tipo.

    A classe escolhe a tabela pelo tipo do identificador da referência, busca
    apenas a coluna ``usuario_id`` e ignora itens com exclusão lógica. Ela
    existe para atender a porta de seleção de itens sem expor o ORM à
    Application e sem carregar a entidade inteira só para conferir propriedade.
    """

    def __init__(self, sessao: AsyncSession) -> None:
        """Guarda a sessão externa usada nas consultas.

        O construtor não abre transação nem conexão; ele existe para que o ciclo
        de vida da sessão continue sob controle da composição.
        """
        self._sessao = sessao

    async def obter_proprietario(
        self, referencia: ReferenciaCurriculo
    ) -> UsuarioId | None:
        """Devolve o dono do item referenciado, ou ``None`` se não existir.

        O método seleciona o modelo pelo tipo do identificador, filtra por id e,
        quando o modelo tem ``deleted_at``, exclui itens removidos. Ele existe
        para que a seleção recuse itens ausentes, apagados ou de outro usuário
        antes de alterar a versão.
        """
        registro = _REGISTRO_POR_TIPO_DE_ID.get(type(referencia.item_id))
        if registro is None:
            return None

        consulta = select(registro.usuario_id).where(
            registro.id == referencia.item_id.valor
        )
        deleted_at = getattr(registro, "deleted_at", None)
        if deleted_at is not None:
            consulta = consulta.where(deleted_at.is_(None))

        dono = await self._sessao.scalar(consulta)
        return UsuarioId(dono) if dono is not None else None
