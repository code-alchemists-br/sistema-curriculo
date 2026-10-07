"""Valida o contrato Code First da seleção de itens em memória, sem executar DDL contra banco."""

from importlib import import_module
import unittest
from unittest.mock import patch

from sqlalchemy import Column, ForeignKeyConstraint, MetaData, Table, Text, Uuid

from backend.infrastructure.persistence.sqlalchemy.curriculo import CurriculoItemRegistro
from backend.infrastructure.persistence.sqlalchemy.metadata import metadata

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001

MIGRATION = "backend.infrastructure.persistence.alembic.versions.20261007_0003_criar_curriculo_itens"
MIGRATION_ANTERIOR = "backend.infrastructure.persistence.alembic.versions.20261005_0002_criar_curriculos"
NOME_CHAVE_ESTRANGEIRA = "fk_curriculo_itens_curriculo_id_curriculos"
COLUNAS = ["curriculo_id", "tipo", "item_id"]


class CurriculoItensMappingTestCase(unittest.TestCase):
    """Protege o esquema de seleção de itens inspecionando metadata e operações simuladas.

    Compara colunas e constraints em memória para detectar divergências entre
    modelo e migration sem abrir conexão ou aplicar migrações reais.
    """

    def test_metadata_descobre_tabela_com_contrato_aprovado(self) -> None:
        """Verifica descoberta, tipos e chave primária pela metadata do Alembic.

        Inspeciona a tabela registrada para assegurar as três colunas, a chave
        primária composta e a obrigatoriedade de todas as colunas no modelo
        externo.
        """
        tabela = metadata.tables["curriculo_itens"]
        self.assertIs(tabela, CurriculoItemRegistro.__table__)
        self.assertEqual(list(tabela.columns.keys()), COLUNAS)
        self.assertEqual(list(tabela.primary_key.columns.keys()), COLUNAS)
        self.assertIsInstance(tabela.c.curriculo_id.type, Uuid)
        self.assertIsInstance(tabela.c.tipo.type, Text)
        self.assertIsInstance(tabela.c.item_id.type, Uuid)
        for coluna in tabela.columns:
            self.assertFalse(coluna.nullable)

    def test_curriculo_id_referencia_curriculos_por_chave_estrangeira_nomeada(self) -> None:
        """Confirma que a seleção pertence a uma versão existente por chave nomeada.

        Inspeciona as chaves estrangeiras da tabela e confere nome, coluna local
        e destino. Ele existe para impedir seleção sem versão e para registrar
        que não há chave estrangeira para os itens.
        """
        chaves = list(metadata.tables["curriculo_itens"].foreign_key_constraints)

        self.assertEqual(len(chaves), 1)
        self.assertEqual(chaves[0].name, NOME_CHAVE_ESTRANGEIRA)
        self.assertEqual(list(chaves[0].columns.keys()), ["curriculo_id"])
        self.assertEqual([item.target_fullname for item in chaves[0].elements], ["curriculos.id"])

    def test_migration_cria_e_remove_somente_curriculo_itens(self) -> None:
        """Confere operações da revisão substituindo a API Alembic.

        Reconstrói a tabela a partir dos argumentos capturados e a compara com a
        metadata, verifica o encadeamento com a revisão anterior e observa o
        downgrade, sem executar operações destrutivas.
        """
        migration = import_module(MIGRATION)
        anterior = import_module(MIGRATION_ANTERIOR)
        self.assertEqual(migration.revision, "20261007_0003")
        self.assertEqual(migration.down_revision, anterior.revision)
        with patch.object(migration, "op") as operacoes:
            migration.upgrade()
            operacoes.create_table.assert_called_once()
            nome, *elementos = operacoes.create_table.call_args.args
            self.assertEqual(nome, "curriculo_itens")
            self.assertEqual([c.name for c in elementos if isinstance(c, Column)], COLUNAS)
            tabela = Table(nome, MetaData(), *elementos)
            esperada = metadata.tables[nome]
            for coluna in tabela.columns:
                self.assertEqual(type(coluna.type), type(esperada.c[coluna.name].type))
                self.assertEqual(coluna.nullable, esperada.c[coluna.name].nullable)
            self.assertEqual(list(tabela.primary_key.columns.keys()), COLUNAS)
            chaves = [item for item in elementos if isinstance(item, ForeignKeyConstraint)]
            self.assertEqual(len(chaves), 1)
            self.assertEqual(chaves[0].name, NOME_CHAVE_ESTRANGEIRA)
            self.assertEqual(chaves[0].column_keys, ["curriculo_id"])
            self.assertEqual([item.target_fullname for item in chaves[0].elements], ["curriculos.id"])
            migration.downgrade()
            operacoes.drop_table.assert_called_once_with("curriculo_itens")
