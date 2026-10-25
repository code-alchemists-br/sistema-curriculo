"""Compõe integração ASGI/SQLite migrado reutilizando o harness autenticado.

Ordenação significa seções persistidas e sort automático de itens na prévia;
não há operação de ordem manual dos itens nem ordem personalizada na prévia.
As consultas de item são doubles tipados: propriedade real em produção não é
provada. Critérios inferidos, sem aceite oficial do card. Não certifica main.py,
cadeia original do Alembic, PostgreSQL, concorrência, falha de banco ou política
de exclusão/alteração de item selecionado. Nenhum adapter produtivo é criado.

Mede migração e seed com perf_counter. Quando migrar custa mais que semear,
copia um template vazio migrado uma vez por classe, com arquivo exclusivo por
variante; caso contrário migra cada arquivo. Nunca usa create_all ou stamp.
"""

# Proveniência: decision-analysis prompts/backend/20261025-193758-integracao-selecao-ordenacao-curriculo-v001.md#v001
from __future__ import annotations

import ast
import asyncio
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import closing
from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, patch
from uuid import UUID

try:
    import aiosqlite
except ModuleNotFoundError as erro:
    if erro.name != "aiosqlite":
        raise
    AIOSQLITE_DISPONIVEL = False
else:
    AIOSQLITE_DISPONIVEL = aiosqlite is not None

from sqlalchemy import select

