"""Expõe a solicitação revisável de adequação de currículo a uma vaga.

O módulo converte o contrato HTTP mínimo em uma entrada da Application e
apresenta a proposta sem serializar entidades de domínio. Ele existe para
preservar a identidade de sessão, o consentimento e a revisão humana na
fronteira pública da assistência de IA.
"""

from typing import Literal, Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict

from backend.application import (
    CurriculoNaoEncontrado,
    GeracaoPropostaAdequacaoIndisponivel,
    ItemAdequacaoNaoEncontrado,
    SolicitarAdequacaoCurriculoVagaEntrada,
)
from backend.domain import (
    CompetenciaId,
    CurriculoId,
    ExperienciaProfissionalId,
    ProjetoAcademicoId,
    PropostaAdequacaoCurriculoVaga,
    ReferenciaCurriculo,
    RegraDeDominioViolada,
    UsuarioId,
)

TipoReferenciaAdequacao = Literal["experiencia", "projeto", "competencia"]

_CLASSES_ID_POR_TIPO = {
    "experiencia": ExperienciaProfissionalId,
    "projeto": ProjetoAcademicoId,
    "competencia": CompetenciaId,
}
_TIPOS_POR_CLASSE = {classe: tipo for tipo, classe in _CLASSES_ID_POR_TIPO.items()}


class ReferenciaAdequacaoRequisicao(BaseModel):
    """Representa um item profissional escolhido para entrar no contexto.

    O DTO limita o tipo aos três itens que a Application consegue materializar
    e recebe apenas seu UUID, sem conteúdo ou proprietário. Ele existe para
    impedir que o cliente envie currículo livre ou aponte para tipos vedados.
    """

    model_config = ConfigDict(extra="ignore")

    tipo: TipoReferenciaAdequacao
    id: UUID


class SolicitarAdequacaoCurriculoVagaRequisicao(BaseModel):
    """Define o corpo mínimo da solicitação de adequação semântica.

    O DTO recebe alvo, vaga opcional, seleção ordenada e consentimento, ignorando
    campos desconhecidos conforme a convenção da API. Ele existe para manter
    identidade, modelo e conteúdos profissionais fora da entrada HTTP.
    """

    model_config = ConfigDict(extra="ignore")

    cargo_alvo: str
    descricao_vaga: str | None = None
    referencias_selecionadas: list[ReferenciaAdequacaoRequisicao]
    consentimento_explicito: bool


class ReferenciaAdequacaoResposta(BaseModel):
    """Apresenta uma referência profissional usada ou afetada pela proposta.

    O DTO converte a referência tipada para tipo textual e UUID, sem expor o
    value object interno. Ele existe para o cliente relacionar cada sugestão ao
    item selecionado em sua própria interface de revisão.
    """

    tipo: TipoReferenciaAdequacao
    id: UUID


class SugestaoAdequacaoResposta(BaseModel):
    """Representa uma sugestão revisável devolvida pelo caso de uso.

    O DTO expõe o texto e sua justificativa, com referência opcional, sem
    oferecer operação de aplicação automática. Ele existe para o estudante
    aceitar, editar ou descartar a proposta de forma granular.
    """

    codigo: str
    tipo: str
    referencia_item: ReferenciaAdequacaoResposta | None
    texto_sugerido: str
    justificativa: str


class PropostaAdequacaoCurriculoVagaResposta(BaseModel):
    """Define a forma pública de uma proposta de adequação ainda não aplicada.

    O DTO expõe modelo, política, itens efetivamente utilizados e sugestões,
    omitindo o currículo já identificado pela rota. Ele existe para estabilizar
    a resposta HTTP sem expor a entidade de domínio nem detalhes do provedor.
    """

    modelo: str
    versao_politica: str
    referencias_utilizadas: list[ReferenciaAdequacaoResposta]
    sugestoes: list[SugestaoAdequacaoResposta]


class SolicitarAdequacaoCurriculoVagaExecutor(Protocol):
    """Define a capacidade de gerar uma proposta que o router consome.

    O contrato recebe a entrada tipada da Application e devolve uma proposta
    revisável, sem revelar adaptadores externos à API. Ele existe para permitir
    composição e testes isolados do transporte HTTP.
    """

    async def executar(
        self, entrada: SolicitarAdequacaoCurriculoVagaEntrada
    ) -> PropostaAdequacaoCurriculoVaga:
        """Gera a proposta correspondente à solicitação autorizada.

        Implementações validam propriedade, consentimento e contexto antes de
        chamar o gerador configurado. O método existe para deixar a rota focada
        apenas na tradução segura de HTTP.
        """


