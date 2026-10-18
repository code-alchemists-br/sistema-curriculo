"""Prepara SQLite migrado e massa sintética para integrar sessões persistidas.

O harness aplica Alembic em subprocesso e controla sessões e transações reais,
com aplicação ASGI montada por operação, para testar persistência e contrato HTTP.
"""

# Proveniência: decision-analysis prompts/backend/20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md#v001

import ast
import asyncio
import base64
import hashlib
import json
import logging
import os
import re
import sys
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from http.cookies import CookieError, SimpleCookie
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import SkipTest
from unittest.mock import patch
from uuid import UUID

from fastapi import Request
from sqlalchemy import event, inspect, select, text, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.api.factory import create_app
from backend.api.sessoes import COOKIE_SESSAO
from backend.application.acesso_estudante import AcessarEstudante
from backend.application.perfil_estudante import ConsultarPerfilEstudante, EditarPerfil
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.repositorio_sessao import (
    RepositorioSessaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_usuario import (
    RepositorioUsuarioSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.sessao import SessaoRegistro
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro
from backend.infrastructure.security.autenticador_sessao import (
    AutenticadorSessaoPersistida,
)
from backend.infrastructure.security.senhas import DerivadorSenhaScrypt
from backend.infrastructure.security.tokens_sessao import (
    CriadorSessaoSeguro,
    RevogadorSessaoSeguro,
)

try:
    import aiosqlite
except ModuleNotFoundError as erro:
    if erro.name != "aiosqlite":
        raise
    AIOSQLITE_DISPONIVEL = False
else:
    AIOSQLITE_DISPONIVEL = aiosqlite is not None

MOTIVO_SEM_AIOSQLITE = "aiosqlite ausente; execute no ambiente Nix tests preparado"
RAIZ = Path(__file__).resolve().parents[4]
INSTANTE_T = datetime(2026, 10, 18, 12, tzinfo=timezone.utc)
USUARIO_A = UUID("10000000-0000-4000-8000-000000000001")
USUARIO_B = UUID("10000000-0000-4000-8000-000000000002")
SENHA_SINTETICA = "Senha-Teste-123"
COLUNAS_SESSAO = (
    "id", "usuario_id", "token_hash", "criada_em", "expira_em", "revogada_em"
)


def verificar_revisoes_unicas() -> None:
    """Detecta revisões Alembic repetidas lendo declarações AST, sem importá-las.

    Inspeciona também atribuições anotadas e informa os pares conflitantes via
    SkipTest, para distinguir o bloqueio preexistente de erros de migration.
    """
    diretorio = RAIZ / "src/backend/infrastructure/persistence/alembic/versions"
    revisoes: dict[str, list[str]] = {}
    for caminho in sorted(diretorio.glob("*.py")):
        arvore = ast.parse(caminho.read_text(encoding="utf-8"), filename=str(caminho))
        for no in arvore.body:
            if isinstance(no, ast.Assign):
                alvos = no.targets
            elif isinstance(no, ast.AnnAssign):
                alvos = [no.target]
            else:
                continue
            if any(isinstance(alvo, ast.Name) and alvo.id == "revision" for alvo in alvos):
                revisao = ast.literal_eval(no.value)
                revisoes.setdefault(revisao, []).append(caminho.name)
    repetidas = [
        f"{revisao}: {', '.join(arquivos)}"
        for revisao, arquivos in revisoes.items() if len(arquivos) > 1
    ]
    if repetidas:
        raise SkipTest("revisões Alembic duplicadas no grafo: " + "; ".join(repetidas))


def token_sintetico(indice: int) -> str:
    """Produz token URL-safe determinístico a partir de um inteiro de 32 bytes.

    Remove padding Base64 para gerar 43 caracteres, permitindo preparar estados
    artificiais sem compartilhar os segredos gerados pelo emissor real.
    """
    return base64.urlsafe_b64encode(indice.to_bytes(32, "big")).rstrip(b"=").decode("ascii")


def resumo_token(token: str) -> str:
    """Calcula SHA-256 UTF-8 da entrada sem gravar ou registrar o segredo.

    Usa a mesma representação hexadecimal do contrato para preparar e comparar
    registros sintéticos nos testes de persistência.
    """
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def ativar_chaves_estrangeiras(conexao, _registro) -> None:
    """Ativa a integridade referencial em cada conexão DBAPI aberta pelo harness.

    Executa o PRAGMA no evento connect da engine para que os testes de FK
    exercitem restrições reais, inclusive quando o pool abre outra conexão.
    """
    cursor = conexao.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=ON")
    finally:
        cursor.close()


class BancoCredenciaisSessao:
    """Mantém banco SQLite exclusivo, migrado e descartável para cada teste.

    Executa Alembic com ambiente filtrado e oferece sessões ORM reais para que
    commit, rollback e reabertura pertençam ao harness, sem alterar o produto.
    """

    def __init__(self) -> None:
        """Reserva diretório exclusivo e URL local, sem abrir banco externo.

        Inicializa a engine como ausente para permitir cleanup mesmo quando
        migrations ou a preparação falham antes de abrir conexões.
        """
        self.diretorio = TemporaryDirectory(prefix="credenciais-sessao-")
        self.url = f"sqlite+aiosqlite:///{Path(self.diretorio.name) / 'sessao.sqlite3'}"
        self.engine = None
        self.head = ""
        self.saida_migrations = ""

    async def executar_alembic(self, *argumentos: str) -> str:
        """Executa Alembic pelo mesmo Python, capturando saída e falhas reais.

        Passa apenas ambiente operacional mínimo e a URL descartável, com cwd
        na raiz, para não herdar credenciais nem apontar para banco do usuário.
        """
        ambiente = {
            chave: os.environ[chave]
            for chave in ("PATH", "TMPDIR", "LANG", "LC_ALL")
            if chave in os.environ
        }
        ambiente.update(
            DATABASE_URL=self.url,
            PYTHONPATH="src",
            PYTHONDONTWRITEBYTECODE="1",
        )
        processo = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "alembic", *argumentos,
            cwd=RAIZ, env=ambiente,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
        )
        try:
            saida, _ = await asyncio.wait_for(processo.communicate(), timeout=60)
        except BaseException:
            if processo.returncode is None:
                processo.kill()
            await processo.wait()
            raise
        texto = saida.decode("utf-8", errors="replace")
        if processo.returncode != 0:
            raise RuntimeError(f"Alembic {' '.join(argumentos)} falhou:\n{texto}")
        if "is present more than once" in texto:
            raise AssertionError("Alembic emitiu aviso de revisão duplicada após preflight")
        return texto

    async def preparar(self) -> None:
        """Migra banco vazio até head e grava usuários com scrypt real.

        Recusa grafo duplicado antes do upgrade e configura FK por conexão,
        permitindo que cada cenário exercite schema e dados persistidos reais.
        """
        verificar_revisoes_unicas()
        heads = await self.executar_alembic("heads")
        linhas = [linha for linha in heads.splitlines() if linha.strip()]
        if len(linhas) != 1 or "(head)" not in linhas[0]:
            raise AssertionError("O grafo usado pelo teste deve possuir uma única head")
        self.head = linhas[0].split()[0]
        self.saida_migrations = await self.executar_alembic("upgrade", "head")
        self.engine = create_async_engine(self.url, hide_parameters=True)
        event.listen(self.engine.sync_engine, "connect", ativar_chaves_estrangeiras)
        self.sessoes = async_sessionmaker(self.engine, expire_on_commit=False)
        derivador = DerivadorSenhaScrypt()
        async with self.sessoes() as sessao:
            for identidade, nome, email in (
                (USUARIO_A, "Pessoa A", "a@example.test"),
                (USUARIO_B, "Pessoa B", "b@example.test"),
            ):
                sessao.add(UsuarioRegistro(
                    id=identidade, nome=nome, email=email,
                    hash_senha=derivador.derivar(SENHA_SINTETICA).valor,
                    deleted_at=None,
                ))
            await sessao.commit()

    async def fechar(self) -> None:
        """Libera engine e remove o diretório reservado, inclusive após falhas.

        Descarta conexões antes de limpar o arquivo SQLite em finally para
        impedir vazamento de recursos ou compartilhamento entre cenários.
        """
        try:
            if self.engine is not None:
                await self.engine.dispose()
        finally:
            self.diretorio.cleanup()

    async def snapshot(self) -> dict:
        """Relê sessões e usuários em sessão nova, sem imprimir dados recebidos.

        Seleciona todas as colunas em ordem estável para comparar o estado por
        igualdade booleana e detectar mutações ou linhas residuais após rollback.
        """
        async with self.sessoes() as sessao:
            sessoes = (await sessao.execute(
                select(SessaoRegistro.__table__).order_by(SessaoRegistro.id)
            )).all()
            usuarios = (await sessao.execute(
                select(UsuarioRegistro.__table__).order_by(UsuarioRegistro.id)
            )).all()
        return {"sessoes": tuple(sessoes), "usuarios": tuple(usuarios)}

    async def inspecionar_schema(self) -> dict:
        """Consulta o inspetor do banco migrado e a versão Alembic efetiva.

        Usa run_sync apenas como ponte da conexão assíncrona para inspeção SQL,
        permitindo verificar DDL real em vez de confiar na metadata do ORM.
        """
        def ler_schema(conexao) -> dict:
            """Lê constraints e colunas pela conexão real para validar M01.

            Instancia o inspetor sobre o banco já migrado e retorna estruturas
            independentes da metadata produtiva para comparar seu contrato.
            """
            inspetor = inspect(conexao)
            return {
                "colunas": inspetor.get_columns("sessoes"),
                "pk": inspetor.get_pk_constraint("sessoes"),
                "fks": inspetor.get_foreign_keys("sessoes"),
                "unicas": inspetor.get_unique_constraints("sessoes"),
            }

        async with self.engine.connect() as conexao:
            schema = await conexao.run_sync(ler_schema)
            schema["versoes"] = tuple((await conexao.execute(
                text("SELECT version_num FROM alembic_version")
            )).scalars())
        return schema
    # Proveniência: decision-analysis prompts/backend/20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md#v001
    async def semear_sessao(
        self, indice: int, usuario_id: UUID, *, expira_em: datetime | None = None,
        revogada_em: datetime | None = None,
    ) -> str:
        """Grava estado sintético de sessão sem guardar seu segredo no banco.

        Usa repositório real, atualização ORM e commit externo para preparar
        expiração ou revogação sem depender de uma operação HTTP anterior.
        """
        token = token_sintetico(indice)
        resumo = resumo_token(token)
        async with self.sessoes() as sessao:
            await RepositorioSessaoSqlAlchemy(sessao).salvar(
                UsuarioId(usuario_id), resumo, INSTANTE_T,
                expira_em if expira_em is not None else INSTANTE_T + timedelta(hours=8),
            )
            if revogada_em is not None:
                await sessao.execute(update(SessaoRegistro).where(
                    SessaoRegistro.token_hash == resumo
                ).values(revogada_em=revogada_em))
            await sessao.commit()
        return token

    async def marcar_conta_excluida(self, usuario_id: UUID) -> None:
        """Exclui logicamente uma conta da massa pelo banco e confirma o commit.

        Atualiza somente deleted_at em transação própria para isolar a regra
        de invalidação das sessões sem testar o endpoint de exclusão de perfil.
        """
        async with self.sessoes() as sessao:
            await sessao.execute(update(UsuarioRegistro).where(
                UsuarioRegistro.id == usuario_id
            ).values(deleted_at=INSTANTE_T))
            await sessao.commit()

    async def requisitar(
        self, metodo: str, caminho: str, *, dados: dict | None = None,
        token: str | None = None, cabecalhos: dict | None = None,
        query: str = "", instante: datetime = INSTANTE_T,
        ausentes: frozenset[str] = frozenset(),
    ) -> "RespostaCredenciais":
        """Monta serviços reais por requisição e confirma a transação no harness.

        Abre nova AsyncSession, instala proxies que delegam e controla somente
        os relógios de segurança. Em erro faz rollback e redige a evidência.
        Prova integração sob commit do teste, não que a produção confirma antes
        de devolver Set-Cookie. Cada chamada seguinte abre outra sessão/app.
        """
        if not ausentes <= {"acesso", "criador", "revogador"}:
            raise ValueError("Dependência ausente não reconhecida pelo harness")
        async with self.sessoes() as sessao:
            usuarios = RepositorioUsuarioSqlAlchemy(sessao)
            sessoes = RepositorioSessaoSqlAlchemy(sessao)
            derivador = DerivadorSenhaScrypt()
            consulta = ObservadorPerfil(ConsultarPerfilEstudante(usuarios))
            edicao = ObservadorPerfil(EditarPerfil(usuarios))
            app = create_app(
                acessar_estudante=None if "acesso" in ausentes else AcessarEstudante(usuarios, derivador),
                derivador_senha=derivador,
                criador_sessao=None if "criador" in ausentes else CriadorSessaoSeguro(sessoes),
                revogador_sessao=None if "revogador" in ausentes else RevogadorSessaoSeguro(sessoes),
                autenticador_sessao=AutenticadorSessaoPersistida(sessoes),
                consultar_perfil=consulta,
                editar_perfil=edicao,
            )
            try:
                with (
                    patch("backend.infrastructure.security.tokens_sessao.datetime") as emissao,
                    patch("backend.infrastructure.security.autenticador_sessao.datetime") as autenticacao,
                ):
                    emissao.now.return_value = instante
                    autenticacao.now.return_value = instante
                    resposta = await solicitar_asgi(
                        app, metodo, caminho, dados=dados, token=token,
                        cabecalhos=cabecalhos, query=query,
                    )
                await sessao.commit()
            except Exception as erro:
                await sessao.rollback()
                raise RuntimeError(
                    f"Falha na operação integrada ({type(erro).__name__}); "
                    "Cookie, Set-Cookie e credenciais [REDACTED]"
                ) from None
        resposta.consultas = tuple(consulta.identidades)
        resposta.edicoes = tuple(edicao.identidades)
        return resposta


# Proveniência: decision-analysis prompts/backend/20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md#v001
class ObservadorPerfil:
    """Conta e observa identidades sem substituir o comportamento do caso real.

    Delega integralmente entradas e saídas ao caso de perfil recebido para
    provar que a autenticação bloqueia chamadas sem fabricar resultados.
    """

    def __init__(self, caso_real) -> None:
        """Retém o caso real e inicia a lista de identidades observadas.

        Mantém somente UUIDs em memória para contar chamadas sem reter
        credenciais nem introduzir consultas ou regras de negócio no proxy.
        """
        self.caso_real = caso_real
        self.identidades = []

    async def executar(self, entrada):
        """Registra o UUID da entrada e aguarda integralmente o caso real.

        Propaga retorno e exceções sem interpretá-los para observar a fronteira
        do caso de uso sem simular autenticação, regras ou persistência.
        """
        self.identidades.append(entrada.usuario_id.valor)
        return await self.caso_real.executar(entrada)


@dataclass
class RespostaCredenciais:
    """Guarda resposta ASGI e observações sem expor credenciais no repr.

    Oculta headers e corpo da representação automática, oferecendo leitura
    explícita para asserções booleanas que não imprimem segredos ao falhar.
    """

    status: int
    headers: tuple = field(repr=False)
    corpo: bytes = field(repr=False)
    consultas: tuple = ()
    edicoes: tuple = ()
    cookie_reconhecido: bool = False

    def cabecalhos(self, nome: str) -> list[str]:
        """Obtém valores de header sem logar seu conteúdo, preservando duplicados.

        Filtra os pares HTTP por nome case insensitive para inspecionar cookies
        separadamente, sem perder múltiplos cabeçalhos Set-Cookie.
        """
        return [valor for chave, valor in self.headers if chave.lower() == nome.lower()]

    def json(self):
        """Decodifica JSON explicitamente e redige falhas de corpo inválido.

        Não inclui o corpo na exceção para permitir conferir DTOs e detalhes
        sem que uma resposta defeituosa exponha credenciais no relatório.
        """
        try:
            return json.loads(self.corpo)
        except (ValueError, UnicodeError):
            raise AssertionError("Corpo JSON inválido [REDACTED]") from None

    def cookie_sessao(self):
        """Analisa somente o cookie de sessão e redige erros de cabeçalhos.

        Exige um único Set-Cookie com o nome contratual, devolvendo o Morsel
        para comparar atributos sem imprimir o valor secreto em falhas.
        """
        valores = self.cabecalhos("set-cookie")
        if len(valores) != 1:
            raise AssertionError("Esperado um Set-Cookie [REDACTED]")
        cookies = SimpleCookie()
        try:
            cookies.load(valores[0])
        except CookieError:
            raise AssertionError("Set-Cookie inválido [REDACTED]") from None
        if set(cookies) != {COOKIE_SESSAO}:
            raise AssertionError("Nome ou quantidade de cookies incorreto [REDACTED]")
        return cookies[COOKIE_SESSAO]


@contextmanager
def redigir_logs_asgi(segredos):
    """Protege a evidência da suíte sem certificar sanitização do produto.

    Encadeia temporariamente a fábrica de logs, removendo credenciais conhecidas,
    tokens e headers sensíveis das mensagens; restaura a fábrica em finally.
    """
    fabrica_original = logging.getLogRecordFactory()

    def fabricar(*args, **kwargs):
        """Redige mensagem e detalhes excepcionais antes de criar evidência.

        Chama a fábrica anterior e remove valores conhecidos e tokens URL-safe
        para impedir exposição acidental durante uma operação HTTP integrada.
        """
        registro = fabrica_original(*args, **kwargs)
        mensagem = registro.getMessage()
        for segredo in sorted(set(segredos), key=len, reverse=True):
            if segredo:
                mensagem = mensagem.replace(segredo, "[REDACTED]")
        mensagem = re.sub(r"(?i)(?:set-cookie|cookie|authorization)\s*[:=][^\r\n]*", "[REDACTED]", mensagem)
        registro.msg = re.sub(r"[A-Za-z0-9_-]{43,}", "[REDACTED]", mensagem)
        registro.args = ()
        if registro.exc_info or registro.exc_text:
            registro.exc_info = None
            registro.exc_text = "[REDACTED]"
        return registro

    logging.setLogRecordFactory(fabricar)
    try:
        yield
    finally:
        logging.setLogRecordFactory(fabrica_original)


async def solicitar_asgi(
    app, metodo: str, caminho: str, *, dados: dict | None = None,
    token: str | None = None, cabecalhos: dict | None = None, query: str = "",
) -> RespostaCredenciais:
    """Exercita HTTPS ASGI em memória com JSON e término de resposta completo.

    Entrega http.request uma vez, espera o último body antes de disconnect e
    limita a execução a dez segundos, sem httpx, sockets ou injeção de state.
    Coleta resposta crua apenas em memória; erros e logs redigem credenciais.
    """
    corpo = json.dumps(dados).encode("utf-8") if dados is not None else b""
    headers = {"host": "testserver", **(cabecalhos or {})}
    if dados is not None:
        headers["content-type"] = "application/json"
    if token is not None:
        headers["cookie"] = f"{COOKIE_SESSAO}={token}"
    scope = {
        "type": "http", "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1", "method": metodo, "scheme": "https",
        "path": caminho, "raw_path": caminho.encode("ascii"),
        "query_string": query.encode("ascii"), "root_path": "",
        "headers": [(chave.lower().encode("ascii"), valor.encode("latin-1")) for chave, valor in headers.items()],
        "client": ("testclient", 50000), "server": ("testserver", 443),
    }
    fim = asyncio.Event()
    entregue = False
    inicios = []
    partes = []

    async def receber():
        """Entrega o JSON uma vez e desconecta somente após o último body.

        Aguarda evento sinalizado pelo envio completo para que o middleware
        não interrompa streaming e o harness possa verificar o corpo real.
        """
        nonlocal entregue
        if not entregue:
            entregue = True
            return {"type": "http.request", "body": corpo, "more_body": False}
        await fim.wait()
        return {"type": "http.disconnect"}

    async def enviar(evento):
        """Coleta headers e corpo e sinaliza conclusão da resposta ASGI.

        Preserva cada fragmento até more_body falso para testar 204 vazio e
        respostas JSON sem imprimir cookies ou conteúdo sensível.
        """
        if evento["type"] == "http.response.start":
            inicios.append(evento)
        elif evento["type"] == "http.response.body":
            partes.append(evento.get("body", b""))
            if not evento.get("more_body", False):
                fim.set()

    segredos = [token or "", SENHA_SINTETICA, query]
    segredos.extend(valor for valor in (dados or {}).values() if isinstance(valor, str))
    segredos.extend(headers.values())
    with redigir_logs_asgi(segredos):
        try:
            await asyncio.wait_for(app(scope, receber, enviar), timeout=10)
        except Exception as erro:
            raise AssertionError(f"Falha ASGI ({type(erro).__name__}); credenciais [REDACTED]") from None
    if len(inicios) != 1 or not fim.is_set():
        raise AssertionError("Resposta ASGI incompleta; cabeçalhos e corpo [REDACTED]")
    inicio = inicios[0]
    return RespostaCredenciais(
        status=inicio["status"],
        headers=tuple((chave.decode("latin-1"), valor.decode("latin-1")) for chave, valor in inicio["headers"]),
        corpo=b"".join(partes),
        cookie_reconhecido=token is not None and Request(scope).cookies.get(COOKIE_SESSAO) == token,
    )
