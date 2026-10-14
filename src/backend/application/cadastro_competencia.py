"""Orquestra o cadastro de competências reutilizáveis de estudantes.

O módulo constrói a entidade de domínio, verifica sua chave lógica por uma
porta e solicita persistência sem importar transporte, ORM ou banco. Ele existe
para concentrar a regra de criação e duplicidade em uma unidade testável.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
from backend.application.ports import GeradorCompetenciaId, RepositorioCompetencia
from backend.domain.itens_perfil import CategoriaCompetencia, Competencia
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class CompetenciaJaCadastrada(ValueError):
    """Sinaliza tentativa de cadastrar uma competência já existente.

    A falha representa uma colisão da chave formada por proprietário, categoria
    e descrição normalizada, sem transportar detalhes de armazenamento. Ela
    existe para que fronteiras externas possam responder conflito de forma
    segura e o caso de uso não persista uma duplicata.
    """


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
@dataclass(frozen=True, slots=True)
class CadastrarCompetenciaEntrada:
    """Agrupa os dados internos necessários ao cadastro de uma competência.

    A entrada conserva proprietário tipado, categoria e textos sem transportar
    tipos HTTP ou detalhes de persistência. Ela existe para tornar explícito e
    testável o contrato do caso de uso de cadastro.
    """

    usuario_id: UsuarioId
    categoria: CategoriaCompetencia
    descricao: str
    nivel: str


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class CadastrarCompetencia:
    """Cria e persiste uma competência não duplicada para um estudante.

    O caso de uso gera identidade por porta, constrói a entidade para aplicar
    invariantes, consulta a chave de duplicidade e só então solicita salvar.
    Ele existe para coordenar a regra entre entidades independentes sem acoplar
    o núcleo a armazenamento ou interface.
    """

    def __init__(
        self,
        repositorio: RepositorioCompetencia,
        gerador_id: GeradorCompetenciaId,
    ) -> None:
        """Recebe as portas usadas para verificar e persistir a competência.

        O construtor conserva somente abstrações internas injetadas, permitindo
        que o fluxo seja exercitado com doubles determinísticos. Ele existe para
        inverter a dependência da orquestração em relação à infraestrutura.
        """
        self._repositorio = repositorio
        self._gerador_id = gerador_id

    async def executar(self, entrada: CadastrarCompetenciaEntrada) -> Competencia:
        """Cria a competência e a salva quando sua chave ainda não existe.

        O método constrói a entidade para validar os campos, consulta o
        repositório usando sua chave canônica e interrompe em caso de colisão;
        somente depois solicita salvar. Ele existe para impedir duplicatas
        lógicas sem delegar regras de negócio ao adapter.
        """
        competencia = Competencia(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            categoria=entrada.categoria,
            descricao=entrada.descricao,
            nivel=entrada.nivel,
        )
        existe = await self._repositorio.existe_por_chave_de_duplicidade(
            competencia.usuario_id,
            competencia.categoria,
            competencia.descricao_normalizada,
        )
        if existe:
            raise CompetenciaJaCadastrada("A competência já está cadastrada.")
        await self._repositorio.salvar(competencia)
        return competencia
