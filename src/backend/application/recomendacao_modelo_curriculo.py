"""Orquestra uma recomendação revisável de modelo de currículo por IA.

O módulo reaproveita a entrada e o preparo seguro da adequação à vaga, mas
delega a resposta a uma porta distinta e não grava alterações. Ele existe para
separar a sugestão de apresentação da decisão posterior do estudante.
"""

from typing import Protocol

from backend.application.adequacao_semantica import (
    ContextoAdequacaoCurriculoVaga,
    PreparadorContextoAssistenciaCurriculo,
    SolicitarAdequacaoCurriculoVagaEntrada,
)
from backend.domain.recomendacao_modelo_curriculo import RecomendacaoModeloCurriculo

# Proveniência: decision-analysis prompts/backend/20261105-181751-adequacao-semantica-gpt-nano-v005.md#v005


class GeradorRecomendacaoModeloCurriculo(Protocol):
    """Define a porta que obtém uma recomendação tipada para contexto autorizado.

    A porta recebe o mesmo contexto limitado da adequação e devolve somente um
    value object de recomendação. Ela existe para permitir IA ou doubles sem
    acoplar o caso de uso a HTTP, SDK ou formato externo.
    """

    async def gerar(
        self, contexto: ContextoAdequacaoCurriculoVaga
    ) -> RecomendacaoModeloCurriculo:
        """Gera uma recomendação revisável a partir do contexto já protegido.

        Implementações escolhem o provedor e validam o formato externo antes de
        devolver o resultado tipado. O método existe para que a Application não
        conheça detalhes de integração nem aplique a sugestão recebida.
        """


class RecomendarModeloCurriculo:
    """Gera sugestão de modelo sem alterar a versão de currículo.

    O caso usa um preparador compartilhado para verificar propriedade,
    consentimento e minimização, e chama uma porta de recomendação. Ele existe
    para tornar a IA uma fonte de proposta, não uma alteração automática.
    """

    def __init__(
        self,
        preparador: PreparadorContextoAssistenciaCurriculo,
        gerador: GeradorRecomendacaoModeloCurriculo,
    ) -> None:
        """Recebe o preparo comum e a porta de geração por injeção interna.

        O construtor mantém as dependências substituíveis e não compõe adapters.
        Ele existe para permitir testes unitários e preservar dependências em
        direção ao núcleo.
        """
        self._preparador = preparador
        self._gerador = gerador

    async def executar(
        self, entrada: SolicitarAdequacaoCurriculoVagaEntrada
    ) -> RecomendacaoModeloCurriculo:
        """Prepara contexto compartilhado e devolve a proposta sem persistir.

        O método delega todas as regras de propriedade, seleção e consentimento
        ao preparador antes de chamar a porta. Ele existe para garantir que a
        recomendação por IA não ultrapasse os dados autorizados nem mude layout.
        """
        preparacao = await self._preparador.preparar(entrada)
        return await self._gerador.gerar(preparacao.contexto)
