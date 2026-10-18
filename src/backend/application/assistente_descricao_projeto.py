"""Define o contrato do assistente de descrição de projeto.

O módulo concentra entrada, saída, falhas e a abstração do assistente sem
depender de API, infraestrutura ou inteligência artificial. Ele existe para
permitir implementações substituíveis e um comportamento controlado quando
nenhuma estratégia estiver disponível.
"""

from dataclasses import dataclass
from typing import Protocol


# Proveniência: decision-analysis prompts/backend/20261018-133100-contrato-assistente-descricao-projeto-v001.md#v001
@dataclass(frozen=True, slots=True)
class AssistenteDescricaoProjetoEntrada:
    """Agrupa os dados usados para solicitar uma sugestão de descrição.

    A entrada utiliza informações já pertencentes ao projeto acadêmico e não
    conhece detalhes de interface ou infraestrutura. Ela existe para tornar
    explícito o contrato de entrada do assistente.
    """

    titulo: str
    tecnologias: str


@dataclass(frozen=True, slots=True)
class AssistenteDescricaoProjetoSaida:
    """Representa a sugestão textual produzida pelo assistente.

    A saída contém somente a descrição sugerida, sem expor a estratégia usada
    para produzi-la. Ela existe para manter o consumidor independente da
    implementação concreta.
    """

    descricao: str


class AssistenteDescricaoProjetoIndisponivel(RuntimeError):
    """Sinaliza que o assistente não está disponível para produzir a sugestão.

    A exceção representa uma falha controlada do contrato e evita que
    consumidores dependam de erros específicos de uma implementação externa.
    Ela existe para permitir tratamento previsível da indisponibilidade.
    """


class AssistenteDescricaoProjeto(Protocol):
    """Define a capacidade de sugerir uma descrição para um projeto acadêmico.

    A porta recebe uma entrada tipada e devolve uma saída tipada, sem conhecer
    inteligência artificial, API ou provedor concreto. Ela existe para permitir
    diferentes estratégias de geração sem alterar seus consumidores.
    """

    async def sugerir_descricao(
        self,
        entrada: AssistenteDescricaoProjetoEntrada,
    ) -> AssistenteDescricaoProjetoSaida:
        """Solicita uma sugestão de descrição para o projeto informado.

        A operação delega a geração do texto para a implementação concreta e
        devolve somente o contrato de saída. Ela existe para separar a intenção
        da aplicação da estratégia utilizada.
        """


class AssistenteDescricaoProjetoAusente:
    """Representa explicitamente a ausência de uma implementação configurada.

    A classe preserva o mesmo contrato do assistente, mas responde de forma
    controlada com a exceção de indisponibilidade. Ela existe para tornar
    verificável o cenário em que nenhuma estratégia está habilitada.
    """

    async def sugerir_descricao(
        self,
        entrada: AssistenteDescricaoProjetoEntrada,
    ) -> AssistenteDescricaoProjetoSaida:
        """Informa que nenhuma implementação do assistente está disponível.

        O método não tenta gerar conteúdo e levanta a exceção específica do
        contrato. Ele existe para evitar comportamento silencioso ou erro
        genérico quando o assistente estiver ausente.
        """
        raise AssistenteDescricaoProjetoIndisponivel(
            "Assistente de descrição de projeto não está disponível."
        )
