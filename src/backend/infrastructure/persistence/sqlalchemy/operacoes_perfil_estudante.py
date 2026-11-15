"""Conecta os casos de uso de perfil a sessões curtas SQLAlchemy para a API real.

O módulo cria adaptadores que instanciam casos de uso com repositórios
baseados em sessões assíncronas isoladas por chamada. As operações de escrita
usam o bloco begin() para garantir confirmação ou reversão atômica, enquanto as
leituras encerram a sessão sem commit de mutação. Ele existe para conectar a
fronteira HTTP aos casos de uso de perfil sem violar as fronteiras da Clean
Architecture.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.perfil_completo import (
    AtualizarPerfilCompleto,
    AtualizarPerfilCompletoEntrada,
)
from backend.application.perfil_estudante import (
    ConsultarPerfilEstudante,
    ConsultarPerfilEstudanteEntrada,
    EditarPerfil,
    EditarPerfilEntrada,
    ExcluirPerfil,
    ExcluirPerfilEntrada,
)
from backend.application.ports import Relogio
from backend.domain.usuario import Usuario
from backend.infrastructure.persistence.sqlalchemy.repositorio_usuario import (
    RepositorioUsuarioSqlAlchemy,
)


class AtualizarPerfilCompletoSqlAlchemy:
    """Executa a atualização integral do perfil em transação própria por chamada.

    O adapter abre uma transação assíncrona com begin(), instancia o repositório
    SQLAlchemy na sessão local e delega a execução ao caso de uso. Ele existe
    para persistir alterações cadastrais de dados pessoais mantendo atomicidade
    e isolamento transacional por requisição HTTP.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Armazena a fábrica de sessões assíncronas sem abrir conexões imediatas.

        O construtor recebe o criador de sessões gerenciado pela composição e
        o retém para instanciação lazy por chamada. Ele existe para permitir
        injeção de dependência e desacoplamento do ciclo de vida da engine.
        """
        self._sessoes = sessoes

    async def executar(self, entrada: AtualizarPerfilCompletoEntrada) -> Usuario:
        """Executa o caso de uso de atualização integral dentro de uma transação.

        Abre o contexto de transação da sessão (begin), repassa a entrada ao
        caso de uso e confirma automaticamente a gravação caso nenhuma exceção
        ocorra. Ele existe para assegurar que dados pessoais e contatos sejam
        persistidos atomicamente no PostgreSQL.
        """
        async with self._sessoes.begin() as sessao:
            caso = AtualizarPerfilCompleto(RepositorioUsuarioSqlAlchemy(sessao))
            return await caso.executar(entrada)


class ConsultarPerfilSqlAlchemy:
    """Conecta a consulta de perfil a uma sessão curta de leitura por chamada.

    O adapter cria uma sessão assíncrona, instancia o repositório e executa o
    caso de uso sem transação de escrita, liberando os recursos ao final. Ele
    existe para disponibilizar a leitura de dados do estudante garantindo que
    nenhum estado de conexão seja compartilhado concorrentemente.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Armazena a fábrica de sessões assíncronas para consultas pontuais.

        O construtor retém a fábrica injetada pela camada externa sem iniciar
        I/O. Ele existe para suportar a injeção do executor na composição ASGI.
        """
        self._sessoes = sessoes

    async def executar(self, entrada: ConsultarPerfilEstudanteEntrada) -> Usuario:
        """Executa a consulta de perfil próprio em sessão de leitura dedicada.

        Abre o contexto assíncrono da sessão, delega a busca ao caso de uso e
        devolve o agregado Usuario ativo antes de descartar a sessão. Ele existe
        para consultar dados pessoais sem produzir efeitos colaterais no banco.
        """
        async with self._sessoes() as sessao:
            caso = ConsultarPerfilEstudante(RepositorioUsuarioSqlAlchemy(sessao))
            return await caso.executar(entrada)


class EdicaoPerfilSqlAlchemy:
    """Executa a edição de nome e e-mail em transação dedicada por chamada.

    O adapter inicia uma transação com begin(), conecta o repositório na sessão
    e delega a alteração ao caso de uso EditarPerfil. Ele existe para atender
    a rota de edição direta do perfil com garantia de consistência.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Armazena a fábrica de sessões sem abrir conexões no construtor.

        O construtor guarda a dependência da composição para uso em cada
        chamada. Ele existe para permitir substituição por doubles em testes.
        """
        self._sessoes = sessoes

    async def executar(self, entrada: EditarPerfilEntrada) -> Usuario:
        """Executa a edição de perfil em bloco transacional assíncrono.

        Abre o contexto begin() da sessão, executa a atualização no caso de
        uso e confirma a persistência ao sair do bloco. Ele existe para
        garantir que alterações parciais de dados de perfil sejam atômicas.
        """
        async with self._sessoes.begin() as sessao:
            caso = EditarPerfil(RepositorioUsuarioSqlAlchemy(sessao))
            return await caso.executar(entrada)


class ExclusaoPerfilSqlAlchemy:
    """Executa a exclusão lógica do perfil em transação dedicada por chamada.

    O adapter orquestra a marcação de exclusão pelo caso de uso dentro de
    begin(), utilizando o relógio para carimbar o instante de deleção. Ele
    existe para permitir exclusão lógica idempotente da conta do estudante.
    """

    def __init__(
        self, sessoes: async_sessionmaker[AsyncSession], relogio: Relogio
    ) -> None:
        """Armazena a fábrica de sessões e o relógio para registro de tempo.

        O construtor recebe as portas necessárias sem disparar operações de I/O.
        Ele existe para manter a orquestração desacoplada e testável.
        """
        self._sessoes = sessoes
        self._relogio = relogio

    async def executar(self, entrada: ExcluirPerfilEntrada) -> Usuario:
        """Executa a exclusão lógica do perfil dentro de uma transação ativa.

        Abre a transação assíncrona, invoca o caso de uso ExcluirPerfil com o
        repositório da sessão e o relógio, e confirma a mutação ao sair. Ele
        existe para persistir o instante de exclusão com segurança no banco.
        """
        async with self._sessoes.begin() as sessao:
            caso = ExcluirPerfil(RepositorioUsuarioSqlAlchemy(sessao), self._relogio)
            return await caso.executar(entrada)