from backend.api.factory import create_app
from backend.application.listagem_versoes_curriculo import ListarVersoesCurriculo
from backend.application.ports import ItemPerfil
from backend.application.previa_versao_curriculo import GerarPreviaVersaoCurriculo
from backend.application.selecao_itens_versao_curriculo import (
    DesselecionarItemVersaoCurriculo,
    SelecionarItemVersaoCurriculo,
)
from backend.application.versao_curriculo import AtualizarOrdemSecoesCurriculo
from backend.domain.curriculo import Curriculo
from backend.domain.itens_perfil import (
    CategoriaCompetencia,
    Competencia,
    Documento,
    ExperienciaProfissional,
    FormacaoAcademica,
    Idioma,
    NivelFormacaoAcademica,
    ProjetoAcademico,
    StatusFormacaoAcademica,
)
from backend.domain.secao_curriculo import ORDEM_PADRAO_SECOES
from backend.domain.value_objects import (
    CompetenciaId,
    CurriculoId,
    DocumentoId,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    IdiomaId,
    IdItemPerfil,
    Periodo,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
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
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro
from backend.infrastructure.security.autenticador_sessao import (
    AutenticadorSessaoPersistida,
)
from backend.infrastructure.security.tokens_sessao import CriadorSessaoSeguro
from backend.tests.fixtures.curriculos_autenticados_integracao import (
    CURRICULO_A,
    CURRICULO_B,
    ITEM_A,
    ITEM_A_NOVO,
    ITEM_B,
    MIGRATIONS,
    RAIZ,
    USUARIO_A,
    USUARIO_B,
    BancoCurriculosAutenticadosIntegracao,
    RotaCurriculo,
    requisitar,
)

CURRICULO_A2 = CurriculoId(UUID(int=204))
TIPOS = (
    "formacao_academica", "experiencia_profissional", "projeto_academico",
    "competencia", "idioma", "documento",
)
CLASSES_ID = (
    FormacaoAcademicaId, ExperienciaProfissionalId, ProjetoAcademicoId,
    CompetenciaId, IdiomaId, DocumentoId,
)
SECOES_PREVIA = ("formacoes", "experiencias", "projetos", "competencias", "idiomas", "documentos")
ORDEM = tuple(secao.value for secao in ORDEM_PADRAO_SECOES)
INVERSA = tuple(reversed(ORDEM))
MOTIVO_DRIVER = "aiosqlite ausente; execute em nix develop .#tests"


def verificar_grafo() -> str:
    """Valida todas as arestas por AST para permitir somente head inequívoca.

    Detecta identidades, referências e ciclos sem importar migrations; ignora
    somente bloqueios conhecidos e deixa parsing/grafo inesperado falhar.
    """
    registros = {}
    arquivos = {}
    for caminho in sorted((MIGRATIONS / "versions").glob("*.py")):
        valores = {}
        for no in ast.parse(caminho.read_text(encoding="utf-8")).body:
            alvos = no.targets if isinstance(no, ast.Assign) else [no.target] if isinstance(no, ast.AnnAssign) else []
            for alvo in alvos:
                if isinstance(alvo, ast.Name) and alvo.id in {"revision", "down_revision"}:
                    valores[alvo.id] = ast.literal_eval(no.value)
        revisao = valores["revision"]
        arquivos.setdefault(revisao, []).append(caminho.name)
        registros[revisao] = valores["down_revision"]
    duplicadas = {r: fs for r, fs in arquivos.items() if len(fs) > 1}
    conhecidas = {
        "20261015_0011": ["20261015_0011_criar_cursos.py", "20261015_0011_exclusao_logica_formacoes_academicas.py"],
        "20261015_0012": ["20261015_0012_criar_links_profissionais.py", "20261015_0012_criar_projetos_academicos.py"],
    }
    if duplicadas:
        if any(fs != conhecidas.get(r) for r, fs in duplicadas.items()):
            raise AssertionError(f"Revisões duplicadas inesperadas: {duplicadas}")
        raise unittest.SkipTest(f"Bloqueio preexistente: revisões Alembic duplicadas {duplicadas}")
    arestas = {r: (d,) if isinstance(d, str) else tuple(d or ()) for r, d in registros.items()}
    for r, pais in arestas.items():
        if any(p not in registros for p in pais):
            raise AssertionError(f"Referência Alembic ausente: {r}: {pais}")
    visitados, ativos = set(), set()

    def visitar(revisao):
        """Percorre ancestrais por DFS e recusa ciclos para não migrar grafo inválido."""
        if revisao in ativos:
            raise AssertionError(f"Ciclo Alembic: {revisao}")
        if revisao in visitados:
            return
        ativos.add(revisao)
        for pai in arestas[revisao]:
            visitar(pai)
        ativos.remove(revisao)
        visitados.add(revisao)

    for revisao in registros:
        visitar(revisao)
    heads = set(registros) - {p for pais in arestas.values() for p in pais}
    if len(heads) != 1:
        detalhe = {r: arquivos[r] for r in sorted(heads)}
        if heads == {"20261017_0004", "20261017_0015"}:
            raise unittest.SkipTest(f"Bloqueio preexistente: múltiplas heads Alembic {detalhe}")
        raise AssertionError(f"Heads Alembic inesperadas: {detalhe}")
    return next(iter(heads))


def identidade(tipo: str, indice: int) -> IdItemPerfil:
    """Cria ID tipado determinístico pela tabela de dados para distinguir referências."""
    t = TIPOS.index(tipo)
    return CLASSES_ID[t](UUID(int=1000 + 100 * (t + 1) + indice))


def construir_item(tipo: str, indice: int) -> ItemPerfil:
    """Constrói entidade válida com enums e período para exercitar seis tipos.

    Usa dados sintéticos Zeta/alfa e IDs fixos, sem atalhos de validação, para
    que as recusas observadas sejam do currículo e não de entidade inválida.
    """
    item_id = identidade(tipo, indice)
    dono = USUARIO_B if indice in {3, 4} else USUARIO_A
    texto = "alfa" if indice in {2, 4} else "Zeta"
    if dono == USUARIO_B:
        texto = "ITEM PRIVADO B " + texto
    if tipo == "formacao_academica":
        andamento = indice % 2 == 1
        return FormacaoAcademica(
            item_id, dono, "Instituição de teste", texto, NivelFormacaoAcademica.GRADUACAO,
            Periodo(date(2024, 2, 1), None if andamento else date(2025, 12, 1)),
            StatusFormacaoAcademica.EM_ANDAMENTO if andamento else StatusFormacaoAcademica.CONCLUIDO,
        )
    if tipo == "experiencia_profissional":
        return ExperienciaProfissional(
            item_id, dono, texto, "Cargo", "Descrição sintética",
            Periodo(date(2024, 1, 1), None if indice % 2 else date(2025, 1, 1)),
        )
    if tipo == "projeto_academico":
        return ProjetoAcademico(item_id, dono, texto, "Descrição sintética", "Python")
    if tipo == "competencia":
        return Competencia(item_id, dono, CategoriaCompetencia.TECNICA, texto, "Básico")
    if tipo == "idioma":
        return Idioma(item_id, dono, texto, "Básico")
    return Documento(item_id, dono, texto + ".pdf", "application/pdf", "https://example.test/documento")


class ConsultasTipadasDouble:
    """Simula as duas portas por classe de ID, registrando consultas por tipo.

    Entidades validadas ficam em memória para provar somente reação do caso de
    uso; nenhum dos seis tipos representa adaptação real de itens em produção.
    """

    def __init__(self):
        """Indexa A/B e extras não selecionados para provar filtro e propriedade simulada."""
        self.por_classe = {classe: {} for classe in CLASSES_ID}
        for tipo in TIPOS:
            for indice in (1, 2, 3, 4, 5, 6):
                item = construir_item(tipo, indice)
                self.por_classe[type(item.id)][item.id] = item
        for item in (
            Idioma(ITEM_A, USUARIO_A, "IDIOMA PRIVADO A", "Intermediário"),
            Idioma(ITEM_B, USUARIO_B, "IDIOMA PRIVADO B", "Avançado"),
            Idioma(ITEM_A_NOVO, USUARIO_A, "IDIOMA NOVO A", "Básico"),
        ):
            self.por_classe[type(item.id)][item.id] = item
        self.consultas_proprietario = []
        self.consultas_item = []

    async def obter_proprietario(self, referencia):
        """Resolve dono no mapa e conta a chamada para localizar a recusa do consumidor."""
        self.consultas_proprietario.append(referencia)
        item = self.por_classe[type(referencia.item_id)].get(referencia.item_id)
        return item.usuario_id if item is not None else None

    async def obter_item(self, referencia):
        """Resolve conteúdo no mapa e conta a leitura para observar o filtro da prévia."""
        self.consultas_item.append(referencia)
        return self.por_classe[type(referencia.item_id)].get(referencia.item_id)


def rota(operacao, usuario=USUARIO_A, curriculo=CURRICULO_A, tipo="idioma", item=None):
    """Monta rota pública com parâmetros explícitos para parear controles e recusas."""
    item = item if item is not None else ITEM_A_NOVO
    base = f"/estudantes/{usuario.valor}/curriculos"
    versao = f"{base}/{curriculo.valor}"
    if operacao == "selecionar":
        return RotaCurriculo(operacao, "POST", versao + "/itens", {"tipo": tipo, "item_id": str(item.valor)}, 201)
    if operacao == "desselecionar":
        return RotaCurriculo(operacao, "DELETE", f"{versao}/itens/{tipo}/{item.valor}", None, 204)
    if operacao == "ordem":
        return RotaCurriculo(operacao, "PUT", versao + "/ordem-secoes", {"ordem_secoes": list(INVERSA)}, 204)
    return RotaCurriculo(operacao, "GET", base if operacao == "listar" else versao + "/previa", None, 200)


def conferir_schema(caminho: Path, head: str):
    """Confere versão e colunas pelo SQLite antes do seed para provar migrations reais."""
    with closing(sqlite3.connect(caminho)) as conexao:
        assert conexao.execute("SELECT version_num FROM alembic_version").fetchall() == [(head,)]
        for tabela, colunas in {
            "curriculos": {"id", "usuario_id", "titulo_versao", "layout", "is_public", "ordem_secoes"},
            "curriculo_itens": {"curriculo_id", "tipo", "item_id"},
        }.items():
            presentes = {r[1] for r in conexao.execute(f"PRAGMA table_info({tabela})")}
            assert presentes == colunas, f"Schema migrado divergiu: {tabela}"


def migrar(caminho: Path, head: str):
    """Aplica upgrade head em subprocesso isolado para nunca herdar URL externa.

    Captura stderr e recusa warnings Alembic; falhas DDL permanecem erros, não
    skips, para separar defeito de execução de bloqueio conhecido de ambiente.
    """
    ambiente = {k: os.environ[k] for k in ("PATH", "TMPDIR", "LANG", "LC_ALL") if k in os.environ}
    ambiente.update(DATABASE_URL=f"sqlite+aiosqlite:///{caminho}", PYTHONPATH=str(RAIZ / "src"), PYTHONDONTWRITEBYTECODE="1")
    resultado = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"], cwd=RAIZ,
        env=ambiente, capture_output=True, text=True, timeout=30, check=True,
    )
    if "warning" in resultado.stderr.casefold():
        raise AssertionError("Alembic emitiu warning durante upgrade local")
    conferir_schema(caminho, head)


