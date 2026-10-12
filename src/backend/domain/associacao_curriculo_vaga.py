"""Define o agregado mínimo de associação entre currículo e vaga.

O agregado protege as classificações aceitas e normaliza candidatura para
incluir interesse tanto na construção quanto na inclusão posterior. Ele existe
para manter essa invariante de domínio em um único ponto, independente de
persistência, aplicação e transporte.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.value_objects import CurriculoId, VagaId


# Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
class ClassificacaoAssociacao(str, Enum):
    """Representa uma das classificações reconhecidas para a associação.

    Os valores identificam interesse, compatibilidade ou candidatura, sem
    acrescentar estados ou regras de cálculo. A enum existe para restringir o
    vocabulário do agregado aos valores definidos nos requisitos.
    """

    INTERESSE = "interesse"
    COMPATIBILIDADE = "compatibilidade"
    CANDIDATURA = "candidatura"


# Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
@dataclass(slots=True, init=False)
class AssociacaoCurriculoVaga:
    """Representa a associação de uma versão de currículo com uma vaga.

    O agregado armazena os dois identificadores tipados e protege um conjunto
    não vazio de classificações; construção e inclusão de candidatura acrescentam
    interesse automaticamente. Ele existe para garantir a regra compartilhável
    entre futuras operações de criação e atualização.
    """

    curriculo_id: CurriculoId
    vaga_id: VagaId
    _classificacoes: set[ClassificacaoAssociacao] = field(repr=False)

    def __init__(
        self,
        curriculo_id: CurriculoId,
        vaga_id: VagaId,
        classificacoes: Iterable[ClassificacaoAssociacao],
    ) -> None:
        """Cria uma associação válida e normaliza candidaturas informadas.

        O método valida que exista ao menos uma classificação reconhecida,
        copia a entrada para um conjunto próprio e inclui interesse se houver
        candidatura. Ele existe para que o agregado nunca seja construído com
        candidatura desacompanhada da classificação exigida.
        """
        self.curriculo_id = curriculo_id
        self.vaga_id = vaga_id
        classificacoes_normalizadas: set[ClassificacaoAssociacao] = set()
        for classificacao in classificacoes:
            if not isinstance(classificacao, ClassificacaoAssociacao):
                raise RegraDeDominioViolada(
                    "Associação currículo-vaga recebeu classificação não reconhecida."
                )
            classificacoes_normalizadas.add(classificacao)

        if not classificacoes_normalizadas:
            raise RegraDeDominioViolada(
                "Associação currículo-vaga deve possuir ao menos uma classificação."
            )
        if ClassificacaoAssociacao.CANDIDATURA in classificacoes_normalizadas:
            classificacoes_normalizadas.add(ClassificacaoAssociacao.INTERESSE)

        self._classificacoes = classificacoes_normalizadas

    @property
    def classificacoes(self) -> frozenset[ClassificacaoAssociacao]:
        """Expõe classificações por uma visão imutável do estado interno.

        A propriedade copia o conjunto protegido para um ``frozenset`` e não
        oferece operação de remoção. Ela existe para permitir leitura sem
        contornar a invariante candidatura implica interesse.
        """
        return frozenset(self._classificacoes)

    def adicionar_classificacao(self, classificacao: ClassificacaoAssociacao) -> None:
        """Adiciona uma classificação preservando as regras do agregado.

        A operação rejeita valores fora do enum, usa um conjunto para evitar
        duplicatas e inclui interesse junto com candidatura. Ela existe para
        manter a associação válida em cada inclusão suportada, sem decidir
        regras de remoção que pertencem a uma entrega posterior.
        """
        if not isinstance(classificacao, ClassificacaoAssociacao):
            raise RegraDeDominioViolada(
                "Associação currículo-vaga recebeu classificação não reconhecida."
            )

        self._classificacoes.add(classificacao)
        if classificacao is ClassificacaoAssociacao.CANDIDATURA:
            self._classificacoes.add(ClassificacaoAssociacao.INTERESSE)
