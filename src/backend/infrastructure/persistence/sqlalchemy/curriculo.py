"""Mapeia a versão de currículo em colunas externas para preservar o domínio desacoplado do ORM."""

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
from collections.abc import Iterable
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.curriculo import Curriculo
from backend.domain.value_objects import (
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    CompetenciaId,
    CurriculoId,
    DocumentoId,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    IdiomaId,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.usuario import Base

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001


class CurriculoRegistro(Base):
    """Representa a versão de currículo persistida por colunas escalares não nulas.

    O modelo declara a chave primária e a chave estrangeira do proprietário na
    infraestrutura, reunindo somente os dados escalares que o agregado
    ``Curriculo`` modela. Ele existe para armazenar a versão sem instrumentar o
    domínio; as referências aos itens do perfil ficam em ``CurriculoItemRegistro``.
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


def para_curriculo(
    registro: CurriculoRegistro,
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    itens: Iterable["CurriculoItemRegistro"] = (),
) -> Curriculo:
    """Converte o registro ORM e suas seleções em agregado de domínio.

    A função recria os value objects de identidade a partir das colunas e inclui
    no agregado, pelo próprio comportamento do domínio, uma referência para cada
    linha de seleção recebida. Ela existe para preservar a fronteira entre
    persistência SQLAlchemy e Application e para que o agregado carregado
    reflita a seleção persistida.
    """
    curriculo = Curriculo(
        id=CurriculoId(registro.id),
        usuario_id=UsuarioId(registro.usuario_id),
        titulo_versao=registro.titulo_versao,
        layout=registro.layout,
        is_public=registro.is_public,
    )
    for item in itens:
        curriculo.incluir_referencia(para_referencia(item.tipo, item.item_id))
    return curriculo


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


# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
def para_registro(curriculo: Curriculo) -> CurriculoRegistro:
    """Converte o agregado em registro extraindo valores primitivos dos VOs.

    A conversão cria uma instância externa sem modificar o agregado e sem as
    referências, convertidas à parte por ``para_registros_itens``, para que a
    sessão ORM insira UUIDs, título, layout e visibilidade. Ela existe para
    preservar a fronteira entre o domínio e o modelo SQLAlchemy na criação.
    """
    return CurriculoRegistro(
        id=curriculo.id.valor,
        usuario_id=curriculo.usuario_id.valor,
        titulo_versao=curriculo.titulo_versao,
        layout=curriculo.layout,
        is_public=curriculo.is_public,
    )


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
class CurriculoItemRegistro(Base):
    """Representa a seleção de um item do perfil em uma versão de currículo.

    O modelo guarda a versão, o tipo textual do item e o identificador do item,
    com chave primária composta que impede a mesma seleção duas vezes. Ele existe
    para persistir as referências do agregado em uma tabela única, sem chave
    estrangeira para os itens, cujas tabelas ainda não existem.
    """

    __tablename__ = "curriculo_itens"

    curriculo_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("curriculos.id", name="fk_curriculo_itens_curriculo_id_curriculos"),
        primary_key=True,
    )
    tipo: Mapped[str] = mapped_column(Text, primary_key=True)
    item_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
_TIPOS_POR_CLASSE = {
    FormacaoAcademicaId: "formacao_academica",
    ExperienciaProfissionalId: "experiencia_profissional",
    ProjetoAcademicoId: "projeto_academico",
    CompetenciaId: "competencia",
    IdiomaId: "idioma",
    DocumentoId: "documento",
}
_CLASSES_POR_TIPO = {tipo: classe for classe, tipo in _TIPOS_POR_CLASSE.items()}


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
def para_tipo_e_item_id(referencia: ReferenciaCurriculo) -> tuple[str, UUID]:
    """Converte a referência no par textual de tipo e UUID do item.

    A função consulta o tipo do identificador tipado e devolve o texto estável
    usado na coluna ``tipo`` junto do UUID puro. Ela existe para que a
    persistência represente os seis tipos de item sem expor value objects.
    """
    return _TIPOS_POR_CLASSE[type(referencia.item_id)], referencia.item_id.valor


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
def para_referencia(tipo: str, item_id: UUID) -> ReferenciaCurriculo:
    """Converte o par textual de tipo e UUID de volta em referência de domínio.

    A função escolhe a classe de identificador pelo texto armazenado e recria a
    referência tipada, recusando tipos desconhecidos. Ela existe para que o
    agregado carregado receba referências válidas e para que dado corrompido
    falhe de forma explícita.
    """
    classe = _CLASSES_POR_TIPO.get(tipo)
    if classe is None:
        raise ValueError(f"Tipo de item de currículo desconhecido: {tipo}.")
    return ReferenciaCurriculo(classe(item_id))


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
def para_registros_itens(curriculo: Curriculo) -> list[CurriculoItemRegistro]:
    """Converte as referências do agregado em registros de seleção ordenados.

    A função cria uma linha por referência, ordenada por tipo e identificador
    para que o resultado seja determinístico, sem modificar o agregado. Ela
    existe para que a sessão ORM insira a seleção da versão.
    """
    chaves = sorted(
        (para_tipo_e_item_id(referencia) for referencia in curriculo.referencias),
        key=lambda chave: (chave[0], str(chave[1])),
    )
    return [
        CurriculoItemRegistro(curriculo_id=curriculo.id.valor, tipo=tipo, item_id=item_id)
        for tipo, item_id in chaves
    ]