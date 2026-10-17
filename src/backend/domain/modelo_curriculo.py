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

    Os valores textuais são identificadores estáveis, iguais aos que o
    front-end já oferece ao estudante (clássico e compacto). A enumeração existe
    para que o modelo seja um vocabulário fechado, reconhecido em qualquer
    camada, e para que um modelo desconhecido possa ser recusado sem interpretar
    texto livre.
    """

    CLASSICO = "classico"
    COMPACTO = "compacto"
