"""Expõe um health check agregado sem detalhes internos das dependências."""

import asyncio
from collections.abc import Sequence

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.application.saude import VerificadorSaude

TEMPO_LIMITE_VERIFICACAO_SEGUNDOS = 2.0


def criar_router(verificadores: Sequence[VerificadorSaude] = ()) -> APIRouter:
    """Cria a rota pública de saúde com verificadores injetados.

    O router executa verificações assíncronas em paralelo, agrega somente o
    resultado geral e converte falhas ou timeout em HTTP 503. Ele existe para
    monitorar a disponibilidade sem revelar nomes, endereços ou erros internos.
    """
    router = APIRouter()
    verificadores_configurados = tuple(verificadores)

    @router.get(
        "/health",
        summary="Verifica a disponibilidade da aplicação",
        description=(
            "Retorna somente o estado agregado da aplicação e de suas "
            "dependências verificadas, sem expor detalhes internos."
        ),
        responses={503: {"description": "Aplicação ou dependência indisponível."}},
    )
    async def consultar_saude() -> JSONResponse:
        """Devolve estado agregado sem identificar dependências ou falhas.

        O handler executa os verificadores injetados com limite de tempo e
        responde apenas `ok` ou `indisponivel`. Ele existe para que monitores
        confirmem disponibilidade sem receber dados sensíveis da infraestrutura.
        """
        try:
            resultados = await asyncio.wait_for(
                asyncio.gather(
                    *(
                        verificador.verificar()
                        for verificador in verificadores_configurados
                    ),
                    return_exceptions=True,
                ),
                timeout=TEMPO_LIMITE_VERIFICACAO_SEGUNDOS,
            )
        except TimeoutError:
            return JSONResponse(
                status_code=503, content={"status": "indisponivel"}
            )

        if not all(resultado is True for resultado in resultados):
            return JSONResponse(status_code=503, content={"status": "indisponivel"})
        return JSONResponse(status_code=200, content={"status": "ok"})

    return router
