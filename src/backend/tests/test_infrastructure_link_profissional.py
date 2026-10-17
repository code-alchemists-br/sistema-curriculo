"""Testa unitariamente o mapeamento e o repositório SQLAlchemy de links profissionais."""

import unittest
from pathlib import Path
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import CreateTable

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.application.cadastro_link_profissional import (
    LinkProfissionalJaCadastrado,
)
from backend.domain import (
    LinkProfissional,
    LinkProfissionalId,
    RegraDeDominioViolada,
    UsuarioId,
)
from backend.infrastructure.identificadores.geradores import (
    GeradorLinkProfissionalIdUuid4,
)
from backend.infrastructure.persistence.sqlalchemy.link_profissional import (
    LinkProfissionalRegistro,
    para_link_profissional,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_link_profissional import (
    RepositorioLinkProfissionalSqlAlchemy,
    _viola_chave_duplicidade,
)

ID_LINK = UUID("00000000-0000-0000-0000-0000000000a1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def criar_link() -> LinkProfissional:
    """Cria um link profissional determinístico para os testes de fronteira ORM.

    A função usa identificadores fixos para comparar conversões e chamadas sem
    banco ou aleatoriedade. Ela existe para manter os cenários focados no
    comportamento observável do adapter.
    """
    return LinkProfissional(
        id=LinkProfissionalId(ID_LINK),
        usuario_id=UsuarioId(ID_USUARIO),
        rotulo="GitHub Perfil",
        url="https://github.com/usuario",
    )


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class MapeamentoLinkProfissionalTestCase(unittest.TestCase):
    """Verifica conversões puras entre link profissional e seu modelo ORM.

    A classe cria registros somente em memória e compara seus valores
    persistíveis. Ela existe para proteger a fronteira sem abrir conexão ou
    depender de infraestrutura de banco.
    """

    def test_converte_entidade_para_registro_com_chaves_normalizadas(self) -> None:
        """Mantém as chaves canônicas e os campos na conversão ao ORM.

        O cenário mapeia a entidade e compara os dados serializados e as chaves
        calculadas. Ele existe para impedir que a persistência redefina a política
        de duplicidade aplicada no núcleo.
        """
        registro = para_registro(criar_link())

        self.assertIsInstance(registro, LinkProfissionalRegistro)
        self.assertEqual(registro.id, ID_LINK)
        self.assertEqual(registro.usuario_id, ID_USUARIO)
        self.assertEqual(registro.rotulo, "GitHub Perfil")
        self.assertEqual(registro.url, "https://github.com/usuario")
        self.assertEqual(registro.url_normalizada, "https://github.com/usuario")

    def test_reconstroi_entidade_a_partir_de_registro(self) -> None:
        """Reconstrói value objects a partir das colunas ORM.

        O cenário percorre ambos os mapeadores e compara a entidade resultante
        com a origem. Ele existe para evitar que dados instrumentados escapem
        para domínio e Application.
        """
        self.assertEqual(
            para_link_profissional(para_registro(criar_link())), criar_link()
        )


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class RepositorioLinkProfissionalSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o adapter com sessão SQLAlchemy substituída por double.

    Os cenários observam query, add, flush e tradução de erro com mocks, sem
    iniciar banco ou transação real. A classe existe para testar a porta na sua
    fronteira unitária permitida.
    """

    async def test_consulta_chave_normalizada_por_usuario(self) -> None:
        """Retorna verdadeiro quando a sessão encontra uma chave equivalente.

        O teste configura apenas ``scalar`` no double e observa o resultado da
        consulta. Ele existe para assegurar que a prevenção prévia usa a chave
        técnica url_normalizada.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = ID_LINK
        repositorio = RepositorioLinkProfissionalSqlAlchemy(session)

        existe = await repositorio.existe_por_chave_de_duplicidade(
            UsuarioId(ID_USUARIO), "https://github.com/usuario"
        )

        self.assertTrue(existe)
        session.scalar.assert_awaited_once()

    async def test_adiciona_registro_e_aguarda_flush_sem_commit(self) -> None:
        """Envia registro mapeado à sessão sem finalizar a transação.

        O cenário usa uma sessão mockada e examina o registro entregue a
        ``add``. Ele existe para preservar a responsabilidade transacional da
        composição externa.
        """
        session = MagicMock(spec=AsyncSession)
        repositorio = RepositorioLinkProfissionalSqlAlchemy(session)

        await repositorio.salvar(criar_link())

        registro = session.add.call_args.args[0]
        self.assertIsInstance(registro, LinkProfissionalRegistro)
        self.assertEqual(registro.url_normalizada, "https://github.com/usuario")
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()

    async def test_traduz_violacao_da_constraint_de_duplicidade(self) -> None:
        """Converte somente a colisão nomeada em falha conhecida da Application.

        O double faz ``flush`` levantar ``IntegrityError`` contendo o nome da
        constraint uq_links_profissionais_usuario_url_normalizada. Ele existe para
        garantir a proteção contra corrida sem vazar SQL pela porta de persistência.
        """
        session = MagicMock(spec=AsyncSession)
        session.flush.side_effect = IntegrityError(
            statement=None,
            params=None,
            orig=RuntimeError(
                'constraint "uq_links_profissionais_usuario_url_normalizada"'
            ),
        )
        repositorio = RepositorioLinkProfissionalSqlAlchemy(session)

        with self.assertRaises(LinkProfissionalJaCadastrado):
            await repositorio.salvar(criar_link())

    async def test_propaga_outros_erros_de_integridade(self) -> None:
        """Propaga erros de integridade não relacionados à constraint de duplicidade.

        O cenário simula uma falha externa qualquer, como chave estrangeira, e
        verifica que a exceção original é repassada. Ele existe para evitar
        mascarar problemas de banco inesperados como duplicidades.
        """
        session = MagicMock(spec=AsyncSession)
        session.flush.side_effect = IntegrityError(
            statement=None,
            params=None,
            orig=RuntimeError('foreign key "fk_outra"'),
        )
        repositorio = RepositorioLinkProfissionalSqlAlchemy(session)

        with self.assertRaises(IntegrityError):
            await repositorio.salvar(criar_link())


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class GeradorLinkProfissionalIdUuid4TestCase(unittest.TestCase):
    """Testa a geração de IDs de link profissional com UUID4.

    A suíte executa o gerador e verifica se o value object retornado é válido.
    Ela existe para garantir a integridade do adapter de identificadores.
    """

    def test_gera_link_profissional_id_com_uuid4(self) -> None:
        """Gera um LinkProfissionalId válido com formato UUID4.

        O cenário invoca o método gerar e valida o tipo e valor retornado. Ele
        existe para assegurar que a implementação concreta atende à porta.
        """
        gerador = GeradorLinkProfissionalIdUuid4()
        link_id = gerador.gerar()

        self.assertIsInstance(link_id, LinkProfissionalId)
        self.assertIsInstance(link_id.valor, UUID)


NOME_CONSTRAINT_DUPLICIDADE = "uq_links_profissionais_usuario_url_normalizada"
MIGRATION_LINKS = (
    Path(__file__).resolve().parents[1]
    / "infrastructure"
    / "persistence"
    / "alembic"
    / "versions"
    / "20261015_0012_criar_links_profissionais.py"
)


class ConsultaDuplicidadeLinkTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica os filtros e o resultado da consulta de duplicidade do adapter.

    A sessão substituída captura o SELECT gerado sem banco. A classe existe
    para garantir que a duplicidade seja procurada pelo dono e pela URL
    normalizada recebida.
    """

    async def test_select_filtra_dono_e_url_normalizada(self) -> None:
        """Confere que a consulta usa dono e URL normalizada com seus valores.

        O teste inspeciona o SQL compilado e seus parâmetros. Ele existe para
        que a remoção do filtro de dono, que faria a duplicidade valer entre
        estudantes, seja detectada.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = ID_LINK
        repositorio = RepositorioLinkProfissionalSqlAlchemy(session)

        await repositorio.existe_por_chave_de_duplicidade(
            UsuarioId(ID_USUARIO), "https://github.com/usuario"
        )

        consulta = session.scalar.await_args.args[0]
        sql = str(consulta)
        self.assertIn("links_profissionais.usuario_id", sql)
        self.assertIn("links_profissionais.url_normalizada", sql)
        parametros = set(consulta.compile().params.values())
        self.assertTrue({ID_USUARIO, "https://github.com/usuario"} <= parametros)

    async def test_devolve_false_quando_nao_ha_registro(self) -> None:
        """Informa ausência quando a consulta não encontra link.

        A sessão devolve ``None`` como resultado escalar. O teste existe para
        cobrir o caminho que libera o cadastro de um link novo.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = None
        repositorio = RepositorioLinkProfissionalSqlAlchemy(session)

        existe = await repositorio.existe_por_chave_de_duplicidade(
            UsuarioId(ID_USUARIO), "https://github.com/usuario"
        )

        self.assertFalse(existe)


class EsquemaLinkProfissionalTestCase(unittest.TestCase):
    """Verifica a tabela de links declarada pelo ORM e pela migration.

    Os testes compilam a DDL sem conexão e comparam o nome da restrição única
    entre ORM, migration e adapter. A classe existe para que o conflito de
    duplicidade continue traduzido em resposta conhecida.
    """

    def test_colunas_obrigatorias_e_chave_estrangeira(self) -> None:
        """Confere colunas não nulas e a ligação do dono com usuários.

        O teste inspeciona a tabela mapeada. Ele existe para que nenhum link
        seja persistido sem dono, rótulo, URL ou chave.
        """
        tabela = LinkProfissionalRegistro.__table__

        for coluna in ("id", "usuario_id", "rotulo", "url", "url_normalizada"):
            with self.subTest(coluna=coluna):
                self.assertFalse(tabela.c[coluna].nullable)
        chaves = {fk.target_fullname for fk in tabela.c.usuario_id.foreign_keys}
        self.assertEqual(chaves, {"usuarios.id"})

    def test_restricao_unica_cobre_dono_e_url_normalizada(self) -> None:
        """Confere colunas e nome da restrição única do ORM.

        O teste localiza a restrição pelo nome usado pelo adapter e compara
        suas colunas. Ele existe para reforçar no banco a mesma duplicidade por
        usuário aplicada pelo caso de uso.
        """
        restricoes = {
            restricao.name: [coluna.name for coluna in restricao.columns]
            for restricao in LinkProfissionalRegistro.__table__.constraints
            if isinstance(restricao, UniqueConstraint)
        }

        self.assertEqual(
            restricoes[NOME_CONSTRAINT_DUPLICIDADE], ["usuario_id", "url_normalizada"]
        )

    def test_nome_da_restricao_coincide_na_migration_e_no_adapter(self) -> None:
        """Garante o mesmo nome de restrição na migration e na tradução de erro.

        O teste lê a migration de criação da tabela e simula uma violação com o
        nome da restrição para o tradutor do adapter. Ele existe para que uma
        renomeação parcial não transforme o conflito 409 em erro inesperado.
        """
        migration = MIGRATION_LINKS.read_text(encoding="utf-8")
        erro = IntegrityError("INSERT", {}, Exception(NOME_CONSTRAINT_DUPLICIDADE))

        self.assertIn(f'name="{NOME_CONSTRAINT_DUPLICIDADE}"', migration)
        self.assertTrue(_viola_chave_duplicidade(erro))

    def test_ddl_compila_em_postgresql_e_sqlite(self) -> None:
        """Confirma que a tabela gera DDL válida nos dois dialetos usados.

        O teste compila o CREATE TABLE sem executar e procura a restrição única
        e a chave estrangeira. Ele existe para validar a portabilidade entre o
        banco de produção e o SQLite das fixtures.
        """
        tabela = LinkProfissionalRegistro.__table__

        for dialeto in (postgresql.dialect(), sqlite.dialect()):
            with self.subTest(dialeto=dialeto.name):
                ddl = str(CreateTable(tabela).compile(dialect=dialeto))
                self.assertIn(NOME_CONSTRAINT_DUPLICIDADE, ddl)
                self.assertIn("fk_links_profissionais_usuario_id_usuarios", ddl)


class CasosDeMapeamentoLinkTestCase(unittest.TestCase):
    """Verifica casos de borda na conversão entre link e registro.

    Os cenários usam URLs com caixa mista, chaves divergentes no banco e
    registros inválidos. A classe existe para proteger a separação entre URL
    exibida e chave de comparação e a revalidação do domínio na leitura.
    """

    def test_url_exibida_e_chave_sao_persistidas_separadamente(self) -> None:
        """Mantém a URL como informada e grava a chave normalizada à parte.

        O teste converte um link com host em maiúsculas e barra final. Ele
        existe para que o currículo mostre o endereço do estudante enquanto a
        duplicidade usa a forma canônica.
        """
        link = LinkProfissional(
            id=LinkProfissionalId(ID_LINK),
            usuario_id=UsuarioId(ID_USUARIO),
            rotulo="GitHub",
            url="https://GitHub.com/Usuario/",
        )

        registro = para_registro(link)

        self.assertEqual(registro.url, "https://GitHub.com/Usuario/")
        self.assertEqual(registro.url_normalizada, "https://github.com/Usuario")

    def test_leitura_recalcula_chave_e_ignora_coluna_normalizada(self) -> None:
        """Reconstrói a chave pela entidade, sem confiar no valor gravado.

        O registro traz uma URL normalizada divergente; a entidade lida deve
        expor a chave derivada da própria URL. O teste existe para que a
        política de normalização pertença apenas ao domínio.
        """
        registro = para_registro(criar_link())
        registro.url_normalizada = "valor-divergente"

        link = para_link_profissional(registro)

        self.assertEqual(link.url_normalizada, "https://github.com/usuario")

    def test_registro_invalido_e_rejeitado_na_leitura(self) -> None:
        """Rejeita na leitura registros com URL insegura ou sem destino.

        O teste altera a URL do registro para formas que violam as regras do
        domínio antes de convertê-lo. Ele existe para impedir que dados
        corrompidos no banco virem entidades válidas.
        """
        for url in ("https://user:senha@site.com", "javascript:alert(1)", "http://:80"):
            with self.subTest(url=url):
                registro = para_registro(criar_link())
                registro.url = url

                with self.assertRaises(RegraDeDominioViolada):
                    para_link_profissional(registro)
