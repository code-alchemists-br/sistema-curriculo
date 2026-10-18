"""Exercita login, sessão e logout pelas rotas ASGI com banco migrado real.

Os cenários H01–H10 e R01–R03 controlam tempo e transações no harness para
verificar o contrato HTTP sem doubles de autenticação ou persistência.
"""

# Proveniência: decision-analysis prompts/backend/20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md#v001

import base64
import unittest
from datetime import timedelta, timezone
from urllib.parse import urlencode
from uuid import UUID

from backend.tests.fixtures.credenciais_sessao import (
    AIOSQLITE_DISPONIVEL,
    COLUNAS_SESSAO,
    INSTANTE_T,
    MOTIVO_SEM_AIOSQLITE,
    SENHA_SINTETICA,
    USUARIO_A,
    USUARIO_B,
    BancoCredenciaisSessao,
    resumo_token,
    token_sintetico,
)


@unittest.skipUnless(AIOSQLITE_DISPONIVEL, MOTIVO_SEM_AIOSQLITE)
class ContratoCredenciaisSessaoIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Valida rotas reais sobre SQLite exclusivo e proxies que delegam ao perfil.

    Reabre aplicação e AsyncSession por operação e lê snapshots após commit
    externo para testar o contrato integrado sem certificar wiring de produção.
    """

    async def asyncSetUp(self) -> None:
        """Migra banco por teste e executa controles positivos antes das negativas.

        Registra cleanup antecipado, faz login de B, consulta e edição própria
        reais para demonstrar que autenticação e proxies permitem operações.
        """
        self.banco = BancoCredenciaisSessao()
        self.addAsyncCleanup(self.banco.fechar)
        await self.banco.preparar()
        self.token_controle = await self._login("B")
        await self._consultar_proprio(self.token_controle, "B")
        with self.subTest(operacao="controle-edicao-propria", identidade="B"):
            resposta = await self.banco.requisitar(
                "PUT", f"/estudantes/{USUARIO_B}", token=self.token_controle,
                dados={"nome": "Pessoa B", "email": "b@example.test"},
            )
            self.assertEqual(resposta.status, 200)
            self.assertEqual(resposta.edicoes, (USUARIO_B,))
            self.assertTrue(resposta.json().get("id") == str(USUARIO_B), "Identidade pública divergente")

    def _assert_cookie(self, resposta, *, removido=False):
        """Confere atributos contratuais sem imprimir conteúdo do cookie.

        Analisa o único Set-Cookie e compara valores por booleanos para validar
        emissão ou remoção sem vazar credenciais em mensagens de asserção.
        """
        cookie = resposta.cookie_sessao()
        atributos = {
            "path": "/", "max-age": "0" if removido else "28800",
            "secure": True, "httponly": True, "samesite": "lax", "domain": "",
        }
        for atributo, esperado in atributos.items():
            atual = cookie[atributo]
            if atributo == "samesite":
                atual = atual.lower()
            self.assertTrue(atual == esperado, f"Atributo {atributo} divergente [REDACTED]")
        if removido:
            self.assertTrue(cookie.value == "", "Cookie não removido [REDACTED]")
        return cookie

    async def _login(self, identidade="A") -> str:
        """Emite sessão por login HTTP real e verifica o controle positivo.

        Confere resposta vazia, atributos e codificação de 32 bytes sem mostrar
        token, retornando o segredo apenas em memória para operações seguintes.
        """
        with self.subTest(operacao="POST /acessos positivo", identidade=identidade):
            resposta = await self.banco.requisitar(
                "POST", "/acessos",
                dados={"email": f"{identidade.lower()}@example.test", "senha": SENHA_SINTETICA},
            )
            self.assertEqual(resposta.status, 204)
            self.assertTrue(resposta.corpo == b"", "Resposta 204 não vazia [REDACTED]")
            token = self._assert_cookie(resposta).value
            self.assertEqual(len(token), 43)
            self.assertTrue("=" not in token, "Padding inesperado [REDACTED]")
            self.assertTrue(all(c.isascii() and (c.isalnum() or c in "-_") for c in token))
            try:
                tamanho = len(base64.urlsafe_b64decode(token + "="))
            except ValueError:
                self.fail("Codificação de token inválida [REDACTED]")
            self.assertEqual(tamanho, 32)
        return token

    async def _consultar_proprio(self, token, identidade="A", instante=INSTANTE_T):
        """Prova uso válido por perfil público e identidade encaminhada ao caso.

        Faz GET via nova aplicação e verifica DTO e proxy real, sem exigir UUID
        no corpo que o DTO atual omite nem imprimir token ou hash em falhas.
        """
        usuario = USUARIO_A if identidade == "A" else USUARIO_B
        with self.subTest(operacao="GET perfil próprio", identidade=identidade):
            resposta = await self.banco.requisitar(
                "GET", f"/estudantes/{usuario}", token=token, instante=instante,
            )
            self.assertEqual(resposta.status, 200)
            self.assertEqual(resposta.consultas, (usuario,))
            esperado = {
                "nome": f"Pessoa {identidade}", "email": f"{identidade.lower()}@example.test",
                "telefones": [], "cidade": None, "linkedin": None, "curriculo_lattes": None,
            }
            self.assertTrue(resposta.json() == esperado, "DTO de perfil divergente [REDACTED]")
            self.assertTrue(token.encode() not in resposta.corpo, "Token exposto [REDACTED]")
            self.assertTrue(resumo_token(token).encode() not in resposta.corpo, "Resumo exposto [REDACTED]")
            self.assertFalse(bool(resposta.cabecalhos("set-cookie")), "Consulta renovou cookie [REDACTED]")
        return resposta

    def _assert_401(self, resposta) -> None:
        """Confere negativa uniforme e ausência de chamadas aos casos de perfil.

        Compara somente valores seguros e contadores para provar bloqueio antes
        do caso real sem interpretar detalhes de credenciais ou imprimir corpo.
        """
        self.assertEqual(resposta.status, 401)
        self.assertTrue(
            resposta.json() == {"detail": "Sessão ausente ou inválida."},
            "Falha de sessão não uniforme [REDACTED]",
        )
        self.assertEqual(resposta.edicoes, ())
        self.assertEqual(resposta.consultas, ())

    async def _assert_intacto(self, anterior) -> None:
        """Compara snapshots de sessões e usuários obtidos em sessões distintas.

        Usa igualdade booleana sem formatar linhas para detectar mutação de
        qualquer coluna sem incluir hashes ou credenciais na mensagem de erro.
        """
        self.assertTrue(anterior == await self.banco.snapshot(), "Estado alterado [REDACTED]")

    async def _trio(self) -> tuple[str, str, str]:
        """Prepara A1, A2 e B1 válidas em transações próprias de banco real.

        Usa massa determinística da fixture, além do controle positivo de B,
        para observar isolamento de revogação sem depender da ordem de testes.
        """
        a1 = await self.banco.semear_sessao(101, USUARIO_A)
        a2 = await self.banco.semear_sessao(102, USUARIO_A)
        b1 = await self.banco.semear_sessao(103, USUARIO_B)
        return a1, a2, b1

    async def _logout(self, token, identidade, instante=INSTANTE_T):
        """Exercita DELETE real e confere resposta vazia e remoção segura.

        Abre operação transacional nova e identifica apenas a sessão por rótulo
        no subTest, para testar idempotência sem imprimir seu segredo.
        """
        with self.subTest(operacao="DELETE /sessao/atual", identidade=identidade):
            resposta = await self.banco.requisitar(
                "DELETE", "/sessao/atual", token=token, instante=instante,
            )
            self.assertEqual(resposta.status, 204)
            self.assertTrue(resposta.corpo == b"", "Resposta 204 não vazia [REDACTED]")
            self._assert_cookie(resposta, removido=True)
        return resposta

    async def test_H01_emissao_cookie_e_persistencia_duravel(self) -> None:
        """H01 verifica emissão HTTP e linha relida após commit controlado.

        Faz login A real e compara hash, datas e proprietário em sessão nova
        para comprovar transporte e persistência sem expor o token em asserts.
        """
        antes = await self.banco.snapshot()
        token = await self._login()
        with self.subTest(operacao="releitura pós-login", identidade="A"):
            depois = await self.banco.snapshot()
            self.assertEqual(len(depois["sessoes"]), len(antes["sessoes"]) + 1)
            self.assertTrue(antes["usuarios"] == depois["usuarios"])
            linhas = [linha._mapping for linha in depois["sessoes"] if linha.token_hash == resumo_token(token)]
            self.assertEqual(len(linhas), 1)
            linha = linhas[0]
            self.assertEqual(tuple(linha), COLUNAS_SESSAO)
            self.assertIsInstance(linha["id"], UUID)
            self.assertEqual(linha["usuario_id"], USUARIO_A)
            self.assertTrue(linha["token_hash"] == resumo_token(token))
            self.assertTrue(linha["token_hash"] != token)
            self.assertIsNone(linha["revogada_em"])
            # Somente a asserção repõe UTC: SQLite não preserva tzinfo e a
            # fixture gravou estes instantes em UTC, sem conversão de fuso.
            criada = linha["criada_em"].replace(tzinfo=timezone.utc)
            expira = linha["expira_em"].replace(tzinfo=timezone.utc)
            self.assertEqual(criada, INSTANTE_T)
            self.assertEqual(expira - criada, timedelta(hours=8))
        await self._consultar_proprio(token)

    async def test_H02_login_recusado_uniforme(self) -> None:
        """H02 compara senha errada, conta inexistente e conta excluída.

        Envia JSON real e fotografa o estado a cada variante para provar a
        mesma falha 401 sem Set-Cookie e sem inserir novas sessões.
        """
        for variante, email, senha in (
            ("senha-incorreta", "a@example.test", "Senha-Errada-123"),
            ("conta-inexistente", "ausente@example.test", SENHA_SINTETICA),
            ("conta-excluida", "a@example.test", SENHA_SINTETICA),
        ):
            with self.subTest(operacao=f"login {variante}", identidade="A/ausente"):
                if variante == "conta-excluida":
                    await self.banco.marcar_conta_excluida(USUARIO_A)
                antes = await self.banco.snapshot()
                resposta = await self.banco.requisitar("POST", "/acessos", dados={"email": email, "senha": senha})
                self.assertEqual(resposta.status, 401)
                self.assertTrue(resposta.json() == {"detail": "E-mail ou senha não conferem."}, "Login não uniforme [REDACTED]")
                self.assertFalse(bool(resposta.cabecalhos("set-cookie")))
                await self._assert_intacto(antes)

    async def test_H03_formatos_de_login(self) -> None:
        """H03 distingue limites do DTO e validação estrutural do domínio.

        Envia quatro variantes HTTP e confere 422 ou 401 conforme contrato,
        com snapshot intacto e nenhum cookie, sem imprimir senha inválida.
        """
        for variante, dados, status in (
            ("senha-ausente", {"email": "a@example.test"}, 422),
            ("senha-curta", {"email": "a@example.test", "senha": "x" * 7}, 422),
            ("senha-longa", {"email": "a@example.test", "senha": "x" * 1025}, 422),
            ("email-estrutural", {"email": "abc", "senha": SENHA_SINTETICA}, 401),
        ):
            with self.subTest(operacao=f"login {variante}", identidade="A/entrada-invalida"):
                antes = await self.banco.snapshot()
                resposta = await self.banco.requisitar("POST", "/acessos", dados=dados)
                self.assertEqual(resposta.status, status)
                if status == 401:
                    self.assertTrue(resposta.json() == {"detail": "E-mail ou senha não conferem."})
                self.assertFalse(bool(resposta.cabecalhos("set-cookie")))
                await self._assert_intacto(antes)

    async def test_H04_uso_proprio_sem_prolongar_sessao(self) -> None:
        """H04 consulta A em T e T+1h usando cookie emitido pelo login real.

        Verifica proxy e DTO público e compara todas as colunas persistidas
        para provar identidade própria e ausência de renovação por atividade.
        """
        token = await self._login()
        antes = await self.banco.snapshot()
        for horas in (0, 1):
            with self.subTest(operacao=f"consulta T+{horas}h", identidade="A"):
                await self._consultar_proprio(token, instante=INSTANTE_T + timedelta(hours=horas))
                await self._assert_intacto(antes)

    async def test_H05_somente_cookie_autentica(self) -> None:
        """H05 rejeita token em Authorization, query, corpo ou ausente.

        Tenta PUT válido com sessão existente fora do cookie e comprova 401,
        proxy zero e snapshot intacto para isolar o transporte de credenciais.
        """
        token = await self._login()
        for variante, opcoes in (
            ("authorization", {"cabecalhos": {"authorization": f"Bearer {token}"}}),
            ("query", {"query": urlencode({"token": token})}),
            ("corpo", {"dados": {"nome": "Pessoa Editada", "email": "editado@example.test", "token": token}}),
            ("ausente", {}),
        ):
            with self.subTest(operacao=f"PUT transporte {variante}", identidade="A"):
                antes = await self.banco.snapshot()
                argumentos = {"dados": {"nome": "Pessoa Editada", "email": "editado@example.test"}, **opcoes}
                resposta = await self.banco.requisitar("PUT", f"/estudantes/{USUARIO_A}", **argumentos)
                self._assert_401(resposta)
                await self._assert_intacto(antes)

    async def test_H06_cookie_desconhecido_e_malformado_caracterizado(self) -> None:
        """H06 caracteriza valores desconhecidos sem inventar gramática de token.

        Envia URL-safe desconhecido, vazio e não Base64 aceitos pelo parser real,
        conferindo 401 e ausência de mutação sem exigir erro sintático próprio.
        """
        for variante, token in (("desconhecido", token_sintetico(900)), ("vazio", ""), ("nao-base64", "nao-base64!")):
            with self.subTest(operacao=f"PUT cookie {variante}", identidade="sem-registro"):
                antes = await self.banco.snapshot()
                self.assertFalse(any(linha.token_hash == resumo_token(token) for linha in antes["sessoes"]))
                resposta = await self.banco.requisitar(
                    "PUT", f"/estudantes/{USUARIO_A}", token=token,
                    dados={"nome": "Pessoa Editada", "email": "editado@example.test"},
                )
                self.assertTrue(resposta.cookie_reconhecido, "Parser não reconheceu o cookie de caracterização [REDACTED]")
                self._assert_401(resposta)
                await self._assert_intacto(antes)

    async def test_H07_sessao_expirada_ou_revogada(self) -> None:
        """H07 rejeita estados expirado e revogado persistidos no banco.

        Usa registros reais com datas T−1s em PUT válido e comprova resposta
        uniforme, proxies zero e estado intacto para validar os filtros reais.
        """
        for indice, variante, campos in (
            (201, "expirada", {"expira_em": INSTANTE_T - timedelta(seconds=1)}),
            (202, "revogada", {"revogada_em": INSTANTE_T - timedelta(seconds=1)}),
        ):
            with self.subTest(operacao=f"PUT sessão {variante}", identidade="A"):
                token = await self.banco.semear_sessao(indice, USUARIO_A, **campos)
                antes = await self.banco.snapshot()
                resposta = await self.banco.requisitar(
                    "PUT", f"/estudantes/{USUARIO_A}", token=token,
                    dados={"nome": "Pessoa Editada", "email": "editado@example.test"},
                )
                self._assert_401(resposta)
                await self._assert_intacto(antes)

    async def test_H08_conta_excluida_invalida_todas_sessoes(self) -> None:
        """H08 invalida A1/A2 pela exclusão da conta e preserva B1.

        Atualiza deleted_at diretamente pela fixture e reabre apps para provar
        a rejeição por JOIN, sem exigir revogação física das linhas de sessão.
        """
        a1, a2, b1 = await self._trio()
        await self.banco.marcar_conta_excluida(USUARIO_A)
        antes = await self.banco.snapshot()
        for identidade, token in (("A1", a1), ("A2", a2)):
            with self.subTest(operacao="GET após exclusão", identidade=identidade):
                resposta = await self.banco.requisitar("GET", f"/estudantes/{USUARIO_A}", token=token)
                self._assert_401(resposta)
                await self._assert_intacto(antes)
        await self._consultar_proprio(b1, "B")
        await self._assert_intacto(antes)

    async def test_H09_isolamento_de_identidade(self) -> None:
        """H09 nega PUT alheio mesmo com proprietário declarado pelo cliente.

        Envia cookie A para editar B, confere 403 e proxy zero e consulta A
        como controle, sem transpor para GET alheio o status da rota de edição.
        """
        token = await self._login()
        antes = await self.banco.snapshot()
        with self.subTest(operacao="PUT recurso de B", identidade="A"):
            resposta = await self.banco.requisitar(
                "PUT", f"/estudantes/{USUARIO_B}", token=token,
                query=urlencode({"usuario_id": str(USUARIO_B)}),
                dados={"nome": "Pessoa Editada", "email": "editado@example.test", "usuario_id": str(USUARIO_B)},
            )
            self.assertEqual(resposta.status, 403)
            self.assertTrue(resposta.json() == {"detail": "A sessão não pode acessar este recurso."})
            self.assertEqual(resposta.edicoes, ())
            self.assertEqual(resposta.consultas, ())
            await self._assert_intacto(antes)
        await self._consultar_proprio(token)
        await self._assert_intacto(antes)

    async def test_H10_dependencias_ausentes(self) -> None:
        """H10 distingue serviços não compostos de falhas de banco não definidas.

        Omite portas selecionadas mantendo autenticador real e verifica 503
        sem cookie, além do logout sem cookie que continua removendo o cookie.
        """
        for ausentes, detalhe in (
            (frozenset({"acesso"}), "Acesso indisponível."),
            (frozenset({"criador"}), "Sessões indisponíveis."),
            (frozenset({"acesso", "criador"}), "Acesso indisponível."),
        ):
            with self.subTest(operacao="login sem " + "/".join(sorted(ausentes)), identidade="A"):
                antes = await self.banco.snapshot()
                resposta = await self.banco.requisitar(
                    "POST", "/acessos", ausentes=ausentes,
                    dados={"email": "a@example.test", "senha": SENHA_SINTETICA},
                )
                self.assertEqual(resposta.status, 503)
                self.assertTrue(resposta.json() == {"detail": detalhe})
                self.assertFalse(bool(resposta.cabecalhos("set-cookie")))
                await self._assert_intacto(antes)
        for presente in (True, False):
            with self.subTest(operacao="logout sem revogador", identidade="B" if presente else "sem-cookie"):
                antes = await self.banco.snapshot()
                resposta = await self.banco.requisitar(
                    "DELETE", "/sessao/atual", ausentes=frozenset({"revogador"}),
                    token=self.token_controle if presente else None,
                )
                self.assertEqual(resposta.status, 503 if presente else 204)
                if presente:
                    self.assertTrue(resposta.json() == {"detail": "Sessões indisponíveis."})
                    self.assertFalse(bool(resposta.cabecalhos("set-cookie")))
                else:
                    self.assertTrue(resposta.corpo == b"")
                    self._assert_cookie(resposta, removido=True)
                await self._assert_intacto(antes)

    async def test_R01_logout_revoga_somente_sessao_atual(self) -> None:
        """R01 revoga A1 e preserva A2/B1 com leitura real após commit.

        Compara todas as linhas para exigir uma única alteração e testa reuso
        negado mais sessões válidas por HTTP para provar o escopo do logout.
        """
        a1, a2, b1 = await self._trio()
        antes = await self.banco.snapshot()
        await self._logout(a1, "A1")
        with self.subTest(operacao="releitura após logout", identidade="A1/A2/B1"):
            depois = await self.banco.snapshot()
            self.assertEqual(len(antes["sessoes"]), len(depois["sessoes"]))
            self.assertEqual(sum(a != b for a, b in zip(antes["sessoes"], depois["sessoes"], strict=True)), 1)
            self.assertTrue(antes["usuarios"] == depois["usuarios"])
            for anterior, posterior in zip(antes["sessoes"], depois["sessoes"], strict=True):
                if anterior.token_hash == resumo_token(a1):
                    self.assertIsNone(anterior.revogada_em)
                    # SQLite retirou tzinfo do UTC gravado; só o assert normaliza.
                    self.assertEqual(posterior.revogada_em.replace(tzinfo=timezone.utc), INSTANTE_T)
                    self.assertTrue(tuple(anterior)[:-1] == tuple(posterior)[:-1])
                else:
                    self.assertTrue(anterior == posterior, "Outra sessão alterada [REDACTED]")
        with self.subTest(operacao="GET reuso após logout", identidade="A1"):
            self._assert_401(await self.banco.requisitar("GET", f"/estudantes/{USUARIO_A}", token=a1))
        await self._consultar_proprio(a2)
        await self._consultar_proprio(b1, "B")
        await self._assert_intacto(depois)

    async def test_R02_repeticao_preserva_primeira_revogacao(self) -> None:
        """R02 repete logout em T+1min sem reescrever a primeira revogação.

        Confere a data inicial após o primeiro DELETE e exige snapshot idêntico
        após o segundo, além de controles A2/B1 válidos em aplicações novas.
        """
        a1, a2, b1 = await self._trio()
        await self._logout(a1, "A1")
        antes = await self.banco.snapshot()
        with self.subTest(operacao="data inicial", identidade="A1"):
            linha = next(linha for linha in antes["sessoes"] if linha.token_hash == resumo_token(a1))
            # UTC conhecido da fixture; normalização exclusiva da asserção SQLite.
            self.assertEqual(linha.revogada_em.replace(tzinfo=timezone.utc), INSTANTE_T)
        await self._logout(a1, "A1-repetida", INSTANTE_T + timedelta(minutes=1))
        await self._assert_intacto(antes)
        await self._consultar_proprio(a2)
        await self._consultar_proprio(b1, "B")
        await self._assert_intacto(antes)

    async def test_R03_logout_sem_sessao_ativa(self) -> None:
        """R03 encerra ausente, desconhecida, expirada e revogada com 204.

        Relê o banco por variante e permite mudança só na expirada apresentada,
        caracterizando o UPDATE sem tornar sua data uma nova exigência pública.
        """
        a2 = await self.banco.semear_sessao(301, USUARIO_A)
        expirada = await self.banco.semear_sessao(302, USUARIO_A, expira_em=INSTANTE_T - timedelta(seconds=1))
        revogada = await self.banco.semear_sessao(303, USUARIO_A, revogada_em=INSTANTE_T - timedelta(seconds=1))
        for identidade, token in (
            ("sem-cookie", None), ("desconhecida", token_sintetico(901)),
            ("expirada", expirada), ("revogada", revogada),
        ):
            with self.subTest(operacao="logout sem sessão ativa", identidade=identidade):
                antes = await self.banco.snapshot()
                await self._logout(token, identidade)
                depois = await self.banco.snapshot()
                self.assertEqual(len(antes["sessoes"]), len(depois["sessoes"]))
                self.assertTrue(antes["usuarios"] == depois["usuarios"])
                for anterior, posterior in zip(antes["sessoes"], depois["sessoes"], strict=True):
                    if identidade == "expirada" and anterior.token_hash == resumo_token(expirada):
                        self.assertTrue(tuple(anterior)[:-1] == tuple(posterior)[:-1])
                    else:
                        self.assertTrue(anterior == posterior, "Sessão não apresentada alterada [REDACTED]")
                await self._consultar_proprio(a2)
                await self._consultar_proprio(self.token_controle, "B")
                await self._assert_intacto(depois)
