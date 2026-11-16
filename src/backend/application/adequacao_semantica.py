"""Orquestra a solicitação revisável de adequação de currículo a uma vaga.

O módulo confirma a propriedade da versão, reduz os itens profissionais que o
estudante selecionou conforme a política vigente e delega a geração a uma porta
interna. Ele existe para que a assistência de IA receba somente o contexto
autorizado e devolva uma proposta, sem conhecer HTTP, SDK, persistência ou
alterar o currículo.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

# Proveniência: decision-analysis prompts/backend/20261020-163820-adequacao-semantica-gpt-nano-v001.md#v001
from backend.application.politica_limites_contexto_ia import (
    FontePoliticaLimitesContextoIa,
    LimitesContextoIa,
)
from backend.application.ports import ConsultaItemPerfil, RepositorioCurriculo
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain.adequacao_semantica import (
    AcaoAdequacaoSemantica,
    ItemSelecionadoAdequacao,
    PropostaAdequacaoCurriculoVaga,
    SolicitacaoAdequacaoCurriculoVaga,
    SolicitacaoAssistenciaCurriculo,
    SugestaoAdequacao,
)
from backend.domain.itens_perfil import (
    Competencia,
    ExperienciaProfissional,
    ProjetoAcademico,
)
from backend.domain.value_objects import CurriculoId, ReferenciaCurriculo, UsuarioId


class ItemAdequacaoNaoEncontrado(LookupError):
    """Indica referência ausente, alheia ou inelegível para a adequação.

    A falha agrupa estados que não devem revelar dados de outros estudantes e
    itens que não pertencem ao contexto profissional permitido. Ela existe para
    que a borda traduza a recusa sem expor qual condição ocorreu.
    """


class GeracaoPropostaAdequacaoIndisponivel(RuntimeError):
    """Indica que o gerador não conseguiu produzir uma proposta revisável.

    A exceção abstrai indisponibilidade, falhas de transporte e respostas
    inválidas de um provedor externo, sem carregar seus detalhes. Ela existe
    para que a API comunique indisponibilidade com segurança sem a Application
    depender de uma tecnologia concreta de IA.
    """


@dataclass(frozen=True, slots=True)
class SolicitarAdequacaoCurriculoVagaEntrada:
    """Reúne ator, vaga, consentimento e itens autorizados para a assistência.

    A entrada carrega apenas conceitos da aplicação e do domínio, preservando a
    ordem declarada pelo estudante para reduzir o contexto de modo reproduzível.
    Ela existe para expressar a intenção sem depender de um formato HTTP.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId
    cargo_alvo: str
    descricao_vaga: str | None
    referencias_selecionadas: tuple[ReferenciaCurriculo, ...]
    consentimento_explicito: bool


@dataclass(frozen=True, slots=True)
class ContextoAdequacaoCurriculoVaga:
    """Representa o contexto mínimo que pode ser entregue ao gerador interno.

    O modelo mantém somente a vaga limitada, os itens já reduzidos e metadados
    da política resolvida, sem contatos, documentos ou dados de transporte. Ele
    existe para tornar a fronteira com o gerador auditável e substituível.
    """

    curriculo_id: CurriculoId
    cargo_alvo: str
    descricao_vaga: str | None
    itens_selecionados: tuple[ItemSelecionadoAdequacao, ...]
    modelo: str
    versao_politica: str
    limites: LimitesContextoIa


# Proveniência: decision-analysis prompts/backend/20261105-181751-adequacao-semantica-gpt-nano-v005.md#v005
@dataclass(frozen=True, slots=True)
class PreparacaoContextoAssistenciaCurriculo:
    """Agrupa solicitação validada e contexto reduzido para uma ação de IA.

    O modelo conserva a solicitação que comprovou consentimento e o contexto
    limitado correspondente, sem depender do tipo de resposta que será gerado.
    Ele existe para reutilizar as mesmas salvaguardas em adequação e recomendação.
    """

    solicitacao: SolicitacaoAssistenciaCurriculo
    contexto: ContextoAdequacaoCurriculoVaga


class GeradorPropostaAdequacao(Protocol):
    """Define a geração de sugestões sem escolher provedor ou transporte.

    A porta recebe somente o contexto já autorizado e limitado e devolve
    sugestões tipadas que o domínio ainda validará. Ela existe para permitir um
    adapter de IA ou um double de teste sem acoplar o caso de uso a SDK ou HTTP.
    """

    async def gerar(
        self, contexto: ContextoAdequacaoCurriculoVaga
    ) -> tuple[SugestaoAdequacao, ...]:
        """Solicita sugestões para o contexto reduzido e rastreável.

        A implementação concreta pode chamar um provedor, mas preserva o
        contrato tipado de retorno sem mutar o currículo. Isso existe para que a
        orquestração mantenha a revisão pelo estudante como etapa posterior.
        """


