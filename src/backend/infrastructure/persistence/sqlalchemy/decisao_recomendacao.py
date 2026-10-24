"""Mapeia decisões sobre recomendações entre o domínio e colunas SQLAlchemy externas.

O módulo conserva detalhes de tabela e chaves fora do domínio. Ele existe para
persistir a decisão do estudante sobre uma recomendação da revisão sem permitir
que modelos ORM atravessem as fronteiras internas da aplicação.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
from backend.domain.decisao_recomendacao import DecisaoEstudante, DecisaoRecomendacao
from backend.domain.value_objects import CurriculoId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
class DecisaoRecomendacaoRegistro(Base):
    """Representa a decisão do estudante sobre uma recomendação, em colunas.

    A chave primária é composta por versão de currículo e código da recomendação,
    de modo que haja uma só decisão por par, e a versão é uma chave estrangeira
    que remove as decisões junto com ela. O registro guarda a decisão em texto e o
    instante técnico, com fuso. Ele existe para materializar a tabela
    ``decisoes_recomendacao``.
    """

    __tablename__ = "decisoes_recomendacao"

    curriculo_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "curriculos.id",
            name="fk_decisoes_recomendacao_curriculo_id_curriculos",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    codigo: Mapped[str] = mapped_column(Text, primary_key=True)
    decisao: Mapped[str] = mapped_column(Text, nullable=False)
    decidida_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )


# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
def para_registro(decisao: DecisaoRecomendacao) -> DecisaoRecomendacaoRegistro:
    """Converte a decisão de domínio em registro persistível.

    A função extrai o UUID da versão, o código, o texto da decisão e o instante,
    sem expor value objects ao ORM. Ela existe para que o banco receba apenas
    valores primitivos.
    """
    return DecisaoRecomendacaoRegistro(
        curriculo_id=decisao.curriculo_id.valor,
        codigo=decisao.codigo,
        decisao=decisao.decisao.value,
        decidida_em=decisao.decidida_em,
    )


# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
def para_decisao(registro: DecisaoRecomendacaoRegistro) -> DecisaoRecomendacao:
    """Reconstrói a decisão de domínio a partir do registro persistido.

    A função recria a identidade da versão e a decisão pela enumeração, recusando
    texto desconhecido, e trata um instante sem fuso (como devolvem alguns bancos)
    como UTC, o fuso em que ele foi gravado. Ela existe para isolar o domínio de
    instâncias instrumentadas do SQLAlchemy.
    """
    instante = registro.decidida_em
    if instante.tzinfo is None:
        instante = instante.replace(tzinfo=UTC)
    return DecisaoRecomendacao(
        curriculo_id=CurriculoId(registro.curriculo_id),
        codigo=registro.codigo,
        decisao=DecisaoEstudante(registro.decisao),
        decidida_em=instante,
    )
