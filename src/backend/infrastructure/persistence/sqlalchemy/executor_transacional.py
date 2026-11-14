"""Liga qualquer caso de uso ao SQLAlchemy com uma transação por chamada.

O módulo oferece um executor genérico que abre sessão e transação, monta o caso
de uso com essa sessão e devolve seu resultado, confirmando em caso de sucesso e
revertendo em caso de exceção. Ele existe para evitar uma classe de composição
repetida para cada rota que precisa de persistência.
"""

from collections.abc import Callable
from typing import Generic, Protocol, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

EntradaContra = TypeVar("EntradaContra", contravariant=True)
SaidaCo = TypeVar("SaidaCo", covariant=True)
Entrada = TypeVar("Entrada")
Saida = TypeVar("Saida")


class CasoDeUsoExecutavel(Protocol[EntradaContra, SaidaCo]):
    """Descreve o contrato mínimo de um caso de uso assíncrono.

    O contrato exige um método ``executar`` que recebe uma entrada e devolve um
    resultado. Ele existe para que o executor genérico aceite qualquer caso de
    uso da Application sem conhecer seus detalhes.
    """

    async def executar(self, entrada: EntradaContra) -> SaidaCo:
        """Executa o caso de uso com a entrada tipada recebida."""


class ExecutorTransacionalSqlAlchemy(Generic[Entrada, Saida]):
    """Executa um caso de uso dentro de uma sessão e transação SQLAlchemy.

    A cada chamada, a classe abre uma sessão com transação, pede à função de
    montagem o caso de uso ligado a essa sessão e delega a execução. A transação
    é confirmada ao sair sem erro e revertida se houver exceção. Ela existe para
    manter o ciclo de vida da sessão fora da Application e reaproveitar o mesmo
    mecanismo em todas as rotas.
    """

    def __init__(
        self,
        sessoes: async_sessionmaker[AsyncSession],
        montar_caso_de_uso: Callable[
            [AsyncSession], CasoDeUsoExecutavel[Entrada, Saida]
        ],
    ) -> None:
        """Guarda a fábrica de sessões e a função que monta o caso de uso.

        O construtor não abre conexão; apenas conserva as dependências da
        composição. Ele existe para que cada rota informe só como montar seu
        caso de uso a partir de uma sessão.
        """
        self._sessoes = sessoes
        self._montar_caso_de_uso = montar_caso_de_uso

    async def executar(self, entrada: Entrada) -> Saida:
        """Abre a transação, executa o caso de uso e devolve o resultado.

        O método usa ``begin`` da fábrica para que sucesso confirme e exceção
        reverta, e propaga qualquer exceção para a API traduzir em HTTP. Ele
        existe para garantir que a resposta só indique sucesso após o banco
        confirmar a operação.
        """
        async with self._sessoes.begin() as sessao:
            caso_de_uso = self._montar_caso_de_uso(sessao)
            return await caso_de_uso.executar(entrada)


def criar_executor_transacional(
    sessoes: async_sessionmaker[AsyncSession] | None,
    montar_caso_de_uso: Callable[
        [AsyncSession], CasoDeUsoExecutavel[Entrada, Saida]
    ],
) -> ExecutorTransacionalSqlAlchemy[Entrada, Saida] | None:
    """Cria o executor quando há persistência e devolve ``None`` sem ela.

    A função devolve ``None`` se não houver fábrica de sessões, mantendo a rota
    indisponível (503), e o executor genérico caso contrário. Ela existe para
    que a composição trate a ausência de banco em um único lugar.
    """
    if sessoes is None:
        return None
    return ExecutorTransacionalSqlAlchemy(sessoes, montar_caso_de_uso)
