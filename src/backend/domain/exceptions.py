"""Define falhas de regra de negócio do núcleo de domínio.

As exceções deste módulo descrevem estados que não podem existir no modelo. A
separação permite que as camadas externas traduzam a falha sem introduzir tipos
de framework nas entidades e nos value objects.
"""


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
class RegraDeDominioViolada(ValueError):
    """Sinaliza que uma construção ou transição violou uma invariante de domínio.

    A classe especializa ``ValueError`` para representar falhas de dados ou
    estado detectadas pelo próprio modelo, sem conhecer transporte ou
    persistência. Ela existe para tornar essas violações distinguíveis nas
    camadas que futuramente as orquestrarão.
    """


# Proveniência: decision-analysis prompts/backend/20261017-120000-propriedade-referencia-curriculo-v001.md#v001
class ReferenciaDeOutroProprietario(RegraDeDominioViolada):
    """Sinaliza que um item selecionado pertence a outro estudante.

    A classe especializa ``RegraDeDominioViolada`` para distinguir a recusa por
    propriedade das demais violações de composição, como a duplicidade. Ela
    existe para que quem orquestra a seleção traduza esse caso específico sem
    inspecionar a mensagem da falha.
    """
