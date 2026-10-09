"""Verifica a fixture híbrida usando ORM e SQLite descartável.

A suíte cria o schema a partir da metadata SQLAlchemy, persiste usuário e
currículo, e então usa a função de leitura para compor os objetos restantes.
Ela existe para provar a fronteira integrada da fixture sem depender de serviço
ou banco externo.
"""

import unittest

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Proveniência: decision-analysis prompts/backend/20261009-160234-dados-reutilizaveis-perfis-testes-integracao-e2e-v003.md#v003
from backend.infrastructure.persistence.sqlalchemy.usuario import Base
from backend.tests.fixtures.perfis_integracao import (
    ID_CURRICULO_ANA_BORDA,
    ID_CURRICULO_ANA_COMPLETO,
    ID_ESTUDANTE_ANA,
    ID_ESTUDANTE_BRUNO,
    ler_perfis_fake,
    popular_perfis_fake,
)


class FixturePerfisIntegracaoTestCase(unittest.TestCase):
    """Verifica a leitura e composição de perfis através de SQLite real.

    Cada teste cria engine SQLite em memória, habilita chaves estrangeiras e
    monta as tabelas pela metadata Code First. A classe existe para demonstrar
    persistência e recuperação sem compartilhar estado entre cenários.
    """

    def setUp(self) -> None:
        """Cria um SQLite isolado e inicializa o schema mapeado.

        A engine usa uma conexão em memória compartilhada somente dentro do
        teste e ativa enforcement de FK no driver SQLite. Ela existe para que a
        fixture atravesse a fronteira ORM/banco em ambiente descartável.
        """

        self.engine = create_engine(
            "sqlite+pysqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        event.listen(self.engine, "connect", _habilitar_chaves_estrangeiras)
        Base.metadata.create_all(self.engine)
        self.criar_sessao = sessionmaker(bind=self.engine, class_=Session, expire_on_commit=False)

    def tearDown(self) -> None:
        """Descarta a engine e a base em memória ao terminar cada caso.

        O método fecha as conexões abertas pelo pool SQLite local. Ele existe
        para impedir que dados de um teste influenciem a execução seguinte.
        """

        self.engine.dispose()

    def test_le_perfis_sqlite_e_compõe_itens_em_memoria(self) -> None:
        """Confirma recuperação ORM e composição híbrida para dois proprietários.

        O teste popula as tabelas reais, consulta por meio da fixture e compara
        os dados persistidos com formação/experiência válidas em memória. Ele
        existe para garantir que a função entrega o cenário aprovado sem
        confundir a origem dos itens.
        """

        with self.criar_sessao() as session:
            popular_perfis_fake(session)
            session.commit()

        with self.criar_sessao() as session:
            perfis = ler_perfis_fake(session)

        por_id = {perfil.usuario.id.valor: perfil for perfil in perfis}
        self.assertEqual(set(por_id), {ID_ESTUDANTE_ANA, ID_ESTUDANTE_BRUNO})

        ana = por_id[ID_ESTUDANTE_ANA]
        self.assertIsNone(ana.curriculo_selecionado_id)
        self.assertEqual(ana.usuario.nome.valor, "Ana Exemplo")
        self.assertEqual(ana.usuario.email.valor, "ana@example.test")
        self.assertEqual(ana.formacao_academica.usuario_id, ana.usuario.id)
        self.assertEqual(ana.experiencia_profissional.usuario_id, ana.usuario.id)
        self.assertEqual(len(ana.curriculos), 2)

        curriculo_completo, curriculo_borda = ana.curriculos
        self.assertEqual(curriculo_completo.id.valor, ID_CURRICULO_ANA_COMPLETO)
        self.assertEqual(len(curriculo_completo.referencias), 2)
        self.assertEqual(curriculo_borda.id.valor, ID_CURRICULO_ANA_BORDA)
        self.assertEqual(curriculo_borda.referencias, frozenset())

        bruno = por_id[ID_ESTUDANTE_BRUNO]
        self.assertEqual(bruno.usuario.email.valor, "bruno@example.test")
        self.assertEqual(len(bruno.curriculos), 1)
        self.assertEqual(bruno.curriculos[0].usuario_id, bruno.usuario.id)

    def test_retorna_vazio_antes_de_executar_o_seed(self) -> None:
        """Confirma que a leitura de banco ainda não seedado retorna coleção vazia.

        O teste consulta uma sessão recém-criada sem chamar o seed. Ele existe
        para distinguir explicitamente setup de leitura e evitar preenchimento
        implícito que esconda dependências entre casos.
        """

        with self.criar_sessao() as session:
            self.assertEqual(ler_perfis_fake(session), ())


def _habilitar_chaves_estrangeiras(conexao, registro) -> None:
    """Ativa a verificação de chaves estrangeiras no SQLite conectado.

    O callback envia `PRAGMA foreign_keys=ON` pela conexão DBAPI ao abrir cada
    conexão física. Ele existe porque SQLite não habilita FK automaticamente,
    permitindo que o cenário integrado use as constraints declaradas no mapping.
    """

    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
