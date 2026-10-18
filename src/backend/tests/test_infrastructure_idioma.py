"""Testa unitariamente o mapeamento e o repositório SQLAlchemy de idiomas."""

import unittest
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
from backend.application.cadastro_idioma import IdiomaJaCadastrado
from backend.domain import Idioma, IdiomaId, UsuarioId
from backend.infrastructure.identificadores.geradores import GeradorIdiomaIdUuid4
from backend.infrastructure.persistence.sqlalchemy.idioma import (
    IdiomaRegistro,
    para_idioma,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_idioma import (
    RepositorioIdiomaSqlAlchemy,
)

# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
ID_IDIOMA = UUID("00000000-0000-0000-0000-0000000000d1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
def criar_idioma() -> Idioma:
    """Cria um idioma determinístico para os testes de fronteira ORM.

    A função usa identificadores fixos para comparar conversões e chamadas sem
    banco ou aleatoriedade. Ela existe para manter os cenários focados no
    comportamento observável do adapter.
    """
    return Idioma(
        id=IdiomaId(ID_IDIOMA),
        usuario_id=UsuarioId(ID_USUARIO),
        idioma="Inglês   Técnico",
        nivel="Avançado",
    )


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class MapeamentoIdiomaTestCase(unittest.TestCase):
    """Verifica conversões puras entre idioma e seu modelo ORM.

    A classe cria registros somente em memória e compara seus valores
    persistíveis. Ela existe para proteger a fronteira sem abrir conexão ou
    depender de infraestrutura de banco.
    """

    def test_converte_entidade_para_registro_com_chave_normalizada(self) -> None:
        """Mantém a chave canônica e os campos exibíveis na conversão ao ORM.

        O cenário mapeia a entidade e compara a denominação serializada e a
        chave calculada. Ele existe para impedir que persistência redefina
        a política de duplicidade aplicada no núcleo.
        """
        registro = para_registro(criar_idioma())

        self.assertIsInstance(registro, IdiomaRegistro)
        self.assertEqual(registro.id, ID_IDIOMA)
        self.assertEqual(registro.usuario_id, ID_USUARIO)
        self.assertEqual(registro.idioma, "Inglês   Técnico")
        self.assertEqual(registro.idioma_normalizado, "inglês técnico")
        self.assertEqual(registro.nivel, "Avançado")

    def test_reconstroi_entidade_a_partir_de_registro(self) -> None:
        """Reconstrói value objects a partir das colunas ORM.

        O cenário percorre ambos os mapeadores e compara a entidade resultante
        com a origem. Ele existe para evitar que dados instrumentados escapem
        para domínio e Application.
        """
        self.assertEqual(
            para_idioma(para_registro(criar_idioma())), criar_idioma()
        )


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class RepositorioIdiomaSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o adapter com sessão SQLAlchemy substituída por double.

    Os cenários observam query, add, flush e tradução de erro com mocks, sem
    iniciar banco ou transação real. A classe existe para testar a porta na sua
    fronteira unitária permitida.
    """

    async def test_consulta_chave_normalizada_por_usuario(self) -> None:
        """Retorna verdadeiro quando a sessão encontra uma chave equivalente.

        O teste configura apenas ``scalar`` no double e observa o resultado da
        consulta. Ele existe para assegurar que a prevenção prévia usa a chave
        técnica, não a denominação exibível ou o nível.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = ID_IDIOMA
        repositorio = RepositorioIdiomaSqlAlchemy(session)

        existe = await repositorio.existe_por_chave_de_duplicidade(
            UsuarioId(ID_USUARIO), "inglês técnico"
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
        repositorio = RepositorioIdiomaSqlAlchemy(session)

        await repositorio.salvar(criar_idioma())

        registro = session.add.call_args.args[0]
        self.assertIsInstance(registro, IdiomaRegistro)
        self.assertEqual(registro.idioma_normalizado, "inglês técnico")
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
                'constraint "uq_idiomas_usuario_idioma_normalizado"'
            ),
        )
        repositorio = RepositorioIdiomaSqlAlchemy(session)

        with self.assertRaises(IdiomaJaCadastrado):
            await repositorio.salvar(criar_idioma())

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
        repositorio = RepositorioIdiomaSqlAlchemy(session)

        with self.assertRaises(IntegrityError):
            await repositorio.salvar(criar_idioma())


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class GeradorIdiomaIdUuid4TestCase(unittest.TestCase):
    """Testa a geração de IDs de idioma com UUID4.

    A suíte executa o gerador e verifica se o value object retornado é válido.
    Ela existe para garantir a integridade do adapter de identificadores.
    """

    def test_gera_idioma_id_com_uuid4(self) -> None:
        """Gera um IdiomaId válido com formato UUID4.

        O cenário invoca o método gerar e valida o tipo e valor retornado. Ele
        existe para assegurar que a implementação concreta atende à porta.
        """
        gerador = GeradorIdiomaIdUuid4()
        idioma_id = gerador.gerar()

        self.assertIsInstance(idioma_id, IdiomaId)
        self.assertIsInstance(idioma_id.valor, UUID)
