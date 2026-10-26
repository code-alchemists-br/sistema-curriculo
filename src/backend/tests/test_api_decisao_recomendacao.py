"""Testa as rotas de decisão sobre recomendações com autenticação e autorização."""

import json
import unittest
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
from backend.api.decisao_recomendacao import CAMINHO_DECISAO, CAMINHO_DECISOES
from backend.api.documentacao_openapi import TAG_VERSOES_CURRICULO
from backend.api.factory import create_app
from backend.api.sessoes import COOKIE_SESSAO
from backend.application import (
    ConsultarDecisoesRecomendacao,
    RegistrarDecisaoRecomendacao,
    RevisarVersaoCurriculo,
)
from backend.tests.fixtures.curriculo_exportacao import (
    ID_CURRICULO_ESTAVEL,
    ID_USUARIO_ESTAVEL,
    obter_curriculo_exportacao_fixture,
)
from backend.tests.test_api_exportacao_curriculo import (
    CREDENCIAL_VALIDA,
    OUTRO_USUARIO,
    AutenticadorSessaoStub,
    GeradorPreviaStub,
)
from backend.tests.test_application_decisao_recomendacao import (
    RelogioFixo,
    RepositorioCurriculoStub,
    RepositorioDecisaoMemoria,
)

INSTANTE = datetime(2026, 10, 25, 14, 0, tzinfo=UTC)
# Dia em que as datas da fixture são coerentes: a única recomendação é a cidade ausente.
DIA_DA_REVISAO = datetime(2025, 6, 1, 12, 0, tzinfo=UTC)
CODIGO_DO_AVISO = "CIDADE_AUSENTE"


def _caminho(usuario_id: UUID, curriculo_id: UUID, codigo: str | None = None) -> str:
    """Monta o caminho da decisão ou da listagem para os identificadores dados.

    A função preenche o modelo de rota publicado. Ela existe para evitar
    divergência entre o teste e o caminho registrado.
    """
    if codigo is None:
        return CAMINHO_DECISOES.format(usuario_id=usuario_id, curriculo_id=curriculo_id)
    return CAMINHO_DECISAO.format(usuario_id=usuario_id, curriculo_id=curriculo_id, codigo=codigo)


def _app(repositorio: RepositorioDecisaoMemoria, *, com_executores: bool = True):
    """Compõe a aplicação com middleware de sessão e os casos de uso reais.

    A função liga a revisão real sobre a prévia da fixture, a persistência em
    memória e os relógios fixos. Ela existe para exercitar autenticação,
    autorização, roteamento e resposta reais, sem banco.
    """
    revisor = RevisarVersaoCurriculo(GeradorPreviaStub(), RelogioFixo(DIA_DA_REVISAO))
    return create_app(
        autenticador_sessao=AutenticadorSessaoStub(),
        registrar_decisao_recomendacao=(
            RegistrarDecisaoRecomendacao(revisor, repositorio, RelogioFixo(INSTANTE))
            if com_executores
            else None
        ),
        consultar_decisoes_recomendacao=(
            ConsultarDecisoesRecomendacao(
                RepositorioCurriculoStub(obter_curriculo_exportacao_fixture().curriculo),
                repositorio,
            )
            if com_executores
            else None
        ),
    )


async def _chamar(
    app: object,
    metodo: str,
    caminho: str,
    corpo: dict[str, Any] | None = None,
    autenticado: bool = True,
) -> tuple[int, Any]:
    """Envia uma requisição à aplicação ASGI e devolve status e corpo em JSON.

    A função inclui o cookie de sessão sintético quando pedido e o corpo JSON
    quando informado. Ela existe para observar a resposta real emitida pelo
    FastAPI, sem servidor nem cliente externo.
    """
    conteudo = json.dumps(corpo).encode() if corpo is not None else b""
    cabecalhos = [(b"content-type", b"application/json")]
    if autenticado:
        cabecalhos.append((b"cookie", f"{COOKIE_SESSAO}={CREDENCIAL_VALIDA}".encode()))
    escopo = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": metodo,
        "scheme": "http",
        "path": caminho,
        "raw_path": caminho.encode(),
        "query_string": b"",
        "headers": cabecalhos,
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }
    status_resposta = 0
    partes: list[bytes] = []

    async def receber() -> dict[str, object]:
        """Entrega o corpo da requisição de uma só vez."""
        return {"type": "http.request", "body": conteudo, "more_body": False}

    async def enviar(mensagem: dict[str, Any]) -> None:
        """Captura o status e os fragmentos do corpo da resposta."""
        nonlocal status_resposta
        if mensagem["type"] == "http.response.start":
            status_resposta = int(mensagem["status"])
        elif mensagem["type"] == "http.response.body":
            partes.append(mensagem.get("body", b""))

    await app(escopo, receber, enviar)  # type: ignore[operator]
    texto = b"".join(partes)
    return status_resposta, (json.loads(texto) if texto else None)


class DecisaoRecomendacaoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o contrato HTTP da decisão sobre recomendações.

    Os cenários cobrem registro, consulta, validação do corpo, recomendação
    inexistente, propriedade da versão, autenticação e indisponibilidade. A
    classe existe para proteger o card F6.8 e a autorização das rotas.
    """

    async def test_registra_a_decisao_de_uma_recomendacao_da_propria_versao(self) -> None:
        """Grava e devolve a decisão sobre um aviso da revisão da própria versão.

        O teste decide sobre a cidade ausente e confere a resposta e o que foi
        gravado. Ele existe para o caminho feliz de ponta a ponta.
        """
        repositorio = RepositorioDecisaoMemoria()

        status, corpo = await _chamar(
            _app(repositorio),
            "PUT",
            _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor, CODIGO_DO_AVISO),
            {"decisao": "rejeitada"},
        )

        self.assertEqual(status, 200)
        self.assertEqual(corpo["codigo"], CODIGO_DO_AVISO)
        self.assertEqual(corpo["decisao"], "rejeitada")
        self.assertEqual(datetime.fromisoformat(corpo["decidida_em"]), INSTANTE)
        self.assertEqual(
            [(d.codigo, d.decisao.value) for d in repositorio.decisoes.values()],
            [(CODIGO_DO_AVISO, "rejeitada")],
        )

    async def test_decisao_fora_das_opcoes_responde_422(self) -> None:
        """Recusa uma decisão que não seja aceita nem rejeitada.

        O teste envia um valor fora do vocabulário. Ele existe para validar o
        corpo na fronteira, sem gravar nada.
        """
        repositorio = RepositorioDecisaoMemoria()

        status, _ = await _chamar(
            _app(repositorio),
            "PUT",
            _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor, CODIGO_DO_AVISO),
            {"decisao": "talvez"},
        )

        self.assertEqual(status, 422)
        self.assertEqual(repositorio.decisoes, {})

    async def test_codigo_que_nao_e_recomendacao_responde_404(self) -> None:
        """Responde 404 para um código que a revisão não aponta como aviso.

        O teste decide sobre um código inexistente. Ele existe para que não se
        grave decisão sobre recomendação inventada.
        """
        repositorio = RepositorioDecisaoMemoria()

        status, corpo = await _chamar(
            _app(repositorio),
            "PUT",
            _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor, "INVENTADO"),
            {"decisao": "aceita"},
        )

        self.assertEqual(status, 404)
        self.assertEqual(corpo, {"detail": "Recomendação não encontrada."})
        self.assertEqual(repositorio.decisoes, {})

    async def test_versao_de_outro_estudante_responde_404_sem_gravar(self) -> None:
        """Responde 404 para uma versão que não pertence ao estudante da sessão.

        O teste usa a própria sessão com uma versão que a prévia não reconhece.
        Ele existe para não revelar versões alheias nem gravar sobre elas.
        """
        repositorio = RepositorioDecisaoMemoria()

        status, corpo = await _chamar(
            _app(repositorio),
            "PUT",
            _caminho(ID_USUARIO_ESTAVEL.valor, OUTRO_USUARIO, CODIGO_DO_AVISO),
            {"decisao": "aceita"},
        )

        self.assertEqual(status, 404)
        self.assertEqual(corpo, {"detail": "Versão de currículo não encontrada."})
        self.assertEqual(repositorio.decisoes, {})

    async def test_outro_estudante_na_url_e_recusado_com_403(self) -> None:
        """Recusa decidir ou consultar quando a URL aponta para outro estudante.

        O teste usa a sessão de um estudante com a URL de outro, para o PUT e o
        GET. Ele existe para impedir o acesso às decisões de terceiros.
        """
        repositorio = RepositorioDecisaoMemoria()
        app = _app(repositorio)

        status_put, _ = await _chamar(
            app,
            "PUT",
            _caminho(OUTRO_USUARIO, ID_CURRICULO_ESTAVEL.valor, CODIGO_DO_AVISO),
            {"decisao": "aceita"},
        )
        status_get, _ = await _chamar(
            app, "GET", _caminho(OUTRO_USUARIO, ID_CURRICULO_ESTAVEL.valor)
        )

        self.assertEqual((status_put, status_get), (403, 403))
        self.assertEqual(repositorio.decisoes, {})

    async def test_sem_sessao_responde_401(self) -> None:
        """Exige sessão autenticada para decidir e para consultar.

        O teste omite o cookie de sessão. Ele existe para impedir o acesso
        anônimo às decisões.
        """
        repositorio = RepositorioDecisaoMemoria()
        app = _app(repositorio)

        status_put, _ = await _chamar(
            app,
            "PUT",
            _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor, CODIGO_DO_AVISO),
            {"decisao": "aceita"},
            autenticado=False,
        )
        status_get, _ = await _chamar(
            app,
            "GET",
            _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor),
            autenticado=False,
        )

        self.assertEqual((status_put, status_get), (401, 401))
        self.assertEqual(repositorio.decisoes, {})

    async def test_sem_executores_responde_503(self) -> None:
        """Responde 503 quando a decisão não foi composta.

        O teste monta a aplicação sem os executores. Ele existe para sinalizar
        indisponibilidade em vez de erro interno.
        """
        app = _app(RepositorioDecisaoMemoria(), com_executores=False)

        status_put, _ = await _chamar(
            app,
            "PUT",
            _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor, CODIGO_DO_AVISO),
            {"decisao": "aceita"},
        )
        status_get, _ = await _chamar(
            app, "GET", _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor)
        )

        self.assertEqual((status_put, status_get), (503, 503))

    async def test_lista_as_decisoes_ja_registradas_da_versao(self) -> None:
        """Devolve, na consulta, a decisão registrada antes pela mesma rota.

        O teste registra uma decisão e a consulta em seguida. Ele existe para
        provar que o que foi gravado volta ao estudante.
        """
        app = _app(RepositorioDecisaoMemoria())
        await _chamar(
            app,
            "PUT",
            _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor, CODIGO_DO_AVISO),
            {"decisao": "aceita"},
        )

        status, corpo = await _chamar(
            app, "GET", _caminho(ID_USUARIO_ESTAVEL.valor, ID_CURRICULO_ESTAVEL.valor)
        )

        self.assertEqual(status, 200)
        self.assertEqual(
            [(d["codigo"], d["decisao"]) for d in corpo["decisoes"]],
            [(CODIGO_DO_AVISO, "aceita")],
        )

    async def test_consulta_de_versao_alheia_responde_404(self) -> None:
        """Responde 404 ao consultar as decisões de uma versão que não é do estudante.

        O teste usa a própria sessão com uma versão desconhecida. Ele existe para
        não revelar a existência de versões de outras pessoas.
        """
        status, corpo = await _chamar(
            _app(RepositorioDecisaoMemoria()),
            "GET",
            _caminho(ID_USUARIO_ESTAVEL.valor, OUTRO_USUARIO),
        )

        self.assertEqual(status, 404)
        self.assertEqual(corpo, {"detail": "Versão de currículo não encontrada."})


class ContratoOpenApiDecisaoRecomendacaoTestCase(unittest.TestCase):
    """Verifica a documentação OpenAPI das rotas de decisão.

    O teste lê o schema gerado pela aplicação. A classe existe para que o
    Swagger mostre as operações e as respostas de erro das rotas.
    """

    def test_documenta_as_duas_rotas_com_tag_e_respostas(self) -> None:
        """Documenta o PUT e o GET com a tag de versões e as respostas de erro.

        O teste confere tags e códigos de resposta. Ele existe para manter o
        contrato publicado fiel aos handlers.
        """
        caminhos = create_app().openapi()["paths"]

        put = caminhos[CAMINHO_DECISAO]["put"]
        get = caminhos[CAMINHO_DECISOES]["get"]
        self.assertEqual(put["tags"], [TAG_VERSOES_CURRICULO])
        self.assertEqual(get["tags"], [TAG_VERSOES_CURRICULO])
        self.assertTrue({"200", "404", "422", "503"} <= set(put["responses"]))
        self.assertTrue({"200", "404", "503"} <= set(get["responses"]))
