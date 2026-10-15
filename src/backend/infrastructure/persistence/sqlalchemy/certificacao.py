"""Mapeia certificações entre o domínio e as colunas SQLAlchemy externas.

O módulo conserva detalhes de tabela e chave técnica fora do domínio. Ele
existe para persistir certificações reutilizáveis sem permitir que modelos ORM
atravessem as fronteiras internas.
"""

from uuid import UUID

from sqlalchemy import ForeignKey, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
from backend.domain.itens_perfil import Certificacao
from backend.domain.value_objects import CertificacaoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class CertificacaoRegistro(Base):
    """Representa uma certificação nas colunas relacionais da aplicação.

    O mapeamento armazena os textos exibíveis e as chaves canônicas calculadas pelo
    domínio, com unicidade por proprietário. Ele existe para reforçar no banco
    a mesma identidade lógica usada pelo caso de uso.
    """

    __tablename__ = "certificacoes"
    __table_args__ = (
        UniqueConstraint(
            "usuario_id",
            "nome_normalizado",
            "organizacao_emissora_normalizada",
            name="uq_certificacoes_usuario_nome_emissor_normalizados",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    usuario_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("usuarios.id", name="fk_certificacoes_usuario_id_usuarios"),
        nullable=False,
    )
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    nome_normalizado: Mapped[str] = mapped_column(Text, nullable=False)
    organizacao_emissora: Mapped[str] = mapped_column(Text, nullable=False)
    organizacao_emissora_normalizada: Mapped[str] = mapped_column(Text, nullable=False)


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
def para_registro(certificacao: Certificacao) -> CertificacaoRegistro:
    """Converte uma certificação válida para seu registro persistível.

    A função extrai identificadores e leva as chaves canônicas já calculadas para o
    ORM. Ela existe para evitar que o banco defina política própria de
    normalização ou receba entidades de domínio.
    """
    return CertificacaoRegistro(
        id=certificacao.id.valor,
        usuario_id=certificacao.usuario_id.valor,
        nome=certificacao.nome,
        nome_normalizado=certificacao.nome_normalizado,
        organizacao_emissora=certificacao.organizacao_emissora,
        organizacao_emissora_normalizada=certificacao.organizacao_emissora_normalizada,
    )


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
def para_certificacao(registro: CertificacaoRegistro) -> Certificacao:
    """Reconstrói uma certificação de domínio a partir de um registro ORM.

    A função recria value objects tipados, reexecutando as invariantes da
    entidade ao cruzar a fronteira. Ela existe para impedir que detalhes
    instrumentados do SQLAlchemy sejam usados nas camadas internas.
    """
    return Certificacao(
        id=CertificacaoId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        nome=registro.nome,
        organizacao_emissora=registro.organizacao_emissora,
    )
