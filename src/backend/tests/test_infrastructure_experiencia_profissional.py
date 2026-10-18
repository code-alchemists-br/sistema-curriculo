"""Verifica o mapeamento e repository de experiências com doubles locais."""

import unittest
from datetime import date, datetime, timezone
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain import (
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    Periodo,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.experiencia_profissional import (
    ExperienciaProfissionalRegistro,
    para_experiencia,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_experiencia_profissional import (
    RepositorioExperienciaProfissionalSqlAlchemy,
)

ID_EXPERIENCIA = UUID("00000000-0000-0000-0000-0000000000e1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


def criar_experiencia() -> ExperienciaProfissional:
    """Cria entidade de experiência válida com dados determinísticos.

    O helper usa UUIDs e datas fixas para comparar mapping sem relógio, rede ou
    banco. Ele existe para manter os cenários focados na fronteira ORM.
    """
    return ExperienciaProfissional(
        id=ExperienciaProfissionalId(ID_EXPERIENCIA),
        usuario_id=UsuarioId(ID_USUARIO),
        empresa="Instituto Exemplo",
        cargo="Desenvolvedora",
        descricao="Construiu integrações.",
        periodo=Periodo(date(2022, 1, 1), date(2024, 2, 1)),
    )


class MapeamentoExperienciaProfissionalTestCase(unittest.TestCase):
    """Verifica mapeamentos puros da entidade para o ORM e de volta.

    A classe usa um registro criado em memória e compara value objects. Ela
    existe para proteger a fronteira sem abrir conexão SQLAlchemy.
    """

    def test_converte_entidade_para_colunas_de_persistencia(self) -> None:
        """Confirma que identidades e datas viram colunas persistíveis.

        O teste converte a entidade e compara os atributos do registro. Ele
        existe para manter o modelo relacional alinhado ao contrato interno.
        """
        registro = para_registro(criar_experiencia())

        self.assertIsInstance(registro, ExperienciaProfissionalRegistro)
        self.assertEqual(registro.id, ID_EXPERIENCIA)
        self.assertEqual(registro.usuario_id, ID_USUARIO)
        self.assertEqual(registro.data_inicio, date(2022, 1, 1))
        self.assertEqual(registro.data_fim, date(2024, 2, 1))

    def test_reconstroi_entidade_e_reaplica_value_objects(self) -> None:
        """Confirma reconstrução de identidades e período a partir do ORM.

        O teste percorre os dois mapeadores e compara a entidade resultante.
        Ele existe para não propagar modelos instrumentados ao núcleo.
        """
        entidade = para_experiencia(para_registro(criar_experiencia()))

        self.assertEqual(entidade, criar_experiencia())

    def test_mapeia_instante_de_exclusao_nos_dois_sentidos(self) -> None:
        """Confirma que ``deleted_at`` atravessa a fronteira ORM sem perdas.

        O teste converte uma experiência excluída para registro e de volta e
        compara o marcador. Ele existe para que a exclusão lógica persistida
        seja reconhecida pelo domínio na leitura.
        """
        instante = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
        excluida = criar_experiencia().excluir(instante)

        registro = para_registro(excluida)

        self.assertEqual(registro.deleted_at, instante)
        self.assertEqual(para_experiencia(registro), excluida)


class RepositorioExperienciaProfissionalSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica operações do repository com AsyncSession substituída.

    Os testes inspecionam add, flush e propagação de erro sem banco real. A
    classe existe para proteger a implementação da porta externa.
    """

    async def test_adiciona_registro_e_aguarda_flush_sem_commit(self) -> None:
        """Confirma que salvar mapeia e envia registro sem commit próprio.

        O cenário usa AsyncSession mockada e observa add/flush. Ele existe para
        deixar transação e commit sob controle da composição da requisição.
        """
        session = MagicMock(spec=AsyncSession)
        repositorio = RepositorioExperienciaProfissionalSqlAlchemy(session)
        experiencia = criar_experiencia()

        await repositorio.salvar(experiencia)

        registro = session.add.call_args.args[0]
        self.assertIsInstance(registro, ExperienciaProfissionalRegistro)
        self.assertEqual(registro.id, ID_EXPERIENCIA)
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()

    async def test_propaga_falha_de_flush(self) -> None:
        """Confirma que erro de flush chega intacto à composição.

        O mock faz flush falhar e o teste exige a mesma exceção. Ele existe para
        evitar que o adapter esconda falhas de persistência.
        """
        session = MagicMock(spec=AsyncSession)
        session.flush.side_effect = RuntimeError("falha no banco")
        repositorio = RepositorioExperienciaProfissionalSqlAlchemy(session)

        with self.assertRaises(RuntimeError):
            await repositorio.salvar(criar_experiencia())

    async def test_obtem_experiencia_por_id_e_usuario_e_reconstroi_entidade(self) -> None:
        """Filtra simultaneamente identidade e proprietário na consulta.

        O teste configura um registro ORM e confere a entidade convertida e os
        parâmetros da instrução. Ele existe para assegurar que a busca nunca
        localize experiência apenas pelo ID informado pelo cliente.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = para_registro(criar_experiencia())
        repositorio = RepositorioExperienciaProfissionalSqlAlchemy(session)

        resultado = await repositorio.obter_por_id_e_usuario(
            ExperienciaProfissionalId(ID_EXPERIENCIA), UsuarioId(ID_USUARIO)
        )

        self.assertEqual(resultado, criar_experiencia())
        consulta = session.scalar.await_args.args[0]
        self.assertIn("experiencias_profissionais.id", str(consulta))
        self.assertIn("experiencias_profissionais.usuario_id", str(consulta))
        self.assertIn("experiencias_profissionais.deleted_at IS NULL", str(consulta))
        self.assertIn(ID_EXPERIENCIA, consulta.compile().params.values())
        self.assertIn(ID_USUARIO, consulta.compile().params.values())

    async def test_devolve_none_quando_id_ou_usuario_nao_correspondem(self) -> None:
        """Devolve ausência quando a consulta conjunta não encontra registro.

        A sessão sem resultado representa experiência inexistente ou de outro
        usuário, que o adapter não distingue. O teste existe para manter
        experiências alheias invisíveis no contrato da porta.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = None
        repositorio = RepositorioExperienciaProfissionalSqlAlchemy(session)

        resultado = await repositorio.obter_por_id_e_usuario(
            ExperienciaProfissionalId(ID_EXPERIENCIA),
            UsuarioId(UUID("00000000-0000-0000-0000-000000000099")),
        )

        self.assertIsNone(resultado)
        consulta = session.scalar.await_args.args[0]
        self.assertIn("experiencias_profissionais.usuario_id", str(consulta))

    async def test_atualiza_com_update_condicional_somente_campos_editaveis(self) -> None:
        """Atualiza textos e datas filtrando por ID e proprietário, sem commit.

        A instrução SQL e o rowcount do double representam a unidade do adapter,
        sem executar banco. O teste existe para garantir que a escrita não
        altere identidade nem dono e que só atinja a experiência do usuário.
        """
        editada = criar_experiencia().editar(
            empresa="Nova Empresa",
            cargo="Analista",
            descricao="Mantém APIs em produção.",
            periodo=Periodo(date(2024, 3, 1)),
        )
        session = MagicMock(spec=AsyncSession)
        session.execute.return_value.rowcount = 1
        repositorio = RepositorioExperienciaProfissionalSqlAlchemy(session)

        resultado = await repositorio.atualizar(editada)

        self.assertTrue(resultado)
        instrucao = session.execute.await_args.args[0]
        sql = str(instrucao)
        self.assertIn("experiencias_profissionais.id", sql)
        self.assertIn("experiencias_profissionais.usuario_id", sql)
        self.assertIn("experiencias_profissionais.deleted_at IS NULL", sql)
        valores = instrucao.compile().params
        self.assertEqual(
            set(valores),
            {"id_1", "usuario_id_1", "empresa", "cargo", "descricao", "data_inicio", "data_fim"},
        )
        self.assertEqual(valores["empresa"], "Nova Empresa")
        self.assertEqual(valores["id_1"], ID_EXPERIENCIA)
        self.assertEqual(valores["usuario_id_1"], ID_USUARIO)
        self.assertIsNone(valores["data_fim"])
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()

    async def test_atualizar_devolve_false_quando_update_nao_afeta_linha(self) -> None:
        """Representa ausência, propriedade divergente ou concorrência.

        O resultado SQL de zero linhas é devolvido sem nova leitura, para que a
        Application converta a condição em experiência não encontrada.
        """
        session = MagicMock(spec=AsyncSession)
        session.execute.return_value.rowcount = 0
        repositorio = RepositorioExperienciaProfissionalSqlAlchemy(session)

        resultado = await repositorio.atualizar(criar_experiencia())

        self.assertFalse(resultado)
        session.scalar.assert_not_awaited()

    async def test_obtem_incluindo_excluidas_sem_filtrar_marcador(self) -> None:
        """Reconstrói a própria experiência excluída filtrando só ID e dono.

        A sessão double devolve registro marcado e a consulta é inspecionada
        para confirmar o filtro de proprietário e a ausência do filtro de
        exclusão. O teste existe para sustentar a exclusão idempotente.
        """
        instante = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = para_registro(criar_experiencia().excluir(instante))
        repositorio = RepositorioExperienciaProfissionalSqlAlchemy(session)

        resultado = await repositorio.obter_por_id_e_usuario_incluindo_excluidas(
            ExperienciaProfissionalId(ID_EXPERIENCIA), UsuarioId(ID_USUARIO)
        )

        self.assertEqual(resultado.deleted_at, instante)
        consulta = session.scalar.await_args.args[0]
        self.assertIn("experiencias_profissionais.id", str(consulta))
        self.assertIn("experiencias_profissionais.usuario_id", str(consulta))
        self.assertNotIn("deleted_at IS NULL", str(consulta))

    async def test_obtem_incluindo_excluidas_devolve_none_para_ausente_ou_alheia(
        self,
    ) -> None:
        """Não revela registro ausente nem de outro proprietário.

        A consulta conjunta sem resultado devolve ``None``. O teste existe para
        que a busca usada pela exclusão também oculte dados de terceiros.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = None
        repositorio = RepositorioExperienciaProfissionalSqlAlchemy(session)

        resultado = await repositorio.obter_por_id_e_usuario_incluindo_excluidas(
            ExperienciaProfissionalId(ID_EXPERIENCIA), UsuarioId(ID_USUARIO)
        )

        self.assertIsNone(resultado)

    async def test_marcar_excluida_grava_somente_instante_em_registro_ativo(self) -> None:
        """Usa UPDATE condicional por ID, dono e ausência de marcador.

        A instrução SQL é inspecionada para confirmar os filtros e o único
        campo alterado, e o rowcount define o retorno; não há commit. O teste
        existe para que a exclusão não sobrescreva o primeiro instante.
        """
        instante = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
        session = MagicMock(spec=AsyncSession)
        session.execute.return_value.rowcount = 1
        repositorio = RepositorioExperienciaProfissionalSqlAlchemy(session)

        resultado = await repositorio.marcar_excluida(
            ExperienciaProfissionalId(ID_EXPERIENCIA), UsuarioId(ID_USUARIO), instante
        )

        self.assertTrue(resultado)
        instrucao = session.execute.await_args.args[0]
        sql = str(instrucao)
        self.assertIn("experiencias_profissionais.usuario_id", sql)
        self.assertIn("experiencias_profissionais.deleted_at IS NULL", sql)
        valores = instrucao.compile().params
        self.assertEqual(set(valores), {"id_1", "usuario_id_1", "deleted_at"})
        self.assertEqual(valores["deleted_at"], instante)
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()

    async def test_marcar_excluida_devolve_false_quando_nada_e_alterado(self) -> None:
        """Representa experiência já excluída, ausente ou de outro dono.

        O resultado SQL de zero linhas é devolvido como ``False``. O teste
        existe para que a Application detecte disputa concorrente e releia.
        """
        session = MagicMock(spec=AsyncSession)
        session.execute.return_value.rowcount = 0
        repositorio = RepositorioExperienciaProfissionalSqlAlchemy(session)

        resultado = await repositorio.marcar_excluida(
            ExperienciaProfissionalId(ID_EXPERIENCIA),
            UsuarioId(ID_USUARIO),
            datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc),
        )

        self.assertFalse(resultado)
