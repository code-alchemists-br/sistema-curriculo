from dataclasses import dataclass
from backend.application.ports import GeradorIdiomaId, RepositorioIdioma
from backend.domain.itens_perfil import Idioma
from backend.domain.value_objects import UsuarioId

@dataclass(frozen=True, slots=True)
class CadastrarIdiomaEntrada:
    usuario_id: UsuarioId
    idioma: str
    nivel: str

class CadastrarIdioma:
    def __init__(self, repositorio: RepositorioIdioma, gerador_id: GeradorIdiomaId) -> None:
        self._repositorio = repositorio
        self._gerador_id = gerador_id

    async def executar(self, entrada: CadastrarIdiomaEntrada) -> Idioma:
        idioma = Idioma(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            idioma=entrada.idioma,
            nivel=entrada.nivel,
        )
        await self._repositorio.salvar(idioma)
        return idioma