"""Valida o contrato Code First em memória, sem executar DDL contra banco."""

import unittest
from importlib import import_module
from unittest.mock import patch

from sqlalchemy import JSON, Column, Text, UniqueConstraint, Uuid

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
        self.assertEqual(
            list(tabela.columns.keys()),
            [
                "id",
                "nome",
                "email",
                "hash_senha",
                "endereco",
                "cidade",
                "telefones",
                "linkedin",
                "curriculo_lattes",
            ],
        )
        self.assertEqual(list(tabela.primary_key.columns.keys()), ["id"])
        self.assertIsInstance(tabela.c.id.type, Uuid)
        self.assertTrue(tabela.c.id.type.as_uuid)
        for nome in ("id", "nome", "email", "hash_senha"):
            self.assertFalse(tabela.c[nome].nullable)
        for nome in ("endereco", "cidade", "telefones", "linkedin", "curriculo_lattes"):
            self.assertTrue(tabela.c[nome].nullable)
        for nome in ("nome", "email", "hash_senha", "endereco", "cidade", "linkedin", "curriculo_lattes"):
            self.assertIsInstance(tabela.c[nome].type, Text)
        self.assertIsInstance(tabela.c.telefones.type, JSON)
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

    def test_migration_adiciona_e_remove_dados_de_contato(self) -> None:
        """Compara a revisão incremental com as colunas opcionais da metadata.

        O teste substitui as operações Alembic e verifica nomes, nulabilidade e
        ordem reversa do downgrade. Ele existe para proteger compatibilidade
        dos perfis existentes sem aplicar DDL em banco real.
        """
        migration = import_module(
            "backend.infrastructure.persistence.alembic.versions.20261014_0007_adicionar_dados_contato_usuario"
        )
        self.assertEqual(migration.revision, "20261014_0007")
        self.assertEqual(migration.down_revision, "20261014_0006")

        with patch.object(migration, "op") as operacoes:
            migration.upgrade()
            colunas_adicionadas = [chamada.args[1] for chamada in operacoes.add_column.call_args_list]
            self.assertEqual(
                [coluna.name for coluna in colunas_adicionadas],
                ["endereco", "cidade", "telefones", "linkedin", "curriculo_lattes"],
            )
            for coluna in colunas_adicionadas:
                self.assertTrue(coluna.nullable)
                self.assertEqual(
                    type(coluna.type), type(metadata.tables["usuarios"].c[coluna.name].type)
                )

            migration.downgrade()

        self.assertEqual(
            [chamada.args for chamada in operacoes.drop_column.call_args_list],
            [
                ("usuarios", "curriculo_lattes"),
                ("usuarios", "linkedin"),
                ("usuarios", "telefones"),
                ("usuarios", "cidade"),
                ("usuarios", "endereco"),
            ],
        )
