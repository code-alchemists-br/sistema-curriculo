"""Verifica S1–S10 pela API com middleware e sessão persistida reais.

ConsultaProprietarioItem e ConsultaItemPerfil são doubles, pois não há adapter
concreto: S5 prova a reação do caso de uso e do banco, não a proteção de um
adapter produtivo de itens. A composição montada no teste não certifica a
composição de produção nem a autenticação persistida de main. Não importa main.app.
"""

# Proveniência: decision-analysis prompts/backend/20261018-123741-recusa-curriculo-alheio-middleware-ativo-v001.md#v001

import json
import unittest
from contextlib import asynccontextmanager
from copy import deepcopy

from backend.domain.secao_curriculo import ORDEM_PADRAO_SECOES
from backend.tests.fixtures.curriculos_autenticados_integracao import (
    CORPO_VERSAO,
    CURRICULO_A,
    CURRICULO_B,
    CURRICULO_INEXISTENTE,
    CURRICULO_NOVO,
    ITEM_A,
    ITEM_A_NOVO,
    ITEM_B,
    ITEM_INEXISTENTE,
    ORDEM_ALTERADA,
    SKIP_SEM_AIOSQLITE,
    USUARIO_A,
    USUARIO_B,
    BancoCurriculosAutenticadosIntegracao,
    requisitar,
    rotas_curriculo,
    verificar_revisoes_alembic,
)

ERRO_SESSAO = {"detail": "Sessão ausente ou inválida."}
ERRO_DONO = {"detail": "A sessão não pode acessar este recurso."}
ERRO_CURRICULO = {"detail": "Versão de currículo não encontrada."}
ERRO_ITEM = {"detail": "Item do perfil não encontrado."}


