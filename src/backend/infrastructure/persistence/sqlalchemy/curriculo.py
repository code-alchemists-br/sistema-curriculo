"""Mapeia a versão de currículo em colunas externas para preservar o domínio desacoplado do ORM."""

from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.curriculo import Curriculo
from backend.domain.value_objects import CurriculoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001


class CurriculoRegistro(Base):
    """Representa a versão de currículo persistida por colunas escalares não nulas.

    O modelo declara a chave primária e a chave estrangeira do proprietário na
    infraestrutura, reunindo somente os dados que o agregado ``Curriculo`` hoje
    modela. Ele existe para armazenar a versão sem instrumentar o domínio e sem
    persistir ainda as referências aos itens do perfil.
    """

    __tablename__ = "curriculos"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("usuarios.id", name="fk_curriculos_usuario_id_usuarios"),
        nullable=False,
    )
    titulo_versao: Mapped[str] = mapped_column(Text, nullable=False)
    layout: Mapped[str] = mapped_column(Text, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False)


def para_curriculo(registro: CurriculoRegistro) -> Curriculo:
    """Converte o registro ORM recuperado em agregado de domínio sem referências.

    A função recria os value objects de identidade a partir das colunas e deixa
    o agregado com a coleção de referências vazia, pois as associações com os
    itens do perfil ainda não são persistidas. Ela existe para preservar a
    fronteira entre persistência SQLAlchemy e Application.
    """
    return Curriculo(
        id=CurriculoId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        titulo_versao=registro.titulo_versao,
        layout=registro.layout,
        is_public=registro.is_public,
    )


def atualizar_registro(registro: CurriculoRegistro, curriculo: Curriculo) -> None:
    """Copia título, layout e visibilidade do agregado para o registro existente.

    A função altera somente as três colunas editáveis e preserva a identidade e
    o proprietário do registro, deixando a sessão ORM detectar a mudança. Ela
    existe para que a atualização não toque associações nem colunas que a edição
    não gerencia.
    """
    registro.titulo_versao = curriculo.titulo_versao
    registro.layout = curriculo.layout
    registro.is_public = curriculo.is_public