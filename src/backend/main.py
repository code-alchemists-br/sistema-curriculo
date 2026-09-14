"""Expõe a aplicação ASGI que um servidor poderá importar futuramente."""

from backend.api.factory import create_app


# Proveniência: decision-analysis prompts/backend/20260913-fundamentos-fastapi-v001.md#v001
app = create_app()
