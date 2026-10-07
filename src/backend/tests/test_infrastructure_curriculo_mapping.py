"""Valida o contrato Code First de currículos em memória, sem executar DDL contra banco."""

import unittest
from importlib import import_module
from unittest.mock import patch

from sqlalchemy import Boolean, Column, ForeignKeyConstraint, Text, Uuid

from backend.infrastructure.persistence.sqlalchemy.curriculo import CurriculoRegistro
from backend.infrastructure.persistence.sqlalchemy.metadata import metadata

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001

MIGRATION = "backend.infrastructure.persistence.alembic.versions.20261005_0002_criar_curriculos"
MIGRATION_ANTERIOR = "backend.infrastructure.persistence.alembic.versions.20260916_0001_criar_usuarios"
NOME_CHAVE_ESTRANGEIRA = "fk_curriculos_usuario_id_usuarios"


class CurriculoMappingTestCase(unittest.TestCase):
    """Protege o esquema de currículos inspecionando metadata e operações simuladas.

    Compara colunas e constraints em memória para detectar divergências entre
    modelo e migration sem abrir conexão ou aplicar migrações reais.
    """

    def test_metadata_descobre_tabela_com_contrato_aprovado(self) -> None:
        """Verifica descoberta e tipos pela metadata consumida pelo Alembic.

        Inspeciona a tabela registrada e suas colunas para assegurar UUID, texto,
        booleano e obrigatoriedade no modelo externo.
        """
        tabela = metadata.tables["curriculos"]
        self.assertIs(tabela, CurriculoRegistro.__table__)
        self.assertEqual(
            list(tabela.columns.keys()),
            ["id", "usuario_id", "titulo_versao", "layout", "is_public"],
        )
        self.assertEqual(list(tabela.primary_key.columns.keys()), ["id"])
        self.assertIsInstance(tabela.c.id.type, Uuid)
        self.assertIsInstance(tabela.c.usuario_id.type, Uuid)
        self.assertIsInstance(tabela.c.titulo_versao.type, Text)
        self.assertIsInstance(tabela.c.layout.type, Text)
        self.assertIsInstance(tabela.c.is_public.type, Boolean)
        for coluna in tabela.columns:
            self.assertFalse(coluna.nullable)

    def test_usuario_id_referencia_usuarios_por_chave_estrangeira_nomeada(self) -> None:
        """Confirma que o proprietário é protegido por chave estrangeira nomeada.

        Inspeciona as chaves estrangeiras da tabela e confere nome, coluna local
        e destino. Ele existe para impedir currículos sem dono existente.
        """
        chaves = list(metadata.tables["curriculos"].foreign_key_constraints)

        self.assertEqual(len(chaves), 1)
        self.assertEqual(chaves[0].name, NOME_CHAVE_ESTRANGEIRA)
        self.assertEqual(list(chaves[0].columns.keys()), ["usuario_id"])
        self.assertEqual([item.target_fullname for item in chaves[0].elements], ["usuarios.id"])

    def test_migration_cria_e_remove_somente_curriculos(self) -> None:
        """Confere operações da revisão substituindo a API Alembic.

        Compara colunas congeladas com a metadata, verifica o encadeamento com a
        revisão anterior e observa o downgrade para proteger a reversibilidade
        sem executar operações destrutivas.
        """
        migration = import_module(MIGRATION)
        anterior = import_module(MIGRATION_ANTERIOR)
        self.assertEqual(migration.revision, "20261005_0002")
        self.assertEqual(migration.down_revision, anterior.revision)
        with patch.object(migration, "op") as operacoes:
            migration.upgrade()
            operacoes.create_table.assert_called_once()
            nome, *elementos = operacoes.create_table.call_args.args
            self.assertEqual(nome, "curriculos")
            colunas = [item for item in elementos if isinstance(item, Column)]
            self.assertEqual([c.name for c in colunas], list(metadata.tables[nome].columns.keys()))
            for coluna in colunas:
                esperada = metadata.tables[nome].c[coluna.name]
                self.assertEqual(type(coluna.type), type(esperada.type))
                self.assertEqual(coluna.nullable, esperada.nullable)
            chaves = [item for item in elementos if isinstance(item, ForeignKeyConstraint)]
            self.assertEqual(len(chaves), 1)
            self.assertEqual(chaves[0].name, NOME_CHAVE_ESTRANGEIRA)
            self.assertEqual(chaves[0].column_keys, ["usuario_id"])
            self.assertEqual([item.target_fullname for item in chaves[0].elements], ["usuarios.id"])
            migration.downgrade()
            operacoes.drop_table.assert_called_once_with("curriculos")