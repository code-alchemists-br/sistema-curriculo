from dataclasses import dataclass
from backend.application.ports import RepositorioUsuario
from backend.domain.entities import Usuario
from backend.domain.exceptions import EmailJaCadastrado, UsuarioNaoEncontrado
from backend.domain.value_objects import Email, Nome, UsuarioId


@dataclass(frozen=True, slots=True)
class EditarPerfilEntrada:
    usuario_id: UsuarioId
    nome: Nome
    email: Email


class EditarPerfil:
    """Orquestra a atualização dos dados cadastrais do perfil."""

    def __init__(self, repositorio_usuario: RepositorioUsuario) -> None:
        self._repositorio_usuario = repositorio_usuario

    async def executar(self, entrada: EditarPerfilEntrada) -> Usuario:
        usuario = await self._repositorio_usuario.buscar_por_id(entrada.usuario_id)
        if usuario is None:
            raise UsuarioNaoEncontrado("Utilizador não encontrado.")

        # Valida colisão caso o e-mail tenha sido alterado
        if usuario.email != entrada.email:
            outro_usuario = await self._repositorio_usuario.buscar_por_email(entrada.email)
            if outro_usuario is not None and outro_usuario.id != usuario.id:
                raise EmailJaCadastrado("Já existe uma conta cadastrada com este e-mail.")

        usuario.atualizar_perfil(novo_nome=entrada.nome, novo_email=entrada.email)
        await self._repositorio_usuario.atualizar(usuario)
        return usuario