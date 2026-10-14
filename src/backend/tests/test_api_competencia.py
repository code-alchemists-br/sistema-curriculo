"""Testa unitariamente a fronteira HTTP de cadastro de competências."""

import unittest
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from backend.api.competencia import CadastroCompetenciaRequisicao, criar_router
from backend.api.factory import create_app
from backend.application.cadastro_competencia import (
    CadastrarCompetenciaEntrada,
    CompetenciaJaCadastrada,
)
from backend.domain import CategoriaCompetencia, Competencia, CompetenciaId

# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_COMPETENCIA = UUID("00000000-0000-0000-0000-0000000000c1")


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class CadastroCompetenciaStub:
    """Substitui o caso de uso por comportamento determinístico em memória.

    O double registra a entrada recebida e constrói a resposta sem banco,
    framework ou rede. Ele existe para isolar a conversão exercida pelo handler
    HTTP e permitir cenários de sucesso e conflito.
    """

    def __init__(self, duplicada: bool = False) -> None:
        """Prepara o histórico de chamadas e o resultado configurável.

        O construtor conserva apenas estado local usado pelo teste. Ele existe
        para representar o executor injetado sem introduzir dependências
        externas na unidade de interface.
        """
        self.duplicada = duplicada
        self.entradas: list[CadastrarCompetenciaEntrada] = []

    async def executar(self, entrada: CadastrarCompetenciaEntrada) -> Competencia:
        """Registra a entrada e devolve ou rejeita a competência configurada.

        O método simula o contrato público do caso de uso usando somente dados
        em memória. Ele existe para verificar que a API traduz corretamente a
        chamada e a falha sem testar regras internas.
        """
        self.entradas.append(entrada)
        if self.duplicada:
            raise CompetenciaJaCadastrada("A competência já está cadastrada.")
        return Competencia(
            id=CompetenciaId(ID_COMPETENCIA),
            usuario_id=entrada.usuario_id,
            categoria=entrada.categoria,
            descricao=entrada.descricao,
            nivel=entrada.nivel,
        )


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def _rota(router: APIRouter):
    """Obtém o endpoint POST de competência diretamente da tabela de rotas.

    A função percorre o router já configurado e devolve o handler sem iniciar
    servidor ASGI. Ela existe para manter o teste no nível unitário da
    fronteira, com executor e requisição controlados.
    """
    for rota in router.routes:
        if rota.path == "/competencias" and "POST" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota POST /competencias não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def _request(usuario_id: UUID | None) -> Request:
    """Constrói uma requisição mínima com o principal opcional no estado.

    A função monta um escopo ASGI local e instala somente o UUID que seria
    fornecido pelo mecanismo existente. Ela existe para verificar a propriedade
    sem aceitar um identificador controlado pelo corpo HTTP.
    """
    request = Request(
        {"type": "http", "method": "POST", "path": "/competencias", "headers": []}
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class CadastroCompetenciaRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução entre transporte HTTP e executor de competência.

    A classe chama o handler decorado com doubles locais, sem criar aplicação
    FastAPI nem servidor. Ela existe para proteger o contrato de fronteira no
    nível unitário apropriado.
    """

    async def test_vincula_a_competencia_ao_principal_autenticado(self) -> None:
        """Encaminha categoria e textos, usando o UUID instalado na requisição.

        O cenário invoca o handler e inspeciona a entrada entregue ao double.
        Ele existe para impedir que a API derive o proprietário do payload ou
        exponha a entidade de domínio na resposta.
        """
        executor = CadastroCompetenciaStub()
        cadastrar = _rota(criar_router(executor))

        resposta = await cadastrar(
            CadastroCompetenciaRequisicao(
                categoria=CategoriaCompetencia.TECNICA,
                descricao="Python",
                nivel="Avançado",
            ),
            _request(ID_USUARIO),
        )

        self.assertEqual(resposta.id, ID_COMPETENCIA)
        self.assertEqual(resposta.usuario_id, ID_USUARIO)
        self.assertEqual(resposta.categoria, CategoriaCompetencia.TECNICA)
        self.assertEqual(executor.entradas[0].usuario_id.valor, ID_USUARIO)

    async def test_traduz_duplicidade_para_conflito(self) -> None:
        """Apresenta 409 quando o executor informa competência já cadastrada.

        O cenário usa o double configurado para falhar e observa a exceção HTTP
        gerada pelo handler. Ele existe para manter o conflito compreensível e
        não revelar dados persistidos de qualquer outra conta.
        """
        cadastrar = _rota(criar_router(CadastroCompetenciaStub(duplicada=True)))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroCompetenciaRequisicao(
                    categoria=CategoriaCompetencia.TECNICA,
                    descricao="Python",
                    nivel="Avançado",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 409)

    async def test_rejeita_requisicao_sem_principal(self) -> None:
        """Retorna 401 sem invocar o executor para requisição anônima.

        O cenário omite o estado de autenticação e compara o histórico do
        double. Ele existe para garantir que o endpoint depende do principal
        fornecido pelo mecanismo de borda já existente.
        """
        executor = CadastroCompetenciaStub()
        cadastrar = _rota(criar_router(executor))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroCompetenciaRequisicao(
                    categoria=CategoriaCompetencia.TECNICA,
                    descricao="Python",
                    nivel="Avançado",
                ),
                _request(None),
            )

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    def test_fabrica_registra_rota_de_competencias(self) -> None:
        """Mantém o endpoint de competência disponível na aplicação composta.

        O teste cria somente a fábrica FastAPI e consulta o contrato OpenAPI,
        sem iniciar servidor ou injetar infraestrutura. Ele existe para evitar
        que o router seja implementado mas fique desconectado da API pública.
        """
        app = create_app()

        self.assertIn("/competencias", app.openapi()["paths"])
