"""Valida o contrato Code First em memória, sem executar DDL contra banco."""

import unittest
from datetime import datetime, timezone
from importlib import import_module
from unittest.mock import patch
from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, Text, UniqueConstraint, Uuid

from backend.domain import (
    Cidade,
    DadosContato,
    Email,
    Endereco,
    HashSenha,
    Nome,
    Telefone,
    Usuario,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.metadata import metadata
from backend.infrastructure.persistence.sqlalchemy.usuario import (
    UsuarioRegistro,
    para_registro,
    para_usuario,
)

# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001


class UsuarioMappingTestCase(unittest.TestCase):
    """Protege o esquema inicial inspecionando metadata e operações simuladas.

    Compara colunas e constraints em memória para detectar divergências entre
    modelo e migration sem abrir conexão ou aplicar migrações reais.
    """

    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    def test_metadata_descobre_tabela_com_contrato_aprovado(self) -> None:
        """Verifica descoberta e tipos pela metadata consumida pelo Alembic.

        Inspeciona a tabela registrada e suas constraints para assegurar UUID,
        campos obrigatórios e unicidade de e-mail no modelo externo.
        """
        tabela = metadata.tables["usuarios"]
        self.assertIs(tabela, UsuarioRegistro.__table__)
        self.assertEqual(
            list(tabela.columns.keys()),
            [
                "id",
                "nome",
                "email",
                "hash_senha",
                "deleted_at",
                "endereco",
                "telefones",
                "cidade",
                "linkedin",
                "curriculo_lattes",
            ],
        )
        self.assertEqual(list(tabela.primary_key.columns.keys()), ["id"])
        self.assertIsInstance(tabela.c.id.type, Uuid)
        self.assertTrue(tabela.c.id.type.as_uuid)
        for nome in ("id", "nome", "email", "hash_senha"):
            self.assertFalse(tabela.c[nome].nullable)
        for nome in (
            "deleted_at",
            "endereco",
            "telefones",
            "cidade",
            "linkedin",
            "curriculo_lattes",
        ):
            self.assertTrue(tabela.c[nome].nullable)
        self.assertIsInstance(tabela.c.telefones.type, JSON)
        self.assertIsInstance(tabela.c.deleted_at.type, DateTime)
        for nome in ("nome", "email", "hash_senha", "endereco", "cidade", "linkedin", "curriculo_lattes"):
            self.assertIsInstance(tabela.c[nome].type, Text)
        unicas = [c for c in tabela.constraints if isinstance(c, UniqueConstraint)]
        self.assertEqual(len(unicas), 1)
        self.assertEqual(unicas[0].name, "uq_usuarios_email")
        self.assertEqual(list(unicas[0].columns.keys()), ["email"])

    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    def test_migration_cria_e_remove_somente_usuarios(self) -> None:
        """Confere operações da revisão inicial substituindo a API Alembic.

        Compara colunas congeladas com metadata e observa downgrade para
        proteger a reversibilidade declarada sem executar operações destrutivas.
        """
        migration = import_module(
            "backend.infrastructure.persistence.alembic.versions.20260916_0001_criar_usuarios"
        )
        self.assertEqual(migration.revision, "20260916_0001")
        self.assertIsNone(migration.down_revision)
        with patch.object(migration, "op") as operacoes:
            migration.upgrade()
            operacoes.create_table.assert_called_once()
            nome, *elementos = operacoes.create_table.call_args.args
            self.assertEqual(nome, "usuarios")
            colunas = [item for item in elementos if isinstance(item, Column)]
            self.assertEqual(
                [c.name for c in colunas], ["id", "nome", "email", "hash_senha"]
            )
            for coluna in colunas:
                esperada = metadata.tables[nome].c[coluna.name]
                self.assertEqual(type(coluna.type), type(esperada.type))
                self.assertEqual(coluna.nullable, esperada.nullable)
            unicas = [c for c in elementos if isinstance(c, UniqueConstraint)]
            self.assertEqual(len(unicas), 1)
            self.assertEqual(unicas[0].name, "uq_usuarios_email")
            migration.downgrade()
            operacoes.drop_table.assert_called_once_with("usuarios")

    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    def test_mapper_persiste_e_reconstroi_contato_cidade_e_exclusao(self) -> None:
        """Confirma ida e volta entre agregado e colunas primitivas.

        Usa somente o modelo ORM em memória e compara o estado reconstituído,
        sem abrir sessão ou banco. O teste existe para manter contato, cidade e
        exclusão lógica duráveis através da fronteira de persistência.
        """
        excluido_em = datetime(2026, 10, 12, tzinfo=timezone.utc)
        usuario = Usuario(
            id=UsuarioId(uuid4()),
            nome=Nome("Ana Silva"),
            email=Email("ana@example.com"),
            hash_senha=HashSenha("hash-ja-derivado"),
            deleted_at=excluido_em,
            dados_contato=DadosContato(
                endereco=Endereco("Rua Um, 100"),
                telefones=(Telefone("11999990000"), Telefone("1133334444")),
                linkedin="https://linkedin.com/in/ana",
                curriculo_lattes="http://lattes.cnpq.br/123",
                cidade=Cidade("São Paulo"),
            ),
        )

        registro = para_registro(usuario)
        reconstituido = para_usuario(registro)

        self.assertEqual(registro.deleted_at, excluido_em)
        self.assertEqual(registro.endereco, "Rua Um, 100")
        self.assertEqual(registro.telefones, ["11999990000", "1133334444"])
        self.assertEqual(registro.cidade, "São Paulo")
        self.assertEqual(registro.linkedin, "https://linkedin.com/in/ana")
        self.assertEqual(registro.curriculo_lattes, "http://lattes.cnpq.br/123")
        self.assertEqual(reconstituido, usuario)

    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    def test_migration_de_consulta_adiciona_e_remove_colunas_opcionais(self) -> None:
        """Confere a migration de perfil sem executar DDL real.

        Substitui a API Alembic e verifica nomes/tipos das colunas, além da
        ordem reversa do downgrade. O teste existe para proteger a evolução
        Code First sem conectar a um banco.
        """
        migration = import_module(
            "backend.infrastructure.persistence.alembic.versions.20261013_0004_adicionar_dados_consulta_estudante"
        )
        self.assertEqual(migration.revision, "20261013_0004")
        self.assertEqual(migration.down_revision, "20261007_0003")
        with patch.object(migration, "op") as operacoes:
            migration.upgrade()
            self.assertEqual(operacoes.add_column.call_count, 6)
            colunas = [chamada.args[1] for chamada in operacoes.add_column.call_args_list]
            self.assertEqual(
                [coluna.name for coluna in colunas],
                [
                    "deleted_at",
                    "endereco",
                    "telefones",
                    "cidade",
                    "linkedin",
                    "curriculo_lattes",
                ],
            )
            self.assertIsInstance(colunas[0].type, DateTime)
            self.assertIsInstance(colunas[2].type, JSON)
            self.assertTrue(all(coluna.nullable for coluna in colunas))

            migration.downgrade()

        self.assertEqual(
            [chamada.args[1] for chamada in operacoes.drop_column.call_args_list],
            [
                "curriculo_lattes",
                "linkedin",
                "cidade",
                "telefones",
                "endereco",
                "deleted_at",
            ],
        )
