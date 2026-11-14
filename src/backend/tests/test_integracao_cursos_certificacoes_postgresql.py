"""Valida os dois cadastros da main contra PostgreSQL migrado e descartável.

A suíte usa conta, login, middleware, executores e repositórios reais, com
leitura em engine independente. Barreiras e falhas locais ao teste exercitam
unicidade e rollback sem modificar o produto nem acessar bancos preexistentes.
Execute exclusivamente pelo executor executar-testes-integracao-postgresql.sh.
"""

# Proveniência: decision-analysis prompts/revisao/20261105-203823-auditoria-impacto-cursos-certificacoes-v002.md#v002

import asyncio
import importlib
import importlib.util
import os
import unittest
from http.cookies import SimpleCookie
from pathlib import Path
from unittest.mock import patch
from uuid import UUID, uuid4

from sqlalchemy import event, func, select, text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

from backend.infrastructure.persistence.sqlalchemy.certificacao import (
    CertificacaoRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.curso import CursoRegistro
from backend.infrastructure.persistence.sqlalchemy.repositorio_certificacao import (
    RepositorioCertificacaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_curso import (
    RepositorioCursoSqlAlchemy,
)
from backend.tests.fixtures.credenciais_sessao import solicitar_asgi


def url_postgresql_descartavel() -> str:
    """Exige a URL do cluster temporário do executor antes de abrir conexões.

    A função verifica driver, banco, ausência de host TCP e diretório exclusivo
    de socket criado pelo script. Ela existe para recusar execução acidental
    contra desenvolvimento, produção ou um banco herdado do terminal.
    """
    valor = os.environ.get("DATABASE_URL")
    if not valor:
        raise RuntimeError("Execute pelo executor PostgreSQL isolado do projeto.")
    url = make_url(valor)
    socket = Path(url.query.get("host", ""))
    if (
        url.drivername != "postgresql+psycopg"
        or url.database != "sistema_curriculo_test"
        or url.host is not None
        or not socket.is_absolute()
        or socket.name != "socket"
        or not socket.parent.name.startswith("sistema-curriculo-postgresql.")
        or not socket.is_dir()
        or not (socket.parent / "dados" / "PG_VERSION").is_file()
    ):
        raise RuntimeError("Alvo recusado: requer cluster descartável do executor.")
    return valor


class CenariosCadastroPostgreSql:
    """Compartilha oráculos de API e banco para os dois recursos existentes.

    O mixin parametriza tabela, campo emissor e repositório, mantendo as chamadas
    à main real. Ele existe para aplicar os mesmos critérios aos dois cadastros
    sem substituir executores, sessão autenticada ou dados persistidos.
    """

    async def asyncSetUp(self) -> None:
        """Prepara main real e duas contas sintéticas no cluster autorizado.

        O método valida a URL, cria engine de leitura sem pool e usa cadastro e
        login HTTP reais. Ele existe para isolar dados por cenário e observar
        commits por conexões distintas, sem controlar transações do produto.
        """
        url = url_postgresql_descartavel()
        self.leitura = create_async_engine(url, poolclass=NullPool)
        self.addAsyncCleanup(self.leitura.dispose)
        async with self.leitura.connect() as conexao:
            self.assertEqual(
                await conexao.scalar(text("SELECT current_database()")),
                "sistema_curriculo_test",
            )
        self.main = importlib.import_module("backend.main")
        self.assertIsNotNone(self.main._engine_persistencia)
        self.assertEqual(self.main._engine_persistencia.url, make_url(url))
        # Dispose no loop de cada cenário impede conexões presas a outro loop.
        self.addAsyncCleanup(self.main._engine_persistencia.dispose)
        self.app = self.main.app
        self.nome_cookie = self.main._configuracao_cookie_sessao.nome
        self.usuario_a, self.cookie_a = await self.criar_conta()
        self.usuario_b, self.cookie_b = await self.criar_conta()

    async def criar_conta(self) -> tuple[UUID, str]:
        """Obtém conta e cookie verdadeiros sem registrar credenciais.

        O helper envia massa sintética única aos endpoints de conta e acesso,
        extrai somente o cookie emitido e retorna identidade/cabeçalho em memória.
        Ele existe para testar autenticação sem fabricar request.state.
        """
        dados = {
            "nome": "Pessoa Integração",
            "email": f"cursos-{uuid4().hex}@example.test",
            "senha": "Senha-Teste-123",
        }
        cadastro = await solicitar_asgi(self.app, "POST", "/estudantes", dados=dados)
        self.assertEqual(cadastro.status, 201, "Pré-condição: cadastro real de conta")
        acesso = await solicitar_asgi(
            self.app, "POST", "/acessos",
            dados={"email": dados["email"], "senha": dados["senha"]},
        )
        self.assertEqual(acesso.status, 204, "Pré-condição: login real")
        cookies = SimpleCookie()
        for cabecalho in acesso.cabecalhos("set-cookie"):
            cookies.load(cabecalho)
        self.assertTrue(self.nome_cookie in cookies, "Cookie de sessão não emitido")
        token = cookies[self.nome_cookie].value
        return UUID(cadastro.json()["id"]), f"{self.nome_cookie}={token}"

    def dados(self, **alteracoes: object) -> dict:
        """Monta payload válido do recurso com substituições explícitas.

        O helper usa somente campos dos contratos existentes e aplica as
        alterações do cenário. Ele existe para manter inválidos e variações
        legíveis sem introduzir requisitos ou valores de domínio novos.
        """
        return {"nome": "  Formação  Ágil  ", self.campo: "  Instituto  Exemplo  ", **alteracoes}

    async def cadastrar(self, dados: dict, cookie: str | None = None):
        """Chama o POST real usando um cabeçalho de sessão opcional.

        O helper delega ao harness ASGI HTTPS existente, que redige segredos e
        aguarda resposta completa. Ele existe para observar transporte e banco
        sem mocks de executores ou alterações na política de autenticação.
        """
        return await solicitar_asgi(
            self.app, "POST", self.rota, dados=dados,
            cabecalhos={"cookie": cookie} if cookie is not None else None,
        )

    async def registros(self, usuario: UUID | None = None) -> list[dict]:
        """Relê linhas do cenário por conexão externa à gravação da aplicação.

        O método consulta a tabela pelo usuário sintético com engine NullPool,
        encerrando a conexão a cada chamada. Ele existe para provar confirmação
        real sem depender de sessão ORM original ou de endpoint de consulta.
        """
        consulta = select(self.modelo.__table__).where(
            self.modelo.usuario_id == (usuario or self.usuario_a)
        )
        async with self.leitura.connect() as conexao:
            return [dict(linha) for linha in (await conexao.execute(consulta)).mappings()]

    async def test_201_confirma_dados_em_outra_conexao(self) -> None:
        """Comprova cadastro autenticado e conteúdo confirmado no PostgreSQL.

        O cenário compara resposta pública e linha lida por engine independente,
        incluindo chaves normalizadas e horas. Ele existe para detectar sucesso
        HTTP sem commit ou mapeamento incorreto dos campos enviados.
        """
        resposta = await self.cadastrar(self.dados(), self.cookie_a)
        self.assertEqual(resposta.status, 201)
        publico = resposta.json()
        linhas = await self.registros()
        self.assertEqual(len(linhas), 1)
        linha = linhas[0]
        self.assertEqual(linha["id"], UUID(publico["id"]))
        self.assertEqual(linha["usuario_id"], self.usuario_a)
        self.assertEqual(publico["usuario_id"], str(self.usuario_a))
        for campo, exibido, chave in (
            ("nome", "Formação  Ágil", "formação ágil"),
            (self.campo, "Instituto  Exemplo", "instituto exemplo"),
        ):
            self.assertEqual(linha[campo], exibido)
            self.assertEqual(publico[campo], exibido)
            coluna_chave = "nome_normalizado" if campo == "nome" else f"{campo}_normalizada"
            self.assertEqual(linha[coluna_chave], chave)
        if self.modelo is CursoRegistro:
            self.assertIsNone(linha["carga_horaria"])
            self.assertIsNone(publico["carga_horaria"])

    async def test_sessao_ausente_nao_grava(self) -> None:
        """Recusa cadastro sem cookie e comprova ausência de escrita.

        O cenário envia o POST sem sessão e consulta o banco separadamente.
        Ele existe para verificar 401 no middleware real antes do cadastro.
        """
        resposta = await self.cadastrar(self.dados())
        self.assertEqual(resposta.status, 401)
        self.assertEqual(await self.registros(), [])

    async def test_sessao_invalida_nao_grava(self) -> None:
        """Recusa uma credencial sintética desconhecida e não persiste dados.

        O cenário usa cookie com nome correto e token não emitido, consultando
        ambos os donos depois. Ele existe para impedir que presença de cookie
        seja aceita como autenticação válida.
        """
        resposta = await self.cadastrar(self.dados(), f"{self.nome_cookie}={'x' * 43}")
        self.assertEqual(resposta.status, 401)
        self.assertEqual(await self.registros(), [])
        self.assertEqual(await self.registros(self.usuario_b), [])

    async def test_usuario_do_payload_nao_transfere_propriedade(self) -> None:
        """Vincula o cadastro à sessão apesar do dono diferente no JSON.

        O cenário envia usuario_id de B autenticado como A e verifica resposta
        e linhas dos dois donos. Ele existe para comprovar a fronteira de
        identidade contra tentativa de transferência pelo payload.
        """
        resposta = await self.cadastrar(
            self.dados(usuario_id=str(self.usuario_b)), self.cookie_a
        )
        self.assertEqual(resposta.status, 201)
        self.assertEqual(resposta.json()["usuario_id"], str(self.usuario_a))
        self.assertEqual((await self.registros())[0]["usuario_id"], self.usuario_a)
        self.assertEqual(await self.registros(self.usuario_b), [])

    async def test_mesma_chave_permitida_para_dois_estudantes(self) -> None:
        """Permite a mesma informação em contas diferentes sem colisão global.

        O cenário usa cookies reais distintos para dois POSTs e relê cada FK.
        Ele existe para verificar a participação do usuário na chave única.
        """
        a = await self.cadastrar(self.dados(), self.cookie_a)
        b = await self.cadastrar(self.dados(), self.cookie_b)
        self.assertEqual((a.status, b.status), (201, 201))
        self.assertNotEqual(a.json()["id"], b.json()["id"])
        self.assertEqual(len(await self.registros()), 1)
        self.assertEqual(len(await self.registros(self.usuario_b)), 1)

    async def test_limites_textuais_validos(self) -> None:
        """Aceita os limites de um e duzentos caracteres após trim.

        O cenário envia textos de ambos os campos nos extremos contratuais e
        confere o conteúdo persistido. Ele existe para detectar restrições
        extras na API ou armazenamento que não pertencem ao domínio atual.
        """
        for tamanho in (1, 200):
            with self.subTest(tamanho=tamanho):
                dados = {"nome": "  " + "Á" * tamanho + "  ", self.campo: "É" * tamanho}
                resposta = await self.cadastrar(dados, self.cookie_a)
                self.assertEqual(resposta.status, 201)
                linha = next(
                    item for item in await self.registros()
                    if str(item["id"]) == resposta.json()["id"]
                )
                self.assertEqual(linha["nome"], "Á" * tamanho)
                self.assertEqual(linha[self.campo], "É" * tamanho)

    async def test_textos_invalidos_422_sem_registros(self) -> None:
        """Rejeita ausência, tipos, tamanho e controles inválidos sem escrever.

        O cenário varia os dois campos do payload e consulta a tabela após
        cada rejeição HTTP. Ele existe para verificar regras existentes de
        fronteira/domínio e ausência de gravações em requisições 422.
        """
        for campo in ("nome", self.campo):
            invalidos = [None, 7, True, "", "   ", "a" * 201, "a\x00b", "a\x07b"]
            if self.modelo is CursoRegistro:
                invalidos.append("a\u200bb")
            else:
                invalidos.extend(["a\nb", "a\rb", "a\tb"])
            for indice, invalido in enumerate(invalidos):
                with self.subTest(campo=campo, caso=indice):
                    resposta = await self.cadastrar(self.dados(**{campo: invalido}), self.cookie_a)
                    self.assertEqual(resposta.status, 422)
                    self.assertEqual(await self.registros(), [])
            with self.subTest(campo=campo, caso="ausente"):
                dados = self.dados()
                del dados[campo]
                self.assertEqual((await self.cadastrar(dados, self.cookie_a)).status, 422)
                self.assertEqual(await self.registros(), [])

    async def test_duplicata_normalizada_409_preserva_original(self) -> None:
        """Mantém o registro original ao rejeitar a mesma chave normalizada.

        O cenário varia caixa e espaços dos textos e compara todas as colunas
        antes/depois do conflito. Ele existe para verificar 409 e integridade
        do cadastro, inclusive sem sobrescrever carga horária existente.
        """
        dados = self.dados()
        if self.modelo is CursoRegistro:
            dados["carga_horaria"] = 30
        self.assertEqual((await self.cadastrar(dados, self.cookie_a)).status, 201)
        original = await self.registros()
        repetido = {"nome": "FORMAÇÃO ÁGIL", self.campo: "instituto exemplo"}
        if self.modelo is CursoRegistro:
            repetido["carga_horaria"] = 60
        self.assertEqual((await self.cadastrar(repetido, self.cookie_a)).status, 409)
        self.assertEqual(await self.registros(), original)

    async def test_outro_emissor_ou_instituicao_permite_mesmo_nome(self) -> None:
        """Distingue chaves com mesmo nome e instituição ou emissor diferente.

        O cenário mantém o dono e nome e altera apenas o segundo campo da
        chave, relendo duas linhas. Ele existe para proteger a unicidade
        composta contra uma restrição indevida por nome isolado.
        """
        self.assertEqual((await self.cadastrar(self.dados(), self.cookie_a)).status, 201)
        outro = await self.cadastrar(self.dados(**{self.campo: "Outro Instituto"}), self.cookie_a)
        self.assertEqual(outro.status, 201)
        self.assertEqual(len(await self.registros()), 2)

    async def test_concorrencia_atinge_constraint_e_retorna_201_409(self) -> None:
        """Força disputa real entre dois INSERTs da mesma chave no PostgreSQL.

        A barreira aguarda duas consultas reais sem resultado antes de permitir
        os flushes, sem substituir executores ou fabricar respostas do banco.
        O cenário existe para provar tradução da constraint em HTTP 409, uma
        única linha confirmada e recuperação posterior sem HTTP 500.
        """
        consultar = self.repositorio.existe_por_chave_de_duplicidade
        barreira = asyncio.Barrier(2)
        observadas = []

        async def consultar_com_barreira(repositorio, *args, **kwargs):
            """Sincroniza consultas negativas preservando a consulta SQL real.

            O wrapper delega integralmente ao método original e espera a outra
            requisição, para garantir disputa de unicidade em vez de um simples
            conflito detectado pela consulta preventiva.
            """
            resultado = await consultar(repositorio, *args, **kwargs)
            observadas.append(resultado)
            await asyncio.wait_for(barreira.wait(), timeout=5)
            return resultado

        with patch.object(self.repositorio, "existe_por_chave_de_duplicidade", consultar_com_barreira):
            respostas = await asyncio.gather(
                self.cadastrar(self.dados(), self.cookie_a),
                self.cadastrar(self.dados(), self.cookie_a),
            )
        self.assertEqual(observadas, [False, False])
        self.assertEqual(sorted(resposta.status for resposta in respostas), [201, 409])
        linhas = await self.registros()
        self.assertEqual(len(linhas), 1)
        vencedor = next(resposta for resposta in respostas if resposta.status == 201)
        self.assertEqual(str(linhas[0]["id"]), vencedor.json()["id"])
        recuperacao = await self.cadastrar(self.dados(nome="Após disputa"), self.cookie_a)
        self.assertEqual(recuperacao.status, 201)

    async def test_rollback_apos_insert_e_recuperacao_independente(self) -> None:
        """Reverte escrita executada e preserva o outro cadastro confirmado.

        Um listener temporário de after_flush observa a linha pela conexão da
        transação e lança falha antes do commit. O cenário verifica ausência em
        conexão externa e recuperação, sem alterar código produtivo ou simular
        executor, para demonstrar rollback e independência entre os recursos.
        """
        outra_rota = "/certificacoes" if self.modelo is CursoRegistro else "/cursos"
        outro_modelo = CertificacaoRegistro if self.modelo is CursoRegistro else CursoRegistro
        outro_campo = "organizacao_emissora" if self.modelo is CursoRegistro else "instituicao"
        confirmado = await solicitar_asgi(
            self.app, "POST", outra_rota,
            dados={"nome": "Item preservado", outro_campo: "Instituto"},
            cabecalhos={"cookie": self.cookie_a},
        )
        self.assertEqual(confirmado.status, 201)
        escritas_observadas = []

        def falhar_apos_escrita(sessao, _contexto):
            """Confirma visibilidade local do INSERT e interrompe antes do commit.

            O listener filtra tabela e dono sintético, consulta pela mesma
            conexão e lança erro controlado. Ele existe apenas neste teste para
            provar uma escrita efetiva revertida, sem hook no produto.
            """
            if any(
                isinstance(item, self.modelo) and item.usuario_id == self.usuario_a
                for item in sessao.new
            ):
                quantidade = sessao.connection().scalar(
                    select(func.count()).select_from(self.modelo).where(
                        self.modelo.usuario_id == self.usuario_a
                    )
                )
                escritas_observadas.append(quantidade)
                raise RuntimeError("Falha controlada após INSERT, antes de commit")

        event.listen(Session, "after_flush", falhar_apos_escrita)
        try:
            with self.assertRaisesRegex(AssertionError, "Falha ASGI"):
                await self.cadastrar(self.dados(), self.cookie_a)
        finally:
            event.remove(Session, "after_flush", falhar_apos_escrita)
        self.assertEqual(escritas_observadas, [1])
        self.assertEqual(await self.registros(), [])
        async with self.leitura.connect() as conexao:
            preservado = (await conexao.execute(
                select(outro_modelo.__table__).where(
                    outro_modelo.id == UUID(confirmado.json()["id"])
                )
            )).mappings().one()
            self.assertEqual(preservado["nome"], "Item preservado")
        recuperacao = await self.cadastrar(self.dados(), self.cookie_a)
        self.assertEqual(recuperacao.status, 201)
        self.assertEqual(len(await self.registros()), 1)


class CursosPostgreSqlTestCase(CenariosCadastroPostgreSql, unittest.IsolatedAsyncioTestCase):
    """Aplica os critérios ao POST de cursos e sua carga horária contratual.

    A classe usa o mixin com a tabela e repositório de cursos reais e acrescenta
    os casos numéricos e textuais próprios. Ela existe para comprovar o caminho
    completo da main ao PostgreSQL sem substituir componentes do cadastro.
    """

    rota = "/cursos"
    campo = "instituicao"
    modelo = CursoRegistro
    repositorio = RepositorioCursoSqlAlchemy

    async def test_carga_opcional_nula_e_extremos_permitidos(self) -> None:
        """Aceita carga omitida, nula e limites inteiros de um e dez mil.

        O cenário grava cada variação com chave própria e compara resposta e
        coluna por conexão nova. Ele existe para provar a opcionalidade e os
        limites de carga no caminho HTTP e relacional real.
        """
        for indice, valor in enumerate(("omitida", None, 1, 10000)):
            with self.subTest(caso=indice):
                dados = self.dados(nome=f"Curso {indice}")
                if valor != "omitida":
                    dados["carga_horaria"] = valor
                resposta = await self.cadastrar(dados, self.cookie_a)
                self.assertEqual(resposta.status, 201)
                esperado = None if valor == "omitida" else valor
                self.assertEqual(resposta.json()["carga_horaria"], esperado)
                linha = next(
                    item for item in await self.registros()
                    if str(item["id"]) == resposta.json()["id"]
                )
                self.assertEqual(linha["carga_horaria"], esperado)

    async def test_carga_invalida_422_sem_gravacao(self) -> None:
        """Rejeita carga fora dos limites e valores que não são inteiros estritos.

        O cenário envia zero, negativo, excesso, frações, booleanos e textos,
        relendo a tabela após cada 422. Ele existe para impedir coerção de tipo
        ou persistência parcial de cargas inválidas.
        """
        for valor in (0, -1, 10001, 1.5, 1.0, True, False, "40", "inválida"):
            with self.subTest(valor=valor):
                resposta = await self.cadastrar(self.dados(carga_horaria=valor), self.cookie_a)
                self.assertEqual(resposta.status, 422)
                self.assertEqual(await self.registros(), [])

    async def test_curso_preserva_separadores_textuais_permitidos(self) -> None:
        """Mantém LF, CR e TAB internos, permitidos na regra atual de curso.

        O cenário grava textos com esses separadores e confere a chave com
        espaços colapsados. Ele existe para não atribuir a cursos a regra mais
        restritiva de controles usada pelas certificações.
        """
        resposta = await self.cadastrar(
            {"nome": "Curso\nLivre", "instituicao": "Instituto\tA\rB"}, self.cookie_a
        )
        self.assertEqual(resposta.status, 201)
        linha = (await self.registros())[0]
        self.assertEqual(linha["nome"], "Curso\nLivre")
        self.assertEqual(linha["instituicao"], "Instituto\tA\rB")
        self.assertEqual(linha["nome_normalizado"], "curso livre")
        self.assertEqual(linha["instituicao_normalizada"], "instituto a b")


class CertificacoesPostgreSqlTestCase(CenariosCadastroPostgreSql, unittest.IsolatedAsyncioTestCase):
    """Aplica os mesmos oráculos ao POST de certificações com emissor real.

    A classe configura o mixin para certificações sem sobrescrever o produto.
    Ela existe para tornar explícita a cobertura dos dois recursos e de suas
    respectivas tabelas, constraints e executores transacionais.
    """

    rota = "/certificacoes"
    campo = "organizacao_emissora"
    modelo = CertificacaoRegistro
    repositorio = RepositorioCertificacaoSqlAlchemy


class ComposicaoSemBancoTestCase(unittest.IsolatedAsyncioTestCase):
    """Exercita a composição da main sem banco por sua interface ASGI real.

    A classe carrega uma instância isolada do módulo sem DATABASE_URL e consulta
    as rotas existentes. Ela existe para verificar indisponibilidade e negação
    sem trocar a aplicação principal nem enfraquecer sua autenticação.
    """

    async def test_main_sem_banco_preserva_readiness_e_negacao(self) -> None:
        """Mantém executores ausentes, readiness 503 e cadastros privados 401.

        O cenário executa o próprio módulo main com ambiente sem URL e usa ASGI,
        sem mocks de executores/autenticador. Ele existe para proteger o caminho
        de ausência de persistência sem exigir 503 antes da autenticação.
        """
        origem = importlib.util.find_spec("backend.main").origin
        spec = importlib.util.spec_from_file_location("backend._main_sem_banco_teste", origem)
        modulo = importlib.util.module_from_spec(spec)
        with patch.dict(os.environ):
            os.environ.pop("DATABASE_URL", None)
            spec.loader.exec_module(modulo)
        self.assertIsNone(modulo._engine_persistencia)
        self.assertIsNone(modulo._cadastrar_curso)
        self.assertIsNone(modulo._cadastrar_certificacao)
        self.assertEqual((await solicitar_asgi(modulo.app, "GET", "/health")).status, 200)
        self.assertEqual((await solicitar_asgi(modulo.app, "GET", "/ready")).status, 503)
        for rota, campo in (("/cursos", "instituicao"), ("/certificacoes", "organizacao_emissora")):
            for headers in ({}, {"cookie": f"{modulo._configuracao_cookie_sessao.nome}={'x' * 43}"}):
                resposta = await solicitar_asgi(
                    modulo.app, "POST", rota,
                    dados={"nome": "Item sintético", campo: "Instituto"}, cabecalhos=headers,
                )
                self.assertEqual(resposta.status, 401)
