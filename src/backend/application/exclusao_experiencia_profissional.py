"""Orquestra a exclusão lógica de experiências profissionais pelo próprio estudante.

O módulo localiza a experiência por identidade e proprietário, inclusive se já
excluída, obtém o instante por uma porta de relógio e solicita a marcação
condicional, sem conhecer transporte ou infraestrutura. Ele existe para que
somente o dono remova suas experiências, sem purga física e sem revelar dados
de terceiros.
"""

from dataclasses import dataclass

from backend.application.edicao_experiencia_profissional import (
    ExperienciaProfissionalNaoEncontrada,
)
from backend.application.ports import Relogio, RepositorioExperienciaProfissional
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import ExperienciaProfissionalId, UsuarioId


@dataclass(frozen=True, slots=True)
class ExcluirExperienciaProfissionalEntrada:
    """Agrupa proprietário e experiência para a intenção de exclusão lógica.

    A entrada contém somente identidades tipadas já resolvidas pela fronteira
    externa, sem instante ou política de retenção. Ela existe para manter a
    exclusão própria independente de HTTP e deixar o instante sob controle do
    caso de uso.
    """

    usuario_id: UsuarioId
    experiencia_id: ExperienciaProfissionalId


class ExcluirExperienciaProfissional:
    """Exclui logicamente uma experiência própria e trata repetição como sucesso.

    O caso busca inclusive registros excluídos sob ID e proprietário, usa o
    relógio somente na primeira transição e relê após conflito concorrente.
    Ele existe para remover experiência ativa sem purga e sem revelar itens
    alheios.
    """

    def __init__(
        self,
        repositorio: RepositorioExperienciaProfissional,
        relogio: Relogio,
    ) -> None:
        """Recebe as portas de experiência e tempo usadas pela exclusão.

        O construtor guarda abstrações substituíveis por doubles e não inicia
        I/O. Ele existe para manter a orquestração independente de persistência
        e tornar instante e concorrência determinísticos nos testes.
        """
        self._repositorio = repositorio
        self._relogio = relogio

    async def executar(
        self, entrada: ExcluirExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Exclui a experiência própria ou devolve seu estado já excluído.

        A operação consulta por ID e proprietário incluindo excluídas, falha de
        forma uniforme para ausência ou dono diferente, devolve sem efeito uma
        experiência já excluída, marca somente registros ativos e relê em caso
        de disputa para preservar o primeiro instante. Ela existe para tornar a
        exclusão idempotente e evitar distinguir ausência de propriedade alheia.
        """
        experiencia = await self._repositorio.obter_por_id_e_usuario_incluindo_excluidas(
            entrada.experiencia_id, entrada.usuario_id
        )
        if experiencia is None or experiencia.usuario_id != entrada.usuario_id:
            raise ExperienciaProfissionalNaoEncontrada(
                "Experiência profissional não encontrada."
            )
        if experiencia.excluida:
            return experiencia

        instante_exclusao = self._relogio.agora()
        experiencia_excluida = experiencia.excluir(instante_exclusao)
        marcada = await self._repositorio.marcar_excluida(
            entrada.experiencia_id, entrada.usuario_id, instante_exclusao
        )
        if marcada:
            return experiencia_excluida

        recarregada = await self._repositorio.obter_por_id_e_usuario_incluindo_excluidas(
            entrada.experiencia_id, entrada.usuario_id
        )
        if (
            recarregada is None
            or recarregada.usuario_id != entrada.usuario_id
            or not recarregada.excluida
        ):
            raise ExperienciaProfissionalNaoEncontrada(
                "Experiência profissional não encontrada."
            )
        return recarregada
