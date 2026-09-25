"""Testa unitariamente a transição de dados de contato no agregado de usuário."""

from datetime import datetime, timezone
import unittest
from uuid import uuid4

from backend.domain import (
    DadosContato,
    Email,
    Endereco,
    HashSenha,
    Nome,
    RegraDeDominioViolada,
    Telefone,
    Usuario,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001


class DadosContatoDomainTestCase(unittest.TestCase):
    """Verifica a transição imutável de dados de contato do agregado ``Usuario``.

    A classe exerce somente o domínio com value objects em memória, sem portas
    ou recursos externos. Ela existe para proteger identidade, credencial e
    invariantes de contato na nova transição.
    """

    def test_atualiza_dados_contato_preservando_identidade_e_credencial(self) -> None:
        """Confirma que os dados de contato mudam sem mutar o agregado anterior.

        O teste compara os dois estados e os value objects preservados após a
        transição. Ele existe para assegurar atualização pela raiz sem trocar
        ID, nome, e-mail ou hash de senha.
        """
        usuario = _criar_usuario()
        dados_contato = DadosContato(
            endereco=Endereco("Rua Um, 100"),
            telefones=(Telefone("11999990000"),),
            linkedin="https://linkedin.com/in/ana",
        )

        atualizado = usuario.atualizar_dados_contato(dados_contato)

        self.assertIsNot(atualizado, usuario)
        self.assertEqual(atualizado.id, usuario.id)
        self.assertEqual(atualizado.hash_senha, usuario.hash_senha)
        self.assertEqual(atualizado.nome, usuario.nome)
        self.assertEqual(atualizado.dados_contato, dados_contato)
        self.assertIsNone(usuario.dados_contato)
        self.assertFalse(atualizado.excluido)

    def test_rejeita_atualizacao_de_dados_contato_em_perfil_excluido(self) -> None:
        """Confirma que um perfil excluído não pode receber novos dados de contato.

        O teste exclui o agregado e tenta atualizar o contato, observando a
        falha de domínio. Ele existe para impedir reativação implícita do
        perfil por meio dos dados de contato.
        """
        usuario = _criar_usuario().excluir(_instante_exclusao())
        dados_contato = DadosContato(
            endereco=Endereco("Rua Um, 100"),
            telefones=(Telefone("11999990000"),),
        )

        with self.assertRaises(RegraDeDominioViolada):
            usuario.atualizar_dados_contato(dados_contato)

    def test_dados_contato_exige_ao_menos_um_telefone(self) -> None:
        """Confirma que contato sem nenhum telefone é rejeitado pelo domínio.

        O teste tenta construir ``DadosContato`` com telefones vazios e observa
        a falha antes de qualquer transição do agregado.
        """
        with self.assertRaises(RegraDeDominioViolada):
            DadosContato(endereco=Endereco("Rua Um, 100"), telefones=())


def _criar_usuario() -> Usuario:
    """Cria um usuário ativo com valores válidos e independentes de I/O.

    A função reúne value objects determinísticos, exceto pela identidade sem
    significado externo. Ela existe para reduzir repetição e manter os testes
    concentrados na transição de dados de contato.
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
    existe para que o teste não dependa do momento em que é executado.
    """
    return datetime(2026, 9, 20, tzinfo=timezone.utc)