"""Recomenda com IA o modelo de currículo que melhor se encaixa no perfil salvo.

O módulo define as portas de leitura do perfil e do provedor de IA e o caso de
uso que os combina. Ele existe para sugerir ao estudante um dos modelos do
catálogo a partir do que ele já salvou, sem acoplar a aplicação ao fornecedor.
"""

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from pydantic import BaseModel

from backend.domain.modelo_curriculo import ModeloCurriculo


@dataclass(frozen=True)
class InformacaoPerfil:
    """Representa um dado profissional do estudante como pergunta e resposta.

    O par textual é o formato comum entre o perfil lido do banco e os dados
    extras enviados pela tela. Ele existe para que o provedor de IA receba o
    perfil como texto simples, sem depender das entidades do domínio.
    """

    pergunta: str
    resposta: str


class RecomendacaoModelo(BaseModel):
    """Descreve o modelo recomendado, o motivo e uma segunda opção.

    O modelo valida que a IA só devolva modelos do catálogo e também serve como
    esquema de saída pedido ao provedor. Ele existe para que a tela mostre uma
    recomendação explicada e uma alternativa ao estudante.
    """

    modelo: ModeloCurriculo
    motivo: str
    alternativa: ModeloCurriculo | None


class RecomendadorModeloIndisponivel(RuntimeError):
    """Sinaliza que a IA não está configurada ou falhou ao recomendar o modelo.

    A exceção é traduzida pela API em indisponível (503). Ela existe para que a
    recomendação seja opcional e a tela possa seguir com a escolha manual.
    """


class LeitorPerfil(Protocol):
    """Define a porta que lê os dados profissionais salvos do estudante.

    A leitura devolve formação, experiências, projetos e demais itens como
    ``InformacaoPerfil``, sem nome nem contatos. A porta existe para que dados
    pessoais não sejam enviados à IA e para isolar o caso de uso do ORM.
    """

    async def informacoes(self, usuario_id: UUID) -> list[InformacaoPerfil]:
        """Lista os dados profissionais salvos do estudante.

        A implementação consulta a persistência e descreve cada item como
        pergunta e resposta. Existe para alimentar a recomendação com o perfil
        real do estudante.
        """
        ...


class RecomendadorModeloIa(Protocol):
    """Define a porta para o provedor de IA que escolhe o modelo de currículo.

    Implementações recebem o perfil descrito como texto e devolvem uma
    ``RecomendacaoModelo``. A porta existe para que o caso de uso não dependa
    do SDK de nenhum fornecedor específico.
    """

    async def recomendar(self, perfil: list[InformacaoPerfil]) -> RecomendacaoModelo:
        """Escolhe o modelo do catálogo que melhor combina com o perfil.

        A implementação consulta o provedor de IA e lança
        ``RecomendadorModeloIndisponivel`` em falhas. Existe para isolar a
        chamada externa atrás de um contrato da aplicação.
        """
        ...


class RecomendarModeloCurriculo:
    """Recomenda o modelo de currículo a partir do perfil salvo e de extras.

    O caso de uso lê o perfil profissional do estudante, acrescenta os dados
    extras enviados pela tela (como o objetivo do currículo) e pede a
    recomendação ao provedor. Ele existe para orientar a escolha do modelo.
    """

    def __init__(self, recomendador: RecomendadorModeloIa, leitor: LeitorPerfil) -> None:
        """Recebe as portas do provedor de IA e da leitura do perfil.

        As dependências são injetadas pela composição, o que permite usar
        doubles em testes. Existe para manter o caso de uso independente de
        infraestrutura.
        """
        self._recomendador = recomendador
        self._leitor = leitor

    async def executar(
        self, usuario_id: UUID, extras: list[InformacaoPerfil] | None = None
    ) -> RecomendacaoModelo:
        """Recomenda o modelo para o estudante informado.

        Junta o perfil salvo com os extras e recusa com ``ValueError`` quando
        não há nenhuma informação, já que a IA não teria base para decidir.
        Existe para entregar uma recomendação apenas quando há dados suficientes.
        """
        perfil = await self._leitor.informacoes(usuario_id) + (extras or [])
        if not perfil:
            raise ValueError("Salve pelo menos um item do perfil antes de pedir a recomendação.")
        return await self._recomendador.recomendar(perfil)
