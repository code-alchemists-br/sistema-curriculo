"""Implementa a porta de cadastro com sessão SQLAlchemy assíncrona injetada."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports import RepositorioUsuario

# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.usuario import Usuario
from backend.domain.value_objects import Email, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.usuario import (
    UsuarioRegistro,
    para_registro,
    para_usuario,
)

# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001


class RepositorioUsuarioSqlAlchemy(RepositorioUsuario):
    """Consulta, insere e atualiza contas usando o modelo externo e AsyncSession.

    O adapter traduz VOs em colunas e aguarda I/O, preservando a porta interna.
    A composição externa possui sessão, commit e rollback; erros são propagados
    para ela sem introduzir política de transação ou tradução de falhas aqui.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Armazena a sessão recebida para delegar a persistência da conta.

        A injeção não abre conexão e permite substituir a sessão em testes,
        mantendo seu ciclo de vida sob responsabilidade da composição externa.
        """
        self._session = session

    async def existe_por_email(self, email: Email) -> bool:
        """Retorna existência consultando EXISTS pelo valor normalizado do e-mail.

        A consulta parametrizada aguarda scalar sem carregar contas ou hashes,
        atendendo a verificação prévia de duplicidade solicitada pelo cadastro.
        """
        consulta = select(
            select(UsuarioRegistro.id)
            .where(UsuarioRegistro.email == email.valor)
            .exists()
        )
        return bool(await self._session.scalar(consulta))

    async def salvar(self, usuario: Usuario) -> None:
        """Insere uma nova conta convertendo o agregado e aguardando flush.

        Não realiza upsert ou commit: conflitos são propagados e a transação
        permanece com o chamador. O flush envia a inserção antes do retorno,
        permitindo detectar falhas sem alterar o objeto de domínio.
        """
        self._session.add(para_registro(usuario))
        await self._session.flush()

    async def obter_por_email(self, email: Email) -> Usuario | None:
        """Obtém a conta pelo e-mail normalizado e a converte para o domínio.

        A consulta aguarda uma única linha do ORM e chama o mapper externo antes
        de retornar o agregado ou a ausência. Ela existe para atender o acesso
        sem fazer a Application conhecer sessão, tabela ou modelo SQLAlchemy.
        """
        consulta = select(UsuarioRegistro).where(UsuarioRegistro.email == email.valor)
        registro = await self._session.scalar(consulta)
        return para_usuario(registro) if registro is not None else None

    async def obter_por_id(self, usuario_id: UsuarioId) -> Usuario | None:
        """Obtém um agregado pelo UUID e converte a linha para o domínio.

        A consulta parametrizada usa a identidade tipada e só devolve valores
        de domínio, incluindo contato quando persistido. Ela existe para
        atender casos de uso de edição sem expor ORM à Application.
        """
        consulta = select(UsuarioRegistro).where(
            UsuarioRegistro.id == usuario_id.valor
        )
        registro = await self._session.scalar(consulta)
        return para_usuario(registro) if registro is not None else None

    async def atualizar(self, usuario: Usuario) -> None:
        """Atualiza todos os campos mapeados sem inserir ou controlar transação.

        O método localiza a linha existente, copia os valores do mapper e
        aguarda flush; commit e rollback continuam com a composição externa.
        Ele existe para persistir edições integrais pela porta do usuário.
        """
        consulta = select(UsuarioRegistro).where(
            UsuarioRegistro.id == usuario.id.valor
        )
        registro = await self._session.scalar(consulta)
        if registro is None:
            raise LookupError("Perfil não encontrado.")

        atualizado = para_registro(usuario)
        registro.nome = atualizado.nome
        registro.email = atualizado.email
        registro.hash_senha = atualizado.hash_senha
        registro.deleted_at = atualizado.deleted_at
        registro.endereco = atualizado.endereco
        registro.cidade = atualizado.cidade
        registro.telefones = atualizado.telefones
        registro.linkedin = atualizado.linkedin
        registro.curriculo_lattes = atualizado.curriculo_lattes
        await self._session.flush()
