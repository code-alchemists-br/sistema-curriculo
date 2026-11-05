"""Define a orientação determinística de modelo de currículo por objetivo.

O módulo representa o objetivo declarado pelo estudante e aplica a tabela
documentada para recomendar uma apresentação inicial. Ele existe para orientar
a escolha de layout de modo explicável, sem inferir perfil, alterar a versão ou
envolver um provedor de inteligência artificial.
"""

from dataclasses import dataclass
from enum import Enum

from backend.domain.modelo_curriculo import ModeloCurriculo

# Proveniência: decision-analysis prompts/backend/20261102-235645-adequacao-semantica-gpt-nano-v003.md#v003


class ObjetivoCurriculo(str, Enum):
    """Enumera os objetivos que orientam uma recomendação inicial de modelo.

    A enumeração fecha o vocabulário recebido pela orquestração e corresponde
    às categorias documentadas de uso do currículo. Ela existe para evitar
    heurísticas implícitas sobre o perfil e manter a recomendação reproduzível.
    """

    PRIMEIRO_EMPREGO = "primeiro_emprego"
    TECNOLOGIA = "tecnologia"
    ADMINISTRATIVO_CORPORATIVO = "administrativo_corporativo"
    CRIATIVO_DESIGN = "criativo_design"
    ACADEMICO_PESQUISADOR = "academico_pesquisador"
    OUTRO = "outro"


@dataclass(frozen=True, slots=True)
class RecomendacaoModeloCurriculo:
    """Representa a recomendação explicável e não vinculante de apresentação.

    O value object reúne o modelo inicial e sua justificativa textual, sem
    referência a uma versão persistida ou comando de alteração. Ele existe para
    que o estudante receba orientação clara e continue livre para escolher
    qualquer modelo disponível.
    """

    modelo_recomendado: ModeloCurriculo
    justificativa: str

    def __post_init__(self) -> None:
        """Valida o modelo tipado e a explicação legível da recomendação.

        O método exige enumeração reconhecida e texto significativo após aparar
        espaços, preservando a imutabilidade do resultado. Ele existe para que
        uma orientação de apresentação nunca seja opaca ou baseada em valores
        soltos fora do vocabulário do domínio.
        """
        if not isinstance(self.modelo_recomendado, ModeloCurriculo):
            raise ValueError("O modelo recomendado deve ser reconhecido.")
        if not isinstance(self.justificativa, str) or not self.justificativa.strip():
            raise ValueError("A justificativa da recomendação deve ser informada.")


class PoliticaRecomendacaoModeloCurriculo:
    """Aplica a tabela documental que relaciona objetivo a modelo inicial.

    A política seleciona um único modelo e uma justificativa predeterminada
    para cada objetivo, sem consultar itens ou serviços externos. Ela existe
    para manter a apresentação explicável e separar esta decisão local da
    adequação textual feita por IA para uma vaga.
    """

    def recomendar(self, objetivo: ObjetivoCurriculo) -> RecomendacaoModeloCurriculo:
        """Devolve a orientação inicial associada ao objetivo declarado.

        O método consulta um mapa fechado de resultados e cria o value object
        tipado correspondente, rejeitando valores fora da enumeração. Ele existe
        para reproduzir de forma determinística a tabela de modelos do produto.
        """
        if not isinstance(objetivo, ObjetivoCurriculo):
            raise ValueError("O objetivo do currículo deve ser reconhecido.")
        modelo, justificativa = _RECOMENDACOES_POR_OBJETIVO[objetivo]
        return RecomendacaoModeloCurriculo(
            modelo_recomendado=modelo, justificativa=justificativa
        )


_RECOMENDACOES_POR_OBJETIVO: dict[ObjetivoCurriculo, tuple[ModeloCurriculo, str]] = {
    ObjetivoCurriculo.PRIMEIRO_EMPREGO: (
        ModeloCurriculo.PRIMEIRO_EMPREGO,
        "O modelo Primeiro emprego evidencia formação, projetos e competências antes da experiência profissional.",
    ),
    ObjetivoCurriculo.TECNOLOGIA: (
        ModeloCurriculo.MODERNO,
        "O modelo Moderno equilibra o destaque para competências, projetos e experiência em tecnologia.",
    ),
    ObjetivoCurriculo.ADMINISTRATIVO_CORPORATIVO: (
        ModeloCurriculo.ATS_SIMPLES,
        "O modelo ATS simples prioriza leitura direta para candidaturas administrativas ou corporativas; o Profissional clássico continua como alternativa.",
    ),
    ObjetivoCurriculo.CRIATIVO_DESIGN: (
        ModeloCurriculo.CRIATIVO,
        "O modelo Criativo dá maior destaque à identidade profissional e aos projetos de design.",
    ),
    ObjetivoCurriculo.ACADEMICO_PESQUISADOR: (
        ModeloCurriculo.ACADEMICO,
        "O modelo Acadêmico valoriza formação, pesquisa e produção científica.",
    ),
    ObjetivoCurriculo.OUTRO: (
        ModeloCurriculo.MODERNO,
        "O modelo Moderno oferece uma apresentação inicial equilibrada para objetivos diversos.",
    ),
}
