"""Testa unitariamente o mapeamento e o repositório SQLAlchemy de cursos."""

import unittest
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
from backend.application.cadastro_curso import CursoJaCadastrado
from backend.domain import Curso, CursoId, UsuarioId
from backend.infrastructure.identificadores.geradores import GeradorCursoIdUuid4
from backend.infrastructure.persistence.sqlalchemy.curso import (
    CursoRegistro,
    para_curso,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_curso import (
    RepositorioCursoSqlAlchemy,
)

ID_CURSO = UUID("00000000-0000-0000-0000-0000000000c1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
def criar_curso(carga_horaria: int | None = 60) -> Curso:
    """Cria um curso determinístico para os testes de fronteira ORM.

    A função usa identificadores fixos para comparar conversões e chamadas sem
    banco ou aleatoriedade. Ela existe para manter os cenários focados no
    comportamento observável do adapter.
    """
    return Curso(
        id=CursoId(ID_CURSO),
        usuario_id=UsuarioId(ID_USUARIO),
        nome="Docker e Kubernetes",
        instituicao="Linux Foundation",
        carga_horaria=carga_horaria,
    )


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class MapeamentoCursoTestCase(unittest.TestCase):
    """Verifica conversões puras entre curso e seu modelo ORM.

    A classe cria registros somente em memória e compara seus valores
    persistíveis. Ela existe para proteger a fronteira sem abrir conexão ou
    depender de infraestrutura de banco.
    """

    def test_converte_entidade_para_registro_com_chaves_normalizadas(self) -> None:
        """Mantém as chaves canônicas e os campos exibíveis na conversão ao ORM.

        O cenário mapeia a entidade e compara os nomes serializados e as chaves
        calculadas. Ele existe para impedir que a persistência redefina a política
        de duplicidade aplicada no núcleo.
        """
        registro = para_registro(criar_curso(carga_horaria=80))

        self.assertIsInstance(registro, CursoRegistro)
        self.assertEqual(registro.id, ID_CURSO)
        self.assertEqual(registro.usuario_id, ID_USUARIO)
        self.assertEqual(registro.nome, "Docker e Kubernetes")
        self.assertEqual(registro.nome_normalizado, "docker e kubernetes")
        self.assertEqual(registro.instituicao, "Linux Foundation")
        self.assertEqual(registro.instituicao_normalizada, "linux foundation")
        self.assertEqual(registro.carga_horaria, 80)

    def test_converte_entidade_sem_carga_horaria_para_registro(self) -> None:
        """Converte curso sem carga horária gerando registro com valor nulo.

        O cenário testa a conversão de curso com carga_horaria None.
        Ele existe para validar o armazenamento de cursos sem duração mensurada.
        """
        registro = para_registro(criar_curso(carga_horaria=None))
        self.assertIsNone(registro.carga_horaria)

    def test_reconstroi_entidade_a_partir_de_registro(self) -> None:
        """Reconstrói value objects a partir das colunas ORM.

        O cenário percorre ambos os mapeadores e compara a entidade resultante
        com a origem. Ele existe para evitar que dados instrumentados escapem
        para domínio e Application.
        """
        self.assertEqual(para_curso(para_registro(criar_curso())), criar_curso())


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class RepositorioCursoSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o adapter com sessão SQLAlchemy substituída por double.

    Os cenários observam query, add, flush e tradução de erro com mocks, sem
    iniciar banco ou transação real. A classe existe para testar a porta na sua
    fronteira unitária permitida.
    """

    async def test_consulta_chave_normalizada_composta_por_usuario(self) -> None:
        """Retorna verdadeiro quando a sessão encontra uma chave composta equivalente.

        O teste configura apenas ``scalar`` no double e observa o resultado da
        consulta. Ele existe para assegurar que a prevenção prévia usa a chave
        técnica composta (nome e instituição normalizados).
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = ID_CURSO
        repositorio = RepositorioCursoSqlAlchemy(session)

        existe = await repositorio.existe_por_chave_de_duplicidade(
            UsuarioId(ID_USUARIO), "docker e kubernetes", "linux foundation"
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
        repositorio = RepositorioCursoSqlAlchemy(session)

        await repositorio.salvar(criar_curso())

        registro = session.add.call_args.args[0]
        self.assertIsInstance(registro, CursoRegistro)
        self.assertEqual(registro.nome_normalizado, "docker e kubernetes")
        self.assertEqual(registro.instituicao_normalizada, "linux foundation")
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()

    async def test_traduz_violacao_da_constraint_de_duplicidade(self) -> None:
        """Converte somente a colisão nomeada em falha conhecida da Application.

        O double faz ``flush`` levantar ``IntegrityError`` contendo o nome da
        constraint uq_cursos_usuario_nome_instituicao_normalizados. Ele existe para
        garantir a proteção contra corrida sem vazar SQL pela porta de persistência.
        """
        session = MagicMock(spec=AsyncSession)
        session.flush.side_effect = IntegrityError(
            statement=None,
            params=None,
            orig=RuntimeError(
                'constraint "uq_cursos_usuario_nome_instituicao_normalizados"'
            ),
        )
        repositorio = RepositorioCursoSqlAlchemy(session)

        with self.assertRaises(CursoJaCadastrado):
            await repositorio.salvar(criar_curso())

    async def test_propaga_outros_erros_de_integridade(self) -> None:
        """Propaga erros de integridade não relacionados à constraint de duplicidade.

        O cenário simula uma falha externa qualquer, como chave estrangeira, e
        verifica que a exceção original é repassada. Ele existe para evitar
        mascarar problemas de banco inesperados como duplicidades.
        """
        session = MagicMock(spec=AsyncSession)
        session.flush.side_effect = IntegrityError(
            statement=None,
            params=None,
            orig=RuntimeError('foreign key "fk_outra"'),
        )
        repositorio = RepositorioCursoSqlAlchemy(session)

        with self.assertRaises(IntegrityError):
            await repositorio.salvar(criar_curso())


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class GeradorCursoIdUuid4TestCase(unittest.TestCase):
    """Testa a geração de IDs de curso com UUID4.

    A suíte executa o gerador e verifica se o value object retornado é válido.
    Ela existe para garantir a integridade do adapter de identificadores.
    """

    def test_gera_curso_id_com_uuid4(self) -> None:
        """Gera um CursoId válido com formato UUID4.

        O cenário invoca o método gerar e valida o tipo e valor retornado. Ele
        existe para assegurar que a implementação concreta atende à porta.
        """
        gerador = GeradorCursoIdUuid4()
        curso_id = gerador.gerar()

        self.assertIsInstance(curso_id, CursoId)
        self.assertIsInstance(curso_id.valor, UUID)
