"""Testa unitariamente o mapeamento e repositório de projeto acadêmico."""

import unittest
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    ForeignKeyConstraint,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import CreateTable

# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
from backend.domain import ProjetoAcademico, ProjetoAcademicoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.projeto_academico import (
    ProjetoAcademicoRegistro,
    para_projeto_academico,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_projeto_academico import (
    RepositorioProjetoAcademicoSQLAlchemy,
)

# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
ID_PROJETO = UUID("00000000-0000-0000-0000-0000000000f1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
def criar_projeto() -> ProjetoAcademico:
    """Cria entidade determinística para os testes de persistência.

    A função usa IDs fixos e textos válidos sem conectar a banco. Ela existe
    para comparar conversões e chamadas do repositório.
    """
    return ProjetoAcademico(
        id=ProjetoAcademicoId(ID_PROJETO),
        usuario_id=UsuarioId(ID_USUARIO),
        titulo="Projeto Acadêmico",
        descricao="Descrição de um projeto acadêmico para testes.",
        tecnologias="Python, SQLAlchemy",
    )


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class MapeamentoProjetoAcademicoTestCase(unittest.TestCase):
    """Confere conversões e metadados sem executar SQL.

    Os cenários usam objetos e metadata declarativa em memória. Eles existem
    para verificar que os contratos do Domain e do banco permanecem alinhados.
    """

    def test_converte_entidade_em_registro(self) -> None:
        """Copia IDs e textos normalizados para o modelo ORM.

        O teste converte uma entidade válida e compara as colunas persistíveis.
        Ele existe para proteger a tradução de dados do Domain para SQLAlchemy.
        """
        registro = para_registro(criar_projeto())

        self.assertIsInstance(registro, ProjetoAcademicoRegistro)
        self.assertEqual(registro.id, ID_PROJETO)
        self.assertEqual(registro.usuario_id, ID_USUARIO)
        self.assertEqual(registro.titulo, "Projeto Acadêmico")
        self.assertEqual(registro.descricao, "Descrição de um projeto acadêmico para testes.")
        self.assertEqual(registro.tecnologias, "Python, SQLAlchemy")

    def test_reconstroi_entidade_a_partir_do_registro(self) -> None:
        """Recria os value objects e textos por meio do construtor do Domain.

        O cenário percorre os dois conversores e compara com a entidade
        original. Ele existe para impedir que modelos ORM vazem para dentro.
        """
        entidade = criar_projeto()

        self.assertEqual(para_projeto_academico(para_registro(entidade)), entidade)

    def test_colunas_foreign_key_e_checks_refletem_limites(self) -> None:
        """Confere tipos, nulabilidade, FK, checks nomeados e ausência de unicidade.

        O teste lê a metadata declarativa sem criar schema. Ele existe para
        detectar divergência entre o contrato de projeto e o modelo relacional.
        """
        tabela = ProjetoAcademicoRegistro.__table__
        checks = {
            constraint.name: str(constraint.sqltext)
            for constraint in tabela.constraints
            if isinstance(constraint, CheckConstraint)
        }
        colunas = (tabela.c.id, tabela.c.usuario_id, tabela.c.titulo, tabela.c.descricao, tabela.c.tecnologias)
        self.assertTrue(all(not coluna.nullable for coluna in colunas))
        self.assertIsInstance(tabela.c.titulo.type, String)
        self.assertEqual(tabela.c.titulo.type.length, 200)
        self.assertIsInstance(tabela.c.descricao.type, Text)
        self.assertIsInstance(tabela.c.tecnologias.type, String)
        self.assertEqual(tabela.c.tecnologias.type.length, 300)

        foreign_keys = [
            constraint
            for constraint in tabela.constraints
            if isinstance(constraint, ForeignKeyConstraint)
        ]
        self.assertEqual(len(foreign_keys), 1)
        self.assertEqual(
            foreign_keys[0].name, "fk_projetos_academicos_usuario_id_usuarios"
        )
        self.assertEqual(
            [element.target_fullname for element in foreign_keys[0].elements],
            ["usuarios.id"],
        )
        self.assertEqual(
            checks,
            {
                "ck_projetos_academicos_titulo_tamanho": (
                    "length(trim(titulo)) BETWEEN 1 AND 200"
                ),
                "ck_projetos_academicos_descricao_tamanho": (
                    "length(trim(descricao)) BETWEEN 1 AND 2000"
                ),
                "ck_projetos_academicos_tecnologias_tamanho": (
                    "length(trim(tecnologias)) BETWEEN 1 AND 300"
                ),
            },
        )
        self.assertFalse(
            any(isinstance(constraint, UniqueConstraint) for constraint in tabela.constraints)
        )

    def test_modelo_compila_para_postgresql_e_sqlite(self) -> None:
        """Compila DDL portável para os dois dialetos suportados.

        O teste gera SQL a partir da tabela sem conexão a banco. Ele existe
        para verificar a sintaxe comum dos tipos, FK e checks.
        """
        tabela = ProjetoAcademicoRegistro.__table__
        ddl_postgresql = str(CreateTable(tabela).compile(dialect=postgresql.dialect()))
        ddl_sqlite = str(CreateTable(tabela).compile(dialect=sqlite.dialect()))

        for ddl in (ddl_postgresql, ddl_sqlite):
            self.assertIn("length(trim(titulo))", ddl)
            self.assertIn("length(trim(descricao))", ddl)
            self.assertIn("length(trim(tecnologias))", ddl)
            self.assertIn("fk_projetos_academicos_usuario_id_usuarios", ddl)


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class RepositorioProjetoAcademicoSQLAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Testa a porta com sessão SQLAlchemy substituída.

    A sessão mockada observa o modelo adicionado, flush e ausência de commit.
    A classe existe para verificar o adapter sem conexão ou transação real.
    """

    async def test_adiciona_registro_e_faz_flush_sem_commit(self) -> None:
        """Persiste o registro mapeado sem finalizar a transação.

        O teste injeta `AsyncSession` mockada e inspeciona suas chamadas. Ele
        existe para manter o commit sob controle da composição externa.
        """
        session = MagicMock(spec=AsyncSession)
        repositorio = RepositorioProjetoAcademicoSQLAlchemy(session)

        await repositorio.salvar(criar_projeto())

        registro = session.add.call_args.args[0]
        self.assertIsInstance(registro, ProjetoAcademicoRegistro)
        self.assertEqual(registro.id, ID_PROJETO)
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()
