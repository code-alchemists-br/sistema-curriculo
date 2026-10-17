"""Mapeia experiências profissionais em registros SQLAlchemy externos.

O modelo converte a entidade e o período para colunas relacionais, mantendo o
domínio livre de ORM. Ele existe para persistir experiências reutilizáveis
associadas à conta proprietária.
"""

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import ExperienciaProfissionalId, Periodo, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


class ExperienciaProfissionalRegistro(Base):
    """Representa uma experiência profissional nas colunas do banco relacional.

    O mapeamento declara proprietário, textos, datas e o instante opcional de
    exclusão lógica sem instrumentar a entidade de domínio. Ele existe para
    armazenar o item de perfil conforme o contrato da aplicação e o vínculo com
    a conta do estudante.
    """

    __tablename__ = "experiencias_profissionais"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("usuarios.id", name="fk_experiencias_usuario_id_usuarios"),
        nullable=False,
    )
    empresa: Mapped[str] = mapped_column(Text, nullable=False)
    cargo: Mapped[str] = mapped_column(Text, nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim: Mapped[date | None] = mapped_column(Date, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


def para_registro(
    experiencia: ExperienciaProfissional,
) -> ExperienciaProfissionalRegistro:
    """Converte uma entidade válida para o modelo persistente externo.

    A função extrai UUIDs, datas e o instante de exclusão sem alterar a
    entidade. Ela existe para traduzir o contrato interno para colunas
    relacionais.
    """
    return ExperienciaProfissionalRegistro(
        id=experiencia.id.valor,
        usuario_id=experiencia.usuario_id.valor,
        empresa=experiencia.empresa,
        cargo=experiencia.cargo,
        descricao=experiencia.descricao,
        data_inicio=experiencia.periodo.inicio,
        data_fim=experiencia.periodo.fim,
        deleted_at=experiencia.deleted_at,
    )


def para_experiencia(
    registro: ExperienciaProfissionalRegistro,
) -> ExperienciaProfissional:
    """Reconstrói a entidade de domínio a partir de um registro persistido.

    A função recria identidades tipadas, ``Periodo`` e o instante de exclusão
    para reaplicar as invariantes de domínio na leitura. Ela existe para impedir
    que modelos ORM atravessem a fronteira da infraestrutura.
    """
    return ExperienciaProfissional(
        id=ExperienciaProfissionalId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        empresa=registro.empresa,
        cargo=registro.cargo,
        descricao=registro.descricao,
        periodo=Periodo(registro.data_inicio, registro.data_fim),
        deleted_at=registro.deleted_at,
    )
