"""Expõe uma aplicação ASGI protegida enquanto adapters de produção não existem.

A composição atual não fornece persistência de sessões, então instala um
autenticador fechado que rejeita todas as credenciais nas rotas privadas. Ela
existe para que importar a aplicação não desative acidentalmente a autenticação.
"""

from backend.api.factory import create_app
from backend.infrastructure.security.autenticador_sessao_indisponivel import (
    AutenticadorSessaoIndisponivel,
)

# Proveniência: decision-analysis prompts/backend/20260913-fundamentos-fastapi-v001.md#v001
app = create_app(autenticador_sessao=AutenticadorSessaoIndisponivel())
