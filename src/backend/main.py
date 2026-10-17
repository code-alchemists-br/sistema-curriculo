"""Compõe uma aplicação ASGI segura e configura o logging do backend.

A composição atual não fornece persistência de sessões, então instala um
autenticador fechado que rejeita todas as credenciais nas rotas privadas. Ela
também aplica o nível configurado por `LOG_LEVEL`. Este módulo existe para
compor as dependências de produção e manter autenticação e logging explícitos.
"""

from backend.api.factory import create_app
from backend.configuracao_logging import configurar_logging
from backend.infrastructure.security.autenticador_sessao_indisponivel import (
    AutenticadorSessaoIndisponivel,
)

configurar_logging()

# Proveniência: decision-analysis prompts/backend/20260913-fundamentos-fastapi-v001.md#v001
app = create_app(autenticador_sessao=AutenticadorSessaoIndisponivel())
