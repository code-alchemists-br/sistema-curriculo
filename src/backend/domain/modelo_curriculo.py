"""Define os modelos de apresentação que uma versão de currículo pode adotar.

O módulo reúne a enumeração fechada dos modelos suportados, sem conhecer banco,
rotas ou formatos de saída. Ele existe para manter em um único ponto do domínio
o vocabulário de modelos que a edição da versão, a API e a exportação
compartilham.
"""

from enum import Enum


# Proveniência: decision-analysis prompts/backend/20261017-140000-modelo-curriculo-edicao-versao-v001.md#v001
class ModeloCurriculo(str, Enum):
    """Identifica cada modelo de apresentação disponível para uma versão.

    - O que faz: Define os identificadores estáveis aceitos para apresentação.
    - Como faz: Centraliza os valores em uma enumeração textual usada pela API e pelo domínio.
    - Qual finalidade atende: Impede que uma versão seja criada ou editada com um modelo que a prévia não conhece.
    """

    CLASSICO = "classico"
    COMPACTO = "compacto"
    ATS_SIMPLES = "ats-simples"
    CRIATIVO = "criativo"
    MODERNO = "moderno"
    ACADEMICO = "academico"
    PRIMEIRO_EMPREGO = "primeiro-emprego"
