"""Implementa a porta de link profissional com SQLAlchemy assíncrono.

O adapter consulta a chave técnica persistida e envia registros para a sessão
injetada, sem controlar a transação. Ele existe para conectar o caso de uso à
persistência relacional sem acoplar as camadas internas ao ORM.
"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.application.cadastro_link_profissional import LinkProfissionalJaCadastrado
from backend.application.ports import RepositorioLinkProfissional
from backend.domain.itens_perfil import LinkProfissional
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.link_profissional import (
    LinkProfissionalRegistro,
    para_registro,
)


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class RepositorioLinkProfissionalSqlAlchemy(RepositorioLinkProfissional):
    """Consulta e persiste links profissionais usando uma sessão externa assíncrona.

    A implementação compara a chave canônica url_normalizada, adiciona o modelo
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
        url_normalizada: str,
    ) -> bool:
        """Informa se a chave de link profissional já possui registro persistido.

        O método consulta os campos da restrição única por proprietário e URL
        normalizada, sem recalcular ou reinterpretar a chave recebida. Ele existe
        para permitir ao caso de uso detectar conflito antes da tentativa de inserção.
        """
        consulta = (
            select(LinkProfissionalRegistro.id)
            .where(
                LinkProfissionalRegistro.usuario_id == usuario_id.valor,
                LinkProfissionalRegistro.url_normalizada == url_normalizada,
            )
            .limit(1)
        )
        return await self._session.scalar(consulta) is not None

    async def salvar(self, link: LinkProfissional) -> None:
        """Envia um link profissional válido à sessão e traduz colisão de unicidade.

        O método mapeia a entidade, chama ``flush`` e reconhece a restrição única
        nomeada desta tabela como duplicidade conhecida relançando LinkProfissionalJaCadastrado.
        Ele existe para proteger contra concorrência sem expor detalhes SQL ao caso de uso.
        """
        self._session.add(para_registro(link))
        try:
            await self._session.flush()
        except IntegrityError as erro:
            if _viola_chave_duplicidade(erro):
                raise LinkProfissionalJaCadastrado(
                    "Link profissional já cadastrado para este usuário."
                ) from erro
            raise


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def _viola_chave_duplicidade(erro: IntegrityError) -> bool:
    """Identifica se uma falha SQL pertence à unicidade de link profissional.

    A função compara o nome estável da constraint na mensagem do erro ou em
    sua causa original, sem transformar violações de outras tabelas em conflito de link.
    Ela existe para preservar a tradução de erro definida pela fronteira externa.
    """
    orig_str = str(erro.orig) if erro.orig else ""
    erro_str = str(erro)
    nome_constraint = "uq_links_profissionais_usuario_url_normalizada"
    return nome_constraint in orig_str or nome_constraint in erro_str
