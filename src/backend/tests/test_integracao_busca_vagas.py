"""Caracteriza A01–A10 pela API ASGI real, isolando provedor e identidade.

Reutiliza solicitar_asgi/RespostaCredenciais sem banco para verificar contratos,
recusas, controles positivos e sensibilidade com caso de uso e adapter reais.
Não é E2E integrado: não há navegador, página roteada no App, schemas compatíveis
entre associacoes e vagas/total, executor em main nem provedor real. Não prova
layout, acessibilidade, desempenho ou composição produtiva. Critérios inferidos
do título, sem aceite oficial do card. O prefixo test_ é desvio autorizado da
análise: a suíte sem banco/aiosqlite entra no discover do CI por decisão do usuário.
"""

# Proveniência: decision-analysis prompts/frontend/20261024-181303-cenario-busca-vagas-tres-desfechos-v001.md#v001

import unittest
from json import dumps
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlsplit
from uuid import UUID

from fastapi import FastAPI, Request

from backend.api.factory import create_app
from backend.application.consulta_vagas import ConsultarVagas, ErroIntegracaoVagas
from backend.infrastructure.integrations.cliente_vagas_grupo2 import (
    ClienteApiVagasGrupo2Http,
)
from backend.tests.fixtures.busca_vagas_integracao import (
    TOKEN_ACEITO,
    URL_PROVEDOR,
    AutenticadorVagasFake,
    PortaVagasCanonicaFake,
    TransporteVagasRegistrado,
    bytes_resultado,
    criar_app_busca_vagas,
    vagas_sinteticas,
)
from backend.tests.fixtures.credenciais_sessao import (
    RespostaCredenciais,
    solicitar_asgi,
)

FILTROS = {"localizacao": "Cidade Sintética", "modalidade": "REMOTO"}
DETALHE_TIMEOUT = "Tempo limite esgotado ao consultar vagas externas. Tente novamente mais tarde."
DETALHE_INVALIDO = "Não foi possível obter dados válidos do serviço de vagas no momento."


def vagas_esperadas() -> list[dict]:
    """Define o resultado esperado após normalização dos dois campos nulos.

    Ajusta explicitamente a segunda vaga da massa sem chamar o mapper real,
    fornecendo oráculo independente para detectar regressão na serialização.
    """
    vagas = vagas_sinteticas()
    vagas[1]["localizacao"] = ""
    vagas[1]["url_candidatura"] = ""
    return vagas


def app_com_state_de_teste(executor, identidade=None) -> FastAPI:
    """Cria configuração auxiliar sem middleware real de sessão para A09.

    Instala middleware exclusivamente de teste que injeta string/UUID quando
    solicitado, permitindo caracterizar o guard do handler sem provar login.
    """
    app = create_app(consultar_vagas=executor)
    if identidade is not None:
        @app.middleware("http")
        async def injetar_state_exclusivo_do_teste(request: Request, call_next):
            """Injeta o valor previsto no state somente neste app auxiliar.

            Delega à rota real após a atribuição para distinguir identidade
            inválida de UUID válido, sem substituir o guard de produção.
            """
            request.state.usuario_id = identidade
            return await call_next(request)
    return app


class BuscaVagasSistemaApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Exercita os dez cenários por HTTP ASGI com controles causais e sem egress.

    Monta dependências novas por teste e verifica status/corpo e registros,
    para distinguir recusa legítima de rota ou provedor que sempre falham.
    """

    def setUp(self) -> None:
        """Isola transporte/autenticador e bloqueia qualquer saída de rede.

        Instala mocks verificados no cleanup, inclusive se o produto capturar
        sua exceção, para impedir que uma chamada externa passe despercebida.
        """
        self.transporte = TransporteVagasRegistrado()
        self.autenticador = AutenticadorVagasFake()
        self.app = criar_app_busca_vagas(self.transporte, self.autenticador)
        for alvo in ("urllib.request.urlopen", "socket.create_connection",
                     "socket.socket.connect", "socket.socket.connect_ex"):
            substituicao = patch(alvo, side_effect=AssertionError("Egress proibido na busca."))
            bloqueio = substituicao.start()
            self.addCleanup(substituicao.stop)
            self.addCleanup(bloqueio.assert_not_called)

    async def solicitar(
        self, termo="Python", filtros=None, *, app=None, token=TOKEN_ACEITO, extras=None,
    ) -> RespostaCredenciais:
        """Envia critérios pela query e identidade pelo cookie no harness existente.

        Usa urlencode e solicitar_asgi sem banco ou state manual no caminho
        principal para observar routing, middleware e serialização reais.
        """
        parametros = {"termo": termo, **(FILTROS if filtros is None else filtros), **(extras or {})}
        return await solicitar_asgi(
            self.app if app is None else app, "GET", "/vagas", token=token,
            query=urlencode(parametros),
        )

    def verificar_resultado(self, resposta, termo="Python", filtros=None, vagas=None) -> None:
        """Exige sucesso, schema, lista não vazia e conteúdo exato da consulta.

        Compara todos os campos e exclui erro/vazio para que respostas truthy
        ou outro estado não satisfaçam o oráculo de resultado positivo.
        """
        corpo = resposta.json()
        esperadas = vagas_esperadas() if vagas is None else vagas
        self.assertEqual(resposta.status, 200)
        self.assertIs(type(corpo["total"]), int)
        self.assertGreater(corpo["total"], 0)
        self.assertEqual(corpo, {"termo": termo, "filtros": FILTROS if filtros is None else filtros,
                                 "total": len(esperadas), "vagas": esperadas})

    def verificar_vazio(self, resposta, termo="Python", filtros=None) -> None:
        """Exige 200 e envelope vazio com critérios exatos, sem campos de erro.

        Compara o corpo integral e o tipo do total para separar ausência de
        vagas de resultado preenchido, falha externa ou resposta incompleta.
        """
        self.assertEqual(resposta.status, 200)
        corpo = resposta.json()
        self.assertIs(type(corpo["total"]), int)
        self.assertEqual(corpo, {"termo": termo, "filtros": FILTROS if filtros is None else filtros,
                                 "total": 0, "vagas": []})

    def verificar_erro(self, resposta, status, detalhe) -> None:
        """Exige status e detalhe públicos literais, excluindo dados e vazamentos.

        Verifica o envelope inteiro e termos técnicos proibidos para evitar
        aprovação por qualquer erro ou por corpo com resultados residuais.
        """
        self.assertEqual(resposta.status, status)
        self.assertEqual(resposta.json(), {"detail": detalhe})
        for proibido in ("provedor.invalid", "interno-sintetico", "incompleta", "Traceback", "conexao-sintetica"):
            self.assertNotIn(proibido, resposta.corpo.decode())

    def verificar_chamadas(self, transporte, termos, filtros=None) -> None:
        """Confere ordem, URL, timeout e query recebidos pelo transporte fake.

        Analisa parâmetros sem depender da ordem textual de urlencode para
        provar passagem pelo adapter real sem alegar filtragem do parceiro.
        """
        self.assertEqual(len(transporte.chamadas), len(termos))
        for ordem, (chamada, termo) in enumerate(zip(transporte.chamadas, termos), 1):
            self.assertEqual(chamada.ordem, ordem)
            self.assertEqual(chamada.timeout, 5.0)
            url = urlsplit(chamada.url)
            self.assertEqual(f"{url.scheme}://{url.netloc}{url.path}", URL_PROVEDOR)
            parametros = dict(FILTROS if filtros is None else filtros)
            if termo.strip():
                parametros["termo"] = termo.strip()
            self.assertEqual(parse_qs(url.query, keep_blank_values=True),
                             {chave: [valor] for chave, valor in parametros.items()})

    async def exercitar_falha(self, falha, status, detalhe) -> None:
        """Executa controle saudável, falha e recuperação no mesmo GET /vagas.

        Usa fila de transporte e contraprovas dos mesmos oráculos para
        provar recusa causal, sanitização e sensibilidade sem mudar produto.
        """
        transporte = TransporteVagasRegistrado(bytes_resultado(), falha, bytes_resultado())
        autenticador = AutenticadorVagasFake()
        app = criar_app_busca_vagas(transporte, autenticador)
        controle = await self.solicitar(app=app)
        self.verificar_resultado(controle)
        resposta = await self.solicitar(app=app)
        self.verificar_erro(resposta, status, detalhe)
        with self.assertRaises(AssertionError, msg="Controle aprovado: resultado recusa erro"):
            self.verificar_resultado(resposta)
        with self.assertRaises(AssertionError, msg="Controle aprovado: vazio recusa erro"):
            self.verificar_vazio(resposta)
        with self.assertRaises(AssertionError, msg="Controle aprovado: erro recusa resultado"):
            self.verificar_erro(controle, status, detalhe)
        self.verificar_resultado(await self.solicitar(app=app))
        self.verificar_chamadas(transporte, ["Python"] * 3)
        self.assertEqual(autenticador.consultas, [TOKEN_ACEITO] * 3)

    async def test_A01_resultado_e_filtros_atravessam_cadeia_real(self) -> None:
        """Prova resultado positivo com dois DTOs serializados em ordem.

        Envia critérios e cookie à app real e compara corpo e spy para
        estabelecer controle positivo da busca sem alegar filtro no fake.
        """
        self.transporte.enfileirar(bytes_resultado())
        self.verificar_resultado(await self.solicitar())
        self.verificar_chamadas(self.transporte, ["Python"])
        self.assertEqual(self.autenticador.consultas, [TOKEN_ACEITO])

    async def test_A02_refinamento_vazio_valido_e_retorno_sem_residuo(self) -> None:
        """Prova resultado, vazio e refinamento com oráculos mutuamente sensíveis.

        Alterna três respostas na mesma app e confere critérios e ausência
        de vagas antigas para distinguir sucesso vazio de erro ou resíduo.
        """
        qa = vagas_sinteticas()[1:]
        self.transporte.enfileirar(bytes_resultado(), b"[]", dumps(qa).encode())
        resultado = await self.solicitar()
        self.verificar_resultado(resultado)
        termo = "sem-correspondencia-sintetica"
        vazio = await self.solicitar(termo)
        self.verificar_vazio(vazio, termo)
        with self.assertRaises(AssertionError, msg="Controle aprovado: resultado recusa vazio"):
            self.verificar_resultado(vazio, termo)
        with self.assertRaises(AssertionError, msg="Controle aprovado: vazio recusa resultado"):
            self.verificar_vazio(resultado)
        with self.assertRaises(AssertionError, msg="Controle aprovado: erro recusa vazio"):
            self.verificar_erro(vazio, 502, DETALHE_INVALIDO)
        self.verificar_resultado(await self.solicitar("QA"), "QA", vagas=vagas_esperadas()[1:])
        self.verificar_chamadas(self.transporte, ["Python", termo, "QA"])

    async def test_A03_timeout_sanitizado_e_recuperacao(self) -> None:
        """Prova 504 e recuperação usando TimeoutError em vez de espera real.

        Percorre a cadeia real com transporte controlado e contraprovas
        para verificar a distinção entre timeout e sucesso na mesma rota.
        """
        await self.exercitar_falha(TimeoutError("interno-sintetico"), 504, DETALHE_TIMEOUT)

    async def test_A04_caracteriza_conexao_e_http_500_como_504(self) -> None:
        """Caracteriza a divergência de rede/HTTP externo traduzidos em 504.

        Injeta URLError e HTTPError 500, ambos capturados como timeout pelo
        adapter atual, para registrar 504 onde o documento sugere 502, sem correção.
        """
        for falha in (URLError("conexao-sintetica"), HTTPError(URL_PROVEDOR, 500, "interno-sintetico", {}, None)):
            with self.subTest(modalidade=type(falha).__name__):
                if isinstance(falha, HTTPError):
                    self.addCleanup(falha.close)
                await self.exercitar_falha(falha, 504, DETALHE_TIMEOUT)

    async def test_A05_json_schema_e_erro_inesperado_retornam_502(self) -> None:
        """Prova 502 controlado para JSON, schema e exceção inesperada.

        Alterna falhas de transporte/resposta com controles saudáveis para
        impedir aprovação por dados corrompidos ou rota permanentemente falha.
        """
        for nome, falha in (("JSON", b"{"), ("schema", b'[{"id":"incompleta"}]'),
                            ("inesperado", RuntimeError("interno-sintetico"))):
            with self.subTest(modalidade=nome):
                await self.exercitar_falha(falha, 502, DETALHE_INVALIDO)

    async def test_A06_erro_canonico_preserva_parametros_sem_adapter_http(self) -> None:
        """Prova a exceção base usando porta canônica auxiliar sem adapter HTTP.

        Alterna sucesso, erro e recuperação via use case real para validar
        tradução 502 e critérios sem alegar cobertura do mapper neste caso.
        """
        porta = PortaVagasCanonicaFake()
        app = create_app(autenticador_sessao=self.autenticador, consultar_vagas=ConsultarVagas(porta))
        self.verificar_resultado(await self.solicitar(app=app))
        porta.erro = ErroIntegracaoVagas("interno-sintetico", "Python", FILTROS)
        resposta = await self.solicitar(app=app)
        self.verificar_erro(resposta, 502, DETALHE_INVALIDO)
        with self.assertRaises(AssertionError, msg="Controle aprovado: resultado recusa erro base"):
            self.verificar_resultado(resposta)
        self.assertEqual(porta.erro.termo, "Python")
        self.assertEqual(porta.erro.filtros, FILTROS)
        porta.erro = None
        self.verificar_resultado(await self.solicitar(app=app))
        self.assertEqual(porta.chamadas, [("Python", FILTROS)] * 3)
        self.assertEqual(self.transporte.chamadas, ())

    async def test_A07_executor_ausente_recusa_antes_do_provedor(self) -> None:
        """Prova 503 com sessão aceita e controle positivo da mesma rota.

        Compara app sem executor à cadeia conectada, mantendo identidade e
        critérios para atribuir a recusa exclusivamente à falta de composição.
        """
        app = create_app(autenticador_sessao=self.autenticador, consultar_vagas=None)
        self.verificar_erro(await self.solicitar(app=app), 503, "Consulta de vagas indisponível.")
        self.assertEqual(self.transporte.chamadas, ())
        self.assertEqual(self.autenticador.consultas, [TOKEN_ACEITO])
        self.transporte.enfileirar(bytes_resultado())
        self.verificar_resultado(await self.solicitar())
        self.verificar_chamadas(self.transporte, ["Python"])

    async def test_A08_sem_cookie_ou_desconhecido_nao_consulta_provedor(self) -> None:
        """Prova as recusas reais do middleware e recuperação com token aceito.

        Distingue zero consultas sem cookie de uma com cookie desconhecido,
        usando controles positivos no mesmo recurso para verificar causalidade.
        """
        for token in (None, "token-sintetico-desconhecido"):
            with self.subTest(cookie=token):
                transporte = TransporteVagasRegistrado(bytes_resultado(), bytes_resultado())
                autenticador = AutenticadorVagasFake()
                app = criar_app_busca_vagas(transporte, autenticador)
                self.verificar_resultado(await self.solicitar(app=app))
                consultas_antes = len(autenticador.consultas)
                resposta = await self.solicitar(app=app, token=token)
                self.verificar_erro(resposta, 401, "Sessão ausente ou inválida.")
                self.verificar_chamadas(transporte, ["Python"])
                self.assertEqual(autenticador.consultas[consultas_antes:], [] if token is None else [token])
                self.verificar_resultado(await self.solicitar(app=app))
                self.verificar_chamadas(transporte, ["Python"] * 2)

    async def test_A09_guard_de_state_e_precedencia_sem_middleware_real(self) -> None:
        """Caracteriza identidade e precedência em middleware exclusivo de teste.

        Injeta ausência/string/UUID em app sem middleware real de sessão e
        compara controles para provar o handler, sem reivindicar login real.
        """
        for identidade in (None, "identidade-invalida"):
            with self.subTest(identidade=identidade):
                transporte = TransporteVagasRegistrado(bytes_resultado())
                adapter = ClienteApiVagasGrupo2Http(url_base=URL_PROVEDOR, executor_http=transporte)
                executor = ConsultarVagas(adapter)
                resposta = await self.solicitar(app=app_com_state_de_teste(executor, identidade))
                self.verificar_erro(resposta, 401, "Autenticação necessária.")
                self.assertEqual(transporte.chamadas, ())
                self.verificar_resultado(await self.solicitar(app=app_com_state_de_teste(executor, UUID(int=101))))
                self.verificar_chamadas(transporte, ["Python"])
        with self.subTest(precedencia="executor ausente vence identidade ausente"):
            self.verificar_erro(await self.solicitar(app=app_com_state_de_teste(None)),
                                503, "Consulta de vagas indisponível.")
            self.assertEqual(self.transporte.chamadas, ())
            self.transporte.enfileirar(bytes_resultado())
            self.verificar_resultado(await self.solicitar())

    async def test_A10_textos_livres_vazios_e_extra_sem_restricao_artificial(self) -> None:
        """Caracteriza aceitação textual sem inventar parâmetro inválido ou 422.

        Envia vazio e espaços com filtros livres e extra desconhecido para
        verificar eco bruto, trim do adapter e descarte de parâmetro extra.
        """
        filtros = {"localizacao": "", "modalidade": "QUALQUER-TEXTO"}
        for termo in ("", "   "):
            with self.subTest(termo=repr(termo)):
                transporte = TransporteVagasRegistrado(bytes_resultado())
                app = criar_app_busca_vagas(transporte, AutenticadorVagasFake())
                self.verificar_resultado(await self.solicitar(termo, filtros, app=app, extras={"extra": "ignorado"}), termo, filtros)
                self.verificar_chamadas(transporte, [termo], filtros)
