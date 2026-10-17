"""Valida a persistência da ordem das seções: coluna, migration e mapeamento."""

import unittest
from importlib import import_module
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from sqlalchemy import Column, Text

# Proveniência: decision-analysis prompts/backend/20261017-180000-persistir-ordem-secoes-curriculo-v001.md#v001
from backend.domain import (
    ORDEM_PADRAO_SECOES,
    Curriculo,
    CurriculoId,
    RegraDeDominioViolada,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.curriculo import (
    atualizar_registro,
    ordem_secoes_para_texto,
    para_curriculo,
    para_registro,
    texto_para_ordem_secoes,
)
from backend.infrastructure.persistence.sqlalchemy.metadata import metadata

MIGRATION = (
    "backend.infrastructure.persistence.alembic.versions."
    "20261017_0015_adicionar_ordem_secoes_curriculos"
)
MIGRATION_ANTERIOR = (
    "backend.infrastructure.persistence.alembic.versions."
    "20261017_0014_exclusao_logica_experiencias_profissionais"
)
ORDEM_INVERTIDA = tuple(reversed(ORDEM_PADRAO_SECOES))


def _criar_curriculo() -> Curriculo:
    """Cria uma versão de currículo válida para os testes de mapeamento.

    A função monta o agregado sem acessar gerador, banco ou relógio. Ela existe
    para que cada teste parta de uma versão válida e altere só a ordem.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=UsuarioId(uuid4()),
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


def _criar_registro(ordem_secoes: str) -> SimpleNamespace:
    """Cria um registro ORM simulado com a ordem das seções informada.

    A função expõe somente as colunas lidas pelo mapeador, sem sessão ou tabela.
    Ela existe para controlar o texto persistido em cada cenário.
    """
    return SimpleNamespace(
        id=uuid4(),
        usuario_id=uuid4(),
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
        ordem_secoes=ordem_secoes,
    )


class ColunaOrdemSecoesTestCase(unittest.TestCase):
    """Verifica a coluna ``ordem_secoes`` e a migration que a cria.

    Os testes inspecionam a metadata e as operações simuladas da migration sem
    abrir conexão com banco. A classe existe para impedir divergência entre o
    modelo e o schema versionado.
    """

    def test_coluna_e_texto_nao_nulo_com_ordem_padrao_no_servidor(self) -> None:
        """Confirma tipo, obrigatoriedade e valor padrão da coluna no modelo.

        O teste lê a coluna na metadata consumida pelo Alembic. Ele existe para
        que versões novas e antigas sempre tenham uma ordem gravada.
        """
        coluna = metadata.tables["curriculos"].c.ordem_secoes

        self.assertIsInstance(coluna.type, Text)
        self.assertFalse(coluna.nullable)
        self.assertEqual(
            str(coluna.server_default.arg), ordem_secoes_para_texto(ORDEM_PADRAO_SECOES)
        )

    def test_migration_adiciona_e_remove_somente_a_coluna(self) -> None:
        """Confirma encadeamento, upgrade e downgrade da migration.

        O teste substitui a API Alembic, confere a revisão anterior e as
        operações sobre a tabela e a coluna. Ele existe para proteger a
        reversibilidade sem executar DDL.
        """
        migration = import_module(MIGRATION)
        anterior = import_module(MIGRATION_ANTERIOR)
        self.assertEqual(migration.revision, "20261017_0015")
        self.assertEqual(migration.down_revision, anterior.revision)

        with patch.object(migration, "op") as operacoes:
            migration.upgrade()
            operacoes.add_column.assert_called_once()
            tabela, coluna = operacoes.add_column.call_args.args
            self.assertEqual(tabela, "curriculos")
            self.assertIsInstance(coluna, Column)
            self.assertEqual(coluna.name, "ordem_secoes")
            self.assertIsInstance(coluna.type, Text)
            self.assertFalse(coluna.nullable)
            self.assertEqual(
                str(coluna.server_default.arg),
                ordem_secoes_para_texto(ORDEM_PADRAO_SECOES),
            )
            migration.downgrade()
            operacoes.drop_column.assert_called_once_with("curriculos", "ordem_secoes")


class MapeamentoOrdemSecoesTestCase(unittest.TestCase):
    """Verifica a conversão da ordem das seções entre agregado e registro.

    Os testes cobrem o texto gravado, a leitura, a atualização e a recusa de
    valores inválidos, sem sessão ou banco. A classe existe para proteger o
    mapeamento da ordem explícita.
    """

    def test_texto_e_ordem_sao_convertidos_nos_dois_sentidos(self) -> None:
        """Confirma que a conversão para texto e de volta preserva a ordem.

        O teste converte a ordem invertida para texto e de volta. Ele existe
        para garantir que a ordem gravada é a mesma que será lida.
        """
        texto = ordem_secoes_para_texto(ORDEM_INVERTIDA)

        self.assertEqual(texto_para_ordem_secoes(texto), ORDEM_INVERTIDA)

    def test_registro_novo_leva_a_ordem_do_agregado(self) -> None:
        """Confirma que o registro criado carrega o texto da ordem do agregado.

        O teste converte um agregado com ordem invertida em registro. Ele existe
        para que a criação grave a ordem explícita e não a padrão por engano.
        """
        curriculo = _criar_curriculo()
        curriculo.definir_ordem_secoes(ORDEM_INVERTIDA)

        registro = para_registro(curriculo)

        self.assertEqual(registro.ordem_secoes, ordem_secoes_para_texto(ORDEM_INVERTIDA))

    def test_leitura_reconstroi_a_ordem_persistida(self) -> None:
        """Confirma que o agregado lido tem a ordem gravada no registro.

        O teste converte um registro com ordem invertida em agregado. Ele existe
        para que a ordem escolhida pelo estudante sobreviva à leitura.
        """
        registro = _criar_registro(ordem_secoes_para_texto(ORDEM_INVERTIDA))

        self.assertEqual(para_curriculo(registro).ordem_secoes, ORDEM_INVERTIDA)  # type: ignore[arg-type]

    def test_atualizacao_copia_a_ordem_para_o_registro(self) -> None:
        """Confirma que a atualização grava a nova ordem no registro existente.

        O teste altera a ordem do agregado e aplica ao registro. Ele existe para
        que a mudança de ordem seja persistida na edição.
        """
        registro = _criar_registro(ordem_secoes_para_texto(ORDEM_PADRAO_SECOES))
        curriculo = _criar_curriculo()
        curriculo.definir_ordem_secoes(ORDEM_INVERTIDA)

        atualizar_registro(registro, curriculo)  # type: ignore[arg-type]

        self.assertEqual(registro.ordem_secoes, ordem_secoes_para_texto(ORDEM_INVERTIDA))

    def test_leitura_recusa_identificador_de_secao_desconhecido(self) -> None:
        """Confirma que um identificador desconhecido no banco falha alto.

        O teste lê um registro com uma seção inexistente. Ele existe para que
        dado corrompido não seja ignorado em silêncio.
        """
        with self.assertRaises(ValueError):
            para_curriculo(_criar_registro("dados-pessoais,hobbies"))  # type: ignore[arg-type]

    def test_leitura_recusa_ordem_incompleta(self) -> None:
        """Confirma que uma ordem gravada incompleta é recusada pelo domínio.

        O teste lê um registro com apenas uma seção. Ele existe para que a
        validação do agregado também proteja os dados vindos do banco.
        """
        with self.assertRaises(RegraDeDominioViolada):
            para_curriculo(_criar_registro("idiomas"))  # type: ignore[arg-type]
