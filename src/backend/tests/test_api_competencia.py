"""Testa unitariamente a fronteira HTTP de cadastro, listagem e exclusão de competências."""

import unittest
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from backend.api.competencia import (
    CadastroCompetenciaRequisicao,
    criar_router,
)
from backend.api.factory import create_app
from backend.application.cadastro_competencia import (
    CadastrarCompetenciaEntrada,
    CompetenciaJaCadastrada,
)
from backend.application.competencia import (
    CompetenciaNaoEncontrada,
    ExcluirCompetenciaEntrada,
    ListarCompetenciasEntrada,
)
from backend.domain import CategoriaCompetencia, Competencia, CompetenciaId
from backend.domain.value_objects import UsuarioId

# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_COMPETENCIA = UUID("00000000-0000-0000-0000-0000000000c1")
ID_COMPETENCIA_2 = UUID("00000000-0000-0000-0000-0000000000c2")


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


class ListagemCompetenciasStub:
    """Substitui o caso de uso de listagem por dados em memória determinísticos.

    O double registra as entradas de consulta recebidas e retorna a sequência
    pré-configurada sem I/O. Ele existe para testar a fronteira HTTP de listagem
    em isolamento de infraestrutura.
    """

    def __init__(self, competencias: tuple[Competencia, ...] = ()) -> None:
        """Armazena a coleção retornada e inicializa o histórico de entradas.

        O construtor recebe os dados fixos e prepara a lista de chamadas. Ele
        existe para viabilizar simulações de sucesso e de coleção vazia.
        """
        self.competencias = competencias
        self.entradas: list[ListarCompetenciasEntrada] = []

    async def executar(
        self, entrada: ListarCompetenciasEntrada
    ) -> tuple[Competencia, ...]:
        """Registra o comando de busca e entrega a coleção pré-configurada.

        O método salva o parâmetro de chamada e devolve as instâncias sem acoplar
        o teste ao banco. Ele existe para validar o handler sem regras de negócio.
        """
        self.entradas.append(entrada)
        return self.competencias


