"""Orquestra o registro e a consulta da decisão do estudante sobre recomendações.

O módulo confere que a versão é do estudante, que o código escolhido é mesmo uma
recomendação (aviso) da revisão atual, marca a decisão com o instante do relógio
e a grava pela porta de persistência, sem conhecer HTTP ou banco. Ele existe
para que o estudante aceite ou rejeite recomendações da revisão de uma versão
própria, sem que se possa decidir sobre erros, sobre códigos inexistentes ou
sobre versões de outro estudante.
"""

from dataclasses import dataclass
from typing import Protocol

# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
from backend.application.ports import (
    Relogio,
    RepositorioCurriculo,
    RepositorioDecisaoRecomendacao,
)
from backend.application.revisao_versao_curriculo import RevisarVersaoCurriculoEntrada
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain.decisao_recomendacao import DecisaoEstudante, DecisaoRecomendacao
from backend.domain.revisao_curriculo import ResultadoRevisao, SeveridadePendencia
from backend.domain.value_objects import CurriculoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
class RecomendacaoNaoEncontrada(LookupError):
    """Sinaliza que o código informado não é uma recomendação da revisão atual.

    A falha agrupa o código inexistente e o código de uma pendência que é erro,
    que não pode ser aceito nem rejeitado. Ela existe para que a borda HTTP
    traduza a recusa sem distinguir os dois casos.
    """


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
class RevisorDeVersao(Protocol):
    """Define a capacidade de revisar uma versão de currículo do estudante.

    O contrato recebe a entrada da revisão e devolve o resultado, recusando
    versão ausente ou alheia com a falha de não encontrado. Ele existe para que a
    decisão dependa de uma abstração, e não do caso de uso concreto, e possa ser
    testada com um double.
    """

    async def executar(self, entrada: RevisarVersaoCurriculoEntrada) -> ResultadoRevisao:
        """Revisa a versão do solicitante e devolve as pendências encontradas.

        Implementações aplicam a verificação de propriedade e levantam a falha de
        versão não encontrada quando for o caso. O método existe para que a
        decisão reaproveite essa garantia sem repeti-la.
        """


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
@dataclass(frozen=True, slots=True)
class RegistrarDecisaoRecomendacaoEntrada:
    """Agrupa o solicitante, a versão, o código da recomendação e a decisão.

    A entrada transporta tipos de domínio independentes de HTTP. Ela existe para
    dar contrato explícito ao registro, mantendo juntos quem decide, a versão, a
    recomendação e a escolha.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId
    codigo: str
    decisao: DecisaoEstudante


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
class RegistrarDecisaoRecomendacao:
    """Registra a decisão do estudante sobre uma recomendação da própria versão.

    O caso revisa a versão (o que recusa versão ausente ou alheia), confere que o
    código é um aviso da revisão atual, lê o instante no relógio e grava a
    decisão, substituindo a anterior do mesmo código. Ele existe para impedir
    decisões sobre erros, sobre códigos inventados e sobre dados de outro
    estudante.
    """

    # Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
    def __init__(
        self,
        revisor: RevisorDeVersao,
        repositorio: RepositorioDecisaoRecomendacao,
        relogio: Relogio,
    ) -> None:
        """Recebe a revisão, a persistência das decisões e o relógio.

        O construtor armazena somente abstrações internas, que podem ser
        substituídas por doubles. Ele existe para manter a orquestração
        independente da infraestrutura e do relógio do sistema.
        """
        self._revisor = revisor
        self._repositorio = repositorio
        self._relogio = relogio

    # Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
    async def executar(
        self, entrada: RegistrarDecisaoRecomendacaoEntrada
    ) -> DecisaoRecomendacao:
        """Grava a decisão e a devolve, se o código for um aviso da revisão atual.

        O método pede a revisão da versão, recusa o código que não seja um aviso
        e só então cria a decisão com o instante do relógio e a persiste. Ele
        existe para que nada seja gravado quando a versão é alheia ou a
        recomendação não existe.
        """
        resultado = await self._revisor.executar(
            RevisarVersaoCurriculoEntrada(
                usuario_id=entrada.usuario_id, curriculo_id=entrada.curriculo_id
            )
        )
        if not any(
            pendencia.codigo == entrada.codigo
            and pendencia.severidade is SeveridadePendencia.AVISO
            for pendencia in resultado.pendencias
        ):
            raise RecomendacaoNaoEncontrada("Recomendação não encontrada.")
        decisao = DecisaoRecomendacao(
            curriculo_id=entrada.curriculo_id,
            codigo=entrada.codigo,
            decisao=entrada.decisao,
            decidida_em=self._relogio.agora(),
        )
        await self._repositorio.salvar(decisao)
        return decisao


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
@dataclass(frozen=True, slots=True)
class ConsultarDecisoesRecomendacaoEntrada:
    """Agrupa o solicitante e a versão cujas decisões são consultadas.

    A entrada transporta tipos de domínio independentes de HTTP. Ela existe para
    dar contrato explícito à consulta, mantendo juntos quem pede e a versão.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
class ConsultarDecisoesRecomendacao:
    """Lista as decisões do estudante sobre as recomendações de uma versão própria.

    O caso confere que a versão existe e pertence ao solicitante e devolve as
    decisões gravadas, em ordem estável. Ele existe para que o estudante saiba o
    que já aceitou ou rejeitou sem ver dados de outra pessoa.
    """

    # Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
    def __init__(
        self,
        repositorio_curriculo: RepositorioCurriculo,
        repositorio_decisao: RepositorioDecisaoRecomendacao,
    ) -> None:
        """Recebe as portas usadas para conferir a versão e ler as decisões.

        O construtor armazena somente abstrações internas, que podem ser
        substituídas por doubles. Ele existe para manter a orquestração
        independente da infraestrutura.
        """
        self._repositorio_curriculo = repositorio_curriculo
        self._repositorio_decisao = repositorio_decisao

    # Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
    async def executar(
        self, entrada: ConsultarDecisoesRecomendacaoEntrada
    ) -> tuple[DecisaoRecomendacao, ...]:
        """Devolve as decisões da versão do solicitante.

        O método trata versão ausente e versão de outro estudante como a mesma
        falha, antes de ler qualquer decisão. Ele existe para impedir a
        consulta das decisões de versões alheias.
        """
        curriculo = await self._repositorio_curriculo.obter_por_id(entrada.curriculo_id)
        if curriculo is None or curriculo.usuario_id != entrada.usuario_id:
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")
        return await self._repositorio_decisao.listar_por_curriculo(entrada.curriculo_id)
