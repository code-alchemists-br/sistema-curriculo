"""Testa unitariamente a fronteira HTTP de cadastro de certificações."""

import json
import unittest
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from starlette.requests import Request

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
from backend.api.certificacao import (
    CadastroCertificacaoRequisicao,
    criar_router,
)
from backend.api.factory import create_app
from backend.application.cadastro_certificacao import (
    CadastrarCertificacaoEntrada,
    CertificacaoJaCadastrada,
)
from backend.domain import (
    Certificacao,
    CertificacaoId,
    RegraDeDominioViolada,
)

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_CERTIFICACAO = UUID("00000000-0000-0000-0000-0000000000c1")


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class CadastroCertificacaoStub:
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
        self.entradas: list[CadastrarCertificacaoEntrada] = []

    async def executar(
        self, entrada: CadastrarCertificacaoEntrada
    ) -> Certificacao:
        """Registra a entrada e devolve ou rejeita a certificação configurada.

        O método simula o contrato público do caso de uso usando somente dados
        em memória. Ele existe para verificar que a API traduz corretamente a
        chamada e a falha sem testar regras internas.
        """
        self.entradas.append(entrada)
        if self.erro_dominio is not None:
            raise RegraDeDominioViolada(self.erro_dominio)
        if self.duplicado:
            raise CertificacaoJaCadastrada("A certificação já está cadastrada.")
        return Certificacao(
            id=CertificacaoId(ID_CERTIFICACAO),
            usuario_id=entrada.usuario_id,
            nome=entrada.nome,
            organizacao_emissora=entrada.organizacao_emissora,
        )


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
def _rota(router: APIRouter):
    """Obtém o endpoint POST de certificação diretamente da tabela de rotas.

    A função percorre o router já configurado e devolve o handler sem iniciar
    servidor ASGI. Ela existe para manter o teste no nível unitário da
    fronteira, com executor e requisição controlados.
    """
    for rota in router.routes:
        if rota.path == "/certificacoes" and "POST" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota POST /certificacoes não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
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
            "path": "/certificacoes",
            "headers": [],
        }
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class CadastroCertificacaoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução entre transporte HTTP e executor de certificação.

    A classe chama o handler decorado com doubles locais, sem criar aplicação
    FastAPI nem servidor. Ela existe para proteger o contrato de fronteira no
    nível unitário apropriado.
    """

    async def test_vincula_a_certificacao_ao_principal_autenticado(
        self,
    ) -> None:
        """Encaminha nome e emissor, usando o UUID instalado na requisição.

        O cenário invoca o handler e inspeciona a entrada entregue ao double.
        Ele existe para impedir que a API derive o proprietário do payload ou
        exponha a entidade de domínio na resposta.
        """
        executor = CadastroCertificacaoStub()
        cadastrar = _rota(criar_router(executor))

        resposta = await cadastrar(
            CadastroCertificacaoRequisicao(
                nome="AWS Certified Solutions Architect",
                organizacao_emissora="Amazon Web Services",
            ),
            _request(ID_USUARIO),
        )

        self.assertEqual(resposta.id, ID_CERTIFICACAO)
        self.assertEqual(resposta.usuario_id, ID_USUARIO)
        self.assertEqual(
            resposta.nome, "AWS Certified Solutions Architect"
        )
        self.assertEqual(
            resposta.organizacao_emissora, "Amazon Web Services"
        )
        self.assertEqual(executor.entradas[0].usuario_id.valor, ID_USUARIO)

    async def test_traduz_duplicidade_para_conflito(self) -> None:
        """Apresenta 409 quando o executor informa certificação já cadastrada.

        O cenário usa o double configurado para falhar e observa a exceção HTTP
        gerada pelo handler. Ele existe para manter o conflito compreensível e
        não revelar dados persistidos de qualquer outra conta.
        """
        cadastrar = _rota(
            criar_router(CadastroCertificacaoStub(duplicado=True))
        )

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroCertificacaoRequisicao(
                    nome="AWS Certified Solutions Architect",
                    organizacao_emissora="Amazon Web Services",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 409)
        self.assertEqual(
            contexto.exception.detail, "A certificação já está cadastrada."
        )

    async def test_traduz_regra_de_dominio_violada_para_422_generico(self) -> None:
        """Apresenta 422 genérico quando o domínio rejeita a certificação.

        O cenário recebe uma requisição válida na fronteira, mas o executor
        sinaliza uma regra violada com texto confidencial; a resposta usa
        mensagem genérica. Ele existe para não expor o texto interno das
        regras de domínio ao cliente HTTP.
        """
        cadastrar = _rota(
            criar_router(
                CadastroCertificacaoStub(erro_dominio="detalhe interno confidencial")
            )
        )

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroCertificacaoRequisicao(
                    nome="AWS Certified Solutions Architect",
                    organizacao_emissora="Amazon Web Services",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(
            contexto.exception.detail,
            "A certificação informada viola as regras de cadastro.",
        )
        self.assertNotIn("confidencial", contexto.exception.detail)

    async def test_rejeita_requisicao_sem_principal(self) -> None:
        """Retorna 401 sem invocar o executor para requisição anônima.

        O cenário omite o estado de autenticação e compara o histórico do
        double. Ele existe para garantir que o endpoint depende do principal
        fornecido pelo mecanismo de borda já existente.
        """
        executor = CadastroCertificacaoStub()
        cadastrar = _rota(criar_router(executor))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroCertificacaoRequisicao(
                    nome="AWS Certified Solutions Architect",
                    organizacao_emissora="Amazon Web Services",
                ),
                _request(None),
            )

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(contexto.exception.detail, "Autenticação necessária.")
        self.assertEqual(executor.entradas, [])

    async def test_retorna_503_quando_executor_nao_disponivel(self) -> None:
        """Retorna 503 quando o executor não foi fornecido à fábrica de router.

        O cenário instancia o router com None e tenta cadastrar uma certificação.
        Ele existe para indicar indisponibilidade controlada do serviço quando
        a dependência não estiver disponível.
        """
        cadastrar = _rota(criar_router(None))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroCertificacaoRequisicao(
                    nome="AWS Certified Solutions Architect",
                    organizacao_emissora="Amazon Web Services",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Cadastro indisponível.")

    def test_fabrica_registra_rota_de_certificacoes(self) -> None:
        """Mantém o endpoint de certificação disponível na aplicação composta.

        O teste cria somente a fábrica FastAPI e consulta o contrato OpenAPI,
        sem iniciar servidor ou injetar infraestrutura. Ele existe para evitar
        que o router seja implementado mas fique desconectado da API pública.
        """
        app = create_app()

        self.assertIn("/certificacoes", app.openapi()["paths"])


def _payload(**alteracoes: object) -> dict[str, object]:
    """Monta um corpo JSON válido com alterações pontuais.

    O dicionário parte de nome e emissor válidos e permite sobrescrever ou
    acrescentar campos. Ele existe para manter os cenários de validação
    focados no campo observado.
    """
    dados: dict[str, object] = {
        "nome": "AWS Certified Solutions Architect",
        "organizacao_emissora": "Amazon Web Services",
    }
    dados.update(alteracoes)
    return dados


async def _enviar_json(app: object, corpo: dict[str, object]) -> int:
    """Envia um POST /certificacoes diretamente à aplicação ASGI.

    A função serializa o corpo, entrega-o uma única vez e captura apenas o
    status da resposta. Ela existe para exercitar a validação da requisição
    feita pelo FastAPI sem servidor nem cliente externo.
    """
    corpo_bytes = json.dumps(corpo).encode()
    escopo = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/certificacoes",
        "raw_path": b"/certificacoes",
        "query_string": b"",
        "headers": [
            (b"content-type", b"application/json"),
            (b"content-length", str(len(corpo_bytes)).encode()),
        ],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }
    recebido = False
    status = 0

    async def receber() -> dict[str, object]:
        """Entrega o corpo da chamada ASGI uma única vez."""
        nonlocal recebido
        if recebido:
            return {"type": "http.disconnect"}
        recebido = True
        return {"type": "http.request", "body": corpo_bytes, "more_body": False}

    async def enviar(mensagem: dict[str, object]) -> None:
        """Captura o status emitido pela aplicação."""
        nonlocal status
        if mensagem["type"] == "http.response.start":
            status = int(mensagem["status"])

    await app(escopo, receber, enviar)  # type: ignore[operator]
    return status


class ValidacaoRequisicaoCertificacaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a validação do corpo de cadastro de certificação na fronteira.

    Os cenários validam o DTO diretamente e pela aplicação montada. A classe
    existe para garantir que requisições malformadas sejam barradas com 422
    antes de chegar ao caso de uso.
    """

    def test_rejeita_campos_invalidos(self) -> None:
        """Rejeita ausência, tipo errado, vazio, excesso e caractere de controle.

        Cada cenário altera um campo do corpo válido e exige
        ``ValidationError``. O teste existe para cobrir formato, tipo e campos
        obrigatórios exigidos na fronteira.
        """
        sem_nome = _payload()
        del sem_nome["nome"]
        sem_emissor = _payload()
        del sem_emissor["organizacao_emissora"]
        cenarios = {
            "nome ausente": sem_nome,
            "emissor ausente": sem_emissor,
            "nome numérico": _payload(nome=123),
            "emissor nulo": _payload(organizacao_emissora=None),
            "nome só com espaços": _payload(nome="   "),
            "emissor vazio": _payload(organizacao_emissora=""),
            "nome acima de 200": _payload(nome="A" * 201),
            "emissor acima de 200": _payload(organizacao_emissora="A" * 201),
            "controle no nome": _payload(nome="AWS\x00Architect"),
            "quebra de linha no emissor": _payload(organizacao_emissora="Amazon\nWeb"),
        }
        for descricao, dados in cenarios.items():
            with self.subTest(cenario=descricao):
                with self.assertRaises(ValidationError):
                    CadastroCertificacaoRequisicao.model_validate(dados)

    def test_apara_espacos_e_aceita_limite_de_200(self) -> None:
        """Remove espaços externos e aceita textos com exatamente 200 caracteres.

        O cenário envia textos com espaços nas pontas e no limite máximo. Ele
        existe para que a fronteira use a mesma regra de tamanho do domínio,
        medida depois do aparo.
        """
        texto = "A" * 200

        requisicao = CadastroCertificacaoRequisicao.model_validate(
            _payload(nome=f"  {texto}  ", organizacao_emissora="  Amazon Web Services ")
        )

        self.assertEqual(requisicao.nome, texto)
        self.assertEqual(requisicao.organizacao_emissora, "Amazon Web Services")

    def test_ignora_usuario_id_enviado_no_corpo(self) -> None:
        """Descarta o proprietário enviado pelo cliente no corpo da requisição.

        O cenário inclui ``usuario_id`` no JSON e confere que o DTO não o
        guarda. Ele existe para que o dono venha somente da sessão autenticada.
        """
        requisicao = CadastroCertificacaoRequisicao.model_validate(
            _payload(usuario_id=str(UUID(int=999)))
        )

        self.assertFalse(hasattr(requisicao, "usuario_id"))

    async def test_requisicao_invalida_responde_422_sem_chamar_executor(self) -> None:
        """Responde 422 pela aplicação montada sem acionar o caso de uso.

        O teste envia um corpo com nome em branco à aplicação criada pela
        fábrica e confere o status e o histórico vazio do executor. Ele existe
        para provar que a validação acontece antes da Application.
        """
        executor = CadastroCertificacaoStub()
        app = create_app(cadastrar_certificacao=executor)

        status = await _enviar_json(app, _payload(nome="   "))

        self.assertEqual(status, 422)
        self.assertEqual(executor.entradas, [])

    def test_openapi_exige_nome_e_organizacao_emissora(self) -> None:
        """Publica nome e organização emissora como campos obrigatórios.

        O teste inspeciona o esquema da requisição no OpenAPI da aplicação. Ele
        existe para que o contrato documentado reflita a validação aplicada.
        """
        esquemas = create_app().openapi()["components"]["schemas"]

        obrigatorios = set(esquemas["CadastroCertificacaoRequisicao"]["required"])

        self.assertEqual(obrigatorios, {"nome", "organizacao_emissora"})
