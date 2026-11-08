"""Conecta os casos de projeto a sessões assíncronas curtas por chamada.

Compõe repositórios locais e contextos transacionais para escritas, mantendo
as regras nos casos internos e a durabilidade fora do repositório.
"""

# Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application import (
    CadastrarProjetoAcademico,
    CadastrarProjetoAcademicoEntrada,
    ConsultarProjetoAcademico,
    ConsultarProjetoAcademicoEntrada,
    EditarProjetoAcademico,
    EditarProjetoAcademicoEntrada,
    ExcluirProjetoAcademico,
    ExcluirProjetoAcademicoEntrada,
    GeradorProjetoAcademicoId,
    Relogio,
)
from backend.domain import ProjetoAcademico
from backend.infrastructure.persistence.sqlalchemy.repositorio_projeto_academico import (
    RepositorioProjetoAcademicoSQLAlchemy,
)


class CadastroProjetoAcademicoSqlAlchemy:
    """Executa cadastro usando caso existente e transação por chamada.

    Cria sessão e repositório locais para confirmar sucesso ou reverter falha
    sem compartilhar sessão entre requisições nem duplicar regras do núcleo.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession],
                 gerador: GeradorProjetoAcademicoId) -> None:
        """Guarda fábrica e gerador injetados sem abrir conexão.

        Conserva as dependências externas para criar a transação somente na
        execução, isolando o ciclo de cada cadastro persistido.
        """
        self._sessoes = sessoes
        self._gerador = gerador

    async def executar(self, entrada: CadastrarProjetoAcademicoEntrada) -> ProjetoAcademico:
        """Delega o cadastro em begin e devolve a entidade após confirmação.

        Injeta repositório e gerador no caso interno para persistir pelo fluxo
        existente, deixando commit ou rollback a cargo do contexto da sessão.
        """
        async with self._sessoes.begin() as sessao:
            return await CadastrarProjetoAcademico(
                RepositorioProjetoAcademicoSQLAlchemy(sessao), self._gerador
            ).executar(entrada)


class ConsultaProjetoAcademicoSqlAlchemy:
    """Conecta detalhe por ID a uma sessão própria sem commit de mutação.

    Cria repositório por chamada e delega ao caso existente para permitir
    leitura independente do ciclo de vida das requisições e da engine.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Guarda a fábrica sem I/O para abrir e encerrar cada leitura.

        Conserva somente a dependência de composição para impedir sessão global
        compartilhada e permitir injeção de contexto isolado nos testes.
        """
        self._sessoes = sessoes

    async def executar(self, entrada: ConsultarProjetoAcademicoEntrada) -> ProjetoAcademico:
        """Executa o caso de consulta na sessão local sem commit.

        Injeta repositório no caso existente e devolve seu resultado antes de
        encerrar o contexto, para manter o ORM fora da Application.
        """
        async with self._sessoes() as sessao:
            return await ConsultarProjetoAcademico(
                RepositorioProjetoAcademicoSQLAlchemy(sessao)
            ).executar(entrada)


class EdicaoProjetoAcademicoSqlAlchemy:
    """Conecta substituição completa a uma transação curta por chamada.

    Injeta repositório local no caso existente para confirmar a edição antes
    da resposta sem introduzir regras de negócio no executor externo.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Guarda fábrica injetada sem abrir conexão durante a composição.

        Retém a dependência para abrir um contexto begin por edição e impedir
        compartilhamento de estado entre atendimentos.
        """
        self._sessoes = sessoes

    async def executar(self, entrada: EditarProjetoAcademicoEntrada) -> ProjetoAcademico:
        """Delega a edição em begin para confirmar sucesso ou reverter erro.

        Cria o repositório na sessão local e chama o caso existente para
        coordenar durabilidade sem reimplementar a validação dos textos.
        """
        async with self._sessoes.begin() as sessao:
            return await EditarProjetoAcademico(
                RepositorioProjetoAcademicoSQLAlchemy(sessao)
            ).executar(entrada)


class ExclusaoProjetoAcademicoSqlAlchemy:
    """Conecta exclusão lógica ao caso existente em transação isolada.

    Injeta repositório e relógio para preservar a idempotência no núcleo e
    confirmar a marcação antes da resposta, sem tocar em seleções de currículo.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession], relogio: Relogio) -> None:
        """Guarda fábrica e relógio sem executar recursos durante composição.

        Conserva dependências externas para criar sessões por chamada e usar
        a política temporal existente sem fixar relógio no caso de uso.
        """
        self._sessoes = sessoes
        self._relogio = relogio

    async def executar(self, entrada: ExcluirProjetoAcademicoEntrada) -> ProjetoAcademico:
        """Delega exclusão no contexto begin e propaga resultado ou falha.

        Injeta portas no caso existente para preservar o primeiro instante e
        permitir que o contexto confirme ou reverta a transação por chamada.
        """
        async with self._sessoes.begin() as sessao:
            return await ExcluirProjetoAcademico(
                RepositorioProjetoAcademicoSQLAlchemy(sessao), self._relogio
            ).executar(entrada)
