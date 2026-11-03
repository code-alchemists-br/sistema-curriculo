"""Define os atributos HTTP usados para transportar a sessão autenticada."""

from dataclasses import dataclass

COOKIE_SESSAO_SEGURA = "__Host-sessao"
COOKIE_SESSAO_DESENVOLVIMENTO = "sessao"


@dataclass(frozen=True)
class ConfiguracaoCookieSessao:
    """Agrupa os atributos de cookie coerentes com cada ambiente de execução.

    A configuração escolhe um nome com prefixo ``__Host-`` quando HTTPS é
    obrigatório e um nome sem esse prefixo apenas para desenvolvimento HTTP.
    Ela existe para preservar os atributos fortes em produção sem impedir o
    teste local deliberadamente configurado.
    """

    seguro: bool = True
    duracao_segundos: int = 28_800

    @property
    def nome(self) -> str:
        """Devolve o nome válido para os atributos de segurança configurados.

        A propriedade usa ``__Host-sessao`` apenas quando o atributo Secure
        está ativo, pois navegadores rejeitam esse prefixo sem HTTPS. Ela existe
        para manter emissão, leitura e remoção do mesmo cookie.
        """
        return COOKIE_SESSAO_SEGURA if self.seguro else COOKIE_SESSAO_DESENVOLVIMENTO
