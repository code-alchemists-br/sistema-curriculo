"""Testes de persistência SQLite da associação currículo-vaga."""

from unittest import TestCase
from uuid import UUID

from sqlalchemy import create_engine, delete, event, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
from backend.domain.associacao_curriculo_vaga import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
)
from backend.domain.value_objects import CurriculoId, VagaId
from backend.infrastructure.persistence.sqlalchemy.associacao_curriculo_vaga import (
    AssociacaoCurriculoVagaRegistro,
    ClassificacaoAssociacaoRegistro,
    para_associacao,
    para_registro,
    para_registros_classificacoes,
)
from backend.infrastructure.persistence.sqlalchemy.curriculo import CurriculoRegistro
from backend.infrastructure.persistence.sqlalchemy.metadata import metadata
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro


# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
def _ativar_chaves_estrangeiras(connection, _record) -> None:
    """Ativa verificação de FKs em cada conexão SQLite de teste.

    A função executa o pragma exigido pelo SQLite antes do início das transações.
    Ela existe para que os cenários cubram as mesmas dependências relacionais
    declaradas pelo mapping e pela migration.
    """
    connection.execute("PRAGMA foreign_keys=ON")


class PersistenciaAssociacaoCurriculoVagaIntegracaoTestCase(TestCase):
    """Valida constraints e rollback com a metadata SQLAlchemy real.

    Os cenários usam SQLite em memória, sessão síncrona e tabelas criadas da
    metadata do projeto para exercitar round-trip, unicidade e atomicidade. Eles
    existem para demonstrar que o modelo relacional protege o agregado sem
    depender de serviço externo.
    """

    def setUp(self) -> None:
        """Cria banco isolado e um currículo válido para os cenários.

        O método ativa FKs, cria o schema atual e semeia usuário e currículo
        mínimos. Ele existe para tornar cada teste independente e determinístico.
        """
        self.usuario_id = UUID("00000000-0000-0000-0000-000000000301")
        self.curriculo_id = UUID("00000000-0000-0000-0000-000000000302")
        self.engine = create_engine("sqlite+pysqlite://")
        event.listen(self.engine, "connect", _ativar_chaves_estrangeiras)
        metadata.create_all(self.engine)
        self.session = Session(self.engine)
        self.session.add(
            UsuarioRegistro(
                id=self.usuario_id,
                nome="Estudante",
                email="estudante@example.test",
                hash_senha="hash",
            )
        )
        # Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
        self.session.flush()
        self.session.add(
            CurriculoRegistro(
                id=self.curriculo_id,
                usuario_id=self.usuario_id,
                titulo_versao="Versão principal",
                layout="simples",
                is_public=False,
            )
        )
        self.session.commit()

    def tearDown(self) -> None:
        """Fecha sessão e engine do banco temporário.

        O método libera os recursos locais após cada cenário. Ele existe para
        impedir que conexões ou transações contaminem outros testes.
        """
        self.session.close()
        self.engine.dispose()

    def _salvar(self, associacao: AssociacaoCurriculoVaga) -> None:
        """Adiciona os registros mapeados à sessão de teste.

        O helper usa as mesmas conversões ORM empregadas pelo adapter e deixa o
        commit explícito no próprio cenário. Ele existe para isolar o schema
        relacional do problema de driver assíncrono no ambiente de teste.
        """
        self.session.add(para_registro(associacao))
        self.session.add_all(para_registros_classificacoes(associacao))

    def test_round_trip_persiste_todas_as_classificacoes_normalizadas(self) -> None:
        """Grava e reconstrói candidatura com interesse em tabelas relacionais.

        O teste salva por mapeadores, consulta a raiz e suas classificações e
        reconstrói o agregado. Ele existe para cobrir round-trip e normalização
        sem replicar a regra da #131.
        """
        associacao = AssociacaoCurriculoVaga(
            curriculo_id=CurriculoId(self.curriculo_id),
            vaga_id=VagaId("vaga-round-trip"),
            classificacoes=(ClassificacaoAssociacao.CANDIDATURA,),
        )

        self._salvar(associacao)
        self.session.commit()

        registro = self.session.get(
            AssociacaoCurriculoVagaRegistro,
            (self.curriculo_id, "vaga-round-trip"),
        )
        classificacoes = self.session.scalars(
            select(ClassificacaoAssociacaoRegistro).where(
                ClassificacaoAssociacaoRegistro.curriculo_id == self.curriculo_id,
                ClassificacaoAssociacaoRegistro.vaga_id == "vaga-round-trip",
            )
        ).all()
        reconstruida = para_associacao(registro, classificacoes)

        self.assertEqual(reconstruida.classificacoes, associacao.classificacoes)
        self.assertEqual(
            {item.classificacao for item in classificacoes},
            {"candidatura", "interesse"},
        )

    def test_chave_composta_rejeita_associacao_duplicada_sem_alterar_estado(
        self,
    ) -> None:
        """Impede gravar novamente o mesmo par e preserva as linhas existentes.

        O teste confirma a primeira gravação e espera violação de PK na segunda,
        depois consulta o estado após rollback. Ele existe para provar a proteção
        de duplicidade no banco e a ausência de atualização implícita.
        """
        original = AssociacaoCurriculoVaga(
            curriculo_id=CurriculoId(self.curriculo_id),
            vaga_id=VagaId("vaga-unica"),
            classificacoes=(ClassificacaoAssociacao.INTERESSE,),
        )
        self._salvar(original)
        self.session.commit()

        duplicada = AssociacaoCurriculoVaga(
            curriculo_id=CurriculoId(self.curriculo_id),
            vaga_id=VagaId("vaga-unica"),
            classificacoes=(ClassificacaoAssociacao.CANDIDATURA,),
        )
        self._salvar(duplicada)
        with self.assertRaises(IntegrityError):
            self.session.flush()
        self.session.rollback()

        total_associacoes = self.session.scalar(
            select(func.count()).select_from(AssociacaoCurriculoVagaRegistro)
        )
        classificacoes = self.session.scalars(
            select(ClassificacaoAssociacaoRegistro).where(
                ClassificacaoAssociacaoRegistro.curriculo_id == self.curriculo_id,
                ClassificacaoAssociacaoRegistro.vaga_id == "vaga-unica",
            )
        ).all()

        self.assertEqual(total_associacoes, 1)
        self.assertEqual(
            {item.classificacao for item in classificacoes},
            {"interesse"},
        )

    def test_falha_em_classificacao_reverte_raiz_da_associacao(self) -> None:
        """Garante rollback integral quando uma linha dependente falha.

        O teste tenta inserir uma classificação cuja chave aponta para vaga
        diferente da raiz, provoca violação de FK e verifica ausência da raiz
        após rollback. Ele existe para comprovar que o transaction boundary pode
        manter associação e classificações atômicas.
        """
        self.session.add(
            AssociacaoCurriculoVagaRegistro(
                curriculo_id=self.curriculo_id,
                vaga_id="vaga-com-falha",
            )
        )
        self.session.add(
            ClassificacaoAssociacaoRegistro(
                curriculo_id=self.curriculo_id,
                vaga_id="vaga-inexistente",
                classificacao="interesse",
            )
        )

        with self.assertRaises(IntegrityError):
            self.session.flush()
        self.session.rollback()

        registro = self.session.get(
            AssociacaoCurriculoVagaRegistro,
            (self.curriculo_id, "vaga-com-falha"),
        )
        self.assertIsNone(registro)

    def test_atualizacao_de_classificacoes_persiste_e_rollback_restaura_estado(
        self,
    ) -> None:
        """Persiste a remoção sem recriar a raiz e prova rollback integral.

        O cenário altera somente linhas de classificação numa sessão SQLite,
        confirma o resultado e depois repete a mutação seguida de rollback. Ele
        existe para demonstrar atomicidade no escopo transacional do chamador.
        """
        associacao = AssociacaoCurriculoVaga(
            CurriculoId(self.curriculo_id),
            VagaId("vaga-atualizada"),
            (ClassificacaoAssociacao.CANDIDATURA,),
        )
        self._salvar(associacao)
        self.session.commit()

        associacao.remover_classificacao(ClassificacaoAssociacao.CANDIDATURA)
        self.session.execute(
            delete(ClassificacaoAssociacaoRegistro).where(
                ClassificacaoAssociacaoRegistro.curriculo_id == self.curriculo_id,
                ClassificacaoAssociacaoRegistro.vaga_id == "vaga-atualizada",
            )
        )
        self.session.add_all(para_registros_classificacoes(associacao))
        self.session.commit()

        registro = self.session.get(
            AssociacaoCurriculoVagaRegistro,
            (self.curriculo_id, "vaga-atualizada"),
        )
        classificacoes = self.session.scalars(
            select(ClassificacaoAssociacaoRegistro).where(
                ClassificacaoAssociacaoRegistro.curriculo_id == self.curriculo_id,
                ClassificacaoAssociacaoRegistro.vaga_id == "vaga-atualizada",
            )
        ).all()
        self.assertIsNotNone(registro)
        self.assertEqual(
            {item.classificacao for item in classificacoes},
            {"interesse"},
        )

        associacao.adicionar_classificacao(ClassificacaoAssociacao.COMPATIBILIDADE)
        self.session.execute(
            delete(ClassificacaoAssociacaoRegistro).where(
                ClassificacaoAssociacaoRegistro.curriculo_id == self.curriculo_id,
                ClassificacaoAssociacaoRegistro.vaga_id == "vaga-atualizada",
            )
        )
        self.session.add_all(para_registros_classificacoes(associacao))
        self.session.flush()
        self.session.rollback()

        classificacoes_apos_rollback = self.session.scalars(
            select(ClassificacaoAssociacaoRegistro).where(
                ClassificacaoAssociacaoRegistro.curriculo_id == self.curriculo_id,
                ClassificacaoAssociacaoRegistro.vaga_id == "vaga-atualizada",
            )
        ).all()
        self.assertEqual(
            {item.classificacao for item in classificacoes_apos_rollback},
            {"interesse"},
        )
