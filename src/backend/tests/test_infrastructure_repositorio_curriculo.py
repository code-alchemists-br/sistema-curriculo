"""Protege a persistência de currículos com doubles, sem conexão com banco."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain import Curriculo, CurriculoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.curriculo import (
    CurriculoRegistro,
    atualizar_registro,
    para_curriculo,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_curriculo import (
    RepositorioCurriculoSqlAlchemy,
)

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001

ID_CURRICULO = UUID("00000000-0000-0000-0000-0000000000c1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


def criar_curriculo() -> Curriculo:
    """Prepara um agregado válido com identidades fixas para isolar os testes.

    Usa UUIDs determinísticos, permitindo comparar a conversão sem aleatoriedade
    ou infraestrutura externa.
    """
    return Curriculo(
        id=CurriculoId(ID_CURRICULO),
        usuario_id=UsuarioId(ID_USUARIO),
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


def criar_registro() -> MagicMock:
    """Prepara um registro ORM simulado equivalente ao agregado de ``criar_curriculo``.

    O double existe somente em memória e expõe os mesmos valores das colunas, de
    modo que a conversão seja testada sem sessão, tabela ou driver.
    """
    return MagicMock(
        id=ID_CURRICULO,
        usuario_id=ID_USUARIO,
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


class ConversaoCurriculoTestCase(unittest.TestCase):
    """Verifica a tradução entre registro ORM e agregado de currículo.

    Usa registros simulados para proteger a separação entre agregado e
    representação persistida sem executar ORM ou I/O.
    """

    def test_reconstroi_agregado_sem_referencias_a_partir_do_registro(self) -> None:
        """Confirma que a leitura transforma colunas em agregado de domínio.

        Compara o agregado reconstruído com o esperado e confirma que as
        referências, ainda não persistidas, permanecem vazias.
        """
        resultado = para_curriculo(criar_registro())

        self.assertEqual(resultado, criar_curriculo())
        self.assertEqual(resultado.referencias, frozenset())

    def test_atualiza_registro_somente_com_dados_editaveis_da_versao(self) -> None:
        """Confirma que apenas título, layout e visibilidade são copiados.

        Edita o agregado, aplica ao registro e verifica que identidade e
        proprietário permanecem inalterados.
        """
        registro = SimpleNamespace(
            id=ID_CURRICULO,
            usuario_id=ID_USUARIO,
            titulo_versao="Antigo",
            layout="antigo",
            is_public=False,
        )
        curriculo = criar_curriculo()
        curriculo.editar_versao("Gestão de Projetos", "moderno", True)

        atualizar_registro(registro, curriculo)  # type: ignore[arg-type]

        self.assertEqual(registro.titulo_versao, "Gestão de Projetos")
        self.assertEqual(registro.layout, "moderno")
        self.assertTrue(registro.is_public)
        self.assertEqual(registro.id, ID_CURRICULO)
        self.assertEqual(registro.usuario_id, ID_USUARIO)


class RepositorioCurriculoSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Exercita a porta assíncrona com sessão substituída.

    Usa mocks aguardáveis para conferir interações, erros e limites de
    transação sem banco, driver conectado ou gerenciador de sessão real.
    """

    def setUp(self) -> None:
        """Cria sessão isolada e adapter por teste usando a especificação real.

        MagicMock transforma métodos async em AsyncMock, permitindo verificar
        awaits e impedir interferência entre cenários.
        """
        self.session = MagicMock(spec=AsyncSession)
        self.repositorio = RepositorioCurriculoSqlAlchemy(self.session)

    async def test_obtem_versao_por_id_e_a_converte_para_agregado(self) -> None:
        """Confirma consulta pela chave primária e mapeamento na leitura.

        Verifica o await de ``get`` com o modelo e o UUID corretos e compara o
        agregado devolvido com o esperado.
        """
        self.session.get.return_value = criar_registro()

        resultado = await self.repositorio.obter_por_id(CurriculoId(ID_CURRICULO))

        self.assertEqual(resultado, criar_curriculo())
        self.session.get.assert_awaited_once_with(CurriculoRegistro, ID_CURRICULO)

    async def test_retorna_ausencia_quando_registro_nao_existe(self) -> None:
        """Confirma que falta de linha não tenta construir agregado inválido.

        Faz a sessão devolver ausência e verifica que o adapter responde ``None``
        sem acionar o mapeador.
        """
        self.session.get.return_value = None

        resultado = await self.repositorio.obter_por_id(CurriculoId(ID_CURRICULO))

        self.assertIsNone(resultado)

    async def test_propaga_falha_na_consulta(self) -> None:
        """Confere que uma consulta falha não se torna ausência de versão.

        Faz a sessão levantar erro e exige que ele chegue intacto ao chamador,
        sem ser confundido com um currículo inexistente.
        """
        self.session.get.side_effect = RuntimeError("falha")

        with self.assertRaises(RuntimeError):
            await self.repositorio.obter_por_id(CurriculoId(ID_CURRICULO))

    async def test_atualiza_somente_colunas_da_versao_e_envia_flush(self) -> None:
        """Confere atualização do registro existente sem criar linha nem commit.

        Verifica a cópia dos campos editáveis, o await de ``flush`` e a ausência
        de ``add``, para proteger que a edição nunca insere uma versão nova.
        """
        registro = criar_registro()
        self.session.get.return_value = registro
        curriculo = criar_curriculo()
        curriculo.editar_versao("Gestão de Projetos", "moderno", True)

        await self.repositorio.atualizar(curriculo)

        self.session.get.assert_awaited_once_with(CurriculoRegistro, ID_CURRICULO)
        self.assertEqual(registro.titulo_versao, "Gestão de Projetos")
        self.assertEqual(registro.layout, "moderno")
        self.assertTrue(registro.is_public)
        self.session.flush.assert_awaited_once_with()
        self.session.add.assert_not_called()

    async def test_rejeita_atualizacao_quando_registro_nao_existe(self) -> None:
        """Confirma que atualizar versão inexistente falha sem enviar alteração.

        Faz a sessão devolver ausência e exige a falha de busca, sem ``flush``
        nem ``add``, para impedir criação implícita durante a atualização.
        """
        self.session.get.return_value = None

        with self.assertRaises(LookupError):
            await self.repositorio.atualizar(criar_curriculo())

        self.session.flush.assert_not_awaited()
        self.session.add.assert_not_called()

    async def test_propaga_falha_no_flush(self) -> None:
        """Confere que falhas de gravação chegam intactas ao chamador.

        Faz o envio da alteração falhar e verifica que o adapter não a mascara
        nem controla transação.
        """
        self.session.get.return_value = criar_registro()
        self.session.flush.side_effect = RuntimeError("falha")

        with self.assertRaises(RuntimeError):
            await self.repositorio.atualizar(criar_curriculo())