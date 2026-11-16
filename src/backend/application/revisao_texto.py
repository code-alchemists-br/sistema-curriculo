"""Revisa com IA um campo de texto do formulário antes de o estudante salvá-lo."""

from enum import StrEnum
from typing import Protocol

from pydantic import BaseModel


class CampoRevisavel(StrEnum):
    """Campos de texto livre do formulário que passam pela revisão da IA."""

    DESCRICAO_EXPERIENCIA = "descricao_experiencia"
    DESCRICAO_PROJETO = "descricao_projeto"
    DESCRICAO_CURSO = "descricao_curso"
    DESCRICAO_CERTIFICACAO = "descricao_certificacao"
    OBJETIVO_PROFISSIONAL = "objetivo_profissional"
    OUTRO = "outro"


class SituacaoTexto(StrEnum):
    """Veredito da IA: o texto já serve, pode melhorar ou não responde à pergunta."""

    VALIDO = "valido"
    MELHORADO = "melhorado"
    INVALIDO = "invalido"


class AvaliacaoIa(BaseModel):
    """O que a IA devolve: veredito, motivo e três sugestões de texto."""

    situacao: SituacaoTexto
    motivo: str
    sugestoes: list[str]


class RevisaoTexto(BaseModel):
    """Resultado da revisão; texto inválido não pode ser mantido como está."""

    situacao: SituacaoTexto
    motivo: str
    sugestoes: list[str]
    pode_manter_texto: bool


class RevisorTextoIndisponivel(RuntimeError):
    """A IA não está configurada ou falhou ao revisar o texto."""


class RevisorTextoIa(Protocol):
    """Porta para o provedor de IA que avalia e reescreve um campo."""

    async def avaliar(
        self, campo: CampoRevisavel, pergunta: str | None, texto: str, contexto: dict[str, str]
    ) -> AvaliacaoIa: ...


class RevisarTexto:
    """Caso de uso: recusa texto vazio sem chamar a IA e limita a três sugestões."""

    def __init__(self, revisor: RevisorTextoIa) -> None:
        self._revisor = revisor

    async def executar(
        self,
        campo: CampoRevisavel,
        texto: str,
        pergunta: str | None = None,
        contexto: dict[str, str] | None = None,
    ) -> RevisaoTexto:
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
