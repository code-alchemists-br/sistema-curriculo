"""Implementa a porta de currículo com sessão SQLAlchemy assíncrona injetada."""

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports import RepositorioCurriculo
from backend.domain.curriculo import Curriculo
from backend.domain.value_objects import CurriculoId
from backend.infrastructure.persistence.sqlalchemy.curriculo import (
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    CurriculoItemRegistro,
    CurriculoRegistro,
    atualizar_registro,
    para_curriculo,
    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    para_registro,
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    para_registros_itens,
    para_tipo_e_item_id,
)

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001


class RepositorioCurriculoSqlAlchemy(RepositorioCurriculo):
    """Consulta, insere e atualiza versões de currículo usando o modelo externo e uma AsyncSession.

    O adapter traduz o agregado em colunas e aguarda I/O, preservando a porta
    interna. A composição externa possui sessão, commit e rollback; erros são
    propagados para ela sem política de transação ou tradução de falhas aqui. O
    adapter reconstrói a seleção de itens ao carregar e, ao gravar, persiste
    somente a diferença entre as referências do agregado e as linhas existentes.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Armazena a sessão recebida para delegar a persistência da versão.

        A injeção não abre conexão e permite substituir a sessão em testes,
        mantendo seu ciclo de vida sob responsabilidade da composição externa.
        """
        self._session = session

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Obtém a versão pela chave primária e a converte para o domínio.

        A consulta aguarda o registro na sessão, carrega as linhas de seleção da
        versão e chama o mapeador externo antes de retornar o agregado, já com
        suas referências, ou a ausência. Ela existe para atender os casos de uso
        sem fazer a Application conhecer sessão, tabela ou modelo SQLAlchemy.
        """
        registro = await self._session.get(CurriculoRegistro, curriculo_id.valor)
        if registro is None:
            return None
        itens = await self._obter_itens(registro.id)
        return para_curriculo(registro, itens)

    async def atualizar(self, curriculo: Curriculo) -> None:
        """Atualiza a versão existente e sua seleção de itens e aguarda flush.

        O método recarrega o registro pela chave primária, copia os campos
        editáveis, sincroniza as linhas de seleção com as referências do
        agregado e envia a alteração antes do retorno, sem commit. Se o registro
        deixou de existir, a falha é propagada. Ele existe para persistir a
        transição decidida pelo núcleo sem criar versões novas.
        """
        registro = await self._session.get(CurriculoRegistro, curriculo.id.valor)
        if registro is None:
            raise LookupError("Currículo não encontrado para atualização.")
        atualizar_registro(registro, curriculo)
        await self._sincronizar_itens(curriculo)
        await self._session.flush()

    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    async def salvar(self, curriculo: Curriculo) -> None:
        """Insere a nova versão convertendo o agregado e aguardando flush.

        Não realiza upsert nem commit: conflitos e violações de chave
        estrangeira são propagados e a transação permanece com o chamador. O
        flush envia a inserção da versão antes de qualquer linha de seleção, para
        que a chave estrangeira desta já encontre a versão, e um segundo flush
        envia a seleção somente quando ela existe. Falhas são detectadas antes
        do retorno, sem alterar o agregado.
        """
        self._session.add(para_registro(curriculo))
        await self._session.flush()
        registros_itens = para_registros_itens(curriculo)
        if registros_itens:
            for registro_item in registros_itens:
                self._session.add(registro_item)
            await self._session.flush()

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def _obter_itens(self, curriculo_id: UUID) -> list[CurriculoItemRegistro]:
        """Carrega as linhas de seleção da versão informada.

        A consulta filtra pela chave estrangeira da versão e aguarda o resultado
        na sessão, devolvendo os registros ORM para o mapeador externo. Ela existe
        para que a leitura e a sincronização partam da mesma fonte de verdade.
        """
        consulta = select(CurriculoItemRegistro).where(CurriculoItemRegistro.curriculo_id == curriculo_id)
        resultado = await self._session.scalars(consulta)
        return list(resultado.all())

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def _sincronizar_itens(self, curriculo: Curriculo) -> None:
        """Remove as linhas que saíram da seleção e insere as que entraram.

        O método compara as linhas existentes com as referências do agregado e
        aplica somente a diferença, em ordem determinística, sem tocar linhas que
        não mudaram. Ele existe para que editar título, layout ou visibilidade
        nunca apague a seleção e para que a seleção persista só o que mudou.
        """
        existentes = {(item.tipo, item.item_id): item for item in await self._obter_itens(curriculo.id.valor)}
        desejadas = {para_tipo_e_item_id(referencia) for referencia in curriculo.referencias}
        for chave in sorted(existentes.keys() - desejadas, key=lambda chave: (chave[0], str(chave[1]))):
            await self._session.delete(existentes[chave])
        for registro_item in para_registros_itens(curriculo):
            if (registro_item.tipo, registro_item.item_id) not in existentes:
                self._session.add(registro_item)