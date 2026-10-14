"""Verifica o mapeamento e repository de experiências com doubles locais."""

import unittest
from datetime import date
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
