"""Verifica a fundação FastAPI sem iniciar um servidor ou recurso externo."""

import unittest

from fastapi import FastAPI

from backend.api.factory import create_app
from backend.main import app


# Proveniência: decision-analysis prompts/backend/20260913-fundamentos-fastapi-v001.md#v001
class FastApiFoundationTestCase(unittest.TestCase):
    """Agrupa verificações unitárias da criação e exposição da aplicação.

    A classe exercita somente a fábrica e o ponto de entrada em memória, sem
    iniciar Uvicorn ou atravessar fronteiras externas. Ela existe para proteger
    a composição mínima que outros componentes poderão ampliar futuramente.
    """

    def test_factory_and_asgi_entry_expose_fastapi_instances(self) -> None:
        """Confirma que fábrica e entrada ASGI disponibilizam aplicações FastAPI.

        O teste cria uma aplicação pela fábrica e inspeciona a instância exposta
        pelo módulo de entrada sem executar servidor ou acessar recursos
        externos. Ele garante que a fundação permanece importável para compor
        adapters futuros com segurança.
        """
        self.assertIsInstance(create_app(), FastAPI)
        self.assertIsInstance(app, FastAPI)
