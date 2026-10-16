"""Orquestra a consulta assíncrona de vagas em serviço externo.

O módulo define as exceções canônicas de integração de vagas, os parâmetros de
entrada tipados e o caso de uso que interage com a porta BuscadorVagas. Ele
existe para concentrar a busca de oportunidades externas na camada Application,
mantendo a independência do transporte e protegendo os filtros originais em falhas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

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

    A estrutura imutável armazena o termo textual de pesquisa e filtros opcionais.
    Ela existe para transportar com segurança os parâmetros de consulta da borda
    para o caso de uso na camada de aplicação.
    """

    termo: str = ""
    filtros: dict[str, Any] = field(default_factory=dict)


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
class ConsultarVagas:
    """Orquestra a consulta assíncrona de vagas utilizando a porta BuscadorVagas.

    O caso de uso recebe os parâmetros de busca, normaliza entradas e delega
    a pesquisa para a abstração do buscador externo configurado. Ele existe para
    desacoplar as regras de consulta de detalhes de transporte ou fornecedores concretos.
    """

    def __init__(self, buscador_vagas: BuscadorVagas) -> None:
        """Injeta a porta abstrata responsável pela busca de vagas.

        O construtor armazena a referência para a abstração BuscadorVagas sem conhecer
        detalhes da implementação concreta de rede ou persistência. Ele existe para
        possibilitar a substituição por test doubles em testes unitários.
        """
        self._buscador_vagas = buscador_vagas

    async def executar(self, entrada: ConsultarVagasEntrada) -> list[VagaExternaDto]:
        """Executa a busca de vagas através da porta configurada.

        O método encaminha o termo e os filtros da entrada para o buscador assíncrono
        e retorna a coleção de DTOs imutáveis obtida. Ele existe para fornecer um ponto
        de entrada único e consistente para a consulta de oportunidades externas.
        """
        return await self._buscador_vagas.buscar_vagas(
            termo=entrada.termo,
            filtros=entrada.filtros if entrada.filtros else None,
        )
