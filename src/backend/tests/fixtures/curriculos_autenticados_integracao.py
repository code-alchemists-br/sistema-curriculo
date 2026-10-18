"""Prepara SQLite migrado e uma aplicação de currículos para integração local.

Sessões, usuários, currículos e seleções usam persistência real. As portas
ConsultaProprietarioItem e ConsultaItemPerfil são doubles sem adapter concreto:
seu conteúdo sintético não representa leitura produtiva de itens no banco.
A composição montada no teste não certifica a composição de produção nem a
autenticação persistida de main; o módulo não importa main.app.
"""

# Proveniência: decision-analysis prompts/backend/20261018-123741-recusa-curriculo-alheio-middleware-ativo-v001.md#v001

from __future__ import annotations

import ast
import asyncio
import hashlib
import json
import os
import tempfile
import threading
import unittest
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch
from uuid import UUID

from alembic import command
from alembic.config import Config
from sqlalchemy import event, func, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.api.factory import create_app
from backend.api.sessoes import COOKIE_SESSAO
from backend.application.exclusao_versao_curriculo import ExcluirVersaoCurriculo
from backend.application.listagem_versoes_curriculo import ListarVersoesCurriculo
from backend.application.previa_versao_curriculo import GerarPreviaVersaoCurriculo
from backend.application.selecao_itens_versao_curriculo import (
    DesselecionarItemVersaoCurriculo,
    SelecionarItemVersaoCurriculo,
)
from backend.application.versao_curriculo import (
    AtualizarOrdemSecoesCurriculo,
    CriarVersaoCurriculo,
    EditarVersaoCurriculo,
)
from backend.domain.curriculo import Curriculo
from backend.domain.itens_perfil import Idioma
from backend.domain.secao_curriculo import ORDEM_PADRAO_SECOES
from backend.domain.value_objects import (
    CurriculoId,
    IdiomaId,
    ReferenciaCurriculo,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.curriculo import (
    CurriculoItemRegistro,
    CurriculoRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_curriculo import (
    RepositorioCurriculoSqlAlchemy,
)
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
from backend.infrastructure.security.tokens_sessao import (
    CriadorSessaoSeguro,
    RevogadorSessaoSeguro,
)

try:
    __import__("aiosqlite")
except ModuleNotFoundError as erro:
    if erro.name != "aiosqlite":
        raise
    AIOSQLITE_DISPONIVEL = False
else:
    AIOSQLITE_DISPONIVEL = True

SKIP_SEM_AIOSQLITE = unittest.skipUnless(
    AIOSQLITE_DISPONIVEL,
    "aiosqlite ausente; execute no ambiente Nix tests preparado",
)

RAIZ = Path(__file__).resolve().parents[4]
MIGRATIONS = RAIZ / "src/backend/infrastructure/persistence/alembic"
_PREPARACAO_SERIAL = threading.Lock()

USUARIO_A = UsuarioId(UUID(int=101))
USUARIO_B = UsuarioId(UUID(int=102))
CURRICULO_A = CurriculoId(UUID(int=201))
CURRICULO_B = CurriculoId(UUID(int=202))
CURRICULO_NOVO = CurriculoId(UUID(int=203))
CURRICULO_INEXISTENTE = CurriculoId(UUID(int=299))
ITEM_A = IdiomaId(UUID(int=301))
ITEM_B = IdiomaId(UUID(int=302))
ITEM_A_NOVO = IdiomaId(UUID(int=303))
ITEM_INEXISTENTE = IdiomaId(UUID(int=399))
CORPO_VERSAO = {
    "titulo_versao": "Atualizado A", "layout": "compacto", "is_public": False,
}
ORDEM_ALTERADA = [secao.value for secao in reversed(ORDEM_PADRAO_SECOES)]


def verificar_revisoes_alembic() -> None:
    """Recusa identidades duplicadas lendo declarações AST das migrations.

    Inspeciona revision sem importar os scripts e lista os arquivos envolvidos
    em SkipTest, para distinguir bloqueio preexistente de falha da aplicação.
    Outras falhas de parsing ou configuração continuam sendo erros.
    """
    por_revisao: dict[str, list[str]] = {}
    for caminho in sorted((MIGRATIONS / "versions").glob("*.py")):
        arvore = ast.parse(caminho.read_text(encoding="utf-8"))
        for no in arvore.body:
            if isinstance(no, ast.Assign):
                alvos = no.targets
            elif isinstance(no, ast.AnnAssign):
                alvos = [no.target]
            else:
                continue
            if any(isinstance(alvo, ast.Name) and alvo.id == "revision" for alvo in alvos):
                revisao = ast.literal_eval(no.value)
                por_revisao.setdefault(revisao, []).append(caminho.name)
    duplicadas = [
        f"{revisao}: {', '.join(arquivos)}"
        for revisao, arquivos in por_revisao.items() if len(arquivos) > 1
    ]
    if duplicadas:
        raise unittest.SkipTest(
            "cadeia Alembic com revisões duplicadas; bloqueio preexistente: "
            + "; ".join(duplicadas)
        )


def _aplicar_migrations(database_url: str) -> None:
    """Migra apenas o SQLite fornecido usando o alembic.ini real.

    Serializa Alembic e a troca temporária de DATABASE_URL, restaurando a
    variável em finally, para não herdar destinos nem contaminar outros casos.
    """
    with _PREPARACAO_SERIAL:
        verificar_revisoes_alembic()
        configuracao = Config(str(RAIZ / "alembic.ini"))
        configuracao.set_main_option("script_location", str(MIGRATIONS))
        anterior = os.environ.get("DATABASE_URL")
        os.environ["DATABASE_URL"] = database_url
        try:
            command.upgrade(configuracao, "heads")
        finally:
            if anterior is None:
                os.environ.pop("DATABASE_URL", None)
            else:
                os.environ["DATABASE_URL"] = anterior


def _ativar_chaves_estrangeiras(conexao, _registro) -> None:
    """Ativa FKs em cada conexão SQLite com PRAGMA, para verificar integridade.

    Não cria schema: somente habilita a validação das relações já migradas,
    evitando que o harness aceite seleções sem currículo ou sessão sem conta.
    """
    cursor = conexao.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=ON")
    finally:
        cursor.close()


class ConsultasItensDouble:
    """Simula ConsultaProprietarioItem e ConsultaItemPerfil por mapa local.

    Guarda entidades sintéticas e registra consultas para observar a interrupção
    após recusa de currículo. Não prova um adapter produtivo de itens.
    """

    def __init__(self) -> None:
        """Indexa três idiomas de A/B em memória para distinguir propriedade.

        Usa identidades fixas e marcadores privados para que seleção e prévia
        reais possam ser exercitadas sem inventar um adapter de produção.
        """
        self.itens = {
            item.id: item for item in (
                Idioma(ITEM_A, USUARIO_A, "IDIOMA PRIVADO A", "Intermediário"),
                Idioma(ITEM_B, USUARIO_B, "IDIOMA PRIVADO B", "Avançado"),
                Idioma(ITEM_A_NOVO, USUARIO_A, "IDIOMA NOVO A", "Básico"),
            )
        }
        self.consultas_proprietario: list[ReferenciaCurriculo] = []
        self.consultas_item: list[ReferenciaCurriculo] = []

    async def obter_proprietario(self, referencia: ReferenciaCurriculo) -> UsuarioId | None:
        """Consulta o dono no mapa e registra a referência para provar a guarda.

        Retorna ausência para ID desconhecido e o dono sintético nos demais,
        permitindo verificar a reação do caso real sem simular sua regra.
        """
        self.consultas_proprietario.append(referencia)
        item = self.itens.get(referencia.item_id)
        return item.usuario_id if item is not None else None

    async def obter_item(self, referencia: ReferenciaCurriculo) -> Idioma | None:
        """Lê conteúdo sintético pelo ID e registra a consulta para a prévia.

        O mapa entrega a entidade ou None sem consultar SQL, para explicitar
        o limite da integração de conteúdo e observar recusas antecipadas.
        """
        self.consultas_item.append(referencia)
        return self.itens.get(referencia.item_id)


class GeradorCurriculoDeterministico:
    """Fornece o ID reservado de criação para comparar estados entre bancos.

    O cenário cria no máximo uma versão por banco, portanto uma constante
    torna os controles equivalentes sem substituir a criação real do agregado.
    """

    def gerar(self) -> CurriculoId:
        """Devolve o ID novo fixo, sem acessar serviços, para isolar a criação."""
        return CURRICULO_NOVO


@dataclass(frozen=True)
class RotaCurriculo:
    """Descreve uma operação HTTP concreta para a matriz integrada.

    Reúne nome do executor, método, caminho, JSON válido e status de sucesso,
    para que todos os cenários usem as mesmas oito operações verificáveis.
    """

    nome: str
    metodo: str
    caminho: str
    corpo: dict[str, Any] | None
    sucesso: int


def rotas_curriculo(
    usuario: UsuarioId = USUARIO_A, curriculo: CurriculoId = CURRICULO_A,
) -> tuple[RotaCurriculo, ...]:
    """Monta as oito rotas existentes com IDs e payloads válidos do cenário.

    Interpola dono e versão, mantendo item próprio novo na seleção e item já
    selecionado na remoção, para que recusas não sejam causadas por payload.
    """
    base = f"/estudantes/{usuario.valor}/curriculos"
    versao = f"{base}/{curriculo.valor}"
    return (
        RotaCurriculo("listar", "GET", base, None, 200),
        RotaCurriculo("criar", "POST", base, dict(CORPO_VERSAO), 201),
        RotaCurriculo("editar", "PUT", versao, dict(CORPO_VERSAO), 200),
        RotaCurriculo("ordem", "PUT", f"{versao}/ordem-secoes",
                      {"ordem_secoes": list(ORDEM_ALTERADA)}, 204),
        RotaCurriculo("excluir", "DELETE", versao, None, 204),
        RotaCurriculo("previa", "GET", f"{versao}/previa", None, 200),
        RotaCurriculo("selecionar", "POST", f"{versao}/itens",
                      {"tipo": "idioma", "item_id": str(ITEM_A_NOVO.valor)}, 201),
        RotaCurriculo("desselecionar", "DELETE",
                      f"{versao}/itens/idioma/{ITEM_A.valor}", None, 204),
    )


class BancoCurriculosAutenticadosIntegracao:
    """Agrupa banco descartável e composição real para um cenário ASGI.

    Migra um arquivo SQLite exclusivo, confirma seed e sessão opaca, injeta
    adapters reais e observa casos por wraps para provar autorização integrada.
    """

    def __init__(self, diretorio: tempfile.TemporaryDirectory, database_url: str) -> None:
        """Abre recursos locais a partir da URL gerada, sem usar URL herdada.

        Cria engine, sessão e pilha de patches próprios para centralizar
        composição e cleanup mesmo se uma asserção ou preparação falhar.
        """
        self.diretorio = diretorio
        self.engine = create_async_engine(database_url)
        event.listen(self.engine.sync_engine, "connect", _ativar_chaves_estrangeiras)
        self.criar_sessao = async_sessionmaker(self.engine, expire_on_commit=False)
        self.sessao = self.criar_sessao()
        self.patches = ExitStack()
        self.itens = ConsultasItensDouble()
        self.cabecalhos_resposta: tuple[tuple[bytes, bytes], ...] = ()

    @classmethod
    async def criar(cls) -> BancoCurriculosAutenticadosIntegracao:
        """Cria e migra SQLite em thread e prepara um cenário independente.

        Registra os recursos à medida que surgem e fecha todos em caso de erro,
        para que cada subteste tenha banco novo sem resíduos nem create_all.
        """
        verificar_revisoes_alembic()
        diretorio = tempfile.TemporaryDirectory(prefix="curriculos-autenticados-")
        url = f"sqlite+aiosqlite:///{Path(diretorio.name) / 'teste.sqlite3'}"
        banco = None
        try:
            await asyncio.to_thread(_aplicar_migrations, url)
            banco = cls(diretorio, url)
            await banco._semear_e_compor()
            return banco
        except BaseException:
            if banco is not None:
                await banco.fechar()
            else:
                diretorio.cleanup()
            raise

    async def _semear_e_compor(self) -> None:
        """Persiste A/B e seus currículos, emite sessão A e monta a fábrica.

        Confirma os dados antes da chamada HTTP e envolve os oito casos reais
        em spies para distinguir recusa no middleware de recusa na aplicação.
        """
        self.sessao.add_all([
            UsuarioRegistro(id=usuario.valor, nome=f"ESTUDANTE PRIVADO {letra}",
                            email=f"{letra.lower()}@example.test",
                            hash_senha="hash-sintetico-nao-utilizavel", deleted_at=None)
            for usuario, letra in ((USUARIO_A, "A"), (USUARIO_B, "B"))
        ])
        await self.sessao.flush()
        repositorio = RepositorioCurriculoSqlAlchemy(self.sessao)
        for identidade, usuario, item, letra in (
            (CURRICULO_A, USUARIO_A, ITEM_A, "A"),
            (CURRICULO_B, USUARIO_B, ITEM_B, "B"),
        ):
            curriculo = Curriculo(id=identidade, usuario_id=usuario,
                                 titulo_versao=f"CURRICULO PRIVADO {letra}",
                                 layout="classico", is_public=False)
            curriculo.incluir_referencia(ReferenciaCurriculo(item))
            await repositorio.salvar(curriculo)
        self.repo_sessoes = RepositorioSessaoSqlAlchemy(self.sessao)
        self.token_a = await CriadorSessaoSeguro(self.repo_sessoes).criar(USUARIO_A)
        await self.sessao.commit()
        casos = {
            "listar": ListarVersoesCurriculo(repositorio),
            "criar": CriarVersaoCurriculo(repositorio, GeradorCurriculoDeterministico()),
            "editar": EditarVersaoCurriculo(repositorio),
            "ordem": AtualizarOrdemSecoesCurriculo(repositorio),
            "excluir": ExcluirVersaoCurriculo(repositorio),
            "previa": GerarPreviaVersaoCurriculo(
                repositorio, RepositorioUsuarioSqlAlchemy(self.sessao), self.itens),
            "selecionar": SelecionarItemVersaoCurriculo(repositorio, self.itens),
            "desselecionar": DesselecionarItemVersaoCurriculo(repositorio),
        }
        self.spies = {
            nome: self.patches.enter_context(patch.object(
                caso, "executar", new=AsyncMock(wraps=caso.executar)))
            for nome, caso in casos.items()
        }
        self.app = create_app(
            autenticador_sessao=AutenticadorSessaoPersistida(self.repo_sessoes),
            listar_versoes_curriculo=casos["listar"],
            criar_versao_curriculo=casos["criar"],
            editar_versao_curriculo=casos["editar"],
            atualizar_ordem_secoes_curriculo=casos["ordem"],
            excluir_versao_curriculo=casos["excluir"],
            gerar_previa_versao_curriculo=casos["previa"],
            selecionar_item_versao_curriculo=casos["selecionar"],
            desselecionar_item_versao_curriculo=casos["desselecionar"],
        )

    async def invalidar_sessao(self, estado: str) -> None:
        """Revoga ou expira a sessão A e confirma a mudança antes de autenticar.

        Usa revogador real ou data passada por margem de um dia, sem sleep nem
        relógio global substituído, para provar os filtros persistidos reais.
        """
        if estado == "revogada":
            await RevogadorSessaoSeguro(self.repo_sessoes).revogar(self.token_a)
        elif estado == "expirada":
            await self.sessao.execute(update(SessaoRegistro).where(
                SessaoRegistro.token_hash == hashlib.sha256(self.token_a.encode()).hexdigest()
            ).values(expira_em=datetime.now(timezone.utc) - timedelta(days=1)))
        else:
            raise ValueError(f"Estado de sessão desconhecido: {estado}")
        await self.sessao.commit()

    async def snapshot(self) -> dict[str, Any]:
        """Lê todas as colunas de versões e seleções em outra sessão ORM.

        Confirma primeiro a sessão do fluxo, sem rollback, e consulta tabelas
        em sessão nova para detectar até escrita indevida após resposta de erro.
        """
        await self.sessao.commit()
        async with self.criar_sessao() as leitura:
            versoes = (await leitura.execute(select(CurriculoRegistro.__table__))).mappings()
            curriculos = {linha["id"]: dict(linha) for linha in versoes}
            itens = tuple((await leitura.execute(
                select(CurriculoItemRegistro.__table__).order_by(
                    CurriculoItemRegistro.curriculo_id, CurriculoItemRegistro.tipo,
                    CurriculoItemRegistro.item_id)
            )).tuples().all())
            quantidade = await leitura.scalar(select(func.count()).select_from(CurriculoRegistro))
        return {"curriculos": curriculos, "itens": itens, "quantidade": quantidade}

    async def fechar(self) -> None:
        """Libera patches, sessão, engine e diretório, mesmo após uma falha.

        Encadeia finally para garantir descarte do SQLite exclusivo e evitar
        compartilhamento de estado ou conexões entre testes.
        """
        try:
            self.patches.close()
            await self.sessao.close()
        finally:
            try:
                await self.engine.dispose()
            finally:
                self.diretorio.cleanup()


async def requisitar(
    banco: BancoCurriculosAutenticadosIntegracao, rota: RotaCurriculo,
    token: str | None, *, query: str = "", corpo: dict | None = None,
    bearer: str | None = None,
) -> tuple[int, Any]:
    """Executa a rota pela aplicação ASGI real sem rede ou helper de outro teste.

    Separa query e caminho, usa HTTPS e mantém receive aberto até o último
    fragmento, com timeout de cinco segundos, para não truncar o middleware.
    """
    conteudo = rota.corpo if corpo is None else corpo
    dados = json.dumps(conteudo).encode() if conteudo is not None else b""
    banco.cabecalhos_resposta = ()
    cabecalhos = [(b"host", b"testserver"), (b"content-type", b"application/json"),
                  (b"content-length", str(len(dados)).encode())]
    if token is not None:
        cabecalhos.append((b"cookie", f"{COOKIE_SESSAO}={token}".encode()))
    if bearer is not None:
        cabecalhos.append((b"authorization", f"Bearer {bearer}".encode()))
    caminho, _, query_no_caminho = rota.caminho.partition("?")
    escopo = {
        "type": "http", "asgi": {"version": "3.0", "spec_version": "2.4"},
        "http_version": "1.1", "method": rota.metodo, "scheme": "https",
        "path": caminho, "raw_path": caminho.encode(),
        "query_string": (query or query_no_caminho).encode(), "root_path": "",
        "headers": cabecalhos, "client": ("testclient", 50000),
        "server": ("testserver", 443),
    }
    entregue = False
    concluida = asyncio.Event()
    status = None
    partes = []

    async def receber() -> dict:
        """Entrega JSON uma vez e aguarda conclusão para preservar a conexão.

        O evento só libera disconnect depois do último fragmento de resposta,
        garantindo observação completa da saída da aplicação real.
        """
        nonlocal entregue
        if not entregue:
            entregue = True
            return {"type": "http.request", "body": dados, "more_body": False}
        await concluida.wait()
        return {"type": "http.disconnect"}

    async def enviar(mensagem: dict) -> None:
        """Acumula status e corpo ASGI e marca a conclusão do último fragmento.

        A coleta preserva corpo vazio e JSON completo para os oráculos HTTP,
        sem comparar cabeçalhos de correlação variáveis.
        """
        nonlocal status
        if mensagem["type"] == "http.response.start":
            status = mensagem["status"]
            banco.cabecalhos_resposta = tuple(mensagem.get("headers", ()))
        elif mensagem["type"] == "http.response.body":
            partes.append(mensagem.get("body", b""))
            if not mensagem.get("more_body", False):
                concluida.set()

    await asyncio.wait_for(banco.app(escopo, receber, enviar), timeout=5)
    if status is None or not concluida.is_set():
        raise AssertionError("Aplicação não concluiu a resposta HTTP ASGI.")
    payload = b"".join(partes)
    return status, json.loads(payload) if payload else None
