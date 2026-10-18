"""Testes unitários do adapter SQLAlchemy de associação currículo-vaga."""

from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
from backend.application.associacao_curriculo_vaga import (
    AssociacaoCurriculoVagaJaExiste,
)
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
from backend.infrastructure.persistence.sqlalchemy.repositorio_associacao_curriculo_vaga import (
    RepositorioAssociacaoCurriculoVagaSqlAlchemy,
)


class RepositorioAssociacaoCurriculoVagaSqlAlchemyTestCase(IsolatedAsyncioTestCase):
    """Verifica conversões e contrato do adapter sem iniciar um banco real.

    Os testes usam AsyncSession simulada para observar leitura, flush e tradução
    de falhas de integridade. Eles existem para garantir a fronteira do adapter
    e que o controle transacional permaneça fora dele.
    """

    def setUp(self) -> None:
        """Prepara sessão simulada e agregado conhecido para os cenários.

        Os doubles isolam o adapter de I/O e os IDs fixos tornam as assertions
        determinísticas. A preparação existe para focar nos contratos SQLAlchemy.
        """
        self.curriculo_id = CurriculoId(UUID("00000000-0000-0000-0000-000000000101"))
        self.vaga_id = VagaId("vaga-102")
        self.associacao = AssociacaoCurriculoVaga(
            curriculo_id=self.curriculo_id,
            vaga_id=self.vaga_id,
            classificacoes=(ClassificacaoAssociacao.CANDIDATURA,),
        )
        self.session = MagicMock(spec=AsyncSession)
        self.session.get = AsyncMock()
        self.session.flush = AsyncMock()
        self.repositorio = RepositorioAssociacaoCurriculoVagaSqlAlchemy(self.session)

    async def test_existe_por_par_consulta_chave_composta(self) -> None:
        """Consulta o registro pela identidade natural da associação.

        O teste configura um registro retornado pelo double e verifica classe e
        tupla de identidade usados por ``AsyncSession.get``. Ele existe para
        fixar a consulta preventiva exigida pelo port.
        """
        registro = AssociacaoCurriculoVagaRegistro(
            curriculo_id=self.curriculo_id.valor,
            vaga_id=self.vaga_id.valor,
        )
        self.session.get.return_value = registro

        existe = await self.repositorio.existe_por_par(self.curriculo_id, self.vaga_id)

        self.assertTrue(existe)
        self.session.get.assert_awaited_once_with(
            AssociacaoCurriculoVagaRegistro,
            (self.curriculo_id.valor, self.vaga_id.valor),
        )

    async def test_salvar_persiste_classificacoes_normalizadas_em_um_flush(
        self,
    ) -> None:
        """Envia associação e classificações normalizadas num único flush.

        O teste captura as instâncias adicionadas à sessão e confirma a presença
        de interesse inferido pelo Domain, além de ausência de commit. Ele existe
        para garantir persistência completa sem duplicar a regra da #131.
        """
        await self.repositorio.salvar(self.associacao)

        registros = [chamada.args[0] for chamada in self.session.add.call_args_list]
        self.assertEqual(len(registros), 3)
        self.assertIsInstance(registros[0], AssociacaoCurriculoVagaRegistro)
        classificacoes = {
            registro.classificacao
            for registro in registros[1:]
            if isinstance(registro, ClassificacaoAssociacaoRegistro)
        }
        self.assertEqual(classificacoes, {"candidatura", "interesse"})
        self.session.flush.assert_awaited_once_with()
        self.session.commit.assert_not_awaited()
        self.session.rollback.assert_not_awaited()

    async def test_salvar_traduz_colisao_da_chave_composta(self) -> None:
        """Converte colisão da PK da associação para erro da Application.

        O teste simula diagnóstico PostgreSQL com o nome da constraint aprovado
        e verifica a falha exposta pelo port. Ele existe para cobrir a corrida
        entre a pré-checagem e a inserção no banco.
        """
        erro_integridade = IntegrityError(
            "INSERT",
            {},
            SimpleNamespace(
                diag=SimpleNamespace(constraint_name="pk_associacoes_curriculo_vaga")
            ),
        )
        self.session.flush.side_effect = erro_integridade

        with self.assertRaises(AssociacaoCurriculoVagaJaExiste) as contexto:
            await self.repositorio.salvar(self.associacao)

        self.assertIs(contexto.exception.__cause__, erro_integridade)
        self.session.commit.assert_not_awaited()

    async def test_salvar_traduz_mensagem_exata_de_chave_composta_sqlite(self) -> None:
        """Reconhece a colisão da PK no SQLite usado pelos testes locais.

        O teste simula a mensagem exata do driver SQLite sem constraint name e
        confirma a mesma falha de Application. Ele existe para cobrir o formato
        do backend de persistência descartável do projeto.
        """
        erro_integridade = IntegrityError(
            "INSERT",
            {},
            Exception(
                "UNIQUE constraint failed: "
                "associacoes_curriculo_vaga.curriculo_id, "
                "associacoes_curriculo_vaga.vaga_id"
            ),
        )
        self.session.flush.side_effect = erro_integridade

        with self.assertRaises(AssociacaoCurriculoVagaJaExiste) as contexto:
            await self.repositorio.salvar(self.associacao)

        self.assertIs(contexto.exception.__cause__, erro_integridade)

    async def test_salvar_propaga_violacao_de_outra_constraint(self) -> None:
        """Não mascara falhas de integridade alheias à duplicidade da associação.

        O teste simula violação com outro nome de constraint e confirma que a
        mesma exceção SQLAlchemy segue ao boundary externo. Ele existe para
        evitar transformar erros internos em conflito de negócio.
        """
        erro_integridade = IntegrityError(
            "INSERT",
            {},
            SimpleNamespace(
                diag=SimpleNamespace(constraint_name="fk_curriculos_usuario_id")
            ),
        )
        self.session.flush.side_effect = erro_integridade

        with self.assertRaises(IntegrityError) as contexto:
            await self.repositorio.salvar(self.associacao)

        self.assertIs(contexto.exception, erro_integridade)


