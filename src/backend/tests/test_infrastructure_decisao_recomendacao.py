"""Valida a tabela, a migration e o mapeamento das decisões sobre recomendações."""

import unittest
from datetime import UTC, datetime, timedelta, timezone
from importlib import import_module
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from sqlalchemy import Column, DateTime, MetaData, Table, Text, Uuid

# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
from backend.domain import (
    CurriculoId,
    DecisaoEstudante,
    DecisaoRecomendacao,
    RegraDeDominioViolada,
)
from backend.infrastructure.persistence.sqlalchemy.decisao_recomendacao import (
    DecisaoRecomendacaoRegistro,
    para_decisao,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.metadata import metadata

MIGRATION = (
    "backend.infrastructure.persistence.alembic.versions."
    "20261023_0016_criar_decisoes_recomendacao"
)
MIGRATION_ANTERIOR = (
    "backend.infrastructure.persistence.alembic.versions."
    "20261017_0015_adicionar_ordem_secoes_curriculos"
)
NOME_CHAVE_ESTRANGEIRA = "fk_decisoes_recomendacao_curriculo_id_curriculos"
INSTANTE = datetime(2026, 10, 23, 12, 0, tzinfo=UTC)


class TabelaDecisoesRecomendacaoTestCase(unittest.TestCase):
    """Protege a tabela ``decisoes_recomendacao`` e a migration que a cria.

    Os testes inspecionam a metadata e as operações simuladas da migration sem
    abrir conexão. A classe existe para impedir divergência entre o modelo e o
    schema versionado.
    """

    def test_metadata_descobre_tabela_com_colunas_e_chave_composta(self) -> None:
        """Confirma colunas, tipos, obrigatoriedade e chave primária da tabela.

        O teste lê a tabela registrada na metadata do Alembic. Ele existe para
        garantir uma só decisão por versão e código.
        """
        tabela = metadata.tables["decisoes_recomendacao"]

        self.assertIs(tabela, DecisaoRecomendacaoRegistro.__table__)
        self.assertEqual(
            list(tabela.columns.keys()),
            ["curriculo_id", "codigo", "decisao", "decidida_em"],
        )
        self.assertEqual(
            list(tabela.primary_key.columns.keys()), ["curriculo_id", "codigo"]
        )
        self.assertIsInstance(tabela.c.curriculo_id.type, Uuid)
        self.assertIsInstance(tabela.c.codigo.type, Text)
        self.assertIsInstance(tabela.c.decisao.type, Text)
        self.assertIsInstance(tabela.c.decidida_em.type, DateTime)
        self.assertTrue(tabela.c.decidida_em.type.timezone)
        for coluna in tabela.columns:
            self.assertFalse(coluna.nullable)

    def test_versao_e_chave_estrangeira_que_remove_as_decisoes_junto(self) -> None:
        """Confirma a chave estrangeira nomeada com exclusão em cascata.

        O teste inspeciona nome, coluna, destino e ``ondelete``. Ele existe para
        que excluir a versão não deixe decisões órfãs nem trave a exclusão.
        """
        chaves = list(metadata.tables["decisoes_recomendacao"].foreign_key_constraints)

        self.assertEqual(len(chaves), 1)
        self.assertEqual(chaves[0].name, NOME_CHAVE_ESTRANGEIRA)
        self.assertEqual(list(chaves[0].columns.keys()), ["curriculo_id"])
        self.assertEqual(
            [item.target_fullname for item in chaves[0].elements], ["curriculos.id"]
        )
        self.assertEqual(chaves[0].ondelete, "CASCADE")

    def test_migration_cria_e_remove_a_tabela_igual_a_metadata(self) -> None:
        """Confere encadeamento, criação e remoção da tabela pela migration.

        O teste substitui a API Alembic, monta uma tabela com os elementos
        recebidos e a compara com a metadata. Ele existe para proteger a
        reversibilidade sem executar DDL.
        """
        migration = import_module(MIGRATION)
        anterior = import_module(MIGRATION_ANTERIOR)
        self.assertEqual(migration.revision, "20261023_0016")
        self.assertEqual(migration.down_revision, anterior.revision)

        with patch.object(migration, "op") as operacoes:
            migration.upgrade()
            operacoes.create_table.assert_called_once()
            nome, *elementos = operacoes.create_table.call_args.args
            self.assertEqual(nome, "decisoes_recomendacao")
            criada = Table(nome, MetaData(), *elementos)
            esperada = metadata.tables[nome]
            self.assertEqual(
                list(criada.columns.keys()), list(esperada.columns.keys())
            )
            for coluna in criada.columns:
                self.assertEqual(type(coluna.type), type(esperada.c[coluna.name].type))
                self.assertEqual(coluna.nullable, esperada.c[coluna.name].nullable)
            self.assertEqual(
                list(criada.primary_key.columns.keys()),
                list(esperada.primary_key.columns.keys()),
            )
            chave = next(iter(criada.foreign_key_constraints))
            self.assertEqual(chave.name, NOME_CHAVE_ESTRANGEIRA)
            self.assertEqual(chave.ondelete, "CASCADE")
            migration.downgrade()
            operacoes.drop_table.assert_called_once_with("decisoes_recomendacao")
        self.assertTrue(any(isinstance(c, Column) for c in elementos))


class MapeamentoDecisaoRecomendacaoTestCase(unittest.TestCase):
    """Verifica a conversão entre a decisão de domínio e o registro ORM.

    Os testes cobrem a ida, a volta, o fuso e os valores inválidos, sem sessão ou
    banco. A classe existe para proteger o mapeamento da decisão.
    """

    def test_registro_carrega_valores_primitivos_da_decisao(self) -> None:
        """Confirma que o registro recebe UUID, código, texto e instante.

        O teste converte uma decisão em registro. Ele existe para que o banco
        nunca receba value objects.
        """
        curriculo_id = CurriculoId(uuid4())
        decisao = DecisaoRecomendacao(
            curriculo_id, "IDIOMA_AUSENTE", DecisaoEstudante.ACEITA, INSTANTE
        )

        registro = para_registro(decisao)

        self.assertEqual(registro.curriculo_id, curriculo_id.valor)
        self.assertEqual(registro.codigo, "IDIOMA_AUSENTE")
        self.assertEqual(registro.decisao, "aceita")
        self.assertEqual(registro.decidida_em, INSTANTE)

    def test_ida_e_volta_preserva_a_decisao(self) -> None:
        """Confirma que converter para registro e voltar devolve a mesma decisão.

        O teste faz a ida e a volta para cada tipo de decisão. Ele existe para
        garantir que o que foi gravado é o que será lido.
        """
        for escolha in DecisaoEstudante:
            with self.subTest(decisao=escolha.value):
                original = DecisaoRecomendacao(
                    CurriculoId(uuid4()), "PROJETO_AUSENTE", escolha, INSTANTE
                )

                self.assertEqual(para_decisao(para_registro(original)), original)

    def test_instante_sem_fuso_vindo_do_banco_e_tratado_como_utc(self) -> None:
        """Confirma que o instante ingênuo lido do banco vira UTC.

        O teste lê um registro com data sem fuso, como alguns bancos devolvem. Ele
        existe para que o domínio, que exige fuso, aceite o que foi gravado.
        """
        registro = SimpleNamespace(
            curriculo_id=uuid4(),
            codigo="PROJETO_AUSENTE",
            decisao="rejeitada",
            decidida_em=datetime(2026, 10, 23, 12, 0),
        )

        decisao = para_decisao(registro)  # type: ignore[arg-type]

        self.assertEqual(decisao.decidida_em, INSTANTE)
        self.assertEqual(decisao.decidida_em.utcoffset(), timedelta(0))

    def test_preserva_o_fuso_quando_o_banco_o_devolve(self) -> None:
        """Confirma que um instante com fuso é mantido como veio.

        O teste lê um registro com o fuso de Brasília. Ele existe para não
        alterar silenciosamente instantes já com fuso.
        """
        brasilia = timezone(timedelta(hours=-3))
        registro = SimpleNamespace(
            curriculo_id=uuid4(),
            codigo="PROJETO_AUSENTE",
            decisao="aceita",
            decidida_em=datetime(2026, 10, 23, 9, 0, tzinfo=brasilia),
        )

        decisao = para_decisao(registro)  # type: ignore[arg-type]

        self.assertEqual(decisao.decidida_em.utcoffset(), timedelta(hours=-3))
        self.assertEqual(decisao.decidida_em, INSTANTE)

    def test_leitura_recusa_decisao_desconhecida_e_codigo_invalido(self) -> None:
        """Confirma que dados corrompidos no banco falham alto.

        O teste lê um registro com decisão inexistente e outro com código fora do
        padrão. Ele existe para que dado inválido não seja ignorado em silêncio.
        """
        base = {"curriculo_id": uuid4(), "decidida_em": INSTANTE}

        with self.assertRaises(ValueError):
            para_decisao(
                SimpleNamespace(codigo="PROJETO_AUSENTE", decisao="talvez", **base)  # type: ignore[arg-type]
            )
        with self.assertRaises(RegraDeDominioViolada):
            para_decisao(
                SimpleNamespace(codigo="projeto", decisao="aceita", **base)  # type: ignore[arg-type]
            )
