"""Verifica autenticação HTTP por sessão persistida."""

import json
import unittest
from uuid import UUID

from fastapi import Request, Response

from backend.api.factory import create_app
from backend.api.middleware_autenticacao import MiddlewareAutenticacaoSessao
from backend.api.sessoes import COOKIE_SESSAO
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.domain.value_objects import UsuarioId


class AutenticadorSessaoStub(AutenticadorSessao):
    """Devolve identidade configurável e registra os tokens consultados.

    O double não consulta persistência. Ele existe para isolar as decisões do
    middleware e observar o encaminhamento do cookie.
    """

    def __init__(self, usuario_id: UsuarioId | None) -> None:
        """Armazena o resultado da autenticação e inicia o histórico.

        A configuração é local e determinística. Ela existe para exercitar
        tokens válidos e inválidos sem banco ou relógio real.
        """
        self.usuario_id = usuario_id
        self.tokens: list[str] = []

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Registra o token consultado e devolve o resultado configurado.

        O método simula uma decisão de sessão sem I/O. Ele existe para testar
        como o middleware reage à identidade retornada.
        """
        self.tokens.append(token)
        return self.usuario_id


def _request(metodo: str, caminho: str, token: str | None = None) -> Request:
    """Monta uma requisição ASGI mínima para chamada direta do dispatch.

    A função constrói scope HTTP em memória e inclui o cookie opcional. Ela
    existe para testar middleware sem cliente de rede ou servidor.
    """
    headers = []
    if token is not None:
        headers.append((b"cookie", f"{COOKIE_SESSAO}={token}".encode("ascii")))
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": metodo,
        "scheme": "https",
        "path": caminho,
        "raw_path": caminho.encode("ascii"),
        "query_string": b"",
        "root_path": "",
        "headers": headers,
        "server": ("testserver", 443),
        "client": ("testclient", 1234),
    }
    return Request(scope)


class MiddlewareAutenticacaoSessaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Protege rotas privadas e propaga a identidade validada."""

    def _middleware(
        self, autenticador: AutenticadorSessaoStub
    ) -> MiddlewareAutenticacaoSessao:
        """Cria middleware sem iniciar aplicação ASGI real.

        A aplicação interna é um callable inerte, pois o teste chama `dispatch`
        diretamente. O helper existe para manter os cenários compactos.
        """
        return MiddlewareAutenticacaoSessao(
            lambda scope, receive, send: None, autenticador
        )

    async def test_rejeita_rota_privada_sem_cookie(self) -> None:
        """Retorna 401 sem chamar autenticador ou handler da rota.

        A requisição privada não contém credencial. O teste existe para impedir
        acesso anônimo a rotas protegidas.
        """
        autenticador = AutenticadorSessaoStub(UsuarioId(UUID(int=1)))
        chamadas = []

        async def proxima(request: Request) -> Response:
            """Registra encaminhamento inesperado do middleware."""
            chamadas.append(request)
            return Response(status_code=204)

        resposta = await self._middleware(autenticador).dispatch(
            _request("GET", "/privado"), proxima
        )

        self.assertEqual(resposta.status_code, 401)
        self.assertTrue(resposta.headers["content-type"].startswith("application/json"))
        self.assertEqual(
            json.loads(resposta.body), {"detail": "Sessão ausente ou inválida."}
        )
        self.assertEqual(autenticador.tokens, [])
        self.assertEqual(chamadas, [])

    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    async def test_cadastro_de_competencia_exige_sessao(self) -> None:
        """Rejeita o cadastro de competência quando falta cookie de sessão.

        O cenário chama o middleware com o caminho público da nova rota e não
        fornece credencial. Ele existe para comprovar que o endpoint não foi
        incluído na lista de exceções de autenticação.
        """
        autenticador = AutenticadorSessaoStub(UsuarioId(UUID(int=1)))
        chamadas = []

        async def proxima(request: Request) -> Response:
            """Registra um encaminhamento que não deve ocorrer no cenário."""
            chamadas.append(request)
            return Response(status_code=204)

        resposta = await self._middleware(autenticador).dispatch(
            _request("POST", "/competencias"), proxima
        )

        self.assertEqual(resposta.status_code, 401)
        self.assertEqual(autenticador.tokens, [])
        self.assertEqual(chamadas, [])

    async def test_rejeita_cookie_sem_sessao_ativa(self) -> None:
        """Retorna 401 quando a consulta não encontra sessão válida.

        O autenticador double devolve `None` para o token recebido. O teste
        existe para impedir acesso com token desconhecido ou inativo.
        """
        autenticador = AutenticadorSessaoStub(None)
        request = _request("GET", "/privado", "token-invalido")

        resposta = await self._middleware(autenticador).dispatch(
            request, lambda _: None
        )

        self.assertEqual(resposta.status_code, 401)
        self.assertTrue(resposta.headers["content-type"].startswith("application/json"))
        self.assertEqual(
            json.loads(resposta.body), {"detail": "Sessão ausente ou inválida."}
        )
        self.assertNotIn("token-invalido", resposta.body.decode("utf-8"))
        self.assertEqual(autenticador.tokens, ["token-invalido"])

    async def test_autentica_cookie_e_disponibiliza_identidade_na_requisicao(
        self,
    ) -> None:
        """Propaga o UUID do estudante após validação positiva.

        O handler seguinte observa `request.state.usuario_id`; o teste existe
        para estabelecer o contrato de identidade consumido por rotas futuras.
        """
        usuario_id = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))
        autenticador = AutenticadorSessaoStub(usuario_id)
        request = _request("GET", "/privado", "token-valido")

        async def proxima(requisicao: Request) -> Response:
            """Confirma a identidade confiável instalada pelo middleware."""
            self.assertEqual(requisicao.state.usuario_id, usuario_id.valor)
            return Response(status_code=204)

        resposta = await self._middleware(autenticador).dispatch(request, proxima)

        self.assertEqual(resposta.status_code, 204)
        self.assertEqual(autenticador.tokens, ["token-valido"])

    async def test_perfil_exige_sessao_em_edicao_e_exclusao(self) -> None:
        """Rejeita chamadas anônimas às operações de perfil PUT e DELETE.

        O teste usa os caminhos reais do router de perfil — edição por UUID e
        exclusão do perfil atual — e confirma que o middleware não encaminha a
        requisição sem cookie. Ele existe para proteger edição e exclusão do
        perfil por autenticação.
        """
        for metodo, caminho in (
            ("PUT", "/estudantes/00000000-0000-0000-0000-000000000001"),
            ("DELETE", "/estudantes/atual"),
        ):
            with self.subTest(metodo=metodo):
                autenticador = AutenticadorSessaoStub(UsuarioId(UUID(int=1)))
                resposta = await self._middleware(autenticador).dispatch(
                    _request(metodo, caminho),
                    lambda _: None,
                )
                self.assertEqual(resposta.status_code, 401)
                self.assertEqual(autenticador.tokens, [])

    # Proveniência: decision-analysis prompts/backend/20261015-120000-expor-exclusao-perfil-estudante-v001.md#v001
    async def test_exclusao_do_perfil_atual_e_encaminhada_com_identidade_da_sessao(
        self,
    ) -> None:
        """Encaminha `DELETE /estudantes/atual` com o principal da sessão.

        A rota não carrega UUID, então o middleware não aplica comparação de
        proprietário e apenas instala a identidade validada. O teste existe
        para garantir que a exclusão chegue ao handler sem 403 indevido e com
        o estudante autenticado disponível em `request.state`.
        """
        usuario_id = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))
        autenticador = AutenticadorSessaoStub(usuario_id)

        async def proxima(request: Request) -> Response:
            """Confirma que a identidade validada chega ao handler de exclusão."""
            self.assertEqual(request.state.usuario_id, usuario_id.valor)
            return Response(status_code=204)

        resposta = await self._middleware(autenticador).dispatch(
            _request("DELETE", "/estudantes/atual", "token-valido"), proxima
        )

        self.assertEqual(resposta.status_code, 204)
        self.assertEqual(autenticador.tokens, ["token-valido"])

    async def test_consulta_perfil_exige_sessao(self) -> None:
        """Rejeita GET de perfil pessoal quando não há cookie de sessão.

        A rota de consulta é privada por padrão no middleware. O cenário omite
        credencial e confirma que o autenticador e o handler não são chamados.
        """
        autenticador = AutenticadorSessaoStub(UsuarioId(UUID(int=1)))
        chamadas = []

        async def proxima(request: Request) -> Response:
            """Registra encaminhamento que não deve ocorrer sem sessão."""
            chamadas.append(request)
            return Response(status_code=200)

        resposta = await self._middleware(autenticador).dispatch(
            _request("GET", "/estudantes/00000000-0000-0000-0000-000000000001"),
            proxima,
        )

        self.assertEqual(resposta.status_code, 401)
        self.assertEqual(autenticador.tokens, [])
        self.assertEqual(chamadas, [])

    async def test_perfil_so_e_alterado_pelo_estudante_da_sessao(self) -> None:
        """Retorna 403 quando UUID da rota pertence a outro estudante.

        Uma sessão válida tenta usar o caminho real do perfil de outra pessoa;
        o handler seguinte não deve ser chamado. O teste existe para proteger
        autorização do recurso além da autenticação da sessão.
        """
        usuario_autenticado = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))
        autenticador = AutenticadorSessaoStub(usuario_autenticado)
        chamadas = []

        async def proxima(request: Request) -> Response:
            """Registra acesso ao handler para comprovar bloqueio anterior."""
            chamadas.append(request)
            return Response(status_code=204)

        resposta = await self._middleware(autenticador).dispatch(
            _request(
                "PUT",
                "/estudantes/00000000-0000-0000-0000-000000000002",
                "token-valido",
            ),
            proxima,
        )

        self.assertEqual(resposta.status_code, 403)
        self.assertEqual(autenticador.tokens, ["token-valido"])
        self.assertEqual(chamadas, [])

    async def test_perfil_proprio_e_encaminhado_apos_autenticacao(self) -> None:
        """Permite edição do perfil quando rota e sessão identificam o mesmo usuário.

        O handler seguinte recebe o UUID autenticado em `request.state`. O teste
        existe para comprovar o fluxo autorizado do perfil sem alterar seu router.
        """
        usuario_id = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))
        autenticador = AutenticadorSessaoStub(usuario_id)

        async def proxima(request: Request) -> Response:
            """Confirma que a identidade validada permanece disponível."""
            self.assertEqual(request.state.usuario_id, usuario_id.valor)
            return Response(status_code=204)

        resposta = await self._middleware(autenticador).dispatch(
            _request("PUT", f"/estudantes/{usuario_id.valor}", "token-valido"), proxima
        )

        self.assertEqual(resposta.status_code, 204)
        self.assertEqual(autenticador.tokens, ["token-valido"])

    async def test_rotas_de_curriculo_exigem_sessao(self) -> None:
        """Rejeita sem cookie leitura e mutações de currículo e itens.

        Os caminhos cobrem listagem, criação, edição, seleção e desseleção reais.
        O teste existe para confirmar que nenhuma operação de currículo fica
        fora da proteção de autenticação.
        """
        usuario_id = "00000000-0000-0000-0000-000000000001"
        curriculo_id = "00000000-0000-0000-0000-000000000002"
        item_id = "00000000-0000-0000-0000-000000000003"
        cenarios = (
            ("GET", f"/estudantes/{usuario_id}/curriculos"),
            ("POST", f"/estudantes/{usuario_id}/curriculos"),
            ("PUT", f"/estudantes/{usuario_id}/curriculos/{curriculo_id}"),
            ("POST", f"/estudantes/{usuario_id}/curriculos/{curriculo_id}/itens"),
            (
                "DELETE",
                f"/estudantes/{usuario_id}/curriculos/{curriculo_id}/itens/idioma/{item_id}",
            ),
        )

        for metodo, caminho in cenarios:
            with self.subTest(metodo=metodo, caminho=caminho):
                autenticador = AutenticadorSessaoStub(UsuarioId(UUID(usuario_id)))
                resposta = await self._middleware(autenticador).dispatch(
                    _request(metodo, caminho), lambda _: None
                )
                self.assertEqual(resposta.status_code, 401)
                self.assertEqual(autenticador.tokens, [])

    async def test_curriculo_de_outro_estudante_e_rejeitado(self) -> None:
        """Retorna 403 para operações de currículo fora do dono autenticado.

        Uma sessão válida tenta atingir listagem, alteração ou seleção sob o
        UUID de outra pessoa. O teste existe para garantir isolamento por
        estudante antes de chamar qualquer handler.
        """
        usuario_autenticado = UUID("00000000-0000-0000-0000-000000000001")
        usuario_alheio = "00000000-0000-0000-0000-000000000002"
        curriculo_id = "00000000-0000-0000-0000-000000000003"
        item_id = "00000000-0000-0000-0000-000000000004"
        cenarios = (
            ("GET", f"/estudantes/{usuario_alheio}/curriculos"),
            ("POST", f"/estudantes/{usuario_alheio}/curriculos"),
            ("PUT", f"/estudantes/{usuario_alheio}/curriculos/{curriculo_id}"),
            ("POST", f"/estudantes/{usuario_alheio}/curriculos/{curriculo_id}/itens"),
            (
                "DELETE",
                f"/estudantes/{usuario_alheio}/curriculos/{curriculo_id}/itens/idioma/{item_id}",
            ),
        )

        for metodo, caminho in cenarios:
            with self.subTest(metodo=metodo, caminho=caminho):
                autenticador = AutenticadorSessaoStub(UsuarioId(usuario_autenticado))
                resposta = await self._middleware(autenticador).dispatch(
                    _request(metodo, caminho, "token-valido"), lambda _: None
                )
                self.assertEqual(resposta.status_code, 403)
                self.assertEqual(autenticador.tokens, ["token-valido"])

    async def test_curriculo_proprio_e_encaminhado_apos_autenticacao(self) -> None:
        """Encaminha operação quando UUID do currículo corresponde à sessão.

        O handler seguinte observa a identidade autenticada instalada em state.
        O teste existe para confirmar o caminho autorizado da operação.
        """
        usuario_id = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))
        autenticador = AutenticadorSessaoStub(usuario_id)
        request = _request(
            "GET", f"/estudantes/{usuario_id.valor}/curriculos", "token-valido"
        )

        async def proxima(requisicao: Request) -> Response:
            """Confirma identidade confiável para o handler de currículo."""
            self.assertEqual(requisicao.state.usuario_id, usuario_id.valor)
            return Response(status_code=200)

        resposta = await self._middleware(autenticador).dispatch(request, proxima)

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(autenticador.tokens, ["token-valido"])

    async def test_login_cadastro_logout_documentacao_e_preflight_sao_publicos(
        self,
    ) -> None:
        """Encaminha rotas públicas sem exigir token ou chamar autenticador.

        Os métodos e caminhos públicos cobrem fluxos prévios à autenticação,
        saída da sessão, documentação e preflight CORS. O teste existe para
        manter esses fluxos acessíveis quando a proteção está ativa.
        """
        cenarios = (
            ("POST", "/estudantes"),
            ("POST", "/acessos"),
            ("DELETE", "/sessao/atual"),
            ("GET", "/docs"),
            ("OPTIONS", "/privado"),
        )
        for metodo, caminho in cenarios:
            with self.subTest(metodo=metodo, caminho=caminho):
                autenticador = AutenticadorSessaoStub(None)
                resposta = await self._middleware(autenticador).dispatch(
                    _request(metodo, caminho), lambda _: self._resposta_vazia()
                )
                self.assertEqual(resposta.status_code, 204)
                self.assertEqual(autenticador.tokens, [])

    async def _resposta_vazia(self) -> Response:
        """Devolve resposta 204 usada pela rota pública simulada."""
        return Response(status_code=204)

    async def test_fabrica_instala_middleware_quando_autenticador_e_injetado(
        self,
    ) -> None:
        """Confirma que a composição adiciona middleware de sessão.

        O teste inspeciona a configuração FastAPI sem iniciar servidor. Ele
        existe para garantir que a capacidade injetada protege a aplicação.
        """
        app = create_app(autenticador_sessao=AutenticadorSessaoStub(None))

        self.assertTrue(
            any(
                middleware.cls is MiddlewareAutenticacaoSessao
                for middleware in app.user_middleware
            )
        )

    async def test_fabrica_preserva_composicao_sem_autenticador_opcional(self) -> None:
        """Mantém compatibilidade com composições existentes sem auth configurada.

        A fábrica recebe dependências opcionais no projeto atual. O teste
        existe para impedir que a nova extensão exija adaptações de outros
        módulos enquanto a composição persistente é preparada.
        """
        app = create_app()

        self.assertFalse(
            any(
                middleware.cls is MiddlewareAutenticacaoSessao
                for middleware in app.user_middleware
            )
        )
