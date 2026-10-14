"""Implementa a geração de identidades de domínio com UUID versão 4.

O adapter encapsula a fonte de aleatoriedade e devolve value objects já tipados,
sem expor o gerador de UUID às camadas internas. Ele existe para atender a porta
de identidade com uma estratégia concreta e substituível.
"""

from uuid import uuid4

from backend.application.ports import GeradorCompetenciaId, GeradorCurriculoId
from backend.domain.value_objects import CompetenciaId, CurriculoId

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


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class GeradorCompetenciaIdUuid4(GeradorCompetenciaId):
    """Gera identidades de competência com UUID versão 4.

    A implementação cria um UUID aleatório e o encapsula no value object de
    competência. Ela existe para satisfazer a porta da Application sem expor a
    biblioteca de geração de identidade às camadas internas.
    """

    def gerar(self) -> CompetenciaId:
        """Devolve uma identidade nova e tipada para competência.

        O método delega a aleatoriedade ao UUID4 e converte seu resultado para
        ``CompetenciaId``. Ele existe para oferecer ao caso de uso uma origem
        concreta, substituível e sem estado de identificadores.
        """
        return CompetenciaId(uuid4())