class PreparadorBanco:
    """Gerencia template migrado e custos para isolar variantes sem repetir DDL caro."""

    def __init__(self):
        """Reserva métricas e recursos vazios para liberar inclusive preparação incompleta."""
        self.diretorio = None
        self.template = None
        self.copiar = False
        self.tempo_migration = 0.0
        self.tempos = []
        self.tempos_seed = []

    async def criar(self):
        """Prepara arquivo exclusivo, mede migração/seed e compõe banco real.

        Reutiliza somente schema migrado se seu custo domina o seed; fecha
        recursos parciais em falha para não compartilhar estado entre variantes.
        """
        inicio = time.perf_counter()
        head = verificar_grafo()
        primeiro = self.template is None
        if primeiro:
            self.diretorio = tempfile.TemporaryDirectory(prefix="schema-curriculo-")
            self.template = Path(self.diretorio.name) / "template.sqlite3"
            antes = time.perf_counter()
            await asyncio.to_thread(migrar, self.template, head)
            self.tempo_migration = time.perf_counter() - antes
        diretorio = tempfile.TemporaryDirectory(prefix="selecao-ordenacao-")
        caminho = Path(diretorio.name) / "teste.sqlite3"
        banco = None
        try:
            if primeiro or self.copiar:
                shutil.copyfile(self.template, caminho)
                conferir_schema(caminho, head)
            else:
                await asyncio.to_thread(migrar, caminho, head)
            banco = BancoSelecaoOrdenacao(diretorio, f"sqlite+aiosqlite:///{caminho}")
            antes = time.perf_counter()
            await banco.semear()
            seed = time.perf_counter() - antes
            self.tempos_seed.append(seed)
            if primeiro:
                self.copiar = self.tempo_migration > seed
            self.tempos.append(time.perf_counter() - inicio)
            return banco
        except BaseException:
            if banco is not None:
                await banco.fechar()
            else:
                diretorio.cleanup()
            raise

    def fechar(self):
        """Descarta template após a classe para não deixar arquivos ou caches persistentes."""
        if self.diretorio is not None:
            self.diretorio.cleanup()


