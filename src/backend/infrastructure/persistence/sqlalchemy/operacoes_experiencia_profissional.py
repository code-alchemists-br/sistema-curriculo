"""Conecta edição e exclusão de experiências a transações por requisição.

Cada executor cria uma sessão e delega ao caso de uso existente dentro de begin
para confirmar sucesso ou reverter falhas antes da resposta HTTP.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.edicao_experiencia_profissional import (
    EditarExperienciaProfissional,
    EditarExperienciaProfissionalEntrada,
)
from backend.application.exclusao_experiencia_profissional import (
    ExcluirExperienciaProfissional,
    ExcluirExperienciaProfissionalEntrada,
)
from backend.application.ports import Relogio
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.infrastructure.persistence.sqlalchemy.repositorio_experiencia_profissional import (
    RepositorioExperienciaProfissionalSqlAlchemy,
)


class EdicaoExperienciaProfissionalSqlAlchemy:
    """Executa a edição existente em transação própria por chamada.

    Constrói o repositório na sessão local para confirmar a alteração antes da
    resposta, mantendo regras de negócio na Application e no domínio.
    """

    # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
    def __init__(self, sessoes: async_sessionmaker[AsyncSession], relogio: Relogio) -> None:
        """Guarda fábrica e relógio sem I/O para isolar cada edição em uma sessão.

        Recebe a dependência da composição e abre a transação apenas na chamada
        para impedir compartilhamento de estado entre requisições.
        """
        self._sessoes = sessoes
        self._relogio = relogio

    async def executar(
        self, entrada: EditarExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Delega a edição dentro de begin para confirmar ou reverter mudanças.

        Injeta o repositório da sessão no caso existente e propaga sua resposta
        ou falha para garantir durabilidade sem duplicar regras de edição.
        """
        async with self._sessoes.begin() as sessao:
            caso = EditarExperienciaProfissional(
                # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
                RepositorioExperienciaProfissionalSqlAlchemy(sessao), self._relogio
            )
            return await caso.executar(entrada)


class ExclusaoExperienciaProfissionalSqlAlchemy:
    """Executa a exclusão lógica existente em transação por chamada.

    Injeta repositório e relógio no caso de uso para confirmar a marcação de
    exclusão antes da resposta sem decidir regras no adapter.
    """

    def __init__(
        self, sessoes: async_sessionmaker[AsyncSession], relogio: Relogio
    ) -> None:
        """Guarda fábrica e relógio sem I/O para isolar cada exclusão lógica.

        Recebe dependências externas substituíveis por doubles e cria a sessão
        apenas ao executar, mantendo o ciclo de recursos sob a composição.
        """
        self._sessoes = sessoes
        self._relogio = relogio

    async def executar(
        self, entrada: ExcluirExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Delega a exclusão em begin para confirmar sucesso ou reverter falhas.

        Constrói o repositório na sessão local e fornece o relógio ao caso
        existente para preservar idempotência e autoria sem purga dos dados.
        """
        async with self._sessoes.begin() as sessao:
            caso = ExcluirExperienciaProfissional(
                RepositorioExperienciaProfissionalSqlAlchemy(sessao), self._relogio
            )
            return await caso.executar(entrada)
