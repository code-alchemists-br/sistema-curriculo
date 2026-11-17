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
from uuid import UUID, uuid4

from backend.application.consulta_vagas import (
    ErroIntegracaoVagas,
    RespostaInvalidaVagas,
    TimeoutIntegracaoVagas,
    VagaRecomendadaDto,
)
from backend.application.curriculo_completo import CurriculoCompleto
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


def _limpar_texto_opcional(valor: Any) -> str | None:
    """Normaliza valores textuais opcionais descartando vazios e espaços.

    Converte somente strings não vazias em texto aparado e retorna ``None`` para
    ausência ou outros tipos. Existe para evitar que campos opcionais nulos ou em
    branco gerem rótulos vazios após a conversão do contrato externo.
    """
    if not isinstance(valor, str):
        return None
    limpo = valor.strip()
    return limpo or None


def _formatar_localizacao_cvmatch(localizacao: Any) -> str:
    """Converte a localização estruturada do cvmatch em texto legível.

    Prioriza ``city`` e ``state`` separados por hífen, recorre a ``country`` ou
    ``raw`` quando ausentes e aceita string direta para tolerância. Existe para
    adaptar o dicionário geográfico do cvmatch para o campo textual único da vaga.
    """
    if isinstance(localizacao, str):
        return _limpar_texto_opcional(localizacao) or ""
    if not isinstance(localizacao, dict):
        return ""
    cidade = _limpar_texto_opcional(localizacao.get("city"))
    estado = _limpar_texto_opcional(localizacao.get("state"))
    partes = [parte for parte in (cidade, estado) if parte]
    if partes:
        return " - ".join(partes)
    pais = _limpar_texto_opcional(localizacao.get("country"))
    if pais:
        return pais
    return _limpar_texto_opcional(localizacao.get("raw")) or ""


def _obter_simbolo_moeda(moeda: Any) -> str:
    """Traduz o código de moeda informado pelo cvmatch em símbolo curto.

    Converte códigos comuns (``BRL``, ``USD``, ``EUR``) para seus símbolos e
    mantém códigos desconhecidos em maiúsculas, assumindo ``R$`` por padrão.
    Existe para formatar valores salariais de forma consistente na resposta.
    """
    codigo = (_limpar_texto_opcional(moeda) or "BRL").upper()
    if codigo == "BRL":
        return "R$"
    if codigo == "USD":
        return "US$"
    if codigo == "EUR":
        return "€"
    return codigo


def _formatar_numero_monetario(valor: int | float) -> str:
    """Formata um número monetário no padrão brasileiro sem separador ambíguo.

    Usa duas casas decimais apenas quando há fração não inteira e substitui os
    separadores para ponto nos milhares e vírgula nos centavos. Existe para
    apresentar bolsas e salários sem depender do locale do sistema operacional.
    """
    if float(valor).is_integer():
        return f"{int(valor):,}".replace(",", ".")
    return f"{float(valor):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def _formatar_salario_cvmatch(salario: Any, moeda: Any) -> str | None:
    """Formata o campo salarial do cvmatch em faixa monetária legível.

    Aceita dicionário (``min``/``max``), número único ou texto já descritivo,
    ignorando valores não positivos e combinando o símbolo da moeda. Existe para
    exibir remuneração ou bolsa sem expor estruturas internas ao consumidor HTTP.
    """
    if salario is None or isinstance(salario, bool):
        return None
    simbolo = _obter_simbolo_moeda(moeda)
    if isinstance(salario, str):
        texto = _limpar_texto_opcional(salario)
        return f"{simbolo} {texto}" if texto else None
    if isinstance(salario, (int, float)):
        return (
            f"{simbolo} {_formatar_numero_monetario(salario)}"
            if salario > 0
            else None
        )
    if not isinstance(salario, dict):
        return None

    valores = sorted(
        valor
        for valor in salario.values()
        if isinstance(valor, (int, float))
        and not isinstance(valor, bool)
        and valor > 0
    )
    if not valores:
        return None
    menor, maior = valores[0], valores[-1]
    if menor == maior:
        return f"{simbolo} {_formatar_numero_monetario(menor)}"
    return (
        f"{simbolo} {_formatar_numero_monetario(menor)} – "
        f"{simbolo} {_formatar_numero_monetario(maior)}"
    )


