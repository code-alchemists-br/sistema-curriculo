"""Orquestra a criação de uma associação currículo-vaga.

O caso de uso verifica a propriedade do currículo, rejeita o par já existente,
constrói o agregado de domínio e solicita seu salvamento por uma porta dedicada.
Ele existe para expor a criação manual sem duplicar invariantes do Domain ou
acoplar o fluxo a API e persistência.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
from backend.application.ports import (
    RepositorioAssociacaoCurriculoVaga,
    RepositorioCurriculo,
)
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain.associacao_curriculo_vaga import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
)
from backend.domain.value_objects import CurriculoId, UsuarioId, VagaId


# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
class AssociacaoCurriculoVagaJaExiste(ValueError):
    """Sinaliza que o par currículo-vaga já está associado.

    A falha é produzida pela pré-checagem da Application e também pode ser
    levantada pelo adapter quando a constraint detectar uma corrida. Ela existe
    para rejeitar a criação duplicada sem alterar as classificações existentes.
    """


class AssociacaoCurriculoVagaNaoEncontrada(LookupError):
    """Sinaliza que o par currículo-vaga solicitado não está associado.

    A falha é produzida somente após a Application confirmar a propriedade do
    currículo. Ela existe para distinguir ausência de associação de currículo
    ausente/alheio sem criar a relação implicitamente.
    """


# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
@dataclass(frozen=True, slots=True)
class CriarAssociacaoCurriculoVagaEntrada:
    """Agrupa o ator autenticado e os dados necessários à associação inicial.

    A entrada recebe IDs tipados e classificações iniciais, sem identidade
    técnica de associação ou dados de transporte. Ela existe para expressar a
    intenção de criação e manter a Application independente da API.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId
    vaga_id: VagaId
    classificacoes: tuple[ClassificacaoAssociacao, ...]


# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
class CriarAssociacaoCurriculoVaga:
    """Cria e solicita o salvamento de uma associação válida.

    O caso consulta o currículo, verifica sua propriedade e a inexistência do
    par antes de construir o agregado existente e chamar o port de salvamento.
    Ele existe para garantir a criação única sem contornar a regra do Domain.
    """

    def __init__(
        self,
        repositorio_curriculo: RepositorioCurriculo,
        repositorio_associacao: RepositorioAssociacaoCurriculoVaga,
    ) -> None:
        """Recebe os ports necessários para ownership, duplicidade e persistência.

        O construtor armazena abstrações internas substituíveis por doubles. Ele
        existe para permitir que o caso de uso coordene o fluxo sem conhecer
        adapters concretos.
        """
        self._repositorio_curriculo = repositorio_curriculo
        self._repositorio_associacao = repositorio_associacao

    async def executar(
        self, entrada: CriarAssociacaoCurriculoVagaEntrada
    ) -> AssociacaoCurriculoVaga:
        """Valida o ator e cria a associação, devolvendo o agregado salvo.

        O método oculta currículo ausente ou alheio, rejeita duplicidade antes
        da construção, delega as invariantes ao agregado e só então solicita
        salvamento. Ele existe para impedir associações não autorizadas,
        duplicadas ou inválidas sem consultar serviço externo de vagas.
        """
        curriculo = await self._repositorio_curriculo.obter_por_id(entrada.curriculo_id)
        if curriculo is None or curriculo.usuario_id != entrada.usuario_id:
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")

        if await self._repositorio_associacao.existe_por_par(
            entrada.curriculo_id, entrada.vaga_id
        ):
            raise AssociacaoCurriculoVagaJaExiste(
                "Já existe uma associação para este currículo e esta vaga."
            )

        associacao = AssociacaoCurriculoVaga(
            curriculo_id=entrada.curriculo_id,
            vaga_id=entrada.vaga_id,
            classificacoes=entrada.classificacoes,
        )
        await self._repositorio_associacao.salvar(associacao)
        return associacao


