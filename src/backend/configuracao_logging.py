"""Configura o nível de logging da aplicação a partir do ambiente."""

import logging
import os
import re
from collections.abc import Mapping
from typing import Any

NIVEIS_LOG_PERMITIDOS = frozenset(
    {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
)
NIVEL_LOG_PADRAO = "INFO"
_PADROES_DADOS_PESSOAIS = (
    re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])"),
    re.compile(r"(?<!\d)\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)"),
    re.compile(r"(?<![A-Za-z0-9])\d{11}(?![A-Za-z0-9])"),
    re.compile(
        r"(?<![A-Za-z0-9])(?:\+?55\s?)?\(?\d{2}\)?\s?"
        r"\d{4,5}[- ]?\d{4}(?![A-Za-z0-9])"
    ),
)
_PADRAO_CAMPO_SENSIVEL = re.compile(
    r"(?i)\b((?:ator_id|authorization|cookie|cpf|email|endereco|nome|"
    r"password|senha|set_cookie|telefone|token)\s*=\s*)[^\s,;]+"
)
_PADRAO_AUTORIZACAO = re.compile(r"(?i)\b(authorization\s*=\s*)[^,;]+")
_CHAVES_SENSIVEIS = frozenset(
    {
        "ator_id",
        "authorization",
        "cookie",
        "cpf",
        "email",
        "endereco",
        "nome",
        "password",
        "senha",
        "set-cookie",
        "set_cookie",
        "telefone",
        "token",
    }
)
_MASCARA = "[REDACTED]"
_CAMPOS_LOG_PADRAO = frozenset(logging.makeLogRecord({}).__dict__)


class FiltroMascaramentoDadosPessoais(logging.Filter):
    """Remove identificadores pessoais e credenciais dos registros de log.

    O filtro mascara padrões conhecidos em mensagens e argumentos, além de
    substituir valores de campos estruturados com nomes sensíveis. Ele existe
    para reduzir a exposição de dados pessoais e segredos nos destinos de log.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Sanitiza a mensagem e campos extras antes da emissão do registro.

        O método mascara texto formatado, argumentos e atributos extras do
        `LogRecord`, preservando a estrutura do evento. Ele existe para aplicar
        uma proteção uniforme a todos os handlers configurados no backend.
        """
        record.msg = _mascarar_valor(record.getMessage())
        record.args = ()
        for chave, valor in tuple(record.__dict__.items()):
            if chave in _CAMPOS_LOG_PADRAO:
                continue
            if chave.lower() in _CHAVES_SENSIVEIS:
                record.__dict__[chave] = _MASCARA
            else:
                record.__dict__[chave] = _mascarar_valor(valor)
        if record.exc_info:
            record.exc_text = _mascarar_valor(
                logging.Formatter().formatException(record.exc_info)
            )
            record.exc_info = None
        elif record.exc_text:
            record.exc_text = _mascarar_valor(record.exc_text)
        return True


def _mascarar_valor(valor: Any) -> Any:
    """Mascarar padrões pessoais em valores textuais aninhados.

    A função percorre strings, sequências e mapas e substitui e-mails, CPFs,
    telefones e campos com chaves sensíveis; os demais tipos permanecem iguais.
    Ela existe para sanitizar tanto mensagens formatadas quanto dados extras.
    """
    if isinstance(valor, str):
        valor = _PADRAO_AUTORIZACAO.sub(
            lambda correspondencia: f"{correspondencia.group(1)}{_MASCARA}",
            valor,
        )
        valor = _PADRAO_CAMPO_SENSIVEL.sub(
            lambda correspondencia: f"{correspondencia.group(1)}{_MASCARA}",
            valor,
        )
        for padrao in _PADROES_DADOS_PESSOAIS:
            valor = padrao.sub(_MASCARA, valor)
        return valor
    if isinstance(valor, tuple):
        return tuple(_mascarar_valor(item) for item in valor)
    if isinstance(valor, list):
        return [_mascarar_valor(item) for item in valor]
    if isinstance(valor, Mapping):
        return {
            chave: (
                _MASCARA
                if str(chave).lower() in _CHAVES_SENSIVEIS
                else _mascarar_valor(item)
            )
            for chave, item in valor.items()
        }
    return valor


def configurar_logging() -> None:
    """Configura o nível do logger raiz usando a variável `LOG_LEVEL`.

    A função lê o valor do ambiente, normaliza espaços e caixa, valida a lista
    de níveis aceitos e configura o logging padrão do Python. Ela existe para
    permitir ajustar a verbosidade da aplicação por ambiente sem alterar código.
    """
    valor_configurado = os.environ.get("LOG_LEVEL", NIVEL_LOG_PADRAO)
    nivel = valor_configurado.strip().upper()
    if nivel not in NIVEIS_LOG_PERMITIDOS:
        niveis = ", ".join(sorted(NIVEIS_LOG_PERMITIDOS))
        raise ValueError(
            f"LOG_LEVEL inválido: {valor_configurado!r}. "
            f"Valores permitidos: {niveis}."
        )

    logging.basicConfig(level=logging.getLevelName(nivel))
    logger_raiz = logging.getLogger()
    logger_raiz.setLevel(logging.getLevelName(nivel))
    for handler in logger_raiz.handlers:
        if not any(
            isinstance(filtro, FiltroMascaramentoDadosPessoais)
            for filtro in handler.filters
        ):
            handler.addFilter(FiltroMascaramentoDadosPessoais())
