"""Testa unitariamente o caso de uso de edição de perfil de estudante."""

import logging
import sys
import unittest
from uuid import uuid4

from backend.application import (
    EditarPerfil,
    EditarPerfilEntrada,
    EmailJaCadastrado,
    UsuarioNaoEncontrado,
)
from backend.domain import Email, HashSenha, Nome, Usuario, UsuarioId

# Configuração básica para imprimir os logs no stderr durante a execução
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s", stream=sys.stderr)
logger = logging.getLogger(__name__)


class RepositorioUsuarioEdicaoSpy:
    """Substitui assincronamente a porta e rastreia atualizações e consultas."""

    def __init__(self, usuarios: list[Usuario] | None = None) -> None:
        self._usuarios: dict[UsuarioId, Usuario] = {
            u.id: u for u in (usuarios or [])
        }
        self.usuarios_atualizados: list[Usuario] = []

    async def buscar_por_id(self, usuario_id: UsuarioId) -> Usuario | None:
        return self._usuarios.get(usuario_id)

    async def buscar_por_email(self, email: Email) -> Usuario | None:
        for u in self._usuarios.values():
            if u.email == email:
                return u
        return None

    async def atualizar(self, usuario: Usuario) -> None:
        self._usuarios[usuario.id] = usuario
        self.usuarios_atualizados.append(usuario)


class EditarPerfilTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a orquestração de edição de perfil em memória."""

    async def test_atualiza_perfil_quando_dados_e_email_sao_validos(self) -> None:
        usuario_existente = _criar_usuario()
        repositorio = RepositorioUsuarioEdicaoSpy([usuario_existente])
        caso_de_uso = EditarPerfil(repositorio)

        entrada = EditarPerfilEntrada(
            usuario_id=usuario_existente.id,
            nome=Nome("Ana Beatriz Silva"),
            email=Email("ana.beatriz@fatec.sp.gov.br"),
        )

        logger.info("\n[TESTE] Iniciar edição com novos dados válidos...")
        usuario_atualizado = await caso_de_uso.executar(entrada)

        self.assertEqual(usuario_atualizado.nome, entrada.nome)
        self.assertEqual(usuario_atualizado.email, entrada.email)
        self.assertEqual(repositorio.usuarios_atualizados, [usuario_atualizado])

        logger.info(
            "Perfil atualizado com sucesso! ID: %s | Novo Nome: %s | Novo Email: %s",
            usuario_atualizado.id,
            usuario_atualizado.nome,
            usuario_atualizado.email,
        )

    async def test_mantem_mesmo_email_sem_acusar_duplicidade(self) -> None:
        usuario_existente = _criar_usuario()
        repositorio = RepositorioUsuarioEdicaoSpy([usuario_existente])
        caso_de_uso = EditarPerfil(repositorio)

        entrada = EditarPerfilEntrada(
            usuario_id=usuario_existente.id,
            nome=Nome("Ana B. Silva"),
            email=usuario_existente.email,
        )

        logger.info("\n[TESTE] Atualizar perfil mantendo o mesmo e-mail...")
        usuario_atualizado = await caso_de_uso.executar(entrada)

        self.assertEqual(usuario_atualizado.nome, entrada.nome)
        self.assertEqual(usuario_atualizado.email, usuario_existente.email)
        self.assertEqual(repositorio.usuarios_atualizados, [usuario_atualizado])

        logger.info("Mesmo e-mail validado com sucesso sem conflito para o utilizador: %s", usuario_atualizado.id)

    async def test_rejeita_edicao_quando_usuario_nao_existe(self) -> None:
        repositorio = RepositorioUsuarioEdicaoSpy([])
        caso_de_uso = EditarPerfil(repositorio)

        id_inexistente = UsuarioId(uuid4())
        entrada = EditarPerfilEntrada(
            usuario_id=id_inexistente,
            nome=Nome("Fantasma"),
            email=Email("fantasma@fatec.sp.gov.br"),
        )

        logger.info("\n[TESTE] Tentar editar perfil de utilizador não existente...")
        with self.assertRaises(UsuarioNaoEncontrado) as contexto:
            await caso_de_uso.executar(entrada)

        self.assertEqual(repositorio.usuarios_atualizados, [])
        logger.info("Exceção esperada intercetada com sucesso: %s (ID: %s)", contexto.exception, id_inexistente)

    async def test_rejeita_novo_email_se_ja_pertencer_a_outro_usuario(self) -> None:
        usuario1 = _criar_usuario()
        usuario2 = Usuario(
            id=UsuarioId(uuid4()),
            nome=Nome("Carlos Lima"),
            email=Email("carlos.lima@fatec.sp.gov.br"),
            hash_senha=HashSenha("outro-hash"),
        )
        repositorio = RepositorioUsuarioEdicaoSpy([usuario1, usuario2])
        caso_de_uso = EditarPerfil(repositorio)

        entrada = EditarPerfilEntrada(
            usuario_id=usuario1.id,
            nome=Nome("Ana Atualizada"),
            email=usuario2.email,
        )

        logger.info("\n[TESTE] Tentar alterar e-mail para um endereço já cadastrado...")
        with self.assertRaises(EmailJaCadastrado) as contexto:
            await caso_de_uso.executar(entrada)

        self.assertEqual(repositorio.usuarios_atualizados, [])
        logger.info("Exceção esperada de duplicidade intercetada com sucesso: %s", contexto.exception)


def _criar_usuario() -> Usuario:
    return Usuario(
        id=UsuarioId(uuid4()),
        nome=Nome("Ana Silva"),
        email=Email("ana.silva@fatec.sp.gov.br"),
        hash_senha=HashSenha("hash-ja-derivado"),
    )