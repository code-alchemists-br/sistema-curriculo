"""Isola handlers e DTOs de projeto usando requisições e executores doubles.

Chama endpoints diretamente sem aplicação ASGI ou servidor para verificar
tradução, identidade da sessão, erros seguros e metadados do corpo no Swagger.
"""

# Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
from json import JSONDecodeError
from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from fastapi import HTTPException

from backend.api.projeto_academico import EdicaoProjetoAcademicoRequisicao, criar_router
from backend.application import ProjetoAcademicoNaoEncontrado
from backend.domain import (
    ProjetoAcademico,
    ProjetoAcademicoId,
    RegraDeDominioViolada,
    UsuarioId,
)

USUARIO = UUID(int=2)
PROJETO = UUID(int=1)


def rotas(executor):
    """Extrai os handlers novos do router sem iniciar a aplicação.

    Registra o mesmo executor double nos três slots para permitir testes de
    tradução isolados, indexando as rotas parametrizadas pelo método HTTP.
    """
    router = criar_router(None, None, executor, executor, executor)
    return {next(iter(rota.methods)): rota for rota in router.routes
            if rota.path == "/projetos-academicos/{projeto_id}"}


class HandlersProjetoTestCase(IsolatedAsyncioTestCase):
    """Verifica tradução direta dos novos handlers com fronteiras substituídas.

    Usa executor e request mockados para observar entradas e falhas sem
    executar casos de uso, autenticação, contexto de aplicação ou banco.
    """

    def setUp(self):
        """Prepara executor e requisição doubles com dono fixo e corpo válido.

        Conserva estados em memória para que cada cenário altere somente uma
        fronteira relevante à tradução do handler.
        """
        self.projeto = ProjetoAcademico(ProjetoAcademicoId(PROJETO), UsuarioId(USUARIO),
                                       "Título", "Descrição", "Python")
        self.executor = Mock()
        self.executor.executar = AsyncMock(return_value=self.projeto)
        self.request = Mock()
        self.request.state = SimpleNamespace(usuario_id=USUARIO)
        self.request.json = AsyncMock(return_value={
            "titulo": " Novo ", "descricao": " Descrição ", "tecnologias": " Rust ",
            "usuario_id": str(UUID(int=9)), "id": str(UUID(int=8)),
        })

    async def test_sucesso_dto_explicito_e_dono_somente_da_sessao(self):
        """Exerce GET, PUT e DELETE verificando resposta e IDs delegados.

        Injeta dono e ID maliciosos no corpo e query double para garantir que
        apenas sessão e caminho formem a entrada, com DELETE sem conteúdo.
        """
        self.request.query_params = {"usuario_id": str(UUID(int=9))}
        self.request.path_params = {"usuario_id": str(UUID(int=9))}
        for metodo, rota in rotas(self.executor).items():
            with self.subTest(metodo=metodo):
                self.executor.executar.reset_mock()
                resposta = await rota.endpoint(str(PROJETO), self.request)
                entrada = self.executor.executar.await_args.args[0]
                self.assertEqual(entrada.usuario_id, UsuarioId(USUARIO))
                self.assertEqual(entrada.projeto_id, ProjetoAcademicoId(PROJETO))
                if metodo == "PUT":
                    self.assertEqual((entrada.titulo, entrada.descricao, entrada.tecnologias),
                                     (" Novo ", " Descrição ", " Rust "))
                if metodo == "DELETE":
                    self.assertEqual(resposta.status_code, 204)
                    self.assertEqual(resposta.body, b"")
                else:
                    self.assertEqual(resposta.model_dump(), {
                        "id": PROJETO, "usuario_id": USUARIO, "titulo": "Título",
                        "descricao": "Descrição", "tecnologias": "Python",
                    })
                    self.assertEqual(rota.status_code or 200, 200)

    async def test_404_uniforme_nao_reflete_falha_interna(self):
        """Simula ausência, dono alheio e exclusão através da falha contratual.

        Varia texto interno em todos os métodos para garantir mensagem 404
        idêntica sem vazar o motivo específico retornado pela Application.
        """
        for motivo in ("ausente", "alheio", "excluído"):
            self.executor.executar.side_effect = ProjetoAcademicoNaoEncontrado(motivo)
            for rota in rotas(self.executor).values():
                with self.assertRaises(HTTPException) as erro:
                    await rota.endpoint(str(PROJETO), self.request)
                self.assertEqual((erro.exception.status_code, erro.exception.detail),
                                 (404, "Projeto acadêmico não encontrado."))

    async def test_uuid_invalido_422_sem_eco_nem_execucao(self):
        """Recusa UUID textual inválido antes da delegação nos três handlers.

        Usa valor identificável para conferir mensagem genérica e ausência de
        chamada ao executor, sem depender da validação automática do framework.
        """
        for rota in rotas(self.executor).values():
            with self.assertRaises(HTTPException) as erro:
                await rota.endpoint("segredo-no-path", self.request)
            self.assertEqual(erro.exception.status_code, 422)
            self.assertNotIn("segredo", erro.exception.detail)
        self.executor.executar.assert_not_awaited()

    async def test_sem_sessao_401_inclusive_sem_executor(self):
        """Exige principal antes da disponibilidade ou corpo em cada operação.

        Remove o dono dos requests doubles e testa executores ausentes e
        presentes para garantir negação uniforme sem delegação.
        """
        self.request.state = SimpleNamespace()
        for executor in (None, self.executor):
            for rota in rotas(executor).values():
                with self.assertRaises(HTTPException) as erro:
                    await rota.endpoint(str(PROJETO), self.request)
                self.assertEqual(erro.exception.status_code, 401)
        self.executor.executar.assert_not_awaited()
        self.request.json.assert_not_awaited()

    async def test_executor_ausente_503_por_operacao(self):
        """Traduz executor ausente em mensagem específica com sessão válida.

        Chama cada handler sem capacidade injetada para evitar sucesso aparente
        quando o armazenamento não foi configurado.
        """
        mensagens = {"GET": "Consulta", "PUT": "Edição", "DELETE": "Exclusão"}
        for metodo, rota in rotas(None).items():
            with self.assertRaises(HTTPException) as erro:
                await rota.endpoint(str(PROJETO), self.request)
            self.assertEqual((erro.exception.status_code, erro.exception.detail),
                             (503, f"{mensagens[metodo]} indisponível."))

    async def test_put_corpo_invalido_422_sem_eco_e_sem_execucao(self):
        """Rejeita corpo malformado, incompleto e valores inválidos sem eco.

        Varia forma e limites via request mockado para impedir delegação antes
        da validação e manter textos recebidos fora das mensagens de erro.
        """
        rota = rotas(self.executor)["PUT"]
        for corpo in (None, [], {}, {"titulo": "segredo"},
                      {"titulo": "x" * 201, "descricao": "segredo", "tecnologias": "Go"},
                      {"titulo": 3, "descricao": "segredo", "tecnologias": "Go"}):
            self.request.json.return_value = corpo
            with self.assertRaises(HTTPException) as erro:
                await rota.endpoint(str(PROJETO), self.request)
            self.assertEqual(erro.exception.status_code, 422)
            self.assertNotIn("segredo", erro.exception.detail)
        self.request.json.side_effect = JSONDecodeError("segredo", "segredo", 0)
        with self.assertRaises(HTTPException) as erro:
            await rota.endpoint(str(PROJETO), self.request)
        self.assertEqual(erro.exception.status_code, 422)
        self.assertNotIn("segredo", erro.exception.detail)
        self.executor.executar.assert_not_awaited()

    async def test_put_regra_violada_422_seguro(self):
        """Mapeia violação do executor em mensagem genérica sem o texto interno.

        Injeta falha de domínio no double para verificar tradução após validação
        estrutural, mantendo o handler sem implementar regras do núcleo.
        """
        self.executor.executar.side_effect = RegraDeDominioViolada("texto-secreto")
        with self.assertRaises(HTTPException) as erro:
            await rotas(self.executor)["PUT"].endpoint(str(PROJETO), self.request)
        self.assertEqual(erro.exception.status_code, 422)
        self.assertNotIn("texto-secreto", erro.exception.detail)


