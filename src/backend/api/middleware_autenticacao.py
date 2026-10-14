"""Autentica requisições usando a sessão persistida no cookie seguro."""

from uuid import UUID

from fastapi import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.api.sessoes import COOKIE_SESSAO
from backend.application.autenticacao_sessao import AutenticadorSessao

DETALHE_NAO_AUTENTICADO = "Sessão ausente ou inválida."

ROTAS_PUBLICAS = frozenset(
    {
        ("POST", "/estudantes"),
        ("POST", "/acessos"),
        ("DELETE", "/sessao/atual"),
        ("GET", "/docs"),
        ("GET", "/docs/oauth2-redirect"),
        ("GET", "/openapi.json"),
        ("GET", "/redoc"),
        # Proveniência: decision-analysis prompts/backend/20261014-175641-health-readiness-checks-v001.md#v001
        ("GET", "/health"),
        ("GET", "/ready"),
    }
)


class MiddlewareAutenticacaoSessao(BaseHTTPMiddleware):
    """Exige sessão ativa nas rotas privadas e associa a identidade validada.

    O middleware libera login, cadastro, logout e documentação; nas demais
    rotas valida o cookie por meio da porta injetada e grava o `UsuarioId` em
    `request.state.usuario_id`. Nas rotas de perfil e currículo, exige que o
    UUID da rota corresponda ao estudante autenticado. Ele existe para
    centralizar autenticação e proteger recursos privados do próprio estudante.
    """

    def __init__(self, app, autenticador: AutenticadorSessao) -> None:
        """Recebe a aplicação ASGI e o serviço de validação de sessão.

        A dependência interna impede acesso direto ao ORM na borda HTTP. Ela
        existe para compor a autenticação sem acoplar a API à infraestrutura.
        """
        super().__init__(app)
        self._autenticador = autenticador

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Valida cookie nas rotas privadas antes de encaminhar a requisição.

        O método ignora preflight e caminhos explicitamente públicos; nos demais
        exige token ativo e expõe a identidade validada em `request.state`.
        Ele existe para negar operações sem sessão válida.
        """
        if request.method == "OPTIONS" or (request.method, request.url.path) in ROTAS_PUBLICAS:
            return await call_next(request)

        token = request.cookies.get(COOKIE_SESSAO)
        if token is None:
            return _resposta_nao_autenticada()

        usuario_id = await self._autenticador.autenticar(token)
        if usuario_id is None:
            return _resposta_nao_autenticada()

        request.state.usuario_id = usuario_id.valor
        usuario_requisitado = _usuario_id_recurso_estudante(request.method, request.url.path)
        if usuario_requisitado is not None and usuario_requisitado != usuario_id.valor:
            return JSONResponse(status_code=403, content={"detail": "A sessão não pode acessar este recurso."})

        return await call_next(request)


def _resposta_nao_autenticada() -> JSONResponse:
    """Cria resposta uniforme para cookie ausente ou sessão inválida.

    A função usa status HTTP 401 e uma mensagem que não revela se o token foi
    encontrado, expirou ou foi revogado. Ela existe para manter a mesma resposta
    em todos os casos sem autenticação.
    """
    return JSONResponse(status_code=401, content={"detail": DETALHE_NAO_AUTENTICADO})


def _usuario_id_recurso_estudante(metodo: str, caminho: str) -> UUID | None:
    """Extrai identidade de rota para operações de perfil e currículo.

    A função reconhece `PUT` e `DELETE /estudantes/{uuid}` e qualquer método
    sob `/estudantes/{uuid}/curriculos`. Ela existe para aplicar autorização
    por proprietário sem alterar handlers ou casos de uso.
    """
    segmentos = caminho.strip("/").split("/")
    if len(segmentos) < 2 or segmentos[0] != "estudantes":
        return None

    eh_perfil = len(segmentos) == 2 and metodo in {"PUT", "DELETE"}
    eh_curriculo = len(segmentos) >= 3 and segmentos[2] == "curriculos"
    if not eh_perfil and not eh_curriculo:
        return None

    try:
        return UUID(segmentos[1])
    except ValueError:
        return None
