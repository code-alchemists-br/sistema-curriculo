"""Testes unitários do adapter SQLAlchemy de associação currículo-vaga."""

from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

from sqlalchemy.dialects import postgresql
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
from backend.domain.value_objects import CurriculoId, UsuarioId, VagaId
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
        self.session.execute = AsyncMock()
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

    async def test_obter_para_atualizacao_carrega_agregado_e_bloqueia_raiz(
        self,
    ) -> None:
        """Reconstrói o agregado e emite lock PostgreSQL pela chave composta.

        O teste simula raiz e classificações retornadas por duas consultas e
        compila a primeira para PostgreSQL. Ele existe para proteger leitura
        serializada de atualizações concorrentes.
        """
        registro = AssociacaoCurriculoVagaRegistro(
            curriculo_id=self.curriculo_id.valor,
            vaga_id=self.vaga_id.valor,
        )
        registro_classificacao = ClassificacaoAssociacaoRegistro(
            curriculo_id=self.curriculo_id.valor,
            vaga_id=self.vaga_id.valor,
            classificacao="interesse",
        )
        resultado_raiz = MagicMock()
        resultado_raiz.scalar_one_or_none.return_value = registro
        resultado_classificacoes = MagicMock()
        resultado_classificacoes.scalars.return_value.all.return_value = [
            registro_classificacao
        ]
        self.session.execute.side_effect = [
            resultado_raiz,
            resultado_classificacoes,
        ]

        associacao = await self.repositorio.obter_para_atualizacao(
            self.curriculo_id, self.vaga_id
        )

        self.assertEqual(associacao.curriculo_id, self.curriculo_id)
        self.assertEqual(associacao.vaga_id, self.vaga_id)
        self.assertEqual(
            associacao.classificacoes,
            frozenset({ClassificacaoAssociacao.INTERESSE}),
        )
        consulta = self.session.execute.await_args_list[0].args[0]
        sql = str(consulta.compile(dialect=postgresql.dialect()))
        self.assertIn("FOR UPDATE", sql)
        self.assertIn("curriculo_id", sql)
        self.assertIn("vaga_id", sql)
        self.assertEqual(self.session.execute.await_count, 2)

    async def test_atualizar_classificacoes_altera_somente_linhas_dependentes(
        self,
    ) -> None:
        """Substitui classificações do par sem inserir a raiz ou confirmar.

        O teste verifica a condição do DELETE, as linhas adicionadas e um flush
        único. Ele existe para fixar a fronteira transacional do adapter.
        """
        self.associacao.remover_classificacao(ClassificacaoAssociacao.CANDIDATURA)

        await self.repositorio.atualizar_classificacoes(self.associacao)

        consulta = self.session.execute.await_args.args[0]
        sql = str(consulta.compile(dialect=postgresql.dialect()))
        self.assertIn("DELETE FROM classificacoes_associacao_curriculo_vaga", sql)
        self.assertIn("curriculo_id", sql)
        self.assertIn("vaga_id", sql)
        linhas = self.session.add_all.call_args.args[0]
        self.assertEqual(len(linhas), 1)
        self.assertIsInstance(linhas[0], ClassificacaoAssociacaoRegistro)
        self.assertEqual(linhas[0].classificacao, "interesse")
        self.session.add.assert_not_called()
        self.assertEqual(self.session.flush.await_count, 2)
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


