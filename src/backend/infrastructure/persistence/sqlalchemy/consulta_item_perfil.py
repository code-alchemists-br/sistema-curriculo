"""Lê um item completo do perfil consultando o banco pelo seu tipo.

O módulo implementa a porta ``ConsultaItemPerfil`` usada pela prévia e pela
revisão de uma versão do currículo. Ele existe para que a Application leia os
seis tipos de item por um único contrato, sem conhecer as tabelas nem o ORM.
"""

from collections.abc import Callable
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports import ConsultaItemPerfil, ItemPerfil
from backend.domain.value_objects import (
    CompetenciaId,
    DocumentoId,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    IdiomaId,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
)
from backend.infrastructure.persistence.sqlalchemy.competencia import (
    CompetenciaRegistro,
    para_competencia,
)
from backend.infrastructure.persistence.sqlalchemy.documento import (
    DocumentoRegistro,
    para_documento,
)
from backend.infrastructure.persistence.sqlalchemy.experiencia_profissional import (
    ExperienciaProfissionalRegistro,
    para_experiencia,
)
from backend.infrastructure.persistence.sqlalchemy.formacao_academica import (
    FormacaoAcademicaRegistro,
    para_formacao_academica,
)
from backend.infrastructure.persistence.sqlalchemy.idioma import (
    IdiomaRegistro,
    para_idioma,
)
from backend.infrastructure.persistence.sqlalchemy.projeto_academico import (
    ProjetoAcademicoRegistro,
    para_projeto_academico,
)

_LEITURA_POR_TIPO_DE_ID: dict[type, tuple[type, Callable[[Any], ItemPerfil]]] = {
    FormacaoAcademicaId: (FormacaoAcademicaRegistro, para_formacao_academica),
    ExperienciaProfissionalId: (ExperienciaProfissionalRegistro, para_experiencia),
    ProjetoAcademicoId: (ProjetoAcademicoRegistro, para_projeto_academico),
    CompetenciaId: (CompetenciaRegistro, para_competencia),
    IdiomaId: (IdiomaRegistro, para_idioma),
    DocumentoId: (DocumentoRegistro, para_documento),
}


class ConsultaItemPerfilSqlAlchemy(ConsultaItemPerfil):
    """Obtém a entidade de um item do perfil pela tabela do seu tipo.

    A classe escolhe o modelo e o conversor pelo tipo do identificador da
    referência, busca o registro pela chave primária e devolve a entidade de
    domínio. Não filtra exclusão lógica: a porta orienta que a prévia decida o
    que fazer com itens excluídos já selecionados. Ela existe para atender a
    prévia sem expor o ORM à Application.
    """

    def __init__(self, sessao: AsyncSession) -> None:
        """Guarda a sessão externa usada nas leituras.

        O construtor não abre transação nem conexão; ele existe para que o ciclo
        de vida da sessão continue sob controle da composição.
        """
        self._sessao = sessao

    async def obter_item(self, referencia: ReferenciaCurriculo) -> ItemPerfil | None:
        """Devolve a entidade do item referenciado, ou ``None`` se não existir.

        O método seleciona modelo e conversor pelo tipo do identificador, busca
        o registro pela chave primária e o converte para o domínio. Ele existe
        para ler o conteúdo dos itens selecionados em uma versão.
        """
        leitura = _LEITURA_POR_TIPO_DE_ID.get(type(referencia.item_id))
        if leitura is None:
            return None

        registro_cls, converter = leitura
        registro = await self._sessao.get(registro_cls, referencia.item_id.valor)
        return converter(registro) if registro is not None else None
