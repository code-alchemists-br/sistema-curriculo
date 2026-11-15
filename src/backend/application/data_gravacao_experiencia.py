"""Obtém o dia civil da gravação por relógio injetado para isolar tempo externo.

Converte um único instante ao fuso do produto e entrega date ao domínio para
que a política de datas permaneça pura e independente do fuso do sistema.
"""

# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
from datetime import date
from zoneinfo import ZoneInfo

from backend.application.ports import Relogio


def obter_hoje_experiencia(relogio: Relogio) -> date:
    """Lê uma vez o relógio e devolve a data civil em America/Sao_Paulo.

    Exige instante com fuso para evitar conversão implícita pelo fuso do SO e
    converte antes de extrair date, permitindo validação determinística de
    gravações mesmo perto da meia-noite ou após mudança de dia sem reinício.
    """
    agora = relogio.agora()
    if agora.tzinfo is None or agora.utcoffset() is None:
        raise ValueError("O relógio deve fornecer um instante com fuso horário.")
    return agora.astimezone(ZoneInfo("America/Sao_Paulo")).date()
