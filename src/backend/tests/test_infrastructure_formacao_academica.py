"""Testa o mapeamento SQLAlchemy e os metadados de formação acadêmica."""

import unittest
from datetime import date, datetime, timezone
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, String, Text
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import CreateTable

from backend.domain import (
    FormacaoAcademica,
    FormacaoAcademicaId,
    NivelFormacaoAcademica,
    Periodo,
    StatusFormacaoAcademica,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.formacao_academica import (
    FormacaoAcademicaRegistro,
    para_formacao_academica,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_formacao_academica import (
    RepositorioFormacaoAcademicaSqlAlchemy,
)

# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
ID_FORMACAO = UUID("00000000-0000-0000-0000-0000000000f1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
def criar_formacao() -> FormacaoAcademica:
    """Cria uma formação determinística válida para os testes do adapter.

    A entidade usa UUIDs estáveis, enums tipados e uma previsão futura. Ela
    existe para comparar conversões e chamadas sem abrir banco ou depender de
    aleatoriedade.
    """
    return FormacaoAcademica(
        id=FormacaoAcademicaId(ID_FORMACAO),
        usuario_id=UsuarioId(ID_USUARIO),
        instituicao="FATEC",
        curso="ADS",
        nivel=NivelFormacaoAcademica.TECNOLOGO,
        periodo=Periodo(date(2024, 2, 1), date(2030, 12, 1)),
        status=StatusFormacaoAcademica.EM_ANDAMENTO,
    )


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
class MapeamentoFormacaoAcademicaTestCase(unittest.TestCase):
    """Confere conversões puras entre entidade e modelo persistente.

    Os cenários constroem objetos em memória e verificam enums, identidades e
    datas serializados. Eles existem para proteger a fronteira ORM sem conexão.
    """

    def test_converte_entidade_em_registro_com_enums_textuais(self) -> None:
        """Armazena os valores canônicos dos enums em colunas de texto.

        O teste converte a entidade e compara os campos persistíveis. Ele
        existe para manter a representação independente de ENUM nativo.
        """
        registro = para_registro(criar_formacao())

        self.assertIsInstance(registro, FormacaoAcademicaRegistro)
        self.assertEqual(registro.id, ID_FORMACAO)
        self.assertEqual(registro.usuario_id, ID_USUARIO)
        self.assertEqual(registro.nivel, "tecnologo")
        self.assertEqual(registro.status, "em_andamento")
        self.assertEqual(registro.data_fim, date(2030, 12, 1))
        self.assertIsNone(registro.deleted_at)

    def test_reconstroi_entidade_com_enums_e_periodo_tipados(self) -> None:
        """Reconstrói tipos de domínio a partir das colunas SQLAlchemy.

        O teste percorre ambos os conversores e compara a entidade resultante
        com a original. Ele existe para impedir vazamento de registros ORM.
        """
        self.assertEqual(
            para_formacao_academica(para_registro(criar_formacao())), criar_formacao()
        )

    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    def test_mapeia_deleted_at_nos_dois_sentidos(self) -> None:
        """Preserva instante de exclusão na conversão em ambos os sentidos.

        A conversão parte de entidade marcada e reconstrói o registro e a
        entidade. O teste existe para não perder o estado lógico na persistência.
        """
        instante = datetime(2026, 10, 15, 12, tzinfo=timezone.utc)
        excluida = criar_formacao().excluir(instante)

        registro = para_registro(excluida)

        self.assertEqual(registro.deleted_at, instante)
        self.assertEqual(para_formacao_academica(registro).deleted_at, instante)

    def test_colunas_e_checks_refletem_o_contrato(self) -> None:
        """Confere tamanhos, armazenamento textual e nomes/expressões dos CHECKs.

        O teste inspeciona somente metadata SQLAlchemy, sem criar schema ou
        conectar em banco. Ele existe para detectar divergência estrutural antes
        de migrations serem aplicadas.
        """
        tabela = FormacaoAcademicaRegistro.__table__
        checks = {
            constraint.name: str(constraint.sqltext)
            for constraint in tabela.constraints
            if isinstance(constraint, CheckConstraint)
        }

        self.assertIsInstance(tabela.c.instituicao.type, String)
        self.assertEqual(tabela.c.instituicao.type.length, 200)
        self.assertEqual(tabela.c.curso.type.length, 200)
        self.assertIsInstance(tabela.c.nivel.type, Text)
        self.assertIsInstance(tabela.c.status.type, Text)
        self.assertIsInstance(tabela.c.deleted_at.type, DateTime)
        self.assertTrue(tabela.c.deleted_at.type.timezone)
        self.assertTrue(tabela.c.deleted_at.nullable)
        self.assertIn("length(trim(instituicao)) BETWEEN 1 AND 200", checks[
            "ck_formacoes_instituicao_tamanho"
        ])
        self.assertIn("length(trim(curso)) BETWEEN 1 AND 200", checks[
            "ck_formacoes_curso_tamanho"
        ])
        self.assertIn("doutorado", checks["ck_formacoes_nivel_valido"])
        self.assertIn("interrompido", checks["ck_formacoes_status_valido"])
        for nivel in NivelFormacaoAcademica:
            self.assertIn(nivel.value, checks["ck_formacoes_nivel_valido"])
        for status in StatusFormacaoAcademica:
            self.assertIn(status.value, checks["ck_formacoes_status_valido"])
        periodo = checks["ck_formacoes_status_periodo_coerente"]
        self.assertIn("status = 'em_andamento'", periodo)
        self.assertIn("status = 'concluido' AND data_fim IS NOT NULL", periodo)
        self.assertIn("status = 'interrompido'", periodo)
        self.assertIn("data_fim >= data_inicio", periodo)

    def test_schema_compila_em_postgresql_e_sqlite(self) -> None:
        """Confirma que colunas e CHECKs usam sintaxe comum aos dialetos.

        O teste compila a metadata para ambos os dialetos sem conexão nem
        execução de DDL. Ele existe para validar a portabilidade declarada pelo
        projeto entre PostgreSQL e o banco SQLite da fixture.
        """
        tabela = FormacaoAcademicaRegistro.__table__

        ddl_postgresql = str(CreateTable(tabela).compile(dialect=postgresql.dialect()))
        ddl_sqlite = str(CreateTable(tabela).compile(dialect=sqlite.dialect()))

        self.assertIn("ck_formacoes_status_periodo_coerente", ddl_postgresql)
        self.assertIn("ck_formacoes_status_periodo_coerente", ddl_sqlite)
        self.assertIn("length(trim(instituicao))", ddl_postgresql)
        self.assertIn("length(trim(instituicao))", ddl_sqlite)


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
class RepositorioFormacaoAcademicaSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Testa consulta e persistência com sessão SQLAlchemy substituída.

    A sessão mockada registra consultas, alterações e flush sem banco ou
    transação real. A classe existe para verificar a implementação da porta.
    """

    async def test_adiciona_modelo_mapeado_e_aguarda_flush_sem_commit(self) -> None:
        """Adiciona a formação convertida e deixa commit com a composição.

        O teste injeta AsyncSession double e confere registro, flush e ausência
        de commit. Ele existe para preservar o limite transacional do adapter.
        """
        session = MagicMock(spec=AsyncSession)
        repositorio = RepositorioFormacaoAcademicaSqlAlchemy(session)

        await repositorio.salvar(criar_formacao())

        registro = session.add.call_args.args[0]
        self.assertIsInstance(registro, FormacaoAcademicaRegistro)
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()
    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    async def test_obtem_formacao_por_id_e_usuario_e_reconstroi_entidade(self) -> None:
        """Filtra simultaneamente identidade e proprietário na consulta.

        O teste configura um registro ORM e confere o agregado convertido e os
        parâmetros da instrução. Ele existe para assegurar isolamento e
        preservar a fronteira de persistência.
        """
        session = MagicMock(spec=AsyncSession)
        registro = para_registro(criar_formacao())
        session.scalar.return_value = registro
        repositorio = RepositorioFormacaoAcademicaSqlAlchemy(session)

        resultado = await repositorio.obter_por_id_e_usuario(
            FormacaoAcademicaId(ID_FORMACAO), UsuarioId(ID_USUARIO)
        )

        self.assertEqual(resultado, criar_formacao())
        consulta = session.scalar.await_args.args[0]
        self.assertIn("formacoes_academicas.id", str(consulta))
        self.assertIn("formacoes_academicas.usuario_id", str(consulta))
        self.assertIn(ID_FORMACAO, consulta.compile().params.values())
        self.assertIn(ID_USUARIO, consulta.compile().params.values())

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    async def test_devolve_none_quando_id_ou_usuario_nao_correspondem(self) -> None:
        """Devolve ausência quando a consulta conjunta não encontra registro.

        O teste executa buscas com IDs diferentes contra uma sessão sem
        resultado. Ele existe para manter invisíveis formações inexistentes e
        de outro usuário no contrato da porta.
        """
        for formacao_id, usuario_id in (
            (FormacaoAcademicaId(ID_FORMACAO), UsuarioId(ID_USUARIO)),
            (
                FormacaoAcademicaId(ID_FORMACAO),
                UsuarioId(UUID("00000000-0000-0000-0000-000000000099")),
            ),
            (
                FormacaoAcademicaId(UUID("00000000-0000-0000-0000-000000000099")),
                UsuarioId(ID_USUARIO),
            ),
        ):
            with self.subTest(formacao_id=formacao_id, usuario_id=usuario_id):
                session = MagicMock(spec=AsyncSession)
                session.scalar.return_value = None
                repositorio = RepositorioFormacaoAcademicaSqlAlchemy(session)

                resultado = await repositorio.obter_por_id_e_usuario(
                    formacao_id, usuario_id
                )

                self.assertIsNone(resultado)
                consulta = session.scalar.await_args.args[0]
                self.assertIn("formacoes_academicas.id", str(consulta))
                self.assertIn("formacoes_academicas.usuario_id", str(consulta))
                self.assertIn("formacoes_academicas.deleted_at IS NULL", str(consulta))

    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    async def test_obtem_incluindo_excluidas_filtrando_id_e_proprietario(self) -> None:
        """Reconstrói a própria formação sem filtrar sua marca de exclusão.

        A sessão double devolve registro marcado e a expressão SQL é inspecionada
        para confirmar filtro de dono e ausência de consulta apenas por ID.
        """
        registro = para_registro(criar_formacao())
        registro.deleted_at = datetime(2026, 10, 15, tzinfo=timezone.utc)
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = registro
        repositorio = RepositorioFormacaoAcademicaSqlAlchemy(session)

        resultado = await repositorio.obter_por_id_e_usuario_incluindo_excluidas(
            FormacaoAcademicaId(ID_FORMACAO), UsuarioId(ID_USUARIO)
        )

        self.assertEqual(resultado.deleted_at, registro.deleted_at)
        consulta = session.scalar.await_args.args[0]
        self.assertIn("formacoes_academicas.id", str(consulta))
        self.assertIn("formacoes_academicas.usuario_id", str(consulta))
        self.assertNotIn("deleted_at IS NULL", str(consulta))
        self.assertIn(ID_FORMACAO, consulta.compile().params.values())
        self.assertIn(ID_USUARIO, consulta.compile().params.values())

    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    async def test_obtem_incluindo_excluidas_devolve_none_para_ausente_ou_alheia(self) -> None:
        """Não revela registro ausente nem de outro proprietário.

        A consulta conjunta retorna vazio para os cenários indistinguíveis e
        confirma ambos os filtros na instrução.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = None
        repositorio = RepositorioFormacaoAcademicaSqlAlchemy(session)

        resultado = await repositorio.obter_por_id_e_usuario_incluindo_excluidas(
            FormacaoAcademicaId(ID_FORMACAO), UsuarioId(ID_USUARIO)
        )

        self.assertIsNone(resultado)
        consulta = session.scalar.await_args.args[0]
        self.assertIn("formacoes_academicas.id", str(consulta))
        self.assertIn("formacoes_academicas.usuario_id", str(consulta))

    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    async def test_atualiza_com_update_condicional_somente_campos_editaveis(self) -> None:
        """Atualiza seis campos ativos sem carregar ou substituir identidades.

        A instrução SQL e o rowcount do double representam a unidade do adapter,
        sem executar banco ou alterar objetos ORM carregados.
        """
        original = criar_formacao()
        editada = original.editar(
            instituicao="Universidade Exemplo",
            curso="Ciência de Dados",
            nivel=NivelFormacaoAcademica.GRADUACAO,
            periodo=Periodo(date(2025, 1, 1), date(2031, 6, 1)),
            status=StatusFormacaoAcademica.CONCLUIDO,
        )
        session = MagicMock(spec=AsyncSession)
        session.execute.return_value.rowcount = 1
        repositorio = RepositorioFormacaoAcademicaSqlAlchemy(session)

        resultado = await repositorio.atualizar(editada)

        self.assertTrue(resultado)
        instrucao = session.execute.await_args.args[0]
        sql = str(instrucao)
        self.assertIn("formacoes_academicas.id", sql)
        self.assertIn("formacoes_academicas.usuario_id", sql)
        self.assertIn("formacoes_academicas.deleted_at IS NULL", sql)
        valores = instrucao.compile().params
        self.assertEqual(
            set(valores),
            {"id_1", "usuario_id_1", "instituicao", "curso", "nivel", "data_inicio", "data_fim", "status"},
        )
        self.assertNotIn("deleted_at", valores)
        self.assertNotIn("id", valores)
        self.assertNotIn("usuario_id", valores)
        self.assertEqual(valores["instituicao"], "Universidade Exemplo")
        session.scalar.assert_not_awaited()
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()

    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    async def test_atualizar_devolve_false_quando_update_nao_afeta_linha(self) -> None:
        """Representa ausência, propriedade divergente ou exclusão concorrente.

        O resultado SQL de zero linhas é devolvido sem nova leitura, para que a
        Application converta a condição em formação não encontrada.
        """
        for estado in ("excluída", "inexistente", "de outro usuário"):
            with self.subTest(estado=estado):
                session = MagicMock(spec=AsyncSession)
                session.execute.return_value.rowcount = 0
                repositorio = RepositorioFormacaoAcademicaSqlAlchemy(session)

                resultado = await repositorio.atualizar(criar_formacao())

                self.assertFalse(resultado)
                instrucao = session.execute.await_args.args[0]
                self.assertIn("formacoes_academicas.deleted_at IS NULL", str(instrucao))
                self.assertIn("formacoes_academicas.usuario_id", str(instrucao))
                session.scalar.assert_not_awaited()

    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    async def test_marcar_excluida_preserva_instante_na_repeticao(self) -> None:
        """Usa predicado ativo e retorna o rowcount sem sobrescrever repetição.

        Duas execuções simuladas mostram o primeiro sucesso e o zero seguinte;
        a instrução da segunda tentativa ainda exige coluna nula.
        """
        instante = datetime(2026, 10, 15, 12, tzinfo=timezone.utc)
        session = MagicMock(spec=AsyncSession)
        session.execute.side_effect = [MagicMock(rowcount=1), MagicMock(rowcount=0)]
        repositorio = RepositorioFormacaoAcademicaSqlAlchemy(session)

        primeira = await repositorio.marcar_excluida(
            FormacaoAcademicaId(ID_FORMACAO), UsuarioId(ID_USUARIO), instante
        )
        segunda = await repositorio.marcar_excluida(
            FormacaoAcademicaId(ID_FORMACAO), UsuarioId(ID_USUARIO), instante
        )

        self.assertTrue(primeira)
        self.assertFalse(segunda)
        for chamada in session.execute.await_args_list:
            instrucao = chamada.args[0]
            self.assertIn("formacoes_academicas.id", str(instrucao))
            self.assertIn("formacoes_academicas.usuario_id", str(instrucao))
            self.assertIn("formacoes_academicas.deleted_at IS NULL", str(instrucao))
            self.assertEqual(instrucao.compile().params["deleted_at"], instante)
        self.assertEqual(session.flush.await_count, 2)
        session.commit.assert_not_called()
