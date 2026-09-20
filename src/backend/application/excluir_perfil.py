from dataclasses import dataclass
from backend.application.ports import RepositorioUsuario
from backend.domain.exceptions import UsuarioNaoEncontrado
from backend.domain.value_objects import UsuarioId


@dataclass(frozen=True, slots=True)
class ExcluirPerfilEntrada:
    usuario_id: UsuarioId


class ExcluirPerfil:
    """Orquestra a remoção definitiva do perfil."""

    def __init__(self, repositorio_usuario: RepositorioUsuario) -> None:
        self._repositorio_usuario = repositorio_usuario

    async def executar(self, entrada: ExcluirPerfilEntrada) -> None:
        usuario = await self._repositorio_usuario.buscar_por_id(entrada.usuario_id)
        if usuario is None:
            raise UsuarioNaoEncontrado("Utilizador não encontrado.")

        await self._repositorio_usuario.excluir(entrada.usuario_id)