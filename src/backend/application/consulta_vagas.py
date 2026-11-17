"""Orquestra a consulta assíncrona de vagas em serviço externo.

O módulo define as exceções canônicas de integração de vagas, os parâmetros de
entrada tipados e o caso de uso que interage com a porta BuscadorVagas. Ele
existe para concentrar a busca de oportunidades externas na camada Application,
mantendo a independência do transporte e protegendo os filtros originais em falhas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID

from backend.application.curriculo_completo import (
    CurriculoCompleto,
    RepositorioCurriculoCompleto,
)
from backend.application.ports import BuscadorVagas, VagaExternaDto


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
class ErroIntegracaoVagas(Exception):
    """Representa uma falha genérica na comunicação com o serviço externo de vagas.

    A classe armazena a mensagem de erro, o termo consultado e o dicionário de
    filtros utilizados na requisição original. Ela existe como base hierárquica para
    que as camadas superiores tratem problemas de integração mantendo o contexto de busca.
    """

    def __init__(
        self,
        mensagem: str,
        termo: str = "",
        filtros: dict[str, Any] | None = None,
    ) -> None:
        """Inicializa a exceção com mensagem descritiva e os parâmetros da busca efetuada.

        O construtor delega a mensagem para a classe base Exception e copia com segurança
        o dicionário de filtros recebido. Ele existe para preservar os critérios de busca
        em qualquer cenário de erro decorrente da integração.
        """
        super().__init__(mensagem)
        self.termo = termo
        self.filtros = dict(filtros) if filtros is not None else {}


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
class RespostaInvalidaVagas(ErroIntegracaoVagas):
    """Sinaliza que a resposta da integração de vagas é inválida, corrompida ou malformada.

    A classe estende ErroIntegracaoVagas especializando ocorrências de quebra de contrato,
    campos obrigatórios ausentes ou erros HTTP de servidor (5xx). Ela existe para
    permitir que a aplicação identifique falhas de especificação de forma amigável ao usuário.
    """


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
class TimeoutIntegracaoVagas(ErroIntegracaoVagas):
    """Representa esgotamento do tempo limite ou indisponibilidade temporária na busca.

    A classe estende ErroIntegracaoVagas mantendo os parâmetros de pesquisa originais.
    Ela existe para satisfazer o requisito de erro transitório (subtarefa #240 / RNF06),
    viabilizando que a interface ofereça nova tentativa sem perda dos filtros preenchidos.
    """


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
@dataclass(frozen=True, slots=True)
class ConsultarVagasEntrada:
    """Encapsula os critérios de busca de vagas fornecidos pelo solicitante.

    A estrutura imutável armazena o termo textual de pesquisa, filtros opcionais,
    a identidade do estudante autenticado e o limite opcional de recomendações.
    Ela existe para transportar com segurança os parâmetros de consulta da borda
    para o caso de uso na camada de aplicação.
    """

    termo: str = ""
    filtros: dict[str, Any] = field(default_factory=dict)
    usuario_id: UUID | None = None
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class VagaRecomendadaDto:
    """Representa de forma imutável uma vaga recomendada com metadados de matching.

    O DTO preserva os oito campos básicos de vaga externa e acrescenta ranque,
    pontuação de compatibilidade, elegibilidade ativa, senioridade, faixa salarial,
    palavras-chave, data de publicação e requisitos atendidos ou faltantes. Ele
    existe para transportar a resposta enriquecida do cvmatch sem alterar o
    contrato congelado de ``VagaExternaDto``.
    """

    id: str
    titulo: str
    empresa: str
    descricao: str
    requisitos: tuple[str, ...]
    localizacao: str
    modalidade: str
    url_candidatura: str
    ranque: int | None = None
    pontuacao_compatibilidade: float | None = None
    elegivel: bool | None = None
    nivel_senioridade: str | None = None
    salario: str | None = None
    moeda: str | None = None
    palavras_chave: tuple[str, ...] = ()
    data_publicacao: str | None = None
    requisitos_atendidos: tuple[str, ...] = ()
    requisitos_faltantes: tuple[str, ...] = ()


class BuscadorVagasPorCurriculo(Protocol):
    """Define a porta assíncrona para buscar vagas compatíveis por currículo.

    O protocolo recebe o currículo completo lido para o estudante e o limite
    desejado de recomendações, retornando DTOs ranqueados. Ele existe para
    desacoplar o caso de uso do transporte HTTP específico do serviço cvmatch.
    """

    async def buscar_vagas_por_curriculo(
        self,
        curriculo: CurriculoCompleto,
        limit: int = 10,
    ) -> list[VagaRecomendadaDto]:
        """Consulta vagas compatíveis com o currículo informado.

        Implementações enviam a projeção autorizada do currículo ao motor de
        matching e convertem a resposta em DTOs imutáveis. O método existe para
        manter a camada Application independente de detalhes HTTP.
        """
        ...


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
class ConsultarVagas:
    """Orquestra a consulta assíncrona de vagas utilizando as portas configuradas.

    O caso de uso suporta tanto a busca por currículo via ``BuscadorVagasPorCurriculo``
    (lendo os dados ativos em ``RepositorioCurriculoCompleto``) quanto a porta
    legada ``BuscadorVagas`` baseada em termo e filtros. Ele existe para
    desacoplar as regras de consulta de detalhes de transporte ou persistência.
    """

    def __init__(
        self,
        buscador_vagas: BuscadorVagas | None = None,
        *,
        buscador_curriculo: BuscadorVagasPorCurriculo | None = None,
        leitor_curriculo: RepositorioCurriculoCompleto | None = None,
        limite_padrao: int = 10,
    ) -> None:
        """Injeta as portas responsáveis pela busca de vagas e leitura do currículo.

        O construtor armazena o buscador por termo/filtros ou o par de leitura
        de currículo e busca por matching, além do limite padrão validado entre 1
        e 100. Ele existe para possibilitar composição em produção e substituição
        por test doubles em testes unitários.
        """
        if buscador_vagas is None and (
            buscador_curriculo is None or leitor_curriculo is None
        ):
            raise ValueError(
                "Informe buscador_vagas ou o par buscador_curriculo e leitor_curriculo."
            )
        self._buscador_vagas = buscador_vagas
        self._buscador_curriculo = buscador_curriculo
        self._leitor_curriculo = leitor_curriculo
        self._limite_padrao = min(max(limite_padrao, 1), 100)

    async def executar(
        self, entrada: ConsultarVagasEntrada
    ) -> list[VagaExternaDto | VagaRecomendadaDto]:
        """Executa a busca de vagas através da porta configurada.

        Quando configurado com busca por currículo, lê o currículo do estudante
        autenticado, aplica o limite solicitado (ou o padrão) e delega ao
        motor de matching; caso contrário, encaminha termo e filtros à porta
        ``BuscadorVagas``. Ele existe para fornecer um ponto de entrada único e
        consistente para a consulta de oportunidades externas.
        """
        if (
            self._buscador_curriculo is not None
            and self._leitor_curriculo is not None
        ):
            if entrada.usuario_id is None:
                raise ErroIntegracaoVagas(
                    mensagem="Identidade do estudante ausente para consulta por currículo.",
                    termo=entrada.termo,
                    filtros=entrada.filtros,
                )
            curriculo = await self._leitor_curriculo.ler(entrada.usuario_id)
            if curriculo is None:
                return []
            limite = (
                entrada.limit
                if entrada.limit is not None
                else self._limite_padrao
            )
            limite = min(max(limite, 1), 100)
            return list(
                await self._buscador_curriculo.buscar_vagas_por_curriculo(
                    curriculo, limit=limite
                )
            )

        assert self._buscador_vagas is not None
        return list(
            await self._buscador_vagas.buscar_vagas(
                termo=entrada.termo,
                filtros=entrada.filtros if entrada.filtros else None,
            )
        )
