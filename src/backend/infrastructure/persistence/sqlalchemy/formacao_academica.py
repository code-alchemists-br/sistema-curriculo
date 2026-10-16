"""Mapeia formações acadêmicas entre o domínio e as colunas SQLAlchemy.

O modelo armazena textos limitados, enums como texto e período em colunas
relacionais com CHECKs coerentes com o contrato do domínio. Ele existe para
persistir formações sem expor SQLAlchemy às camadas internas.
"""

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.itens_perfil import (
    TAMANHO_MAXIMO_TEXTO_FORMACAO,
    TAMANHO_MINIMO_TEXTO_FORMACAO,
    FormacaoAcademica,
    NivelFormacaoAcademica,
    StatusFormacaoAcademica,
)
from backend.domain.value_objects import FormacaoAcademicaId, Periodo, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
class FormacaoAcademicaRegistro(Base):
    """Representa uma formação acadêmica em colunas relacionais.

    A tabela persiste os enums por seus valores textuais e reforça limites,
    vocabulário e período por constraints. Ela existe para armazenar o item de
    perfil associado ao estudante sem instrumentar a entidade de domínio.
    """

    __tablename__ = "formacoes_academicas"
    __table_args__ = (
        CheckConstraint(
            f"length(trim(instituicao)) BETWEEN "
            f"{TAMANHO_MINIMO_TEXTO_FORMACAO} AND "
            f"{TAMANHO_MAXIMO_TEXTO_FORMACAO}",
            name="ck_formacoes_instituicao_tamanho",
        ),
        CheckConstraint(
            f"length(trim(curso)) BETWEEN "
            f"{TAMANHO_MINIMO_TEXTO_FORMACAO} AND "
            f"{TAMANHO_MAXIMO_TEXTO_FORMACAO}",
            name="ck_formacoes_curso_tamanho",
        ),
        CheckConstraint(
            "nivel IN ("
            + ", ".join(f"'{nivel.value}'" for nivel in NivelFormacaoAcademica)
            + ")",
            name="ck_formacoes_nivel_valido",
        ),
        CheckConstraint(
            "status IN ("
            + ", ".join(f"'{status.value}'" for status in StatusFormacaoAcademica)
            + ")",
            name="ck_formacoes_status_valido",
        ),
        CheckConstraint(
            "(status = 'em_andamento' AND "
            "(data_fim IS NULL OR data_fim >= data_inicio)) OR "
            "(status = 'concluido' AND data_fim IS NOT NULL AND "
            "data_fim >= data_inicio) OR "
            "(status = 'interrompido' AND "
            "(data_fim IS NULL OR data_fim >= data_inicio))",
            name="ck_formacoes_status_periodo_coerente",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("usuarios.id", name="fk_formacoes_usuario_id_usuarios"),
        nullable=False,
    )
    instituicao: Mapped[str] = mapped_column(
        String(TAMANHO_MAXIMO_TEXTO_FORMACAO), nullable=False
    )
    curso: Mapped[str] = mapped_column(
        String(TAMANHO_MAXIMO_TEXTO_FORMACAO), nullable=False
    )
    nivel: Mapped[str] = mapped_column(Text, nullable=False)
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
def para_registro(formacao: FormacaoAcademica) -> FormacaoAcademicaRegistro:
    """Converte uma formação válida em seu registro SQLAlchemy.

    A conversão extrai UUIDs, datas e valores textuais dos enums, sem modificar
    a entidade. Ela existe para traduzir o contrato interno em colunas externas.
    """
    return FormacaoAcademicaRegistro(
        id=formacao.id.valor,
        usuario_id=formacao.usuario_id.valor,
        instituicao=formacao.instituicao,
        curso=formacao.curso,
        nivel=formacao.nivel.value,
        data_inicio=formacao.periodo.inicio,
        data_fim=formacao.periodo.fim,
        status=formacao.status.value,
        # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
        deleted_at=formacao.deleted_at,
    )


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
def para_formacao_academica(
    registro: FormacaoAcademicaRegistro,
) -> FormacaoAcademica:
    """Reconstrói a formação de domínio a partir de um registro persistido.

    A função recria identificadores, enums e período tipados, reaplicando as
    invariantes da entidade. Ela existe para evitar que o modelo ORM atravesse
    a fronteira da infraestrutura.
    """
    return FormacaoAcademica(
        id=FormacaoAcademicaId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        instituicao=registro.instituicao,
        curso=registro.curso,
        nivel=NivelFormacaoAcademica(registro.nivel),
        periodo=Periodo(registro.data_inicio, registro.data_fim),
        status=StatusFormacaoAcademica(registro.status),
        # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
        deleted_at=registro.deleted_at,
    )
