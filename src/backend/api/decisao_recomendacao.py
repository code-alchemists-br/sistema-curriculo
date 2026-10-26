"""Expõe a decisão do estudante sobre recomendações da revisão por HTTP.

O módulo converte as identidades da rota e o corpo da requisição em entradas da
Application e traduz o resultado em DTOs públicos, sem expor entidades de
domínio. Ele existe para que o estudante aceite ou rejeite recomendações da
revisão de uma versão própria e consulte o que já decidiu.
"""

# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
from datetime import datetime
from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.application import (
    ConsultarDecisoesRecomendacaoEntrada,
    CurriculoNaoEncontrado,
    RecomendacaoNaoEncontrada,
    RegistrarDecisaoRecomendacaoEntrada,
)
from backend.domain import (
    CurriculoId,
    DecisaoEstudante,
    DecisaoRecomendacao,
    UsuarioId,
)

CAMINHO_DECISOES = "/estudantes/{usuario_id}/curriculos/{curriculo_id}/recomendacoes"
CAMINHO_DECISAO = CAMINHO_DECISOES + "/{codigo}"


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
class DecisaoRecomendacaoRequisicao(BaseModel):
    """Representa o JSON aceito para decidir sobre uma recomendação.

    O DTO aceita somente a decisão, limitada às opções do domínio (aceita ou
    rejeitada); versão e código vêm da rota. Ele existe para recusar já na
    fronteira uma decisão que não esteja no vocabulário.
    """

    decisao: DecisaoEstudante


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
class DecisaoRecomendacaoResposta(BaseModel):
    """Representa uma decisão do estudante como dado público.

    O DTO expõe o código da recomendação, a decisão em texto e o instante em que
    foi tomada, sem serializar o value object de domínio. Ele existe para manter
    a saída HTTP estável mesmo se a representação interna evoluir.
    """

    codigo: str
    decisao: str
    decidida_em: datetime


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
class DecisoesRecomendacaoResposta(BaseModel):
    """Representa as decisões de uma versão de currículo.

    O DTO reúne a lista de decisões, em ordem estável. Ele existe para que o
    cliente saiba, em uma resposta, o que já foi aceito ou rejeitado.
    """

    decisoes: list[DecisaoRecomendacaoResposta]


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
class RegistroDecisaoRecomendacaoExecutor(Protocol):
    """Define a capacidade de registrar a decisão que o router invoca.

    O contrato recebe a entrada da Application e devolve a decisão gravada, sem
    acoplar o handler a banco ou a implementação concreta. Ele existe para
    tornar a interface HTTP testável com doubles.
    """

    async def executar(
        self, entrada: RegistrarDecisaoRecomendacaoEntrada
    ) -> DecisaoRecomendacao:
        """Registra a decisão e a devolve.

        Implementações aplicam as regras de propriedade e de recomendação sem
        definir respostas HTTP. O método existe para que o router se concentre
        em traduzir fronteiras.
        """


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
class ConsultaDecisoesRecomendacaoExecutor(Protocol):
    """Define a capacidade de consultar as decisões que o router invoca.

    O contrato recebe a entrada da Application e devolve as decisões da versão,
    sem acoplar o handler a banco. Ele existe para tornar a interface HTTP
    testável com doubles.
    """

    async def executar(
        self, entrada: ConsultarDecisoesRecomendacaoEntrada
    ) -> tuple[DecisaoRecomendacao, ...]:
        """Devolve as decisões da versão do solicitante.

        Implementações aplicam a verificação de propriedade sem definir
        respostas HTTP. O método existe para que o router se concentre em
        traduzir fronteiras.
        """


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
def _para_resposta(decisao: DecisaoRecomendacao) -> DecisaoRecomendacaoResposta:
    """Converte uma decisão de domínio em DTO público.

    A função extrai o código, o texto da decisão e o instante. Ela existe para
    que o registro e a consulta montem a resposta do mesmo jeito.
    """
    return DecisaoRecomendacaoResposta(
        codigo=decisao.codigo,
        decisao=decisao.decisao.value,
        decidida_em=decisao.decidida_em,
    )


# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
def criar_router(
    registrar_decisao: RegistroDecisaoRecomendacaoExecutor | None,
    consultar_decisoes: ConsultaDecisoesRecomendacaoExecutor | None = None,
) -> APIRouter:
    """Cria as rotas de decisão sobre recomendações com os casos de uso injetados.

    A função registra o PUT que grava a decisão e o GET que lista as decisões da
    versão, convertendo identidades de rota em entradas da Application. Ela
    existe para registrar a API e permitir testes com doubles, sem sessão de
    banco real.

    Nota: as rotas ficam sob ``/estudantes/{usuario_id}/curriculos``, caminho que
    o middleware de autenticação já protege exigindo sessão ativa do próprio
    estudante; a verificação de propriedade da versão fica no caso de uso.
    """
    router = APIRouter()

    @router.put(
        CAMINHO_DECISAO,
        response_model=DecisaoRecomendacaoResposta,
        responses={
            404: {"description": "Versão ou recomendação não encontrada."},
            422: {"description": "Decisão fora das opções aceitas."},
            503: {"description": "Decisão indisponível."},
        },
    )
    async def decidir(
        usuario_id: UUID,
        curriculo_id: UUID,
        codigo: str,
        requisicao: DecisaoRecomendacaoRequisicao,
    ) -> DecisaoRecomendacaoResposta:
        """Registra a decisão do estudante sobre uma recomendação da versão.

        O handler monta a entrada da Application, aguarda o caso de uso e
        traduz versão ausente, versão alheia e recomendação inexistente em 404,
        sem distinguir os casos de versão. Ele existe para expor a decisão sem
        levar HTTP à Application.
        """
        if registrar_decisao is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Decisão indisponível.",
            )
        try:
            decisao = await registrar_decisao.executar(
                RegistrarDecisaoRecomendacaoEntrada(
                    usuario_id=UsuarioId(usuario_id),
                    curriculo_id=CurriculoId(curriculo_id),
                    codigo=codigo,
                    decisao=requisicao.decisao,
                )
            )
        except (CurriculoNaoEncontrado, RecomendacaoNaoEncontrada) as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
            ) from erro
        return _para_resposta(decisao)

    @router.get(
        CAMINHO_DECISOES,
        response_model=DecisoesRecomendacaoResposta,
        responses={
            404: {"description": "Versão de currículo não encontrada."},
            503: {"description": "Decisão indisponível."},
        },
    )
    async def listar(usuario_id: UUID, curriculo_id: UUID) -> DecisoesRecomendacaoResposta:
        """Lista as decisões do estudante sobre as recomendações da versão.

        O handler monta a entrada, aguarda o caso de uso e traduz versão ausente
        ou alheia em 404. Ele existe para que o cliente saiba o que já foi
        aceito ou rejeitado.
        """
        if consultar_decisoes is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Decisão indisponível.",
            )
        try:
            decisoes = await consultar_decisoes.executar(
                ConsultarDecisoesRecomendacaoEntrada(
                    usuario_id=UsuarioId(usuario_id),
                    curriculo_id=CurriculoId(curriculo_id),
                )
            )
        except CurriculoNaoEncontrado as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
            ) from erro
        return DecisoesRecomendacaoResposta(
            decisoes=[_para_resposta(decisao) for decisao in decisoes]
        )

    return router
