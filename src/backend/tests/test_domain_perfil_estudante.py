"""Testa unitariamente as transições do perfil no agregado de usuário."""

from datetime import datetime, timezone
import unittest
from uuid import uuid4

from backend.domain import (
    Email,
    HashSenha,
    Nome,
    RegraDeDominioViolada,
    Usuario,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001


class PerfilEstudanteDomainTestCase(unittest.TestCase):
    """Verifica edição imutável e exclusão lógica do agregado ``Usuario``.

    A classe exerce somente o domínio com value objects e instantes controlados,
    sem portas ou recursos externos. Ela existe para proteger identidade,
    credencial e idempotência nas transições do perfil.
    """

    def test_edita_perfil_preservando_identidade_credencial_e_original(self) -> None:
        """Confirma que nome e e-mail mudam sem mutar o agregado anterior.

        O teste compara os dois estados e os value objects preservados após a
        transição. Ele existe para assegurar edição pela raiz sem trocar ID ou
        hash de senha.
        """
        usuario = _criar_usuario()

        editado = usuario.editar_perfil(
            Nome("Ana Souza"), Email("ana.souza@example.com")
        )

        self.assertIsNot(editado, usuario)
        self.assertEqual(editado.id, usuario.id)
        self.assertEqual(editado.hash_senha, usuario.hash_senha)
        self.assertEqual(editado.nome, Nome("Ana Souza"))
        self.assertEqual(editado.email, Email("ana.souza@example.com"))
        self.assertEqual(usuario.nome, Nome("Ana Silva"))
        self.assertFalse(editado.excluido)

    def test_rejeita_edicao_de_perfil_excluido(self) -> None:
        """Confirma que uma exclusão não pode ser revertida por edição.

        O teste exclui o agregado e tenta trocar seus dados, observando a falha
        de domínio. Ele existe para impedir reativação implícita do perfil.
        """
        usuario = _criar_usuario().excluir(_instante_exclusao())

        with self.assertRaises(RegraDeDominioViolada):
            usuario.editar_perfil(Nome("Outro Nome"), Email("outro@example.com"))

    def test_exclusao_e_idempotente_e_preserva_primeiro_instante(self) -> None:
        """Confirma que excluir novamente devolve o mesmo estado já excluído.

        O teste aplica dois instantes e exige que o segundo não substitua o
        primeiro nem crie novo agregado. Ele existe para tornar repetição segura.
        """
        usuario = _criar_usuario()
        primeiro = usuario.excluir(_instante_exclusao())
        segundo = primeiro.excluir(datetime(2026, 9, 21, tzinfo=timezone.utc))

        self.assertTrue(primeiro.excluido)
        self.assertEqual(primeiro.deleted_at, _instante_exclusao())
        self.assertIs(segundo, primeiro)


def _criar_usuario() -> Usuario:
    """Cria um usuário ativo com valores válidos e independentes de I/O.

    A função reúne value objects determinísticos, exceto pela identidade sem
    significado externo. Ela existe para reduzir repetição e manter os testes
    concentrados nas transições do agregado.
    """
    return Usuario(
        id=UsuarioId(uuid4()),
        nome=Nome("Ana Silva"),
        email=Email("ana@example.com"),
        hash_senha=HashSenha("hash-ja-derivado"),
    )


def _instante_exclusao() -> datetime:
    """Fornece um instante fixo para comparar exclusões deterministicamente.

    A função retorna sempre o mesmo valor UTC sem ler o relógio do sistema. Ela
    existe para que os testes não dependam do momento em que são executados.
    """
    return datetime(2026, 9, 20, tzinfo=timezone.utc)
