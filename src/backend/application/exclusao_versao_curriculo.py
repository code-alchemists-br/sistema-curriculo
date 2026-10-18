"""Orquestra a exclusão de uma versão de currículo de um estudante.

O módulo localiza a versão por porta, confere que ela pertence ao usuário
solicitante e só então solicita a remoção, sem conhecer HTTP ou persistência.
Ele existe para concentrar a intenção de excluir uma versão, e a verificação de
propriedade do recurso, fora de controllers e adapters.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
from backend.application.ports import RepositorioCurriculo
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain.value_objects import CurriculoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
@dataclass(frozen=True, slots=True)
class ExcluirVersaoCurriculoEntrada:
    """Agrupa a identidade do solicitante e da versão que ele quer excluir.

    A entrada transporta somente tipos de domínio, independentes de HTTP. Ela
    existe para dar contrato explícito ao caso de uso, mantendo juntos o usuário
    que pede e a versão que deseja remover.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId


# Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
class ExcluirVersaoCurriculo:
    """Exclui uma versão de currículo própria do estudante.

    O caso localiza a versão, trata ausência e propriedade de outro usuário como
    a mesma falha e só então solicita a remoção ao repositório. Ele existe para
    impedir que um estudante apague a versão de outro e para coordenar a
    exclusão sem acoplar regras a API ou banco.
    """

    # Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
    def __init__(self, repositorio_curriculo: RepositorioCurriculo) -> None:
        """Recebe a porta usada para consultar e remover versões de currículo.

        O construtor armazena somente a abstração interna, que será usada
        durante a execução e pode ser substituída por double. Ele existe para
        manter a orquestração independente da infraestrutura.
        """
        self._repositorio_curriculo = repositorio_curriculo

    # Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
    async def executar(self, entrada: ExcluirVersaoCurriculoEntrada) -> None:
        """Remove a versão do solicitante, ou falha sem nenhum efeito.

        O método localiza a versão, trata ausência e propriedade de outro usuário
        do mesmo modo, para não revelar a existência de versões alheias, e só
        então chama a remoção, uma única vez. Ele existe para garantir que a
        exclusão, que é definitiva, só ocorra para o dono da versão.
        """
        curriculo = await self._repositorio_curriculo.obter_por_id(entrada.curriculo_id)
        if curriculo is None or curriculo.usuario_id != entrada.usuario_id:
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")

        await self._repositorio_curriculo.excluir(curriculo)