def _limpar_lista_textos(lista: Any) -> tuple[str, ...]:
    """Filtra uma coleção externa para uma tupla imutável de textos não vazios.

    Percorre apenas listas ou tuplas, convertendo strings aparadas e ignorando
    entradas nulas ou em branco. Existe para padronizar skills, keywords e
    evidências de matching com segurança de tipos.
    """
    if not isinstance(lista, (list, tuple)):
        return ()
    return tuple(
        texto
        for item in lista
        if isinstance(item, str) and (texto := item.strip())
    )


def montar_payload_match_cvmatch(
    curriculo: CurriculoCompleto,
    curriculo_id: UUID | None = None,
) -> dict[str, Any]:
    """Projeta ``CurriculoCompleto`` no payload exato exigido por ``POST /matches``.

    Usa o ``curriculo_id`` informado (ou o persistido no currículo, recorrendo a
    um UUID temporário por requisição) e serializa exclusivamente as cinco
    seções aceitas pelo cvmatch (``formacoes``, ``experiencias``, ``projetos``,
    ``competencias`` e ``idiomas``), omitindo dados pessoais, cursos,
    certificações, layout e ``categoria`` de competência. Existe para atender
    estritamente ao contrato autoritativo com ``extra="forbid"`` do Grupo 2.
    """
    identificador = curriculo_id or curriculo.curriculo_id or uuid4()
    return {
        "curriculo_id": str(identificador),
        "formacoes": [
            {
                "instituicao": formacao.instituicao,
                "curso": formacao.curso,
                "nivel": (
                    formacao.nivel.value
                    if hasattr(formacao.nivel, "value")
                    else str(formacao.nivel)
                ),
                "status": (
                    formacao.status.value
                    if hasattr(formacao.status, "value")
                    else str(formacao.status)
                ),
                "inicio": formacao.data_inicio.isoformat(),
                "fim": (
                    formacao.data_fim.isoformat()
                    if formacao.data_fim is not None
                    else None
                ),
            }
            for formacao in curriculo.formacoes
        ],
        "experiencias": [
            {
                "empresa": experiencia.empresa,
                "cargo": experiencia.cargo,
                "descricao": experiencia.descricao,
                "inicio": experiencia.data_inicio.isoformat(),
                "fim": (
                    experiencia.data_fim.isoformat()
                    if experiencia.data_fim is not None
                    else None
                ),
            }
            for experiencia in curriculo.experiencias
        ],
        "projetos": [
            {
                "titulo": projeto.titulo,
                "descricao": projeto.descricao,
                "tecnologias": projeto.tecnologias,
            }
            for projeto in curriculo.projetos
        ],
        "competencias": [
            {
                "descricao": competencia.descricao,
                "nivel": competencia.nivel,
            }
            for competencia in curriculo.competencias
        ],
        "idiomas": [
            {
                "idioma": idioma.idioma,
                "nivel": idioma.nivel,
            }
            for idioma in curriculo.idiomas
        ],
    }