class ExclusaoCompetenciaStub:
    """Substitui o caso de uso de exclusão por comportamento determinístico.

    O double armazena comandos de remoção e permite simular exclusão bem-sucedida
    ou ausência de registro. Ele existe para proteger a fronteira HTTP de deleção
    em testes unitários isolados.
    """

    def __init__(self, nao_encontrada: bool = False) -> None:
        """Configura se a operação deve simular ausência de registro.

        O construtor inicializa o sinalizador de erro e a lista de chamadas. Ele
        existe para viabilizar cenários de 204 No Content e de 404 Not Found.
        """
        self.nao_encontrada = nao_encontrada
        self.entradas: list[ExcluirCompetenciaEntrada] = []

    async def executar(self, entrada: ExcluirCompetenciaEntrada) -> None:
        """Registra a exclusão solicitada ou levanta CompetenciaNaoEncontrada.

        O método simula a porta de aplicação sem realizar operações de banco. Ele
        existe para testar o mapeamento de status e mensagens da rota DELETE.
        """
        self.entradas.append(entrada)
        if self.nao_encontrada:
            raise CompetenciaNaoEncontrada("Competência não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def _rota_post(router: APIRouter):
    """Obtém o endpoint POST de competência diretamente da tabela de rotas.

    A função percorre o router já configurado e devolve o handler sem iniciar
    servidor ASGI. Ela existe para manter o teste no nível unitário da
    fronteira, com executor e requisição controlados.
    """
    for rota in router.routes:
        if rota.path == "/competencias" and "POST" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota POST /competencias não encontrada.")


def _rota_get(router: APIRouter):
    """Obtém o endpoint GET de listagem de competências do router.

    A função busca a rota GET /competencias configurada e devolve seu endpoint.
    Ela existe para isolar a invocação direta do handler sem subir servidor HTTP.
    """
    for rota in router.routes:
        if rota.path == "/competencias" and "GET" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota GET /competencias não encontrada.")


def _rota_delete(router: APIRouter):
    """Obtém o endpoint DELETE de exclusão de competência do router.

    A função localiza a rota DELETE /competencias/{competencia_id} no router.
    Ela existe para permitir teste direto da função do handler sem ASGI.
    """
    for rota in router.routes:
        if rota.path == "/competencias/{competencia_id}" and "DELETE" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota DELETE /competencias/{competencia_id} não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def _request(
    usuario_id: UUID | None, metodo: str = "POST", caminho: str = "/competencias"
) -> Request:
    """Constrói uma requisição mínima com o principal opcional no estado.

    A função monta um escopo ASGI local e instala somente o UUID que seria
    fornecido pelo mecanismo existente. Ela existe para verificar a propriedade
    sem aceitar um identificador controlado pelo corpo HTTP.
    """
    request = Request(
        {"type": "http", "method": metodo, "path": caminho, "headers": []}
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
        cadastrar = _rota_post(criar_router(cadastrar_competencia=executor))

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
        cadastrar = _rota_post(
            criar_router(cadastrar_competencia=CadastroCompetenciaStub(duplicada=True))
        )

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
        cadastrar = _rota_post(criar_router(cadastrar_competencia=executor))

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

    async def test_cadastrar_sem_executor_retorna_503(self) -> None:
        """Retorna 503 quando o executor de cadastro não estiver configurado.

        O teste invoca o handler com router criado sem executor de cadastro. Ele
        existe para garantir a tradução padronizada de indisponibilidade de serviço.
        """
        cadastrar = _rota_post(criar_router(cadastrar_competencia=None))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroCompetenciaRequisicao(
                    categoria=CategoriaCompetencia.TECNICA,
                    descricao="Python",
                    nivel="Avançado",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_listar_competencias_retorna_lista_estruturada_do_usuario(
        self,
    ) -> None:
        """Retorna 200 e as competências pertencentes ao estudante autenticado.

        O teste consulta o endpoint GET com itens cadastrados no stub e valida a
        projeção para o DTO de listagem. Ele existe para garantir integridade e
        visibilidade correta das habilidades cadastradas.
        """
        comp1 = Competencia(
            id=CompetenciaId(ID_COMPETENCIA),
            usuario_id=UsuarioId(ID_USUARIO),
            categoria=CategoriaCompetencia.TECNICA,
            descricao="Python",
            nivel="Avançado",
        )
        comp2 = Competencia(
            id=CompetenciaId(ID_COMPETENCIA_2),
            usuario_id=UsuarioId(ID_USUARIO),
            categoria=CategoriaCompetencia.COMPORTAMENTAL,
            descricao="Comunicação",
            nivel="Básico",
        )
        executor = ListagemCompetenciasStub(competencias=(comp1, comp2))
        listar = _rota_get(criar_router(listar_competencias=executor))

        resposta = await listar(_request(ID_USUARIO, metodo="GET"))

        self.assertEqual(len(resposta.competencias), 2)
        self.assertEqual(resposta.competencias[0].id, ID_COMPETENCIA)
        self.assertEqual(resposta.competencias[0].descricao, "Python")
        self.assertEqual(resposta.competencias[1].id, ID_COMPETENCIA_2)
        self.assertEqual(resposta.competencias[1].descricao, "Comunicação")
        self.assertEqual(executor.entradas[0].usuario_id.valor, ID_USUARIO)

    async def test_listar_competencias_vazia_retorna_lista_vazia(self) -> None:
        """Retorna 200 com array vazio quando o estudante não possui competências.

        O teste invoca o handler GET com stub vazio e verifica a resposta
        estruturada. Ele existe para assegurar que ausência de dados não gera erro.
        """
        executor = ListagemCompetenciasStub(competencias=())
        listar = _rota_get(criar_router(listar_competencias=executor))

        resposta = await listar(_request(ID_USUARIO, metodo="GET"))

        self.assertEqual(resposta.competencias, [])
        self.assertEqual(executor.entradas[0].usuario_id.valor, ID_USUARIO)

    async def test_listar_competencias_sem_autenticacao_retorna_401(self) -> None:
        """Retorna 401 ao tentar listar competências sem principal na requisição.

        O teste omite o usuário na requisição ASGI e verifica a rejeição com 401.
        Ele existe para proteger a rota de consultas anônimas.
        """
        executor = ListagemCompetenciasStub()
        listar = _rota_get(criar_router(listar_competencias=executor))

        with self.assertRaises(HTTPException) as contexto:
            await listar(_request(None, metodo="GET"))

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    async def test_listar_competencias_sem_executor_retorna_503(self) -> None:
        """Retorna 503 quando o executor de listagem não estiver injetado.

        O teste cria o router sem executor de listagem e verifica a falha HTTP 503.
        Ele existe para expor indisponibilidade explícita de infraestrutura.
        """
        listar = _rota_get(criar_router(listar_competencias=None))

        with self.assertRaises(HTTPException) as contexto:
            await listar(_request(ID_USUARIO, metodo="GET"))

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_excluir_competencia_com_sucesso_retorna_204(self) -> None:
        """Remove a competência própria com sucesso e responde sem conteúdo.

        O teste chama o handler DELETE e confirma que a delegação ocorreu com os
        identificadores corretos do estudante e da competência. Ele existe para
        garantir reversibilidade da adição de competências.
        """
        executor = ExclusaoCompetenciaStub()
        excluir = _rota_delete(criar_router(excluir_competencia=executor))

        resultado = await excluir(
            ID_COMPETENCIA,
            _request(
                ID_USUARIO, metodo="DELETE", caminho=f"/competencias/{ID_COMPETENCIA}"
            ),
        )

        self.assertIsNone(resultado)
        self.assertEqual(len(executor.entradas), 1)
        self.assertEqual(executor.entradas[0].competencia_id.valor, ID_COMPETENCIA)
        self.assertEqual(executor.entradas[0].usuario_id.valor, ID_USUARIO)

    async def test_excluir_competencia_inexistente_ou_alheia_retorna_404(self) -> None:
        """Traduz CompetenciaNaoEncontrada em HTTP 404 Not Found.

        O teste configura o stub para falhar com a exceção de domínio/aplicação e
        verifica o status 404. Ele existe para evitar vazamento de propriedade.
        """
        executor = ExclusaoCompetenciaStub(nao_encontrada=True)
        excluir = _rota_delete(criar_router(excluir_competencia=executor))

        with self.assertRaises(HTTPException) as contexto:
            await excluir(
                ID_COMPETENCIA,
                _request(
                    ID_USUARIO,
                    metodo="DELETE",
                    caminho=f"/competencias/{ID_COMPETENCIA}",
                ),
            )

        self.assertEqual(contexto.exception.status_code, 404)
        self.assertEqual(contexto.exception.detail, "Competência não encontrada.")

    async def test_excluir_competencia_sem_autenticacao_retorna_401(self) -> None:
        """Rejeita exclusão sem usuário autenticado com status 401.

        O teste envia requisição sem principal na sessão e valida a recusa
        imediata. Ele existe para impedir exclusões não autorizadas.
        """
        executor = ExclusaoCompetenciaStub()
        excluir = _rota_delete(criar_router(excluir_competencia=executor))

        with self.assertRaises(HTTPException) as contexto:
            await excluir(
                ID_COMPETENCIA,
                _request(
                    None, metodo="DELETE", caminho=f"/competencias/{ID_COMPETENCIA}"
                ),
            )

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    async def test_excluir_competencia_sem_executor_retorna_503(self) -> None:
        """Retorna 503 quando o executor de exclusão não estiver injetado.

        O teste chama o handler sem executor de deleção e verifica a falha HTTP.
        Ele existe para expor indisponibilidade clara de serviço.
        """
        excluir = _rota_delete(criar_router(excluir_competencia=None))

        with self.assertRaises(HTTPException) as contexto:
            await excluir(
                ID_COMPETENCIA,
                _request(
                    ID_USUARIO,
                    metodo="DELETE",
                    caminho=f"/competencias/{ID_COMPETENCIA}",
                ),
            )

        self.assertEqual(contexto.exception.status_code, 503)

    def test_fabrica_registra_rotas_de_competencias(self) -> None:
        """Mantém os endpoints de competência disponíveis na aplicação composta.

        O teste cria somente a fábrica FastAPI e consulta o contrato OpenAPI,
        sem iniciar servidor ou injetar infraestrutura. Ele existe para evitar
        que o router seja implementado mas fique desconectado da API pública.
        """
        app = create_app()
        paths = app.openapi()["paths"]

        self.assertIn("/competencias", paths)
        self.assertIn("post", paths["/competencias"])
        self.assertIn("get", paths["/competencias"])
        self.assertIn("/competencias/{competencia_id}", paths)
        self.assertIn("delete", paths["/competencias/{competencia_id}"])
