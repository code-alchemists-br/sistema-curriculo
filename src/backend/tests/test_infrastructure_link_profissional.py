"""Testa unitariamente o mapeamento e o repositório SQLAlchemy de links profissionais."""

import unittest
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.application.cadastro_link_profissional import (
    LinkProfissionalJaCadastrado,
)
from backend.domain import LinkProfissional, LinkProfissionalId, UsuarioId
from backend.infrastructure.identificadores.geradores import (
    GeradorLinkProfissionalIdUuid4,
)
from backend.infrastructure.persistence.sqlalchemy.link_profissional import (
    LinkProfissionalRegistro,
    para_link_profissional,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_link_profissional import (
    RepositorioLinkProfissionalSqlAlchemy,
)

ID_LINK = UUID("00000000-0000-0000-0000-0000000000a1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def criar_link() -> LinkProfissional:
    """Cria um link profissional determinístico para os testes de fronteira ORM.

    A função usa identificadores fixos para comparar conversões e chamadas sem
    banco ou aleatoriedade. Ela existe para manter os cenários focados no
    comportamento observável do adapter.
    """
    return LinkProfissional(
        id=LinkProfissionalId(ID_LINK),
        usuario_id=UsuarioId(ID_USUARIO),
        rotulo="GitHub Perfil",
        url="https://github.com/usuario",
    )


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class MapeamentoLinkProfissionalTestCase(unittest.TestCase):
    """Verifica conversões puras entre link profissional e seu modelo ORM.

    A classe cria registros somente em memória e compara seus valores
    persistíveis. Ela existe para proteger a fronteira sem abrir conexão ou
    depender de infraestrutura de banco.
    """

    def test_converte_entidade_para_registro_com_chaves_normalizadas(self) -> None:
        """Mantém as chaves canônicas e os campos na conversão ao ORM.

        O cenário mapeia a entidade e compara os dados serializados e as chaves
        calculadas. Ele existe para impedir que a persistência redefina a política
        de duplicidade aplicada no núcleo.
        """
        registro = para_registro(criar_link())

        self.assertIsInstance(registro, LinkProfissionalRegistro)
        self.assertEqual(registro.id, ID_LINK)
        self.assertEqual(registro.usuario_id, ID_USUARIO)
        self.assertEqual(registro.rotulo, "GitHub Perfil")
        self.assertEqual(registro.url, "https://github.com/usuario")
        self.assertEqual(registro.url_normalizada, "https://github.com/usuario")

    def test_reconstroi_entidade_a_partir_de_registro(self) -> None:
        """Reconstrói value objects a partir das colunas ORM.

        O cenário percorre ambos os mapeadores e compara a entidade resultante
        com a origem. Ele existe para evitar que dados instrumentados escapem
        para domínio e Application.
        """
        self.assertEqual(
            para_link_profissional(para_registro(criar_link())), criar_link()
        )


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class RepositorioLinkProfissionalSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o adapter com sessão SQLAlchemy substituída por double.

    Os cenários observam query, add, flush e tradução de erro com mocks, sem
    iniciar banco ou transação real. A classe existe para testar a porta na sua
    fronteira unitária permitida.
    """

    async def test_consulta_chave_normalizada_por_usuario(self) -> None:
        """Retorna verdadeiro quando a sessão encontra uma chave equivalente.

        O teste configura apenas ``scalar`` no double e observa o resultado da
        consulta. Ele existe para assegurar que a prevenção prévia usa a chave
        técnica url_normalizada.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = ID_LINK
        repositorio = RepositorioLinkProfissionalSqlAlchemy(session)

        existe = await repositorio.existe_por_chave_de_duplicidade(
            UsuarioId(ID_USUARIO), "https://github.com/usuario"
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
        repositorio = RepositorioLinkProfissionalSqlAlchemy(session)

        await repositorio.salvar(criar_link())

        registro = session.add.call_args.args[0]
        self.assertIsInstance(registro, LinkProfissionalRegistro)
        self.assertEqual(registro.url_normalizada, "https://github.com/usuario")
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()

    async def test_traduz_violacao_da_constraint_de_duplicidade(self) -> None:
        """Converte somente a colisão nomeada em falha conhecida da Application.

        O double faz ``flush`` levantar ``IntegrityError`` contendo o nome da
        constraint uq_links_profissionais_usuario_url_normalizada. Ele existe para
        garantir a proteção contra corrida sem vazar SQL pela porta de persistência.
        """
        session = MagicMock(spec=AsyncSession)
        session.flush.side_effect = IntegrityError(
            statement=None,
            params=None,
            orig=RuntimeError(
                'constraint "uq_links_profissionais_usuario_url_normalizada"'
            ),
        )
        repositorio = RepositorioLinkProfissionalSqlAlchemy(session)

        with self.assertRaises(LinkProfissionalJaCadastrado):
            await repositorio.salvar(criar_link())

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
        repositorio = RepositorioLinkProfissionalSqlAlchemy(session)

        with self.assertRaises(IntegrityError):
            await repositorio.salvar(criar_link())


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class GeradorLinkProfissionalIdUuid4TestCase(unittest.TestCase):
    """Testa a geração de IDs de link profissional com UUID4.

    A suíte executa o gerador e verifica se o value object retornado é válido.
    Ela existe para garantir a integridade do adapter de identificadores.
    """

    def test_gera_link_profissional_id_com_uuid4(self) -> None:
        """Gera um LinkProfissionalId válido com formato UUID4.

        O cenário invoca o método gerar e valida o tipo e valor retornado. Ele
        existe para assegurar que a implementação concreta atende à porta.
        """
        gerador = GeradorLinkProfissionalIdUuid4()
        link_id = gerador.gerar()

        self.assertIsInstance(link_id, LinkProfissionalId)
        self.assertIsInstance(link_id.valor, UUID)
