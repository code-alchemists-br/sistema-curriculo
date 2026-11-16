"""Define a proposta revisável de modelo de currículo.

O módulo representa somente o resultado validado que um gerador pode propor,
sem decidir como ele foi obtido ou alterar a versão do currículo. Ele existe
para manter a escolha de apresentação tipada e subordinada ao estudante.
"""

from dataclasses import dataclass

from backend.domain.modelo_curriculo import ModeloCurriculo

# Proveniência: decision-analysis prompts/backend/20261105-181751-adequacao-semantica-gpt-nano-v005.md#v005


@dataclass(frozen=True, slots=True)
class RecomendacaoModeloCurriculo:
    """Representa a recomendação explicável e não vinculante de apresentação.

    O value object reúne um modelo permitido e sua justificativa, sem referência
    a uma versão persistida ou comando de alteração. Ele existe para que uma
    sugestão externa só alcance o estudante em forma validável e revisável.
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
            raise ValueError(
                "O modelo recomendado deve pertencer ao catálogo reconhecido."
            )
        if not isinstance(self.justificativa, str) or not self.justificativa.strip():
            raise ValueError("A justificativa da recomendação deve ser informada.")
