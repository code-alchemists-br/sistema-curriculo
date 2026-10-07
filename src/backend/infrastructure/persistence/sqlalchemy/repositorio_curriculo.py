"""Implementa a porta de currículo com sessão SQLAlchemy assíncrona injetada."""

from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports import RepositorioCurriculo
from backend.domain.curriculo import Curriculo
from backend.domain.value_objects import CurriculoId
from backend.infrastructure.persistence.sqlalchemy.curriculo import (
    CurriculoRegistro,
    atualizar_registro,
    para_curriculo,
    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    para_registro,
)

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001


class RepositorioCurriculoSqlAlchemy(RepositorioCurriculo):
    """Consulta, insere e atualiza versões de currículo usando o modelo externo e uma AsyncSession.

    O adapter traduz o agregado em colunas e aguarda I/O, preservando a porta
    interna. A composição externa possui sessão, commit e rollback; erros são
    propagados para ela sem política de transação ou tradução de falhas aqui. O
    adapter lê e grava somente as colunas escalares, sem as referências.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Armazena a sessão recebida para delegar a persistência da versão.

        A injeção não abre conexão e permite substituir a sessão em testes,
        mantendo seu ciclo de vida sob responsabilidade da composição externa.
        """
        self._session = session

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Obtém a versão pela chave primária e a converte para o domínio.

        A consulta aguarda o registro na sessão e chama o mapeador externo antes
        de retornar o agregado ou a ausência. Ela existe para atender a edição
        sem fazer a Application conhecer sessão, tabela ou modelo SQLAlchemy.
        """
        registro = await self._session.get(CurriculoRegistro, curriculo_id.valor)
        return para_curriculo(registro) if registro is not None else None

    async def atualizar(self, curriculo: Curriculo) -> None:
        """Atualiza título, layout e visibilidade do registro existente e aguarda flush.

        O método recarrega o registro pela chave primária, copia somente os
        campos editáveis e envia a alteração antes do retorno, sem commit. Se o
        registro deixou de existir, a falha é propagada. Ele existe para
        persistir a transição decidida pelo núcleo sem criar linhas novas.
        """
        registro = await self._session.get(CurriculoRegistro, curriculo.id.valor)
        if registro is None:
            raise LookupError("Currículo não encontrado para atualização.")
        atualizar_registro(registro, curriculo)
        await self._session.flush()

    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    async def salvar(self, curriculo: Curriculo) -> None:
        """Insere a nova versão convertendo o agregado e aguardando flush.

        Não realiza upsert nem commit: conflitos e violações de chave
        estrangeira são propagados e a transação permanece com o chamador. O
        flush envia a inserção antes do retorno, permitindo detectar falhas sem
        alterar o agregado.
        """
        self._session.add(para_registro(curriculo))
        await self._session.flush()