# Proveniência: decision-analysis prompts/backend/20261105-181751-adequacao-semantica-gpt-nano-v005.md#v005
class PreparadorContextoAssistenciaCurriculo:
    """Prepara contexto profissional autorizado para uma ação interna de IA.

    O preparador verifica propriedade, resolve limites por ação, materializa só
    itens permitidos e cria a solicitação que valida consentimento. Ele existe
    para evitar que adequação e recomendação divirjam na proteção do contexto.
    """

    def __init__(
        self,
        repositorio_curriculo: RepositorioCurriculo,
        consulta_item: ConsultaItemPerfil,
        fonte_politica: FontePoliticaLimitesContextoIa,
        modelo: str,
        acao: AcaoAdequacaoSemantica,
    ) -> None:
        """Recebe portas internas e a intenção que seleciona a política efetiva.

        O construtor guarda somente abstrações e valida identificador e ação
        tipados antes do fluxo assíncrono. Ele existe para tornar o preparo
        reutilizável sem conhecer provedor, transporte ou persistência concreta.
        """
        if not isinstance(modelo, str) or not modelo.strip():
            raise ValueError("O modelo de assistência deve ser informado.")
        if not isinstance(acao, AcaoAdequacaoSemantica):
            raise ValueError("A ação de assistência deve ser reconhecida.")
        self._repositorio_curriculo = repositorio_curriculo
        self._consulta_item = consulta_item
        self._fonte_politica = fonte_politica
        self._modelo = modelo.strip()
        self._acao = acao

    async def preparar(
        self, entrada: SolicitarAdequacaoCurriculoVagaEntrada
    ) -> PreparacaoContextoAssistenciaCurriculo:
        """Valida a entrada e devolve somente o contexto autorizado e limitado.

        O método oculta versão alheia, aplica a política da ação, reduz campos e
        itens e deixa o domínio exigir consentimento explícito. Ele existe para
        garantir uma fronteira de dados idêntica para todas as intenções de IA.
        """
        curriculo = await self._repositorio_curriculo.obter_por_id(entrada.curriculo_id)
        if curriculo is None or curriculo.usuario_id != entrada.usuario_id:
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")
        politica = self._fonte_politica.obter()
        limites = politica.resolver(self._acao.value, self._modelo)
        descricao_vaga = _limitar_texto(
            entrada.descricao_vaga, limites.limites_campos["descricao_vaga"]
        )
        itens = await self._materializar_itens(entrada, curriculo.referencias, limites)
        solicitacao = SolicitacaoAssistenciaCurriculo(
            curriculo_id=entrada.curriculo_id,
            cargo_alvo=_limitar_texto(
                entrada.cargo_alvo, limites.limites_campos["cargo"]
            ),
            descricao_vaga=descricao_vaga,
            itens_selecionados=itens,
            consentimento_explicito=entrada.consentimento_explicito,
            acao=self._acao,
        )
        contexto = ContextoAdequacaoCurriculoVaga(
            curriculo_id=entrada.curriculo_id,
            cargo_alvo=solicitacao.cargo_alvo,
            descricao_vaga=solicitacao.descricao_vaga,
            itens_selecionados=solicitacao.itens_selecionados,
            modelo=self._modelo,
            versao_politica=politica.versao,
            limites=limites,
        )
        return PreparacaoContextoAssistenciaCurriculo(solicitacao, contexto)

    async def _materializar_itens(
        self,
        entrada: SolicitarAdequacaoCurriculoVagaEntrada,
        referencias_do_curriculo: frozenset[ReferenciaCurriculo],
        limites: LimitesContextoIa,
    ) -> tuple[ItemSelecionadoAdequacao, ...]:
        """Lê e reduz itens selecionados sem ultrapassar o orçamento permitido.

        O método respeita ordem, propriedade e pertencimento à versão antes de
        cortar conteúdos ao orçamento restante. Ele existe para impedir que uma
        ação de IA amplie o contexto autorizado pelo estudante.
        """
        if len(set(entrada.referencias_selecionadas)) != len(
            entrada.referencias_selecionadas
        ):
            raise ItemAdequacaoNaoEncontrado("Item do perfil não encontrado.")
        restantes = limites.orcamento_total_caracteres - len(entrada.cargo_alvo)
        if entrada.descricao_vaga is not None:
            restantes -= len(
                _limitar_texto(
                    entrada.descricao_vaga, limites.limites_campos["descricao_vaga"]
                )
            )
        itens: list[ItemSelecionadoAdequacao] = []
        for referencia in entrada.referencias_selecionadas:
            if referencia not in referencias_do_curriculo:
                raise ItemAdequacaoNaoEncontrado("Item do perfil não encontrado.")
            item = await self._consulta_item.obter_item(referencia)
            conteudo = _conteudo_permitido(
                item, entrada.usuario_id, referencia, limites
            )
            if conteudo is None:
                raise ItemAdequacaoNaoEncontrado("Item do perfil não encontrado.")
            if restantes <= 0:
                break
            conteudo = conteudo[:restantes].strip()
            if not conteudo:
                break
            itens.append(
                ItemSelecionadoAdequacao(referencia=referencia, conteudo=conteudo)
            )
            restantes -= len(conteudo)
        return tuple(itens)


