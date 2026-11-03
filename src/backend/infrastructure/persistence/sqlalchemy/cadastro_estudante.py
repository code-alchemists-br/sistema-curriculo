"""Executa o cadastro de estudante com sessão SQLAlchemy por requisição.

O adapter abre uma transação curta, conecta o repositório concreto ao caso de
uso e confirma ou reverte a operação antes de devolver o agregado. Ele existe
para manter o ciclo de vida da sessão fora da Application e tornar o endpoint
de cadastro utilizável na composição executada pelo backend.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.cadastro_estudante import (
    CadastrarEstudante,
    CadastrarEstudanteEntrada,
)
from backend.application.ports import GeradorUsuarioId
from backend.domain.usuario import Usuario
from backend.infrastructure.persistence.sqlalchemy.repositorio_usuario import (
    RepositorioUsuarioSqlAlchemy,
)


class CadastroEstudanteSqlAlchemy:
    """Orquestra uma execução de cadastro dentro de transação SQLAlchemy.

    O adapter cria uma sessão por chamada, entrega o repositório ao caso de uso
    e usa o contexto transacional da fábrica para confirmar sucesso ou reverter
    falhas. Ele existe para evitar sessões globais e garantir durabilidade da
    conta antes da resposta HTTP ser enviada.
    """

    def __init__(
        self,
        sessoes: async_sessionmaker[AsyncSession],
        gerador_usuario_id: GeradorUsuarioId,
    ) -> None:
        """Recebe a fábrica de sessões e a estratégia externa de identidade.

        O construtor não abre conexão nem inicia transação; apenas guarda as
        dependências que serão usadas em cada requisição. Ele existe para que a
        composição controle infraestrutura e o caso de uso continue testável.
        """
        self._sessoes = sessoes
        self._gerador_usuario_id = gerador_usuario_id

    async def executar(self, entrada: CadastrarEstudanteEntrada) -> Usuario:
        """Persiste uma nova conta e confirma a transação da requisição.

        O método cria sessão curta, instancia o repositório concreto e delega
        a regra de duplicidade ao caso de uso dentro de ``begin``. Ele existe
        para que exceções interrompam a transação automaticamente e o endpoint
        nunca devolva sucesso para uma conta não confirmada no banco.
        """
        async with self._sessoes.begin() as sessao:
            repositorio = RepositorioUsuarioSqlAlchemy(sessao)
            caso_de_uso = CadastrarEstudante(
                repositorio,
                self._gerador_usuario_id,
            )
            return await caso_de_uso.executar(entrada)