@dataclass(frozen=True, slots=True)
class AlterarClassificacaoAssociacaoCurriculoVagaEntrada:
    """Agrupa identidade autenticada, associação e classificação solicitada.

    A entrada usa IDs tipados e uma única classificação, sem campo de transporte
    confiável para identidade. Ela existe para compartilhar o contrato das
    intenções explícitas de adicionar e remover.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId
    vaga_id: VagaId
    classificacao: ClassificacaoAssociacao


class AdicionarClassificacaoAssociacaoCurriculoVaga:
    """Adiciona uma classificação a uma associação existente do proprietário.

    O caso de uso valida ownership antes de carregar a associação, delega a
    transição ao agregado e solicita persistência somente quando há mudança.
    Ele existe para alterar classificações sem recriar a associação nem duplicar
    regras de domínio.
    """

    def __init__(
        self,
        repositorio_curriculo: RepositorioCurriculo,
        repositorio_associacao: RepositorioAssociacaoCurriculoVaga,
    ) -> None:
        """Armazena as portas necessárias à autorização e persistência.

        O construtor recebe abstrações substituíveis por doubles. Ele existe
        para manter o caso de uso independente dos adapters concretos.
        """
        self._repositorio_curriculo = repositorio_curriculo
        self._repositorio_associacao = repositorio_associacao

    async def executar(
        self, entrada: AlterarClassificacaoAssociacaoCurriculoVagaEntrada
    ) -> AssociacaoCurriculoVaga:
        """Adiciona a classificação e devolve o agregado resultante.

        O método valida propriedade, carrega a raiz sob proteção transacional,
        aplica a regra do Domain e persiste somente se o conjunto mudou. Ele
        existe para orquestrar a intenção sem expor estado de outro proprietário.
        """
        associacao = await _obter_associacao_do_proprietario(
            entrada, self._repositorio_curriculo, self._repositorio_associacao
        )
        if associacao.adicionar_classificacao(entrada.classificacao):
            await self._repositorio_associacao.atualizar_classificacoes(associacao)
        return associacao


class RemoverClassificacaoAssociacaoCurriculoVaga:
    """Remove uma classificação da associação existente do proprietário.

    O caso valida ownership antes da consulta, delega idempotência e invariantes
    ao agregado e persiste somente uma transição válida que mudou o estado. Ele
    existe para executar a intenção de remoção sem permitir associação inválida.
    """

    def __init__(
        self,
        repositorio_curriculo: RepositorioCurriculo,
        repositorio_associacao: RepositorioAssociacaoCurriculoVaga,
    ) -> None:
        """Armazena as portas necessárias à autorização e persistência.

        O construtor recebe abstrações substituíveis por doubles. Ele existe
        para manter o caso de uso independente dos adapters concretos.
        """
        self._repositorio_curriculo = repositorio_curriculo
        self._repositorio_associacao = repositorio_associacao

    async def executar(
        self, entrada: AlterarClassificacaoAssociacaoCurriculoVagaEntrada
    ) -> AssociacaoCurriculoVaga:
        """Remove a classificação e devolve o agregado resultante.

        O método valida propriedade, carrega a raiz sob proteção transacional,
        aplica as regras do Domain e persiste somente se o conjunto mudou. Ele
        existe para impedir que a remoção crie um estado inválido ou vaze dados.
        """
        associacao = await _obter_associacao_do_proprietario(
            entrada, self._repositorio_curriculo, self._repositorio_associacao
        )
        if associacao.remover_classificacao(entrada.classificacao):
            await self._repositorio_associacao.atualizar_classificacoes(associacao)
        return associacao


async def _obter_associacao_do_proprietario(
    entrada: AlterarClassificacaoAssociacaoCurriculoVagaEntrada,
    repositorio_curriculo: RepositorioCurriculo,
    repositorio_associacao: RepositorioAssociacaoCurriculoVaga,
) -> AssociacaoCurriculoVaga:
    """Carrega a associação após validar propriedade do currículo.

    A função consulta o currículo antes do repository de associação, oculta
    ausência e ownership alheio com `CurriculoNaoEncontrado` e exige que o par
    exista. Ela existe para centralizar a ordem segura comum às duas intenções.
    """
    curriculo = await repositorio_curriculo.obter_por_id(entrada.curriculo_id)
    if curriculo is None or curriculo.usuario_id != entrada.usuario_id:
        raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")

    associacao = await repositorio_associacao.obter_para_atualizacao(
        entrada.curriculo_id, entrada.vaga_id
    )
    if associacao is None:
        raise AssociacaoCurriculoVagaNaoEncontrada(
            "Associação currículo-vaga não encontrada."
        )
    return associacao
