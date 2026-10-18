"""Implementa a porta de idioma com SQLAlchemy assíncrono.

O adapter consulta a chave técnica persistida e envia registros para a sessão
injetada, sem controlar a transação. Ele existe para conectar o caso de uso à
persistência relacional sem acoplar as camadas internas ao ORM.
"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
from backend.application.cadastro_idioma import IdiomaJaCadastrado
from backend.application.ports import RepositorioIdioma
from backend.domain.itens_perfil import Idioma
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.idioma import (
    IdiomaRegistro,
    para_registro,
)


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class RepositorioIdiomaSqlAlchemy(RepositorioIdioma):
    """Consulta e persiste idiomas usando uma sessão externa assíncrona.

    A implementação compara somente a chave já normalizada, adiciona o modelo
    ORM e usa ``flush`` para expor conflitos de unicidade sem executar commit.
    Ela existe para satisfazer a porta preservando o ciclo transacional da
    composição que forneceu a sessão.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Armazena a sessão que executará as operações de persistência.

        O construtor recebe a sessão criada na borda externa e não abre conexão
        própria. Ele existe para manter o adapter testável e subordinado ao
        ciclo de vida transacional da requisição.
        """
        self._session = session

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        idioma_normalizado: str,
    ) -> bool:
        """Informa se a chave de idioma já possui registro persistido.

        O método consulta os dois campos da restrição única, sem recalcular ou
        reinterpretar a chave recebida. Ele existe para permitir ao caso de uso
        detectar conflito antes da tentativa de inserção.
        """
        consulta = (
            select(IdiomaRegistro.id)
            .where(
                IdiomaRegistro.usuario_id == usuario_id.valor,
                IdiomaRegistro.idioma_normalizado == idioma_normalizado,
            )
            .limit(1)
        )
        return await self._session.scalar(consulta) is not None

    async def salvar(self, idioma: Idioma) -> None:
        """Envia um idioma válido à sessão e traduz colisão de unicidade.

        O método mapeia a entidade, chama ``flush`` e reconhece somente a
        restrição nomeada desta tabela como duplicidade conhecida. Ele existe
        para proteger contra corridas sem expor detalhes SQL ao caso de uso.
        """
        self._session.add(para_registro(idioma))
        try:
            await self._session.flush()
        except IntegrityError as erro:
            if _viola_chave_duplicidade(erro):
                raise IdiomaJaCadastrado(
                    "O idioma já está cadastrado."
                ) from erro
            raise


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
def _viola_chave_duplicidade(erro: IntegrityError) -> bool:
    """Identifica se uma falha SQL pertence à unicidade de idioma.

    A função compara o nome estável da constraint na causa do driver, sem
    transformar violações de outras tabelas em conflito de idioma. Ela
    existe para preservar a tradução de erro definida pela fronteira externa.
    """
    return "uq_idiomas_usuario_idioma_normalizado" in str(erro.orig)
