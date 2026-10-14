"""Testa unitariamente o mapeamento e o repositório SQLAlchemy de competências."""

import unittest
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.cadastro_competencia import CompetenciaJaCadastrada
from backend.domain import CategoriaCompetencia, Competencia, CompetenciaId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.competencia import (
    CompetenciaRegistro,
    para_competencia,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_competencia import (
    RepositorioCompetenciaSqlAlchemy,
)

# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
ID_COMPETENCIA = UUID("00000000-0000-0000-0000-0000000000c1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def criar_competencia() -> Competencia:
    """Cria uma competência determinística para os testes de fronteira ORM.

    A função usa identificadores fixos e a categoria válida para comparar
    conversões e chamadas sem banco ou aleatoriedade. Ela existe para manter
    os cenários focados no comportamento observável do adapter.
    """
    return Competencia(
        id=CompetenciaId(ID_COMPETENCIA),
        usuario_id=UsuarioId(ID_USUARIO),
        categoria=CategoriaCompetencia.TECNICA,
        descricao="Power   BI",
        nivel="Avançado",
    )


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class MapeamentoCompetenciaTestCase(unittest.TestCase):
    """Verifica conversões puras entre competência e seu modelo ORM.

    A classe cria registros somente em memória e compara seus valores
    persistíveis. Ela existe para proteger a fronteira sem abrir conexão ou
    depender de infraestrutura de banco.
    """

    def test_converte_entidade_para_registro_com_chave_normalizada(self) -> None:
        """Mantém a chave canônica e os campos exibíveis na conversão ao ORM.

        O cenário mapeia a entidade e compara a categoria serializada e a
        descrição preservada. Ele existe para impedir que persistência redefina
        a política de duplicidade aplicada no núcleo.
        """
        registro = para_registro(criar_competencia())

        self.assertIsInstance(registro, CompetenciaRegistro)
        self.assertEqual(registro.id, ID_COMPETENCIA)
        self.assertEqual(registro.usuario_id, ID_USUARIO)
        self.assertEqual(registro.categoria, "tecnica")
        self.assertEqual(registro.descricao, "Power   BI")
        self.assertEqual(registro.descricao_normalizada, "power bi")

    def test_reconstroi_entidade_tipando_categoria(self) -> None:
        """Reconstrói value objects e enumeração a partir das colunas ORM.

        O cenário percorre ambos os mapeadores e compara a entidade resultante
        com a origem. Ele existe para evitar que dados instrumentados escapem
        para domínio e Application.
        """
        self.assertEqual(
            para_competencia(para_registro(criar_competencia())), criar_competencia()
        )


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class RepositorioCompetenciaSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o adapter com sessão SQLAlchemy substituída por double.

    Os cenários observam query, add, flush e tradução de erro com mocks, sem
    iniciar banco ou transação real. A classe existe para testar a porta na sua
    fronteira unitária permitida.
    """

    async def test_consulta_chave_normalizada_por_usuario_e_categoria(self) -> None:
        """Retorna verdadeiro quando a sessão encontra uma chave equivalente.

        O teste configura apenas ``scalar`` no double e observa o resultado da
        consulta. Ele existe para assegurar que a prevenção prévia usa a chave
        técnica, não a descrição exibível ou o nível.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = ID_COMPETENCIA
        repositorio = RepositorioCompetenciaSqlAlchemy(session)

        existe = await repositorio.existe_por_chave_de_duplicidade(
            UsuarioId(ID_USUARIO), CategoriaCompetencia.TECNICA, "power bi"
        )

        self.assertTrue(existe)
        session.scalar.assert_awaited_once()

    async def test_adiciona_registro_e_aguarda_flush_sem_commit(self) -> None:
        """Envia registro mapeado à sessão sem finalizar a transação.

        O cenário usa uma sessão mockada e examina o registro entregue a
        ``add``. Ele existe para preservar a responsabilidade transacional da
        composição externa.
        """
        session = MagicMock(spec=AsyncSession)
        repositorio = RepositorioCompetenciaSqlAlchemy(session)

        await repositorio.salvar(criar_competencia())

        registro = session.add.call_args.args[0]
        self.assertIsInstance(registro, CompetenciaRegistro)
        self.assertEqual(registro.descricao_normalizada, "power bi")
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()

    async def test_traduz_violacao_da_constraint_de_duplicidade(self) -> None:
        """Converte somente a colisão nomeada em falha conhecida da Application.

        O double faz ``flush`` levantar ``IntegrityError`` contendo o nome da
        constraint. Ele existe para garantir a proteção contra corrida sem
        vazar SQL pela porta de persistência.
        """
        session = MagicMock(spec=AsyncSession)
        session.flush.side_effect = IntegrityError(
            statement=None,
            params=None,
            orig=RuntimeError(
                'constraint "uq_competencias_usuario_categoria_descricao_normalizada"'
            ),
        )
        repositorio = RepositorioCompetenciaSqlAlchemy(session)

        with self.assertRaises(CompetenciaJaCadastrada):
            await repositorio.salvar(criar_competencia())
