"""Conecta a recuperação de senha a transações SQLAlchemy curtas."""

from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.ports import Relogio
from backend.application.recuperacao_senha import (
    EntradaRedefinicaoSenha,
    EnvioRecuperacaoSenha,
    GeradorTokenRecuperacao,
    RedefinirSenha,
    RepositorioTokensRecuperacao,
    SolicitarRecuperacaoSenha,
)
from backend.domain.value_objects import Email, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.repositorio_sessao import (
    RepositorioSessaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_usuario import (
    RepositorioUsuarioSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.token_recuperacao_senha import (
    TokenRecuperacaoSenhaRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro


class RepositorioTokensRecuperacaoSqlAlchemy(RepositorioTokensRecuperacao):
    """Armazena, limita e consome tokens usando a transação recebida.

    O adapter substitui tokens anteriores, aplica intervalo mínimo por usuário
    e bloqueia a linha consumida. Ele existe para persistir uso único sem deixar
    SQLAlchemy atravessar a fronteira da Application.
    """

    INTERVALO_ENTRE_ENVIOS = timedelta(minutes=1)

    def __init__(self, sessao: AsyncSession) -> None:
        """Guarda a sessão transacional cujo ciclo de vida pertence ao executor.

        O construtor não abre conexão. Ele existe para que todas as operações
        do fluxo compartilhem a mesma transação externa.
        """
        self._sessao = sessao

    async def criar(
        self,
        usuario_id: UsuarioId,
        resumo: str,
        criada_em: datetime,
        expira_em: datetime,
    ) -> bool:
        """Cria solicitação se o usuário não excedeu o intervalo de um minuto.

        Consulta a solicitação mais recente, remove tokens anteriores e grava
        somente o resumo. Ela existe para restringir envios e manter um único
        link ativo por conta.
        """
        usuario_existe = await self._sessao.scalar(
            select(UsuarioRegistro.id)
            .where(UsuarioRegistro.id == usuario_id.valor)
            .with_for_update()
        )
        if usuario_existe is None:
            return False
        ultima_solicitacao = await self._sessao.scalar(
            select(func.max(TokenRecuperacaoSenhaRegistro.criada_em)).where(
                TokenRecuperacaoSenhaRegistro.usuario_id == usuario_id.valor
            )
        )
        if (
            ultima_solicitacao is not None
            and criada_em < ultima_solicitacao + self.INTERVALO_ENTRE_ENVIOS
        ):
            return False

        await self._sessao.execute(
            delete(TokenRecuperacaoSenhaRegistro).where(
                TokenRecuperacaoSenhaRegistro.usuario_id == usuario_id.valor
            )
        )
        self._sessao.add(
            TokenRecuperacaoSenhaRegistro(
                id=uuid4(),
                usuario_id=usuario_id.valor,
                token_hash=resumo,
                criada_em=criada_em,
                expira_em=expira_em,
                usada_em=None,
            )
        )
        await self._sessao.flush()
        return True

    async def consumir(self, resumo: str, instante: datetime) -> UsuarioId | None:
        """Marca como usado um token válido ainda não consumido.

        Seleciona com bloqueio de linha e atualiza antes de devolver o dono; a
        transação externa reverte consumo se uma escrita posterior falhar. Ela
        existe para impedir replay e concorrência na redefinição.
        """
        registro = await self._sessao.scalar(
            select(TokenRecuperacaoSenhaRegistro)
            .where(
                TokenRecuperacaoSenhaRegistro.token_hash == resumo,
                TokenRecuperacaoSenhaRegistro.expira_em > instante,
                TokenRecuperacaoSenhaRegistro.usada_em.is_(None),
            )
            .with_for_update()
        )
        if registro is None:
            return None
        registro.usada_em = instante
        await self._sessao.flush()
        return UsuarioId(registro.usuario_id)


class SolicitarRecuperacaoSenhaSqlAlchemy:
    """Persiste solicitação e devolve dados para envio após a resposta HTTP.

    O executor fecha a transação antes de devolver o envio pendente. Ele existe
    para que a API use tarefa de segundo plano e não exponha diferença de tempo
    entre conta existente e inexistente.
    """

    def __init__(
        self,
        sessoes: async_sessionmaker[AsyncSession],
        gerador: GeradorTokenRecuperacao,
        relogio: Relogio,
    ) -> None:
        """Recebe fábrica transacional e serviços de token e tempo.

        O construtor guarda dependências sem abrir conexões. Ele existe para
        que o executor possa ser composto ou substituído em testes.
        """
        self._sessoes = sessoes
        self._gerador = gerador
        self._relogio = relogio

    async def executar(self, email: Email) -> EnvioRecuperacaoSenha | None:
        """Cria token e devolve dados privados para agendamento do e-mail.

        A rota não serializa o resultado e agenda a entrega depois de responder.
        O método existe para manter SMTP fora da transação e da latência HTTP.
        """
        async with self._sessoes.begin() as sessao:
            caso = SolicitarRecuperacaoSenha(
                RepositorioUsuarioSqlAlchemy(sessao),
                RepositorioTokensRecuperacaoSqlAlchemy(sessao),
                self._gerador,
                self._relogio,
            )
            envio = await caso.executar(email)

        return envio


class RedefinirSenhaSqlAlchemy:
    """Aplica troca de senha, consumo de token e revogação atomicamente.

    O executor monta usuário, tokens e sessões na mesma transação. Ele existe
    para confirmar todas as alterações juntas ou revertê-las em caso de erro.
    """

    def __init__(
        self,
        sessoes: async_sessionmaker[AsyncSession],
        gerador: GeradorTokenRecuperacao,
        relogio: Relogio,
    ) -> None:
        """Guarda fábrica e serviços sem iniciar I/O.

        A composição entrega dependências reutilizáveis e cada chamada abre
        sua própria transação. Ela existe para isolar os pedidos concorrentes.
        """
        self._sessoes = sessoes
        self._gerador = gerador
        self._relogio = relogio

    async def executar(self, entrada: EntradaRedefinicaoSenha) -> bool:
        """Executa a redefinição no contexto transacional de uma solicitação.

        O caso consome o token, atualiza a conta e revoga sessões na mesma
        sessão SQLAlchemy. O resultado booleano permite resposta uniforme para
        token inválido, vencido ou reutilizado.
        """
        async with self._sessoes.begin() as sessao:
            caso = RedefinirSenha(
                RepositorioUsuarioSqlAlchemy(sessao),
                RepositorioTokensRecuperacaoSqlAlchemy(sessao),
                RepositorioSessaoSqlAlchemy(sessao),
                self._gerador,
                self._relogio,
            )
            return await caso.executar(entrada)
