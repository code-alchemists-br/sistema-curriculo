"""Mapeia cursos complementares entre o domínio e as colunas SQLAlchemy externas.

O módulo conserva detalhes de tabela e chave técnica fora do domínio. Ele
existe para persistir cursos reutilizáveis sem permitir que modelos ORM
atravessem as fronteiras internas.
"""

from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
from backend.domain.itens_perfil import Curso
from backend.domain.value_objects import CursoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class CursoRegistro(Base):
    """Representa um curso complementar nas colunas relacionais da aplicação.

    O mapeamento armazena os textos exibíveis, a carga horária opcional e a chave
    canônica composta calculada pelo domínio, com unicidade por usuário, nome e
    instituição normalizados. Ele existe para reforçar no banco a mesma identidade
    lógica usada pelo caso de uso.
    """

    __tablename__ = "cursos"
    __table_args__ = (
        UniqueConstraint(
            "usuario_id",
            "nome_normalizado",
            "instituicao_normalizada",
            name="uq_cursos_usuario_nome_instituicao_normalizados",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("usuarios.id", name="fk_cursos_usuario_id_usuarios"),
        nullable=False,
    )
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    nome_normalizado: Mapped[str] = mapped_column(Text, nullable=False)
    instituicao: Mapped[str] = mapped_column(Text, nullable=False)
    instituicao_normalizada: Mapped[str] = mapped_column(Text, nullable=False)
    carga_horaria: Mapped[int | None] = mapped_column(Integer, nullable=True)


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
def para_registro(curso: Curso) -> CursoRegistro:
    """Converte um curso válido para seu registro persistível no SQLAlchemy.

    A função extrai identificadores e leva as chaves canônicas já calculadas para
    o ORM. Ela existe para evitar que o banco defina política própria de normalização
    ou receba entidades de domínio.
    """
    return CursoRegistro(
        id=curso.id.valor,
        usuario_id=curso.usuario_id.valor,
        nome=curso.nome,
        nome_normalizado=curso.nome_normalizado,
        instituicao=curso.instituicao,
        instituicao_normalizada=curso.instituicao_normalizada,
        carga_horaria=curso.carga_horaria,
    )


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
def para_curso(registro: CursoRegistro) -> Curso:
    """Reconstrói um curso de domínio a partir de um registro ORM persistido.

    A função recria value objects tipados, reexecutando as invariantes da
    entidade ao cruzar a fronteira. Ela existe para impedir que detalhes
    instrumentados do SQLAlchemy sejam usados nas camadas internas.
    """
    return Curso(
        id=CursoId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        nome=registro.nome,
        instituicao=registro.instituicao,
        carga_horaria=registro.carga_horaria,
    )