class BancoSelecaoOrdenacao(BancoCurriculosAutenticadosIntegracao):
    """Estende suporte existente sem editá-lo, compondo cinco casos e seis doubles.

    Reutiliza engine/FKs, snapshots brutos, sessão e cleanup do harness; semeia
    A/A2/B e recompõe factory para testar seleção e ordem com isolamento real.
    """

    async def semear(self):
        """Persiste contas, versões e sessões A/B com commit para controles autenticados."""
        for usuario, letra in ((USUARIO_A, "A"), (USUARIO_B, "B")):
            self.sessao.add(UsuarioRegistro(
                id=usuario.valor, nome=f"ESTUDANTE PRIVADO {letra}",
                email=f"{letra.lower()}@example.test", hash_senha="hash-sintetico-nao-utilizavel", deleted_at=None,
            ))
        await self.sessao.flush()
        repositorio = RepositorioCurriculoSqlAlchemy(self.sessao)
        for cid, dono, item, ordem in (
            (CURRICULO_A, USUARIO_A, ITEM_A, ORDEM_PADRAO_SECOES),
            (CURRICULO_B, USUARIO_B, ITEM_B, ORDEM_PADRAO_SECOES[2:] + ORDEM_PADRAO_SECOES[:2]),
            (CURRICULO_A2, USUARIO_A, identidade("projeto_academico", 1), ORDEM_PADRAO_SECOES[1:] + ORDEM_PADRAO_SECOES[:1]),
        ):
            curriculo = Curriculo(cid, dono, f"CURRICULO PRIVADO {'B' if dono == USUARIO_B else 'A'}", "classico", False, ordem)
            curriculo.incluir_referencia(ReferenciaCurriculo(item))
            await repositorio.salvar(curriculo)
        self.repo_sessoes = RepositorioSessaoSqlAlchemy(self.sessao)
        self.token_a = await CriadorSessaoSeguro(self.repo_sessoes).criar(USUARIO_A)
        self.token_b = await CriadorSessaoSeguro(self.repo_sessoes).criar(USUARIO_B)
        await self.sessao.commit()
        self.itens = ConsultasTipadasDouble()
        self.casos = {
            "selecionar": SelecionarItemVersaoCurriculo(repositorio, self.itens),
            "desselecionar": DesselecionarItemVersaoCurriculo(repositorio),
            "ordem": AtualizarOrdemSecoesCurriculo(repositorio),
            "previa": GerarPreviaVersaoCurriculo(repositorio, RepositorioUsuarioSqlAlchemy(self.sessao), self.itens),
            "listar": ListarVersoesCurriculo(repositorio),
        }
        self.spies = {
            nome: self.patches.enter_context(patch.object(caso, "executar", new=AsyncMock(wraps=caso.executar)))
            for nome, caso in self.casos.items()
        }
        self.compor()

    def compor(self, ausente=None):
        """Monta factory mantendo auth real e omitindo só executor solicitado para provar 503."""
        parametros = {
            "selecionar": "selecionar_item_versao_curriculo",
            "desselecionar": "desselecionar_item_versao_curriculo",
            "ordem": "atualizar_ordem_secoes_curriculo",
            "previa": "gerar_previa_versao_curriculo",
            "listar": "listar_versoes_curriculo",
        }
        self.app = create_app(
            autenticador_sessao=AutenticadorSessaoPersistida(self.repo_sessoes),
            **{parametros[nome]: caso for nome, caso in self.casos.items() if nome != ausente},
        )

    def zerar_observadores(self):
        """Zera somente históricos de spies e doubles após controles para medir a tentativa."""
        for spy in self.spies.values():
            spy.reset_mock()
        self.itens.consultas_proprietario.clear()
        self.itens.consultas_item.clear()

    async def solicitar(self, rota_http, token, **kwargs):
        """Observa bytes ASGI e confirma resposta para provar corpo vazio e escrita real.

        Delega ao transporte HTTPS existente com observador transparente de send,
        sem substituir middleware ou handler, para não confundir JSON null com
        ausência de corpo num 204 nem esconder mutação por rollback preventivo.
        """
        aplicacao = self.app
        partes = []

        async def observar_corpo(escopo, receber, enviar):
            """Encaminha ASGI intacto e observa fragmentos para verificar bytes da resposta."""
            async def observar_envio(mensagem):
                """Acumula somente corpo de resposta e delega send para não alterar transporte."""
                if mensagem["type"] == "http.response.body":
                    partes.append(mensagem.get("body", b""))
                await enviar(mensagem)

            await aplicacao(escopo, receber, observar_envio)

        self.app = observar_corpo
        try:
            resposta = await requisitar(self, rota_http, token, **kwargs)
        finally:
            self.app = aplicacao
        self.corpo_http = b"".join(partes)
        await self.sessao.commit()
        return resposta

    async def estado(self):
        """Lê SQL bruto e agregados em sessões novas para detectar diferenças escondidas.

        O snapshot herdado lê tabelas inteiras; outra sessão reconstrói todas as
        versões para comparar referências, ordem e metadados sem identity map.
        """
        bruto = await self.snapshot()
        async with self.criar_sessao() as leitura:
            repositorio = RepositorioCurriculoSqlAlchemy(leitura)
            agregados = {}
            for cid in bruto["curriculos"]:
                c = await repositorio.obter_por_id(CurriculoId(cid))
                agregados[cid] = (c.usuario_id, c.titulo_versao, c.layout, c.is_public, c.referencias, c.ordem_secoes)
            assert await leitura.scalar(select(UsuarioRegistro.id).limit(1)) is not None
        return {"bruto": bruto, "agregados": agregados}
