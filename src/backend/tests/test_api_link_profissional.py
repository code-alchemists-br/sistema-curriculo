"""Testa unitariamente a fronteira HTTP de cadastro de links profissionais."""

import json
import unittest
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from starlette.requests import Request

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.api.factory import create_app
from backend.api.link_profissional import (
    CadastroLinkProfissionalRequisicao,
    criar_router,
)
from backend.api.sessoes import COOKIE_SESSAO
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.application.cadastro_link_profissional import (
    CadastrarLinkProfissionalEntrada,
    LinkProfissionalJaCadastrado,
)
from backend.domain import (
    LinkProfissional,
    LinkProfissionalId,
    RegraDeDominioViolada,
    UsuarioId,
)

ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_LINK = UUID("00000000-0000-0000-0000-0000000000a1")


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class CadastroLinkProfissionalStub:
    """Substitui o caso de uso por comportamento determinístico em memória.

    O double registra a entrada recebida e constrói a resposta sem banco,
    framework ou rede. Ele existe para isolar a conversão exercida pelo handler
    HTTP e permitir cenários de sucesso, conflito e validação.
    """

    def __init__(
        self,
        duplicado: bool = False,
        erro_dominio: str | None = None,
    ) -> None:
        """Prepara o histórico de chamadas e o resultado configurável.

        O construtor conserva apenas estado local usado pelo teste. Ele existe
        para representar o executor injetado sem introduzir dependências
        externas na unidade de interface.
        """
        self.duplicado = duplicado
        self.erro_dominio = erro_dominio
        self.entradas: list[CadastrarLinkProfissionalEntrada] = []

    async def executar(
        self, entrada: CadastrarLinkProfissionalEntrada
    ) -> LinkProfissional:
        """Registra a entrada e devolve ou rejeita o link configurado.

        O método simula o contrato público do caso de uso usando somente dados
        em memória. Ele existe para verificar que a API traduz corretamente a
        chamada e a falha sem testar regras internas.
        """
        self.entradas.append(entrada)
        if self.erro_dominio is not None:
            raise RegraDeDominioViolada(self.erro_dominio)
        if self.duplicado:
            raise LinkProfissionalJaCadastrado(
                "Link profissional já cadastrado para este usuário."
            )
        return LinkProfissional(
            id=LinkProfissionalId(ID_LINK),
            usuario_id=entrada.usuario_id,
            rotulo=entrada.rotulo,
            url=entrada.url,
        )


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def _rota(router: APIRouter) -> Any:
    """Obtém o endpoint POST de links profissionais diretamente da tabela de rotas.

    A função percorre o router já configurado e devolve o handler sem iniciar
    servidor ASGI. Ela existe para manter o teste no nível unitário da
    fronteira, com executor e requisição controlados.
    """
    for rota in router.routes:
        if getattr(rota, "path", None) == "/links-profissionais" and "POST" in getattr(
            rota, "methods", set()
        ):
            return rota.endpoint
    raise AssertionError("Rota POST /links-profissionais não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def _request(usuario_id: UUID | None) -> Request:
    """Constrói uma requisição mínima com o principal opcional no estado.

    A função monta um escopo ASGI local e instala somente o UUID que seria
    fornecido pelo mecanismo existente. Ela existe para verificar a propriedade
    sem aceitar um identificador controlado pelo corpo HTTP.
    """
    request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/links-profissionais",
            "headers": [],
        }
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class CadastroLinkProfissionalRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução entre transporte HTTP e executor de link profissional.

    A classe chama o handler decorado com doubles locais, sem criar aplicação
    FastAPI nem servidor. Ela existe para proteger o contrato de fronteira no
    nível unitário apropriado.
    """

    async def test_vincula_o_link_ao_principal_autenticado(self) -> None:
        """Encaminha dados completos usando o UUID instalado na requisição.

        O cenário invoca o handler e inspeciona a entrada entregue ao double.
        Ele existe para impedir que a API derive o proprietário do payload ou
        exponha a entidade de domínio na resposta.
        """
        executor = CadastroLinkProfissionalStub()
        cadastrar = _rota(criar_router(executor))

        resposta = await cadastrar(
            CadastroLinkProfissionalRequisicao(
                rotulo="GitHub Perfil",
                url="https://github.com/usuario",
            ),
            _request(ID_USUARIO),
        )

        self.assertEqual(resposta.id, ID_LINK)
        self.assertEqual(resposta.usuario_id, ID_USUARIO)
        self.assertEqual(resposta.rotulo, "GitHub Perfil")
        self.assertEqual(resposta.url, "https://github.com/usuario")
        self.assertEqual(executor.entradas[0].usuario_id.valor, ID_USUARIO)
        self.assertEqual(executor.entradas[0].rotulo, "GitHub Perfil")
        self.assertEqual(executor.entradas[0].url, "https://github.com/usuario")

    async def test_traduz_duplicidade_para_conflito(self) -> None:
        """Apresenta 409 quando o executor informa link já cadastrado.

        O cenário usa o double configurado para falhar e observa a exceção HTTP
        gerada pelo handler. Ele existe para manter o conflito compreensível e
        não revelar dados persistidos de qualquer outra conta.
        """
        cadastrar = _rota(criar_router(CadastroLinkProfissionalStub(duplicado=True)))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroLinkProfissionalRequisicao(
                    rotulo="Portfólio",
                    url="https://github.com/usuario",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            contexto.exception.detail,
            "Link profissional já cadastrado para este usuário.",
        )

    async def test_traduz_regra_de_dominio_violada_para_422_generico(self) -> None:
        """Apresenta 422 genérico quando o domínio rejeita o link.

        O cenário recebe uma requisição válida na fronteira, mas o executor
        sinaliza uma regra violada com texto confidencial; a resposta usa
        mensagem genérica. Ele existe para não expor o texto interno das regras
        de domínio ao cliente HTTP.
        """
        cadastrar = _rota(
            criar_router(
                CadastroLinkProfissionalStub(erro_dominio="detalhe interno confidencial")
            )
        )

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroLinkProfissionalRequisicao(
                    rotulo="GitHub",
                    url="https://github.com/usuario",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(
            contexto.exception.status_code,
            status.HTTP_422_UNPROCESSABLE_CONTENT,
        )
        self.assertEqual(
            contexto.exception.detail,
            "O link profissional informado viola as regras de cadastro.",
        )
        self.assertNotIn("confidencial", contexto.exception.detail)

    async def test_rejeita_requisicao_sem_principal(self) -> None:
        """Retorna 401 sem invocar o executor para requisição anônima.

        O cenário omite o estado de autenticação e compara o histórico do
        double. Ele existe para garantir que o endpoint depende do principal
        fornecido pelo mecanismo de borda já existente.
        """
        executor = CadastroLinkProfissionalStub()
        cadastrar = _rota(criar_router(executor))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroLinkProfissionalRequisicao(
                    rotulo="Portfólio",
                    url="https://site.com",
                ),
                _request(None),
            )

        self.assertEqual(contexto.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(contexto.exception.detail, "Autenticação necessária.")
        self.assertEqual(executor.entradas, [])

    async def test_retorna_503_quando_executor_nao_disponivel(self) -> None:
        """Retorna 503 quando o executor não foi fornecido à fábrica de router.

        O cenário instancia o router com None e tenta cadastrar um link.
        Ele existe para indicar indisponibilidade controlada do serviço quando
        a dependência não estiver disponível.
        """
        cadastrar = _rota(criar_router(None))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroLinkProfissionalRequisicao(
                    rotulo="Portfólio",
                    url="https://site.com",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(
            contexto.exception.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )
        self.assertEqual(contexto.exception.detail, "Cadastro indisponível.")

    def test_fabrica_registra_rota_de_links_profissionais(self) -> None:
        """Mantém o endpoint de link profissional disponível na aplicação composta.

        O teste cria somente a fábrica FastAPI e consulta o contrato OpenAPI,
        sem iniciar servidor ou injetar infraestrutura. Ele existe para evitar
        que o router seja implementado mas fique desconectado da API pública.
        """
        app = create_app()

        self.assertIn("/links-profissionais", app.openapi()["paths"])


CREDENCIAL_VALIDA = "credencial-sintetica-link"
CAMPOS_PUBLICOS = {"id", "usuario_id", "rotulo", "url"}


class AutenticadorSessaoStub(AutenticadorSessao):
    """Autentica somente a credencial sintética do cenário.

    O double devolve o estudante do teste para o token conhecido e ``None`` para
    qualquer outro. Ele existe para exercitar o middleware real de sessão sem
    banco de sessões.
    """

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Devolve o estudante do teste apenas para a credencial conhecida.

        O método compara o token recebido sem consultar serviços. Ele existe
        para que o dono da requisição venha da sessão autenticada.
        """
        return UsuarioId(ID_USUARIO) if token == CREDENCIAL_VALIDA else None


