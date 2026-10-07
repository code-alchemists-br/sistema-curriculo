"""Orquestra a criação e a edição de versões de currículo de um estudante.

O módulo constrói o agregado ``Curriculo`` na criação e, na edição, localiza-o
por porta, confere que ele pertence ao usuário solicitante e delega a alteração
ao domínio, sem conhecer HTTP ou persistência. Ele existe para concentrar as
intenções de criar e editar uma versão, e a verificação de propriedade do
recurso, fora de controllers e adapters.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
from backend.application.ports import GeradorCurriculoId, RepositorioCurriculo
from backend.domain.curriculo import Curriculo
from backend.domain.value_objects import CurriculoId, UsuarioId


class CurriculoNaoEncontrado(LookupError):
    """Sinaliza que a versão de currículo não existe ou não pertence ao usuário.

    A falha agrupa ausência e propriedade de outro usuário sob a mesma resposta,
    evitando revelar que o recurso existe. Ela existe para que a borda HTTP
    traduza a negação de acesso sem expor informação sobre currículos alheios.
    """


@dataclass(frozen=True, slots=True)
class EditarVersaoCurriculoEntrada:
    """Agrupa identidade do solicitante, da versão e os novos dados válidos.

    A entrada transporta tipos de domínio e valores primitivos independentes de
    HTTP. Ela existe para dar contrato explícito ao caso de uso, mantendo juntos
    o usuário que pede e a versão que deseja alterar.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId
    titulo_versao: str
    layout: str
    is_public: bool


class EditarVersaoCurriculo:
    """Edita título, layout e visibilidade de uma versão de currículo própria.

    O caso busca o agregado, rejeita ausência ou propriedade alheia, delega a
    alteração ao domínio e persiste o novo estado. Ele existe para coordenar a
    edição sem acoplar regras a API ou repositório real.
    """

    def __init__(self, repositorio_curriculo: RepositorioCurriculo) -> None:
        """Recebe a porta usada para consultar e atualizar versões de currículo.

        O construtor armazena somente a abstração interna que será aguardada
        durante a execução e pode ser substituída por double. Ele existe para
        manter a orquestração independente da infraestrutura.
        """
        self._repositorio_curriculo = repositorio_curriculo

    async def executar(self, entrada: EditarVersaoCurriculoEntrada) -> Curriculo:
        """Aplica a edição válida e devolve a versão com o novo estado persistido.

        O método localiza a versão, trata ausência e propriedade de outro usuário
        do mesmo modo, deixa o domínio validar os dados e só então solicita a
        atualização. Ele existe para impedir que um usuário altere currículos
        alheios e que dados inválidos cheguem ao armazenamento.
        """
        curriculo = await self._repositorio_curriculo.obter_por_id(entrada.curriculo_id)
        if curriculo is None or curriculo.usuario_id != entrada.usuario_id:
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")

        curriculo.editar_versao(entrada.titulo_versao, entrada.layout, entrada.is_public)
        await self._repositorio_curriculo.atualizar(curriculo)
        return curriculo


# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
@dataclass(frozen=True, slots=True)
class CriarVersaoCurriculoEntrada:
    """Agrupa o proprietário e os dados válidos para criar uma versão de currículo.

    A entrada transporta tipos de domínio e valores primitivos independentes de
    HTTP e não inclui identidade, que é gerada pelo caso de uso. Ela existe para
    dar contrato explícito à criação, mantendo juntos o dono e os dados da nova
    versão.
    """

    usuario_id: UsuarioId
    titulo_versao: str
    layout: str
    is_public: bool


# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
class CriarVersaoCurriculo:
    """Cria e solicita o salvamento de uma nova versão de currículo.

    O caso obtém uma identidade por porta, constrói o agregado para que o
    domínio aplique suas invariantes e só então delega o salvamento ao
    repositório. Ele existe para coordenar a criação sem acoplar regras a API ou
    banco e sem persistir versões inválidas.
    """

    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    def __init__(
        self,
        repositorio_curriculo: RepositorioCurriculo,
        gerador_id: GeradorCurriculoId,
    ) -> None:
        """Recebe as portas necessárias para gerar a identidade e salvar a versão.

        O construtor armazena somente abstrações internas, que serão usadas
        durante a execução e podem ser substituídas por doubles. Ele existe para
        manter a orquestração independente da infraestrutura.
        """
        self._repositorio_curriculo = repositorio_curriculo
        self._gerador_id = gerador_id

    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    async def executar(self, entrada: CriarVersaoCurriculoEntrada) -> Curriculo:
        """Cria uma versão validada e devolve o agregado salvo.

        O método gera a identidade, constrói o ``Curriculo`` (o domínio recusa
        título em branco e visibilidade inválida) e só chama o repositório após a
        construção bem-sucedida. Ele existe para assegurar que somente versões
        válidas sejam persistidas.
        """
        curriculo = Curriculo(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            titulo_versao=entrada.titulo_versao,
            layout=entrada.layout,
            is_public=entrada.is_public,
        )
        await self._repositorio_curriculo.salvar(curriculo)
        return curriculo