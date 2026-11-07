"""Implementa a porta de tempo com o relógio do sistema.

O adapter devolve o instante corrente em UTC, sem expor a biblioteca de datas
às camadas internas. Ele existe para atender a porta ``Relogio`` com uma fonte
concreta e substituível, exigida pela exclusão lógica de itens do perfil.
"""

from datetime import datetime, timezone

from backend.application.ports import Relogio


class RelogioSistema(Relogio):
    """Fornece o instante atual do sistema com fuso horário UTC.

    A implementação consulta ``datetime.now`` em UTC a cada chamada. Ela existe
    porque o domínio recusa instantes de exclusão sem fuso e a Application não
    deve conhecer o relógio real.
    """

    def agora(self) -> datetime:
        """Devolve o instante corrente com fuso horário UTC.

        O método chama ``datetime.now`` informando UTC para que o resultado
        sempre carregue fuso. Ele existe para satisfazer a regra de domínio de
        exclusão e manter a fonte de tempo substituível em testes.
        """
        return datetime.now(timezone.utc)
