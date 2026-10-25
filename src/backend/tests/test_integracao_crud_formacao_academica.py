"""Integra cadastro, edição e exclusão HTTP de formação com propriedade.

Usa ASGI, sessão persistida, casos/repos reais e SQLite migrado, com controles
positivos, spies delegantes e snapshots brutos em outra sessão. O CRUD HTTP
não está completo: consulta GET/listagem não existe (L1); a leitura aqui é a
porta interna escopada, sem rota inventada ou placeholder ignorado para Q1.
Critérios inferidos do título; o aceite oficial do card não é verificável.

Não certifica main.py, cadeia original do Alembic, PostgreSQL/timezone,
concorrência, HTTPS/cookie real, retenção/purga, desempenho, falha de banco ou
leitura histórica de currículo. Seleções preservadas provam apenas suas linhas.
O modelo migra uma vez por classe, com tempo medido, e cada cenário copia o
arquivo fechado para manter isolamento sem repetir a preparação dominante.
"""

# Proveniência: decision-analysis prompts/backend/20261025-112457-integracao-crud-formacao-academica-propriedade-v001.md#v001

import asyncio
import unittest
from contextlib import asynccontextmanager
from copy import deepcopy
from datetime import date, timedelta
from urllib.parse import urlencode

from backend.tests.fixtures.credenciais_sessao import (
    INSTANTE_T,
    USUARIO_A,
    USUARIO_B,
    token_sintetico,
)
from backend.tests.fixtures.formacoes_academicas_integracao import (
    AIOSQLITE_DISPONIVEL,
    CURRICULO_B,
    MOTIVO_DRIVER,
    BancoFormacoesAcademicasIntegracao,
    F,
    G,
    H,
    V,
    W,
    verificar_grafo,
)

ERRO_FORMACAO = "Formação acadêmica não encontrada."
ERRO_SESSAO = "Sessão ausente ou inválida."
ERRO_CADASTRO = "A formação informada viola as regras de cadastro."
ERRO_EDICAO = "A formação informada viola as regras de edição."
CAMPOS = {
    "id",
    "usuario_id",
    "instituicao",
    "curso",
    "nivel",
    "data_inicio",
    "data_fim",
    "status",
}


