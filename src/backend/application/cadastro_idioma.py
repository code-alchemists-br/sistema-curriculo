"""Orquestra o cadastro de idiomas reutilizáveis de estudantes.

O módulo constrói a entidade de domínio, verifica sua chave lógica por uma
porta e solicita persistência sem importar transporte, ORM ou banco. Ele existe
para concentrar a regra de criação e duplicidade em uma unidade testável.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
from backend.application.ports import GeradorIdiomaId, RepositorioIdioma
from backend.domain.itens_perfil import Idioma
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class IdiomaJaCadastrado(ValueError):
    """Sinaliza tentativa de cadastrar um idioma já existente para o estudante.

    A falha representa uma colisão da chave formada por proprietário e
    denominação normalizada, sem transportar detalhes de armazenamento. Ela
    existe para que fronteiras externas possam responder conflito de forma
    segura e o caso de uso não persista uma duplicata.
    """


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
@dataclass(frozen=True, slots=True)
class CadastrarIdiomaEntrada:
    """Agrupa os dados internos necessários ao cadastro de um idioma.

    A entrada conserva proprietário tipado, denominação e nível textual sem
    transportar tipos HTTP ou detalhes de persistência. Ela existe para tornar
    explícito e testável o contrato do caso de uso de cadastro.
    """

    usuario_id: UsuarioId
    idioma: str
    nivel: str


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class CadastrarIdioma:
    """Cria e persiste um idioma não duplicado para um estudante.

    O caso de uso gera identidade por porta, constrói a entidade para aplicar
    invariantes, consulta a chave de duplicidade e só então solicita salvar.
    Ele existe para coordenar a regra entre entidades independentes sem acoplar
    o núcleo a armazenamento ou interface.
    """

    def __init__(
        self,
        repositorio: RepositorioIdioma,
        gerador_id: GeradorIdiomaId,
    ) -> None:
        """Recebe as portas usadas para verificar e persistir o idioma.

        O construtor conserva somente abstrações internas injetadas, permitindo
        que o fluxo seja exercitado com doubles determinísticos. Ele existe para
        inverter a dependência da orquestração em relação à infraestrutura.
        """
        self._repositorio = repositorio
        self._gerador_id = gerador_id

    async def executar(self, entrada: CadastrarIdiomaEntrada) -> Idioma:
        """Cria o idioma e o salva quando sua chave ainda não existe.

        O método constrói a entidade para validar os campos, consulta o
        repositório usando sua chave canônica e interrompe em caso de colisão;
        somente depois solicita salvar. Ele existe para impedir duplicatas
        lógicas sem delegar regras de negócio ao adapter.
        """
        idioma = Idioma(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            idioma=entrada.idioma,
            nivel=entrada.nivel,
        )
        existe = await self._repositorio.existe_por_chave_de_duplicidade(
            idioma.usuario_id,
            idioma.idioma_normalizado,
        )
        if existe:
            raise IdiomaJaCadastrado("O idioma já está cadastrado.")
        await self._repositorio.salvar(idioma)
        return idioma
