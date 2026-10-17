"""Expõe um health check agregado sem detalhes internos das dependências."""

import asyncio
from collections.abc import Sequence

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.application.saude import VerificadorPersistencia, VerificadorSaude

TEMPO_LIMITE_VERIFICACAO_SEGUNDOS = 2.0


def criar_router(
    verificadores: Sequence[VerificadorSaude] = (),
    verificador_persistencia: VerificadorPersistencia | None = None,
) -> APIRouter:
    """Cria rotas públicas de saúde e prontidão com probes injetados.

    Health agrega verificações gerais; readiness exige um probe de persistência.
    Ambas as rotas limitam o tempo de espera e retornam estado genérico. O
    router existe para monitorar disponibilidade sem revelar detalhes internos.
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

    @router.get(
        "/ready",
        summary="Verifica se a aplicação está pronta para receber tráfego",
        description=(
            "A prontidão depende da disponibilidade da persistência e não "
            "expõe detalhes da conexão ou do erro."
        ),
        responses={503: {"description": "Persistência indisponível ou não configurada."}},
    )
    async def consultar_prontidao() -> JSONResponse:
        """Indica prontidão somente quando a persistência responde com sucesso.

        O handler exige um verificador injetado, aguarda seu resultado com
        timeout e converte ausência, falha ou exceção em HTTP 503 sem detalhes.
        Ele existe para impedir tráfego quando o armazenamento não está pronto.
        """
        if verificador_persistencia is None:
            return JSONResponse(
                status_code=503, content={"status": "indisponivel"}
            )

        try:
            disponivel = await asyncio.wait_for(
                verificador_persistencia.verificar(),
                timeout=TEMPO_LIMITE_VERIFICACAO_SEGUNDOS,
            )
        except Exception:
            return JSONResponse(
                status_code=503, content={"status": "indisponivel"}
            )

        if disponivel is not True:
            return JSONResponse(status_code=503, content={"status": "indisponivel"})
        return JSONResponse(status_code=200, content={"status": "ok"})

    return router