# Proveniência: decision-analysis prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md#v001
class ConsultaRepositorioAssociacaoCurriculoVagaTestCase(IsolatedAsyncioTestCase):
    """Verifica a consulta paginada com AsyncSession substituída.

    Os testes inspecionam a query compilada e controlam suas linhas por doubles,
    sem iniciar um banco. Eles existem para validar filtro, ordenação, paginação
    e reconstrução de agregados na fronteira SQLAlchemy.
    """

    def setUp(self) -> None:
        """Prepara um adapter e sessão assíncrona simulada.

        A sessão recebe resultados determinísticos em cada teste. A preparação
        existe para isolar a implementação SQLAlchemy de qualquer I/O real.
        """
        self.session = MagicMock(spec=AsyncSession)
        self.session.scalars = AsyncMock()
        self.repositorio = RepositorioAssociacaoCurriculoVagaSqlAlchemy(self.session)

    async def test_lista_pagina_do_usuario_com_filtro_ordenacao_e_mapeamento(
        self,
    ) -> None:
        """Compila filtro anterior à paginação e reconstrói os agregados da página.

        O teste verifica o join, o proprietário, a chave de ordenação, offset e
        limit, e controla as linhas devolvidas para duas consultas. Ele existe
        para provar que a página é filtrada e devolvida como domínio.
        """
        usuario_id = UsuarioId(UUID("00000000-0000-0000-0000-000000000301"))
        curriculo_a = UUID("00000000-0000-0000-0000-000000000101")
        curriculo_b = UUID("00000000-0000-0000-0000-000000000102")
        registros = [
            AssociacaoCurriculoVagaRegistro(
                curriculo_id=curriculo_a,
                vaga_id="vaga-a",
            ),
            AssociacaoCurriculoVagaRegistro(
                curriculo_id=curriculo_b,
                vaga_id="vaga-b",
            ),
        ]
        linhas = [
            ClassificacaoAssociacaoRegistro(
                curriculo_id=curriculo_a,
                vaga_id="vaga-a",
                classificacao="interesse",
            ),
            ClassificacaoAssociacaoRegistro(
                curriculo_id=curriculo_b,
                vaga_id="vaga-b",
                classificacao="compatibilidade",
            ),
        ]
        resultado_registros = MagicMock()
        resultado_registros.all.return_value = registros
        resultado_classificacoes = MagicMock()
        resultado_classificacoes.all.return_value = linhas
        self.session.scalars.side_effect = [
            resultado_registros,
            resultado_classificacoes,
        ]

        resultado = await self.repositorio.listar_por_usuario(
            usuario_id,
            offset=10,
            limit=5,
        )

        self.assertEqual(
            tuple((item.curriculo_id.valor, item.vaga_id.valor) for item in resultado),
            ((curriculo_a, "vaga-a"), (curriculo_b, "vaga-b")),
        )
        self.assertEqual(
            resultado[0].classificacoes,
            frozenset({ClassificacaoAssociacao.INTERESSE}),
        )
        self.assertEqual(
            resultado[1].classificacoes,
            frozenset({ClassificacaoAssociacao.COMPATIBILIDADE}),
        )
        self.assertEqual(self.session.scalars.await_count, 2)

        consulta = self.session.scalars.await_args_list[0].args[0]
        compilada = consulta.compile(dialect=postgresql.dialect())
        sql = str(compilada)
        self.assertIn("JOIN curriculos", sql)
        self.assertIn("WHERE curriculos.usuario_id", sql)
        self.assertIn(
            "ORDER BY associacoes_curriculo_vaga.curriculo_id, "
            "associacoes_curriculo_vaga.vaga_id",
            sql,
        )
        self.assertLess(sql.index("WHERE"), sql.index("ORDER BY"))
        self.assertLess(sql.index("ORDER BY"), sql.index("LIMIT"))
        self.assertIn("OFFSET", sql)
        self.assertIn(usuario_id.valor, compilada.params.values())
        self.assertIn(10, compilada.params.values())
        self.assertIn(5, compilada.params.values())

    async def test_pagina_vazia_nao_consulta_classificacoes(self) -> None:
        """Devolve tupla vazia e evita uma consulta secundária desnecessária.

        A sessão simulada devolve zero associações na primeira consulta. O teste
        existe para manter resultado vazio eficiente e não produzir consultas
        de classificações sem pares.
        """
        resultado_registros = MagicMock()
        resultado_registros.all.return_value = []
        self.session.scalars.return_value = resultado_registros

        resultado = await self.repositorio.listar_por_usuario(
            UsuarioId(UUID("00000000-0000-0000-0000-000000000302")),
            offset=0,
            limit=10,
        )

        self.assertEqual(resultado, ())
        self.session.scalars.assert_awaited_once()


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
