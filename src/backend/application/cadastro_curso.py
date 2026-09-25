from dataclasses import dataclass
from backend.application.ports import GeradorCursoId, RepositorioCurso
from backend.domain.itens_perfil import Curso
from backend.domain.value_objects import UsuarioId

@dataclass(frozen=True, slots=True)
class CadastrarCursoEntrada:
    usuario_id: UsuarioId
    nome: str
    instituicao: str
    carga_horaria: int | None = None

class CadastrarCurso:
    def __init__(self, repositorio: RepositorioCurso, gerador_id: GeradorCursoId) -> None:
        self._repositorio = repositorio
        self._gerador_id = gerador_id

    async def executar(self, entrada: CadastrarCursoEntrada) -> Curso:
        curso = Curso(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            nome=entrada.nome,
            instituicao=entrada.instituicao,
            carga_horaria=entrada.carga_horaria,
        )
        await self._repositorio.salvar(curso)
        return curso