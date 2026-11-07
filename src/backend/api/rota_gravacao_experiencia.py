"""Traduz falhas de validação das gravações sem refletir os dados recebidos.

Limita o tratamento às rotas POST/PUT do router de experiências para manter
422 seguro sem mudar handlers globais ou a validação de outros recursos.
"""

# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from pydantic import BaseModel


class ErroGravacaoExperienciaResposta(BaseModel):
    """Documenta o detalhe público dos erros 422 de gravação de experiências.

    Expõe somente uma mensagem textual para refletir a tradução local sem
    incluir o input ou o contexto bruto do validador na resposta do contrato.
    """

    detail: str


class RotaGravacaoExperiencia(APIRoute):
    """Adapta falhas de desserialização de experiências para um 422 genérico.

    Envolve somente POST e PUT e descarta detalhes com inputs/contextos para
    impedir exposição de textos ou dados pessoais sem alterar GET e DELETE.
    """

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        """Envolve o handler do framework para traduzir falhas de entrada.

        Delega execução e validação ao handler original e converte somente
        RequestValidationError nas gravações, sem logar o conteúdo rejeitado,
        para preservar o status e impedir reflexo de dados na resposta pública.
        """
        handler = super().get_route_handler()
        if not self.methods or not self.methods.intersection({"POST", "PUT"}):
            return handler

        async def executar(request: Request) -> Response:
            """Delega ao handler original e sanitiza somente erros de entrada.

            Traduz a exceção do framework em HTTP 422 com mensagem constante
            para impedir que corpo, input ou contexto de validação sejam expostos.
            """
            try:
                return await handler(request)
            except RequestValidationError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Dados da experiência inválidos.",
                ) from None

        return executar
