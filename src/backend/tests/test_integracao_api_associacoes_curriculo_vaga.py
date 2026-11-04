"""Integra a rota de associações com middleware, sessões e persistência reais."""

# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001

import unittest
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import FastAPI

from backend.api.associacoes_curriculo_vaga import CAMINHO_LISTAGEM_ASSOCIACOES
from backend.api.documentacao_openapi import (
    ESQUEMA_SESSAO,
    TAG_ASSOCIACOES_CURRICULO_VAGA,
)
from backend.api.factory import create_app
from backend.domain.associacao_curriculo_vaga import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
)
from backend.domain.value_objects import CurriculoId, VagaId
from backend.infrastructure.persistence.sqlalchemy.acesso_estudante import (
    AutenticadorSessaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.associacao_curriculo_vaga import (
    para_registro,
    para_registros_classificacoes,
)
from backend.infrastructure.persistence.sqlalchemy.curriculo import CurriculoRegistro
from backend.infrastructure.persistence.sqlalchemy.listar_associacoes_curriculo_vaga import (
    ListarAssociacoesCurriculoVagaSqlAlchemy,
)
from backend.tests.fixtures.credenciais_sessao import (
    AIOSQLITE_DISPONIVEL,
    USUARIO_A,
    USUARIO_B,
    BancoCredenciaisSessao,
    RespostaCredenciais,
    solicitar_asgi,
)

CURRICULO_A_INICIAL = UUID(int=201)
CURRICULO_B = UUID(int=202)
CURRICULO_A_FINAL = UUID(int=203)
VAGA_A_INICIAL = "vaga-z"
VAGA_B = "vaga-b"
VAGA_A_FINAL = "vaga-a"


@unittest.skipUnless(
    AIOSQLITE_DISPONIVEL,
    "aiosqlite ausente; execute no ambiente Nix tests preparado",
)
class ListagemAssociacoesCurriculoVagaIntegracaoTestCase(
    unittest.IsolatedAsyncioTestCase
):
    """Exercita a API com autenticação persistida e banco descartável migrado.

    Cada teste compõe a fábrica HTTP com o middleware e os adapters SQLAlchemy
    reais, usando dados sintéticos e sessões persistidas em SQLite temporário.
    A classe existe para validar o contrato integrado da listagem sem servidor
    ou banco compartilhado.
    """

    async def asyncSetUp(self) -> None:
        """Prepara banco migrado, associações A/B, sessões válidas e aplicação.

        O fixture existente cria um SQLite descartável com usuários reais; o
        setup persiste associações e emite cookies ativos para cada estudante.
        Ele existe para que cada cenário atravesse as fronteiras de API,
        autenticação e repositório sem compartilhar estado com outros testes.
        """
        self.banco = BancoCredenciaisSessao()
        self.addAsyncCleanup(self.banco.fechar)
        await self.banco.preparar()

        expiracao = datetime.now(timezone.utc) + timedelta(days=1)
        self.token_a = await self.banco.semear_sessao(
            2441, USUARIO_A, expira_em=expiracao
        )
        self.token_b = await self.banco.semear_sessao(
            2442, USUARIO_B, expira_em=expiracao
        )
        await self._semear_associacoes()
        self.app = self._criar_app()

    def _criar_app(self, *, executor_disponivel: bool = True) -> FastAPI:
        """Compõe a rota com middleware e adapters SQLAlchemy reais.

        A fábrica usa autenticação de sessão persistida e injeta o executor real
        ou sua ausência, sem iniciar servidor nem substituir a persistência. Ela
        existe para testar tanto o fluxo funcional quanto o 503 de composição.
        """
        return create_app(
            autenticador_sessao=AutenticadorSessaoSqlAlchemy(self.banco.sessoes),
            listar_associacoes_curriculo_vaga=(
                ListarAssociacoesCurriculoVagaSqlAlchemy(self.banco.sessoes)
                if executor_disponivel
                else None
            ),
        )

    async def _semear_associacoes(self) -> None:
        """Persiste uma associação de B entre duas associações de A.

        O cenário grava currículos e agregados reais em ordem global A/B/A,
        incluindo múltiplas classificações e candidatura normalizada pelo
        domínio. Ele existe para provar isolamento anterior à paginação e
        serialização correta dos valores persistidos.
        """
        associacoes = (
            AssociacaoCurriculoVaga(
                CurriculoId(CURRICULO_A_INICIAL),
                VagaId(VAGA_A_INICIAL),
                (
                    ClassificacaoAssociacao.CANDIDATURA,
                    ClassificacaoAssociacao.COMPATIBILIDADE,
                ),
            ),
            AssociacaoCurriculoVaga(
                CurriculoId(CURRICULO_B),
                VagaId(VAGA_B),
                (ClassificacaoAssociacao.COMPATIBILIDADE,),
            ),
            AssociacaoCurriculoVaga(
                CurriculoId(CURRICULO_A_FINAL),
                VagaId(VAGA_A_FINAL),
                (ClassificacaoAssociacao.INTERESSE,),
            ),
        )
        curriculos = (
            (CURRICULO_A_INICIAL, USUARIO_A, "Currículo privado A inicial"),
            (CURRICULO_B, USUARIO_B, "Currículo privado B"),
            (CURRICULO_A_FINAL, USUARIO_A, "Currículo privado A final"),
        )

        async with self.banco.sessoes() as sessao:
            sessao.add_all(
                [
                    CurriculoRegistro(
                        id=curriculo_id,
                        usuario_id=usuario_id,
                        titulo_versao=titulo,
                        layout="classico",
                        is_public=False,
                    )
                    for curriculo_id, usuario_id, titulo in curriculos
                ]
            )
            await sessao.flush()
            for associacao in associacoes:
                sessao.add(para_registro(associacao))
                sessao.add_all(para_registros_classificacoes(associacao))
            await sessao.commit()

    async def _requisitar(
        self,
        token: str | None,
        query: str,
        *,
        app: FastAPI | None = None,
    ) -> RespostaCredenciais:
        """Executa GET pela interface ASGI usando a sessão fornecida.

        A chamada usa o harness ASGI existente, sem socket ou servidor, e
        preserva a sessão no cookie contratado pela API. Ela existe para que
        as asserções observem respostas HTTP completas da aplicação composta.
        """
        return await solicitar_asgi(
            app or self.app,
            "GET",
            CAMINHO_LISTAGEM_ASSOCIACOES,
            token=token,
            query=query,
        )

    async def test_responde_associacoes_com_classificacoes_e_ordem_estaveis(
        self,
    ) -> None:
        """Confere status, DTO mínimo e ordem estável dos dados persistidos.

        A sessão A consulta sua coleção completa e compara IDs, campos e
        classificações, inclusive interesse implícito em candidatura. O teste
        existe para proteger o contrato HTTP observável da listagem real.
        """
        resposta = await self._requisitar(
            self.token_a,
            "offset=0&limit=10",
        )

        self.assertEqual(resposta.status, 200)
        corpo = resposta.json()
        self.assertEqual(
            set(corpo),
            {"associacoes"},
        )
        self.assertEqual(
            [
                (item["curriculo_id"], item["vaga_id"], item["classificacoes"])
                for item in corpo["associacoes"]
            ],
            [
                (
                    str(CURRICULO_A_INICIAL),
                    VAGA_A_INICIAL,
                    ["candidatura", "compatibilidade", "interesse"],
                ),
                (
                    str(CURRICULO_A_FINAL),
                    VAGA_A_FINAL,
                    ["interesse"],
                ),
            ],
        )
        for item in corpo["associacoes"]:
            self.assertEqual(
                set(item),
                {"curriculo_id", "vaga_id", "classificacoes"},
            )

    async def test_exige_sessao_valida_para_consultar(self) -> None:
        """Retorna 401 para cookie ausente e token não persistido.

        O middleware valida ambos os casos contra o repositório de sessões real,
        sem executar a consulta de associação. Ele existe para comprovar a
        autenticação da rota por sessão em vez de identidade recebida no pedido.
        """
        sem_sessao = await self._requisitar(None, "offset=0&limit=1")
        sessao_invalida = await self._requisitar(
            "token-sintetico-invalido",
            "offset=0&limit=1",
        )

        self.assertEqual(sem_sessao.status, 401)
        self.assertEqual(sessao_invalida.status, 401)
        self.assertEqual(
            sem_sessao.json(),
            {"detail": "Sessão ausente ou inválida."},
        )
        self.assertEqual(
            sessao_invalida.json(),
            {"detail": "Sessão ausente ou inválida."},
        )

    async def test_isola_estudantes_e_filtra_proprietario_antes_da_paginacao(
        self,
    ) -> None:
        """Comprova isolamento A/B e páginas próprias contíguas.

        As linhas persistidas estão ordenadas globalmente A/B/A; consultas A
        com páginas unitárias devem retornar as duas linhas próprias sem que a
        de B consuma offset, e consulta B deve retornar somente sua linha. Ele
        existe para detectar vazamento e paginação aplicada antes do filtro.
        """
        pagina_a_inicial = await self._requisitar(
            self.token_a,
            "offset=0&limit=1",
        )
        pagina_a_final = await self._requisitar(
            self.token_a,
            "offset=1&limit=1",
        )
        pagina_b = await self._requisitar(
            self.token_b,
            "offset=0&limit=1",
        )
        identidade_cliente = await self._requisitar(
            self.token_a,
            f"offset=0&limit=10&usuario_id={USUARIO_B}",
        )

        self.assertEqual(
            pagina_a_inicial.json(),
            {
                "associacoes": [
                    {
                        "curriculo_id": str(CURRICULO_A_INICIAL),
                        "vaga_id": VAGA_A_INICIAL,
                        "classificacoes": [
                            "candidatura",
                            "compatibilidade",
                            "interesse",
                        ],
                    }
                ]
            },
        )
        self.assertEqual(
            pagina_a_final.json(),
            {
                "associacoes": [
                    {
                        "curriculo_id": str(CURRICULO_A_FINAL),
                        "vaga_id": VAGA_A_FINAL,
                        "classificacoes": ["interesse"],
                    }
                ]
            },
        )
        self.assertEqual(
            pagina_b.json(),
            {
                "associacoes": [
                    {
                        "curriculo_id": str(CURRICULO_B),
                        "vaga_id": VAGA_B,
                        "classificacoes": ["compatibilidade"],
                    }
                ]
            },
        )
        self.assertEqual(
            [item["curriculo_id"] for item in identidade_cliente.json()["associacoes"]],
            [str(CURRICULO_A_INICIAL), str(CURRICULO_A_FINAL)],
        )
        for resposta in (
            pagina_a_inicial,
            pagina_a_final,
            pagina_b,
            identidade_cliente,
        ):
            self.assertEqual(resposta.status, 200)

    async def test_pagina_sem_resultados_retorna_colecao_vazia(self) -> None:
        """Representa página além do fim como sucesso com lista vazia.

        A consulta autenticada de A usa offset igual à quantidade de itens
        próprios persistidos e espera `associacoes` vazia. Ela existe para
        distinguir ausência de resultados de indisponibilidade da API.
        """
        resposta = await self._requisitar(
            self.token_a,
            "offset=2&limit=1",
        )

        self.assertEqual(resposta.status, 200)
        self.assertEqual(resposta.json(), {"associacoes": []})

    async def test_parametros_invalidos_ou_ausentes_retorna_422(self) -> None:
        """Rejeita parâmetros de paginação negativos, nulos ou não informados.

        Cada consulta usa sessão válida para que a validação HTTP seja observada
        antes do caso de uso. O teste existe para fixar obrigatoriedade e limites
        de offset e limit no contrato público.
        """
        consultas = (
            "offset=-1&limit=1",
            "offset=0&limit=0",
            "offset=0",
            "limit=1",
        )

        for query in consultas:
            with self.subTest(query=query):
                resposta = await self._requisitar(self.token_a, query)
                self.assertEqual(resposta.status, 422)

    async def test_executor_ausente_retorna_503_com_sessao_valida(self) -> None:
        """Sinaliza dependência não composta sem mascarar como página vazia.

        O cenário monta create_app com middleware real e executor de listagem
        ausente, depois autentica por token persistido. Ele existe para proteger
        o contrato explícito de indisponibilidade da composição.
        """
        app_sem_executor = self._criar_app(executor_disponivel=False)
        resposta = await self._requisitar(
            self.token_a,
            "offset=0&limit=1",
            app=app_sem_executor,
        )

        self.assertEqual(resposta.status, 503)
        self.assertEqual(
            resposta.json(),
            {"detail": "Listagem de associações indisponível."},
        )

    def test_openapi_declara_rota_privada_e_dto_minimo(self) -> None:
        """Valida o schema documentado para autenticação, query e resposta.

        O schema OpenAPI da aplicação compõe a rota privada com cookie de sessão,
        query obrigatória e propriedades mínimas de associação. Ele existe para
        detectar divergências entre a interface executável e seu contrato.
        """
        schema = self.app.openapi()
        operacao = schema["paths"][CAMINHO_LISTAGEM_ASSOCIACOES]["get"]

        self.assertEqual(operacao["tags"], [TAG_ASSOCIACOES_CURRICULO_VAGA])
        self.assertEqual(operacao["security"], [{ESQUEMA_SESSAO: []}])
        parametros = {item["name"]: item for item in operacao["parameters"]}
        self.assertEqual(set(parametros), {"offset", "limit"})
        self.assertTrue(parametros["offset"]["required"])
        self.assertTrue(parametros["limit"]["required"])

        componentes = schema["components"]["schemas"]
        resposta_ref = operacao["responses"]["200"]["content"]["application/json"][
            "schema"
        ]["$ref"].rsplit("/", 1)[-1]
        resposta_schema = componentes[resposta_ref]
        self.assertEqual(set(resposta_schema["properties"]), {"associacoes"})
        item_ref = resposta_schema["properties"]["associacoes"]["items"]["$ref"].rsplit(
            "/", 1
        )[-1]
        item_schema = componentes[item_ref]
        self.assertEqual(
            set(item_schema["properties"]),
            {"curriculo_id", "vaga_id", "classificacoes"},
        )
