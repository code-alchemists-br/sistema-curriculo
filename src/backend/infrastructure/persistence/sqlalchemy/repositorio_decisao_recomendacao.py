"""Implementa a porta de decisões sobre recomendações com SQLAlchemy assíncrono.

O adapter grava e lista as decisões do estudante usando a sessão assíncrona,
convertendo entre o value object de domínio e o registro ORM. Ele existe para
conectar a Application ao banco relacional sem expor o ORM internamente.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
from backend.application.ports import RepositorioDecisaoRecomendacao
from backend.domain.decisao_recomendacao import DecisaoRecomendacao
from backend.domain.value_objects import CurriculoId
from backend.infrastructure.persistence.sqlalchemy.decisao_recomendacao import (
    DecisaoRecomendacaoRegistro,
    para_decisao,
    para_registro,
)


# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
class RepositorioDecisaoRecomendacaoSqlAlchemy(RepositorioDecisaoRecomendacao):
    """Grava e lista decisões sobre recomendações usando uma sessão externa.

    O adapter procura o registro do par versão e código: se existe, atualiza a
    decisão e o instante; se não, insere um novo. A composição externa possui
    sessão, commit e rollback. Ele existe para atender o contrato da porta
    ``RepositorioDecisaoRecomendacao`` com uma decisão por par.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Armazena a sessão que executará as operações de persistência.

        O construtor recebe a sessão gerenciada pela composição externa. Ele
        existe para manter o adapter subordinado ao ciclo de vida transacional.
        """
        self._session = session

    async def salvar(self, decisao: DecisaoRecomendacao) -> None:
        """Insere a decisão ou atualiza a existente do mesmo par, e aguarda flush.

        O método lê o registro pela chave composta; se existe, copia a decisão e
        o instante, e se não, adiciona o registro novo. Ele existe para que
        decidir de novo substitua a escolha anterior.
        """
        registro = await self._session.get(
            DecisaoRecomendacaoRegistro,
            (decisao.curriculo_id.valor, decisao.codigo),
        )
        if registro is None:
            self._session.add(para_registro(decisao))
        else:
            registro.decisao = decisao.decisao.value
            registro.decidida_em = decisao.decidida_em
        await self._session.flush()

    async def listar_por_curriculo(
        self, curriculo_id: CurriculoId
    ) -> tuple[DecisaoRecomendacao, ...]:
        """Lista as decisões da versão em ordem estável pelo código.

        O método consulta os registros da versão ordenados pelo código e converte
        cada um para o domínio. Ele existe para que a revisão saiba o que o
        estudante já decidiu.
        """
        consulta = (
            select(DecisaoRecomendacaoRegistro)
            .where(DecisaoRecomendacaoRegistro.curriculo_id == curriculo_id.valor)
            .order_by(DecisaoRecomendacaoRegistro.codigo)
        )
        resultado = await self._session.scalars(consulta)
        return tuple(para_decisao(registro) for registro in resultado.all())
