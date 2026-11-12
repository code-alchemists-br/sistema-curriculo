"""Conecta o cadastro existente a uma transação curta por requisição.

Abre uma sessão e injeta repositório e gerador no caso de uso, confirmando ou
revertendo pelo contexto SQLAlchemy para garantir durabilidade antes do HTTP 201.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.cadastro_experiencia_profissional import (
    CadastrarExperienciaProfissional,
    CadastrarExperienciaProfissionalEntrada,
)

# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
from backend.application.ports import GeradorExperienciaProfissionalId, Relogio
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.infrastructure.persistence.sqlalchemy.repositorio_experiencia_profissional import (
    RepositorioExperienciaProfissionalSqlAlchemy,
)


class CadastroExperienciaProfissionalSqlAlchemy:
    """Executa o cadastro existente dentro de uma transação por chamada.

    Constrói o repositório na sessão local e delega as regras à Application
    para conectar a rota ao banco sem compartilhar sessões entre requisições.
    """

    # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
    def __init__(
        self,
        sessoes: async_sessionmaker[AsyncSession],
        gerador_id: GeradorExperienciaProfissionalId,
        relogio: Relogio,
    ) -> None:
        """Guarda fábrica, gerador e relógio sem I/O para atender cada cadastro.

        Recebe as dependências da composição externa para criar a sessão apenas
        na execução, permitindo isolamento e substituição nos testes unitários.
        """
        self._sessoes = sessoes
        self._gerador_id = gerador_id
        self._relogio = relogio

    async def executar(
        self, entrada: CadastrarExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Confirma o cadastro antes de devolver a entidade criada pelo caso.

        Usa begin para abrir e encerrar sessão e transação, injeta o repositório
        no caso de uso e propaga falhas para reverter mudanças automaticamente,
        evitando sucesso HTTP para uma experiência que não foi persistida.
        """
        async with self._sessoes.begin() as sessao:
            caso = CadastrarExperienciaProfissional(
                RepositorioExperienciaProfissionalSqlAlchemy(sessao),
                self._gerador_id,
                # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
                self._relogio,
            )
            return await caso.executar(entrada)
