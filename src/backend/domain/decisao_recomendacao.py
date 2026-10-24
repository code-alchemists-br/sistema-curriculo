"""Define a decisão do estudante sobre uma recomendação da revisão do currículo.

O módulo reúne a enumeração das decisões possíveis e o value object que associa
uma decisão a uma versão de currículo e a um código de recomendação, com o
instante técnico em que foi tomada. Ele existe para manter no domínio o que o
estudante decidiu, sem conhecer banco, rotas ou formatos de saída.
"""

import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.value_objects import CurriculoId

_PADRAO_CODIGO = re.compile(r"[A-Z][A-Z0-9_]*")


# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
class DecisaoEstudante(str, Enum):
    """Identifica o que o estudante decidiu fazer com uma recomendação.

    Os valores textuais são identificadores estáveis, gravados e expostos. A
    enumeração existe para que a decisão seja um vocabulário fechado: o estudante
    aceita ou rejeita a recomendação, sem outros estados.
    """

    ACEITA = "aceita"
    REJEITADA = "rejeitada"


# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
@dataclass(frozen=True, slots=True)
class DecisaoRecomendacao:
    """Registra a decisão do estudante sobre uma recomendação de uma versão.

    O value object guarda a versão do currículo, o código da recomendação (por
    exemplo, ``PROJETO_AUSENTE``), a decisão e o instante técnico em que ela foi
    tomada, sempre com fuso. Ele existe para que a escolha do estudante seja um
    dado válido desde a criação e possa ser persistida e consultada.
    """

    curriculo_id: CurriculoId
    codigo: str
    decisao: DecisaoEstudante
    decidida_em: datetime

    def __post_init__(self) -> None:
        """Valida a versão, o código, a decisão e o instante da decisão.

        A validação exige identidade de currículo tipada, código em maiúsculas
        com sublinhados, uma decisão da enumeração e um instante com fuso
        horário. Ela existe para impedir que uma decisão incompleta ou ambígua
        chegue à persistência.
        """
        if not isinstance(self.curriculo_id, CurriculoId):
            raise RegraDeDominioViolada("A decisão exige a identidade da versão.")
        if not isinstance(self.codigo, str) or not _PADRAO_CODIGO.fullmatch(self.codigo):
            raise RegraDeDominioViolada(
                "O código da recomendação deve usar letras maiúsculas, números e sublinhados."
            )
        if not isinstance(self.decisao, DecisaoEstudante):
            raise RegraDeDominioViolada("A decisão deve ser aceita ou rejeitada.")
        if not isinstance(self.decidida_em, datetime) or self.decidida_em.tzinfo is None:
            raise RegraDeDominioViolada(
                "O instante da decisão deve ser uma data e hora com fuso horário."
            )
