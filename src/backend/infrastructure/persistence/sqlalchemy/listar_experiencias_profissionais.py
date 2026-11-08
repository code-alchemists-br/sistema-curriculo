"""Conecta a listagem existente a sessões curtas para atender a leitura HTTP.

Abre uma sessão por chamada e injeta o repositório no caso de uso, sem commit
de mutação, para manter a composição da persistência fora das camadas internas.
"""

# Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.perfil_estudante import (
    ListarExperienciasProfissionais,
    ListarExperienciasProfissionaisEntrada,
)
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.infrastructure.persistence.sqlalchemy.repositorio_experiencia_profissional import (
    RepositorioExperienciaProfissionalSqlAlchemy,
)


class ListarExperienciasProfissionaisSqlAlchemy:
    """Executa a leitura existente com sessão e repositório por chamada.

    Conserva somente a fábrica de sessões e delega a consulta à Application
    para permitir leitura persistida sem duplicar regras ou compartilhar sessão.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Armazena a fábrica sem abrir conexão para isolar cada leitura.

        Guarda a dependência fornecida pela composição externa e cria a sessão
        somente ao executar, permitindo encerrar seus recursos por requisição.
        """
        self._sessoes = sessoes

    async def executar(
        self, entrada: ListarExperienciasProfissionaisEntrada
    ) -> tuple[ExperienciaProfissional, ...]:
        """Consulta em sessão própria e preserva a ordem retornada pelo caso.

        Abre o contexto da sessão, injeta o repositório e delega a execução sem
        commit para conectar a Application ao armazenamento com recursos curtos.
        """
        async with self._sessoes() as sessao:
            caso = ListarExperienciasProfissionais(
                RepositorioExperienciaProfissionalSqlAlchemy(sessao)
            )
            return await caso.executar(entrada)
