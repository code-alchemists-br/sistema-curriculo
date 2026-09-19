"""Implementa derivação e conferência segura de senhas com scrypt.

O adapter mantém salt e parâmetros junto ao hash serializado e não persiste a
senha em texto claro. Ele existe para atender à proteção de credenciais sem
levar uma biblioteca criptográfica ou detalhes de formato ao núcleo do sistema.
"""

import base64
import binascii
import hashlib
import hmac
import secrets

from backend.application.ports import VerificadorSenha
from backend.domain.value_objects import HashSenha


class DerivadorSenhaScrypt(VerificadorSenha):
    """Deriva e confere hashes scrypt com parâmetros explícitos e salt aleatório.

    A implementação serializa algoritmo, custo, salt e resultado em texto e usa
    comparação em tempo constante para conferir credenciais. Ela existe para
    que API e Application trabalhem com portas e HashSenha, não com criptografia.
    """

    _CUSTO = 2**14
    _TAMANHO_BLOCO = 8
    _PARALELISMO = 1
    _TAMANHO_SALT = 16

    def derivar(self, senha: str) -> HashSenha:
        """Gera um HashSenha scrypt a partir da senha informada no cadastro.

        O metodo rejeita senha vazia, cria salt criptograficamente aleatório e
        codifica os elementos necessários à verificação posterior. Ele existe
        para que nenhuma senha em texto claro seja enviada à persistência.
        """
        if not senha:
            raise ValueError("Senha não pode ser vazia.")
        salt = secrets.token_bytes(self._TAMANHO_SALT)
        resultado = self._derivar(senha, salt)
        return HashSenha(
            "scrypt$"
            f"{self._CUSTO}${self._TAMANHO_BLOCO}${self._PARALELISMO}$"
            f"{self._codificar(salt)}${self._codificar(resultado)}"
        )

    def confere(self, senha: str, hash_senha: str) -> bool:
        """Compara senha e hash scrypt serializado sem expor formato inválido.

        O metodo aceita somente os parâmetros esperados, recalcula scrypt e usa
        comparação em tempo constante. Ele existe para que hashes corrompidos
        resultem apenas em acesso negado, não em falha de infraestrutura.
        """
        try:
            algoritmo, custo, bloco, paralelismo, salt_texto, resultado_texto = hash_senha.split("$")
            if (algoritmo, int(custo), int(bloco), int(paralelismo)) != (
                "scrypt", self._CUSTO, self._TAMANHO_BLOCO, self._PARALELISMO,
            ):
                return False
            resultado_recebido = self._derivar(senha, self._decodificar(salt_texto))
            resultado_esperado = self._decodificar(resultado_texto)
        except (ValueError, UnicodeEncodeError, binascii.Error):
            return False
        return hmac.compare_digest(resultado_recebido, resultado_esperado)

    def _derivar(self, senha: str, salt: bytes) -> bytes:
        """Executa scrypt com os parâmetros privados e constantes deste adapter.

        A função transforma senha e salt no resultado de derivação, assegurando
        custos idênticos na criação e na conferência. Ela existe para concentrar
        a política criptográfica fora de API, Application e domínio.
        """
        return hashlib.scrypt(senha.encode("utf-8"), salt=salt, n=self._CUSTO, r=self._TAMANHO_BLOCO, p=self._PARALELISMO)

    def _codificar(self, valor: bytes) -> str:
        """Codifica bytes em Base64 para armazená-los no hash textual.

        A função usa a representação ASCII da biblioteca padrão e não altera o
        valor binário. Ela existe para registrar salt e resultado em uma coluna
        textual sem criar uma estrutura paralela de persistência.
        """
        return base64.b64encode(valor).decode("ascii")

    def _decodificar(self, valor: str) -> bytes:
        """Decodifica e valida uma parte Base64 do hash scrypt persistido.

        A função pede validação estrita à biblioteca padrão e permite que o
        chamador traduza formato inválido em credenciais não confirmadas. Ela
        existe para não aceitar salt ou resultado corrompidos silenciosamente.
        """
        return base64.b64decode(valor.encode("ascii"), validate=True)
