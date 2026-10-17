"""Testa unitariamente o mapeamento e o repositório SQLAlchemy de certificações."""

import unittest
from pathlib import Path
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import CreateTable

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
from backend.application.cadastro_certificacao import CertificacaoJaCadastrada
from backend.domain import (
    Certificacao,
    CertificacaoId,
    RegraDeDominioViolada,
    UsuarioId,
)
from backend.infrastructure.identificadores.geradores import (
    GeradorCertificacaoIdUuid4,
)
from backend.infrastructure.persistence.sqlalchemy.certificacao import (
    CertificacaoRegistro,
    para_certificacao,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_certificacao import (
    RepositorioCertificacaoSqlAlchemy,
    _viola_chave_duplicidade,
)

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
ID_CERTIFICACAO = UUID("00000000-0000-0000-0000-0000000000c1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
def criar_certificacao() -> Certificacao:
    """Cria uma certificação determinística para os testes de fronteira ORM.

    A função usa identificadores fixos para comparar conversões e chamadas sem
    banco ou aleatoriedade. Ela existe para manter os cenários focados no
    comportamento observável do adapter.
    """
    return Certificacao(
        id=CertificacaoId(ID_CERTIFICACAO),
        usuario_id=UsuarioId(ID_USUARIO),
        nome="AWS Solutions Architect",
        organizacao_emissora="Amazon Web Services",
    )


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class MapeamentoCertificacaoTestCase(unittest.TestCase):
    """Verifica conversões puras entre certificação e seu modelo ORM.

    A classe cria registros somente em memória e compara seus valores
    persistíveis. Ela existe para proteger a fronteira sem abrir conexão ou
    depender de infraestrutura de banco.
    """

    def test_converte_entidade_para_registro_com_chaves_normalizadas(
        self,
    ) -> None:
        """Mantém as chaves canônicas e os campos exibíveis na conversão ao ORM.

        O cenário mapeia a entidade e compara os nomes serializados e as chaves
        calculadas. Ele existe para impedir que a persistência redefina a
        política de duplicidade aplicada no núcleo.
        """
        registro = para_registro(criar_certificacao())

        self.assertIsInstance(registro, CertificacaoRegistro)
        self.assertEqual(registro.id, ID_CERTIFICACAO)
        self.assertEqual(registro.usuario_id, ID_USUARIO)
        self.assertEqual(registro.nome, "AWS Solutions Architect")
        self.assertEqual(
            registro.nome_normalizado, "aws solutions architect"
        )
        self.assertEqual(registro.organizacao_emissora, "Amazon Web Services")
        self.assertEqual(
            registro.organizacao_emissora_normalizada, "amazon web services"
        )

    def test_reconstroi_entidade_a_partir_de_registro(self) -> None:
        """Reconstrói value objects a partir das colunas ORM.

        O cenário percorre ambos os mapeadores e compara a entidade resultante
        com a origem. Ele existe para evitar que dados instrumentados escapem
        para o domínio e para a Application.
        """
        self.assertEqual(
            para_certificacao(para_registro(criar_certificacao())),
            criar_certificacao(),
        )


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class RepositorioCertificacaoSqlAlchemyTestCase(
    unittest.IsolatedAsyncioTestCase
):
    """Verifica o adapter com sessão SQLAlchemy substituída por double.

    Os cenários observam query, add, flush e tradução de erro com mocks, sem
    iniciar banco ou transação real. A classe existe para testar a porta na sua
    fronteira unitária permitida.
    """

    async def test_consulta_chave_normalizada_por_usuario(self) -> None:
        """Retorna verdadeiro quando a sessão encontra uma chave equivalente.

        O teste configura apenas ``scalar`` no double e observa o resultado da
        consulta. Ele existe para assegurar que a prevenção prévia usa a chave
        composta normalizada.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = ID_CERTIFICACAO
        repositorio = RepositorioCertificacaoSqlAlchemy(session)

        existe = await repositorio.existe_por_chave_de_duplicidade(
            UsuarioId(ID_USUARIO),
            "aws solutions architect",
            "amazon web services",
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
        repositorio = RepositorioCertificacaoSqlAlchemy(session)

        await repositorio.salvar(criar_certificacao())

        registro = session.add.call_args.args[0]
        self.assertIsInstance(registro, CertificacaoRegistro)
        self.assertEqual(
            registro.nome_normalizado, "aws solutions architect"
        )
        self.assertEqual(
            registro.organizacao_emissora_normalizada, "amazon web services"
        )
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()

    async def test_traduz_violacao_da_constraint_de_duplicidade(self) -> None:
        """Converte somente a colisão nomeada em falha conhecida da Application.

        O double faz ``flush`` levantar ``IntegrityError`` contendo o nome da
        constraint de certificação. Ele existe para garantir a proteção contra
        corrida sem vazar SQL pela porta de persistência.
        """
        session = MagicMock(spec=AsyncSession)
        session.flush.side_effect = IntegrityError(
            statement=None,
            params=None,
            orig=RuntimeError(
                'constraint "uq_certificacoes_usuario_nome_emissor_normalizados"'
            ),
        )
        repositorio = RepositorioCertificacaoSqlAlchemy(session)

        with self.assertRaises(CertificacaoJaCadastrada):
            await repositorio.salvar(criar_certificacao())

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
        repositorio = RepositorioCertificacaoSqlAlchemy(session)

        with self.assertRaises(IntegrityError):
            await repositorio.salvar(criar_certificacao())


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class GeradorCertificacaoIdUuid4TestCase(unittest.TestCase):
    """Testa a geração de IDs de certificação com UUID4.

    A suíte executa o gerador e verifica se o value object retornado é válido.
    Ela existe para garantir a integridade do adapter de identificadores.
    """

    def test_gera_certificacao_id_com_uuid4(self) -> None:
        """Gera um CertificacaoId válido com formato UUID4.

        O cenário invoca o método gerar e valida o tipo e valor retornado. Ele
        existe para assegurar que a implementação concreta atende à porta.
        """
        gerador = GeradorCertificacaoIdUuid4()
        cert_id = gerador.gerar()

        self.assertIsInstance(cert_id, CertificacaoId)
        self.assertIsInstance(cert_id.valor, UUID)


NOME_CONSTRAINT_DUPLICIDADE = "uq_certificacoes_usuario_nome_emissor_normalizados"
MIGRATION_CERTIFICACOES = (
    Path(__file__).resolve().parents[1]
    / "infrastructure"
    / "persistence"
    / "alembic"
    / "versions"
    / "20261015_0010_criar_certificacoes.py"
)


class ConsultaDuplicidadeCertificacaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica os filtros e o resultado da consulta de duplicidade do adapter.

    A sessão substituída captura o SELECT gerado sem banco. A classe existe
    para garantir que a duplicidade seja procurada pelo dono e pela chave
    composta normalizada recebida.
    """

    async def test_select_filtra_dono_nome_e_emissor_normalizados(self) -> None:
        """Confere que a consulta usa os três campos da chave e seus valores.

        O teste inspeciona o SQL compilado e seus parâmetros. Ele existe para
        que a remoção do filtro de dono, que faria a duplicidade valer entre
        estudantes, seja detectada.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = ID_CERTIFICACAO
        repositorio = RepositorioCertificacaoSqlAlchemy(session)

        await repositorio.existe_por_chave_de_duplicidade(
            UsuarioId(ID_USUARIO), "aws solutions architect", "amazon web services"
        )

        consulta = session.scalar.await_args.args[0]
        sql = str(consulta)
        self.assertIn("certificacoes.usuario_id", sql)
        self.assertIn("certificacoes.nome_normalizado", sql)
        self.assertIn("certificacoes.organizacao_emissora_normalizada", sql)
        parametros = set(consulta.compile().params.values())
        self.assertTrue(
            {ID_USUARIO, "aws solutions architect", "amazon web services"} <= parametros
        )

    async def test_devolve_false_quando_nao_ha_registro(self) -> None:
        """Informa ausência quando a consulta não encontra certificação.

        A sessão devolve ``None`` como resultado escalar. O teste existe para
        cobrir o caminho que libera o cadastro de uma certificação nova.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = None
        repositorio = RepositorioCertificacaoSqlAlchemy(session)

        existe = await repositorio.existe_por_chave_de_duplicidade(
            UsuarioId(ID_USUARIO), "aws solutions architect", "amazon web services"
        )

        self.assertFalse(existe)


class EsquemaCertificacaoTestCase(unittest.TestCase):
    """Verifica a tabela de certificações declarada pelo ORM e pela migration.

    Os testes compilam a DDL sem conexão e comparam o nome da restrição única
    entre ORM, migration e adapter. A classe existe para que o conflito de
    duplicidade continue traduzido em resposta conhecida.
    """

    def test_colunas_obrigatorias_e_chave_estrangeira(self) -> None:
        """Confere colunas não nulas e a ligação do dono com usuários.

        O teste inspeciona a tabela mapeada. Ele existe para que nenhuma
        certificação seja persistida sem dono ou sem textos e chaves.
        """
        tabela = CertificacaoRegistro.__table__

        for coluna in (
            "id",
            "usuario_id",
            "nome",
            "nome_normalizado",
            "organizacao_emissora",
            "organizacao_emissora_normalizada",
        ):
            with self.subTest(coluna=coluna):
                self.assertFalse(tabela.c[coluna].nullable)
        chaves = {fk.target_fullname for fk in tabela.c.usuario_id.foreign_keys}
        self.assertEqual(chaves, {"usuarios.id"})

    def test_restricao_unica_cobre_dono_e_chave_composta(self) -> None:
        """Confere colunas e nome da restrição única do ORM.

        O teste localiza a restrição pelo nome usado pelo adapter e compara
        suas colunas. Ele existe para reforçar no banco a mesma regra de
        duplicidade aplicada pelo caso de uso.
        """
        restricoes = {
            restricao.name: [coluna.name for coluna in restricao.columns]
            for restricao in CertificacaoRegistro.__table__.constraints
            if isinstance(restricao, UniqueConstraint)
        }

        self.assertEqual(
            restricoes[NOME_CONSTRAINT_DUPLICIDADE],
            ["usuario_id", "nome_normalizado", "organizacao_emissora_normalizada"],
        )

    def test_nome_da_restricao_coincide_na_migration_e_no_adapter(self) -> None:
        """Garante o mesmo nome de restrição na migration e na tradução de erro.

        O teste lê a migration de criação da tabela e simula uma violação com o
        nome da restrição para o tradutor do adapter. Ele existe para que uma
        renomeação parcial não transforme o conflito 409 em erro inesperado.
        """
        migration = MIGRATION_CERTIFICACOES.read_text(encoding="utf-8")
        erro = IntegrityError("INSERT", {}, Exception(NOME_CONSTRAINT_DUPLICIDADE))

        self.assertIn(f'name="{NOME_CONSTRAINT_DUPLICIDADE}"', migration)
        self.assertTrue(_viola_chave_duplicidade(erro))

    def test_ddl_compila_em_postgresql_e_sqlite(self) -> None:
        """Confirma que a tabela gera DDL válida nos dois dialetos usados.

        O teste compila o CREATE TABLE sem executar e procura a restrição única
        e a chave estrangeira. Ele existe para validar a portabilidade entre o
        banco de produção e o SQLite das fixtures.
        """
        tabela = CertificacaoRegistro.__table__

        for dialeto in (postgresql.dialect(), sqlite.dialect()):
            with self.subTest(dialeto=dialeto.name):
                ddl = str(CreateTable(tabela).compile(dialect=dialeto))
                self.assertIn(NOME_CONSTRAINT_DUPLICIDADE, ddl)
                self.assertIn("fk_certificacoes_usuario_id_usuarios", ddl)


class CasosDeMapeamentoCertificacaoTestCase(unittest.TestCase):
    """Verifica casos de borda na conversão entre entidade e registro.

    Os cenários usam textos com espaços internos, acentos e registros
    inconsistentes. A classe existe para proteger a separação entre texto
    exibido e chave de comparação e a revalidação do domínio na leitura.
    """

    def test_texto_exibido_e_chave_sao_persistidos_separadamente(self) -> None:
        """Mantém o texto como digitado e grava a chave normalizada à parte.

        O teste converte uma certificação com espaços internos e acentos. Ele
        existe para que a apresentação preserve a escrita do estudante enquanto
        a duplicidade usa a forma canônica.
        """
        certificacao = Certificacao(
            id=CertificacaoId(ID_CERTIFICACAO),
            usuario_id=UsuarioId(ID_USUARIO),
            nome="Certificação   em Gestão",
            organizacao_emissora="Fundação   Exemplo",
        )

        registro = para_registro(certificacao)

        self.assertEqual(registro.nome, "Certificação   em Gestão")
        self.assertEqual(registro.nome_normalizado, "certificação em gestão")
        self.assertEqual(registro.organizacao_emissora, "Fundação   Exemplo")
        self.assertEqual(registro.organizacao_emissora_normalizada, "fundação exemplo")

    def test_leitura_recalcula_chaves_e_ignora_colunas_normalizadas(self) -> None:
        """Reconstrói a chave pela entidade, sem confiar no valor gravado.

        O registro traz colunas normalizadas divergentes do texto; a entidade
        lida deve expor chaves derivadas do próprio texto. O teste existe para
        que a política de normalização pertença apenas ao domínio.
        """
        registro = para_registro(criar_certificacao())
        registro.nome_normalizado = "valor-divergente"
        registro.organizacao_emissora_normalizada = "outro-valor"

        certificacao = para_certificacao(registro)

        self.assertEqual(certificacao.nome_normalizado, "aws solutions architect")
        self.assertEqual(
            certificacao.organizacao_emissora_normalizada, "amazon web services"
        )

    def test_registro_invalido_e_rejeitado_na_leitura(self) -> None:
        """Rejeita na leitura registros que violam as regras do domínio.

        O teste altera o nome do registro para vazio e para mais de 200
        caracteres antes de convertê-lo. Ele existe para impedir que dados
        corrompidos no banco virem entidades válidas.
        """
        for nome in ("   ", "A" * 201):
            with self.subTest(tamanho=len(nome)):
                registro = para_registro(criar_certificacao())
                registro.nome = nome

                with self.assertRaises(RegraDeDominioViolada):
                    para_certificacao(registro)
