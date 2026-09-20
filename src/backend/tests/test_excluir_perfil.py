"""Testa unitariamente o caso de uso de exclusão de perfil de estudante."""

import unittest
from uuid import uuid4

from backend.application import (
    ExcluirPerfil,
    ExcluirPerfilEntrada,
    UsuarioNaoEncontrado,
)
from backend.domain import Email, HashSenha, Nome, Usuario, UsuarioId


class RepositorioUsuarioExclusaoSpy:
    """Substitui assincronamente a porta e registra exclusões solicitadas."""

    def __init__(self, usuarios: list[Usuario] | None = None) -> None:
        self._usuarios: dict[UsuarioId, Usuario] = {
            u.id: u for u in (usuarios or [])
        }
        self.ids_excluidos: list[UsuarioId] = []

    async def buscar_por_id(self, usuario_id: UsuarioId) -> Usuario | None:
        return self._usuarios.get(usuario_id)

    async def excluir(self, usuario_id: UsuarioId) -> None:
        self._usuarios.pop(usuario_id, None)
        self.ids_excluidos.append(usuario_id)


class ExcluirPerfilTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a orquestração de exclusão de conta em memória."""

    async def test_exclui_usuario_existente_com_sucesso(self) -> None:
        usuario = _criar_usuario()
        repositorio = RepositorioUsuarioExclusaoSpy([usuario])
        caso_de_uso = ExcluirPerfil(repositorio)

        await caso_de_uso.executar(ExcluirPerfilEntrada(usuario_id=usuario.id))

        self.assertEqual(repositorio.ids_excluidos, [usuario.id])
        self.assertIsNone(await repositorio.buscar_por_id(usuario.id))

    async def test_rejeita_exclusao_de_usuario_inexistente(self) -> None:
        repositorio = RepositorioUsuarioExclusaoSpy([])
        caso_de_uso = ExcluirPerfil(repositorio)
        id_inexistente = UsuarioId(uuid4())

        with self.assertRaises(UsuarioNaoEncontrado):
            await caso_de_uso.executar(ExcluirPerfilEntrada(usuario_id=id_inexistente))

        self.assertEqual(repositorio.ids_excluidos, [])


def _criar_usuario() -> Usuario:
    return Usuario(
        id=UsuarioId(uuid4()),
        nome=Nome("Ana Silva"),
        email=Email("ana.silva@fatec.sp.gov.br"),
        hash_senha=HashSenha("hash-ja-derivado"),
    )