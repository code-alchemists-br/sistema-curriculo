"""Cliente HTTP adaptador para integração com a API de vagas do Grupo 2.

O módulo implementa a porta BuscadorVagas da camada Application, realizando
requisições HTTP assíncronas utilizando a biblioteca padrão (urllib encapsulado
via asyncio.to_thread). Ele lida com a desserialização defensiva do payload JSON
recebido do Grupo 2, converte chaves ausentes/nulas para o DTO canônico VagaExternaDto,
traduz respostas malformadas ou HTTP 5xx para RespostaInvalidaVagas e mapeia
timeouts e falhas de conexão para TimeoutIntegracaoVagas, preservando os parâmetros
de busca para viabilizar novas tentativas sem perda de filtros.
"""

from __future__ import annotations

import asyncio
import json
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from typing import Any

from backend.application.consulta_vagas import (
    RespostaInvalidaVagas,
    TimeoutIntegracaoVagas,
)
from backend.application.ports import BuscadorVagas, VagaExternaDto


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
def mapear_vaga_grupo2_para_dto(item: Any) -> VagaExternaDto:
    """Converte um objeto JSON individual retornado pelo Grupo 2 no DTO interno VagaExternaDto.

    A função valida a presença dos campos obrigatórios e trata campos opcionais
    e nulos com tolerância defensiva: converte requisitos nulos ou ausentes em tupla vazia
    e substitui valores ausentes ou nulos em localização, modalidade e url_candidatura por
    strings vazias seguras. Ela existe para desacoplar a camada Application da estrutura
    específica de payload de terceiros e evitar falhas de execução por campos incompletos.
    """
    if not isinstance(item, dict):
        raise ValueError("O item de vaga deve ser um dicionário JSON.")

    # Se o item vier envelopado com a chave "vaga" (conforme Contrato 3 de associações)
    dados = item.get("vaga") if isinstance(item.get("vaga"), dict) else item

    id_vaga = dados.get("id")
    titulo = dados.get("titulo")
    empresa = dados.get("empresa")
    descricao = dados.get("descricao")

    # Validação de campos obrigatórios conforme contrato de integração (Contrato 2)
    if not all(isinstance(v, str) and v.strip() for v in (id_vaga, titulo, empresa)):
        raise ValueError(
            "Vaga sem campos obrigatórios essenciais (id, titulo ou empresa)."
        )

    if descricao is None or not isinstance(descricao, str):
        raise ValueError("Vaga sem descrição válida.")

    # Requisitos: garantir que resulte sempre em tupla de strings
    requisitos_brutos = dados.get("requisitos")
    if isinstance(requisitos_brutos, (list, tuple)):
        requisitos = tuple(str(r) for r in requisitos_brutos if r is not None)
    else:
        requisitos = ()

    # Campos opcionais: normalizar nulos e tipos para string segura
    localizacao = str(dados.get("localizacao") or "").strip()
    modalidade = str(dados.get("modalidade") or "").strip()
    url_candidatura = str(dados.get("url_candidatura") or "").strip()

    return VagaExternaDto(
        id=str(id_vaga),
        titulo=str(titulo),
        empresa=str(empresa),
        descricao=str(descricao),
        requisitos=requisitos,
        localizacao=localizacao,
        modalidade=modalidade,
        url_candidatura=url_candidatura,
    )


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
class ClienteApiVagasGrupo2Http(BuscadorVagas):
    """Implementa a porta BuscadorVagas realizando chamadas HTTP para o serviço do Grupo 2.

    A classe monta a requisição HTTP com parâmetros de busca, executa a chamada
    através de um executor em thread (asyncio.to_thread) para não bloquear o loop de
    eventos e normaliza as respostas e falhas do provedor externo. Ela existe para fornecer
    uma implementação real e resiliente da porta de busca de vagas sem requisições concorrentes bloqueantes.
    """

    def __init__(
        self,
        url_base: str = "https://grupo2.exemplo.com/api/vagas",
        timeout_segundos: float = 5.0,
        executor_http: Callable[[str, float], bytes] | None = None,
    ) -> None:
        """Inicializa o cliente HTTP com a URL base, timeout e executor configuráveis.

        O construtor recebe os parâmetros de conexão e aceita uma função de transporte
        customizada para injeção de dependência em testes. Ele existe para permitir testes
        unitários determinísticos em memória sem chamadas reais de rede.
        """
        self._url_base = url_base.rstrip("/")
        self._timeout_segundos = timeout_segundos
        self._executor_http = executor_http or self._executar_requisicao_padrao

    def _executar_requisicao_padrao(self, url: str, timeout: float) -> bytes:
        """Executa uma requisição HTTP GET síncrona utilizando urllib.request.

        O método cria a requisição com headers adequados de aceitação de JSON e
        lê o corpo da resposta respeitando o tempo limite configurado. Ele existe
        para isolar a chamada de rede bruta em uma função delegável a workers de thread.
        """
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "SistemaCurriculo-Grupo1/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read()

    async def buscar_vagas(
        self,
        termo: str = "",
        filtros: dict[str, Any] | None = None,
    ) -> list[VagaExternaDto]:
        """Consulta as vagas na API do Grupo 2 com os filtros e termo especificados.

        O método monta a URL de busca codificando parâmetros na query string,
        delega a execução do I/O para uma thread assíncrona, intercepta falhas de rede,
        timeouts e formatos inválidos de retorno, convertendo-os nas exceções canônicas
        da camada Application. Ele existe para cumprir o contrato da porta BuscadorVagas.
        """
        filtros_dict = dict(filtros) if filtros is not None else {}
        parametros_busca: dict[str, str] = {}
        if termo.strip():
            parametros_busca["termo"] = termo.strip()

        for chave, valor in filtros_dict.items():
            if valor is not None:
                parametros_busca[str(chave)] = str(valor)

        query_string = urllib.parse.urlencode(parametros_busca)
        url = f"{self._url_base}?{query_string}" if query_string else self._url_base

        try:
            conteudo_bruto = await asyncio.to_thread(
                self._executor_http,
                url,
                self._timeout_segundos,
            )
        except (TimeoutError, urllib.error.URLError) as erro:
            # Verifica se o URLError foi causado por timeout
            razao = getattr(erro, "reason", None)
            if (
                isinstance(erro, TimeoutError)
                or isinstance(razao, TimeoutError)
                or "timed out" in str(erro).lower()
            ):
                raise TimeoutIntegracaoVagas(
                    mensagem="Tempo limite excedido ao consultar o serviço externo de vagas.",
                    termo=termo,
                    filtros=filtros_dict,
                ) from erro
            # Outros erros de rede ou conexão também são tratados defensivamente
            raise TimeoutIntegracaoVagas(
                mensagem=f"Falha de conexão com a API de vagas: {erro}",
                termo=termo,
                filtros=filtros_dict,
            ) from erro
        except Exception as erro:
            raise RespostaInvalidaVagas(
                mensagem=f"Erro inesperado durante a comunicação com o serviço de vagas: {erro}",
                termo=termo,
                filtros=filtros_dict,
            ) from erro

        # Processamento e decodificação do payload JSON
        try:
            texto = conteudo_bruto.decode("utf-8")
            dados = json.loads(texto)
        except (UnicodeDecodeError, json.JSONDecodeError) as erro:
            raise RespostaInvalidaVagas(
                mensagem="A resposta retornada pela API de vagas não é um JSON válido.",
                termo=termo,
                filtros=filtros_dict,
            ) from erro

        # O payload pode ser uma lista direta de vagas ou um dicionário contendo "associacoes" ou "vagas"
        itens: list[Any] = []
        if isinstance(dados, list):
            itens = dados
        elif isinstance(dados, dict):
            if "associacoes" in dados and isinstance(dados["associacoes"], list):
                itens = dados["associacoes"]
            elif "vagas" in dados and isinstance(dados["vagas"], list):
                itens = dados["vagas"]
            else:
                raise RespostaInvalidaVagas(
                    mensagem="Estrutura de dados inesperada no JSON de vagas recebido do Grupo 2.",
                    termo=termo,
                    filtros=filtros_dict,
                )
        else:
            raise RespostaInvalidaVagas(
                mensagem="Formato raiz da resposta da API de vagas inválido.",
                termo=termo,
                filtros=filtros_dict,
            )

        # Mapeamento defensivo item a item
        vagas_mapeadas: list[VagaExternaDto] = []
        for item in itens:
            try:
                vagas_mapeadas.append(mapear_vaga_grupo2_para_dto(item))
            except ValueError as erro:
                raise RespostaInvalidaVagas(
                    mensagem=f"Falha de schema ao converter vaga externa: {erro}",
                    termo=termo,
                    filtros=filtros_dict,
                ) from erro

        return vagas_mapeadas
