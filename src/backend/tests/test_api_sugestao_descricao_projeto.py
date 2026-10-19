"""Testa a rota HTTP de sugestão de descrição de projeto e sua falha controlada."""

import json
import unittest
from typing import Any
from uuid import UUID

from backend.api.factory import create_app
from backend.api.sessoes import COOKIE_SESSAO
from backend.application import (
    AssistenteDescricaoProjetoAusente,
    AssistenteDescricaoProjetoDeterministico,
    AssistenteDescricaoProjetoEntrada,
    AssistenteDescricaoProjetoSaida,
)
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.domain import RegraDeDominioViolada, UsuarioId

CAMINHO = "/projetos-academicos/sugestao-descricao"
CREDENCIAL_VALIDA = "credencial-sintetica-sugestao"
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
CORPO_VALIDO = {"titulo": "Sistema de Currículos", "tecnologias": "Python, FastAPI"}


class AutenticadorSessaoStub(AutenticadorSessao):
    """Autentica somente a credencial sintética do cenário.

    O double devolve o estudante do teste para o token conhecido e ``None``
    para qualquer outro. Ele existe para exercitar o middleware real de sessão
    sem banco de sessões.
    """

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Devolve o estudante do teste apenas para a credencial conhecida.

        O método compara o token recebido sem consultar serviços. Ele existe
        para que a rota só responda a requisições autenticadas.
        """
        return UsuarioId(ID_USUARIO) if token == CREDENCIAL_VALIDA else None


class AssistenteEspiao:
    """Substitui o assistente registrando chamadas e simulando falhas.

    O double devolve uma sugestão fixa ou levanta o erro configurado. Ele
    existe para observar se a rota chamou o assistente e como traduziu cada
    falha.
    """

    def __init__(self, erro: Exception | None = None) -> None:
        """Guarda o erro opcional e inicia o histórico de entradas.

        O construtor mantém apenas estado em memória. Ele existe para que cada
        cenário configure sucesso ou falha.
        """
        self.erro = erro
        self.entradas: list[AssistenteDescricaoProjetoEntrada] = []

    async def sugerir_descricao(
        self, entrada: AssistenteDescricaoProjetoEntrada
    ) -> AssistenteDescricaoProjetoSaida:
        """Registra a entrada e devolve a sugestão fixa ou levanta o erro.

        O método não executa regra real. Ele existe para isolar a tradução HTTP
        da estratégia concreta.
        """
        self.entradas.append(entrada)
        if self.erro is not None:
            raise self.erro
        return AssistenteDescricaoProjetoSaida(descricao="Sugestão fixa.")


class RepositorioProjetoQueNaoDeveSerUsado:
    """Falha se a rota tentar cadastrar um projeto.

    O double implementa o executor de cadastro levantando erro em qualquer
    chamada. Ele existe para provar que pedir uma sugestão nunca salva nada.
    """

    async def executar(self, entrada: object) -> object:
        """Falha imediatamente se o cadastro for acionado.

        O método não persiste nada. Ele existe para tornar visível qualquer
        gravação indevida durante a sugestão.
        """
        raise AssertionError("A sugestão de descrição não pode salvar projeto.")


async def _postar(
    app: object, corpo: object, credencial: str | None = CREDENCIAL_VALIDA
) -> tuple[int, dict[str, Any]]:
    """Envia um POST de sugestão diretamente à aplicação ASGI.

    A função serializa o corpo, inclui o cookie de sessão quando informado e
    coleta status e JSON da resposta. Ela existe para observar a resposta real
    emitida pelo FastAPI, sem servidor nem cliente externo.
    """
    corpo_bytes = json.dumps(corpo).encode()
    cabecalhos = [
        (b"content-type", b"application/json"),
        (b"content-length", str(len(corpo_bytes)).encode()),
    ]
    if credencial is not None:
        cabecalhos.append((b"cookie", f"{COOKIE_SESSAO}={credencial}".encode()))
    escopo = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": CAMINHO,
        "raw_path": CAMINHO.encode(),
        "query_string": b"",
        "headers": cabecalhos,
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


def _app(**dependencias: object):
    """Compõe a aplicação com middleware de sessão e dependências do cenário.

    A fábrica real recebe o autenticador sintético e o executor de cadastro que
    falha se usado, além do assistente configurado pelo teste. Ela existe para
    exercitar autenticação, validação e composição reais.
    """
    return create_app(
        autenticador_sessao=AutenticadorSessaoStub(),
        cadastrar_projeto_academico=RepositorioProjetoQueNaoDeveSerUsado(),
        **dependencias,
    )


class SugestaoDescricaoProjetoApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a rota de sugestão pela aplicação montada.

    Os cenários enviam requisições reais à aplicação ASGI e inspecionam status
    e corpo. A classe existe para proteger o contrato público da sugestão e a
    falha controlada do assistente.
    """

    async def test_sugestao_padrao_responde_200_somente_com_descricao(self) -> None:
        """Usa a estratégia sem IA por padrão e devolve só o texto sugerido.

        A aplicação é criada sem assistente informado; a resposta deve ser 200,
        conter apenas ``descricao`` e coincidir com a estratégia determinística.
        O teste existe para garantir a orientação sempre disponível do RF04.
        """
        esperado = await AssistenteDescricaoProjetoDeterministico().sugerir_descricao(
            AssistenteDescricaoProjetoEntrada(**CORPO_VALIDO)
        )

        status_resposta, corpo = await _postar(_app(), CORPO_VALIDO)

        self.assertEqual(status_resposta, 200)
        self.assertEqual(corpo, {"descricao": esperado.descricao})

    async def test_encaminha_titulo_e_tecnologias_ao_assistente(self) -> None:
        """Entrega ao assistente exatamente os campos recebidos.

        O assistente espião registra a entrada e a resposta usa seu texto. O
        teste existe para que a rota apenas traduza o transporte.
        """
        assistente = AssistenteEspiao()

        status_resposta, corpo = await _postar(
            _app(assistente_descricao_projeto=assistente),
            {**CORPO_VALIDO, "usuario_id": str(UUID(int=999))},
        )

        self.assertEqual(status_resposta, 200)
        self.assertEqual(corpo, {"descricao": "Sugestão fixa."})
        self.assertEqual(
            assistente.entradas,
            [AssistenteDescricaoProjetoEntrada(**CORPO_VALIDO)],
        )

    async def test_assistente_desligado_responde_503_controlado(self) -> None:
        """Responde 503 com mensagem controlada quando o assistente está ausente.

        A aplicação recebe ``AssistenteDescricaoProjetoAusente``, que sempre
        sinaliza indisponibilidade. O teste existe para cobrir a falha
        controlada pedida pelo card, sem erro 500.
        """
        status_resposta, corpo = await _postar(
            _app(assistente_descricao_projeto=AssistenteDescricaoProjetoAusente()),
            CORPO_VALIDO,
        )

        self.assertEqual(status_resposta, 503)
        self.assertEqual(corpo, {"detail": "Assistente de descrição indisponível."})

    async def test_regra_violada_no_assistente_responde_422_generico(self) -> None:
        """Converte a recusa do assistente em 422 sem expor o texto interno.

        O assistente espião levanta ``RegraDeDominioViolada`` com detalhe
        confidencial. O teste existe para manter a resposta pública genérica.
        """
        assistente = AssistenteEspiao(erro=RegraDeDominioViolada("detalhe confidencial"))

        status_resposta, corpo = await _postar(
            _app(assistente_descricao_projeto=assistente), CORPO_VALIDO
        )

        self.assertEqual(status_resposta, 422)
        self.assertEqual(
            corpo, {"detail": "Os dados informados não permitem sugerir uma descrição."}
        )

    async def test_corpo_invalido_responde_422_sem_chamar_o_assistente(self) -> None:
        """Barra na fronteira corpos malformados, sem acionar o assistente.

        Os cenários cobrem campo ausente, tipo errado, título vazio, textos
        acima dos limites, caractere de controle e JSON que não é objeto. O
        teste existe para que só entradas válidas cheguem ao assistente.
        """
        cenarios = {
            "título ausente": {"tecnologias": "Python"},
            "tecnologias ausentes": {"titulo": "Projeto"},
            "título numérico": {"titulo": 123, "tecnologias": "Python"},
            "título vazio": {"titulo": "   ", "tecnologias": "Python"},
            "título acima de 200": {"titulo": "A" * 201, "tecnologias": "Python"},
            "tecnologias acima de 300": {"titulo": "Projeto", "tecnologias": "A" * 301},
            "controle no título": {"titulo": "Pro\x00jeto", "tecnologias": "Python"},
            "corpo não objeto": ["Projeto", "Python"],
        }
        for descricao, corpo in cenarios.items():
            with self.subTest(cenario=descricao):
                assistente = AssistenteEspiao()

                status_resposta, resposta = await _postar(
                    _app(assistente_descricao_projeto=assistente), corpo
                )

                self.assertEqual(status_resposta, 422)
                self.assertEqual(
                    resposta, {"detail": "Dados da sugestão de descrição inválidos."}
                )
                self.assertEqual(assistente.entradas, [])

    async def test_tecnologias_vazias_sao_aceitas(self) -> None:
        """Aceita pedir sugestão antes de informar as tecnologias.

        O corpo envia tecnologias em branco e a estratégia padrão usa o modelo
        sem tecnologias. O teste existe para que o estudante receba orientação
        logo no início do preenchimento.
        """
        status_resposta, corpo = await _postar(
            _app(), {"titulo": "Pesquisa sobre Acessibilidade", "tecnologias": ""}
        )

        self.assertEqual(status_resposta, 200)
        self.assertTrue(
            corpo["descricao"].startswith("Pesquisa sobre Acessibilidade é um projeto acadêmico.")
        )

    async def test_sem_sessao_responde_401(self) -> None:
        """Recusa a sugestão sem credencial ou com credencial inválida.

        As requisições são enviadas sem cookie e com cookie desconhecido. O
        teste existe para que a rota privada não seja usada anonimamente.
        """
        for credencial in (None, "credencial-invalida"):
            with self.subTest(credencial=credencial):
                assistente = AssistenteEspiao()

                status_resposta, _ = await _postar(
                    _app(assistente_descricao_projeto=assistente),
                    CORPO_VALIDO,
                    credencial=credencial,
                )

                self.assertEqual(status_resposta, 401)
                self.assertEqual(assistente.entradas, [])

    def test_openapi_documenta_rota_respostas_e_contrato(self) -> None:
        """Publica a rota na tag de projetos com respostas e campos obrigatórios.

        O teste inspeciona o documento OpenAPI da aplicação. Ele existe para
        que o contrato consumido pelo frontend reflita a implementação.
        """
        documento = create_app().openapi()
        operacao = documento["paths"][CAMINHO]["post"]
        esquemas = documento["components"]["schemas"]

        self.assertIn("Projetos acadêmicos", operacao["tags"])
        self.assertTrue({"200", "422", "503"} <= set(operacao["responses"]))
        self.assertEqual(esquemas["SugestaoDescricaoProjetoResposta"]["required"], ["descricao"])
        requisicao = operacao["requestBody"]["content"]["application/json"]["schema"]
        self.assertEqual(set(requisicao["required"]), {"titulo", "tecnologias"})
