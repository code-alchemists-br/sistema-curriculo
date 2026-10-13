"""Verifica formato e persistência do token criado para uma sessão."""

import hashlib
import unittest
from datetime import timedelta
from importlib import import_module
from unittest.mock import patch
from uuid import UUID

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKeyConstraint,
    String,
    UniqueConstraint,
    Uuid,
)

from backend.application.sessoes import RepositorioSessao
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.metadata import metadata
from backend.infrastructure.persistence.sqlalchemy.repositorio_sessao import (
    RepositorioSessaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.sessao import SessaoRegistro
from backend.infrastructure.security.tokens_sessao import (
    CriadorSessaoSeguro,
    RevogadorSessaoSeguro,
)


class RepositorioSessaoStub(RepositorioSessao):
    """Captura os metadados enviados pelo emissor sem usar banco.

    O double guarda em memória os valores recebidos e nunca precisa do token em
    claro. Ele existe para testar o limite entre segurança e persistência.
    """

    def __init__(self) -> None:
        """Inicializa o histórico de sessões capturadas.

        O construtor não abre recursos externos. Ele existe para tornar a
        persistência chamada pelo emissor observável.
        """
        self.sessoes = []
        self.revogacoes = []

    async def salvar(self, usuario_id, token_hash, criada_em, expira_em) -> None:
        """Armazena a identidade, hash e validade recebidos.

        O método simula uma porta assíncrona sem banco e não recebe token
        original. Ele existe para validar o conteúdo persistido.
        """
        self.sessoes.append((usuario_id, token_hash, criada_em, expira_em))

    async def revogar_por_hash(self, token_hash, revogada_em) -> None:
        """Registra os argumentos recebidos para revogar uma sessão.

        O double mantém a chamada em memória, sem interpretar o token ou
        consultar banco. Ele existe para isolar o adapter de hash.
        """
        self.revogacoes.append((token_hash, revogada_em))


class CriadorSessaoSeguroTestCase(unittest.IsolatedAsyncioTestCase):
    """Protege a entropia do token e o armazenamento exclusivo de seu hash."""

    async def test_gera_token_opaco_e_salva_hash_sha256_com_prazo_de_oito_horas(self) -> None:
        """Confirma token URL-safe, resumo persistido e validade de oito horas.

        O teste controla apenas o repositório e usa os campos observados para
        calcular as garantias. Ele existe para prevenir armazenamento do segredo.
        """
        repositorio = RepositorioSessaoStub()
        usuario_id = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))

        token = await CriadorSessaoSeguro(repositorio).criar(usuario_id)

        self.assertEqual(len(token), 43)
        self.assertNotIn("=", token)
        self.assertEqual(len(repositorio.sessoes), 1)
        identidade, resumo, criada_em, expira_em = repositorio.sessoes[0]
        self.assertEqual(identidade, usuario_id)
        self.assertEqual(resumo, hashlib.sha256(token.encode("ascii")).hexdigest())
        self.assertNotEqual(resumo, token)
        self.assertIsNotNone(criada_em.tzinfo)
        self.assertEqual(expira_em - criada_em, timedelta(hours=8))


class RevogadorSessaoSeguroTestCase(unittest.IsolatedAsyncioTestCase):
    """Protege o resumo e o instante enviados pelo adapter de revogação."""

    async def test_revoga_com_hash_sha256_e_data_utc_sem_repassar_token(self) -> None:
        """Confirma que a porta recebe somente o hash do token apresentado.

        O repositório em memória observa argumentos e não persiste credencial.
        O teste existe para impedir que o segredo em claro atravesse a fronteira.
        """
        repositorio = RepositorioSessaoStub()
        token = "credencial-de-sessao"

        await RevogadorSessaoSeguro(repositorio).revogar(token)

        resumo, revogada_em = repositorio.revogacoes[0]
        self.assertEqual(resumo, hashlib.sha256(token.encode("utf-8")).hexdigest())
        self.assertNotEqual(resumo, token)
        self.assertIsNotNone(revogada_em.tzinfo)
        self.assertEqual(revogada_em.utcoffset().total_seconds(), 0)

    async def test_token_unicode_e_processado_sem_erro(self) -> None:
        """Trata entrada Unicode malformada como hash opaco desconhecido.

        A codificação UTF-8 permite resumir qualquer valor recebido, sem
        registrar o segredo. O teste existe para evitar erro interno no logout.
        """
        repositorio = RepositorioSessaoStub()
        token = "token-inválido"

        await RevogadorSessaoSeguro(repositorio).revogar(token)

        self.assertEqual(
            repositorio.revogacoes[0][0],
            hashlib.sha256(token.encode("utf-8")).hexdigest(),
        )


class AsyncSessionDouble:
    """Registra linhas adicionadas e chamadas de flush sem SQLAlchemy I/O.

    O double imita apenas as duas operações usadas pelo repositório. Ele existe
    para testar o adapter sem banco ou transação real.
    """

    def __init__(self) -> None:
        """Prepara lista de linhas e contador de flush.

        O estado local é observável e não inicia conexão. Ele existe para
        confirmar o comportamento do adapter de persistência.
        """
        self.registros = []
        self.flush_count = 0
        self.comandos = []

    def add(self, registro) -> None:
        """Guarda a linha que o repositório solicitou inserir.

        A chamada é síncrona como na AsyncSession. Ela existe para inspecionar
        os campos mapeados pelo adapter.
        """
        self.registros.append(registro)

    async def flush(self) -> None:
        """Conta o flush solicitado sem acessar armazenamento.

        A operação assíncrona não executa SQL. Ela existe para confirmar que o
        repositório envia a linha antes de retornar.
        """
        self.flush_count += 1

    async def execute(self, comando) -> None:
        """Captura o comando SQL solicitado pelo adapter sem executá-lo.

        O double registra a expressão em memória. Ele existe para verificar as
        condições da atualização sem banco ou transação real.
        """
        self.comandos.append(comando)


class RepositorioSessaoSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica conversão e inserção de metadados pelo adapter SQLAlchemy."""

    async def test_insere_hash_e_validade_sem_token_em_claro(self) -> None:
        """Cria linha com associação de conta e aguarda flush sem commit.

        O adapter recebe dados de teste e a sessão double captura a linha. O
        teste existe para proteger os campos persistidos e o limite transacional.
        """
        from datetime import datetime, timedelta, timezone

        session = AsyncSessionDouble()
        usuario_id = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))
        criada_em = datetime.now(timezone.utc)
        token_hash = "a" * 64

        await RepositorioSessaoSqlAlchemy(session).salvar(
            usuario_id, token_hash, criada_em, criada_em + timedelta(hours=8)
        )

        self.assertEqual(session.flush_count, 1)
        self.assertEqual(len(session.registros), 1)
        registro = session.registros[0]
        self.assertIsInstance(registro, SessaoRegistro)
        self.assertEqual(registro.usuario_id, usuario_id.valor)
        self.assertEqual(registro.token_hash, token_hash)
        self.assertEqual(registro.criada_em, criada_em)
        self.assertNotEqual(registro.token_hash, "token-em-claro")

    async def test_revoga_apenas_hash_ativo_e_aguarda_flush_sem_commit(self) -> None:
        """Gera update condicionado ao hash e à ausência de revogação.

        A sessão double captura a expressão SQL e o flush, sem banco real. O
        teste existe para proteger idempotência e escopo por sessão.
        """
        from datetime import datetime, timezone

        session = AsyncSessionDouble()
        revogada_em = datetime.now(timezone.utc)

        await RepositorioSessaoSqlAlchemy(session).revogar_por_hash("a" * 64, revogada_em)

        self.assertEqual(session.flush_count, 1)
        self.assertEqual(len(session.comandos), 1)
        comando = session.comandos[0]
        compilado = comando.compile()
        self.assertEqual(compilado.params["token_hash_1"], "a" * 64)
        self.assertIn("token_hash", str(compilado))
        self.assertIn("revogada_em IS NULL", str(compilado))
        self.assertEqual(compilado.params["revogada_em"], revogada_em)


class SessaoMappingTestCase(unittest.TestCase):
    """Protege o mapeamento Code First e a migration da tabela de sessões."""

    def test_metadata_registra_hash_unico_e_chave_para_usuario(self) -> None:
        """Confirma campos, constraints e tipos da tabela ORM.

        A inspeção ocorre sobre metadata em memória e não abre banco. Ela existe
        para manter o mapeamento alinhado ao contrato de sessão.
        """
        tabela = metadata.tables["sessoes"]
        self.assertIs(tabela, SessaoRegistro.__table__)
        self.assertEqual(
            list(tabela.columns.keys()),
            ["id", "usuario_id", "token_hash", "criada_em", "expira_em", "revogada_em"],
        )
        self.assertIsInstance(tabela.c.id.type, Uuid)
        self.assertIsInstance(tabela.c.usuario_id.type, Uuid)
        self.assertIsInstance(tabela.c.token_hash.type, String)
        self.assertIsInstance(tabela.c.criada_em.type, DateTime)
        self.assertIsInstance(tabela.c.expira_em.type, DateTime)
        unicas = [constraint for constraint in tabela.constraints if isinstance(constraint, UniqueConstraint)]
        self.assertEqual(len(unicas), 1)
        self.assertEqual(list(unicas[0].columns.keys()), ["token_hash"])
        chaves = [constraint for constraint in tabela.constraints if isinstance(constraint, ForeignKeyConstraint)]
        self.assertEqual(len(chaves), 1)
        self.assertEqual([element.target_fullname for element in chaves[0].elements], ["usuarios.id"])

    def test_migration_cria_e_remove_tabela_de_sessoes(self) -> None:
        """Compara migration e metadata sem executar DDL real.

        O teste substitui operações Alembic e compara colunas/chaves capturadas.
        Ele existe para detectar divergência entre modelo e schema versionado.
        """
        migration = import_module(
            "backend.infrastructure.persistence.alembic.versions.20261012_0004_criar_sessoes"
        )
        anterior = import_module(
            "backend.infrastructure.persistence.alembic.versions.20261007_0003_criar_curriculo_itens"
        )
        self.assertEqual(migration.down_revision, anterior.revision)
        with patch.object(migration, "op") as operacoes:
            migration.upgrade()
            operacoes.create_table.assert_called_once()
            nome, *elementos = operacoes.create_table.call_args.args
            self.assertEqual(nome, "sessoes")
            colunas = [elemento for elemento in elementos if isinstance(elemento, Column)]
            self.assertEqual([coluna.name for coluna in colunas], list(metadata.tables[nome].columns.keys()))
            for coluna in colunas:
                self.assertEqual(type(coluna.type), type(metadata.tables[nome].c[coluna.name].type))
                self.assertEqual(coluna.nullable, metadata.tables[nome].c[coluna.name].nullable)
            migration.downgrade()
            operacoes.drop_table.assert_called_once_with("sessoes")
