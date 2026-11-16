"""Exercita cadastro de idiomas pela main real em PostgreSQL descartável.

Usa conta e sessão reais e consulta por uma engine independente para provar
commit, propriedade, recusa e recuperação sem alterar bancos preexistentes.
"""

import importlib
import os
import unittest
from http.cookies import SimpleCookie
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from backend.infrastructure.persistence.sqlalchemy.idioma import IdiomaRegistro
from backend.tests.fixtures.credenciais_sessao import solicitar_asgi
from backend.tests.test_integracao_cursos_certificacoes_postgresql import (
    url_postgresql_descartavel,
)


@unittest.skipUnless(
    os.environ.get("DATABASE_URL"),
    "Requer o PostgreSQL efêmero do executor de integração.",
)
class CadastroIdiomaPostgreSqlTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a aplicação composta e seus commits reais sem substituir executores."""

    async def asyncSetUp(self):
        """Exige cluster isolado e abre leitura independente para observar confirmação real."""
        url = url_postgresql_descartavel()
        self.leitura = create_async_engine(url, poolclass=NullPool)
        self.addAsyncCleanup(self.leitura.dispose)
        self.main = importlib.import_module("backend.main")
        self.addAsyncCleanup(self.main._engine_persistencia.dispose)
        self.app = self.main.app
        self.usuario, self.cookie = await self.criar_conta()

    async def criar_conta(self):
        """Cadastra e autentica massa sintética para exercitar propriedade sem fabricar sessão."""
        dados = {
            "nome": "Pessoa Idiomas",
            "email": f"idioma-{uuid4().hex}@example.test",
            "senha": "Senha-Teste-123",
        }
        cadastro = await solicitar_asgi(self.app, "POST", "/estudantes", dados=dados)
        self.assertEqual(cadastro.status, 201)
        acesso = await solicitar_asgi(
            self.app,
            "POST",
            "/acessos",
            dados={"email": dados["email"], "senha": dados["senha"]},
        )
        self.assertEqual(acesso.status, 204)
        cookies = SimpleCookie()
        for cabecalho in acesso.cabecalhos("set-cookie"):
            cookies.load(cabecalho)
        nome = self.main._configuracao_cookie_sessao.nome
        return UUID(cadastro.json()["id"]), f"{nome}={cookies[nome].value}"

    async def cadastrar(self, idioma="Inglês", nivel="basico", cookie=None, **extras):
        """Envia JSON pelo ASGI real com cookie explícito para observar respostas públicas."""
        return await solicitar_asgi(
            self.app,
            "POST",
            "/idiomas",
            dados={"idioma": idioma, "nivel": nivel, **extras},
            cabecalhos={"cookie": cookie} if cookie else None,
        )

    async def registros(self, usuario=None):
        """Relê por conexão externa para distinguir resposta de cadastro de commit durável."""
        async with self.leitura.connect() as conexao:
            resultado = await conexao.execute(
                select(IdiomaRegistro.__table__).where(
                    IdiomaRegistro.usuario_id == (usuario or self.usuario)
                )
            )
            return [dict(linha) for linha in resultado.mappings()]

    async def test_201_persiste_com_proprietario_da_sessao(self):
        """Cadastra com dono forjado no payload e relê o dono real para impedir falsificação de propriedade."""
        resposta = await self.cadastrar(cookie=self.cookie, usuario_id=str(uuid4()))
        self.assertEqual(resposta.status, 201)
        self.assertEqual(resposta.json()["usuario_id"], str(self.usuario))
        linhas = await self.registros()
        self.assertEqual(len(linhas), 1)
        self.assertEqual(linhas[0]["idioma"], "Inglês")
        self.assertEqual(linhas[0]["nivel"], "basico")
        self.assertEqual(linhas[0]["id"], UUID(resposta.json()["id"]))

    async def test_sem_cookie_nao_persiste(self):
        """Recusa HTTP anônimo e relê o banco para impedir mutação sem identidade autenticada."""
        resposta = await self.cadastrar()
        self.assertEqual(resposta.status, 401)
        self.assertEqual(await self.registros(), [])

    async def test_422_nao_grava_e_proxima_requisicao_recupera(self):
        """Rejeita nível vazio e cadastra depois para provar rollback e sessão curta reutilizável."""
        invalida = await self.cadastrar(nivel="", cookie=self.cookie)
        self.assertEqual(invalida.status, 422)
        self.assertEqual(await self.registros(), [])
        valida = await self.cadastrar(cookie=self.cookie)
        self.assertEqual(valida.status, 201)
        self.assertEqual(len(await self.registros()), 1)

    async def test_409_preserva_confirmado_e_nao_bloqueia_outro_idioma(self):
        """Repete a chave e cadastra outra para observar conflito sem duplicação ou transação presa."""
        self.assertEqual((await self.cadastrar(cookie=self.cookie)).status, 201)
        self.assertEqual(
            (await self.cadastrar(idioma=" INGLÊS ", cookie=self.cookie)).status, 409
        )
        self.assertEqual(
            (await self.cadastrar(idioma="Espanhol", cookie=self.cookie)).status, 201
        )
        self.assertEqual(len(await self.registros()), 2)

    async def test_mesmo_idioma_permitido_a_outro_proprietario(self):
        """Cadastra a mesma língua em duas sessões e relê cada dono para proteger isolamento de conta."""
        outro_usuario, outro_cookie = await self.criar_conta()
        self.assertEqual((await self.cadastrar(cookie=self.cookie)).status, 201)
        self.assertEqual((await self.cadastrar(cookie=outro_cookie)).status, 201)
        self.assertEqual(len(await self.registros()), 1)
        self.assertEqual(len(await self.registros(outro_usuario)), 1)
