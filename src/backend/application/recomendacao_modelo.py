"""Recomenda com IA o modelo de currículo que melhor se encaixa no perfil salvo."""

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from pydantic import BaseModel

from backend.domain.modelo_curriculo import ModeloCurriculo


@dataclass(frozen=True)
class InformacaoPerfil:
    """Um dado profissional do estudante, descrito como pergunta e resposta."""

    pergunta: str
    resposta: str


class RecomendacaoModelo(BaseModel):
    """Modelo recomendado, o motivo e uma segunda opção."""

    modelo: ModeloCurriculo
    motivo: str
    alternativa: ModeloCurriculo | None


class RecomendadorModeloIndisponivel(RuntimeError):
    """A IA não está configurada ou falhou ao recomendar o modelo."""


class LeitorPerfil(Protocol):
    """Porta que lê os dados profissionais salvos, sem nome nem contatos."""

    async def informacoes(self, usuario_id: UUID) -> list[InformacaoPerfil]: ...


class RecomendadorModeloIa(Protocol):
    """Porta para o provedor de IA que escolhe o modelo."""

    async def recomendar(self, perfil: list[InformacaoPerfil]) -> RecomendacaoModelo: ...


class RecomendarModeloCurriculo:
    """Caso de uso: junta o perfil salvo com dados extras e pede a recomendação à IA."""

    def __init__(self, recomendador: RecomendadorModeloIa, leitor: LeitorPerfil) -> None:
        self._recomendador = recomendador
        self._leitor = leitor

    async def executar(
        self, usuario_id: UUID, extras: list[InformacaoPerfil] | None = None
    ) -> RecomendacaoModelo:
        perfil = await self._leitor.informacoes(usuario_id) + (extras or [])
        if not perfil:
            raise ValueError("Salve pelo menos um item do perfil antes de pedir a recomendação.")
        return await self._recomendador.recomendar(perfil)
