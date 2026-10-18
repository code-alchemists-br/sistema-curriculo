"""Mapeia projetos acadêmicos entre entidade e registro SQLAlchemy.

O modelo persiste identidade, proprietário e três textos limitados por checks
relacionais. As conversões preservam o domínio fora do ORM e existem para
armazenar projetos sem acoplar as camadas internas ao SQLAlchemy.
"""

from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
from backend.domain import (
    TAMANHO_MAXIMO_DESCRICAO_PROJETO,
    TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO,
    TAMANHO_MAXIMO_TITULO_PROJETO,
    TAMANHO_MINIMO_TEXTO_PROJETO,
    ProjetoAcademico,
    ProjetoAcademicoId,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class ProjetoAcademicoRegistro(Base):
    """Representa um projeto acadêmico em colunas relacionais.

    A tabela declara UUIDs, textos obrigatórios, FK para o usuário e checks de
    comprimento compatíveis com os bancos usados. Ela existe para persistir o
    projeto sem instrumentar sua entidade de domínio.
    """

    __tablename__ = "projetos_academicos"
    __table_args__ = (
        CheckConstraint(
            f"length(trim(titulo)) BETWEEN {TAMANHO_MINIMO_TEXTO_PROJETO} AND "
            f"{TAMANHO_MAXIMO_TITULO_PROJETO}",
            name="ck_projetos_academicos_titulo_tamanho",
        ),
        CheckConstraint(
            f"length(trim(descricao)) BETWEEN {TAMANHO_MINIMO_TEXTO_PROJETO} AND "
            f"{TAMANHO_MAXIMO_DESCRICAO_PROJETO}",
            name="ck_projetos_academicos_descricao_tamanho",
        ),
        CheckConstraint(
            f"length(trim(tecnologias)) BETWEEN {TAMANHO_MINIMO_TEXTO_PROJETO} AND "
            f"{TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO}",
            name="ck_projetos_academicos_tecnologias_tamanho",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "usuarios.id", name="fk_projetos_academicos_usuario_id_usuarios"
        ),
        nullable=False,
    )
    titulo: Mapped[str] = mapped_column(
        String(TAMANHO_MAXIMO_TITULO_PROJETO), nullable=False
    )
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    tecnologias: Mapped[str] = mapped_column(
        String(TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO), nullable=False
    )


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
def para_registro(projeto: ProjetoAcademico) -> ProjetoAcademicoRegistro:
    """Converte a entidade validada em um registro SQLAlchemy.

    A função extrai os UUIDs e textos já normalizados sem alterar o projeto.
    Ela existe para traduzir o contrato do domínio em colunas persistíveis.
    """
    return ProjetoAcademicoRegistro(
        id=projeto.id.valor,
        usuario_id=projeto.usuario_id.valor,
        titulo=projeto.titulo,
        descricao=projeto.descricao,
        tecnologias=projeto.tecnologias,
    )


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
def para_projeto_academico(
    registro: ProjetoAcademicoRegistro,
) -> ProjetoAcademico:
    """Reconstrói a entidade acadêmica a partir do registro ORM.

    A função recria os identificadores tipados e passa os textos pelo
    construtor do domínio. Ela existe para impedir que modelos SQLAlchemy
    atravessem as fronteiras internas da aplicação.
    """
    return ProjetoAcademico(
        id=ProjetoAcademicoId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        titulo=registro.titulo,
        descricao=registro.descricao,
        tecnologias=registro.tecnologias,
    )
