"""Compõe casos e adapters reais sobre o SQLite migrado do harness de sessões.

Reutiliza BancoCredenciaisSessao, abre sessões curtas e oferece snapshots SQL
sem reconstruir agregados, para observar a persistência de interesse derivado.
"""

# Proveniência: decision-analysis prompts/backend/20261024-171508-integracao-associacao-candidatura-interesse-v001.md#v001

import ast
from collections import defaultdict
from contextlib import ExitStack
from pathlib import Path
from unittest import SkipTest
from unittest.mock import AsyncMock, patch
from uuid import UUID

from sqlalchemy import select

from backend.application.associacao_curriculo_vaga import (
    AdicionarClassificacaoAssociacaoCurriculoVaga,
    CriarAssociacaoCurriculoVaga,
    RemoverClassificacaoAssociacaoCurriculoVaga,
)
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.associacao_curriculo_vaga import (
    AssociacaoCurriculoVagaRegistro,
    ClassificacaoAssociacaoRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.curriculo import CurriculoRegistro
from backend.infrastructure.persistence.sqlalchemy.repositorio_associacao_curriculo_vaga import (
    RepositorioAssociacaoCurriculoVagaSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_curriculo import (
    RepositorioCurriculoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_sessao import (
    RepositorioSessaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.sessao import SessaoRegistro
from backend.infrastructure.security.autenticador_sessao import (
    AutenticadorSessaoPersistida,
)
from backend.infrastructure.security.tokens_sessao import CriadorSessaoSeguro
from backend.tests.fixtures.credenciais_sessao import (
    BancoCredenciaisSessao,
    resumo_token,
)

try:
    import aiosqlite
except ModuleNotFoundError as erro:
    if erro.name != "aiosqlite":
        raise
    AIOSQLITE_DISPONIVEL = False
else:
    AIOSQLITE_DISPONIVEL = aiosqlite is not None

MOTIVO_SEM_AIOSQLITE = "aiosqlite ausente; execute com nix develop .#tests"
MIGRATIONS = Path(__file__).resolve().parents[2] / "infrastructure/persistence/alembic/versions"
A1, A2, B1, AUSENTE = (UUID(int=n) for n in (201, 203, 202, 299))
VAGA01, VAGA02 = "vaga-integracao-01", "vaga-integracao-02"


# Proveniência: decision-analysis prompts/backend/20261025-201917-teste-associacao-curriculo-vaga-candidatura-interesse-v001.md#v001
def verificar_grafo() -> str:
    """Inspeciona IDs e arestas por AST antes de criar o banco descartável.

    Valida referências e ordenação topológica antes de classificar duplicatas
    e múltiplas heads como bloqueios explícitos do ambiente. Não captura erros
    de parsing, referências, ciclos ou execução de migrations, para impedir que
    uma falha real seja confundida com teste de negócio aprovado ou ignorado.
    """
    arquivos = defaultdict(set)
    pais = defaultdict(set)
    for caminho in sorted(MIGRATIONS.glob("*.py")):
        valores = {}
        for no in ast.parse(caminho.read_text(encoding="utf-8")).body:
            if isinstance(no, ast.Assign):
                alvos = no.targets
            elif isinstance(no, ast.AnnAssign):
                alvos = [no.target]
            else:
                continue
            for alvo in alvos:
                if isinstance(alvo, ast.Name) and alvo.id in {"revision", "down_revision"}:
                    valores[alvo.id] = ast.literal_eval(no.value)
        if not valores:
            continue
        revisao = valores["revision"]
        anterior = valores["down_revision"]
        if not isinstance(revisao, str):
            raise AssertionError(f"revision inválida: {caminho.name}")
        predecessores = () if anterior is None else (
            (anterior,) if isinstance(anterior, str) else anterior
        )
        if not isinstance(predecessores, tuple) or not all(
            isinstance(pai, str) for pai in predecessores
        ):
            raise AssertionError(f"down_revision inválida: {caminho.name}")
        arquivos[revisao].add(caminho.name)
        pais[revisao].update(predecessores)
    if not arquivos:
        raise AssertionError("Nenhuma revisão Alembic encontrada")
    referencias = set().union(*pais.values())
    if referencias - arquivos.keys():
        raise AssertionError(f"Predecessores ausentes: {sorted(referencias - arquivos.keys())}")
    visitados = set()
    while len(visitados) < len(arquivos):
        livres = {r for r in arquivos if r not in visitados and pais[r] <= visitados}
        if not livres:
            raise AssertionError(f"Ciclo Alembic: {sorted(arquivos.keys() - visitados)}")
        visitados.update(livres)
    duplicadas = {r: nomes for r, nomes in arquivos.items() if len(nomes) > 1}
    heads = arquivos.keys() - referencias
    if duplicadas or len(heads) > 1:
        detalhes = "; ".join(
            f"{r}: {', '.join(sorted(duplicadas[r]))}" for r in sorted(duplicadas)
        )
        terminais = "; ".join(
            f"{r}: {', '.join(sorted(arquivos[r]))}" for r in sorted(heads)
        )
        raise SkipTest(
            f"Grafo Alembic original bloqueado; duplicatas [{detalhes}]; "
            f"heads declaradas [{terminais}]; não comprova negócio"
        )
    return next(iter(heads))


class OperacaoObservada:
    """Observa métodos reais de casos e adapters sem substituir seus resultados.

    Instala AsyncMock com wraps em instâncias locais à sessão, permitindo provar
    a ordem das guardas e ausência de escrita sem simular SQL ou domínio.
    """

    def __init__(self, sessao) -> None:
        """Compõe repositórios e casos na sessão recebida para observar fronteiras.

        Retém uma ExitStack e spies delegantes, deixando transação e fechamento
        ao chamador para que cada operação use banco real e cleanup explícito.
        """
        self.patches = ExitStack()
        self.curriculos = RepositorioCurriculoSqlAlchemy(sessao)
        self.associacoes = RepositorioAssociacaoCurriculoVagaSqlAlchemy(sessao)
        self.spies = {}
        for nome in ("existe_por_par", "obter_para_atualizacao", "salvar", "atualizar_classificacoes"):
            self.spies[nome] = self.patches.enter_context(patch.object(
                self.associacoes, nome, new=AsyncMock(wraps=getattr(self.associacoes, nome)),
            ))
        self.spies["curriculo"] = self.patches.enter_context(patch.object(
            self.curriculos, "obter_por_id", new=AsyncMock(wraps=self.curriculos.obter_por_id),
        ))
        self.casos = {}
        for nome, tipo in (
            ("criar", CriarAssociacaoCurriculoVaga),
            ("adicionar", AdicionarClassificacaoAssociacaoCurriculoVaga),
            ("remover", RemoverClassificacaoAssociacaoCurriculoVaga),
        ):
            caso = tipo(self.curriculos, self.associacoes)
            self.casos[nome] = self.patches.enter_context(patch.object(
                caso, "executar", new=AsyncMock(wraps=caso.executar),
            ))

    def fechar(self) -> None:
        """Restaura métodos observados pela ExitStack para liberar os patches locais.

        Executa o cleanup mesmo após exceção do caso, evitando vazamento de
        observadores entre operações independentes do mesmo cenário.
        """
        self.patches.close()


class BancoAssociacoes:
    """Prepara contas e currículos sobre o harness migrado já existente.

    Encapsula sessões curtas, autenticação persistida e leitura bruta para que
    o teste prove integração de componentes sem compor HTTP ou produção.
    """

    def __init__(self) -> None:
        """Reserva o harness de credenciais após o preflight feito pelo chamador.

        Não abre engine; expõe cleanup imediato para registrá-lo antes do preparo
        e garantir descarte mesmo quando a migração ou a semeadura falhar.
        """
        self.base = BancoCredenciaisSessao()

    async def preparar(self, usuario_a, usuario_b, *, incluir_ausente=False) -> None:
        """Migra SQLite e semeia currículos sintéticos depois das duas contas.

        Usa commit externo e opcionalmente UUID 299 para o controle de ausência,
        preservando a única diferença de preparo entre controle e negativa N03.
        """
        await self.base.preparar()
        schema = await self.base.inspecionar_schema()
        if schema["versoes"] != (self.base.head,):
            raise AssertionError("Banco não está na head aplicada pelo harness")
        async with self.base.sessoes() as sessao:
            dados = [(A1, usuario_a), (A2, usuario_a), (B1, usuario_b)]
            if incluir_ausente:
                dados.append((AUSENTE, usuario_a))
            sessao.add_all([
                CurriculoRegistro(id=identidade, usuario_id=usuario,
                                  titulo_versao="Versão sintética de integração",
                                  layout="simples", is_public=False)
                for identidade, usuario in dados
            ])
            await sessao.commit()

    async def identidade(self, usuario: UUID) -> UsuarioId:
        """Emite sessão real e autentica seu token em outra sessão de banco.

        Confirma a linha pelo hash sem imprimi-lo e usa o autenticador persistido,
        para fornecer ao caso interno uma identidade validada sem alegar HTTP.
        """
        async with self.base.sessoes() as sessao:
            token = await CriadorSessaoSeguro(RepositorioSessaoSqlAlchemy(sessao)).criar(
                UsuarioId(usuario),
            )
            await sessao.commit()
        async with self.base.sessoes() as sessao:
            linha = (await sessao.scalars(select(SessaoRegistro).where(
                SessaoRegistro.token_hash == resumo_token(token),
            ))).one()
            if linha.usuario_id != usuario:
                raise AssertionError("Sessão emitida para identidade incorreta")
            autenticado = await AutenticadorSessaoPersistida(
                RepositorioSessaoSqlAlchemy(sessao),
            ).autenticar(token)
            if autenticado is None or autenticado.valor != usuario:
                raise AssertionError("Sessão persistida não autenticou o proprietário")
            return autenticado

    async def snapshot(self) -> dict:
        """Relê todas as colunas das três tabelas por sessão nova e SQL bruto.

        Ordena pela chave e não chama mapeadores de agregado, para que interesse
        ausente no banco não seja recomposto e escondido pelo normalizador.
        """
        tabelas = {
            "raizes": AssociacaoCurriculoVagaRegistro.__table__,
            "classes": ClassificacaoAssociacaoRegistro.__table__,
            "curriculos": CurriculoRegistro.__table__,
        }
        async with self.base.sessoes() as sessao:
            resultado = {}
            for nome, tabela in tabelas.items():
                resultado[nome] = tuple((await sessao.execute(
                    select(tabela).order_by(*tabela.primary_key.columns),
                )).tuples().all())
        return resultado

    async def fechar(self) -> None:
        """Descarta a engine antes do diretório pelo cleanup do harness existente.

        Delega a liberação em finally já implementada na base, para garantir
        isolamento mesmo quando preparar ou uma asserção não conclui.
        """
        await self.base.fechar()
