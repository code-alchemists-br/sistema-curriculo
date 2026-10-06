"""Orquestra a edição de uma versão de currículo de um estudante.

O módulo localiza o agregado ``Curriculo`` por porta, confere que ele pertence
ao usuário solicitante e delega a alteração ao domínio, sem conhecer HTTP ou
persistência. Ele existe para concentrar a intenção de editar uma versão e a
verificação de propriedade do recurso fora de controllers e adapters.
"""

from dataclasses import dataclass

from backend.application.ports import RepositorioCurriculo
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