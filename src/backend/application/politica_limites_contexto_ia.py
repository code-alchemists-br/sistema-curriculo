"""Define a política interna que limita contextos enviados a modelos de IA.

O módulo representa os limites como dados imutáveis, resolve substituições por
ação e modelo e não conhece arquivos, API ou provedores. Ele existe para que a
aplicação preserve custo e minimização de dados independentemente de como a
política é armazenada.
"""

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping, Protocol


@dataclass(frozen=True, slots=True)
class LimitesContextoIa:
    """Agrupa os limites efetivos usados na preparação de um contexto de IA.

    O value object mantém um orçamento total e limites por campo positivos e
    imutáveis. Ele existe para que a montagem de contexto aplique uma política
    consistente sem depender da origem ou do formato de sua configuração.
    """

    limites_campos: Mapping[str, int]
    orcamento_total_caracteres: int

    def __post_init__(self) -> None:
        """Valida e torna imutáveis os limites recebidos na construção.

        O método verifica valores positivos e protege o mapa contra alterações
        posteriores. Ele existe para impedir que uma política já resolvida seja
        modificada durante o atendimento de outra requisição.
        """
        if not isinstance(self.orcamento_total_caracteres, int) or isinstance(
            self.orcamento_total_caracteres, bool
        ) or self.orcamento_total_caracteres <= 0:
            raise ValueError("O orçamento total deve ser um inteiro positivo.")

        limites = dict(self.limites_campos)
        if not limites:
            raise ValueError("A política deve definir ao menos um limite de campo.")
        for campo, limite in limites.items():
            if not isinstance(campo, str) or not campo:
                raise ValueError("Cada campo limitado deve ter um nome não vazio.")
            if not isinstance(limite, int) or isinstance(limite, bool) or limite <= 0:
                raise ValueError("Os limites de campo devem ser inteiros positivos.")
        object.__setattr__(self, "limites_campos", MappingProxyType(limites))


@dataclass(frozen=True, slots=True)
class SobrescritaLimitesContextoIa:
    """Representa apenas os valores de uma política que precisam ser alterados.

    A sobrescrita pode ajustar campos isolados e/ou o orçamento total, sem
    repetir o padrão global. Ela existe para manter configurações por ação ou
    modelo pequenas e legíveis.
    """

    limites_campos: Mapping[str, int]
    orcamento_total_caracteres: int | None = None

    def __post_init__(self) -> None:
        """Valida os valores parciais e impede alterações no mapa armazenado.

        O método aceita uma coleção vazia de campos quando apenas o orçamento
        muda, mas rejeita valores não positivos. Ele existe para que uma
        sobrescrita nunca gere um limite inválido ao ser aplicada.
        """
        limites = dict(self.limites_campos)
        for campo, limite in limites.items():
            if not isinstance(campo, str) or not campo:
                raise ValueError("Cada campo limitado deve ter um nome não vazio.")
            if not isinstance(limite, int) or isinstance(limite, bool) or limite <= 0:
                raise ValueError("Os limites de campo devem ser inteiros positivos.")
        if self.orcamento_total_caracteres is not None and (
            not isinstance(self.orcamento_total_caracteres, int)
            or isinstance(self.orcamento_total_caracteres, bool)
            or self.orcamento_total_caracteres <= 0
        ):
            raise ValueError("O orçamento total deve ser um inteiro positivo.")
        object.__setattr__(self, "limites_campos", MappingProxyType(limites))

    def aplicar(self, base: LimitesContextoIa) -> LimitesContextoIa:
        """Produz limites efetivos ao mesclar esta sobrescrita com uma base.

        O método conserva campos e orçamento não informados, substituindo só os
        valores explicitamente configurados. Ele existe para aplicar a
        precedência da política sem mutar o padrão compartilhado.
        """
        limites = dict(base.limites_campos)
        limites.update(self.limites_campos)
        return LimitesContextoIa(
            limites_campos=limites,
            orcamento_total_caracteres=(
                self.orcamento_total_caracteres
                if self.orcamento_total_caracteres is not None
                else base.orcamento_total_caracteres
            ),
        )


