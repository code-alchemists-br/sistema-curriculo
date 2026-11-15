"""Implementa a porta de competência com SQLAlchemy assíncrono.

O adapter consulta a chave técnica persistida e envia registros para a sessão
injetada, sem controlar a transação. Ele existe para conectar o caso de uso à
persistência relacional sem acoplar as camadas internas ao ORM.
"""

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.cadastro_competencia import CompetenciaJaCadastrada
from backend.application.ports import RepositorioCompetencia
from backend.domain.itens_perfil import CategoriaCompetencia, Competencia
from backend.domain.value_objects import CompetenciaId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.competencia import (
    CompetenciaRegistro,
    para_competencia,
    para_registro,
)


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class RepositorioCompetenciaSqlAlchemy(RepositorioCompetencia):
    """Consulta e persiste competências usando uma sessão externa assíncrona.

    A implementação compara somente a chave já normalizada, adiciona o modelo
    ORM e usa ``flush`` para expor conflitos de unicidade sem executar commit.
    Ela existe para satisfazer a porta preservando o ciclo transacional da
    composição que forneceu a sessão.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Armazena a sessão que executará as operações de persistência.

        O construtor recebe a sessão criada na borda externa e não abre conexão
        própria. Ele existe para manter o adapter testável e subordinado ao
        ciclo de vida transacional da requisição.
        """
        self._session = session

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        categoria: CategoriaCompetencia,
        descricao_normalizada: str,
    ) -> bool:
        """Informa se a chave de competência já possui registro persistido.

        O método consulta os três campos da restrição única, sem recalcular ou
        reinterpretar a chave recebida. Ele existe para permitir ao caso de uso
        detectar conflito antes da tentativa de inserção.
        """
        consulta = (
            select(CompetenciaRegistro.id)
            .where(
                CompetenciaRegistro.usuario_id == usuario_id.valor,
                CompetenciaRegistro.categoria == categoria.value,
                CompetenciaRegistro.descricao_normalizada == descricao_normalizada,
            )
            .limit(1)
        )
        return await self._session.scalar(consulta) is not None

    async def salvar(self, competencia: Competencia) -> None:
        """Envia uma competência válida à sessão e traduz colisão de unicidade.

        O método mapeia a entidade, chama ``flush`` e reconhece somente a
        restrição nomeada desta tabela como duplicidade conhecida. Ele existe
        para proteger contra corridas sem expor detalhes SQL ao caso de uso.
        """
        self._session.add(para_registro(competencia))
        try:
            await self._session.flush()
        except IntegrityError as erro:
            if _viola_chave_duplicidade(erro):
                raise CompetenciaJaCadastrada(
                    "A competência já está cadastrada."
                ) from erro
            raise

    async def listar_por_usuario(
        self, usuario_id: UsuarioId
    ) -> tuple[Competencia, ...]:
        """Consulta e retorna todas as competências registradas para o usuário.

        O método seleciona as linhas filtrando pela chave estrangeira usuario_id,
        ordena por categoria e descrição e converte cada registro em entidade
        Competencia. Ele existe para recuperar as competências ativas do
        estudante sem expor o modelo ORM.
        """
        consulta = (
            select(CompetenciaRegistro)
            .where(CompetenciaRegistro.usuario_id == usuario_id.valor)
            .order_by(CompetenciaRegistro.categoria, CompetenciaRegistro.descricao)
        )
        resultado = await self._session.scalars(consulta)
        return tuple(para_competencia(registro) for registro in resultado)

    async def obter_por_id_e_usuario(
        self, competencia_id: CompetenciaId, usuario_id: UsuarioId
    ) -> Competencia | None:
        """Busca uma competência específica garantindo a validação de propriedade.

        O método executa consulta pontual por ID primário e chave estrangeira do
        usuário, retornando a entidade de domínio ou None caso não exista. Ele
        existe para permitir verificação segura de autoria antes de operações.
        """
        consulta = select(CompetenciaRegistro).where(
            CompetenciaRegistro.id == competencia_id.valor,
            CompetenciaRegistro.usuario_id == usuario_id.valor,
        )
        registro = await self._session.scalar(consulta)
        return para_competencia(registro) if registro is not None else None

    async def excluir(
        self, competencia_id: CompetenciaId, usuario_id: UsuarioId
    ) -> bool:
        """Remove a competência do banco se pertencer ao estudante informado.

        O método executa a instrução DELETE restrita ao ID da competência e ao
        usuario_id proprietário, confirmando a alteração com flush e avaliando
        o rowcount afetado. Ele existe para garantir a exclusão segura e reversível.
        """
        instrucao = delete(CompetenciaRegistro).where(
            CompetenciaRegistro.id == competencia_id.valor,
            CompetenciaRegistro.usuario_id == usuario_id.valor,
        )
        resultado = await self._session.execute(instrucao)
        await self._session.flush()
        return bool(resultado.rowcount and resultado.rowcount > 0)


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def _viola_chave_duplicidade(erro: IntegrityError) -> bool:
    """Identifica se uma falha SQL pertence à unicidade de competência.

    A função compara o nome estável da constraint na causa do driver, sem
    transformar violações de outras tabelas em conflito de competência. Ela
    existe para preservar a tradução de erro definida pela fronteira externa.
    """
    return "uq_competencias_usuario_categoria_descricao_normalizada" in str(erro.orig)
