"""Testa o mapeamento SQLAlchemy e os metadados de formação acadêmica."""

import unittest
from datetime import date
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy import CheckConstraint, String, Text
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

    def test_reconstroi_entidade_com_enums_e_periodo_tipados(self) -> None:
        """Reconstrói tipos de domínio a partir das colunas SQLAlchemy.

        O teste percorre ambos os conversores e compara a entidade resultante
        com a original. Ele existe para impedir vazamento de registros ORM.
        """
        self.assertEqual(
            para_formacao_academica(para_registro(criar_formacao())), criar_formacao()
        )

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

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    async def test_atualiza_campos_mutaveis_preservando_identidades_e_sem_commit(
        self,
    ) -> None:
        """Atualiza as seis propriedades mutáveis no registro carregado.

        O teste usa um registro mapeado existente e verifica os novos textos,
        enums e datas, além de identidade, proprietário, flush e ausência de
        commit. Ele existe para proteger a tradução persistente da edição.
        """
        formacao_original = criar_formacao()
        formacao_editada = formacao_original.editar(
            instituicao="Universidade Exemplo",
            curso="Ciência de Dados",
            nivel=NivelFormacaoAcademica.GRADUACAO,
            periodo=Periodo(date(2025, 1, 1), date(2031, 6, 1)),
            status=StatusFormacaoAcademica.CONCLUIDO,
        )
        registro = para_registro(formacao_original)
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = registro
        repositorio = RepositorioFormacaoAcademicaSqlAlchemy(session)

        await repositorio.atualizar(formacao_editada)

        self.assertEqual(registro.id, ID_FORMACAO)
        self.assertEqual(registro.usuario_id, ID_USUARIO)
        self.assertEqual(registro.instituicao, "Universidade Exemplo")
        self.assertEqual(registro.curso, "Ciência de Dados")
        self.assertEqual(registro.nivel, "graduacao")
        self.assertEqual(registro.data_inicio, date(2025, 1, 1))
        self.assertEqual(registro.data_fim, date(2031, 6, 1))
        self.assertEqual(registro.status, "concluido")
        session.add.assert_not_called()
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()