def mapear_match_cvmatch_para_dto(item: Any) -> VagaRecomendadaDto:
    """Converte um item de ``MatchesResponse.matches`` do cvmatch em ``VagaRecomendadaDto``.

    Valida a presença de ``job``, identificador inteiro positivo (ou string não
    vazia), ``title`` não vazio, ``rank`` inteiro positivo, ``score`` numérico e
    ``eligibility`` booleano, normalizando campos opcionais ausentes ou nulos.
    Existe para isolar o domínio e a API da estrutura específica do Grupo 2.
    """
    if not isinstance(item, dict):
        raise ValueError("Cada match retornado pelo cvmatch deve ser um objeto JSON.")

    job = item.get("job")
    if not isinstance(job, dict):
        raise ValueError("Match sem objeto 'job' válido.")

    id_bruto = job.get("id")
    if isinstance(id_bruto, bool) or id_bruto is None:
        raise ValueError("Vaga do match sem identificador válido.")
    if isinstance(id_bruto, int):
        if id_bruto < 1:
            raise ValueError("Identificador numérico da vaga deve ser positivo.")
        id_vaga = str(id_bruto)
    elif isinstance(id_bruto, str) and id_bruto.strip():
        id_vaga = id_bruto.strip()
    else:
        raise ValueError("Vaga do match sem identificador válido.")

    titulo = _limpar_texto_opcional(job.get("title"))
    if not titulo:
        raise ValueError("Vaga do match sem título válido.")

    ranque = item.get("rank")
    if not isinstance(ranque, int) or isinstance(ranque, bool) or ranque < 1:
        raise ValueError("Match sem ranque inteiro positivo.")

    score = item.get("score")
    if not isinstance(score, (int, float)) or isinstance(score, bool):
        raise ValueError("Match sem pontuação numérica válida.")

    elegivel = item.get("eligibility")
    if not isinstance(elegivel, bool):
        raise ValueError("Match sem indicador booleano de elegibilidade.")

    empresa = _limpar_texto_opcional(job.get("company")) or "Empresa confidencial"
    descricao = _limpar_texto_opcional(job.get("description")) or ""
    requisitos = _limpar_lista_textos(job.get("skills"))
    palavras_chave = _limpar_lista_textos(job.get("keywords"))
    localizacao = _formatar_localizacao_cvmatch(job.get("location"))
    modalidade = _limpar_texto_opcional(job.get("work_arrangement")) or ""
    nivel_senioridade = _limpar_texto_opcional(job.get("seniority_level"))
    moeda = _limpar_texto_opcional(job.get("currency"))
    salario = _formatar_salario_cvmatch(job.get("salary"), moeda)
    url_candidatura = _limpar_texto_opcional(job.get("job_url")) or ""
    data_publicacao = _limpar_texto_opcional(job.get("publication_date"))
    requisitos_atendidos = _limpar_lista_textos(item.get("matched_skills"))
    requisitos_faltantes = _limpar_lista_textos(item.get("missing_requirements"))

    return VagaRecomendadaDto(
        id=id_vaga,
        titulo=titulo,
        empresa=empresa,
        descricao=descricao,
        requisitos=requisitos,
        localizacao=localizacao,
        modalidade=modalidade,
        url_candidatura=url_candidatura,
        ranque=ranque,
        pontuacao_compatibilidade=float(score),
        elegivel=elegivel,
        nivel_senioridade=nivel_senioridade,
        salario=salario,
        moeda=moeda,
        palavras_chave=palavras_chave,
        data_publicacao=data_publicacao,
        requisitos_atendidos=requisitos_atendidos,
        requisitos_faltantes=requisitos_faltantes,
    )


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
class ClienteApiVagasGrupo2Http(BuscadorVagas):
    """Implementa as portas de busca de vagas realizando chamadas HTTP para o Grupo 2.

    A classe suporta o fluxo autoritativo de recomendação por currículo via
    ``POST /matches`` no cvmatch (``BuscadorVagasPorCurriculo``) e preserva a
    porta legada ``BuscadorVagas`` para compatibilidade dos testes existentes.
    Ela existe para fornecer uma implementação resiliente e desacoplada de
    transporte, sem bloquear o loop de eventos assíncrono.
    """

    def __init__(
        self,
        url_base: str = "https://grupo2.exemplo.com/api/vagas",
        timeout_segundos: float = 5.0,
        executor_http: Callable[[str, float], bytes] | None = None,
        executor_post_http: Callable[[str, bytes, float], bytes] | None = None,
    ) -> None:
        """Inicializa o cliente HTTP com a URL base, timeout e executores configuráveis.

        O construtor recebe os parâmetros de conexão e aceita funções de transporte
        customizadas para GET e POST em testes. Ele existe para permitir testes
        unitários determinísticos em memória sem chamadas reais de rede.
        """
        self._url_base = url_base.rstrip("/")
        self._timeout_segundos = timeout_segundos
        self._executor_http = executor_http or self._executar_requisicao_padrao
        self._executor_post_http = (
            executor_post_http or self._executar_requisicao_post_padrao
        )

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

    def _executar_requisicao_post_padrao(
        self, url: str, corpo: bytes, timeout: float
    ) -> bytes:
        """Executa uma requisição HTTP POST síncrona com corpo JSON via urllib.request.

        O método envia os bytes JSON com cabeçalhos explícitos de tipo de conteúdo
        e lê a resposta respeitando o timeout configurado. Ele existe para isolar
        a chamada POST ao cvmatch em função delegável a ``asyncio.to_thread``.
        """
        req = urllib.request.Request(
            url,
            data=corpo,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "SistemaCurriculo-Grupo1/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read()

    def _montar_url_matches(self, limit: int) -> str:
        """Compõe a URL completa de ``POST /matches`` com o parâmetro ``limit``.

        Evita duplicar ``/matches`` quando a URL base já termina nesse segmento e
        restringe ``limit`` ao intervalo ``1..100``. Existe para manter a montagem
        da rota consistente independentemente de barra final na variável de ambiente.
        """
        limite = min(max(limit, 1), 100)
        base = (
            self._url_base
            if self._url_base.endswith("/matches")
            else f"{self._url_base}/matches"
        )
        query = urllib.parse.urlencode({"limit": limite})
        return f"{base}?{query}"

    async def buscar_vagas_por_curriculo(
        self,
        curriculo: CurriculoCompleto,
        limit: int = 10,
    ) -> list[VagaRecomendadaDto]:
        """Consulta recomendações ranqueadas no endpoint ``POST /matches`` do cvmatch.

        Serializa apenas os campos do currículo autorizados pelo contrato, envia o
        POST em thread separada, traduz timeouts, indisponibilidades (429/503/504)
        e respostas inválidas nas exceções canônicas da Application sem vazar
        segredos nem dados pessoais. Existe para integrar o backend ao cvmatch.
        """
        url = self._montar_url_matches(limit)
        corpo = json.dumps(
            montar_payload_match_cvmatch(curriculo),
            ensure_ascii=False,
        ).encode("utf-8")

        try:
            conteudo_bruto = await asyncio.to_thread(
                self._executor_post_http,
                url,
                corpo,
                self._timeout_segundos,
            )
        except urllib.error.HTTPError as erro:
            if erro.code == 504:
                raise TimeoutIntegracaoVagas(
                    mensagem="Tempo limite excedido ao consultar o serviço de matching."
                ) from erro
            if erro.code in (429, 503):
                raise ErroIntegracaoVagas(
                    mensagem="Serviço de matching temporariamente indisponível."
                ) from erro
            raise RespostaInvalidaVagas(
                mensagem=f"Resposta HTTP inesperada do serviço de matching: {erro.code}."
            ) from erro
        except (TimeoutError, urllib.error.URLError) as erro:
            razao = getattr(erro, "reason", None)
            if (
                isinstance(erro, TimeoutError)
                or isinstance(razao, TimeoutError)
                or "timed out" in str(erro).lower()
            ):
                raise TimeoutIntegracaoVagas(
                    mensagem="Tempo limite excedido ao consultar o serviço de matching."
                ) from erro
            raise ErroIntegracaoVagas(
                mensagem=f"Falha de conexão com a API do cvmatch: {erro}"
            ) from erro
        except Exception as erro:
            raise RespostaInvalidaVagas(
                mensagem=f"Erro inesperado durante a comunicação com o cvmatch: {erro}"
            ) from erro

        try:
            dados = json.loads(conteudo_bruto.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as erro:
            raise RespostaInvalidaVagas(
                mensagem="A resposta retornada pela API do cvmatch não é um JSON válido."
            ) from erro

        if not isinstance(dados, dict) or not isinstance(dados.get("matches"), list):
            raise RespostaInvalidaVagas(
                mensagem="Estrutura inesperada na resposta de matches do cvmatch."
            )

        vagas_mapeadas: list[VagaRecomendadaDto] = []
        for item in dados["matches"]:
            try:
                vagas_mapeadas.append(mapear_match_cvmatch_para_dto(item))
            except ValueError as erro:
                raise RespostaInvalidaVagas(
                    mensagem=f"Falha de schema ao converter match do cvmatch: {erro}"
                ) from erro

        return vagas_mapeadas

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
