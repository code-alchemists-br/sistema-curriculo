"""Constrói a aplicação FastAPI na borda de interface do backend."""

from fastapi import FastAPI


# Proveniência: decision-analysis prompts/backend/20260913-fundamentos-fastapi-v001.md#v001
def create_app() -> FastAPI:
    """Cria a aplicação HTTP vazia para composição posterior.

    A função instancia FastAPI sem registrar rotas, dependências ou recursos
    externos. Ela existe para concentrar, na camada de interface, a composição
    futura de adapters e manter o domínio independente do framework.
    """
    return FastAPI()