class MapeamentoAssociacaoCurriculoVagaTestCase(TestCase):
    """Verifica conversão ORM e identidade sem depender de sessão persistente.

    O teste constrói registros e reconstrói o agregado usando os mapeadores
    públicos do módulo. Ele existe para garantir round-trip de valores e
    classificações antes da integração com um banco.
    """

    def test_mapeadores_reconstroem_classificacoes_do_agregado(self) -> None:
        """Reconstrói candidatura e interesse através dos registros relacionais.

        O teste converte um agregado normalizado em registros e volta a domínio,
        comparando IDs e classificações. Ele existe para assegurar que a leitura
        ORM preserve o estado aprovado pela regra da #131.
        """
        original = AssociacaoCurriculoVaga(
            curriculo_id=CurriculoId(UUID("00000000-0000-0000-0000-000000000201")),
            vaga_id=VagaId("vaga-202"),
            classificacoes=(ClassificacaoAssociacao.CANDIDATURA,),
        )
        registro = para_registro(original)
        registros_classificacoes = para_registros_classificacoes(original)

        reconstruida = para_associacao(registro, registros_classificacoes)

        self.assertEqual(reconstruida.curriculo_id, original.curriculo_id)
        self.assertEqual(reconstruida.vaga_id, original.vaga_id)
        self.assertEqual(reconstruida.classificacoes, original.classificacoes)

    def test_mapping_define_chave_primaria_composta(self) -> None:
        """Confirma que a tabela ORM usa o par aprovado como identidade.

        O teste lê as colunas de primary key registradas na metadata declarativa.
        Ele existe para impedir a introdução acidental de um ID técnico.
        """
        self.assertEqual(
            tuple(
                coluna.name
                for coluna in AssociacaoCurriculoVagaRegistro.__table__.primary_key.columns
            ),
            ("curriculo_id", "vaga_id"),
        )
