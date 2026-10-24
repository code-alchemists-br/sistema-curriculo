"""Integra o ciclo autorizado do perfil com HTTP real e SQLite migrado.

Percorre cadastro, login, consulta, edições e exclusão com releituras em sessões
novas e controles positivos para provar o fluxo e as recusas implementadas.
Os critérios são inferidos do título; o card não tem aceite oficial fornecido.

Não certifica backend.main:app operacional, transação de produção ou entrega de
cookie sob falha de banco, PostgreSQL, rede, TLS, navegador, RBAC, concorrência,
desempenho, retenção ou eliminação física. HTTPS ASGI sintético não prova o
comportamento do cookie em navegador; o commit pertence somente ao harness.
"""

# Proveniência: decision-analysis prompts/backend/20261024-105607-cenario-integracao-ciclo-vida-perfil-autorizado-v001.md#v001

import base64
import unittest
from datetime import timedelta, timezone
from uuid import UUID

from backend.infrastructure.security.senhas import DerivadorSenhaScrypt
from backend.tests.fixtures.ciclo_vida_perfil_autorizado import (
    CADASTRO_A,
    CADASTRO_B,
    CADASTRO_C,
    EDICAO_A,
    OPERACOES_PERFIL,
    PERFIL_COMPLETO_A,
    SENHA,
    BancoCicloVidaPerfilAutorizado,
)
from backend.tests.fixtures.credenciais_sessao import (
    AIOSQLITE_DISPONIVEL,
    COLUNAS_SESSAO,
    MOTIVO_SEM_AIOSQLITE,
    resumo_token,
)


