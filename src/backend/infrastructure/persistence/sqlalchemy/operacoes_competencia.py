"""Conecta os casos de uso de competência a sessões curtas SQLAlchemy para a API real.

O módulo cria adaptadores que instanciam casos de uso com repositórios baseados
em sessões assíncronas isoladas por chamada. As operações de escrita (cadastro e
exclusão) utilizam o bloco begin() para garantir confirmação ou reversão atômica,
enquanto a leitura encerra a sessão sem transação de mutação. Ele existe para
conectar a fronteira HTTP aos casos de uso de competência sem violar as fronteiras
da Clean Architecture.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.cadastro_competencia import (
    CadastrarCompetencia,
    CadastrarCompetenciaEntrada,
)
from backend.application.competencia import (
    ExcluirCompetencia,
    ExcluirCompetenciaEntrada,
    ListarCompetencias,
    ListarCompetenciasEntrada,
)
from backend.application.ports import GeradorCompetenciaId
from backend.domain.itens_perfil import Competencia
from backend.infrastructure.persistence.sqlalchemy.repositorio_competencia import (
    RepositorioCompetenciaSqlAlchemy,
)


class CadastroCompetenciaSqlAlchemy:
    """Executa o cadastro de competência em transação própria por chamada.

    O adapter abre uma transação assíncrona com begin(), instancia o repositório
    SQLAlchemy na sessão local e delega a criação e validação ao caso de uso. Ele
    existe para persistir competências garantindo atomicidade e isolamento
    transacional por requisição HTTP.
    """

    def __init__(
        self,
        sessoes: async_sessionmaker[AsyncSession],
        gerador_id: GeradorCompetenciaId,
    ) -> None:
        """Armazena a fábrica de sessões e o gerador de identificadores sem abrir conexões.

        O construtor recebe o criador de sessões e o gerador de IDs injetados pela
        composição externa para uso a cada chamada. Ele existe para permitir injeção
        de dependências e isolamento da engine.
        """
        self._sessoes = sessoes
        self._gerador_id = gerador_id

    async def executar(self, entrada: CadastrarCompetenciaEntrada) -> Competencia:
        """Executa o caso de uso de cadastro dentro de uma transação.

        Abre o contexto de transação da sessão (begin), repassa a entrada ao caso
        de uso CadastrarCompetencia e confirma automaticamente a gravação. Ele
        existe para persistir competências de forma atômica no PostgreSQL.
        """
        async with self._sessoes.begin() as sessao:
            caso = CadastrarCompetencia(
                repositorio=RepositorioCompetenciaSqlAlchemy(sessao),
                gerador_id=self._gerador_id,
            )
            return await caso.executar(entrada)


class ListarCompetenciasSqlAlchemy:
    """Conecta a listagem de competências a uma sessão curta de leitura por chamada.

    O adapter cria uma sessão assíncrona, instancia o repositório e executa o
    caso de uso de listagem sem transação de escrita, liberando os recursos ao final.
    Ele existe para consultar competências do estudante garantindo ausência de
    concorrência em conexões abertas.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Armazena a fábrica de sessões assíncronas para consultas pontuais.

        O construtor retém a fábrica injetada pela camada externa sem iniciar
        I/O. Ele existe para suportar a injeção do executor na composição ASGI.
        """
        self._sessoes = sessoes

    async def executar(
        self, entrada: ListarCompetenciasEntrada
    ) -> tuple[Competencia, ...]:
        """Executa a consulta de competências próprias em sessão de leitura dedicada.

        Abre o contexto assíncrono da sessão, delega a consulta ao caso de uso e
        devolve as entidades encontradas antes de descartar a sessão. Ele existe
        para consultar competências sem produzir efeitos colaterais no banco.
        """
        async with self._sessoes() as sessao:
            caso = ListarCompetencias(RepositorioCompetenciaSqlAlchemy(sessao))
            return await caso.executar(entrada)


class ExclusaoCompetenciaSqlAlchemy:
    """Executa a exclusão de competência em transação própria por chamada.

    O adapter inicia uma transação com begin(), conecta o repositório na sessão
    local e delega a remoção ao caso de uso ExcluirCompetencia. Ele existe para
    assegurar a exclusão segura e a reversibilidade atômica de competências.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Armazena a fábrica de sessões assíncronas para operações de exclusão.

        O construtor recebe a dependência externa sem abrir conexões antecipadas.
        Ele existe para viabilizar composição externa e testes unitários com doubles.
        """
        self._sessoes = sessoes

    async def executar(self, entrada: ExcluirCompetenciaEntrada) -> None:
        """Executa o caso de uso de exclusão de competência dentro de uma transação.

        Abre o contexto de transação da sessão (begin), repassa a entrada com o
        identificador da competência e do estudante ao caso de uso e confirma a
        remoção no banco. Ele existe para garantir a exclusão atômica no PostgreSQL.
        """
        async with self._sessoes.begin() as sessao:
            caso = ExcluirCompetencia(RepositorioCompetenciaSqlAlchemy(sessao))
            await caso.executar(entrada)
