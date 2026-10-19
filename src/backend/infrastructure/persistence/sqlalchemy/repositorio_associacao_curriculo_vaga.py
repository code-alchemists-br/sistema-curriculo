"""Implementa a persistência SQLAlchemy do port de associação currículo-vaga.

O adapter consulta o par pela chave composta e grava a raiz junto às linhas de
classificação em um único flush, sem realizar commit. Ele existe para conectar
o caso de uso à persistência relacional e traduzir somente colisões da chave
primária da associação para a falha conhecida pela Application.
"""

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
from backend.application.associacao_curriculo_vaga import (
    AssociacaoCurriculoVagaJaExiste,
)
from backend.application.ports import RepositorioAssociacaoCurriculoVaga
from backend.domain.associacao_curriculo_vaga import AssociacaoCurriculoVaga
from backend.domain.value_objects import CurriculoId, VagaId
from backend.infrastructure.persistence.sqlalchemy.associacao_curriculo_vaga import (
    AssociacaoCurriculoVagaRegistro,
    ClassificacaoAssociacaoRegistro,
    para_associacao,
    para_registro,
    para_registros_classificacoes,
)

_NOME_CONSTRAINT_ASSOCIACAO = "pk_associacoes_curriculo_vaga"
_ERRO_SQLITE_PK_ASSOCIACAO = (
    "UNIQUE constraint failed: "
    "associacoes_curriculo_vaga.curriculo_id, "
    "associacoes_curriculo_vaga.vaga_id"
)


# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
class RepositorioAssociacaoCurriculoVagaSqlAlchemy(RepositorioAssociacaoCurriculoVaga):
    """Consulta e grava associações através de uma sessão assíncrona injetada.

    O adapter converte o agregado em registros, consulta por chave composta e
    traduz apenas a violação nominal da PK da associação. Ele existe para
    implementar o port interno sem assumir controle do ciclo transacional.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Armazena a sessão cuja vida útil pertence à composição externa.

        O construtor não abre conexão e aceita uma sessão substituível em testes.
        Ele existe para manter commit e rollback no boundary da aplicação.
        """
        self._session = session

    async def existe_por_par(self, curriculo_id: CurriculoId, vaga_id: VagaId) -> bool:
        """Consulta a existência da associação pela chave primária composta.

        A operação usa ``AsyncSession.get`` sem alterar estado e devolve se o
        registro está presente. Ela existe para a checagem preventiva do caso
        de uso.
        """
        registro = await self._session.get(
            AssociacaoCurriculoVagaRegistro,
            (curriculo_id.valor, vaga_id.valor),
        )
        return registro is not None

    async def obter_para_atualizacao(
        self, curriculo_id: CurriculoId, vaga_id: VagaId
    ) -> AssociacaoCurriculoVaga | None:
        """Carrega o agregado e bloqueia sua raiz até o fim da transação.

        A consulta usa a chave composta com `FOR UPDATE` e depois carrega as
        classificações relacionadas. No PostgreSQL, o lock serializa mutações
        concorrentes do mesmo par; a sessão externa deve manter a transação até
        confirmar a escrita. Ela existe para evitar lost updates.
        """
        consulta_raiz = (
            select(AssociacaoCurriculoVagaRegistro)
            .where(
                AssociacaoCurriculoVagaRegistro.curriculo_id == curriculo_id.valor,
                AssociacaoCurriculoVagaRegistro.vaga_id == vaga_id.valor,
            )
            .with_for_update()
        )
        resultado_raiz = await self._session.execute(consulta_raiz)
        registro = resultado_raiz.scalar_one_or_none()
        if registro is None:
            return None

        consulta_classificacoes = select(ClassificacaoAssociacaoRegistro).where(
            ClassificacaoAssociacaoRegistro.curriculo_id == curriculo_id.valor,
            ClassificacaoAssociacaoRegistro.vaga_id == vaga_id.valor,
        )
        resultado_classificacoes = await self._session.execute(consulta_classificacoes)
        return para_associacao(registro, resultado_classificacoes.scalars().all())

    async def atualizar_classificacoes(
        self, associacao: AssociacaoCurriculoVaga
    ) -> None:
        """Substitui somente as linhas de classificação sem alterar a raiz.

        A operação exclui as classificações do par e insere as do agregado já
        validado. O flush intermediário libera as identidades ORM excluídas antes
        de inserir linhas com as mesmas chaves; ambos os flushes permanecem na
        transação externa, sem confirmar a transação. Ela existe para persistir
        alterações atômicas mantendo todas as regras na entidade de domínio.
        """
        await self._session.execute(
            delete(ClassificacaoAssociacaoRegistro).where(
                ClassificacaoAssociacaoRegistro.curriculo_id
                == associacao.curriculo_id.valor,
                ClassificacaoAssociacaoRegistro.vaga_id == associacao.vaga_id.valor,
            )
        )
        await self._session.flush()
        self._session.add_all(para_registros_classificacoes(associacao))
        await self._session.flush()

    async def salvar(self, associacao: AssociacaoCurriculoVaga) -> None:
        """Adiciona raiz e classificações e envia a unidade em um único flush.

        A operação não confirma nem reverte a transação. Se o flush indicar
        especificamente colisão da PK composta, lança a falha Application
        acordada; outros erros permanecem explícitos para o boundary externo.
        Ela existe para persistir o agregado completo sem gravação parcial.
        """
        self._session.add(para_registro(associacao))
        for registro in para_registros_classificacoes(associacao):
            self._session.add(registro)
        try:
            await self._session.flush()
        except IntegrityError as erro:
            if _violacao_da_pk_da_associacao(erro):
                raise AssociacaoCurriculoVagaJaExiste(
                    "Já existe uma associação para este currículo e esta vaga."
                ) from erro
            raise


# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
def _violacao_da_pk_da_associacao(erro: IntegrityError) -> bool:
    """Reconhece somente a colisão de identidade do agregado.

    A função consulta o nome de constraint fornecido pelo PostgreSQL ou a
    mensagem exata da chave composta produzida pelo SQLite de teste. Ela existe
    para não transformar violações de outras constraints em conflito de negócio.
    """
    diagnostico = getattr(erro.orig, "diag", None)
    if getattr(diagnostico, "constraint_name", None) == _NOME_CONSTRAINT_ASSOCIACAO:
        return True
    return str(erro.orig) == _ERRO_SQLITE_PK_ASSOCIACAO
