"""Autentica requisições usando a sessão persistida no cookie seguro."""

import logging
from uuid import UUID

from fastapi import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.api.sessoes import COOKIE_SESSAO
from backend.application.autenticacao_sessao import AutenticadorSessao

DETALHE_NAO_AUTENTICADO = "Sessão ausente ou inválida."
logger = logging.getLogger(__name__)

ROTAS_PUBLICAS = frozenset(
    {
        ("POST", "/estudantes"),
        ("POST", "/acessos"),
        ("DELETE", "/sessao/atual"),
        ("GET", "/docs"),
        ("GET", "/docs/oauth2-redirect"),
        ("GET", "/openapi.json"),
        ("GET", "/redoc"),
    }
)


class MiddlewareAutenticacaoSessao(BaseHTTPMiddleware):
    """Exige sessão ativa nas rotas privadas e associa a identidade validada.

    O middleware libera login, cadastro, logout e documentação; nas demais
    rotas valida o cookie por meio da porta injetada e grava o `UsuarioId` em
    `request.state.usuario_id`. Nas rotas de perfil e currículo, exige que o
    UUID da rota corresponda ao estudante autenticado para perfil e dados de
    contato, além de recursos de currículo. Registra rota, motivo e ID técnico
    do ator quando nega acesso. Ele existe para proteger recursos privados e
    manter um histórico auditável das decisões de autorização.
    """

    def __init__(self, app, autenticador: AutenticadorSessao) -> None:
        """Recebe a aplicação ASGI e o serviço de validação de sessão.

        A dependência interna impede acesso direto ao ORM na borda HTTP. Ela
        existe para compor a autenticação sem acoplar a API à infraestrutura.
        """
        super().__init__(app)
        self._autenticador = autenticador

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Valida cookie nas rotas privadas antes de encaminhar a requisição.

        O método ignora preflight e caminhos explicitamente públicos; nos demais
        exige token ativo, expõe a identidade validada e registra negações de
        propriedade com a rota, o motivo e o ID técnico do ator. Ele existe para
        negar operações sem sessão e auditar decisões de acesso.
        """
        if (
            request.method == "OPTIONS"
            or (request.method, request.url.path) in ROTAS_PUBLICAS
        ):
            return await call_next(request)

        token = request.cookies.get(COOKIE_SESSAO)
        if token is None:
            return _resposta_nao_autenticada()

        usuario_id = await self._autenticador.autenticar(token)
        if usuario_id is None:
            return _resposta_nao_autenticada()

        request.state.usuario_id = usuario_id.valor
        usuario_requisitado = _usuario_id_recurso_estudante(
            request.method, request.url.path
        )
        if usuario_requisitado is not None and usuario_requisitado != usuario_id.valor:
            rota = _rota_para_log(request.method, request.url.path)
            motivo = "proprietario_diferente"
            ator_id = str(usuario_id.valor)
            logger.warning(
                "negacao_autorizacao rota=%s motivo=%s ator_id=%s",
                rota,
                motivo,
                ator_id,
                extra={
                    "evento": "negacao_autorizacao",
                    "rota": rota,
                    "motivo": motivo,
                    "ator_id": ator_id,
                },
            )
            return JSONResponse(
                status_code=403,
                content={"detail": "A sessão não pode acessar este recurso."},
            )

        return await call_next(request)


def _resposta_nao_autenticada() -> JSONResponse:
    """Cria resposta uniforme para cookie ausente ou sessão inválida.

    A função usa status HTTP 401 e uma mensagem que não revela se o token foi
    encontrado, expirou ou foi revogado. Ela existe para manter a mesma resposta
    em todos os casos sem autenticação.
    """
    return JSONResponse(status_code=401, content={"detail": DETALHE_NAO_AUTENTICADO})


def _rota_para_log(metodo: str, caminho: str) -> str:
    """Monta uma rota de log sem IDs UUID presentes no caminho.

    A função preserva segmentos fixos e troca UUIDs por `{uuid}`, sem incluir
    query string ou valores de credencial. Ela existe para identificar a rota
    de uma negação sem registrar dados específicos do recurso acessado.
    """
    segmentos = caminho.strip("/").split("/")
    for indice, segmento in enumerate(segmentos):
        try:
            UUID(segmento)
        except ValueError:
            continue
        segmentos[indice] = "{uuid}"
    return f"{metodo} /{'/'.join(segmentos)}"


def _usuario_id_recurso_estudante(metodo: str, caminho: str) -> UUID | None:
    """Extrai identidade de rota para operações de perfil e currículo.

    A função reconhece `PUT /estudantes/{uuid}`, `PUT` em
    `/estudantes/{uuid}/dados-contato` e qualquer método sob
    `/estudantes/{uuid}/curriculos`. A exclusão de perfil usa
    `/estudantes/atual`, sem UUID, e por isso não passa por esta comparação.
    Ela existe para aplicar autorização por proprietário sem alterar handlers
    ou casos de uso.
    """
    segmentos = caminho.strip("/").split("/")
    if len(segmentos) < 2 or segmentos[0] != "estudantes":
        return None

    eh_perfil = len(segmentos) == 2 and metodo == "PUT"
    eh_dados_contato = (
        len(segmentos) == 3 and segmentos[2] == "dados-contato" and metodo == "PUT"
    )
    eh_curriculo = len(segmentos) >= 3 and segmentos[2] == "curriculos"
    if not eh_perfil and not eh_dados_contato and not eh_curriculo:
        return None

    try:
        return UUID(segmentos[1])
    except ValueError:
        return None