async def _postar(app: object, corpo: dict[str, object]) -> tuple[int, dict[str, Any]]:
    """Envia um POST /links-profissionais autenticado diretamente à aplicação ASGI.

    A função serializa o corpo, inclui o cookie de sessão sintético e coleta
    status e JSON da resposta. Ela existe para observar a resposta pública real
    emitida pelo FastAPI, sem servidor nem cliente externo.
    """
    corpo_bytes = json.dumps(corpo).encode()
    escopo = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/links-profissionais",
        "raw_path": b"/links-profissionais",
        "query_string": b"",
        "headers": [
            (b"content-type", b"application/json"),
            (b"content-length", str(len(corpo_bytes)).encode()),
            (b"cookie", f"{COOKIE_SESSAO}={CREDENCIAL_VALIDA}".encode()),
        ],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }
    recebido = False
    status_resposta = 0
    partes: list[bytes] = []

    async def receber() -> dict[str, object]:
        """Entrega o corpo da chamada ASGI uma única vez."""
        nonlocal recebido
        if recebido:
            return {"type": "http.disconnect"}
        recebido = True
        return {"type": "http.request", "body": corpo_bytes, "more_body": False}

    async def enviar(mensagem: dict[str, object]) -> None:
        """Captura status e fragmentos do corpo de resposta ASGI."""
        nonlocal status_resposta
        if mensagem["type"] == "http.response.start":
            status_resposta = int(mensagem["status"])
        elif mensagem["type"] == "http.response.body":
            partes.append(mensagem.get("body", b""))  # type: ignore[arg-type]

    await app(escopo, receber, enviar)  # type: ignore[operator]
    payload = b"".join(partes)
    return status_resposta, json.loads(payload) if payload else {}


