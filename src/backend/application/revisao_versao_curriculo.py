"""Orquestra a revisão de campos obrigatórios de uma versão de currículo.

O módulo obtém a prévia da versão, que já confere a propriedade de tudo o que
entra nela, e aplica a regra de revisão do domínio sobre o conteúdo recebido,
sem conhecer HTTP ou persistência. Ele existe para concentrar a intenção de
revisar o currículo antes da exportação fora de controllers e adapters.
"""

from dataclasses import dataclass
from typing import Protocol

# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
from backend.application.previa_versao_curriculo import (
    GerarPreviaVersaoCurriculoEntrada,
    PreviaVersaoCurriculo,
)
from backend.domain.revisao_curriculo import ResultadoRevisao, revisar_curriculo
from backend.domain.value_objects import CurriculoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
class GeradorDePrevia(Protocol):
    """Define a capacidade de gerar a prévia de uma versão de currículo.

    O contrato recebe a entrada da prévia e devolve o modelo de leitura já
    filtrado por proprietário. Ele existe para que a revisão dependa de uma
    abstração, e não do caso de uso concreto, e possa ser testada com um double.
    """

    # Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
    async def executar(
        self, entrada: GerarPreviaVersaoCurriculoEntrada
    ) -> PreviaVersaoCurriculo:
        """Gera a prévia da versão do solicitante.

        Implementações aplicam a verificação de propriedade e levantam a falha de
        versão não encontrada quando for o caso. O método existe para que a
        revisão reaproveite essa garantia sem repeti-la.
        """


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
@dataclass(frozen=True, slots=True)
class RevisarVersaoCurriculoEntrada:
    """Agrupa a identidade do solicitante e da versão que ele quer revisar.

    A entrada transporta somente tipos de domínio, independentes de HTTP. Ela
    existe para dar contrato explícito ao caso de uso, mantendo juntos o usuário
    que pede e a versão que deseja revisar.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
class RevisarVersaoCurriculo:
    """Revisa os campos obrigatórios de uma versão de currículo própria.

    O caso obtém a prévia da versão e entrega seu conteúdo à regra de revisão do
    domínio, sem alterar nenhum estado. Ele existe para que o estudante saiba o
    que falta no currículo sem que dados alheios possam entrar na revisão.
    """

    # Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
    def __init__(self, gerar_previa: GeradorDePrevia) -> None:
        """Recebe a capacidade usada para obter a prévia da versão.

        O construtor armazena somente a abstração interna, que será usada durante
        a execução e pode ser substituída por double. Ele existe para manter a
        orquestração independente da infraestrutura.
        """
        self._gerar_previa = gerar_previa

    # Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
    async def executar(self, entrada: RevisarVersaoCurriculoEntrada) -> ResultadoRevisao:
        """Devolve o resultado da revisão da versão do solicitante.

        O método pede a prévia, que recusa versão ausente ou alheia com a falha
        de não encontrado, e aplica a regra de revisão sobre o estudante e os
        itens de cada seção. Ele existe para impedir que se revise dado de outro
        estudante e para manter a regra de completude no domínio.
        """
        previa = await self._gerar_previa.executar(
            GerarPreviaVersaoCurriculoEntrada(
                usuario_id=entrada.usuario_id,
                curriculo_id=entrada.curriculo_id,
            )
        )
        return revisar_curriculo(
            usuario=previa.usuario,
            formacoes=previa.formacoes,
            experiencias=previa.experiencias,
            projetos=previa.projetos,
            competencias=previa.competencias,
            idiomas=previa.idiomas,
        )