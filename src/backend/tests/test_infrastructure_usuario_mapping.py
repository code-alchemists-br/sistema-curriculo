"""Valida o contrato Code First em memória, sem executar DDL contra banco."""

from importlib import import_module
import unittest
from unittest.mock import patch

from sqlalchemy import Column, Text, UniqueConstraint, Uuid

from backend.infrastructure.persistence.sqlalchemy.metadata import metadata
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro

# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001


class UsuarioMappingTestCase(unittest.TestCase):
    """Protege o esquema inicial inspecionando metadata e operações simuladas.

    Compara colunas e constraints em memória para detectar divergências entre
    modelo e migration sem abrir conexão ou aplicar migrações reais.
    """

    def test_metadata_descobre_tabela_com_contrato_aprovado(self) -> None:
        """Verifica descoberta e tipos pela metadata consumida pelo Alembic.

        Inspeciona a tabela registrada e suas constraints para assegurar UUID,
        campos obrigatórios e unicidade de e-mail no modelo externo.
        """
        tabela = metadata.tables["usuarios"]
        self.assertIs(tabela, UsuarioRegistro.__table__)
        self.assertEqual(list(tabela.columns.keys()), ["id", "nome", "email", "hash_senha"])
        self.assertEqual(list(tabela.primary_key.columns.keys()), ["id"])
        self.assertIsInstance(tabela.c.id.type, Uuid)
        self.assertTrue(tabela.c.id.type.as_uuid)
        for coluna in tabela.columns:
            self.assertFalse(coluna.nullable)
            if coluna.name != "id":
                self.assertIsInstance(coluna.type, Text)
        unicas = [c for c in tabela.constraints if isinstance(c, UniqueConstraint)]
        self.assertEqual(len(unicas), 1)
        self.assertEqual(unicas[0].name, "uq_usuarios_email")
        self.assertEqual(list(unicas[0].columns.keys()), ["email"])

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
            self.assertEqual([c.name for c in colunas], list(metadata.tables[nome].columns.keys()))
            for coluna in colunas:
                esperada = metadata.tables[nome].c[coluna.name]
                self.assertEqual(type(coluna.type), type(esperada.type))
                self.assertEqual(coluna.nullable, esperada.nullable)
            unicas = [c for c in elementos if isinstance(c, UniqueConstraint)]
            self.assertEqual(len(unicas), 1)
            self.assertEqual(unicas[0].name, "uq_usuarios_email")
            migration.downgrade()
            operacoes.drop_table.assert_called_once_with("usuarios")