@unittest.skipUnless(AIOSQLITE_DISPONIVEL, MOTIVO_SEM_AIOSQLITE)
class CicloVidaPerfilAutorizadoIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica jornada e caracterização isoladas com componentes reais.

    Usa banco novo por método e assertions fail-fast, sem mocks de negócio,
    para distinguir integração aprovada de preparação ignorada por ambiente.
    """

    async def asyncSetUp(self) -> None:
        """Prepara o banco vazio e registra cleanup antes de qualquer migration.

        Confere head, colunas e FK após Alembic para que cada método parta de
        schema migrado isolado e libere recursos mesmo quando o preparo falha.
        """
        self.banco = BancoCicloVidaPerfilAutorizado()
        self.addAsyncCleanup(self.banco.fechar)
        self.segredos = [SENHA]
        await self.banco.preparar()
        schema = await self.banco.inspecionar_schema()
        self.assertEqual(schema["versoes"], (self.banco.head,))
        self.assertEqual({coluna["name"] for coluna in schema["colunas"]}, set(COLUNAS_SESSAO))
        self.assertEqual(schema["usuarios"], {
            "id", "nome", "email", "hash_senha", "deleted_at", "endereco",
            "cidade", "telefones", "linkedin", "curriculo_lattes",
        })
        self.assertEqual(schema["fk_ativa"], 1)
        vazio = await self.banco.snapshot()
        self.assertTrue(vazio == {"usuarios": (), "sessoes": ()}, "Seed inesperado [REDACTED]")

    def _dto(self, resposta, esperado: dict) -> None:
        """Compara a resposta pública sem expor conteúdo quando houver diferença.

        Exige igualdade exata de DTO e verifica segredos conhecidos somente no
        corpo para impedir vazamento de hash, senha ou token nos diagnósticos.
        """
        self.assertTrue(resposta.json() == esperado, "DTO público divergente [REDACTED]")
        self.assertTrue(
            all(segredo.encode() not in resposta.corpo for segredo in self.segredos),
            "Segredo exposto no corpo [REDACTED]",
        )

    def _chamadas(self, operacao: str | None = None, usuario_id: UUID | None = None) -> None:
        """Confere execução ou bloqueio de todos os casos de perfil observados.

        Compara históricos delegantes com uma única operação esperada para
        provar a origem da identidade e ausência de chamadas nas recusas.
        """
        esperado = {
            nome: (usuario_id,) if nome == operacao else ()
            for nome in OPERACOES_PERFIL
        }
        self.assertTrue(self.banco.chamadas_perfil == esperado, "Chamadas divergentes [REDACTED]")

    def _cookie(self, resposta, *, removido: bool = False) -> str:
        """Valida atributos contratuais do cookie sem imprimir seu segredo.

        Analisa Set-Cookie com o parser compartilhado e compara atributos por
        booleanos para verificar emissão ou expiração pelo contrato atual.
        """
        cookie = resposta.cookie_sessao()
        for atributo, esperado in {
            "path": "/", "max-age": "0" if removido else "28800",
            "secure": True, "httponly": True, "samesite": "lax", "domain": "",
        }.items():
            atual = cookie[atributo]
            if atributo == "samesite":
                atual = atual.lower()
            self.assertTrue(atual == esperado, f"Atributo {atributo} divergente [REDACTED]")
        if removido:
            self.assertTrue(cookie.value == "", "Cookie não expirado [REDACTED]")
        return cookie.value

    async def _cadastrar(self, dados: dict) -> UUID:
        """Cria uma conta por HTTP e confere seus dados em sessão independente.

        Captura o UUID público, verifica scrypt real e ausência de sessão/cookie
        para provar cadastro persistente sem autenticação ou seed implícitos.
        """
        antes = await self.banco.snapshot()
        resposta = await self.banco.requisitar("POST", "/estudantes", dados=dados)
        self.assertEqual(resposta.status, 201)
        corpo = resposta.json()
        self.assertTrue(set(corpo) == {"id", "nome", "email"}, "Campos de cadastro [REDACTED]")
        try:
            usuario_id = UUID(corpo["id"])
        except (ValueError, TypeError, AttributeError):
            self.fail("Cadastro não retornou UUID válido [REDACTED]")
        usuario = await self.banco.ler_usuario(usuario_id)
        self.segredos.append(usuario["hash_senha"])
        self._dto(resposta, {"id": str(usuario_id), "nome": dados["nome"], "email": dados["email"]})
        self._chamadas()
        self.assertFalse(bool(resposta.cabecalhos("set-cookie")), "Cadastro emitiu cookie [REDACTED]")
        self.assertTrue(
            usuario["id"] == usuario_id and usuario["nome"] == dados["nome"]
            and usuario["email"] == dados["email"], "Conta persistida divergente [REDACTED]",
        )
        self.assertTrue(usuario["hash_senha"].startswith("scrypt$"), "Hash não scrypt [REDACTED]")
        self.assertTrue(usuario["hash_senha"] != dados["senha"], "Senha em claro [REDACTED]")
        self.assertTrue(
            DerivadorSenhaScrypt().confere(dados["senha"], usuario["hash_senha"]),
            "Hash não verifica a senha [REDACTED]",
        )
        self.assertTrue(all(usuario[campo] is None for campo in (
            "deleted_at", "endereco", "cidade", "telefones", "linkedin", "curriculo_lattes",
        )), "Estado inicial divergente [REDACTED]")
        self.assertTrue(not await self.banco.ler_sessoes(usuario_id), "Login implícito [REDACTED]")
        depois = await self.banco.snapshot()
        self.assertEqual(len(depois["usuarios"]), len(antes["usuarios"]) + 1)
        self.assertTrue(depois["sessoes"] == antes["sessoes"], "Sessões alteradas [REDACTED]")
        return usuario_id

    async def _login(self, usuario_id: UUID, email: str) -> str:
        """Obtém sessão por login real e verifica o registro durável correspondente.

        Confere cookie, SHA-256, identidade e validade em outra sessão para
        provar que o token retornado representa uma nova sessão persistida.
        """
        antes = await self.banco.snapshot()
        resposta = await self.banco.requisitar(
            "POST", "/acessos", dados={"email": email, "senha": SENHA},
        )
        self.assertEqual(resposta.status, 204)
        self.assertTrue(resposta.corpo == b"", "Login devolveu corpo [REDACTED]")
        self._chamadas()
        token = self._cookie(resposta)
        self.assertTrue(len(token) == 43, "Token opaco divergente [REDACTED]")
        try:
            decodificado = base64.b64decode(token + "=", altchars=b"-_", validate=True)
        except ValueError:
            self.fail("Token opaco inválido [REDACTED]")
        self.assertTrue(len(decodificado) == 32, "Entropia do token divergente [REDACTED]")
        self.segredos.extend((token, resumo_token(token)))
        depois = await self.banco.snapshot()
        self.assertTrue(depois["usuarios"] == antes["usuarios"], "Login alterou contas [REDACTED]")
        self.assertEqual(len(depois["sessoes"]), len(antes["sessoes"]) + 1)
        self.assertTrue(all(linha in depois["sessoes"] for linha in antes["sessoes"]),
                        "Login alterou sessão existente [REDACTED]")
        linhas = await self.banco.ler_sessoes(usuario_id)
        emitidas = [linha for linha in linhas if linha["token_hash"] == resumo_token(token)]
        self.assertEqual(len(emitidas), 1)
        linha = emitidas[0]
        self.assertTrue(linha["usuario_id"] == usuario_id, "Dono da sessão divergente [REDACTED]")
        self.assertTrue(linha["revogada_em"] is None, "Sessão já revogada [REDACTED]")
        self.assertTrue(linha["expira_em"] - linha["criada_em"] == timedelta(hours=8),
                        "Validade da sessão divergente [REDACTED]")
        self.assertTrue(linha["expira_em"].replace(tzinfo=timezone.utc) >
                        linha["criada_em"].replace(tzinfo=timezone.utc),
                        "Datas da sessão inválidas [REDACTED]")
        self.assertTrue(token not in repr(depois), "Token em claro no banco [REDACTED]")
        return token

    async def _consultar(self, usuario_id: UUID, token: str, esperado: dict) -> None:
        """Lê o próprio perfil por cookie e exige projeção pública exata.

        Verifica o observador e snapshots novos antes/depois para provar que a
        rota funcional lê a identidade correta sem escrever estado ou cookie.
        """
        antes = await self.banco.snapshot()
        resposta = await self.banco.requisitar("GET", f"/estudantes/{usuario_id}", token=token)
        self.assertEqual(resposta.status, 200)
        self._dto(resposta, esperado)
        self._chamadas("consulta", usuario_id)
        self.assertTrue(resposta.cookie_reconhecido, "Cookie não chegou ao scope [REDACTED]")
        self.assertFalse(bool(resposta.cabecalhos("set-cookie")), "Consulta emitiu cookie [REDACTED]")
        self.assertTrue(antes == await self.banco.snapshot(), "Consulta alterou estado [REDACTED]")

    async def _recusar(
        self, metodo: str, caminho: str, *, dados: dict | None = None,
        token: str | None = None, status: int = 401,
        detalhe: str = "Sessão ausente ou inválida.",
    ) -> None:
        """Verifica recusa uniforme com estado intacto e nenhum caso de perfil.

        Envia entrada válida e compara snapshots externos antes do controle
        positivo para isolar a regra de acesso de falhas gerais da rota.
        """
        antes = await self.banco.snapshot()
        resposta = await self.banco.requisitar(metodo, caminho, dados=dados, token=token)
        self.assertEqual(resposta.status, status)
        self._dto(resposta, {"detail": detalhe})
        self._chamadas()
        self.assertFalse(bool(resposta.cabecalhos("set-cookie")), "Recusa emitiu cookie [REDACTED]")
        if token is not None:
            self.assertTrue(resposta.cookie_reconhecido, "Token não foi transportado [REDACTED]")
        self.assertTrue(antes == await self.banco.snapshot(), "Recusa alterou estado [REDACTED]")

    async def _editar(self, usuario_id: UUID, token: str, dados: dict, *, completo=False) -> None:
        """Edita o perfil pela rota escolhida e confere todas as colunas duráveis.

        Compara linha relida com o estado anterior atualizado só nos campos do
        payload para demonstrar efeito persistido e preservação de ID e hash.
        """
        antes = await self.banco.ler_usuario(usuario_id)
        sessoes_antes = (await self.banco.snapshot())["sessoes"]
        caminho = "/estudantes/me/perfil" if completo else f"/estudantes/{usuario_id}"
        resposta = await self.banco.requisitar("PUT", caminho, token=token, dados=dados)
        self.assertEqual(resposta.status, 200)
        self._dto(resposta, {"id": str(usuario_id), **dados})
        self._chamadas("completo" if completo else "edicao", usuario_id)
        self.assertFalse(bool(resposta.cabecalhos("set-cookie")), "Edição emitiu cookie [REDACTED]")
        esperado = {**antes, **dados}
        self.assertTrue(await self.banco.ler_usuario(usuario_id) == esperado,
                        "Edição persistida divergente [REDACTED]")
        self.assertTrue((await self.banco.snapshot())["sessoes"] == sessoes_antes,
                        "Edição alterou sessões [REDACTED]")

    async def _excluir(self, usuario_id: UUID, token: str) -> dict:
        """Exclui o perfil da sessão e confirma soft delete sem efeitos laterais.

        Verifica 204, cookie expirado e primeira marca persistida, comparando
        demais contas e sessões para provar exclusão própria sem purga física.
        """
        antes = await self.banco.snapshot()
        usuario_antes = await self.banco.ler_usuario(usuario_id)
        resposta = await self.banco.requisitar("DELETE", "/estudantes/atual", token=token)
        self.assertEqual(resposta.status, 204)
        self.assertTrue(resposta.corpo == b"", "Exclusão devolveu corpo [REDACTED]")
        self._cookie(resposta, removido=True)
        self._chamadas("exclusao", usuario_id)
        excluido = await self.banco.ler_usuario(usuario_id)
        self.assertTrue(excluido["deleted_at"] is not None, "Soft delete ausente [REDACTED]")
        self.assertTrue(excluido == {**usuario_antes, "deleted_at": excluido["deleted_at"]},
                        "Exclusão alterou outros campos [REDACTED]")
        depois = await self.banco.snapshot()
        self.assertTrue(antes["sessoes"] == depois["sessoes"], "Sessões apagadas/alteradas [REDACTED]")
        self.assertTrue(
            tuple(linha for linha in antes["usuarios"] if linha.id != usuario_id) ==
            tuple(linha for linha in depois["usuarios"] if linha.id != usuario_id),
            "Exclusão alterou outra conta [REDACTED]",
        )
        return excluido

    async def test_cadastro_consulta_edicao_exclusao_do_proprio_perfil_com_sessao_valida(self) -> None:
        """Percorre E0–E7 de forma encadeada, com controles reais por operação.

        Usa identidades capturadas, três logins de A e releituras após cada
        transição para demonstrar persistência e bloqueio após exclusão própria.
        """
        # E0: banco migrado em asyncSetUp; conta e sessão de controle por HTTP.
        b = await self._cadastrar(CADASTRO_B)
        b1 = await self._login(b, CADASTRO_B["email"])
        pessoal_b = dados_consulta(CADASTRO_B)
        await self._consultar(b, b1, pessoal_b)
        b_original = await self.banco.ler_usuario(b)

        # E1–E2: cadastro não autentica; ambos os tokens funcionam antes do DELETE.
        a = await self._cadastrar(CADASTRO_A)
        pessoal_a = dados_consulta(CADASTRO_A)
        a1 = await self._login(a, CADASTRO_A["email"])
        a2 = await self._login(a, CADASTRO_A["email"])
        self.assertTrue(a1 != a2, "Tokens distintos esperados [REDACTED]")
        linhas_a = await self.banco.ler_sessoes(a)
        self.assertEqual(len(linhas_a), 2)
        self.assertEqual(len({linha["token_hash"] for linha in linhas_a}), 2)
        for token in (a1, a2):
            await self._consultar(a, token, pessoal_a)

        # E3: recusa sem sessão, seguida de controle da mesma rota.
        await self._consultar(a, a1, pessoal_a)
        await self._recusar("GET", f"/estudantes/{a}")
        await self._consultar(a, a1, pessoal_a)

        # E4a: identidade persistida, hash preservado e login pelo email atual.
        await self._recusar("PUT", f"/estudantes/{a}", dados=EDICAO_A)
        await self._editar(a, a1, EDICAO_A)
        await self._consultar(a, a1, dados_consulta(EDICAO_A))
        a3 = await self._login(a, EDICAO_A["email"])
        await self._consultar(a, a3, dados_consulta(EDICAO_A))

        # E4b: contato durável; GET omite endereço e demais campos internos.
        await self._recusar("PUT", "/estudantes/me/perfil", dados=PERFIL_COMPLETO_A)
        await self._editar(a, a1, PERFIL_COMPLETO_A, completo=True)
        await self._consultar(a, a1, dados_consulta(PERFIL_COMPLETO_A))

        # E5: positivo da exclusão prova que a recusa anônima não é rota fechada.
        await self._recusar("DELETE", "/estudantes/atual")
        excluido_a = await self._excluir(a, a1)
        self.assertTrue(await self.banco.ler_usuario(b) == b_original,
                        "Conta de controle alterada [REDACTED]")
        self.assertEqual(len(await self.banco.ler_sessoes(a)), 3)

        # E6: reenviar segredos preservados em memória, sem depender do cookie jar.
        for token in (a1, a2, a3):
            await self._recusar("GET", f"/estudantes/{a}", token=token)
            await self._recusar("PUT", f"/estudantes/{a}", token=token, dados=EDICAO_A)
            await self._recusar("PUT", "/estudantes/me/perfil", token=token, dados=PERFIL_COMPLETO_A)
        await self._consultar(b, b1, pessoal_b)
        edicao_b = {"nome": "Pessoa B Editada", "email": CADASTRO_B["email"]}
        completo_b = {**PERFIL_COMPLETO_A, **edicao_b, "nome": "Pessoa B Completa"}
        await self._editar(b, b1, edicao_b)
        await self._editar(b, b1, completo_b, completo=True)
        await self._consultar(b, b1, dados_consulta(completo_b))

        # E7: recusa de login não cria sessão; B continua fazendo login e DELETE.
        await self._recusar(
            "POST", "/acessos", dados={"email": EDICAO_A["email"], "senha": SENHA},
            detalhe="E-mail ou senha não conferem.",
        )
        b2 = await self._login(b, CADASTRO_B["email"])
        for token in (a1, a2):
            await self._recusar("DELETE", "/estudantes/atual", token=token)
        self.assertTrue(await self.banco.ler_usuario(a) == excluido_a,
                        "Primeira exclusão não preservada [REDACTED]")
        await self._excluir(b, b2)
        self.assertTrue(await self.banco.ler_usuario(a) == excluido_a,
                        "Exclusão de B alterou A [REDACTED]")

    async def test_caracteriza_reserva_atual_do_email_de_conta_excluida(self) -> None:
        """Caracteriza E8 como comportamento atual, sem política definitiva (L05).

        Cria, autentica e exclui por HTTP, então compara recadastro recusado com
        cadastro novo permitido; pode ser revisado/removido sem afetar E0–E7.
        """
        a = await self._cadastrar(CADASTRO_A)
        token = await self._login(a, CADASTRO_A["email"])
        excluido = await self._excluir(a, token)
        await self._recusar(
            "POST", "/estudantes", dados=CADASTRO_A, status=409,
            detalhe="Já existe uma conta cadastrada com este e-mail.",
        )
        await self._cadastrar(CADASTRO_C)
        self.assertTrue(await self.banco.ler_usuario(a) == excluido,
                        "Caracterização reativou conta [REDACTED]")


def dados_consulta(dados: dict) -> dict:
    """Define os valores esperados na projeção pessoal a partir da massa do teste.

    Seleciona explicitamente nome, email e contatos públicos, com defaults do
    cadastro, para conferir GET exato sem depender do serializador produtivo.
    """
    return {
        "nome": dados["nome"], "email": dados["email"],
        "telefones": dados.get("telefones", []), "cidade": dados.get("cidade"),
        "linkedin": dados.get("linkedin"), "curriculo_lattes": dados.get("curriculo_lattes"),
    }
