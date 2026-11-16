"""Exercita a leitura e a substituição do currículo completo em PostgreSQL descartável.

Usa a ``main`` real com conta e sessão reais e relê o banco por uma engine
independente para provar que salvar de novo uma seção substitui os itens (sem
duplicar), que falhas desfazem tudo e que o modelo escolhido é persistido.
"""

import importlib
import os
import unittest
from http.cookies import SimpleCookie
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from backend.infrastructure.persistence.sqlalchemy.curriculo import CurriculoRegistro
from backend.infrastructure.persistence.sqlalchemy.experiencia_profissional import (
    ExperienciaProfissionalRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.idioma import IdiomaRegistro
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro
from backend.tests.fixtures.credenciais_sessao import solicitar_asgi
from backend.tests.test_integracao_cursos_certificacoes_postgresql import (
    url_postgresql_descartavel,
)

BASE = "/estudantes/me/curriculo"
EXPERIENCIA = {
    "empresa": "Empresa X",
    "cargo": "Estagiária",
    "descricao": "Desenvolvi telas em React e APIs em Python.",
    "data_inicio": "2024-03-01",
    "data_fim": "2024-12-01",
}


@unittest.skipUnless(
    os.environ.get("DATABASE_URL"),
    "Requer o PostgreSQL efêmero do executor de integração.",
)
class CurriculoCompletoPostgreSqlTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica as rotas do currículo completo com commits reais no PostgreSQL.

    Cada teste cria uma conta nova e observa o banco por fora da aplicação.
    Existe para provar no dialeto real a substituição atômica das seções.
    """

    async def asyncSetUp(self):
        """Abre a leitura independente, carrega a aplicação real e cria uma conta.

        Existe para que cada teste comece com um estudante autenticado e sem itens.
        """
        url = url_postgresql_descartavel()
        self.leitura = create_async_engine(url, poolclass=NullPool)
        self.addAsyncCleanup(self.leitura.dispose)
        self.main = importlib.import_module("backend.main")
        self.addAsyncCleanup(self.main._engine_persistencia.dispose)
        self.app = self.main.app
        self.usuario, self.cookie = await self.criar_conta()

    async def criar_conta(self):
        """Cadastra e autentica uma conta sintética e devolve seu id e cookie.

        Existe para exercitar a propriedade dos dados com sessão real.
        """
        dados = {
            "nome": "Pessoa Currículo",
            "email": f"curriculo-{uuid4().hex}@example.test",
            "senha": "Senha-Teste-123",
        }
        cadastro = await solicitar_asgi(self.app, "POST", "/estudantes", dados=dados)
        self.assertEqual(cadastro.status, 201)
        acesso = await solicitar_asgi(
            self.app, "POST", "/acessos", dados={"email": dados["email"], "senha": dados["senha"]}
        )
        self.assertEqual(acesso.status, 204)
        cookies = SimpleCookie()
        for cabecalho in acesso.cabecalhos("set-cookie"):
            cookies.load(cabecalho)
        nome = self.main._configuracao_cookie_sessao.nome
        return UUID(cadastro.json()["id"]), f"{nome}={cookies[nome].value}"

    async def requisitar(self, metodo, caminho, dados=None, cookie=None):
        """Envia a requisição pelo ASGI real com o cookie do estudante.

        Existe para observar as respostas públicas das rotas.
        """
        return await solicitar_asgi(
            self.app, metodo, caminho, dados=dados, cabecalhos={"cookie": cookie or self.cookie}
        )

    async def linhas(self, tabela, usuario=None, somente_ativas=False):
        """Relê as linhas de uma tabela do estudante por conexão externa.

        Existe para distinguir a resposta HTTP do que de fato foi gravado.
        """
        consulta = select(tabela.__table__).where(tabela.usuario_id == (usuario or self.usuario))
        if somente_ativas:
            consulta = consulta.where(tabela.deleted_at.is_(None))
        async with self.leitura.connect() as conexao:
            return [dict(linha) for linha in (await conexao.execute(consulta)).mappings()]

    async def test_salvar_duas_vezes_substitui_sem_duplicar(self):
        """Salva a mesma seção duas vezes e encontra um único item ativo.

        Em tabelas com exclusão lógica, o item anterior fica marcado como
        excluído. Existe para provar o fim da duplicação ao revisitar etapas.
        """
        for _ in range(2):
            resposta = await self.requisitar("PUT", f"{BASE}/experiencias", {"itens": [EXPERIENCIA]})
            self.assertEqual(resposta.status, 204)

        ativas = await self.linhas(ExperienciaProfissionalRegistro, somente_ativas=True)
        todas = await self.linhas(ExperienciaProfissionalRegistro)
        self.assertEqual(len(ativas), 1)
        self.assertEqual(len(todas), 2)

        lido = (await self.requisitar("GET", BASE)).json()
        self.assertEqual([e["empresa"] for e in lido["experiencias"]], ["Empresa X"])

    async def test_repetidos_viram_409_e_preservam_o_que_estava_salvo(self):
        """Recusa idiomas repetidos sem apagar os idiomas já gravados.

        Existe para provar que a troca é atômica no PostgreSQL.
        """
        inicial = {"itens": [{"idioma": "Inglês", "nivel": "avancado"}]}
        self.assertEqual((await self.requisitar("PUT", f"{BASE}/idiomas", inicial)).status, 204)

        repetidos = {"itens": [{"idioma": "Espanhol", "nivel": "basico"}, {"idioma": " ESPANHOL ", "nivel": "basico"}]}
        self.assertEqual((await self.requisitar("PUT", f"{BASE}/idiomas", repetidos)).status, 409)

        self.assertEqual([linha["idioma"] for linha in await self.linhas(IdiomaRegistro)], ["Inglês"])

    async def test_lista_vazia_remove_a_secao(self):
        """Envia lista vazia e encontra a seção sem itens.

        Existe para que apagar tudo na tela também apague no banco.
        """
        await self.requisitar("PUT", f"{BASE}/idiomas", {"itens": [{"idioma": "Inglês", "nivel": "basico"}]})
        self.assertEqual((await self.requisitar("PUT", f"{BASE}/idiomas", {"itens": []})).status, 204)
        self.assertEqual(await self.linhas(IdiomaRegistro), [])

    async def test_formacoes_gravam_o_lattes_da_conta(self):
        """Grava o Lattes enviado junto com as formações na conta do estudante.

        Existe porque o Lattes é informado na etapa de formação.
        """
        formacao = {
            "instituicao": "Fatec",
            "curso": "ADS",
            "nivel": "tecnologo",
            "status": "em_andamento",
            "data_inicio": "2024-02-01",
        }
        corpo = {"itens": [formacao], "curriculo_lattes": "http://lattes.cnpq.br/123"}
        self.assertEqual((await self.requisitar("PUT", f"{BASE}/formacoes", corpo)).status, 204)

        async with self.leitura.connect() as conexao:
            lattes = await conexao.scalar(
                select(UsuarioRegistro.curriculo_lattes).where(UsuarioRegistro.id == self.usuario)
            )
        self.assertEqual(lattes, "http://lattes.cnpq.br/123")
        lido = (await self.requisitar("GET", BASE)).json()
        self.assertEqual(lido["formacoes"][0]["curso"], "ADS")
        self.assertEqual(lido["dados_pessoais"]["curriculo_lattes"], "http://lattes.cnpq.br/123")

    async def test_modelo_e_criado_uma_vez_e_depois_atualizado(self):
        """Cria o currículo principal na primeira escolha e só troca o modelo depois.

        Existe para que o modelo escolhido sobreviva entre sessões.
        """
        for modelo in ("moderno", "compacto"):
            resposta = await self.requisitar("PUT", f"{BASE}/modelo", {"modelo": modelo})
            self.assertEqual(resposta.status, 204)

        curriculos = await self.linhas(CurriculoRegistro)
        self.assertEqual([c["layout"] for c in curriculos], ["compacto"])
        self.assertEqual((await self.requisitar("GET", BASE)).json()["modelo"], "compacto")

    async def test_secoes_sao_isoladas_por_estudante(self):
        """Garante que um estudante não altera nem lê os itens de outro.

        Existe para proteger a propriedade dos dados entre contas.
        """
        outro_usuario, outro_cookie = await self.criar_conta()
        await self.requisitar("PUT", f"{BASE}/experiencias", {"itens": [EXPERIENCIA]})
        await self.requisitar("PUT", f"{BASE}/experiencias", {"itens": []}, cookie=outro_cookie)

        self.assertEqual(len(await self.linhas(ExperienciaProfissionalRegistro, somente_ativas=True)), 1)
        lido_outro = (await self.requisitar("GET", BASE, cookie=outro_cookie)).json()
        self.assertEqual(lido_outro["experiencias"], [])

    async def test_sem_sessao_responde_401(self):
        """Recusa leitura e gravação sem cookie de sessão.

        Existe para que o currículo só seja acessado pelo próprio dono.
        """
        for metodo, caminho, dados in (("GET", BASE, None), ("PUT", f"{BASE}/idiomas", {"itens": []})):
            with self.subTest(metodo=metodo):
                resposta = await solicitar_asgi(self.app, metodo, caminho, dados=dados)
                self.assertEqual(resposta.status, 401)


if __name__ == "__main__":
    unittest.main()
