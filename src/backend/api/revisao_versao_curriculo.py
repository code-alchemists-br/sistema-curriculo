"""Expõe DTOs e o handler HTTP da revisão de campos obrigatórios do currículo.

O módulo converte as identidades de rota em entrada da Application e traduz o
resultado da revisão em DTOs públicos, sem expor entidades de domínio. Ele
existe para manter transporte e apresentação de dados fora das regras de domínio
e do caso de uso de revisão.
"""

# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.application import CurriculoNaoEncontrado, RevisarVersaoCurriculoEntrada
from backend.domain import CurriculoId, ResultadoRevisao, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
class RevisaoVersaoCurriculoExecutor(Protocol):
    """Define a capacidade de revisar uma versão de currículo que o router invoca.

    O contrato recebe a entrada da Application e devolve o resultado da revisão,
    sem acoplar o handler a banco ou implementação concreta. Ele existe para
    tornar a interface HTTP testável com doubles que exercitam a mesma intenção
    do caso de uso real.
    """

    # Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
    async def executar(
        self, entrada: RevisarVersaoCurriculoEntrada
    ) -> ResultadoRevisao:
        """Executa a revisão interna e devolve as pendências encontradas.

        Implementações aplicam as regras de propriedade e de completude sem
        definir respostas HTTP. O método existe para que o router se concentre
        em traduzir fronteiras.
        """


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
class PendenciaRevisaoResposta(BaseModel):
    """Representa uma pendência da revisão como dado público.

    O DTO expõe código, seção, mensagem e severidade como texto, sem serializar
    as enumerações do domínio. Ele existe para manter a saída HTTP estável mesmo
    se a representação interna evoluir.
    """

    codigo: str
    secao: str
    mensagem: str
    severidade: str


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
class RevisaoVersaoCurriculoResposta(BaseModel):
    """Representa o resultado da revisão de uma versão de currículo.

    O DTO reúne o veredito e a lista de pendências, já em ordem. Ele existe para
    que o cliente saiba se a versão está aprovada e o que corrigir, em uma única
    resposta.
    """

    aprovado: bool
    pendencias: list[PendenciaRevisaoResposta]


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
def criar_router(revisar_versao: RevisaoVersaoCurriculoExecutor | None) -> APIRouter:
    """Cria a rota HTTP de revisão usando o caso de uso injetado.

    A função converte as identidades de rota em entrada da Application e monta a
    resposta pública a partir do resultado. Ela existe para registrar a API e
    permitir testes unitários com doubles, sem sessão de banco real.

    Nota: a rota fica sob ``/estudantes/{usuario_id}/curriculos``, caminho que o
    middleware de autenticação, quando instalado, já protege exigindo sessão
    ativa do próprio estudante; a verificação de propriedade da versão continua
    no caso de uso, conforme
    prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md.
    """
    router = APIRouter()

    @router.get(
        "/estudantes/{usuario_id}/curriculos/{curriculo_id}/revisao",
        response_model=RevisaoVersaoCurriculoResposta,
    )
    async def revisar(
        usuario_id: UUID, curriculo_id: UUID
    ) -> RevisaoVersaoCurriculoResposta:
        """Executa a revisão HTTP e devolve o veredito e as pendências.

        O handler monta a entrada da Application a partir da rota, aguarda o caso
        de uso e traduz a ausência ou a propriedade alheia da versão, sem
        distinguir os dois casos. Ele existe para expor a revisão sem levar HTTP
        à Application.
        """
        if revisar_versao is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Revisão indisponível.",
            )
        entrada = RevisarVersaoCurriculoEntrada(
            usuario_id=UsuarioId(usuario_id),
            curriculo_id=CurriculoId(curriculo_id),
        )
        try:
            resultado = await revisar_versao.executar(entrada)
        except CurriculoNaoEncontrado as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
            ) from erro
        return RevisaoVersaoCurriculoResposta(
            aprovado=resultado.aprovado,
            pendencias=[
                PendenciaRevisaoResposta(
                    codigo=pendencia.codigo,
                    secao=pendencia.secao.value,
                    mensagem=pendencia.mensagem,
                    severidade=pendencia.severidade.value,
                )
                for pendencia in resultado.pendencias
            ],
        )

    return router