class SolicitarAdequacaoCurriculoVaga:
    """Solicita uma proposta de adequação para uma versão própria de currículo.

    O caso verifica propriedade e seleção, materializa apenas experiências,
    projetos e competências próprios, aplica a política e chama uma porta de
    geração. Ele existe para bloquear envio não consentido ou excessivo antes
    de qualquer integração externa e nunca persiste a proposta como edição.
    """

    def __init__(
        self,
        repositorio_curriculo: RepositorioCurriculo,
        consulta_item: ConsultaItemPerfil,
        fonte_politica: FontePoliticaLimitesContextoIa,
        gerador: GeradorPropostaAdequacao,
        modelo: str,
    ) -> None:
        """Armazena as portas e o modelo configurado para a assistência.

        O construtor recebe somente abstrações internas e exige o identificador
        não vazio do modelo antes de executar qualquer fluxo. Ele existe para
        manter a troca de provedor e os testes independente da composição
        externa.
        """
        if not isinstance(modelo, str) or not modelo.strip():
            raise ValueError("O modelo de adequação deve ser informado.")
        self._preparador = PreparadorContextoAssistenciaCurriculo(
            repositorio_curriculo,
            consulta_item,
            fonte_politica,
            modelo,
            AcaoAdequacaoSemantica.ADEQUAR_CURRICULO_VAGA,
        )
        self._gerador = gerador
        self._modelo = modelo.strip()

    async def executar(
        self, entrada: SolicitarAdequacaoCurriculoVagaEntrada
    ) -> PropostaAdequacaoCurriculoVaga:
        """Gera uma proposta revisável sem alterar a versão de currículo.

        O método oculta currículo alheio, confirma cada referência previamente
        selecionada, reduz textos conforme os limites e só então chama a porta
        com consentimento explícito validado pelo domínio. Ele existe para que
        todo dado enviado ao gerador seja mínimo, rastreável e autorizado.
        """
        preparacao = await self._preparador.preparar(entrada)
        sugestoes = await self._gerador.gerar(preparacao.contexto)
        solicitacao = SolicitacaoAdequacaoCurriculoVaga(
            curriculo_id=preparacao.solicitacao.curriculo_id,
            cargo_alvo=preparacao.solicitacao.cargo_alvo,
            descricao_vaga=preparacao.solicitacao.descricao_vaga,
            itens_selecionados=preparacao.solicitacao.itens_selecionados,
            consentimento_explicito=preparacao.solicitacao.consentimento_explicito,
        )
        return solicitacao.criar_proposta(
            modelo=self._modelo,
            versao_politica=preparacao.contexto.versao_politica,
            sugestoes=sugestoes,
        )


def _limitar_texto(valor: str | None, limite: int) -> str | None:
    """Reduz um texto opcional ao limite configurado preservando sua ausência.

    A função deixa a validação de texto obrigatório para o domínio, mas aplica
    o corte determinístico aos campos que podem chegar ao gerador. Ela existe
    para impedir que um valor de entrada aumente o contexto além da política.
    """
    if valor is None:
        return None
    return valor[:limite].strip()


def _conteudo_permitido(
    item: object | None,
    usuario_id: UsuarioId,
    referencia: ReferenciaCurriculo,
    limites: LimitesContextoIa,
) -> str | None:
    """Projeta apenas campos profissionais permitidos de um item próprio.

    A função confere identidade e proprietário antes de serializar experiências,
    projetos ou competências, aplicando limites por campo conhecidos. Ela existe
    para excluir contatos, documentos e quaisquer tipos sem relação direta com
    a adequação da vaga.
    """
    if (
        item is None
        or getattr(item, "usuario_id", None) != usuario_id
        or getattr(item, "id", None) != referencia.item_id
    ):
        return None
    if isinstance(item, ExperienciaProfissional):
        return "\n".join(
            (
                f"Empresa: {_limitar_texto(item.empresa, limites.limites_campos['empresa'])}",
                f"Cargo: {_limitar_texto(item.cargo, limites.limites_campos['cargo'])}",
                f"Descrição: {_limitar_texto(item.descricao, limites.limites_campos['descricao_experiencia'])}",
            )
        )
    if isinstance(item, ProjetoAcademico):
        return f"Projeto: {item.titulo}\nDescrição: {item.descricao}\nTecnologias: {item.tecnologias}"
    if isinstance(item, Competencia):
        return "\n".join(
            (
                f"Competência: {_limitar_texto(item.descricao, limites.limites_campos['descricao_competencia'])}",
                f"Nível: {_limitar_texto(item.nivel, limites.limites_campos['nivel_competencia'])}",
            )
        )
    return None
