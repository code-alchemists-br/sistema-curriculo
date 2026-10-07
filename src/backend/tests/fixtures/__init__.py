"""Define o pacote de fixtures reutilizáveis para testes do backend.

O pacote agrupa dados sintéticos e cenários estáveis compartilhados entre testes
unitários, de integração e de nível superior. Ele existe para evitar duplicação de
preparação de dados e garantir determinismo nas suítes de teste.
"""

# Proveniência: decision-analysis prompts/backend/20261006-215500-fixture-teste-exportacao-curriculo-v001.md#v001
from backend.tests.fixtures.curriculo_exportacao import (
    CurriculoExportacaoFixture,
    obter_curriculo_exportacao_fixture,
)

__all__ = [
    "CurriculoExportacaoFixture",
    "obter_curriculo_exportacao_fixture",
]
