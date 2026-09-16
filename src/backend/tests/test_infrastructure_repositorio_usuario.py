"""Protege a persistência de usuários com doubles, sem conexão com banco."""

import unittest
from unittest.mock import MagicMock, call, patch, sentinel
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain import Email, HashSenha, Nome, Usuario, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.repositorio_usuario import (
    RepositorioUsuarioSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.usuario import para_registro

# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001

ADAPTER = "backend.infrastructure.persistence.sqlalchemy.repositorio_usuario"
MODELO = "backend.infrastructure.persistence.sqlalchemy.usuario"


def criar_usuario() -> Usuario:
    """Prepara um agregado válido com VOs determinísticos para isolar os testes.

    Usa UUID fixo e hash já derivado, permitindo comparar a conversão sem
    aleatoriedade, criptografia ou infraestrutura externa.
    """
    return Usuario(
        id=UsuarioId(UUID("00000000-0000-0000-0000-000000000001")),
        nome=Nome("Ana Silva"),
        email=Email(" ANA@EXAMPLE.COM "),
        hash_senha=HashSenha("hash-ja-derivado"),
    )


class ConversaoUsuarioTestCase(unittest.TestCase):
    """Verifica a tradução dos VOs usando um construtor ORM substituído.

    Inspeciona os argumentos primitivos para proteger a separação entre
    agregado imutável e representação persistida sem executar ORM ou I/O.
    """

    def test_converte_valores_sem_modificar_agregado(self) -> None:
        """Confere a conversão comparando argumentos recebidos pelo double.

        Preserva o agregado original e verifica UUID, e-mail normalizado e hash
        já derivado para evitar persistência de VOs ou credenciais em claro.
        """
        usuario = criar_usuario()
        with patch(f"{MODELO}.UsuarioRegistro") as registro:
            resultado = para_registro(usuario)
        registro.assert_called_once_with(
            id=usuario.id.valor,
            nome="Ana Silva",
            email="ana@example.com",
            hash_senha="hash-ja-derivado",
        )
        self.assertIs(resultado, registro.return_value)
        self.assertEqual(usuario, criar_usuario())


class RepositorioUsuarioSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Exercita a porta assíncrona com sessão e consultas substituídas.

    Usa mocks aguardáveis para conferir interações, erros e limites de
    transação sem banco, driver conectado ou gerenciador de sessão real.
    """

    def setUp(self) -> None:
        """Cria sessão isolada e adapter por teste usando a especificação real.

        MagicMock transforma métodos async em AsyncMock, permitindo verificar
        awaits e impedir interferência entre cenários.
        """
        self.session = MagicMock(spec=AsyncSession)
        self.repositorio = RepositorioUsuarioSqlAlchemy(self.session)

    async def test_consulta_existencia_com_email_normalizado(self) -> None:
        """Confere respostas de existência com consulta e sessão simuladas.

        Verifica o predicado normalizado e o await de scalar para assegurar
        consulta parametrizada sem carregar ou salvar agregados.
        """
        for existente in (True, False):
            with self.subTest(existente=existente):
                self.session.reset_mock()
                self.session.scalar.return_value = existente
                with patch(f"{ADAPTER}.select") as select_mock, patch(
                    f"{ADAPTER}.UsuarioRegistro"
                ) as registro:
                    registro.email.__eq__.return_value = sentinel.predicado
                    resultado = await self.repositorio.existe_por_email(
                        Email(" ANA@EXAMPLE.COM ")
                    )
                registro.email.__eq__.assert_called_once_with("ana@example.com")
                select_mock.assert_any_call(registro.id)
                select_mock.return_value.where.assert_called_once_with(
                    registro.email.__eq__.return_value
                )
                select_mock.assert_any_call(
                    select_mock.return_value.where.return_value.exists.return_value
                )
                self.session.scalar.assert_awaited_once_with(select_mock.return_value)
                self.assertIs(resultado, existente)
                self.session.add.assert_not_called()
                self.session.commit.assert_not_called()

    async def test_salva_com_add_e_flush_sem_controlar_transacao(self) -> None:
        """Confere inserção aguardável observando a ordem das chamadas da sessão.

        Substitui a conversão e exige add seguido de flush, sem commit, rollback
        ou fechamento, preservando a transação sob responsabilidade externa.
        """
        usuario = criar_usuario()
        with patch(f"{ADAPTER}.para_registro", return_value=sentinel.registro) as converter:
            resultado = await self.repositorio.salvar(usuario)
        converter.assert_called_once_with(usuario)
        self.assertIsNone(resultado)
        self.assertEqual(self.session.mock_calls, [call.add(sentinel.registro), call.flush()])
        self.session.flush.assert_awaited_once_with()

    async def test_propaga_falha_no_flush(self) -> None:
        """Confere que falhas de gravação chegam intactas ao chamador.

        Injeta uma exceção em flush e inspeciona sua identidade para impedir
        tradução de erros ou rollback não autorizados dentro do adapter.
        """
        erro = RuntimeError("falha simulada de persistência")
        self.session.flush.side_effect = erro
        with patch(f"{ADAPTER}.para_registro", return_value=sentinel.registro):
            with self.assertRaises(RuntimeError) as capturado:
                await self.repositorio.salvar(criar_usuario())
        self.assertIs(capturado.exception, erro)
        self.session.flush.assert_awaited_once_with()
        self.session.commit.assert_not_called()
        self.session.rollback.assert_not_called()
        self.session.close.assert_not_called()

    async def test_propaga_falha_na_consulta(self) -> None:
        """Confere que uma consulta falha não se torna ausência de usuário.

        Injeta erro no scalar aguardável e verifica propagação sem gravação,
        evitando que indisponibilidade permita prosseguir como e-mail inédito.
        """
        erro = RuntimeError("falha simulada de consulta")
        self.session.scalar.side_effect = erro
        with patch(f"{ADAPTER}.select"):
            with self.assertRaises(RuntimeError) as capturado:
                await self.repositorio.existe_por_email(Email("ana@example.com"))
        self.assertIs(capturado.exception, erro)
        self.session.scalar.assert_awaited_once()
        self.session.add.assert_not_called()
        self.session.rollback.assert_not_called()
