"""Compõe o caso de uso de listagem com sessões SQLAlchemy curtas.

O adapter abre uma sessão por chamada, cria o repositório existente e delega a
consulta ao caso de uso da Application. Ele existe para habilitar a listagem
HTTP sem manter sessões globais nem importar persistência na camada interna.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
from backend.application.consulta_associacao_curriculo_vaga import (
    ListarAssociacoesCurriculoVaga,
    ListarAssociacoesCurriculoVagaEntrada,
)
from backend.domain.associacao_curriculo_vaga import AssociacaoCurriculoVaga
from backend.infrastructure.persistence.sqlalchemy.repositorio_associacao_curriculo_vaga import (
    RepositorioAssociacaoCurriculoVagaSqlAlchemy,
)


# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
class ListarAssociacoesCurriculoVagaSqlAlchemy:
    """Executa a listagem existente com um repositório por sessão.

    A classe recebe uma fábrica de sessões e, para cada entrada, instancia o
    adapter SQLAlchemy e o caso de uso já existente. Ela existe para conectar a
    composição HTTP à persistência sem reter recursos entre requisições.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Armazena a fábrica que cria sessões de leitura por chamada.

        O construtor não abre conexões e conserva somente a dependência
        configurada na composição externa. Ele existe para permitir lifecycle
        curto de sessão e teste isolado do adapter.
        """
        self._sessoes = sessoes

    async def executar(
        self, entrada: ListarAssociacoesCurriculoVagaEntrada
    ) -> tuple[AssociacaoCurriculoVaga, ...]:
        """Executa o caso de uso dentro do contexto de uma sessão curta.

        O método abre a sessão, injeta o repositório SQLAlchemy no caso de uso e
        devolve sua página antes de fechar o contexto. Ele existe para expor a
        consulta sem acoplar Application ou API ao ORM.
        """
        async with self._sessoes() as sessao:
            repositorio = RepositorioAssociacaoCurriculoVagaSqlAlchemy(sessao)
            caso_de_uso = ListarAssociacoesCurriculoVaga(repositorio)
            return await caso_de_uso.executar(entrada)
