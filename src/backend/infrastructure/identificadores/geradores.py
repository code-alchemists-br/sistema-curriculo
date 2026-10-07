"""Implementa a geração de identidades de domínio com UUID versão 4.

O adapter encapsula a fonte de aleatoriedade e devolve value objects já tipados,
sem expor o gerador de UUID às camadas internas. Ele existe para atender a porta
de identidade de currículo com uma estratégia concreta e substituível.
"""

from uuid import uuid4

from backend.application.ports import GeradorCurriculoId
from backend.domain.value_objects import CurriculoId

# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001


class GeradorCurriculoIdUuid4(GeradorCurriculoId):
    """Gera identidades de versão de currículo a partir de UUID versão 4.

    A implementação cria um UUID aleatório a cada chamada e o embrulha em um
    ``CurriculoId``. Ela existe para que a criação de versões receba identidades
    únicas sem que a Application conheça a biblioteca ou a estratégia de geração.
    """

    def gerar(self) -> CurriculoId:
        """Gera um ``CurriculoId`` novo e aleatório.

        O método chama o gerador de UUID versão 4 e devolve o value object do
        domínio, sem manter estado entre chamadas. Ele existe para implementar o
        contrato da porta de identidade de currículo.
        """
        return CurriculoId(uuid4())
