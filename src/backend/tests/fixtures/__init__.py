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
# Proveniência: decision-analysis prompts/backend/20261009-160234-dados-reutilizaveis-perfis-testes-integracao-e2e-v003.md#v003
from backend.tests.fixtures.perfis_integracao import (
    PerfilIntegracaoFake,
    ler_perfis_fake,
    popular_perfis_fake,
)

__all__ = [
    "CurriculoExportacaoFixture",
    "PerfilIntegracaoFake",
    "obter_curriculo_exportacao_fixture",
    "ler_perfis_fake",
    "popular_perfis_fake",
]
