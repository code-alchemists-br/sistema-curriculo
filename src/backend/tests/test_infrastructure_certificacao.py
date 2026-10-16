"""Testa unitariamente o mapeamento e o repositório SQLAlchemy de certificações."""

import unittest
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
from backend.application.cadastro_certificacao import CertificacaoJaCadastrada
from backend.domain import Certificacao, CertificacaoId, UsuarioId
from backend.infrastructure.identificadores.geradores import (
    GeradorCertificacaoIdUuid4,
)
from backend.infrastructure.persistence.sqlalchemy.certificacao import (
    CertificacaoRegistro,
    para_certificacao,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_certificacao import (
    RepositorioCertificacaoSqlAlchemy,
)

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
ID_CERTIFICACAO = UUID("00000000-0000-0000-0000-0000000000c1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
def criar_certificacao() -> Certificacao:
    """Cria uma certificação determinística para os testes de fronteira ORM.

    A função usa identificadores fixos para comparar conversões e chamadas sem
    banco ou aleatoriedade. Ela existe para manter os cenários focados no
    comportamento observável do adapter.
    """
    return Certificacao(
        id=CertificacaoId(ID_CERTIFICACAO),
        usuario_id=UsuarioId(ID_USUARIO),
        nome="AWS Solutions Architect",
        organizacao_emissora="Amazon Web Services",
    )


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class MapeamentoCertificacaoTestCase(unittest.TestCase):
    """Verifica conversões puras entre certificação e seu modelo ORM.

    A classe cria registros somente em memória e compara seus valores
    persistíveis. Ela existe para proteger a fronteira sem abrir conexão ou
    depender de infraestrutura de banco.
    """

    def test_converte_entidade_para_registro_com_chaves_normalizadas(
        self,
    ) -> None:
        """Mantém as chaves canônicas e os campos exibíveis na conversão ao ORM.

        O cenário mapeia a entidade e compara os nomes serializados e as chaves
        calculadas. Ele existe para impedir que a persistência redefina a
        política de duplicidade aplicada no núcleo.
        """
        registro = para_registro(criar_certificacao())

        self.assertIsInstance(registro, CertificacaoRegistro)
        self.assertEqual(registro.id, ID_CERTIFICACAO)
        self.assertEqual(registro.usuario_id, ID_USUARIO)
        self.assertEqual(registro.nome, "AWS Solutions Architect")
        self.assertEqual(
            registro.nome_normalizado, "aws solutions architect"
        )
        self.assertEqual(registro.organizacao_emissora, "Amazon Web Services")
        self.assertEqual(
            registro.organizacao_emissora_normalizada, "amazon web services"
        )

    def test_reconstroi_entidade_a_partir_de_registro(self) -> None:
        """Reconstrói value objects a partir das colunas ORM.

        O cenário percorre ambos os mapeadores e compara a entidade resultante
        com a origem. Ele existe para evitar que dados instrumentados escapem
        para o domínio e para a Application.
        """
        self.assertEqual(
            para_certificacao(para_registro(criar_certificacao())),
            criar_certificacao(),
        )


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class RepositorioCertificacaoSqlAlchemyTestCase(
    unittest.IsolatedAsyncioTestCase
):
    """Verifica o adapter com sessão SQLAlchemy substituída por double.

    Os cenários observam query, add, flush e tradução de erro com mocks, sem
    iniciar banco ou transação real. A classe existe para testar a porta na sua
    fronteira unitária permitida.
    """

    async def test_consulta_chave_normalizada_por_usuario(self) -> None:
        """Retorna verdadeiro quando a sessão encontra uma chave equivalente.

        O teste configura apenas ``scalar`` no double e observa o resultado da
        consulta. Ele existe para assegurar que a prevenção prévia usa a chave
        composta normalizada.
        """
        session = MagicMock(spec=AsyncSession)
        session.scalar.return_value = ID_CERTIFICACAO
        repositorio = RepositorioCertificacaoSqlAlchemy(session)

        existe = await repositorio.existe_por_chave_de_duplicidade(
            UsuarioId(ID_USUARIO),
            "aws solutions architect",
            "amazon web services",
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
        repositorio = RepositorioCertificacaoSqlAlchemy(session)

        await repositorio.salvar(criar_certificacao())

        registro = session.add.call_args.args[0]
        self.assertIsInstance(registro, CertificacaoRegistro)
        self.assertEqual(
            registro.nome_normalizado, "aws solutions architect"
        )
        self.assertEqual(
            registro.organizacao_emissora_normalizada, "amazon web services"
        )
        session.flush.assert_awaited_once_with()
        session.commit.assert_not_called()

    async def test_traduz_violacao_da_constraint_de_duplicidade(self) -> None:
        """Converte somente a colisão nomeada em falha conhecida da Application.

        O double faz ``flush`` levantar ``IntegrityError`` contendo o nome da
        constraint de certificação. Ele existe para garantir a proteção contra
        corrida sem vazar SQL pela porta de persistência.
        """
        session = MagicMock(spec=AsyncSession)
        session.flush.side_effect = IntegrityError(
            statement=None,
            params=None,
            orig=RuntimeError(
                'constraint "uq_certificacoes_usuario_nome_emissor_normalizados"'
            ),
        )
        repositorio = RepositorioCertificacaoSqlAlchemy(session)

        with self.assertRaises(CertificacaoJaCadastrada):
            await repositorio.salvar(criar_certificacao())

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
        repositorio = RepositorioCertificacaoSqlAlchemy(session)

        with self.assertRaises(IntegrityError):
            await repositorio.salvar(criar_certificacao())


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class GeradorCertificacaoIdUuid4TestCase(unittest.TestCase):
    """Testa a geração de IDs de certificação com UUID4.

    A suíte executa o gerador e verifica se o value object retornado é válido.
    Ela existe para garantir a integridade do adapter de identificadores.
    """

    def test_gera_certificacao_id_com_uuid4(self) -> None:
        """Gera um CertificacaoId válido com formato UUID4.

        O cenário invoca o método gerar e valida o tipo e valor retornado. Ele
        existe para assegurar que a implementação concreta atende à porta.
        """
        gerador = GeradorCertificacaoIdUuid4()
        cert_id = gerador.gerar()

        self.assertIsInstance(cert_id, CertificacaoId)
        self.assertIsInstance(cert_id.valor, UUID)
