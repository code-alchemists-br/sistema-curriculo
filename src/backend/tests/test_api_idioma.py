"""Testa unitariamente a fronteira HTTP de cadastro de idiomas."""

import unittest
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
from backend.api.factory import create_app
from backend.api.idioma import CadastroIdiomaRequisicao, criar_router
from backend.application.cadastro_idioma import (
    CadastrarIdiomaEntrada,
    IdiomaJaCadastrado,
)
from backend.domain import Idioma, IdiomaId, RegraDeDominioViolada

# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_IDIOMA = UUID("00000000-0000-0000-0000-0000000000d1")


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class CadastroIdiomaStub:
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
        self.entradas: list[CadastrarIdiomaEntrada] = []

    async def executar(self, entrada: CadastrarIdiomaEntrada) -> Idioma:
        """Registra a entrada e devolve ou rejeita o idioma configurado.

        O método simula o contrato público do caso de uso usando somente dados
        em memória. Ele existe para verificar que a API traduz corretamente a
        chamada e a falha sem testar regras internas.
        """
        self.entradas.append(entrada)
        if self.erro_dominio is not None:
            raise RegraDeDominioViolada(self.erro_dominio)
        if self.duplicado:
            raise IdiomaJaCadastrado("O idioma já está cadastrado.")
        return Idioma(
            id=IdiomaId(ID_IDIOMA),
            usuario_id=entrada.usuario_id,
            idioma=entrada.idioma,
            nivel=entrada.nivel,
        )


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
def _rota(router: APIRouter):
    """Obtém o endpoint POST de idioma diretamente da tabela de rotas.

    A função percorre o router já configurado e devolve o handler sem iniciar
    servidor ASGI. Ela existe para manter o teste no nível unitário da
    fronteira, com executor e requisição controlados.
    """
    for rota in router.routes:
        if rota.path == "/idiomas" and "POST" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota POST /idiomas não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
def _request(usuario_id: UUID | None) -> Request:
    """Constrói uma requisição mínima com o principal opcional no estado.

    A função monta um escopo ASGI local e instala somente o UUID que seria
    fornecido pelo mecanismo existente. Ela existe para verificar a propriedade
    sem aceitar um identificador controlado pelo corpo HTTP.
    """
    request = Request(
        {"type": "http", "method": "POST", "path": "/idiomas", "headers": []}
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class CadastroIdiomaRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução entre transporte HTTP e executor de idioma.

    A classe chama o handler decorado com doubles locais, sem criar aplicação
    FastAPI nem servidor. Ela existe para proteger o contrato de fronteira no
    nível unitário apropriado.
    """

    async def test_vincula_o_idioma_ao_principal_autenticado(self) -> None:
        """Encaminha denominação e nível, usando o UUID instalado na requisição.

        O cenário invoca o handler e inspeciona a entrada entregue ao double.
        Ele existe para impedir que a API derive o proprietário do payload ou
        exponha a entidade de domínio na resposta.
        """
        executor = CadastroIdiomaStub()
        cadastrar = _rota(criar_router(executor))

        resposta = await cadastrar(
            CadastroIdiomaRequisicao(
                idioma="Inglês",
                nivel="Avançado",
            ),
            _request(ID_USUARIO),
        )

        self.assertEqual(resposta.id, ID_IDIOMA)
        self.assertEqual(resposta.usuario_id, ID_USUARIO)
        self.assertEqual(resposta.idioma, "Inglês")
        self.assertEqual(resposta.nivel, "Avançado")
        self.assertEqual(executor.entradas[0].usuario_id.valor, ID_USUARIO)

    async def test_traduz_duplicidade_para_conflito(self) -> None:
        """Apresenta 409 quando o executor informa idioma já cadastrado.

        O cenário usa o double configurado para falhar e observa a exceção HTTP
        gerada pelo handler. Ele existe para manter o conflito compreensível e
        não revelar dados persistidos de qualquer outra conta.
        """
        cadastrar = _rota(criar_router(CadastroIdiomaStub(duplicado=True)))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroIdiomaRequisicao(
                    idioma="Inglês",
                    nivel="Avançado",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 409)
        self.assertEqual(contexto.exception.detail, "O idioma já está cadastrado.")

    async def test_traduz_regra_de_dominio_violada_para_422(self) -> None:
        """Apresenta 422 quando o domínio rejeita os dados do idioma.

        O cenário simula a falha de validação de domínio e observa a resposta
        HTTP unprocessable. Ele existe para traduzir erros de regra de negócio
        em respostas compreensíveis ao cliente HTTP.
        """
        cadastrar = _rota(
            criar_router(
                CadastroIdiomaStub(erro_dominio="O idioma exige denominação preenchida.")
            )
        )

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroIdiomaRequisicao(
                    idioma="   ",
                    nivel="Avançado",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(
            contexto.exception.detail, "O idioma exige denominação preenchida."
        )

    async def test_rejeita_requisicao_sem_principal(self) -> None:
        """Retorna 401 sem invocar o executor para requisição anônima.

        O cenário omite o estado de autenticação e compara o histórico do
        double. Ele existe para garantir que o endpoint depende do principal
        fornecido pelo mecanismo de borda já existente.
        """
        executor = CadastroIdiomaStub()
        cadastrar = _rota(criar_router(executor))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroIdiomaRequisicao(
                    idioma="Inglês",
                    nivel="Avançado",
                ),
                _request(None),
            )

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(contexto.exception.detail, "Autenticação necessária.")
        self.assertEqual(executor.entradas, [])

    async def test_retorna_503_quando_executor_nao_disponivel(self) -> None:
        """Retorna 503 quando o executor não foi fornecido à fábrica de router.

        O cenário instancia o router com None e tenta cadastrar um idioma.
        Ele existe para indicar indisponibilidade controlada do serviço quando
        a dependência não estiver disponível.
        """
        cadastrar = _rota(criar_router(None))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroIdiomaRequisicao(
                    idioma="Inglês",
                    nivel="Avançado",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Cadastro indisponível.")

    def test_fabrica_registra_rota_de_idiomas(self) -> None:
        """Mantém o endpoint de idioma disponível na aplicação composta.

        O teste cria somente a fábrica FastAPI e consulta o contrato OpenAPI,
        sem iniciar servidor ou injetar infraestrutura. Ele existe para evitar
        que o router seja implementado mas fique desconectado da API pública.
        """
        app = create_app()

        self.assertIn("/idiomas", app.openapi()["paths"])
