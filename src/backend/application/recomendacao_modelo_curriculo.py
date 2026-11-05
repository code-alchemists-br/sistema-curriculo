"""Orquestra a recomendação local de modelo para uma versão de currículo.

O módulo verifica que a versão pertence ao estudante e delega a orientação à
política pura de domínio. Ele existe para separar a intenção de recomendar
apresentação da adequação textual por IA e não persiste qualquer mudança.
"""

from dataclasses import dataclass

from backend.application.ports import RepositorioCurriculo
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain.recomendacao_modelo_curriculo import (
    ObjetivoCurriculo,
    PoliticaRecomendacaoModeloCurriculo,
    RecomendacaoModeloCurriculo,
)
from backend.domain.value_objects import CurriculoId, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261102-235645-adequacao-semantica-gpt-nano-v003.md#v003


@dataclass(frozen=True, slots=True)
class RecomendarModeloCurriculoEntrada:
    """Reúne solicitante, versão e objetivo para pedir orientação de layout.

    A entrada transporta identidades e a enumeração de domínio sem representar
    transporte HTTP ou estado persistido. Ela existe para tornar a intenção de
    recomendação explícita e independente do adaptador de entrada.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId
    objetivo: ObjetivoCurriculo


class RecomendarModeloCurriculo:
    """Recomenda um modelo inicial sem alterar uma versão de currículo.

    O caso de uso consulta a versão por porta, oculta ausência ou propriedade
    alheia e delega o mapeamento à política do domínio, sem chamar IA nem
    persistir a resposta. Ele existe para orientar a decisão do estudante sem
    remover sua autonomia sobre o layout final.
    """

    def __init__(
        self,
        repositorio_curriculo: RepositorioCurriculo,
        politica: PoliticaRecomendacaoModeloCurriculo | None = None,
    ) -> None:
        """Armazena a porta de consulta e a política de recomendação escolhida.

        O construtor usa a política padrão quando nenhuma é informada e aceita
        injeção para testes ou evolução de regras internas, sem conhecer
        persistência concreta. Ele existe para manter a orquestração coesa e
        substituível dentro das fronteiras da Application.
        """
        self._repositorio_curriculo = repositorio_curriculo
        self._politica = politica or PoliticaRecomendacaoModeloCurriculo()

    async def executar(
        self, entrada: RecomendarModeloCurriculoEntrada
    ) -> RecomendacaoModeloCurriculo:
        """Verifica propriedade e devolve a recomendação sem persistir alterações.

        O método consulta apenas a versão indicada, trata ausência e dono alheio
        pela mesma falha e aplica a política ao objetivo declarado. Ele existe
        para impedir recomendação sobre currículo de terceiros e garantir que
        este fluxo permaneça somente de leitura.
        """
        curriculo = await self._repositorio_curriculo.obter_por_id(entrada.curriculo_id)
        if curriculo is None or curriculo.usuario_id != entrada.usuario_id:
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")
        return self._politica.recomendar(entrada.objetivo)
