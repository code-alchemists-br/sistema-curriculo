"""Compõe CUD de formação por ASGI e leitura interna em SQLite migrado.

Reutiliza o banco e o transporte de credenciais, com casos/repos reais e spies
delegantes, para provar propriedade sem inventar consulta HTTP (pendência L1).
Não certifica main.py, cadeia Alembic original, PostgreSQL, concorrência,
retenção, falhas de banco nem HTTPS/cookies em navegador. Critérios inferidos
do título: não foi fornecido aceite oficial do card.

Um modelo migrado é preparado por classe e copiado com engines fechadas para
cada cenário. Os tempos de migração e cópia são medidos para explicitar esse
custo e preservar isolamento sem repetir Alembic e scrypt em cada subteste.
"""

# Proveniência: decision-analysis prompts/backend/20261025-112457-integracao-crud-formacao-academica-propriedade-v001.md#v001

import ast
import shutil
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from time import perf_counter
from unittest import SkipTest
from unittest.mock import AsyncMock, patch
from uuid import UUID

from sqlalchemy import event, select, text, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.api.factory import create_app
from backend.application.perfil_estudante import (
    CadastrarFormacaoAcademica,
    EditarFormacaoAcademica,
    ExcluirFormacaoAcademica,
)
from backend.domain.value_objects import FormacaoAcademicaId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.curriculo import (
    CurriculoItemRegistro,
    CurriculoRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.formacao_academica import (
    FormacaoAcademicaRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_formacao_academica import (
    RepositorioFormacaoAcademicaSqlAlchemy,
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
from backend.tests.fixtures.credenciais_sessao import (
    INSTANTE_T,
    RAIZ,
    USUARIO_A,
    USUARIO_B,
    BancoCredenciaisSessao,
    RespostaCredenciais,
    ativar_chaves_estrangeiras,
    resumo_token,
    solicitar_asgi,
)

try:
    import aiosqlite
except ModuleNotFoundError as erro:
    if erro.name != "aiosqlite":
        raise
    AIOSQLITE_DISPONIVEL = False
else:
    AIOSQLITE_DISPONIVEL = aiosqlite is not None

F = UUID("30000000-0000-4000-8000-000000000001")
G = UUID("30000000-0000-4000-8000-000000000002")
H = UUID("30000000-0000-4000-8000-000000000099")
CURRICULO_A = UUID("20000000-0000-4000-8000-000000000001")
CURRICULO_B = UUID("20000000-0000-4000-8000-000000000002")
V = {
    "instituicao": " Instituto A ",
    "curso": " Sistemas ",
    "nivel": "graduacao",
    "data_inicio": "2024-02-01",
    "data_fim": None,
    "status": "em_andamento",
}
W = {
    "instituicao": "Instituto Atualizado",
    "curso": "Sistemas Avançados",
    "nivel": "mestrado",
    "data_inicio": "2025-02-01",
    "data_fim": "2030-12-01",
    "status": "concluido",
}
MOTIVO_DRIVER = "aiosqlite ausente; execute no ambiente Nix tests preparado"


def verificar_grafo() -> str:
    """Valida o grafo por AST antes de reservar banco, sem importar migrations.

    Confere IDs, referências, ciclos e heads, ignorando somente os defeitos
    conhecidos da branch; falhas novas/parsing continuam erros para não ocultar
    regressões. Devolve a head única para conferir alembic_version real.
    """
    diretorio = RAIZ / "src/backend/infrastructure/persistence/alembic/versions"
    arquivos = defaultdict(list)
    pais = defaultdict(set)
    for caminho in sorted(diretorio.glob("*.py")):
        dados = {}
        for no in ast.parse(caminho.read_text(encoding="utf-8")).body:
            alvos = (
                no.targets
                if isinstance(no, ast.Assign)
                else ([no.target] if isinstance(no, ast.AnnAssign) else [])
            )
            for alvo in alvos:
                if isinstance(alvo, ast.Name) and alvo.id in {
                    "revision",
                    "down_revision",
                }:
                    dados[alvo.id] = ast.literal_eval(no.value)
        if not dados:
            continue
        revisao, anterior = dados["revision"], dados["down_revision"]
        arquivos[revisao].append(caminho.name)
        pais[revisao].update(
            anterior
            if isinstance(anterior, tuple)
            else ((anterior,) if anterior else ())
        )
    ausentes = {pai for valores in pais.values() for pai in valores} - set(pais)
    if ausentes:
        raise AssertionError(f"Referências Alembic ausentes: {sorted(ausentes)}")
    visitados, pilha = set(), set()

    def visitar(revisao):
        """Percorre ancestrais por DFS para rejeitar ciclos antes de executar Alembic.

        Marca a pilha ativa separada dos nós completos, permitindo detectar
        arestas de retorno sem tratar merges legítimos como ciclos.
        """
        if revisao in pilha:
            raise AssertionError(f"Ciclo Alembic em {revisao}: {arquivos[revisao]}")
        if revisao in visitados:
            return
        pilha.add(revisao)
        for pai in pais[revisao]:
            visitar(pai)
        pilha.remove(revisao)
        visitados.add(revisao)

    for revisao in pais:
        visitar(revisao)
    duplicadas = {rev: nomes for rev, nomes in arquivos.items() if len(nomes) > 1}
    conhecidas = {
        "20261015_0011": [
            "20261015_0011_criar_cursos.py",
            "20261015_0011_exclusao_logica_formacoes_academicas.py",
        ],
        "20261015_0012": [
            "20261015_0012_criar_links_profissionais.py",
            "20261015_0012_criar_projetos_academicos.py",
        ],
    }
    heads = set(pais) - {pai for valores in pais.values() for pai in valores}
    if duplicadas == conhecidas and heads == {"20261017_0004", "20261017_0015"}:
        raise SkipTest(
            "grafo Alembic original bloqueado; revisões duplicadas: "
            + "; ".join(
                f"{rev}: {', '.join(nomes)}" for rev, nomes in duplicadas.items()
            )
            + "; heads: "
            + ", ".join(f"{rev} ({', '.join(arquivos[rev])})" for rev in sorted(heads))
        )
    if duplicadas or len(heads) != 1:
        raise AssertionError(
            f"Grafo Alembic inesperado: duplicadas={duplicadas}, heads={sorted(heads)}"
        )
    return next(iter(heads))


def normalizar_utc(valor):
    """Normaliza datetime bruto do SQLite explicitamente para UTC.

    Atribui UTC ao valor sem fuso e converte os demais para comparar snapshots;
    isso evita inferir suporte de timezone de PostgreSQL a partir deste teste.
    """
    if isinstance(valor, datetime):
        return (
            valor.replace(tzinfo=timezone.utc)
            if valor.tzinfo is None
            else valor.astimezone(timezone.utc)
        )
    return valor


class GeradorFormacaoSequencial:
    """Gera IDs tipados em sequência local para controlar candidatos do cenário.

    Mantém cursor por banco e permite reservar um candidato ainda não persistido,
    para que uma recusa e seu controle usem a mesma identidade sem tocar produto.
    """

    def __init__(self):
        """Inicia o cursor em F para gerar identidades determinísticas por banco.

        Guarda apenas estado local, isolando cenários e dispensando aleatoriedade.
        """
        self.proximo = F.int

    def gerar(self) -> FormacaoAcademicaId:
        """Devolve o cursor tipado e o incrementa para criar formações previsíveis.

        A sequência existe somente na fixture, sem substituir persistência real.
        """
        identidade = FormacaoAcademicaId(UUID(int=self.proximo))
        self.proximo += 1
        return identidade


class RelogioExclusaoFixo:
    """Controla o instante de exclusão e conta leituras do caso real.

    Fornece UTC fixo e permite avançar o instante para provar que a repetição
    não muda o primeiro tombstone nem consulta novamente o relógio.
    """

    def __init__(self):
        """Reserva UTC e contador por banco para isolar a prova de idempotência.

        Não consulta relógio externo, mantendo o cenário determinístico.
        """
        self.instante = INSTANTE_T
        self.chamadas = 0

    def agora(self):
        """Conta a leitura e retorna o UTC controlado para marcar a exclusão.

        O contador permite provar que uma segunda exclusão não produz transição.
        """
        self.chamadas += 1
        return self.instante


class BancoFormacoesAcademicasIntegracao:
    """Mantém cópia isolada de SQLite migrado e compõe formação por requisição.

    Delega lifecycle/seeds ao BancoCredenciaisSessao e usa adapters reais com
    spies para provar estado persistido sem modificar fixtures existentes.
    """

    def __init__(self, banco):
        """Retém o banco exclusivo e inicia gerador, relógio e observações.

        O construtor só é chamado após preflight, para não reservar recursos
        quando o grafo conhecido impede a execução.
        """
        self.banco = banco
        self.gerador = GeradorFormacaoSequencial()
        self.relogio = RelogioExclusaoFixo()
        self.spies = {}
        self.tokens = {}
        self.segundos_copia = 0.0

    @classmethod
    async def preparar_modelo(cls):
        """Prepara uma vez o banco do harness existente e fecha sua engine.

        Mede Alembic e seed reais antes de copiar o arquivo sem conexões abertas,
        para amortizar preparação mantendo um banco independente por cenário.
        """
        verificar_grafo()
        banco = BancoCredenciaisSessao()
        inicio = perf_counter()
        try:
            await banco.preparar()
            await banco.engine.dispose()
            banco.engine = None
            banco.segundos_preparacao = perf_counter() - inicio
            return banco
        except BaseException:
            await banco.fechar()
            raise

    @classmethod
    async def criar(cls, modelo):
        """Copia um modelo fechado e abre engine própria com FKs ativas.

        Verifica a versão efetivamente migrada e semeia sessões A/B reais,
        permitindo cenários novos sem compartilhar transação ou identity map.
        """
        head = verificar_grafo()
        banco = BancoCredenciaisSessao()
        fixture = cls(banco)
        try:
            inicio = perf_counter()
            shutil.copy2(
                Path(modelo.diretorio.name) / "sessao.sqlite3",
                Path(banco.diretorio.name) / "sessao.sqlite3",
            )
            fixture.segundos_copia = perf_counter() - inicio
            banco.engine = create_async_engine(banco.url, hide_parameters=True)
            event.listen(
                banco.engine.sync_engine, "connect", ativar_chaves_estrangeiras
            )
            banco.sessoes = async_sessionmaker(banco.engine, expire_on_commit=False)
            async with banco.sessoes() as sessao:
                versoes = tuple(
                    (
                        await sessao.execute(
                            text("SELECT version_num FROM alembic_version")
                        )
                    ).scalars()
                )
                if versoes != (head,):
                    raise AssertionError("Cópia não está na head do grafo validado")
            fixture.tokens[USUARIO_A] = await banco.semear_sessao(1, USUARIO_A)
            fixture.tokens[USUARIO_B] = await banco.semear_sessao(2, USUARIO_B)
            return fixture
        except BaseException:
            await fixture.fechar()
            raise

    async def fechar(self):
        """Fecha conexões e apaga somente a cópia descartável via harness existente.

        Delega cleanup para não deixar banco ou sessão compartilhados após falha.
        """
        await self.banco.fechar()

    async def requisitar(
        self,
        metodo,
        identidade=F,
        *,
        dados=None,
        token=None,
        query="",
        cabecalhos=None,
        ausente=None,
    ) -> RespostaCredenciais:
        """Executa ASGI com casos/autenticação persistidos e commit após resposta.

        Abre sessão nova, envolve executar com AsyncMock delegante e controla
        somente tempo de autenticação; 4xx/503 também fazem commit, para que
        snapshots detectem escrita indevida sem rollback que a esconderia.
        """
        if ausente not in {None, "POST", "PUT", "DELETE"}:
            raise ValueError("Executor ausente desconhecido")
        async with self.banco.sessoes() as sessao:
            usuarios = RepositorioUsuarioSqlAlchemy(sessao)
            formacoes = RepositorioFormacaoAcademicaSqlAlchemy(sessao)
            sessoes = RepositorioSessaoSqlAlchemy(sessao)
            casos = {
                "POST": CadastrarFormacaoAcademica(usuarios, formacoes, self.gerador),
                "PUT": EditarFormacaoAcademica(formacoes),
                "DELETE": ExcluirFormacaoAcademica(formacoes, self.relogio),
            }
            self.spies = {}
            for nome, caso in casos.items():
                self.spies[nome] = AsyncMock(wraps=caso.executar)
                caso.executar = self.spies[nome]
            app = create_app(
                autenticador_sessao=AutenticadorSessaoPersistida(sessoes),
                cadastrar_formacao_academica=None
                if ausente == "POST"
                else casos["POST"],
                editar_formacao_academica=None if ausente == "PUT" else casos["PUT"],
                excluir_formacao_academica=None
                if ausente == "DELETE"
                else casos["DELETE"],
            )
            caminho = "/formacoes-academicas" + (
                f"/{identidade}" if metodo != "POST" else ""
            )
            try:
                with patch(
                    "backend.infrastructure.security.autenticador_sessao.datetime"
                ) as tempo:
                    tempo.now.return_value = INSTANTE_T
                    resposta = await solicitar_asgi(
                        app,
                        metodo,
                        caminho,
                        dados=dados,
                        token=token,
                        query=query,
                        cabecalhos=cabecalhos,
                    )
                await sessao.commit()
                return resposta
            except Exception as erro:
                await sessao.rollback()
                raise AssertionError(
                    f"Falha integrada ({type(erro).__name__}); credenciais [REDACTED]"
                ) from None

    async def snapshot(self):
        """Relê todas as colunas de cinco tabelas em outra sessão independente.

        Ordena por PK e normaliza datetime para comparar inclusive tombstones;
        o chamador compara booleanos, sem imprimir hashes de conta ou sessão.
        """
        resultado = {}
        async with self.banco.sessoes() as sessao:
            for modelo in (
                FormacaoAcademicaRegistro,
                UsuarioRegistro,
                SessaoRegistro,
                CurriculoRegistro,
                CurriculoItemRegistro,
            ):
                tabela = modelo.__table__
                linhas = (
                    await sessao.execute(
                        select(tabela).order_by(*tabela.primary_key.columns)
                    )
                ).mappings()
                resultado[tabela.name] = tuple(
                    {nome: normalizar_utc(valor) for nome, valor in linha.items()}
                    for linha in linhas
                )
        return resultado

    async def ler_formacao(self, identidade=F):
        """Consulta a tabela bruta por ID em sessão nova, incluindo deleted_at.

        Dispensa o filtro ativo do agregado para detectar mutação ou purga que
        a leitura da porta poderia esconder após uma resposta negativa.
        """
        async with self.banco.sessoes() as sessao:
            linha = (
                (
                    await sessao.execute(
                        select(FormacaoAcademicaRegistro.__table__).where(
                            FormacaoAcademicaRegistro.id == identidade
                        )
                    )
                )
                .mappings()
                .one_or_none()
            )
        return (
            None
            if linha is None
            else {nome: normalizar_utc(valor) for nome, valor in linha.items()}
        )

    async def consultar(self, identidade, usuario, *, incluir_excluidas=False):
        """Lê a porta escopada em sessão nova usando o adapter real.

        Escolhe a variante ativa ou com tombstones para provar filtro no banco;
        esta leitura interna não representa GET, DTO HTTP ou autenticação.
        """
        async with self.banco.sessoes() as sessao:
            repo = RepositorioFormacaoAcademicaSqlAlchemy(sessao)
            consulta = (
                repo.obter_por_id_e_usuario_incluindo_excluidas
                if incluir_excluidas
                else repo.obter_por_id_e_usuario
            )
            return await consulta(FormacaoAcademicaId(identidade), UsuarioId(usuario))

    async def semear_referencia(self, usuario, formacao):
        """Grava currículo sintético e seleção de formação em transação própria.

        Preenche colunas obrigatórias e tipo polimórfico real, permitindo provar
        que DELETE de formação preserva as linhas sem alegar leitura histórica.
        """
        curriculo = CURRICULO_A if usuario == USUARIO_A else CURRICULO_B
        async with self.banco.sessoes() as sessao:
            sessao.add(
                CurriculoRegistro(
                    id=curriculo,
                    usuario_id=usuario,
                    titulo_versao="Versão sintética",
                    layout="classico",
                    is_public=False,
                )
            )
            await sessao.flush()
            sessao.add(
                CurriculoItemRegistro(
                    curriculo_id=curriculo,
                    tipo="formacao_academica",
                    item_id=formacao,
                )
            )
            await sessao.commit()

    async def invalidar_sessao(self, estado):
        """Expira ou revoga a sessão A diretamente no banco, sem espera real.

        Confirma o estado antes de tirar snapshot para separar a preparação
        intencional de qualquer efeito indevido da requisição recusada.
        """
        valores = (
            {"expira_em": INSTANTE_T}
            if estado == "expirada"
            else {"revogada_em": INSTANTE_T - timedelta(seconds=1)}
        )
        if estado not in {"expirada", "revogada"}:
            raise ValueError("Estado de sessão desconhecido")
        async with self.banco.sessoes() as sessao:
            await sessao.execute(
                update(SessaoRegistro)
                .where(
                    SessaoRegistro.token_hash == resumo_token(self.tokens[USUARIO_A])
                )
                .values(**valores)
            )
            await sessao.commit()