def _para_referencia(requisicao: ReferenciaAdequacaoRequisicao) -> ReferenciaCurriculo:
    """Converte uma referência pública no value object usado pela Application.

    A função seleciona a classe de identificador a partir do tipo já validado
    pelo DTO e cria a referência tipada. Ela existe para impedir que textos ou
    UUIDs soltos atravessem a fronteira de transporte.
    """
    return ReferenciaCurriculo(_CLASSES_ID_POR_TIPO[requisicao.tipo](requisicao.id))


def _para_resposta_referencia(
    referencia: ReferenciaCurriculo,
) -> ReferenciaAdequacaoResposta:
    """Converte a referência tipada do domínio na representação HTTP estável.

    A função reconhece apenas os três tipos profissionais que participam da
    adequação e extrai seu UUID. Ela existe para que a resposta não serialize
    value objects nem exponha tipos fora do contrato público.
    """
    tipo = _TIPOS_POR_CLASSE.get(type(referencia.item_id))
    if tipo is None:
        raise ValueError("Tipo de referência de adequação não suportado.")
    return ReferenciaAdequacaoResposta(tipo=tipo, id=referencia.item_id.valor)


def _para_resposta(
    proposta: PropostaAdequacaoCurriculoVaga,
) -> PropostaAdequacaoCurriculoVagaResposta:
    """Apresenta a proposta de domínio como resposta sem efeito de persistência.

    A função projeta explicitamente cada sugestão e referência usada, mantendo
    a proposta como informação para revisão. Ela existe para desacoplar o
    contrato HTTP da estrutura imutável usada no domínio.
    """
    return PropostaAdequacaoCurriculoVagaResposta(
        modelo=proposta.modelo,
        versao_politica=proposta.versao_politica,
        referencias_utilizadas=[
            _para_resposta_referencia(referencia)
            for referencia in proposta.referencias_utilizadas
        ],
        sugestoes=[
            SugestaoAdequacaoResposta(
                codigo=sugestao.codigo,
                tipo=sugestao.tipo.value,
                referencia_item=(
                    _para_resposta_referencia(sugestao.referencia_item)
                    if sugestao.referencia_item is not None
                    else None
                ),
                texto_sugerido=sugestao.texto_sugerido,
                justificativa=sugestao.justificativa,
            )
            for sugestao in proposta.sugestoes
        ],
    )


def criar_router(
    solicitar_adequacao: SolicitarAdequacaoCurriculoVagaExecutor | None,
) -> APIRouter:
    """Cria a rota autenticada que solicita uma proposta de adequação.

    O handler deriva o estudante da sessão, converte apenas os campos públicos
    do corpo e traduz falhas conhecidas em respostas seguras. Ele existe para
    expor a assistência sem deixar HTTP, identidade ou detalhes do provedor
    alcançar a Application.
    """
    router = APIRouter()

    @router.post(
        "/curriculos/{curriculo_id}/adequacoes-semanticas",
        response_model=PropostaAdequacaoCurriculoVagaResposta,
        status_code=status.HTTP_200_OK,
        responses={
            401: {"description": "Autenticação necessária."},
            404: {"description": "Versão ou item não encontrado."},
            422: {"description": "Dados da adequação inválidos."},
            503: {"description": "Adequação semântica indisponível."},
        },
    )
    async def solicitar(
        curriculo_id: UUID,
        requisicao: SolicitarAdequacaoCurriculoVagaRequisicao,
        request: Request,
    ) -> PropostaAdequacaoCurriculoVagaResposta:
        """Gera uma proposta revisável para a versão própria autenticada.

        O handler exige executor e principal de sessão, monta a entrada sem
        dados livres do currículo e converte ausências, invariantes e falhas de
        geração em códigos públicos. Ele existe para garantir que a proposta
        nunca seja uma edição automática nem revele detalhes operacionais.
        """
        if solicitar_adequacao is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Adequação semântica indisponível.",
            )
        usuario_id = getattr(request.state, "usuario_id", None)
        if not isinstance(usuario_id, UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária.",
            )
        entrada = SolicitarAdequacaoCurriculoVagaEntrada(
            usuario_id=UsuarioId(usuario_id),
            curriculo_id=CurriculoId(curriculo_id),
            cargo_alvo=requisicao.cargo_alvo,
            descricao_vaga=requisicao.descricao_vaga,
            referencias_selecionadas=tuple(
                _para_referencia(referencia)
                for referencia in requisicao.referencias_selecionadas
            ),
            consentimento_explicito=requisicao.consentimento_explicito,
        )
        try:
            proposta = await solicitar_adequacao.executar(entrada)
        except (CurriculoNaoEncontrado, ItemAdequacaoNaoEncontrado) as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Versão ou item não encontrado.",
            ) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Dados da adequação inválidos.",
            ) from erro
        except GeracaoPropostaAdequacaoIndisponivel as erro:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Adequação semântica indisponível.",
            ) from erro
        return _para_resposta(proposta)

    return router
