"""Testa o adapter scrypt que protege credenciais fora do núcleo."""

import unittest

from backend.infrastructure.security.senhas import DerivadorSenhaScrypt


class DerivadorSenhaScryptTestCase(unittest.TestCase):
    """Verifica criação e conferência de hashes sem persistência ou rede.

    A classe deriva uma credencial real e avalia resultados esperados. Ela existe
    para proteger o formato serializado e a recusa segura de dados inválidos.
    """

    def setUp(self) -> None:
        """Cria um adapter independente para cada cenário de teste.

        O metodo evita estado compartilhado entre derivações com salts aleatórios.
        Ele existe para manter os testes isolados e determinísticos no resultado.
        """
        self.derivador = DerivadorSenhaScrypt()

    def test_deriva_hash_que_confere_apenas_com_a_senha_original(self) -> None:
        """Confirma derivação e comparação para senha correta e incorreta.

        O teste gera um hash e o confere contra duas entradas. Ele existe para
        garantir que o adapter não aceite uma credencial diferente.
        """
        hash_senha = self.derivador.derivar("senha-segura")

        self.assertTrue(self.derivador.confere("senha-segura", hash_senha.valor))
        self.assertFalse(self.derivador.confere("senha-incorreta", hash_senha.valor))

    def test_rejeita_hash_malformado_sem_propagar_erro(self) -> None:
        """Confirma que credencial persistida inválida resulta somente em recusa.

        O teste oferece um formato que não pode ser decodificado. Ele existe para
        impedir que corrupção de hash exponha erro técnico no fluxo de acesso.
        """
        self.assertFalse(self.derivador.confere("senha-segura", "scrypt$invalido"))