@SKIP_SEM_AIOSQLITE
class RecusaCurriculoAlheioIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Integra oito rotas com banco novo por subcenário para proteger A/B.

    Usa status exato, spies dos executores reais e snapshots independentes,
    distinguindo negação no middleware de recusa de propriedade do objeto.
    """

    async def asyncSetUp(self) -> None:
        """Verifica duplicações antes de preparar cada teste integrado.

        O preflight identifica pares de scripts no motivo de SkipTest, sem
        converter falhas de migration ou asserções de segurança em skips.
        """
        verificar_revisoes_alembic()

    @asynccontextmanager
    async def _banco(self):
        """Fornece banco exclusivo ao subteste e garante sua limpeza em finally.

        A criação inclui migrations e seed confirmados; o fechamento ocorre
        mesmo se o fluxo HTTP ou um oráculo falhar, isolando todas as operações.
        """
        banco = await BancoCurriculosAutenticadosIntegracao.criar()
        try:
            yield banco
        finally:
            await banco.fechar()

    def _executores(self, banco, esperado=None) -> None:
        """Confere chamada e await de um único executor ou nenhum na recusa.

        Inspeciona todos os spies e a identidade do DTO interno, para comprovar
        que sessão A não executa operações por B nem perde a guarda de entrada.
        """
        for nome, spy in banco.spies.items():
            if nome == esperado:
                self.assertEqual(spy.call_count, 1, nome)
                self.assertEqual(spy.await_count, 1, nome)
                self.assertEqual(spy.call_args, spy.await_args, nome)
                self.assertEqual(spy.await_args.args[0].usuario_id, USUARIO_A, nome)
            else:
                spy.assert_not_called()
                spy.assert_not_awaited()

    def _sem_dados_b(self, corpo) -> None:
        """Procura marcadores e IDs privados de B no JSON devolvido pela API.

        Compara texto serializado com valores sintéticos conhecidos, para
        detectar divulgação mesmo que a resposta use status de erro correto.
        """
        texto = json.dumps(corpo, ensure_ascii=False)
        for privado in (
            "CURRICULO PRIVADO B", "ESTUDANTE PRIVADO B", "IDIOMA PRIVADO B",
            "b@example.test", str(USUARIO_B.valor), str(CURRICULO_B.valor), str(ITEM_B.valor),
        ):
            self.assertNotIn(privado, texto)
        self.assertNotIn("hash_senha", texto)

    async def _recusa(self, banco, rota, status, corpo_esperado, *, token, executor=None, **kwargs):
        """Compara resposta, execução e SQL antes/depois de uma tentativa negada.

        Confirma a transação antes de ler outra sessão sem rollback, para que
        uma resposta de erro não esconda alterações indevidas em A ou B.
        """
        antes = await banco.snapshot()
        resposta = await requisitar(banco, rota, token, **kwargs)
        self.assertEqual(resposta, (status, corpo_esperado))
        self._sem_dados_b(resposta[1])
        self._executores(banco, executor)
        self.assertEqual(await banco.snapshot(), antes, "Recusa alterou banco")
        return resposta

    async def _sucesso(self, banco, rota, **kwargs):
        """Verifica o controle próprio e seu efeito completo no banco de A/B.

        Constrói a mudança esperada sobre o snapshot e compara todas as colunas,
        seleções e contagem, para excluir sucesso HTTP sem operação funcional.
        """
        antes = await banco.snapshot()
        status, corpo = await requisitar(banco, rota, banco.token_a, **kwargs)
        self.assertEqual(status, rota.sucesso)
        self._sem_dados_b(corpo)
        self._executores(banco, rota.nome)
        esperado = deepcopy(antes)
        versao = esperado["curriculos"][CURRICULO_A.valor]
        if rota.nome == "listar":
            self.assertEqual(corpo, {"versoes": [{
                "id": str(CURRICULO_A.valor), "titulo_versao": "CURRICULO PRIVADO A",
                "layout": "classico", "is_public": False, "total_itens": 1,
            }]})
        elif rota.nome == "previa":
            self.assertEqual(corpo, {
                "curriculo_id": str(CURRICULO_A.valor),
                "titulo_versao": "CURRICULO PRIVADO A", "layout": "classico",
                "estudante": {"nome": "ESTUDANTE PRIVADO A", "email": "a@example.test",
                              "contato": None},
                "formacoes": [], "experiencias": [], "projetos": [], "competencias": [],
                "idiomas": [{"id": str(ITEM_A.valor), "idioma": "IDIOMA PRIVADO A",
                             "nivel": "Intermediário"}], "documentos": [],
            })
        elif rota.nome == "criar":
            self.assertEqual(corpo, {"id": str(CURRICULO_NOVO.valor), **CORPO_VERSAO})
            esperado["curriculos"][CURRICULO_NOVO.valor] = {
                **versao, "id": CURRICULO_NOVO.valor, **CORPO_VERSAO,
                "ordem_secoes": ",".join(secao.value for secao in ORDEM_PADRAO_SECOES),
            }
            esperado["quantidade"] += 1
        elif rota.nome == "editar":
            self.assertEqual(corpo, {"id": str(CURRICULO_A.valor), **CORPO_VERSAO})
            versao.update(CORPO_VERSAO)
        elif rota.nome == "ordem":
            self.assertIsNone(corpo)
            versao["ordem_secoes"] = ",".join(ORDEM_ALTERADA)
        elif rota.nome == "excluir":
            self.assertIsNone(corpo)
            del esperado["curriculos"][CURRICULO_A.valor]
            esperado["quantidade"] -= 1
            esperado["itens"] = tuple(item for item in antes["itens"] if item[0] != CURRICULO_A.valor)
        elif rota.nome == "selecionar":
            self.assertEqual(corpo, {"curriculo_id": str(CURRICULO_A.valor), "itens": [
                {"tipo": "idioma", "item_id": str(item.valor)} for item in (ITEM_A, ITEM_A_NOVO)
            ]})
            esperado["itens"] = tuple(sorted(
                (*antes["itens"], (CURRICULO_A.valor, "idioma", ITEM_A_NOVO.valor))))
        elif rota.nome == "desselecionar":
            self.assertIsNone(corpo)
            esperado["itens"] = tuple(item for item in antes["itens"] if item[0] != CURRICULO_A.valor)
        else:
            self.fail(f"Controle positivo sem oráculo: {rota.nome}")
        depois = await banco.snapshot()
        self.assertEqual(depois, esperado, "Efeito próprio divergiu ou alterou B")
        return status, corpo, depois

    async def test_s1_controle_positivo_em_cada_rota(self):
        """Prova oito operações próprias por HTTP e efeito SQL confirmado.

        Usa banco novo por rota e DTO real com A para garantir que as recusas
        dos demais cenários não sejam causadas por endpoints sempre falhando.
        """
        for rota in rotas_curriculo():
            with self.subTest(cenario="S1", operacao=f"{rota.metodo} {rota.caminho}",
                              identidade="sessão A, dono A, currículo A"):
                async with self._banco() as banco:
                    await self._sucesso(banco, rota)

    async def test_s2_dono_b_no_caminho_recusado_antes_dos_executores(self):
        """Exige 403 nas oito rotas com sessão A e dono B no caminho.

        Verifica zero executores e snapshot SQL idêntico, inclusive contagem
        após tentativa de criação, para provar a interrupção pelo middleware.
        """
        for rota in rotas_curriculo(USUARIO_B, CURRICULO_B):
            with self.subTest(cenario="S2", operacao=f"{rota.metodo} {rota.caminho}",
                              identidade="sessão A, dono B, currículo B"):
                async with self._banco() as banco:
                    await self._recusa(banco, rota, 403, ERRO_DONO, token=banco.token_a)

    async def test_s3_curriculo_b_sob_dono_a_recusado_no_caso_de_uso(self):
        """Exige 404 de objeto alheio nas seis rotas com ID de versão.

        Mantém A no caminho e comprova execução real uma vez antes da recusa,
        sem consultas de item nem escrita SQL, para testar a segunda guarda.
        """
        for rota in rotas_curriculo(USUARIO_A, CURRICULO_B)[2:]:
            with self.subTest(cenario="S3", operacao=f"{rota.metodo} {rota.caminho}",
                              identidade="sessão A, dono A, currículo B"):
                async with self._banco() as banco:
                    await self._recusa(banco, rota, 404, ERRO_CURRICULO,
                                       token=banco.token_a, executor=rota.nome)
                    self.assertEqual(banco.itens.consultas_item, [])
                    self.assertEqual(banco.itens.consultas_proprietario, [])

    async def test_s4_curriculo_alheio_e_inexistente_tem_mesma_resposta(self):
        """Compara status e JSON de objeto B e inexistente por cada uma das seis rotas.

        Usa bancos equivalentes novos e não compara X-Correlation-ID nem erros
        de outras camadas, para verificar somente ocultação de existência.
        """
        respostas_b = {}
        for recurso, identidade in ((CURRICULO_B, "B"), (CURRICULO_INEXISTENTE, "inexistente")):
            for rota in rotas_curriculo(USUARIO_A, recurso)[2:]:
                with self.subTest(cenario="S4", operacao=f"{rota.metodo} {rota.caminho}",
                                  identidade=f"sessão A, dono A, currículo {identidade}"):
                    async with self._banco() as banco:
                        resposta = await self._recusa(
                            banco, rota, 404, ERRO_CURRICULO,
                            token=banco.token_a, executor=rota.nome)
                        if identidade == "B":
                            respostas_b[rota.nome] = resposta
                        else:
                            self.assertIn(rota.nome, respostas_b, "Comparação alheia não concluiu")
                            self.assertEqual(resposta, respostas_b[rota.nome])

    async def test_s5_item_alheio_e_inexistente_nao_entram_no_curriculo_a(self):
        """Prova reação do caso real e do banco com portas de item em doubles.

        ConsultaProprietarioItem e ConsultaItemPerfil não têm adapter concreto;
        os doubles devolvem dono B ou ausência. O teste não prova que um adapter
        de produção impeça acesso a item alheio; comprova 404 e seleção intacta.
        O controle positivo de seleção está em S1.
        """
        rota = rotas_curriculo()[6]
        respostas = []
        for item, identidade in ((ITEM_B, "B"), (ITEM_INEXISTENTE, "inexistente")):
            with self.subTest(cenario="S5", operacao=f"{rota.metodo} {rota.caminho}",
                              identidade=f"sessão A, dono A, item {identidade}"):
                async with self._banco() as banco:
                    respostas.append(await self._recusa(
                        banco, rota, 404, ERRO_ITEM, token=banco.token_a,
                        executor="selecionar", corpo={"tipo": "idioma", "item_id": str(item.valor)}))
                    self.assertEqual(len(banco.itens.consultas_proprietario), 1)
                    self.assertEqual(banco.itens.consultas_proprietario[0].item_id, item)
        self.assertEqual(len(respostas), 2)
        self.assertEqual(respostas[0], respostas[1])

    async def test_s6_caracteriza_extras_ignorados_sem_trocar_proprietario(self):
        """Caracteriza o comportamento atual de extras ignorados, ligado a L1/L3.

        Compara chamadas próprias equivalentes com e sem usuario_id=B para
        separar a política de extras da segurança: dono continua A e B não
        muda; o banco final deve ser idêntico ao da operação legítima.
        """
        for rota in rotas_curriculo():
            if rota.nome not in {"listar", "previa", "criar", "editar", "selecionar"}:
                continue
            resultados = []
            for extra in (False, True):
                with self.subTest(cenario="S6-caracterização",
                                  operacao=f"{rota.metodo} {rota.caminho}",
                                  identidade="sessão A, dono A, extra B" if extra else "sessão A, dono A",
                                  extra=extra):
                    async with self._banco() as banco:
                        kwargs = {}
                        if extra and rota.metodo == "GET":
                            kwargs["query"] = f"usuario_id={USUARIO_B.valor}"
                        elif extra:
                            kwargs["corpo"] = {**rota.corpo, "usuario_id": str(USUARIO_B.valor)}
                        resultados.append(await self._sucesso(banco, rota, **kwargs))
            self.assertEqual(len(resultados), 2)
            self.assertEqual(resultados[0], resultados[1], rota.nome)

    async def test_s6_caracteriza_extra_proibido_na_ordem_sem_efeitos(self):
        """Caracteriza o comportamento atual de extra=forbid, ligado a L1/L3.

        Acrescenta usuario_id=B ao DTO de ordem e observa 422 por campo extra;
        a segurança central exige zero executor e banco A/B intacto, sem
        estender essa política de validação aos demais endpoints.
        """
        rota = rotas_curriculo()[3]
        with self.subTest(cenario="S6-caracterização-ordem",
                          operacao=f"{rota.metodo} {rota.caminho}",
                          identidade="sessão A, dono A, extra B"):
            async with self._banco() as banco:
                antes = await banco.snapshot()
                status, corpo = await requisitar(banco, rota, banco.token_a,
                    corpo={**rota.corpo, "usuario_id": str(USUARIO_B.valor)})
                self._executores(banco)
                self.assertEqual(await banco.snapshot(), antes)
                self.assertEqual(status, 422)
                self.assertEqual(len(corpo["detail"]), 1)
                self.assertEqual(corpo["detail"][0]["type"], "extra_forbidden")
                self.assertEqual(corpo["detail"][0]["loc"], ["body", "usuario_id"])

    async def _sessao_recusada(self, cenario, estado):
        """Aplica um estado de credencial às oito rotas e exige 401 sem efeitos.

        Revoga/expira por banco real ou usa token ausente/desconhecido, com
        Bearer e parâmetros incapazes de substituir o cookie, para validar a
        precedência da autenticação sobre autorização e execução.
        """
        for rota in rotas_curriculo():
            with self.subTest(cenario=cenario, operacao=f"{rota.metodo} {rota.caminho}",
                              identidade=f"sessão A {estado}, dono A"):
                async with self._banco() as banco:
                    if estado in {"revogada", "expirada"}:
                        await banco.invalidar_sessao(estado)
                    token = (None if estado == "ausente" else
                             "cookie-sintetico-nao-emitido" if estado == "desconhecida" else
                             banco.token_a)
                    corpo = {**(rota.corpo or {}), "token": banco.token_a,
                             "usuario_id": str(USUARIO_B.valor)}
                    await self._recusa(
                        banco, rota, 401, ERRO_SESSAO, token=token,
                        bearer=banco.token_a, query=f"token={banco.token_a}&usuario_id={USUARIO_B.valor}",
                        corpo=corpo)

    async def test_s7_sem_cookie_recusa_todas_as_rotas(self):
        """Exige 401 sem cookie apesar de Bearer, query e corpo com token válido.

        Percorre oito operações e compara SQL e spies para comprovar que esses
        transportes alternativos não autenticam nem substituem o cookie seguro.
        """
        await self._sessao_recusada("S7", "ausente")

    async def test_s8_sessao_revogada_recusa_todas_as_rotas(self):
        """Reapresenta cookie A após revogação real e exige 401 nas oito rotas.

        Confirma revogação antes de chamar HTTP, sem substituir autenticador,
        para comprovar que a consulta persistida bloqueia executores e escritas.
        """
        await self._sessao_recusada("S8", "revogada")

    async def test_s9_sessao_expirada_recusa_todas_as_rotas(self):
        """Expira sessão A no banco com margem e exige 401 nas oito operações.

        Usa data passada confirmada, sem sleep, e verifica SQL independente e
        spies para provar recusa real sem modificar o relógio de produção.
        """
        await self._sessao_recusada("S9", "expirada")

    async def test_s10_cookie_desconhecido_recusa_todas_as_rotas(self):
        """Envia cookie não emitido e exige 401, mesmo com Bearer válido.

        Percorre as oito rotas e observa banco e executores para demonstrar
        consulta de hash real sem sessão correspondente, além do double antigo.
        """
        await self._sessao_recusada("S10", "desconhecida")
