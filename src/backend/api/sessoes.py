"""Expoe o encerramento HTTP de uma sessão autenticada."""

from fastapi import APIRouter, Cookie, HTTPException, Response, status

from backend.application.sessoes import RevogadorSessao

COOKIE_SESSAO = "__Host-sessao"


def criar_router(revogador_sessao: RevogadorSessao | None) -> APIRouter:
    """Cria rota de logout com revogador injetado pela composição externa.

    A rota lê somente o cookie de sessão, revoga seu registro se houver e
    remove o cookie com os atributos compatíveis com sua emissão. Ela existe
    para oferecer encerramento idempotente da sessão atual.
    """
    router = APIRouter()

    @router.delete("/sessao/atual", status_code=status.HTTP_204_NO_CONTENT)
    async def encerrar(
        resposta: Response,
        token: str | None = Cookie(default=None, alias=COOKIE_SESSAO),
    ) -> None:
        """Revoga a sessão do cookie, quando presente, e limpa o navegador.

        O handler delega o token ao serviço seguro, não distingue ausência,
        expiração ou desconhecimento e remove o cookie. Ele existe para tornar
        logout idempotente sem afetar outras sessões do estudante.
        """
        if token is not None:
            if revogador_sessao is None:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Sessões indisponíveis.",
                )
            await revogador_sessao.revogar(token)
        resposta.delete_cookie(
            key=COOKIE_SESSAO,
            path="/",
            secure=True,
            httponly=True,
            samesite="lax",
        )

    return router