@unittest.skipUnless(AIOSQLITE_DISPONIVEL, MOTIVO_DRIVER)
class CrudFormacaoAcademicaIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Exercita dezenove cenários integrados com bancos independentes.

    Reusa somente o arquivo de um modelo migrado fechado e cria uma cópia por
    subcenário, para provar isolamento sem depender da ordem entre métodos.
    """

    modelo = None
    tempos_copia = []

    async def asyncSetUp(self):
        """Valida o grafo antes de qualquer banco e prepara modelo se necessário.

        Faz o skip conhecido por método no original, preservando a contagem;
        somente grafo válido chega à migração real, cuja falha nunca vira skip.
        """
        verificar_grafo()
        classe = type(self)
        if classe.modelo is None:
            classe.modelo = await BancoFormacoesAcademicasIntegracao.preparar_modelo()
            classe.tempos_copia = []
            print(
                f"Preparação modelo migrado: {classe.modelo.segundos_preparacao:.6f}s"
            )

    @classmethod
    def tearDownClass(cls):
        """Libera o modelo fechado e relata tempos sem registrar credenciais.

        Usa o cleanup do harness em loop próprio para remover o arquivo após
        todos os cenários, inclusive quando uma asserção tenha falhado.
        """
        if cls.modelo is not None:
            try:
                print(
                    f"Cópias isoladas: {len(cls.tempos_copia)}; "
                    f"tempo total de cópia: {sum(cls.tempos_copia):.6f}s"
                )
                asyncio.run(cls.modelo.fechar())
            finally:
                cls.modelo = None
        super().tearDownClass()

    @asynccontextmanager
    async def _banco(self, *, com_f=True):
        """Fornece banco novo com G/B e opcional F/A, ambos criados pela API.

        Semeia seleções reais e fecha a cópia em finally, isolando cada caso
        negativo e garantindo que seu controle não use persistência simulada.
        """
        banco = await BancoFormacoesAcademicasIntegracao.criar(type(self).modelo)
        type(self).tempos_copia.append(banco.segundos_copia)
        try:
            await self._cadastrar(banco, G, USUARIO_B)
            await banco.semear_referencia(USUARIO_B, G)
            banco.estado_b = self._estado_b(await banco.snapshot())
            if com_f:
                await self._cadastrar(banco, F)
                await banco.semear_referencia(USUARIO_A, F)
            yield banco
        finally:
            await banco.fechar()

    def _estado_b(self, snapshot):
        """Extrai dados e referências de B sem expô-los em mensagens de falha.

        Filtra o snapshot bruto pelas identidades da massa para conferir que
        cada operação de A preserva integralmente o outro estudante.
        """
        return {
            "formacoes": tuple(
                l
                for l in snapshot["formacoes_academicas"]
                if l["usuario_id"] == USUARIO_B
            ),
            "curriculos": tuple(
                l for l in snapshot["curriculos"] if l["usuario_id"] == USUARIO_B
            ),
            "itens": tuple(
                l
                for l in snapshot["curriculo_itens"]
                if l["curriculo_id"] == CURRICULO_B
            ),
            "usuarios": tuple(l for l in snapshot["usuarios"] if l["id"] == USUARIO_B),
            "sessoes": tuple(
                l for l in snapshot["sessoes"] if l["usuario_id"] == USUARIO_B
            ),
        }

    async def _preservou_b(self, banco):
        """Confere B em sessão nova por igualdade booleana para não imprimir hashes.

        Compara todas as colunas e seleções com a preparação, provando isolamento
        a cada etapa e evitando que o identity map mascare mudanças.
        """
        self.assertTrue(
            self._estado_b(await banco.snapshot()) == banco.estado_b,
            "Estado persistido de B foi alterado",
        )

    def _spies(self, banco, operacao=None, usuario=USUARIO_A, identidade=F):
        """Confere chamadas/awaits e identidade nos três spies da requisição.

        Cada chamada ASGI cria spies novos; comparar suas contagens equivale ao
        delta dessa operação e distingue recusa anterior ao caso da recusa nele.
        """
        for nome, spy in banco.spies.items():
            esperado = int(nome == operacao)
            self.assertEqual(
                (spy.call_count, spy.await_count), (esperado, esperado), nome
            )
            if esperado:
                entrada = spy.call_args.args[0]
                self.assertTrue(
                    entrada.usuario_id.valor == usuario, "Dono interno incorreto"
                )
                if nome != "POST":
                    self.assertTrue(
                        entrada.formacao_id.valor == identidade, "ID interno incorreto"
                    )

    async def _cadastrar(self, banco, identidade=F, usuario=USUARIO_A, dados=None):
        """Reserva candidato e cadastra-o pela API real para um controle positivo.

        Ajusta somente o gerador da fixture e verifica resposta, spy e leitura
        independente, inclusive para H que antes não existia.
        """
        banco.gerador.proximo = identidade.int
        return await self._sucesso(banco, "POST", identidade, usuario, dados=dados)

    async def _sucesso(
        self, banco, metodo, identidade=F, usuario=USUARIO_A, *, dados=None, query=""
    ):
        """Executa controle autorizado e confere contrato e persistência reais.

        Usa o cookie do dono e verifica os oito campos públicos mais os dados
        brutos em outra sessão, para impedir controle de rota que sempre falha.
        """
        corpo = dict(V if metodo == "POST" else W) if dados is None else dict(dados)
        resposta = await banco.requisitar(
            metodo,
            identidade,
            dados=corpo if metodo != "DELETE" else dados,
            token=banco.tokens[usuario],
            query=query,
        )
        self.assertEqual(
            resposta.status, {"POST": 201, "PUT": 200, "DELETE": 204}[metodo]
        )
        self._spies(banco, metodo, usuario, identidade)
        raw = await banco.ler_formacao(identidade)
        self.assertIsNotNone(raw)
        if metodo == "DELETE":
            self.assertTrue(resposta.corpo == b"", "DELETE deve ter corpo vazio")
            self.assertIsNotNone(raw["deleted_at"])
        else:
            esperado = {chave: corpo[chave] for chave in CAMPOS - {"id", "usuario_id"}}
            esperado["instituicao"] = esperado["instituicao"].strip()
            esperado["curso"] = esperado["curso"].strip()
            esperado.update(id=str(identidade), usuario_id=str(usuario))
            self.assertTrue(
                resposta.json() == esperado,
                "DTO público divergente ou com campos internos",
            )
            self.assertEqual(set(resposta.json()), CAMPOS)
            for chave in CAMPOS:
                valor = esperado[chave]
                if chave in {"id", "usuario_id"}:
                    valor = identidade if chave == "id" else usuario
                elif chave in {"data_inicio", "data_fim"} and valor is not None:
                    valor = date.fromisoformat(valor)
                self.assertTrue(
                    raw[chave] == valor, f"Persistência divergente em {chave}"
                )
            self.assertIsNone(raw["deleted_at"])
        return resposta

    async def _negativa(
        self,
        banco,
        metodo,
        status,
        detalhe,
        *,
        identidade=F,
        token=None,
        dados=None,
        chamadas=0,
        usuario=USUARIO_A,
        query="",
        cabecalhos=None,
        ausente=None,
    ):
        """Prova recusa com snapshot bruto independente e spies delegantes.

        Tira o estado depois do controle/transição, deixa a resposta fazer commit
        e compara booleanos para não imprimir hashes, cookies ou tokens.
        """
        antes = await banco.snapshot()
        corpo = dict(V if metodo == "POST" else W) if metodo != "DELETE" else None
        resposta = await banco.requisitar(
            metodo,
            identidade,
            dados=corpo if dados is None else dados,
            token=token,
            query=query,
            cabecalhos=cabecalhos,
            ausente=ausente,
        )
        self.assertEqual(resposta.status, status)
        if detalhe is None:
            erros = resposta.json().get("detail")
            self.assertTrue(
                isinstance(erros, list) and bool(erros),
                "Esperada validação do framework",
            )
            self.assertTrue(
                all("loc" in erro and "type" in erro for erro in erros),
                "Estrutura de validação inválida",
            )
        else:
            self.assertTrue(
                resposta.json() == {"detail": detalhe}, "Detalhe HTTP divergente"
            )
        self._spies(banco, metodo if chamadas else None, usuario, identidade)
        depois = await banco.snapshot()
        self.assertTrue(
            antes == depois, "Requisição recusada mudou estado persistido [REDACTED]"
        )
        # O snapshot usa Table, não o filtro ativo, e inclui explicitamente tombstones.
        if identidade in {F, G, H}:
            linha = await banco.ler_formacao(identidade)
            original = next(
                (l for l in antes["formacoes_academicas"] if l["id"] == identidade),
                None,
            )
            self.assertTrue(linha == original, "Tabela bruta mudou após recusa")
        print(
            f"EVIDENCIA {self._testMethodName} {self._subtest or ''}: "
            f"{metodo} recusa/estado/spies aprovados"
        )
        return resposta

    async def test_ciclo_cadastro_edicao_exclusao_persistido(self):
        """P1 encadeia CUD real e relê cada etapa para provar durabilidade e dono.

        Compara B e seleções, limita a mutação final a deleted_at e lê a porta
        interna para demonstrar exclusão lógica sem alegar CRUD HTTP completo.
        """
        async with self._banco(com_f=False) as banco:
            await self._cadastrar(banco)
            await self._preservou_b(banco)
            self.assertIsNotNone(await banco.consultar(F, USUARIO_A))
            await self._sucesso(banco, "PUT")
            await self._preservou_b(banco)
            await banco.semear_referencia(USUARIO_A, F)
            antes = await banco.snapshot()
            await self._sucesso(banco, "DELETE")
            esperado = deepcopy(antes)
            next(l for l in esperado["formacoes_academicas"] if l["id"] == F)[
                "deleted_at"
            ] = INSTANTE_T
            self.assertTrue(
                await banco.snapshot() == esperado,
                "DELETE alterou mais que o tombstone",
            )
            await self._preservou_b(banco)
            self.assertIsNone(await banco.consultar(F, USUARIO_A))
            tombstone = await banco.consultar(F, USUARIO_A, incluir_excluidas=True)
            self.assertTrue(
                tombstone.id.valor == F and tombstone.usuario_id.valor == USUARIO_A
            )

    async def test_isolamento_das_operacoes_de_a_preserva_b(self):
        """P2 compara B após cada operação de A por leituras brutas independentes.

        Cria, edita e exclui F com cookies reais para provar que dados e seleções
        de outro estudante não são atingidos pelo fluxo autorizado.
        """
        async with self._banco(com_f=False) as banco:
            await self._cadastrar(banco)
            await self._preservou_b(banco)
            await banco.semear_referencia(USUARIO_A, F)
            for metodo in ("PUT", "DELETE"):
                with self.subTest(operacao=metodo):
                    await self._sucesso(banco, metodo)
                    await self._preservou_b(banco)

    async def test_delete_repetido_preserva_primeiro_instante(self):
        """P3 repete DELETE próprio após avançar relógio para provar idempotência.

        Confere os dois 204, spy por requisição e snapshot idêntico, inclusive
        timestamp, garantindo ausência de novo efeito e nova consulta ao relógio.
        """
        async with self._banco() as banco:
            await self._sucesso(banco, "DELETE")
            antes = await banco.snapshot()
            self.assertEqual(banco.relogio.chamadas, 1)
            banco.relogio.instante += timedelta(days=1)
            await self._sucesso(banco, "DELETE")
            self.assertEqual(banco.relogio.chamadas, 1)
            self.assertTrue(
                await banco.snapshot() == antes, "Repetição mudou o primeiro instante"
            )

    async def test_aceita_previsao_futura_e_limpeza_explicita(self):
        """P4 aceita previsão futura e limpa data_fim por PUT completo.

        Confere resposta e colunas após cada operação para provar a regra
        temporal vigente sem duplicar todos os enums dos testes unitários.
        """
        async with self._banco(com_f=False) as banco:
            await self._cadastrar(banco, dados={**V, "data_fim": "2030-12-01"})
            await self._sucesso(banco, "PUT", dados=V)

    async def test_consulta_interna_filtra_dono_e_exclusao(self):
        """R1 integra somente repositório e banco, sem provar autenticação/HTTP/DTO.

        Controla leitura própria e compara recusas e tombstones em sessões novas
        para verificar filtro conjunto de dono, identidade e estado ativo.
        """
        async with self._banco() as banco:
            antes = await banco.snapshot()
            propria = await banco.consultar(F, USUARIO_A)
            self.assertTrue(
                propria.id.valor == F and propria.usuario_id.valor == USUARIO_A
            )
            self.assertIsNone(await banco.consultar(F, USUARIO_B))
            self.assertIsNone(await banco.consultar(H, USUARIO_A))
            self.assertTrue(
                await banco.snapshot() == antes, "Leitura interna alterou banco"
            )
            await self._sucesso(banco, "DELETE")
            antes = await banco.snapshot()
            self.assertIsNone(await banco.consultar(F, USUARIO_A))
            self.assertIsNotNone(
                await banco.consultar(F, USUARIO_A, incluir_excluidas=True)
            )
            self.assertIsNone(
                await banco.consultar(F, USUARIO_B, incluir_excluidas=True)
            )
            self.assertIsNone(
                await banco.consultar(H, USUARIO_A, incluir_excluidas=True)
            )
            self.assertTrue(
                await banco.snapshot() == antes, "Leitura de tombstone alterou banco"
            )
            # Controle posterior no mesmo H antes ausente, sem inventar consulta HTTP.
            await self._cadastrar(banco, H)
            antes = await banco.snapshot()
            self.assertIsNotNone(await banco.consultar(H, USUARIO_A))
            self.assertIsNotNone(
                await banco.consultar(H, USUARIO_A, incluir_excluidas=True)
            )
            self.assertTrue(
                await banco.snapshot() == antes, "Controle de leitura alterou banco"
            )

    async def test_b_nao_edita_formacao_de_a(self):
        """S1 contrasta PUT próprio com alheio/ausente no mesmo fluxo real.

        Compara 404 e corpo uniforme com spies chamados e estado inalterado,
        depois torna H próprio para controlar a mesma identidade antes ausente.
        """
        async with self._banco() as banco:
            await self._sucesso(banco, "PUT")
            respostas = []
            for identidade in (F, H):
                with self.subTest(recurso="alheio" if identidade == F else "ausente"):
                    resposta = await self._negativa(
                        banco,
                        "PUT",
                        404,
                        ERRO_FORMACAO,
                        identidade=identidade,
                        token=banco.tokens[USUARIO_B],
                        chamadas=1,
                        usuario=USUARIO_B,
                    )
                    respostas.append(resposta.corpo)
            self.assertTrue(respostas[0] == respostas[1], "404 revelou existência")
            await self._cadastrar(banco, H, USUARIO_B)
            await self._sucesso(banco, "PUT", H, USUARIO_B)

    async def test_b_nao_exclui_formacao_de_a(self):
        """S2 recusa DELETE alheio em ativo/tombstone com controles do dono.

        Compara o inexistente e verifica tabelas intactas para provar que a
        recusa decorre da propriedade, e não de uma rota sempre indisponível.
        """
        for estado in ("ativa", "tombstone"):
            with self.subTest(estado=estado):
                async with self._banco() as banco:
                    if estado == "tombstone":
                        await self._sucesso(banco, "DELETE")
                    alheia = await self._negativa(
                        banco,
                        "DELETE",
                        404,
                        ERRO_FORMACAO,
                        token=banco.tokens[USUARIO_B],
                        chamadas=1,
                        usuario=USUARIO_B,
                    )
                    ausente = await self._negativa(
                        banco,
                        "DELETE",
                        404,
                        ERRO_FORMACAO,
                        identidade=H,
                        token=banco.tokens[USUARIO_B],
                        chamadas=1,
                        usuario=USUARIO_B,
                    )
                    self.assertTrue(
                        alheia.corpo == ausente.corpo, "404 revelou existência"
                    )
                    if estado == "ativa":
                        await self._sucesso(banco, "DELETE")
                    await self._cadastrar(banco, H, USUARIO_B)
                    await self._sucesso(banco, "DELETE", H, USUARIO_B)

    async def test_id_inexistente_na_edicao_e_exclusao(self):
        """S3 testa ausência com cookie A e depois controla o mesmo H persistido.

        Usa banco novo por operação e 404 igual ao alheio, comprovando ausência
        de escrita antes de cadastrar H pelo POST real e operar com sucesso.
        """
        for metodo in ("PUT", "DELETE"):
            with self.subTest(operacao=metodo):
                async with self._banco() as banco:
                    await self._sucesso(banco, "PUT")
                    alheia = await self._negativa(
                        banco,
                        metodo,
                        404,
                        ERRO_FORMACAO,
                        token=banco.tokens[USUARIO_B],
                        chamadas=1,
                        usuario=USUARIO_B,
                    )
                    ausente = await self._negativa(
                        banco,
                        metodo,
                        404,
                        ERRO_FORMACAO,
                        identidade=H,
                        token=banco.tokens[USUARIO_A],
                        chamadas=1,
                    )
                    self.assertTrue(alheia.corpo == ausente.corpo)
                    await self._cadastrar(banco, H)
                    await self._sucesso(banco, metodo, H)
                    if metodo == "DELETE":
                        await self._sucesso(banco, metodo)

    async def test_edicao_apos_exclusao_nao_ressuscita(self):
        """S4 controla PUT antes de excluir F e recusa a edição posterior.

        Compara raw completo e timestamp após 404 com caso chamado, garantindo
        que o filtro de ativo não permita ressuscitar nem alterar seleções.
        """
        async with self._banco() as banco:
            await self._sucesso(banco, "PUT")
            await self._sucesso(banco, "DELETE")
            await self._negativa(
                banco,
                "PUT",
                404,
                ERRO_FORMACAO,
                token=banco.tokens[USUARIO_A],
                chamadas=1,
            )

    async def test_identidade_do_cliente_nao_troca_proprietario(self):
        """S5 caracteriza extras ignorados e recusa B tentando declarar dono A.

        Confere ID/dono reais e snapshots nas recusas, distinguindo criação
        autorizada de uma negativa que obrigatoriamente deixa o banco intacto.
        """
        async with self._banco(com_f=False) as banco:
            extras = {"usuario_id": str(USUARIO_B), "id": str(G)}
            query = urlencode(extras)
            banco.gerador.proximo = F.int
            await self._sucesso(banco, "POST", dados={**V, **extras}, query=query)
            await banco.semear_referencia(USUARIO_A, F)
            await self._sucesso(banco, "PUT", dados=V)
            antes = await banco.snapshot()
            await self._sucesso(banco, "PUT", dados={**V, **extras}, query=query)
            self.assertTrue(
                await banco.snapshot() == antes, "Extras trocaram dono ou ID"
            )
            await self._preservou_b(banco)
            await self._negativa(
                banco,
                "PUT",
                404,
                ERRO_FORMACAO,
                dados={**W, "usuario_id": str(USUARIO_A)},
                token=banco.tokens[USUARIO_B],
                usuario=USUARIO_B,
                chamadas=1,
            )
            await self._sucesso(banco, "DELETE")
            await self._negativa(
                banco,
                "DELETE",
                404,
                ERRO_FORMACAO,
                query=urlencode({"usuario_id": str(USUARIO_A)}),
                token=banco.tokens[USUARIO_B],
                usuario=USUARIO_B,
                chamadas=1,
            )

    async def _autenticacao(self, estado):
        """Controla cada operação e então aplica uma pré-condição de autenticação.

        Usa banco novo por operação, snapshot posterior à transição e cookie
        real para provar 401 uniforme sem chamadas ou mudanças persistidas.
        """
        for metodo in ("POST", "PUT", "DELETE"):
            with self.subTest(estado=estado, operacao=metodo):
                async with self._banco(com_f=metodo != "POST") as banco:
                    if metodo == "POST":
                        await self._cadastrar(banco)
                        banco.gerador.proximo = F.int
                    else:
                        await self._sucesso(banco, metodo)
                        if metodo == "DELETE":
                            # Controle no mesmo estado tombstonado da requisição negativa.
                            await self._sucesso(banco, metodo)
                    token = banco.tokens[USUARIO_A]
                    if estado == "sem_cookie":
                        token = None
                    elif estado == "desconhecido":
                        token = token_sintetico(99)
                    elif estado == "conta_excluida":
                        await banco.banco.marcar_conta_excluida(USUARIO_A)
                    else:
                        await banco.invalidar_sessao(estado)
                    await self._negativa(banco, metodo, 401, ERRO_SESSAO, token=token)

    async def test_sem_cookie_nao_executa_operacoes(self):
        """S6 compara sucessos com requisições sem cookie para provar a guarda.

        Exercita as três operações pela matriz real com spies zero e tabelas
        inalteradas, isolando autenticação de erros de payload.
        """
        await self._autenticacao("sem_cookie")

    async def test_token_desconhecido_nao_executa_operacoes(self):
        """S7 usa token não semeado após controles para provar recusa uniforme.

        Reusa a matriz de três operações reais e snapshots, sem fabricar
        resposta do autenticador ou imprimir a credencial sintética.
        """
        await self._autenticacao("desconhecido")

    async def test_sessao_expirada_ou_revogada_nao_executa_operacoes(self):
        """S8 altera expiração/revogação persistidas sem espera ou auth double.

        Executa cada operação após seu controle válido e compara snapshots
        posteriores à preparação para provar que a recusa não muda dados.
        """
        for estado in ("expirada", "revogada"):
            await self._autenticacao(estado)

    async def test_conta_excluida_invalida_sessao_nas_operacoes(self):
        """S9 marca conta excluída após controles e prova invalidação da sessão.

        Inclui DELETE próprio antes da exclusão da conta para controlar o
        mesmo tombstone, sem confundir preparação com efeito da recusa 401.
        """
        await self._autenticacao("conta_excluida")

    async def test_validacao_de_fronteira_nao_chama_casos(self):
        """S10 amostra validações do framework com controles no recurso válido.

        Usa payloads e UUID alterados com snapshots e spies zero; para UUID
        malformado só há controle de F bem formado, pois não existe recurso
        material correspondente ao identificador inválido.
        """
        alteracoes = (
            ("enum", {"nivel": "invalido"}),
            ("espacos", {"instituicao": "   "}),
            ("limite", {"curso": "x" * 201}),
            ("controle", {"curso": "x\ny"}),
        )
        for metodo in ("POST", "PUT"):
            for nome, alteracao in alteracoes:
                with self.subTest(operacao=metodo, violacao=nome):
                    async with self._banco(com_f=metodo != "POST") as banco:
                        if metodo == "POST":
                            await self._cadastrar(banco)
                            banco.gerador.proximo = F.int
                        else:
                            await self._sucesso(banco, metodo)
                        await self._negativa(
                            banco,
                            metodo,
                            422,
                            None,
                            dados={**(V if metodo == "POST" else W), **alteracao},
                            token=banco.tokens[USUARIO_A],
                        )
        with self.subTest(violacao="data_fim_omitida"):
            async with self._banco() as banco:
                await self._sucesso(banco, "PUT")
                dados = dict(W)
                del dados["data_fim"]
                await self._negativa(
                    banco, "PUT", 422, None, dados=dados, token=banco.tokens[USUARIO_A]
                )
        for metodo in ("PUT", "DELETE"):
            with self.subTest(operacao=metodo, violacao="uuid_malformado"):
                async with self._banco() as banco:
                    await self._sucesso(banco, metodo)
                    await self._negativa(
                        banco,
                        metodo,
                        422,
                        None,
                        identidade=str(F)[:-1] + "z",
                        token=banco.tokens[USUARIO_A],
                    )

    async def test_precedencia_autenticacao_validacao_propriedade(self):
        """S11 caracteriza a ordem real de autenticação, DTO, Periodo e propriedade.

        Varia só os erros conflitantes depois de PUT válido no mesmo F, usando
        contagens do caso e raw para não impor uma política universal de status.
        """
        casos = (
            (
                "sem_cookie_enum",
                F,
                {**W, "nivel": "invalido"},
                None,
                401,
                ERRO_SESSAO,
                0,
            ),
            ("sem_cookie_uuid", str(F)[:-1] + "z", W, None, 401, ERRO_SESSAO, 0),
            ("dto", F, {**W, "nivel": "invalido"}, USUARIO_A, 422, None, 0),
            (
                "periodo_alheio",
                F,
                {**W, "data_fim": "2020-01-01"},
                USUARIO_B,
                422,
                ERRO_EDICAO,
                0,
            ),
            (
                "conclusao_alheia",
                F,
                {**W, "data_fim": None},
                USUARIO_B,
                404,
                ERRO_FORMACAO,
                1,
            ),
            (
                "conclusao_propria",
                F,
                {**W, "data_fim": None},
                USUARIO_A,
                422,
                ERRO_EDICAO,
                1,
            ),
        )
        for nome, identidade, dados, usuario, status, detalhe, chamadas in casos:
            with self.subTest(precedencia=nome):
                async with self._banco() as banco:
                    await self._sucesso(banco, "PUT")
                    await self._negativa(
                        banco,
                        "PUT",
                        status,
                        detalhe,
                        identidade=identidade,
                        dados=dados,
                        chamadas=chamadas,
                        usuario=usuario,
                        token=banco.tokens.get(usuario),
                    )

    async def test_rejeita_periodo_invalido_e_conclusao_sem_fim(self):
        """S12 distingue Periodo antes do caso de entidade inválida dentro dele.

        Controla POST/PUT no mesmo ID, reserva novamente o candidato e exige
        detalhe seguro, contagem correta e nenhuma alteração de tabelas.
        """
        for metodo in ("POST", "PUT"):
            for nome, alteracao, chamadas in (
                ("periodo", {"data_fim": "2020-01-01"}, 0),
                ("conclusao", {"status": "concluido", "data_fim": None}, 1),
            ):
                with self.subTest(operacao=metodo, violacao=nome):
                    async with self._banco(com_f=metodo != "POST") as banco:
                        if metodo == "POST":
                            await self._cadastrar(banco)
                            banco.gerador.proximo = F.int
                        else:
                            await self._sucesso(banco, "PUT")
                        await self._negativa(
                            banco,
                            metodo,
                            422,
                            ERRO_CADASTRO if metodo == "POST" else ERRO_EDICAO,
                            dados={**(V if metodo == "POST" else W), **alteracao},
                            chamadas=chamadas,
                            token=banco.tokens[USUARIO_A],
                        )

    async def test_executor_ausente_na_factory(self):
        """S13 caracteriza 503 de cada binding ausente sem certificar produção.

        Controla a mesma factory com o caso presente e remove só o executor
        pedido na chamada seguinte, verificando ausência de chamadas e escrita.
        """
        for metodo, detalhe in (
            ("POST", "Cadastro indisponível."),
            ("PUT", "Edição indisponível."),
            ("DELETE", "Exclusão indisponível."),
        ):
            with self.subTest(operacao=metodo):
                async with self._banco(com_f=metodo != "POST") as banco:
                    if metodo == "POST":
                        await self._cadastrar(banco)
                        banco.gerador.proximo = F.int
                    else:
                        await self._sucesso(banco, metodo)
                    await self._negativa(
                        banco,
                        metodo,
                        503,
                        detalhe,
                        ausente=metodo,
                        token=banco.tokens[USUARIO_A],
                    )

    async def test_token_fora_do_cookie_nao_autentica(self):
        """S14 envia token válido fora do cookie após controlar o canal aceito.

        Testa Authorization, query e corpo nas três operações com spies zero
        e snapshots idênticos, sem imprimir o token em labels ou asserções.
        """
        for metodo in ("POST", "PUT", "DELETE"):
            for canal in ("authorization", "query", "corpo"):
                with self.subTest(operacao=metodo, canal=canal):
                    async with self._banco(com_f=metodo != "POST") as banco:
                        if metodo == "POST":
                            await self._cadastrar(banco)
                            banco.gerador.proximo = F.int
                        else:
                            await self._sucesso(banco, metodo)
                        token = banco.tokens[USUARIO_A]
                        dados = dict(V if metodo == "POST" else W)
                        cabecalhos = (
                            {"Authorization": f"Bearer {token}"}
                            if canal == "authorization"
                            else None
                        )
                        query = urlencode({"token": token}) if canal == "query" else ""
                        if canal == "corpo":
                            dados["token"] = token
                        await self._negativa(
                            banco,
                            metodo,
                            401,
                            ERRO_SESSAO,
                            dados=dados,
                            query=query,
                            cabecalhos=cabecalhos,
                        )
