"""Exercita P1–P4/N1–N14 por ASGI, sessão persistida e SQLite migrado.

Ordenação é ordem persistida de seções e sort automático dos itens na prévia;
não prova ordem manual de itens nem ordem personalizada de seções na prévia.
Consultas de item são doubles: propriedade real em produção não foi provada.
Critérios inferidos do título, sem aceite oficial verificável. Não certifica
main.py, cadeia original Alembic, PostgreSQL, concorrência, falha de banco nem
política de exclusão/alteração de selecionados. P4 caracteriza só o consumidor.

Cada negativo usa controle pareado, spies delegantes e SQL bruto mais agregado
em sessões independentes. Variantes usam arquivos SQLite isolados; o template
migrado é copiado quando a medição confirma migração mais cara que seed.
"""

# Proveniência: decision-analysis prompts/backend/20261025-193758-integracao-selecao-ordenacao-curriculo-v001.md#v001
import json
import statistics
import unittest
from contextlib import asynccontextmanager
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import update

from backend.domain.value_objects import ReferenciaCurriculo
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro
from backend.tests.fixtures.curriculos_autenticados_integracao import (
    CURRICULO_A,
    CURRICULO_B,
    CURRICULO_INEXISTENTE,
    ITEM_A,
    ITEM_A_NOVO,
    ITEM_B,
    USUARIO_A,
    USUARIO_B,
)
from backend.tests.fixtures.selecao_ordenacao_curriculo import (
    AIOSQLITE_DISPONIVEL,
    CLASSES_ID,
    CURRICULO_A2,
    INVERSA,
    MOTIVO_DRIVER,
    SECOES_PREVIA,
    TIPOS,
    PreparadorBanco,
    identidade,
    rota,
    verificar_grafo,
)

OPERACOES = ("selecionar", "desselecionar", "ordem")
ERRO_CURRICULO = "Versão de currículo não encontrada."
ERRO_ITEM = "Item do perfil não encontrado."
ERRO_SESSAO = "Sessão ausente ou inválida."
ERRO_DONO = "A sessão não pode acessar este recurso."
ERRO_ORDEM = "A ordem das seções deve conter cada seção exatamente uma vez."


