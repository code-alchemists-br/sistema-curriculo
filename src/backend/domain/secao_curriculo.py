"""Define as seções suportadas pelo currículo e a ordem padrão de apresentação.

O módulo reúne a enumeração fechada de seções e a sequência em que elas aparecem
quando o estudante não definiu outra ordem, sem conhecer banco, rotas ou formatos
de saída. Ele existe para manter em um único ponto do domínio o vocabulário de
seções que consultas, persistência e exportação compartilham.
"""

from enum import Enum


# Proveniência: decision-analysis prompts/backend/20261017-100000-secoes-curriculo-ordem-padrao-v001.md#v001
class SecaoCurriculo(str, Enum):
    """Identifica cada seção que um currículo pode apresentar.

    Os valores textuais são identificadores estáveis, no mesmo formato já usado
    pela revisão e pelo front-end, e cobrem os dados pessoais e os tipos de item
    que o currículo consegue referenciar. A enumeração existe para que a seção
    seja um vocabulário fechado, reconhecido em qualquer camada sem interpretar
    texto livre.
    """

    DADOS_PESSOAIS = "dados-pessoais"
    FORMACAO_ACADEMICA = "formacao-academica"
    EXPERIENCIAS_PROFISSIONAIS = "experiencias-profissionais"
    PROJETOS_ACADEMICOS = "projetos-academicos"
    COMPETENCIAS = "competencias"
    IDIOMAS = "idiomas"
    DOCUMENTOS_COMPLEMENTARES = "documentos-complementares"


# Proveniência: decision-analysis prompts/backend/20261017-100000-secoes-curriculo-ordem-padrao-v001.md#v001
# Ordem em que as seções aparecem enquanto não houver ordem definida pelo estudante.
# É uma tupla explícita, e não a ordem de declaração do Enum, para que reordenar
# a apresentação seja uma decisão visível e não um efeito colateral.
ORDEM_PADRAO_SECOES: tuple[SecaoCurriculo, ...] = (
    SecaoCurriculo.DADOS_PESSOAIS,
    SecaoCurriculo.FORMACAO_ACADEMICA,
    SecaoCurriculo.EXPERIENCIAS_PROFISSIONAIS,
    SecaoCurriculo.PROJETOS_ACADEMICOS,
    SecaoCurriculo.COMPETENCIAS,
    SecaoCurriculo.IDIOMAS,
    SecaoCurriculo.DOCUMENTOS_COMPLEMENTARES,
)
