"""Gera e resume tokens de uso único da recuperação de senha."""

import hashlib
import secrets

from backend.application.recuperacao_senha import TokenRecuperacaoGerado


class GeradorTokenRecuperacaoSeguro:
    """Gera tokens aleatórios de 256 bits e mantém somente seus resumos no banco.

    Usa ``secrets`` para produzir um valor URL-safe e SHA-256 para consulta
    persistente. A classe existe para que a camada de aplicação não conheça
    detalhes de aleatoriedade ou hashing.
    """

    def gerar(self) -> TokenRecuperacaoGerado:
        """Cria token imprevisível e o respectivo resumo hexadecimal.

        O token contém 32 bytes aleatórios e o resumo é o único valor destinado
        à persistência. O método existe para entregar o segredo ao canal de
        recuperação uma única vez.
        """
        token = secrets.token_urlsafe(32)
        return TokenRecuperacaoGerado(token, self.resumir(token))

    def resumir(self, token: str) -> str:
        """Calcula SHA-256 UTF-8 para localizar o token sem persistir seu valor.

        O resumo é estável e não contém o segredo original. O método existe
        para comparar a credencial apresentada com o registro armazenado.
        """
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
