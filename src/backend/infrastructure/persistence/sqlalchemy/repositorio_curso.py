"""Implementa a porta de curso com SQLAlchemy assíncrono.

O adapter consulta a chave técnica persistida e envia registros para a sessão
injetada, sem controlar a transação. Ele existe para conectar o caso de uso à
persistência relacional sem acoplar as camadas internas ao ORM.
"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
from backend.application.cadastro_curso import CursoJaCadastrado
from backend.application.ports import RepositorioCurso
from backend.domain.itens_perfil import Curso
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.curso import (
    CursoRegistro,
    para_registro,
)


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class RepositorioCursoSqlAlchemy(RepositorioCurso):
    """Consulta e persiste cursos usando uma sessão externa assíncrona.

    A implementação compara a chave canônica composta normalizada, adiciona o modelo
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
        nome_normalizado: str,
        instituicao_normalizada: str,
    ) -> bool:
        """Informa se a chave de curso já possui registro persistido.

        O método consulta os campos da restrição única composta, sem recalcular ou
        reinterpretar a chave recebida. Ele existe para permitir ao caso de uso
        detectar conflito antes da tentativa de inserção.
        """
        consulta = (
            select(CursoRegistro.id)
            .where(
                CursoRegistro.usuario_id == usuario_id.valor,
                CursoRegistro.nome_normalizado == nome_normalizado,
                CursoRegistro.instituicao_normalizada == instituicao_normalizada,
            )
            .limit(1)
        )
        return await self._session.scalar(consulta) is not None

    async def salvar(self, curso: Curso) -> None:
        """Envia um curso válido à sessão e traduz colisão de unicidade.

        O método mapeia a entidade, chama ``flush`` e reconhece a restrição única
        nomeada desta tabela como duplicidade conhecida relançando CursoJaCadastrado.
        Ele existe para proteger contra concorrência sem expor detalhes SQL ao caso de uso.
        """
        self._session.add(para_registro(curso))
        try:
            await self._session.flush()
        except IntegrityError as erro:
            if _viola_chave_duplicidade(erro):
                raise CursoJaCadastrado(
                    "Curso já cadastrado para este usuário nesta instituição."
                ) from erro
            raise


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
def _viola_chave_duplicidade(erro: IntegrityError) -> bool:
    """Identifica se uma falha SQL pertence à unicidade composta de curso.

    A função compara o nome estável da constraint na mensagem do erro ou em
    sua causa original, sem transformar violações de outras tabelas em conflito de curso.
    Ela existe para preservar a tradução de erro definida pela fronteira externa.
    """
    orig_str = str(erro.orig) if erro.orig else ""
    erro_str = str(erro)
    nome_constraint = "uq_cursos_usuario_nome_instituicao_normalizados"
    return nome_constraint in orig_str or nome_constraint in erro_str
