"""Entrega links temporários de redefinição por SMTP configurado no ambiente."""

import asyncio
import logging
import os
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage
from urllib.parse import urlsplit

from backend.domain.value_objects import Email

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ConfiguracaoSmtpRecuperacao:
    """Agrupa os dados necessários para enviar mensagens de recuperação.

    A configuração guarda somente host, remetente, destino do link e credenciais
    do provedor. Ela existe para impedir valores de e-mail hardcoded no adapter.
    """

    host: str
    porta: int
    remetente: str
    url_redefinicao: str
    usuario: str | None = None
    senha: str | None = None

    @classmethod
    def do_ambiente(cls) -> "ConfiguracaoSmtpRecuperacao | None":
        """Lê configuração SMTP completa ou informa que o serviço está ausente.

        A função exige host, remetente e URL da tela de redefinição, valida a
        porta e exige usuário e senha em conjunto. Ela existe para deixar a
        recuperação indisponível explicitamente quando o ambiente não tem
        entrega de e-mail configurada.
        """
        host = os.environ.get("PASSWORD_RESET_SMTP_HOST")
        remetente = os.environ.get("PASSWORD_RESET_FROM_EMAIL")
        url = os.environ.get("PASSWORD_RESET_URL")
        if not host or not remetente or not url:
            return None
        destino = urlsplit(url.replace("{token}", "token-de-validacao"))
        if destino.scheme != "https" or not destino.netloc or "{token}" not in url:
            raise ValueError(
                "PASSWORD_RESET_URL deve ser HTTPS e conter o marcador {token}."
            )
        usuario = os.environ.get("PASSWORD_RESET_SMTP_USERNAME") or None
        senha = os.environ.get("PASSWORD_RESET_SMTP_PASSWORD") or None
        if bool(usuario) != bool(senha):
            raise ValueError("Credenciais SMTP devem ser configuradas em conjunto.")
        porta = int(os.environ.get("PASSWORD_RESET_SMTP_PORT", "465"))
        if not 1 <= porta <= 65535:
            raise ValueError("Porta SMTP de recuperação fora do intervalo permitido.")
        return cls(host, porta, remetente, url, usuario, senha)


class EnviadorRecuperacaoSmtp:
    """Envia mensagem SMTP com link de redefinição sem registrar o token.

    Usa SMTP sobre TLS em thread para não bloquear o event loop e compõe a URL
    a partir da base configurada. A classe existe para entregar a recuperação
    fora das camadas de API e domínio.
    """

    def __init__(self, configuracao: ConfiguracaoSmtpRecuperacao) -> None:
        """Recebe configuração validada sem abrir conexão com o provedor.

        O construtor apenas guarda parâmetros da integração. Ele existe para
        que cada envio crie e encerre sua conexão de forma independente.
        """
        self._configuracao = configuracao

    async def enviar(self, email: Email, token: str) -> None:
        """Entrega instruções de redefinição ao endereço da conta.

        O método transfere a comunicação SMTP para uma thread e nunca devolve
        conteúdo da mensagem ao chamador. Ele existe para manter I/O bloqueante
        fora do loop assíncrono da API.
        """
        try:
            await asyncio.to_thread(self._enviar_sincrono, email.valor, token)
        except Exception:
            logger.warning("falha_envio_email operacao=recuperacao_senha")

    def _enviar_sincrono(self, destinatario: str, token: str) -> None:
        """Monta e envia a mensagem sobre SMTP com TLS e timeout limitado.

        A função insere o token apenas no link enviado ao destinatário e usa
        contexto TLS padrão com timeout de dez segundos. Ela existe para
        encapsular o transporte síncrono da biblioteca padrão.
        """
        configuracao = self._configuracao
        link = configuracao.url_redefinicao.format(token=token)
        mensagem = EmailMessage()
        mensagem["Subject"] = "Redefinição de senha"
        mensagem["From"] = configuracao.remetente
        mensagem["To"] = destinatario
        mensagem.set_content(
            "Recebemos uma solicitação para redefinir sua senha.\n\n"
            f"Acesse este link em até 15 minutos: {link}\n\n"
            "Se você não solicitou a redefinição, ignore esta mensagem."
        )
        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            configuracao.host,
            configuracao.porta,
            timeout=10,
            context=contexto,
        ) as servidor:
            if configuracao.usuario is not None and configuracao.senha is not None:
                servidor.login(configuracao.usuario, configuracao.senha)
            servidor.send_message(mensagem)