def _app(executor: CadastroLinkProfissionalStub):
    """Compõe a aplicação com middleware de sessão e o executor de teste.

    A fábrica real recebe o autenticador sintético e o double do caso de uso.
    Ela existe para exercitar autenticação, validação e serialização reais.
    """
    return create_app(
        autenticador_sessao=AutenticadorSessaoStub(),
        cadastrar_link_profissional=executor,
    )


class RespostaPublicaLinkProfissionalTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o JSON público emitido pela aplicação montada.

    Os cenários enviam requisições reais à aplicação ASGI e inspecionam status
    e corpo. A classe existe para proteger o contrato público do cadastro de
    link profissional, inclusive nas respostas de erro.
    """

    async def test_resposta_201_expoe_somente_campos_publicos_tratados(self) -> None:
        """Devolve 201 com id, dono, rótulo e URL já tratados, e nada mais.

        O corpo envia rótulo com espaços e URL com esquema em maiúsculas; a
        resposta deve trazer exatamente os quatro campos, com valores já
        tratados pelo domínio e sem a chave normalizada. O teste existe para
        impedir que a resposta passe a expor dados internos.
        """
        status_resposta, corpo = await _postar(
            _app(CadastroLinkProfissionalStub()),
            {"rotulo": "  GitHub Perfil  ", "url": "HTTPS://GitHub.com/Usuario/"},
        )

        self.assertEqual(status_resposta, 201)
        self.assertEqual(set(corpo), CAMPOS_PUBLICOS)
        self.assertEqual(corpo["id"], str(ID_LINK))
        self.assertEqual(corpo["rotulo"], "GitHub Perfil")
        self.assertEqual(corpo["url"], "https://GitHub.com/Usuario/")
        self.assertNotIn("url_normalizada", json.dumps(corpo))

    async def test_usuario_da_resposta_e_o_da_sessao(self) -> None:
        """Usa o dono da sessão mesmo quando o corpo envia outro ``usuario_id``.

        O cliente tenta indicar outro proprietário no JSON; a resposta e a
        entrada do caso de uso usam o estudante autenticado. O teste existe
        para que o cliente nunca escolha o dono do link.
        """
        executor = CadastroLinkProfissionalStub()

        status_resposta, corpo = await _postar(
            _app(executor),
            {
                "rotulo": "GitHub",
                "url": "https://github.com/usuario",
                "usuario_id": str(UUID(int=999)),
            },
        )

        self.assertEqual(status_resposta, 201)
        self.assertEqual(corpo["usuario_id"], str(ID_USUARIO))
        self.assertEqual(executor.entradas[0].usuario_id, UsuarioId(ID_USUARIO))

    async def test_erros_devolvem_apenas_detalhe_publico(self) -> None:
        """Responde 409 e 422 apenas com ``detail``, sem dados internos.

        Os cenários simulam duplicidade e regra de domínio violada com texto
        confidencial. O teste existe para que as respostas de erro também
        respeitem o contrato público.
        """
        cenarios = (
            (
                CadastroLinkProfissionalStub(duplicado=True),
                409,
                "Link profissional já cadastrado para este usuário.",
            ),
            (
                CadastroLinkProfissionalStub(erro_dominio="detalhe interno confidencial"),
                422,
                "O link profissional informado viola as regras de cadastro.",
            ),
        )
        for executor, esperado_status, esperado_detalhe in cenarios:
            with self.subTest(status=esperado_status):
                status_resposta, corpo = await _postar(
                    _app(executor), {"rotulo": "GitHub", "url": "https://github.com/usuario"}
                )

                self.assertEqual(status_resposta, esperado_status)
                self.assertEqual(corpo, {"detail": esperado_detalhe})

    async def test_requisicao_invalida_responde_422_sem_chamar_executor(self) -> None:
        """Barra na fronteira URLs e rótulos inválidos, sem acionar o caso de uso.

        O teste envia URL com esquema proibido, URL com credenciais e rótulo em
        branco. Ele existe para provar que a validação acontece antes da
        Application.
        """
        for corpo in (
            {"rotulo": "Script", "url": "javascript:alert(1)"},
            {"rotulo": "GitHub", "url": "https://user:senha@github.com"},
            {"rotulo": "   ", "url": "https://github.com/usuario"},
        ):
            with self.subTest(corpo=corpo):
                executor = CadastroLinkProfissionalStub()

                status_resposta, _ = await _postar(_app(executor), corpo)

                self.assertEqual(status_resposta, 422)
                self.assertEqual(executor.entradas, [])


class ValidacaoRequisicaoLinkTestCase(unittest.TestCase):
    """Verifica a validação do corpo de cadastro de link na fronteira.

    Os cenários validam o DTO diretamente. A classe existe para garantir que
    rótulo e URL sigam as mesmas regras do domínio já na API.
    """

    def test_rejeita_campos_invalidos(self) -> None:
        """Rejeita ausência, tipo errado e valores que violam as regras do domínio.

        Cada cenário altera um campo do corpo válido e exige
        ``ValidationError``. O teste existe para cobrir formato, tipo e campos
        obrigatórios exigidos na fronteira.
        """
        cenarios = {
            "rótulo ausente": {"url": "https://github.com/usuario"},
            "URL ausente": {"rotulo": "GitHub"},
            "rótulo numérico": {"rotulo": 123, "url": "https://github.com/usuario"},
            "rótulo acima de 100": {"rotulo": "A" * 101, "url": "https://github.com/usuario"},
            "esquema proibido": {"rotulo": "GitHub", "url": "ftp://arquivos.com"},
            "sem host": {"rotulo": "GitHub", "url": "http://:80"},
            "espaço na URL": {"rotulo": "GitHub", "url": "https://github.com/a b"},
        }
        for descricao, dados in cenarios.items():
            with self.subTest(cenario=descricao):
                with self.assertRaises(ValidationError):
                    CadastroLinkProfissionalRequisicao.model_validate(dados)

    def test_normaliza_rotulo_e_esquema(self) -> None:
        """Apara o rótulo e coloca o esquema da URL em minúsculas.

        O cenário envia valores com espaços e esquema em maiúsculas. Ele existe
        para que a fronteira entregue ao caso de uso os mesmos valores tratados
        pelo domínio.
        """
        requisicao = CadastroLinkProfissionalRequisicao.model_validate(
            {"rotulo": "  GitHub  ", "url": "HTTPS://github.com/usuario"}
        )

        self.assertEqual(requisicao.rotulo, "GitHub")
        self.assertEqual(requisicao.url, "https://github.com/usuario")


class ContratoOpenApiLinkTestCase(unittest.TestCase):
    """Verifica o contrato publicado no OpenAPI para o cadastro de link.

    Os testes inspecionam o esquema gerado pela aplicação. A classe existe para
    que a documentação pública reflita exatamente a resposta e a requisição.
    """

    def test_resposta_201_usa_somente_campos_publicos(self) -> None:
        """Publica a resposta 201 com os quatro campos públicos obrigatórios.

        O teste segue a referência da resposta 201 até o esquema e compara as
        propriedades e os obrigatórios. Ele existe para que a chave normalizada
        nunca apareça no contrato documentado.
        """
        documento = create_app().openapi()
        resposta = documento["paths"]["/links-profissionais"]["post"]["responses"]["201"]
        referencia = resposta["content"]["application/json"]["schema"]["$ref"]
        esquema = documento["components"]["schemas"][referencia.rsplit("/", 1)[-1]]

        self.assertTrue(referencia.endswith("/LinkProfissionalResposta"))
        self.assertEqual(set(esquema["properties"]), CAMPOS_PUBLICOS)
        self.assertEqual(set(esquema["required"]), CAMPOS_PUBLICOS)

    def test_requisicao_exige_rotulo_e_url(self) -> None:
        """Publica rótulo e URL como campos obrigatórios da requisição.

        O teste inspeciona o esquema da requisição no OpenAPI. Ele existe para
        que o contrato documentado reflita a validação aplicada.
        """
        esquemas = create_app().openapi()["components"]["schemas"]

        self.assertEqual(
            set(esquemas["CadastroLinkProfissionalRequisicao"]["required"]), {"rotulo", "url"}
        )


if __name__ == "__main__":
    unittest.main()
