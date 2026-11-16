"""Revisa com IA um campo de texto do formulário antes de o estudante salvá-lo.

O módulo define o vocabulário da revisão (campos, veredito e resultado), a
porta para o provedor de IA e o caso de uso que aplica as regras da revisão.
Ele existe para que a experiência guiada do currículo avise sobre textos
vagos ou inválidos sem acoplar a aplicação a um fornecedor de IA.
"""

from enum import StrEnum
from typing import Protocol

from pydantic import BaseModel


class CampoRevisavel(StrEnum):
    """Enumera os campos de texto livre que podem passar pela revisão da IA.

    O enum restringe o identificador enviado pelo frontend a valores conhecidos
    e é repassado ao provedor de IA como contexto da pergunta. Ele existe para
    que a revisão saiba que tipo de texto avalia sem aceitar campos arbitrários.
    """

    DESCRICAO_EXPERIENCIA = "descricao_experiencia"
    DESCRICAO_PROJETO = "descricao_projeto"
    DESCRICAO_CURSO = "descricao_curso"
    DESCRICAO_CERTIFICACAO = "descricao_certificacao"
    OBJETIVO_PROFISSIONAL = "objetivo_profissional"
    OUTRO = "outro"


class SituacaoTexto(StrEnum):
    """Representa o veredito da revisão sobre o texto do estudante.

    ``valido`` indica que o texto já serve, ``melhorado`` que serve mas pode
    ficar melhor e ``invalido`` que não responde à pergunta. O enum existe para
    que frontend e regras de bloqueio usem o mesmo vocabulário fechado.
    """

    VALIDO = "valido"
    MELHORADO = "melhorado"
    INVALIDO = "invalido"


class AvaliacaoIa(BaseModel):
    """Descreve a resposta estruturada esperada do provedor de IA.

    O modelo reúne veredito, motivo e sugestões de reescrita e também serve como
    esquema de saída JSON pedido ao provedor. Ele existe para validar a resposta
    da IA antes que ela chegue às regras do caso de uso.
    """

    situacao: SituacaoTexto
    motivo: str
    sugestoes: list[str]


class RevisaoTexto(BaseModel):
    """Representa o resultado da revisão devolvido ao estudante.

    Além do veredito, do motivo e de até três sugestões, informa se o texto
    original pode ser mantido, o que é falso apenas para texto inválido. Ele
    existe para que o frontend decida, sem regra própria, se bloqueia o avanço.
    """

    situacao: SituacaoTexto
    motivo: str
    sugestoes: list[str]
    pode_manter_texto: bool


class RevisorTextoIndisponivel(RuntimeError):
    """Sinaliza que a IA não está configurada ou falhou ao revisar o texto.

    A exceção é lançada pelos adaptadores e traduzida pela API em indisponível
    (503). Ela existe para que a revisão seja opcional: sem IA, o fluxo segue.
    """


class RevisorTextoIa(Protocol):
    """Define a porta para o provedor de IA que avalia e reescreve um campo.

    Implementações recebem o campo, a pergunta, o texto e um contexto livre e
    devolvem uma ``AvaliacaoIa``. A porta existe para que o caso de uso não
    dependa do SDK de nenhum fornecedor específico.
    """

    async def avaliar(
        self, campo: CampoRevisavel, pergunta: str | None, texto: str, contexto: dict[str, str]
    ) -> AvaliacaoIa:
        """Avalia o texto e propõe reescritas para o campo indicado.

        A implementação consulta o provedor de IA e devolve a avaliação
        estruturada, ou lança ``RevisorTextoIndisponivel`` em falhas. O método
        existe para isolar a chamada externa atrás de um contrato da aplicação.
        """
        ...


class RevisarTexto:
    """Revisa um campo de texto aplicando as regras da experiência guiada.

    O caso de uso recusa texto vazio sem chamar a IA, limpa e limita as
    sugestões a três e marca se o texto pode ser mantido. Ele existe para
    concentrar essas regras fora do provedor de IA e do transporte HTTP.
    """

    def __init__(self, revisor: RevisorTextoIa) -> None:
        """Recebe a porta do provedor de IA usada nas revisões.

        A dependência é injetada pela composição, o que permite trocar o
        provedor ou usar um double em testes. Existe para manter o caso de uso
        independente de infraestrutura.
        """
        self._revisor = revisor

    async def executar(
        self,
        campo: CampoRevisavel,
        texto: str,
        pergunta: str | None = None,
        contexto: dict[str, str] | None = None,
    ) -> RevisaoTexto:
        """Revisa o texto do campo e devolve veredito, motivo e sugestões.

        Texto vazio vira ``invalido`` sem consultar a IA; nos demais casos a
        avaliação do provedor é normalizada (sugestões sem espaços sobrando,
        vazias descartadas, no máximo três). Existe para entregar ao estudante
        uma revisão consistente qualquer que seja a resposta da IA.
        """
        texto = texto.strip()
        if not texto:
            return RevisaoTexto(
                situacao=SituacaoTexto.INVALIDO,
                motivo="Escreva um texto para este campo.",
                sugestoes=[],
                pode_manter_texto=False,
            )
        avaliacao = await self._revisor.avaliar(campo, pergunta, texto, contexto or {})
        return RevisaoTexto(
            situacao=avaliacao.situacao,
            motivo=avaliacao.motivo,
            sugestoes=[s.strip() for s in avaliacao.sugestoes if s.strip()][:3],
            pode_manter_texto=avaliacao.situacao is not SituacaoTexto.INVALIDO,
        )