@unittest.skipUnless(AIOSQLITE_DISPONIVEL, MOTIVO_DRIVER)
class SelecaoOrdenacaoCurriculoIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Integra três escritas e duas leituras para provar estado e camada de recusa.

    Usa controle de mesma operação/recurso e observa deltas reais, sem simular
    resultados dos casos, para distinguir autorização, DTO e invariantes.
    """

    @classmethod
    def setUpClass(cls):
        """Reserva preparador e contagens sem migrar para permitir skips por método."""
        cls.preparador = PreparadorBanco()
        cls.provas = {}

    @classmethod
    def tearDownClass(cls):
        """Reporta custos e deltas por método e limpa template para tornar a prova auditável."""
        try:
            for nome, contagens in sorted(cls.provas.items()):
                print(f"PROVA {nome}: {contagens}")
            p = cls.preparador
            if p.tempos:
                print(
                    f"PREPARACAO bancos={len(p.tempos)} migracao={p.tempo_migration:.6f}s "
                    f"seed_mediana={statistics.median(p.tempos_seed):.6f}s copiar={p.copiar} "
                    f"total_mediana={statistics.median(p.tempos):.6f}s "
                    f"faixa={min(p.tempos):.6f}..{max(p.tempos):.6f}s"
                )
        finally:
            cls.preparador.fechar()

    async def asyncSetUp(self):
        """Exige grafo inequívoco antes de cada método para relatar bloqueio original nominal."""
        verificar_grafo()

    @asynccontextmanager
    async def banco(self, variante):
        """Fornece banco novo por variante e relata sucesso somente se asserções concluírem.

        Envolve o fluxo em subTest e fecha recursos em finally para preservar
        isolamento inclusive quando uma variante falha, sem esconder a falha.
        """
        with self.subTest(variante=variante):
            banco = await self.preparador.criar()
            try:
                yield banco
            except BaseException:
                print(f"SUBTEST {self._testMethodName} [{variante}]: falhou/erro")
                raise
            else:
                print(f"SUBTEST {self._testMethodName} [{variante}]: aprovado")
            finally:
                await banco.fechar()

    def contar(self, resultado):
        """Acumula tipo de prova por método sem dados sensíveis para resumir controles e spies."""
        contagens = self.provas.setdefault(self._testMethodName, {})
        contagens[resultado] = contagens.get(resultado, 0) + 1

    def observar(self, banco, rota_http, executou, donos=0):
        """Confere call/await e DTO do delegado para localizar a camada e contar consultas."""
        for nome, spy in banco.spies.items():
            esperado = int(executou and nome == rota_http.nome)
            self.assertEqual((spy.call_count, spy.await_count), (esperado, esperado), nome)
            if esperado:
                self.assertEqual(spy.call_args, spy.await_args)
                entrada = spy.await_args.args[0]
                partes = rota_http.caminho.split("/")
                self.assertEqual(entrada.usuario_id.valor, UUID(partes[2]))
                self.assertEqual(entrada.curriculo_id.valor, UUID(partes[4]))
                if rota_http.nome == "ordem":
                    self.assertEqual(tuple(s.value for s in entrada.ordem_secoes), tuple(rota_http.corpo["ordem_secoes"]))
                else:
                    tipo, iid = (
                        (rota_http.corpo["tipo"], rota_http.corpo["item_id"])
                        if rota_http.nome == "selecionar" else (partes[6], partes[7])
                    )
                    self.assertEqual(entrada.referencia, ReferenciaCurriculo(CLASSES_ID[TIPOS.index(tipo)](UUID(iid))))
        self.assertEqual(len(banco.itens.consultas_proprietario), donos)
        self.assertEqual(banco.itens.consultas_item, [])

    async def sucesso(self, banco, r, *, usuario=USUARIO_A):
        """Prova controle positivo por resposta e delta exato de todas as linhas e agregados.

        Calcula somente a alteração pedida sobre snapshot independente e mantém
        B/A2 e metadados no esperado para detectar sucesso sem persistência.
        """
        antes = await banco.estado()
        banco.zerar_observadores()
        token = banco.token_a if usuario == USUARIO_A else banco.token_b
        status, corpo = await banco.solicitar(r, token)
        self.assertEqual(status, r.sucesso)
        if status == 204:
            self.assertEqual(banco.corpo_http, b"")
        self.observar(banco, r, True, int(r.nome == "selecionar"))
        esperado = deepcopy(antes)
        cid = UUID(r.caminho.split("/")[4])
        agregado = list(esperado["agregados"][cid])
        linhas = set(esperado["bruto"]["itens"])
        if r.nome == "selecionar":
            tipo, iid = r.corpo["tipo"], UUID(r.corpo["item_id"])
            linhas.add((cid, tipo, iid))
            agregado[4] = agregado[4] | {ReferenciaCurriculo(CLASSES_ID[TIPOS.index(tipo)](iid))}
            itens = [{"tipo": t, "item_id": str(i)} for c, t, i in sorted(linhas) if c == cid]
            self.assertEqual(corpo, {"curriculo_id": str(cid), "itens": itens})
        elif r.nome == "desselecionar":
            partes = r.caminho.split("/")
            tipo, iid = partes[6], UUID(partes[7])
            linhas.remove((cid, tipo, iid))
            agregado[4] = agregado[4] - {ReferenciaCurriculo(CLASSES_ID[TIPOS.index(tipo)](iid))}
            self.assertIsNone(corpo)
        else:
            ordem = tuple(r.corpo["ordem_secoes"])
            esperado["bruto"]["curriculos"][cid]["ordem_secoes"] = ",".join(ordem)
            agregado[5] = tuple(type(agregado[5][0])(s) for s in ordem)
            self.assertIsNone(corpo)
        esperado["bruto"]["itens"] = tuple(sorted(linhas))
        esperado["agregados"][cid] = tuple(agregado)
        self.assertEqual(await banco.estado(), esperado)
        self.contar("controle_exec1_dono1" if r.nome == "selecionar" else "controle_exec1_dono0")
        return corpo

    async def controle(self, banco, operacao, *, usuario=USUARIO_A, curriculo=CURRICULO_A):
        """Exercita mesma operação/recurso e recompõe seleção por HTTP para parear negativa.

        Seleção e remoção têm inversa legítima, evitando que o próprio controle
        cause duplicata ou item ausente na tentativa que deve testar outra regra.
        """
        if operacao == "ordem":
            await self.sucesso(banco, rota(operacao, usuario, curriculo), usuario=usuario)
            return
        item = (ITEM_A_NOVO if usuario == USUARIO_A else identidade("idioma", 3)) if operacao == "selecionar" else (ITEM_A if usuario == USUARIO_A else ITEM_B)
        await self.sucesso(banco, rota(operacao, usuario, curriculo, item=item), usuario=usuario)
        inversa = "desselecionar" if operacao == "selecionar" else "selecionar"
        await self.sucesso(banco, rota(inversa, usuario, curriculo, item=item), usuario=usuario)

    async def recusa(self, banco, r, status, detalhe=None, *, token=None, executou=False, donos=0, erro_dto=None, **kwargs):
        """Prova negativa por camada, spy e ausência de delta SQL/agregado após controle.

        Snapshot é posterior à preparação; commit não é substituído por rollback.
        Erros DTO comparam loc/type sem ecoar entradas sensíveis ou correlação.
        """
        banco.zerar_observadores()
        antes = await banco.estado()
        codigo, corpo = await banco.solicitar(r, token, **kwargs)
        self.assertEqual(codigo, status)
        if erro_dto is not None:
            self.assertTrue(any(e["loc"] == erro_dto[0] and e["type"] == erro_dto[1] for e in corpo["detail"]))
        else:
            self.assertEqual(corpo, {"detail": detalhe})
        self.observar(banco, r, executou, donos)
        self.assertEqual(await banco.estado(), antes)
        texto = json.dumps(corpo, ensure_ascii=False)
        for marcador in ("ITEM PRIVADO B", "IDIOMA PRIVADO B", "CURRICULO PRIVADO B", "ESTUDANTE PRIVADO B", "b@example.test"):
            self.assertNotIn(marcador, texto)
        self.contar(f"recusa_{status}_exec{int(executou)}_dono{donos}")
        return corpo

    async def ler(self, banco, operacao):
        """Lê prévia/listagem por ASGI e compara SQL intacto para provar efeito sem escrita."""
        antes = await banco.estado()
        banco.zerar_observadores()
        status, corpo = await banco.solicitar(rota(operacao), banco.token_a)
        self.assertEqual(status, 200)
        for nome, spy in banco.spies.items():
            self.assertEqual((spy.call_count, spy.await_count), (int(nome == operacao),) * 2)
        self.assertEqual(await banco.estado(), antes)
        self.assertNotIn("ordem_secoes", corpo)
        return corpo

    async def test_fluxo_seleciona_seis_tipos_ordena_secoes_e_desseleciona(self):
        """P1 liga seleção, sort e remoção por HTTP para provar persistência e isolamento.

        Usa listas explícitas e SQL/agregado a cada escrita, sem exigir ordem
        personalizada na prévia nem usar comparadores produtivos como oráculo.
        """
        async with self.banco("P1-seis-tipos-fluxo") as b:
            for rodada in (0, 1):
                for tipo in reversed(TIPOS):
                    indice = (2, 1)[rodada] if tipo in TIPOS[:2] else (1, 2)[rodada]
                    await self.sucesso(b, rota("selecionar", tipo=tipo, item=identidade(tipo, indice)))
            previa = await self.ler(b, "previa")
            esperados = ([1101, 1102], [1201, 1202], [1302, 1301], [1402, 1401], [1502, 301, 1501], [1602, 1601])
            for secao, ids in zip(SECOES_PREVIA, esperados, strict=True):
                self.assertEqual([i["id"] for i in previa[secao]], [str(UUID(int=i)) for i in ids])
            await self.sucesso(b, rota("selecionar", tipo="projeto_academico", item=identidade("projeto_academico", 5)))
            previa = await self.ler(b, "previa")
            self.assertEqual([i["id"] for i in previa["projetos"]], [str(UUID(int=i)) for i in (1302, 1301, 1305)])
            listado = await self.ler(b, "listar")
            self.assertEqual(next(v["total_itens"] for v in listado["versoes"] if v["id"] == str(CURRICULO_A.valor)), 14)
            await self.sucesso(b, rota("ordem"))
            for tipo in TIPOS:
                await self.sucesso(b, rota("desselecionar", tipo=tipo, item=identidade(tipo, 1)))
            estado = await b.estado()
            self.assertEqual(estado["bruto"]["curriculos"][CURRICULO_A.valor]["ordem_secoes"], ",".join(INVERSA))
            previa = await self.ler(b, "previa")
            esperados = ([1102], [1202], [1302, 1305], [1402], [1502, 301], [1602])
            for secao, ids in zip(SECOES_PREVIA, esperados, strict=True):
                self.assertEqual([i["id"] for i in previa[secao]], [str(UUID(int=i)) for i in ids])
            listado = await self.ler(b, "listar")
            self.assertEqual(next(v["total_itens"] for v in listado["versoes"] if v["id"] == str(CURRICULO_A.valor)), 8)

    async def test_repetir_ordem_valida_preserva_texto_e_selecao(self):
        """P2 repete PUT e compara estado completo para caracterizar repetição válida."""
        async with self.banco("P2-repeticao") as b:
            await self.sucesso(b, rota("ordem"))
            antes = await b.estado()
            await self.sucesso(b, rota("ordem"))
            self.assertEqual(await b.estado(), antes)

    async def test_selecao_em_a_nao_altera_b_nem_segunda_versao_a(self):
        """P3 muda só A por três operações e relê A2/B para provar isolamento por versão."""
        async with self.banco("P3-isolamento") as b:
            inicial = await b.estado()
            item = identidade("projeto_academico", 1)
            for r in (rota("selecionar", tipo="projeto_academico", item=item), rota("ordem"), rota("desselecionar", tipo="projeto_academico", item=item)):
                await self.sucesso(b, r)
                atual = await b.estado()
                for cid in (CURRICULO_A2.valor, CURRICULO_B.valor):
                    self.assertEqual(atual["agregados"][cid], inicial["agregados"][cid])

    async def test_previa_caracteriza_item_resolvido_atual_e_omite_ausente(self):
        """P4 muda só double e relê DTO/SQL para caracterizar consumidor, não política de exclusão."""
        async with self.banco("P4-double-caracterizacao") as b:
            await self.sucesso(b, rota("selecionar"))
            antes = await b.estado()
            previa = await self.ler(b, "previa")
            self.assertEqual(len(previa["idiomas"]), 2)
            self.assertEqual(next(i["idioma"] for i in previa["idiomas"] if i["id"] == str(ITEM_A_NOVO.valor)), "IDIOMA NOVO A")
            mapa = b.itens.por_classe[type(ITEM_A_NOVO)]
            mapa[ITEM_A_NOVO] = replace(mapa[ITEM_A_NOVO], idioma="Conteúdo atualizado")
            previa = await self.ler(b, "previa")
            self.assertEqual(next(i["idioma"] for i in previa["idiomas"] if i["id"] == str(ITEM_A_NOVO.valor)), "Conteúdo atualizado")
            del mapa[ITEM_A_NOVO]
            previa = await self.ler(b, "previa")
            self.assertEqual([i["id"] for i in previa["idiomas"]], [str(ITEM_A.valor)])
            listado = await self.ler(b, "listar")
            self.assertEqual(next(v["total_itens"] for v in listado["versoes"] if v["id"] == str(CURRICULO_A.valor)), 2)
            self.assertEqual(await b.estado(), antes)

    async def test_sessao_b_recusada_no_caminho_a(self):
        """N1 controla A antes de B atacar mesma operação/recurso para provar guarda 403."""
        for op in OPERACOES:
            async with self.banco(f"N1-{op}") as b:
                await self.controle(b, op)
                await self.recusa(b, rota(op, item=ITEM_A if op == "desselecionar" else ITEM_A_NOVO), 403, ERRO_DONO, token=b.token_b)

    async def test_curriculo_alheio_sob_pessoa_autenticada_e_inexistente(self):
        """N2 compara 404 alheio/ausente por casos reais sem consultar itens.

        ID ausente não pode ter controle positivo literal; usa mesma operação
        no currículo existente do ator, documentando essa impossibilidade lógica.
        """
        for op in OPERACOES:
            respostas = []
            for ator, cid in ((USUARIO_B, CURRICULO_A), (USUARIO_A, CURRICULO_B), (USUARIO_A, CURRICULO_INEXISTENTE), (USUARIO_B, CURRICULO_INEXISTENTE)):
                async with self.banco(f"N2-{op}-ator{ator.valor.int}-curriculo{cid.valor.int}") as b:
                    dono = USUARIO_A if cid == CURRICULO_A else USUARIO_B if cid == CURRICULO_B else ator
                    controle_cid = cid if cid != CURRICULO_INEXISTENTE else CURRICULO_A if ator == USUARIO_A else CURRICULO_B
                    await self.controle(b, op, usuario=dono, curriculo=controle_cid)
                    respostas.append(await self.recusa(b, rota(op, ator, cid), 404, ERRO_CURRICULO, token=b.token_a if ator == USUARIO_A else b.token_b, executou=True))
            self.assertEqual(respostas, [{"detail": ERRO_CURRICULO}] * 4)

    async def test_item_alheio_ou_ausente_por_tipo(self):
        """N3 usa double, não adaptador real, para provar 404 por tipo sem alterar SQL.

        Controla B com o mesmo item e A com item próprio antes da tentativa para
        separar reação do consumidor da existência real em produção não provada.
        """
        for tipo in TIPOS:
            respostas = []
            for indice in (3, 90):
                async with self.banco(f"N3-{tipo}-indice{indice}") as b:
                    for ator, cid, iid in ((USUARIO_B, CURRICULO_B, identidade(tipo, 3)), (USUARIO_A, CURRICULO_A, identidade(tipo, 1))):
                        await self.sucesso(b, rota("selecionar", ator, cid, tipo, iid), usuario=ator)
                        await self.sucesso(b, rota("desselecionar", ator, cid, tipo, iid), usuario=ator)
                    respostas.append(await self.recusa(b, rota("selecionar", tipo=tipo, item=identidade(tipo, indice)), 404, ERRO_ITEM, token=b.token_a, executou=True, donos=1))
            self.assertEqual(respostas, [{"detail": ERRO_ITEM}] * 2)

    async def test_selecao_duplicada_nao_altera_banco(self):
        """N4 repete POST após controle 201 para provar 422 de duplicata sem linha nova."""
        async with self.banco("N4-duplicata") as b:
            await self.sucesso(b, rota("selecionar"))
            await self.recusa(b, rota("selecionar"), 422, "Item já está incluído no currículo.", token=b.token_a, executou=True, donos=1)

    async def test_desselecao_ausente_nao_altera_banco(self):
        """N5 seleciona/remove e repete DELETE para provar domínio sem consulta de item."""
        async with self.banco("N5-remocao-ausente") as b:
            await self.sucesso(b, rota("selecionar"))
            await self.sucesso(b, rota("desselecionar"))
            await self.recusa(b, rota("desselecionar"), 422, "Item não está incluído no currículo.", token=b.token_a, executou=True)

    async def test_tipo_ou_uuid_invalido_na_selecao_e_remocao(self):
        """N6 varia formato após controle e observa DTO sem executor para provar 422 de entrada."""
        for op in ("selecionar", "desselecionar"):
            valido = rota(op, item=ITEM_A if op == "desselecionar" else ITEM_A_NOVO)
            variantes = []
            for tipo in ("curso", "hobby"):
                r = replace(valido, corpo={**valido.corpo, "tipo": tipo}) if op == "selecionar" else replace(valido, caminho=valido.caminho.replace("/idioma/", f"/{tipo}/"))
                variantes.append((tipo, r, (["body" if op == "selecionar" else "path", "tipo"], "literal_error")))
            r = replace(valido, corpo={**valido.corpo, "item_id": "nao-uuid"}) if op == "selecionar" else replace(valido, caminho=valido.caminho.rsplit("/", 1)[0] + "/nao-uuid")
            variantes.append(("item-malformado", r, (["body" if op == "selecionar" else "path", "item_id"], "uuid_parsing")))
            if op == "selecionar":
                for campo in ("tipo", "item_id"):
                    variantes.append((f"sem-{campo}", replace(valido, corpo={k: v for k, v in valido.corpo.items() if k != campo}), (["body", campo], "missing")))
            for campo, valor in (("usuario_id", USUARIO_A.valor), ("curriculo_id", CURRICULO_A.valor)):
                variantes.append((campo, replace(valido, caminho=valido.caminho.replace(str(valor), "nao-uuid")), (["path", campo], "uuid_parsing")))
            for nome, r, erro in variantes:
                async with self.banco(f"N6-{op}-{nome}") as b:
                    await self.controle(b, op)
                    await self.recusa(b, r, 422, token=b.token_a, erro_dto=erro)

    async def test_ordem_com_secao_desconhecida_ou_valor_invalido(self):
        """N7 controla PUT e varia enum/lista para provar validação antes do executor."""
        for nome, ordem, loc, tipo in (
            ("desconhecida", ["hobbies", *INVERSA[1:]], ["body", "ordem_secoes", 0], "enum"),
            ("numero", [-1, *INVERSA[1:]], ["body", "ordem_secoes", 0], "enum"),
            ("objeto", {}, ["body", "ordem_secoes"], "list_type"),
            ("null", None, ["body", "ordem_secoes"], "list_type"),
        ):
            async with self.banco(f"N7-{nome}") as b:
                await self.controle(b, "ordem")
                await self.recusa(b, replace(rota("ordem"), corpo={"ordem_secoes": ordem}), 422, token=b.token_a, erro_dto=(loc, tipo))

    async def test_ordem_incompleta_ou_extensa(self):
        """N8 compara tamanhos seis/zero/oito após controle para provar limite DTO sem escrita."""
        for lista, tipo in ((list(INVERSA[:6]), "too_short"), ([], "too_short"), ([*INVERSA, INVERSA[0]], "too_long")):
            async with self.banco(f"N8-tamanho{len(lista)}") as b:
                await self.controle(b, "ordem")
                await self.recusa(b, replace(rota("ordem"), corpo={"ordem_secoes": lista}), 422, token=b.token_a, erro_dto=(["body", "ordem_secoes"], tipo))

    async def test_ordem_repetida_com_sete_entradas(self):
        """N9 mantém tamanho sete e repete seção para provar 422 de domínio com executor único."""
        async with self.banco("N9-permutacao") as b:
            await self.controle(b, "ordem")
            r = replace(rota("ordem"), corpo={"ordem_secoes": [INVERSA[1], *INVERSA[1:]]})
            await self.recusa(b, r, 422, ERRO_ORDEM, token=b.token_a, executou=True)

    async def test_dono_extra_na_ordem_e_ignorado_na_selecao(self):
        """N10 compara POST tolerante e PUT estrito para caracterizar extras sem trocar dono."""
        resultados = []
        for extra in (False, True):
            async with self.banco(f"N10-selecao-extra{extra}") as b:
                r = rota("selecionar")
                if extra:
                    r = replace(r, corpo={**r.corpo, "usuario_id": str(USUARIO_B.valor)})
                resultados.append((await self.sucesso(b, r), await b.estado()))
        self.assertEqual(resultados[0], resultados[1])
        async with self.banco("N10-ordem-extra") as b:
            await self.controle(b, "ordem")
            r = replace(rota("ordem"), corpo={**rota("ordem").corpo, "usuario_id": str(USUARIO_B.valor)})
            await self.recusa(b, r, 422, token=b.token_a, erro_dto=(["body", "usuario_id"], "extra_forbidden"))

    async def test_credenciais_invalidas_interrompem_operacoes(self):
        """N11 invalida credencial após controle para provar 401 uniforme sem executar negócio.

        Cookie ausente é testado separadamente com Bearer, query e corpo válidos,
        sem registrar credenciais, para provar que transportes extras não autenticam.
        """
        for op in OPERACOES:
            for estado in ("ausente", "bearer", "query", "corpo", "desconhecido", "expirada", "revogada"):
                async with self.banco(f"N11-{op}-{estado}") as b:
                    await self.controle(b, op)
                    r = rota(op, item=ITEM_A if op == "desselecionar" else ITEM_A_NOVO)
                    token, extras = None, {}
                    if estado in {"expirada", "revogada"}:
                        await b.invalidar_sessao(estado)
                        token = b.token_a
                    elif estado == "desconhecido":
                        token = "nao-emitido-sintetico"
                    elif estado == "bearer":
                        extras["bearer"] = b.token_a
                    elif estado == "query":
                        extras["query"] = "token=" + b.token_a
                    elif estado == "corpo":
                        extras["corpo"] = {**(r.corpo or {}), "token": b.token_a}
                    await self.recusa(b, r, 401, ERRO_SESSAO, token=token, **extras)

    async def test_conta_excluida_interrompe_operacoes(self):
        """N12 exclui conta diretamente após controle e compara pós-preparo para provar 401."""
        for op in OPERACOES:
            async with self.banco(f"N12-{op}") as b:
                await self.controle(b, op)
                await b.sessao.execute(update(UsuarioRegistro).where(UsuarioRegistro.id == USUARIO_A.valor).values(deleted_at=datetime.now(timezone.utc)))
                await b.sessao.commit()
                await self.recusa(b, rota(op, item=ITEM_A if op == "desselecionar" else ITEM_A_NOVO), 401, ERRO_SESSAO, token=b.token_a)

    async def test_executor_ausente_com_autenticacao_ativa(self):
        """N13 omite só executor após controle com ele ligado para provar 503 sem bypass de auth."""
        for op, mensagem in zip(OPERACOES, ("Seleção indisponível.", "Desseleção indisponível.", "Atualização da ordem indisponível."), strict=True):
            async with self.banco(f"N13-{op}") as b:
                await self.controle(b, op)
                b.compor(ausente=op)
                await self.recusa(b, rota(op, item=ITEM_A if op == "desselecionar" else ITEM_A_NOVO), 503, mensagem, token=b.token_a)

    async def test_precedencia_recusa_na_camada_correta(self):
        """N14 combina erros com controle pareado para distinguir middleware, DTO e aplicação."""
        for variante in ("sem-cookie", "dono-b", "sem-executor", "curriculo-ausente"):
            async with self.banco(f"N14-{variante}") as b:
                if variante == "curriculo-ausente":
                    await self.controle(b, "ordem")
                    r = replace(rota("ordem", curriculo=CURRICULO_INEXISTENTE), corpo={"ordem_secoes": [INVERSA[1], *INVERSA[1:]]})
                    await self.recusa(b, r, 404, ERRO_CURRICULO, token=b.token_a, executou=True)
                else:
                    await self.controle(b, "selecionar")
                    r = replace(rota("selecionar"), corpo={})
                    if variante == "sem-executor":
                        b.compor(ausente="selecionar")
                        await self.recusa(b, r, 422, token=b.token_a, erro_dto=(["body", "tipo"], "missing"))
                    else:
                        await self.recusa(b, r, 401 if variante == "sem-cookie" else 403, ERRO_SESSAO if variante == "sem-cookie" else ERRO_DONO, token=None if variante == "sem-cookie" else b.token_b)