class SchemaProjetoTestCase(TestCase):
    """Verifica metadados de DTO e decoradores sem gerar aplicação OpenAPI real.

    Inspeciona o schema de modelo e atributos locais de rotas para proteger
    documentação e validação pós-strip sem iniciar framework ou contrato externo.
    """

    def test_limites_documentados_e_validacao_pos_strip_unicode(self):
        """Confere min/max do schema e aceitação do limite com bordas externas.

        Compara strings Unicode nos três campos para garantir que metadata de
        documentação não introduza restrição de comprimento bruto no DTO.
        """
        schema = EdicaoProjetoAcademicoRequisicao.model_json_schema()
        self.assertEqual(set(schema["required"]), {"titulo", "descricao", "tecnologias"})
        for campo, limite in (("titulo", 200), ("descricao", 2000), ("tecnologias", 300)):
            self.assertEqual(schema["properties"][campo]["minLength"], 1)
            self.assertEqual(schema["properties"][campo]["maxLength"], limite)
            dados = {"titulo": "T", "descricao": "D", "tecnologias": "Go"}
            dados[campo] = "  " + "🙂" * limite + "  "
            dto = EdicaoProjetoAcademicoRequisicao.model_validate(dados)
            self.assertEqual(getattr(dto, campo), dados[campo])
        for metodo, rota in rotas(None).items():
            self.assertTrue(rota.summary)
            self.assertTrue(rota.description)
            self.assertTrue({401, 404, 422, 503}.issubset(rota.responses))
            if metodo == "PUT":
                corpo = rota.openapi_extra["requestBody"]["content"]["application/json"]["schema"]
                self.assertEqual(corpo, schema)
                self.assertIn("Unicode", rota.description)
