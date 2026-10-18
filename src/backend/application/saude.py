"""Define a porta para verificar a disponibilidade de uma dependência."""

from typing import Protocol


class VerificadorSaude(Protocol):
    """Abstrai uma verificação assíncrona de dependência da aplicação.

    Implementações consultam apenas a disponibilidade e devolvem um booleano,
    sem incluir detalhes da dependência. A porta existe para permitir que a
    API agregue verificações sem depender de banco, rede ou infraestrutura.
    """

    async def verificar(self) -> bool:
        """Indica se a dependência está disponível.

        A implementação retorna `True` quando pode atender operações e `False`
        em caso de indisponibilidade. Ela existe para produzir um estado de
        saúde agregado sem expor informações internas.
        """


class VerificadorPersistencia(VerificadorSaude, Protocol):
    """Identifica o probe de persistência usado para decidir prontidão.

    A interface herda a resposta booleana assíncrona de `VerificadorSaude` e
    especializa seu papel para armazenamento persistente. Ela existe para que
    readiness dependa explicitamente da capacidade de persistir dados.
    """

