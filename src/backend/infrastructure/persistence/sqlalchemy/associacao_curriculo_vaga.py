"""Mapeia associações currículo-vaga e suas classificações no SQLAlchemy.

O módulo converte o agregado de domínio em registros relacionais com identidade
composta e reconstrói o estado válido a partir dessas linhas. Ele existe para
persistir a associação sem instrumentar o Domain com detalhes de ORM.
"""

from collections.abc import Iterable
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
from backend.domain.associacao_curriculo_vaga import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
)
from backend.domain.value_objects import CurriculoId, VagaId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
class AssociacaoCurriculoVagaRegistro(Base):
    """Representa uma associação persistida identificada pelo par currículo-vaga.

    A tabela declara o par como chave primária e referencia o currículo local;
    a vaga permanece uma referência textual externa. Ela existe para impor a
    unicidade aprovada sem adicionar uma identidade técnica.
    """

    __tablename__ = "associacoes_curriculo_vaga"
    __table_args__ = (
        PrimaryKeyConstraint(
            "curriculo_id",
            "vaga_id",
            name="pk_associacoes_curriculo_vaga",
        ),
    )

    curriculo_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "curriculos.id",
            name="fk_associacoes_curriculo_vaga_curriculo_id_curriculos",
        ),
        nullable=False,
    )
    vaga_id: Mapped[str] = mapped_column(Text, nullable=False)


# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
class ClassificacaoAssociacaoRegistro(Base):
    """Armazena uma classificação sem duplicá-la para o mesmo par.

    A linha usa o par da associação mais o valor textual da classificação como
    chave composta e referencia a associação proprietária. Ela existe para
    persistir todas as classificações normalizadas no mesmo conjunto relacional.
    """

    __tablename__ = "classificacoes_associacao_curriculo_vaga"
    __table_args__ = (
        PrimaryKeyConstraint(
            "curriculo_id",
            "vaga_id",
            "classificacao",
            name="pk_classificacoes_associacao_curriculo_vaga",
        ),
        ForeignKeyConstraint(
            ["curriculo_id", "vaga_id"],
            [
                "associacoes_curriculo_vaga.curriculo_id",
                "associacoes_curriculo_vaga.vaga_id",
            ],
            name="fk_classificacoes_associacao_assoc_curriculo_vaga",
            ondelete="CASCADE",
        ),
    )

    curriculo_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    vaga_id: Mapped[str] = mapped_column(Text, nullable=False)
    classificacao: Mapped[str] = mapped_column(Text, nullable=False)


# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
def para_registro(
    associacao: AssociacaoCurriculoVaga,
) -> AssociacaoCurriculoVagaRegistro:
    """Converte a raiz do agregado para seu registro ORM.

    A função extrai os valores primitivos dos identificadores tipados e cria
    somente a linha da associação. Ela existe para persistir a identidade
    natural sem expor SQLAlchemy ao caso de uso.
    """
    return AssociacaoCurriculoVagaRegistro(
        curriculo_id=associacao.curriculo_id.valor,
        vaga_id=associacao.vaga_id.valor,
    )


# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
def para_registros_classificacoes(
    associacao: AssociacaoCurriculoVaga,
) -> tuple[ClassificacaoAssociacaoRegistro, ...]:
    """Converte classificações do agregado em linhas ordenadas e distintas.

    A função usa o conjunto protegido pelo agregado e ordena pelo valor textual
    para produzir registros determinísticos. Ela existe para persistir somente
    classificações válidas, incluindo as normalizadas pelo Domain.
    """
    return tuple(
        ClassificacaoAssociacaoRegistro(
            curriculo_id=associacao.curriculo_id.valor,
            vaga_id=associacao.vaga_id.valor,
            classificacao=classificacao.value,
        )
        for classificacao in sorted(
            associacao.classificacoes, key=lambda item: item.value
        )
    )


# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
def para_associacao(
    registro: AssociacaoCurriculoVagaRegistro,
    classificacoes: Iterable[ClassificacaoAssociacaoRegistro],
) -> AssociacaoCurriculoVaga:
    """Reconstrói o agregado a partir da linha e das classificações relacionadas.

    A função recria VOs e enum pelos valores persistidos e passa a coleção ao
    construtor do Domain, que valida e normaliza o agregado. Ela existe para
    devolver um objeto de negócio válido em vez de expor registros ORM.
    """
    return AssociacaoCurriculoVaga(
        curriculo_id=CurriculoId(registro.curriculo_id),
        vaga_id=VagaId(registro.vaga_id),
        classificacoes=(
            ClassificacaoAssociacao(item.classificacao) for item in classificacoes
        ),
    )
