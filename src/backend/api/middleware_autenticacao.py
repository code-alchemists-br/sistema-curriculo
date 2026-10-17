"""Autentica requisições usando a sessão persistida no cookie seguro."""

import logging
from contextvars import ContextVar, Token
from uuid import UUID, uuid4

from fastapi import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.api.sessoes import COOKIE_SESSAO
from backend.application.autenticacao_sessao import AutenticadorSessao

DETALHE_NAO_AUTENTICADO = "Sessão ausente ou inválida."
_contexto_correlacao: ContextVar[str | None] = ContextVar(
    "contexto_correlacao", default=None
)
_fabrica_log_original = logging.getLogRecordFactory()


def _fabricar_log_com_contexto(*args, **kwargs) -> logging.LogRecord:
    """Acrescenta a correlação ativa a cada registro de log.

    A função encadeia a fábrica já configurada e atribui seu identificador
    contextual ao registro criado. Ela existe para que logs emitidos durante
    uma requisição autenticada possam ser filtrados pela mesma correlação.
    """
    registro = _fabrica_log_original(*args, **kwargs)
    registro.correlation_id = _contexto_correlacao.get() or "-"
    return registro


logging.setLogRecordFactory(_fabricar_log_com_contexto)
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
        ("GET", "/health"),
        ("GET", "/ready"),
    }
)


class MiddlewareAutenticacaoSessao(BaseHTTPMiddleware):
    """Exige sessão ativa nas rotas privadas e associa a identidade validada.

    O middleware libera login, cadastro, logout e documentação; nas demais
    rotas valida o cookie por meio da porta injetada e grava o `UsuarioId` em
    `request.state.usuario_id` e um identificador de correlação em
    `request.state.correlation_id`. O identificador também fica disponível em
    `LogRecord.correlation_id` e no cabeçalho `X-Correlation-ID`. Nas rotas de
    perfil e currículo, exige que o UUID da rota corresponda ao estudante
    autenticado. Quando nega acesso, registra rota, motivo e ID técnico do ator.
    Ele existe para proteger recursos, auditar decisões e localizar seus logs.
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
        """Valida sessão, autoriza o recurso e propaga correlação da requisição.

        O método ignora preflight e caminhos explicitamente públicos; nos demais
        valida o cookie, instala identidade e correlação, compara a propriedade
        do recurso e registra rota, motivo e ator em caso de negação. Ele existe
        para negar operações sem sessão, auditar decisões e rastrear chamadas.
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
        correlation_id = str(uuid4())
        request.state.correlation_id = correlation_id
        token_contexto: Token[str | None] = _contexto_correlacao.set(correlation_id)
        try:
            logger.info("Requisição autenticada correlation_id=%s", correlation_id)
            usuario_requisitado = _usuario_id_recurso_estudante(
                request.method, request.url.path
            )
            if (
                usuario_requisitado is not None
                and usuario_requisitado != usuario_id.valor
            ):
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
                resposta = JSONResponse(
                    status_code=403,
                    content={"detail": "A sessão não pode acessar este recurso."},
                )
            else:
                resposta = await call_next(request)

            resposta.headers["X-Correlation-ID"] = correlation_id
            return resposta
        finally:
            _contexto_correlacao.reset(token_contexto)


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
