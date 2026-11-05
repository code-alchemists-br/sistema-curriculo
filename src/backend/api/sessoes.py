"""Expõe consulta e encerramento HTTP da sessão autenticada."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel

from backend.api.configuracao_cookie_sessao import (
    COOKIE_SESSAO_SEGURA,
    ConfiguracaoCookieSessao,
)
from backend.application.sessoes import RevogadorSessao

COOKIE_SESSAO = COOKIE_SESSAO_SEGURA


class SessaoAtualResposta(BaseModel):
    """Representa a identidade mínima associada à sessão HTTP válida.

    O DTO serializa somente o UUID instalado pelo middleware e não consulta ou
    revela credenciais. Ele existe para que clientes restaurem autenticação
    após recarregar a aplicação sem receber o token do cookie.
    """

    usuario_id: UUID


def criar_router(
    revogador_sessao: RevogadorSessao | None,
    configuracao_cookie: ConfiguracaoCookieSessao = ConfiguracaoCookieSessao(),
) -> APIRouter:
    """Cria rota de logout com revogador injetado pela composição externa.

    A rota lê somente o cookie de sessão, revoga seu registro se houver e
    remove o cookie com os atributos compatíveis com sua emissão. Também expõe
    a identidade já validada pelo middleware. Ela existe para permitir
    restauração de sessão e encerramento idempotente da sessão atual.
    """
    router = APIRouter()

    @router.get("/sessao/atual", response_model=SessaoAtualResposta)
    async def consultar_atual(requisicao: Request) -> SessaoAtualResposta:
        """Devolve a identidade instalada pelo middleware para a sessão válida.

        O handler lê somente o UUID que o middleware autenticado colocou no
        estado da requisição e responde 401 se a composição não o forneceu. Ele
        existe para expor a sessão atual sem consultar token ou banco novamente.
        """
        usuario_id = getattr(requisicao.state, "usuario_id", None)
        if not isinstance(usuario_id, UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Sessão ausente ou inválida.",
            )
        return SessaoAtualResposta(usuario_id=usuario_id)

    @router.delete("/sessao/atual", status_code=status.HTTP_204_NO_CONTENT)
    async def encerrar(
        resposta: Response,
        requisicao: Request,
    ) -> None:
        """Revoga a sessão do cookie, quando presente, e limpa o navegador.

        O handler delega o token ao serviço seguro, não distingue ausência,
        expiração ou desconhecimento e remove o cookie. Ele existe para tornar
        logout idempotente sem afetar outras sessões do estudante.
        """
        token = requisicao.cookies.get(configuracao_cookie.nome)
        if token is not None:
            if revogador_sessao is None:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Sessões indisponíveis.",
                )
            await revogador_sessao.revogar(token)
        resposta.delete_cookie(
            key=configuracao_cookie.nome,
            path="/",
            secure=configuracao_cookie.seguro,
            httponly=True,
            samesite="lax",
        )

    return router
