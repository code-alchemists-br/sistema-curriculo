"""Valida recuperação e redefinição com API e PostgreSQL migrado."""

import hashlib
import os
import unittest
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.api.factory import create_app
from backend.domain.usuario import Usuario
from backend.domain.value_objects import Email, Nome, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.operacoes_recuperacao_senha import (
    RedefinirSenhaSqlAlchemy,
    SolicitarRecuperacaoSenhaSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_sessao import (
    RepositorioSessaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_usuario import (
    RepositorioUsuarioSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.sessao import SessaoRegistro
from backend.infrastructure.persistence.sqlalchemy.token_recuperacao_senha import (
    TokenRecuperacaoSenhaRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.usuario import (
    UsuarioRegistro,
)
from backend.infrastructure.security.senhas import DerivadorSenhaScrypt
from backend.infrastructure.security.tokens_recuperacao_senha import (
    GeradorTokenRecuperacaoSeguro,
)
from backend.tests.fixtures.credenciais_sessao import solicitar_asgi


class RelogioIntegracao:
    """Entrega instante UTC controlado para tokens e sessões do cenário."""

    def agora(self) -> datetime:
        """Devolve instante corrente com fuso para validar datas persistidas."""
        return datetime.now(timezone.utc)


class MailboxIntegracao:
    """Captura mensagens fora do banco sem contatar destinatários externos."""

    def __init__(self) -> None:
        """Cria lista de mensagens para o teste ler token entregue."""
        self.envios: list[tuple[Email, str]] = []

    async def enviar(self, email: Email, token: str) -> None:
        """Registra destinatário e token em memória sem emitir logs."""
        self.envios.append((email, token))


@unittest.skipUnless(
    os.environ.get("DATABASE_URL"),
    "Requer PostgreSQL fornecido pelo executor de integração.",
)
class RecuperacaoSenhaPostgreSqlTestCase(unittest.IsolatedAsyncioTestCase):
    """Exercita fluxo público, persistência de token e invalidação de sessões."""

    async def asyncSetUp(self) -> None:
        """Abre sessões no banco migrado e registra descarte da engine."""
        database_url = os.environ["DATABASE_URL"]
        self.engine = create_async_engine(database_url)
        self.addAsyncCleanup(self.engine.dispose)
        self.sessoes = async_sessionmaker(self.engine, expire_on_commit=False)
        self.relogio = RelogioIntegracao()
        self.gerador = GeradorTokenRecuperacaoSeguro()
        self.derivador = DerivadorSenhaScrypt()
        self.mailbox = MailboxIntegracao()
        self.usuario_id = UsuarioId(uuid4())
        self.email = Email(f"recuperacao-{self.usuario_id.valor}@example.test")
        self.senha_antiga = "Senha-Antiga-123"
        self.senha_nova = "Senha-Nova-456"
        usuario = Usuario(
            id=self.usuario_id,
            nome=Nome("Ana Recuperação"),
            email=self.email,
            hash_senha=self.derivador.derivar(self.senha_antiga),
        )
        instante = self.relogio.agora()
        async with self.sessoes.begin() as sessao:
            await RepositorioUsuarioSqlAlchemy(sessao).salvar(usuario)
            repositorio_sessoes = RepositorioSessaoSqlAlchemy(sessao)
            for indice in (1, 2):
                await repositorio_sessoes.salvar(
                    self.usuario_id,
                hashlib.sha256(
                    f"{self.usuario_id.valor}-sessao-{indice}".encode()
                ).hexdigest(),
                    instante,
                    instante + timedelta(hours=8),
                )
        solicitador = SolicitarRecuperacaoSenhaSqlAlchemy(
            self.sessoes, self.gerador, self.relogio
        )
        redefinidor = RedefinirSenhaSqlAlchemy(
            self.sessoes, self.gerador, self.relogio
        )
        self.app = create_app(
            solicitar_recuperacao_senha=solicitador,
            redefinir_senha=redefinidor,
            derivador_senha=self.derivador,
            enviador_recuperacao_senha=self.mailbox,
        )

    async def test_redefine_senha_uma_vez_e_revoga_todas_as_sessoes(self) -> None:
        """Confere resposta genérica, token protegido, nova senha e sessões revogadas."""
        pedido = await solicitar_asgi(
            self.app,
            "POST",
            "/recuperacoes-senha",
            dados={"email": self.email.valor},
        )
        self.assertEqual(pedido.status, 202)
        self.assertEqual(
            pedido.json(),
            {"mensagem": "Se houver uma conta associada, enviaremos instruções."},
        )
        self.assertFalse(pedido.cabecalhos("set-cookie"))
        self.assertEqual(len(self.mailbox.envios), 1)
        email_enviado, token = self.mailbox.envios[0]
        self.assertEqual(email_enviado, self.email)

        async with self.sessoes() as sessao:
            token_persistido = await sessao.scalar(
                select(TokenRecuperacaoSenhaRegistro).where(
                    TokenRecuperacaoSenhaRegistro.usuario_id == self.usuario_id.valor
                )
            )
        self.assertIsNotNone(token_persistido)
        assert token_persistido is not None
        self.assertEqual(token_persistido.token_hash, self.gerador.resumir(token))
        self.assertNotEqual(token_persistido.token_hash, token)

        redefinicao = await solicitar_asgi(
            self.app,
            "POST",
            "/recuperacoes-senha/confirmacao",
            dados={"token": token, "senha": self.senha_nova},
        )
        self.assertEqual(redefinicao.status, 204)
        self.assertEqual(redefinicao.corpo, b"")
        self.assertFalse(redefinicao.cabecalhos("set-cookie"))

        async with self.sessoes() as sessao:
            usuario = await sessao.get(UsuarioRegistro, self.usuario_id.valor)
            token_usado = await sessao.scalar(
                select(TokenRecuperacaoSenhaRegistro).where(
                    TokenRecuperacaoSenhaRegistro.token_hash
                    == self.gerador.resumir(token)
                )
            )
            sessoes = (
                await sessao.scalars(
                    select(SessaoRegistro).where(
                        SessaoRegistro.usuario_id == self.usuario_id.valor
                    )
                )
            ).all()
        assert usuario is not None and token_usado is not None
        self.assertTrue(self.derivador.confere(self.senha_nova, usuario.hash_senha))
        self.assertFalse(self.derivador.confere(self.senha_antiga, usuario.hash_senha))
        self.assertIsNotNone(token_usado.usada_em)
        self.assertEqual(len(sessoes), 2)
        self.assertTrue(all(sessao.revogada_em is not None for sessao in sessoes))

        repeticao = await solicitar_asgi(
            self.app,
            "POST",
            "/recuperacoes-senha/confirmacao",
            dados={"token": token, "senha": "Senha-Terceira-789"},
        )
        self.assertEqual(repeticao.status, 400)
        self.assertFalse(self.derivador.confere("Senha-Terceira-789", usuario.hash_senha))

    async def test_conta_ausente_tem_mesma_resposta_sem_criar_token_ou_email(self) -> None:
        """Evita enumeração e não cria persistência para endereço desconhecido."""
        resposta = await solicitar_asgi(
            self.app,
            "POST",
            "/recuperacoes-senha",
            dados={"email": "inexistente@example.test"},
        )

        self.assertEqual(resposta.status, 202)
        self.assertEqual(
            resposta.json(),
            {"mensagem": "Se houver uma conta associada, enviaremos instruções."},
        )
        self.assertEqual(self.mailbox.envios, [])
        async with self.sessoes() as sessao:
            quantidade = await sessao.scalar(
                select(TokenRecuperacaoSenhaRegistro.id).where(
                    TokenRecuperacaoSenhaRegistro.usuario_id == self.usuario_id.valor
                )
            )
        self.assertIsNone(quantidade)

    async def test_token_expirado_e_recusado_sem_alterar_credencial(self) -> None:
        """Recusa token vencido e mantém a credencial original persistida."""
        token = self.gerador.gerar().token
        instante = self.relogio.agora()
        async with self.sessoes.begin() as sessao:
            sessao.add(
                TokenRecuperacaoSenhaRegistro(
                    id=uuid4(),
                    usuario_id=self.usuario_id.valor,
                    token_hash=self.gerador.resumir(token),
                    criada_em=instante - timedelta(hours=1),
                    expira_em=instante - timedelta(seconds=1),
                    usada_em=None,
                )
            )

        resposta = await solicitar_asgi(
            self.app,
            "POST",
            "/recuperacoes-senha/confirmacao",
            dados={"token": token, "senha": self.senha_nova},
        )

        self.assertEqual(resposta.status, 400)
        async with self.sessoes() as sessao:
            usuario = await sessao.get(UsuarioRegistro, self.usuario_id.valor)
        assert usuario is not None
        self.assertTrue(self.derivador.confere(self.senha_antiga, usuario.hash_senha))
