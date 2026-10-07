"""Orquestra a seleção e a desseleção de itens do perfil em uma versão de currículo.

O módulo localiza o agregado ``Curriculo`` por porta, confere que ele pertence
ao usuário solicitante, verifica por outra porta que o item é do mesmo usuário e
delega a alteração ao domínio, sem conhecer HTTP ou persistência. Ele existe
para concentrar as intenções de selecionar e desselecionar itens e a regra de
propriedade transagregados fora do domínio, de controllers e de adapters.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
from backend.application.ports import ConsultaProprietarioItem, RepositorioCurriculo
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain.curriculo import Curriculo
from backend.domain.value_objects import CurriculoId, ReferenciaCurriculo, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
class ItemNaoEncontrado(LookupError):
    """Sinaliza que o item do perfil não existe ou não pertence ao usuário.

    A falha agrupa ausência e propriedade de outro usuário sob a mesma resposta,
    evitando revelar que o item existe. Ela existe para que a borda HTTP
    traduza a negação sem expor informação sobre itens de outros estudantes.
    """


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
@dataclass(frozen=True, slots=True)
class SelecionarItemVersaoCurriculoEntrada:
    """Agrupa o solicitante, a versão e a referência do item a selecionar.

    A entrada transporta tipos de domínio independentes de HTTP, com a
    referência já tipada pelo seu identificador. Ela existe para dar contrato
    explícito à seleção, mantendo juntos o usuário, a versão e o item.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId
    referencia: ReferenciaCurriculo


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
@dataclass(frozen=True, slots=True)
class DesselecionarItemVersaoCurriculoEntrada:
    """Agrupa o solicitante, a versão e a referência do item a desselecionar.

    A entrada transporta tipos de domínio independentes de HTTP, com a
    referência já tipada pelo seu identificador. Ela existe para dar contrato
    explícito à desseleção, mantendo juntos o usuário, a versão e o item.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId
    referencia: ReferenciaCurriculo


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
class SelecionarItemVersaoCurriculo:
    """Inclui um item do próprio perfil em uma versão de currículo própria.

    O caso busca a versão, rejeita ausência ou propriedade alheia, confere que o
    item pertence ao mesmo usuário, delega a inclusão ao domínio e persiste o
    novo estado. Ele existe para impedir que o item de outro estudante entre em
    uma versão e seja exposto em uma exportação.
    """

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    def __init__(
        self,
        repositorio_curriculo: RepositorioCurriculo,
        consulta_proprietario: ConsultaProprietarioItem,
    ) -> None:
        """Recebe as portas usadas para consultar a versão, o dono do item e atualizar.

        O construtor armazena somente abstrações internas, que serão aguardadas
        durante a execução e podem ser substituídas por doubles. Ele existe para
        manter a orquestração independente da infraestrutura.
        """
        self._repositorio_curriculo = repositorio_curriculo
        self._consulta_proprietario = consulta_proprietario

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def executar(self, entrada: SelecionarItemVersaoCurriculoEntrada) -> Curriculo:
        """Seleciona o item e devolve a versão com a seleção atualizada e persistida.

        O método trata ausência e propriedade alheia da versão do mesmo modo,
        faz o mesmo com o item, deixa o domínio recusar duplicidade e só então
        solicita a atualização. Ele existe para garantir que somente itens do
        próprio usuário componham a versão.
        """
        curriculo = await self._repositorio_curriculo.obter_por_id(entrada.curriculo_id)
        if curriculo is None or curriculo.usuario_id != entrada.usuario_id:
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")

        proprietario = await self._consulta_proprietario.obter_proprietario(entrada.referencia)
        if proprietario is None or proprietario != entrada.usuario_id:
            raise ItemNaoEncontrado("Item do perfil não encontrado.")

        curriculo.incluir_referencia(entrada.referencia)
        await self._repositorio_curriculo.atualizar(curriculo)
        return curriculo


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
class DesselecionarItemVersaoCurriculo:
    """Remove um item da seleção de uma versão de currículo própria.

    O caso busca a versão, rejeita ausência ou propriedade alheia, delega a
    remoção ao domínio e persiste o novo estado. Ele existe para permitir
    desfazer a seleção sem consultar o dono do item, pois a referência só existe
    se já passou pela verificação ao ser incluída.
    """

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    def __init__(self, repositorio_curriculo: RepositorioCurriculo) -> None:
        """Recebe a porta usada para consultar e atualizar versões de currículo.

        O construtor armazena somente a abstração interna, que será aguardada
        durante a execução e pode ser substituída por double. Ele existe para
        manter a orquestração independente da infraestrutura.
        """
        self._repositorio_curriculo = repositorio_curriculo

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def executar(self, entrada: DesselecionarItemVersaoCurriculoEntrada) -> Curriculo:
        """Desseleciona o item e devolve a versão com a seleção atualizada e persistida.

        O método trata ausência e propriedade alheia da versão do mesmo modo,
        deixa o domínio recusar a remoção de item não selecionado e só então
        solicita a atualização. Ele existe para manter a regra de composição no
        agregado e impedir que um usuário altere versões alheias.
        """
        curriculo = await self._repositorio_curriculo.obter_por_id(entrada.curriculo_id)
        if curriculo is None or curriculo.usuario_id != entrada.usuario_id:
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")

        curriculo.remover_referencia(entrada.referencia)
        await self._repositorio_curriculo.atualizar(curriculo)
        return curriculo