@dataclass(frozen=True, slots=True)
class PoliticaLimitesContextoIa:
    """Resolve a política de limites conforme a ação e o modelo solicitados.

    A política combina padrão global, substituições por modelo, por ação e pela
    combinação de ambos; o teto de segurança é aplicado ao resultado. Ela
    existe para manter o envio de dados previsível mesmo quando a operação usa
    modelos com custo ou capacidade diferentes.
    """

    versao: str
    padrao: LimitesContextoIa
    teto_seguranca: LimitesContextoIa
    por_acao: Mapping[str, SobrescritaLimitesContextoIa]
    por_modelo: Mapping[str, SobrescritaLimitesContextoIa]
    por_acao_modelo: Mapping[str, Mapping[str, SobrescritaLimitesContextoIa]]

    def __post_init__(self) -> None:
        """Protege coleções internas e valida a versão identificadora da política.

        O método copia os mapas configurados para proxies somente leitura e
        exige uma versão não vazia. Ele existe para garantir que a política
        auditada por uma requisição não seja alterada em memória.
        """
        if not isinstance(self.versao, str) or not self.versao.strip():
            raise ValueError("A versão da política deve ser informada.")
        object.__setattr__(self, "por_acao", MappingProxyType(dict(self.por_acao)))
        object.__setattr__(self, "por_modelo", MappingProxyType(dict(self.por_modelo)))
        object.__setattr__(
            self,
            "por_acao_modelo",
            MappingProxyType(
                {
                    acao: MappingProxyType(dict(por_modelo))
                    for acao, por_modelo in self.por_acao_modelo.items()
                }
            ),
        )

    def resolver(self, acao: str | None, modelo: str | None) -> LimitesContextoIa:
        """Obtém limites efetivos na precedência global, modelo, ação e combinação.

        O método mescla apenas substituições aplicáveis e rejeita resultados que
        ultrapassem o teto de segurança. Ele existe para centralizar a decisão
        que a preparação de contexto deve aplicar antes de enviar dados à IA.
        """
        resultado = self.padrao
        if modelo and (sobrescrita := self.por_modelo.get(modelo)):
            resultado = sobrescrita.aplicar(resultado)
        if acao and (sobrescrita := self.por_acao.get(acao)):
            resultado = sobrescrita.aplicar(resultado)
        if acao and modelo and (
            sobrescrita := self.por_acao_modelo.get(acao, {}).get(modelo)
        ):
            resultado = sobrescrita.aplicar(resultado)
        self._validar_teto(resultado)
        return resultado

    def _validar_teto(self, limites: LimitesContextoIa) -> None:
        """Confirma que um resultado não aumenta os limites de segurança definidos.

        O método compara o orçamento e todos os campos conhecidos com o teto.
        Ele existe para impedir que uma substituição operacional amplie o volume
        de dados enviado além da proteção aprovada pelo serviço.
        """
        if limites.orcamento_total_caracteres > self.teto_seguranca.orcamento_total_caracteres:
            raise ValueError("O orçamento total ultrapassa o teto de segurança.")
        for campo, limite in limites.limites_campos.items():
            teto = self.teto_seguranca.limites_campos.get(campo)
            if teto is None or limite > teto:
                raise ValueError(f"O limite de {campo!r} ultrapassa o teto de segurança.")


class FontePoliticaLimitesContextoIa(Protocol):
    """Define a leitura substituível da política de contexto de inteligência artificial.

    A porta devolve sempre uma política válida e não revela se ela veio de
    arquivo, serviço de configuração ou memória. Ela existe para que casos de
    uso dependam do contrato interno, e não do mecanismo de armazenamento.
    """

    def obter(self) -> PoliticaLimitesContextoIa:
        """Obtém a política atual a ser aplicada a uma nova requisição.

        Implementações podem atualizar seu cache antes de devolver a política,
        mas não devem retornar uma configuração incompleta. O método existe
        para permitir recarga operacional sem acoplamento à aplicação.
        """
