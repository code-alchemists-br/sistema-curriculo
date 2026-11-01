"""Conecta acesso e sessões às transações SQLAlchemy por requisição.

Os adapters abrem sessões curtas para consultar credenciais, emitir tokens e
validar cookies, delegando regras aos casos de uso e serviços de segurança. Eles
existem para tornar o login da aplicação executada independente de sessões
globais e preservar as fronteiras da Application.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.acesso_estudante import (
    AcessarEstudante,
    AcessarEstudanteEntrada,
)
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.application.ports import VerificadorSenha
from backend.application.sessoes import CriadorSessao
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.repositorio_sessao import (
    RepositorioSessaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_usuario import (
    RepositorioUsuarioSqlAlchemy,
)
from backend.infrastructure.security.autenticador_sessao import (
    AutenticadorSessaoPersistida,
)
from backend.infrastructure.security.tokens_sessao import CriadorSessaoSeguro


class AcessarEstudanteSqlAlchemy:
    """Executa a conferência de credenciais em uma sessão SQLAlchemy curta.

    O adapter cria o repositório de usuários para cada chamada e delega a regra
    de acesso ao caso de uso com o verificador de senha recebido. Ele existe
    para que login não retenha conexões nem leve SQL à Application.
    """

    def __init__(
        self,
        sessoes: async_sessionmaker[AsyncSession],
        verificador_senha: VerificadorSenha,
    ) -> None:
        """Armazena a fábrica de sessões e o verificador usado pelo acesso.

        O construtor não abre I/O; apenas mantém dependências de infraestrutura
        e segurança que serão usadas por requisição. Ele existe para permitir
        composição explícita e doubles sem alterar o caso de uso.
        """
        self._sessoes = sessoes
        self._verificador_senha = verificador_senha

    async def executar(self, entrada: AcessarEstudanteEntrada) -> UsuarioId:
        """Confere as credenciais e devolve a identidade da conta autenticada.

        O método abre uma sessão de leitura, constrói o repositório concreto e
        aguarda o caso de uso. Ele existe para que falhas de credencial não
        criem transações de escrita nem compartilhem estado entre requisições.
        """
        async with self._sessoes() as sessao:
            repositorio = RepositorioUsuarioSqlAlchemy(sessao)
            caso_de_uso = AcessarEstudante(repositorio, self._verificador_senha)
            return await caso_de_uso.executar(entrada)


class CriadorSessaoSqlAlchemy(CriadorSessao):
    """Emite e persiste uma sessão opaca em transação SQLAlchemy por chamada.

    O adapter cria uma sessão transacional, associa o repositório de sessões ao
    emissor seguro e confirma a gravação antes de devolver o token. Ele existe
    para que a resposta de login não contenha uma sessão que o banco perdeu.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Armazena a fábrica que abrirá a transação de cada novo login.

        O construtor mantém somente a infraestrutura de sessão sem iniciar
        conexões. Ele existe para que o ciclo de vida do banco permaneça na
        camada externa e não no handler HTTP.
        """
        self._sessoes = sessoes

    async def criar(self, usuario_id: UsuarioId) -> str:
        """Persiste o token resumido e devolve o valor opaco uma única vez.

        O método abre uma transação, delega geração ao emissor seguro e permite
        que o contexto confirme ou reverta a sessão. Ele existe para tornar a
        emissão atômica com o armazenamento de metadados da autenticação.
        """
        async with self._sessoes.begin() as sessao:
            repositorio = RepositorioSessaoSqlAlchemy(sessao)
            return await CriadorSessaoSeguro(repositorio).criar(usuario_id)


class AutenticadorSessaoSqlAlchemy(AutenticadorSessao):
    """Valida cookies consultando sessões persistidas em conexão curta.

    O adapter cria o repositório de sessões para cada requisição protegida e
    delega hash, expiração e revogação ao autenticador seguro. Ele existe para
    impedir cache de autenticação ou retenção de sessão SQLAlchemy no middleware.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Recebe a fábrica de sessões usada nas validações de cookie.

        O construtor não consulta o banco; ele preserva uma dependência externa
        que será aberta somente durante a autenticação. Ele existe para manter
        o middleware independente do ORM concreto.
        """
        self._sessoes = sessoes

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Devolve a identidade associada a token ativo ou a ausência segura.

        O método abre sessão de leitura, constrói o repositório e aguarda o
        autenticador persistido. Ele existe para que expiração e revogação sejam
        observadas a cada requisição protegida sem carregar tokens em memória.
        """
        async with self._sessoes() as sessao:
            repositorio = RepositorioSessaoSqlAlchemy(sessao)
            return await AutenticadorSessaoPersistida(repositorio).autenticar(token)
