"""Conecta os casos de formação a sessões curtas para atender a API real.

Cada executor abre uma sessão por chamada. As escritas confirmam ou revertem
pelo contexto transacional; a leitura encerra sua sessão sem commit de mutação,
preservando as regras nos casos de uso e no domínio.
"""

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.perfil_estudante import (
    CadastrarFormacaoAcademica,
    CadastrarFormacaoAcademicaEntrada,
    EditarFormacaoAcademica,
    EditarFormacaoAcademicaEntrada,
    ExcluirFormacaoAcademica,
    ExcluirFormacaoAcademicaEntrada,
    # Proveniência: decision-analysis prompts/backend/20261107-171028-listar-formacoes-academicas-v001.md#v001
    ListarFormacoesAcademicas,
    ListarFormacoesAcademicasEntrada,
)
from backend.application.ports import GeradorFormacaoAcademicaId, Relogio
from backend.domain.itens_perfil import FormacaoAcademica
from backend.infrastructure.persistence.sqlalchemy.repositorio_formacao_academica import (
    RepositorioFormacaoAcademicaSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_usuario import (
    RepositorioUsuarioSqlAlchemy,
)


# Proveniência: decision-analysis prompts/backend/20261107-171028-listar-formacoes-academicas-v001.md#v001
class ListarFormacoesAcademicasSqlAlchemy:
    """Conecta a consulta de formações a uma sessão curta por chamada.

    Constrói o repositório na sessão local e delega ao caso de uso existente,
    sem commit de mutação, para permitir leitura sem compartilhar sessões.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Guarda a fábrica sem abrir conexão para isolar cada leitura.

        Conserva somente a dependência configurada pela composição externa,
        permitindo criar e encerrar a sessão no atendimento de cada chamada.
        """
        self._sessoes = sessoes

    async def executar(
        self, entrada: ListarFormacoesAcademicasEntrada
    ) -> tuple[FormacaoAcademica, ...]:
        """Executa a consulta existente em sessão própria e preserva sua ordem.

        Abre o contexto da sessão, injeta o repositório no caso de uso e devolve
        seu resultado antes do encerramento, sem commit, para conectar a leitura
        à persistência sem incorporar regras de apresentação neste adapter.
        """
        async with self._sessoes() as sessao:
            caso = ListarFormacoesAcademicas(
                RepositorioFormacaoAcademicaSqlAlchemy(sessao)
            )
            return await caso.executar(entrada)


class RelogioUtc:
    """Fornece o instante atual em UTC usando o sistema para datar exclusões."""

    def agora(self) -> datetime:
        """Obtém a hora do sistema com fuso UTC para registrar a exclusão lógica."""
        return datetime.now(timezone.utc)


class CadastroFormacaoAcademicaSqlAlchemy:
    """Persiste cadastros em sessão própria delegando as regras à Application.

    Usa uma transação por chamada para garantir durabilidade antes da resposta.
    """

    def __init__(
        self,
        sessoes: async_sessionmaker[AsyncSession],
        gerador: GeradorFormacaoAcademicaId,
    ) -> None:
        """Guarda fábrica e gerador sem abrir conexão para atender cada cadastro."""
        self._sessoes = sessoes
        self._gerador = gerador

    async def executar(
        self, entrada: CadastrarFormacaoAcademicaEntrada
    ) -> FormacaoAcademica:
        """Cadastra pelo caso existente em begin para confirmar ou reverter tudo."""
        async with self._sessoes.begin() as sessao:
            caso = CadastrarFormacaoAcademica(
                RepositorioUsuarioSqlAlchemy(sessao),
                RepositorioFormacaoAcademicaSqlAlchemy(sessao),
                self._gerador,
            )
            return await caso.executar(entrada)


class EdicaoFormacaoAcademicaSqlAlchemy:
    """Confirma edições pelo caso existente em transações isoladas por chamada.

    Constrói o repositório na sessão local para não compartilhar estado HTTP.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Guarda a fábrica sem I/O para abrir uma transação por edição."""
        self._sessoes = sessoes

    async def executar(
        self, entrada: EditarFormacaoAcademicaEntrada
    ) -> FormacaoAcademica:
        """Delega a edição em begin para persistir sucesso ou reverter falhas."""
        async with self._sessoes.begin() as sessao:
            caso = EditarFormacaoAcademica(
                RepositorioFormacaoAcademicaSqlAlchemy(sessao)
            )
            return await caso.executar(entrada)


class ExclusaoFormacaoAcademicaSqlAlchemy:
    """Executa exclusão lógica transacional usando o caso de uso e o relógio.

    Cria repositório por chamada para confirmar a remoção antes da resposta.
    """

    def __init__(
        self, sessoes: async_sessionmaker[AsyncSession], relogio: Relogio
    ) -> None:
        """Guarda fábrica e relógio sem I/O para isolar cada exclusão lógica."""
        self._sessoes = sessoes
        self._relogio = relogio

    async def executar(
        self, entrada: ExcluirFormacaoAcademicaEntrada
    ) -> FormacaoAcademica:
        """Delega a exclusão em begin para confirmar sucesso ou reverter falhas."""
        async with self._sessoes.begin() as sessao:
            caso = ExcluirFormacaoAcademica(
                RepositorioFormacaoAcademicaSqlAlchemy(sessao), self._relogio
            )
            return await caso.executar(entrada)
