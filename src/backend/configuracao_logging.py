"""Configura o nível de logging da aplicação a partir do ambiente."""

import logging
import os

NIVEIS_LOG_PERMITIDOS = frozenset(
    {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
)
NIVEL_LOG_PADRAO = "INFO"


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
    logging.getLogger().setLevel(logging.getLevelName(nivel))
