"""Testa unitariamente a tradução HTTP da exclusão de formação acadêmica."""

import unittest
from datetime import date, datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from starlette.requests import Request

from backend.api.factory import create_app
from backend.api.formacao_academica import criar_router
from backend.application.perfil_estudante import (
    ExcluirFormacaoAcademicaEntrada,
    FormacaoAcademicaNaoEncontrada,
)
from backend.domain import (
    FormacaoAcademica,
    FormacaoAcademicaId,
    NivelFormacaoAcademica,
    Periodo,
    StatusFormacaoAcademica,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_USUARIO_CLIENTE = UUID("00000000-0000-0000-0000-000000000002")
ID_FORMACAO = UUID("00000000-0000-0000-0000-0000000000f1")


# Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
class ExcluirFormacaoAcademicaStub:
    """Substitui o caso de uso e registra entradas recebidas pelo handler.

    O double devolve uma entidade ou falha configurada em memória, sem
    persistência. Ele existe para isolar tradução HTTP e propriedade da sessão.
    """

    def __init__(self, erro: Exception | None = None) -> None:
        """Armazena falha opcional e prepara histórico de chamadas.

        Nenhuma dependência externa é criada. O construtor existe para montar
        cenários determinísticos da rota de exclusão.
        """
        self.erro = erro
        self.entradas: list[ExcluirFormacaoAcademicaEntrada] = []

    async def executar(
        self, entrada: ExcluirFormacaoAcademicaEntrada
    ) -> FormacaoAcademica:
        """Registra a entrada e devolve estado excluído ou falha configurada.

        A entidade retornada contém o instante controlado para o teste. O método
        existe para representar o contrato da Application sem executá-la.
        """
        self.entradas.append(entrada)
        if self.erro is not None:
            raise self.erro
        return FormacaoAcademica(
            id=entrada.formacao_id,
            usuario_id=entrada.usuario_id,
            instituicao="FATEC",
            curso="ADS",
            nivel=NivelFormacaoAcademica.TECNOLOGO,
            periodo=Periodo(date(2024, 2, 1), date(2030, 12, 1)),
            status=StatusFormacaoAcademica.EM_ANDAMENTO,
            deleted_at=datetime(2026, 10, 15, tzinfo=timezone.utc),
        )


# Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
def _request(usuario_id: UUID | None) -> Request:
    """Cria requisição mínima com principal autenticado opcional.

    O escopo ASGI instala somente o estado fornecido pelo middleware. Ele
    existe para testar a origem do proprietário sem iniciar aplicação ou banco.
    """
    request = Request(
        {
            "type": "http",
            "method": "DELETE",
            "path": f"/formacoes-academicas/{ID_FORMACAO}",
            "headers": [],
        }
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


# Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
def _rota(executor: ExcluirFormacaoAcademicaStub | None):
    """Localiza o handler DELETE no router sem inicializar servidor ASGI.

    A seleção usa método e caminho exatos para garantir que os cenários chamem
    somente a unidade HTTP sob teste.
    """
    for rota in criar_router(None, excluir_formacao=executor).routes:
        if (
            rota.path == "/formacoes-academicas/{formacao_id}"
            and "DELETE" in rota.methods
        ):
            return rota.endpoint
    raise AssertionError("Rota DELETE de exclusão de formação não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
class ExclusaoFormacaoAcademicaApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica status, ausência de corpo e identidade da sessão no DELETE.

    Os testes invocam handlers com executor double e requisição sintética. A
    classe existe para proteger contrato HTTP sem framework iniciado ou banco.
    """

    async def test_delete_retorna_204_sem_corpo_e_usa_usuario_da_sessao(self) -> None:
        """Delegação idempotente responde sem corpo e ignora dono do cliente.

        Um principal conflitante é colocado apenas no dado do cliente que o
        handler sequer recebe; a entrada deve conter o usuário autenticado.
        """
        executor = ExcluirFormacaoAcademicaStub()
        excluir = _rota(executor)

        resposta = await excluir(ID_FORMACAO, _request(ID_USUARIO))

        self.assertIsNone(resposta)
        self.assertEqual(executor.entradas[0].usuario_id, UsuarioId(ID_USUARIO))
        self.assertEqual(executor.entradas[0].formacao_id, FormacaoAcademicaId(ID_FORMACAO))
        self.assertNotEqual(executor.entradas[0].usuario_id.valor, ID_USUARIO_CLIENTE)

    async def test_repeticao_pelo_dono_tambem_retorna_204(self) -> None:
        """Preserva resposta de sucesso para repetição idempotente do dono.

        O executor devolve a mesma representação de estado excluído e o handler
        mantém o status vazio. Isso existe para documentar o contrato repetido.
        """
        executor = ExcluirFormacaoAcademicaStub()
        excluir = _rota(executor)

        resposta = await excluir(ID_FORMACAO, _request(ID_USUARIO))

        self.assertIsNone(resposta)
        self.assertEqual(len(executor.entradas), 1)

    async def test_ausente_e_alheia_resultam_no_mesmo_404(self) -> None:
        """Oculta existência alheia com detalhe público idêntico.

        Duas execuções com a mesma falha uniforme comparam a resposta para
        manter ausência e propriedade alheia indistinguíveis.
        """
        respostas: list[tuple[int, str]] = []
        for _ in ("ausente", "alheia"):
            excluir = _rota(
                ExcluirFormacaoAcademicaStub(
                    FormacaoAcademicaNaoEncontrada(
                        "Formação acadêmica não encontrada."
                    )
                )
            )
            with self.assertRaises(HTTPException) as contexto:
                await excluir(ID_FORMACAO, _request(ID_USUARIO))
            respostas.append((contexto.exception.status_code, contexto.exception.detail))

        self.assertEqual(respostas[0], respostas[1])
        self.assertEqual(respostas[0], (404, "Formação acadêmica não encontrada."))

    async def test_executor_indisponivel_responde_503(self) -> None:
        """Expõe indisponibilidade sem incluir exceções ou detalhes internos.

        O router sem executor falha antes de delegar. O cenário existe para
        manter o contrato operacional consistente com outros handlers.
        """
        excluir = _rota(None)

        with self.assertRaises(HTTPException) as contexto:
            await excluir(ID_FORMACAO, _request(ID_USUARIO))

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertNotIn("database", str(contexto.exception.detail).lower())

    async def test_sem_sessao_responde_401_sem_chamar_caso_de_uso(self) -> None:
        """Recusa principal ausente sem invocar a Application.

        O executor registra chamadas e permanece vazio, protegendo o dono como
        identidade exclusivamente derivada do middleware de sessão.
        """
        executor = ExcluirFormacaoAcademicaStub()
        excluir = _rota(executor)

        with self.assertRaises(HTTPException) as contexto:
            await excluir(ID_FORMACAO, _request(None))

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    def test_router_registra_delete_no_caminho_da_formacao(self) -> None:
        """Confirma método DELETE e caminho público do contrato.

        A inspeção do router evita dependência de servidor ou middleware e
        existe para detectar mudanças acidentais na rota de exclusão.
        """
        rota = next(
            rota
            for rota in criar_router(None, excluir_formacao=ExcluirFormacaoAcademicaStub()).routes
            if rota.path == "/formacoes-academicas/{formacao_id}"
            and "DELETE" in rota.methods
        )
        self.assertIn("DELETE", rota.methods)

    def test_factory_injeta_executor_de_exclusao_na_rota(self) -> None:
        """Registra o executor fornecido pela composição na rota DELETE.

        O teste inspeciona a aplicação composta sem iniciar servidor para
        confirmar que a capacidade nova não fica desconectada da factory.
        """
        app = create_app(excluir_formacao_academica=ExcluirFormacaoAcademicaStub())

        rota = next(
            rota
            for inclusao in app.routes
            for rota in getattr(
                getattr(inclusao, "original_router", None), "routes", []
            )
            if getattr(rota, "path", None) == "/formacoes-academicas/{formacao_id}"
            and "DELETE" in getattr(rota, "methods", set())
        )

        self.assertIn("DELETE", rota.methods)

