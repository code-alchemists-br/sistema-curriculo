"""Executa o cadastro de certificação em uma transação SQLAlchemy por chamada.

O adapter abre sessão curta, conecta repositório e caso de uso existentes e
aguarda a confirmação antes de devolver a entidade. Ele existe para garantir
durabilidade sem levar o ciclo transacional para a Application ou para a API.
"""

# Proveniência: decision-analysis prompts/revisao/20261105-203823-auditoria-impacto-cursos-certificacoes-v002.md#v002

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.cadastro_certificacao import (
    CadastrarCertificacao,
    CadastrarCertificacaoEntrada,
)
from backend.application.ports import GeradorCertificacaoId
from backend.domain.itens_perfil import Certificacao
from backend.infrastructure.persistence.sqlalchemy.repositorio_certificacao import (
    RepositorioCertificacaoSqlAlchemy,
)


class CadastroCertificacaoSqlAlchemy:
    """Conecta o cadastro de certificação ao limite transacional externo.

    A unidade cria uma sessão por execução e delega as regras ao caso de uso,
    usando begin para confirmar sucesso ou reverter falhas. Ela existe para
    impedir sessões compartilhadas e sucesso antes da confirmação do banco.
    """

    def __init__(
        self,
        sessoes: async_sessionmaker[AsyncSession],
        gerador_id: GeradorCertificacaoId,
    ) -> None:
        """Guarda a fábrica de sessões e o gerador de identidade injetados.

        O construtor conserva somente dependências, sem abrir conexão ou
        transação. Ele existe para deixar a composição controlar os recursos
        que serão usados separadamente em cada cadastro.
        """
        self._sessoes = sessoes
        self._gerador_id = gerador_id

    async def executar(self, entrada: CadastrarCertificacaoEntrada) -> Certificacao:
        """Executa o cadastro e confirma a transação antes de retornar.

        O método monta repositório e caso de uso dentro de begin, deixando
        exceções escaparem para reversão e fechamento do contexto. Ele existe
        para preservar a atomicidade e propagar inclusive falhas de commit,
        sem transformar falhas inesperadas em sucesso ou duplicidade.
        """
        async with self._sessoes.begin() as sessao:
            repositorio = RepositorioCertificacaoSqlAlchemy(sessao)
            caso_de_uso = CadastrarCertificacao(repositorio, self._gerador_id)
            return await caso_de_uso.executar(entrada)
