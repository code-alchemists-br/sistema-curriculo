"""Orquestra o cadastro de cursos complementares reutilizáveis de estudantes.

O módulo constrói a entidade de domínio, verifica sua chave lógica por uma
porta e solicita persistência sem importar transporte, ORM ou banco. Ele existe
para concentrar a regra de criação e duplicidade em uma unidade testável.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
from backend.application.ports import GeradorCursoId, RepositorioCurso
from backend.domain.itens_perfil import Curso
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class CursoJaCadastrado(ValueError):
    """Sinaliza tentativa de cadastrar um curso já existente para o estudante.

    A falha representa uma colisão da chave composta formada por proprietário,
    nome e instituição normalizados, sem transportar detalhes de armazenamento.
    Ela existe para que fronteiras externas possam responder conflito de forma
    segura e o caso de uso não persista uma duplicata.
    """


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
@dataclass(frozen=True, slots=True)
class CadastrarCursoEntrada:
    """Agrupa os dados internos necessários ao cadastro de um curso complementar.

    A entrada conserva proprietário tipado, nome, instituição e carga horária
    opcional sem transportar tipos HTTP ou detalhes de persistência. Ela existe
    para tornar explícito e testável o contrato do caso de uso de cadastro.
    """

    usuario_id: UsuarioId
    nome: str
    instituicao: str
    carga_horaria: int | None = None


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class CadastrarCurso:
    """Cria e persiste um curso complementar não duplicado para um estudante.

    O caso de uso gera identidade por porta, constrói a entidade para aplicar
    invariantes, consulta a chave composta de duplicidade e só então solicita salvar.
    Ele existe para coordenar a regra entre entidades independentes sem acoplar
    o núcleo a armazenamento ou interface.
    """

    def __init__(
        self,
        repositorio: RepositorioCurso,
        gerador_id: GeradorCursoId,
    ) -> None:
        """Recebe as portas usadas para verificar e persistir o curso.

        O construtor conserva somente abstrações internas injetadas, permitindo
        que o fluxo seja exercitado com doubles determinísticos. Ele existe para
        inverter a dependência da orquestração em relação à infraestrutura.
        """
        self._repositorio = repositorio
        self._gerador_id = gerador_id

    async def executar(self, entrada: CadastrarCursoEntrada) -> Curso:
        """Cria o curso e o salva quando sua chave ainda não existe.

        O método constrói a entidade para validar os campos, consulta o
        repositório usando o par canônico de nome e instituição normalizados
        e interrompe em caso de colisão; somente depois solicita salvar.
        Ele existe para impedir duplicatas lógicas sem delegar regras de negócio ao adapter.
        """
        curso = Curso(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            nome=entrada.nome,
            instituicao=entrada.instituicao,
            carga_horaria=entrada.carga_horaria,
        )
        existe = await self._repositorio.existe_por_chave_de_duplicidade(
            usuario_id=curso.usuario_id,
            nome_normalizado=curso.nome_normalizado,
            instituicao_normalizada=curso.instituicao_normalizada,
        )
        if existe:
            raise CursoJaCadastrado(
                "Curso já cadastrado para este usuário nesta instituição."
            )
        await self._repositorio.salvar(curso)
        return curso
