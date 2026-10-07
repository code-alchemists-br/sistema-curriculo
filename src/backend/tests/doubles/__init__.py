"""Agrupa doubles e simuladores de testes para integração com serviços externos.

O pacote disponibiliza implementações substitutas que reproduzem contratos e
comportamentos assíncronos de clientes de rede e APIs parceiras. Ele existe para
tornar as suítes de testes rápidas, determinísticas e resilientes, sem depender
de conectividade real ou disponibilidade de terceiros.
"""

# Proveniência: decision-analysis prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md#v001
from backend.tests.doubles.api_vagas_grupo2 import (
    ApiVagasIndisponivel,
    ClienteApiVagasGrupo2,
    DoubleApiVagasGrupo2,
    ErroIntegracaoApiVagas,
    ModoDoubleApiVagas,
    RespostaInvalidaApiVagas,
    VagaExternaDto,
)

__all__ = [
    "ApiVagasIndisponivel",
    "ClienteApiVagasGrupo2",
    "DoubleApiVagasGrupo2",
    "ErroIntegracaoApiVagas",
    "ModoDoubleApiVagas",
    "RespostaInvalidaApiVagas",
    "VagaExternaDto",
]
