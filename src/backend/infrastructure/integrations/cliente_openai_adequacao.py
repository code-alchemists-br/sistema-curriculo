"""Implementa o gateway HTTP da Responses API para adequação semântica.

O módulo traduz o contexto mínimo definido pela Application para uma requisição
estruturada da OpenAI e converte a resposta JSON em sugestões de domínio. Ele
existe para manter HTTP, JSON e autenticação bearer fora do caso de uso, sem
persistir ou aplicar automaticamente qualquer sugestão.
"""

from __future__ import annotations

import asyncio
import json
import urllib.request
from collections.abc import Callable
from typing import Any
from urllib.error import URLError

# Proveniência: decision-analysis prompts/backend/20261020-163820-adequacao-semantica-gpt-nano-v001.md#v001
from backend.application.adequacao_semantica import (
    ContextoAdequacaoCurriculoVaga,
    GeracaoPropostaAdequacaoIndisponivel,
)
from backend.domain.adequacao_semantica import SugestaoAdequacao, TipoSugestaoAdequacao
from backend.domain.value_objects import (
    CompetenciaId,
    ExperienciaProfissionalId,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
)

URL_RESPONSES_OPENAI = "https://api.openai.com/v1/responses"


class RespostaOpenAiAdequacaoInvalida(ValueError):
    """Sinaliza falha de transporte ou estrutura inválida da resposta externa.

    A exceção encapsula detalhes de HTTP, decodificação e schema sem expor o
    payload recebido ao restante do backend. Ela existe para que a futura borda
    traduza indisponibilidade do provedor sem depender da biblioteca HTTP.
    """


def montar_requisicao_openai(contexto: ContextoAdequacaoCurriculoVaga) -> dict[str, Any]:
    """Converte o contexto autorizado em payload estruturado da Responses API.

    A função envia cargo, vaga e itens já limitados, preservando referências
    tipadas para que a resposta seja conferida pelo domínio depois. Ela existe
    para separar o formato do provedor do contrato interno e não inclui dados
    pessoais que o caso de uso não autorizou.
    """
    itens = [
        {
            "referencia": _serializar_referencia(item.referencia),
            "conteudo": item.conteudo,
        }
        for item in contexto.itens_selecionados
    ]
    dados = {
        "cargo_alvo": contexto.cargo_alvo,
        "descricao_vaga": contexto.descricao_vaga,
        "itens_selecionados": itens,
    }
    return {
        "model": contexto.modelo,
        "input": [
            {
                "role": "developer",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Produza somente sugestões revisáveis para adequar um currículo "
                            "a uma vaga. Responda no schema solicitado e não altere dados."
                        ),
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": json.dumps(dados, ensure_ascii=False)}
                ],
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "proposta_adequacao_curriculo_vaga",
                "strict": True,
                "schema": _schema_resposta_adequacao(),
            }
        },
    }


def mapear_resposta_openai_para_sugestoes(
    resposta: object,
) -> tuple[SugestaoAdequacao, ...]:
    """Extrai sugestões tipadas do envelope retornado pela Responses API.

    A função localiza o texto de saída, interpreta seu JSON estruturado e
    reconstitui enums e referências de domínio. Ela existe para impedir que o
    formato específico do provedor atravesse a fronteira da infraestrutura.
    """
    if not isinstance(resposta, dict):
        raise RespostaOpenAiAdequacaoInvalida("A resposta da OpenAI deve ser um objeto.")
    texto = _extrair_texto_saida(resposta)
    try:
        dados = json.loads(texto)
    except (TypeError, json.JSONDecodeError) as erro:
        raise RespostaOpenAiAdequacaoInvalida(
            "A saída estruturada da OpenAI não contém JSON válido."
        ) from erro
    if not isinstance(dados, dict) or not isinstance(dados.get("sugestoes"), list):
        raise RespostaOpenAiAdequacaoInvalida(
            "A saída estruturada da OpenAI não contém sugestões válidas."
        )
    try:
        return tuple(_mapear_sugestao(item) for item in dados["sugestoes"])
    except (KeyError, TypeError, ValueError) as erro:
        raise RespostaOpenAiAdequacaoInvalida(
            "A saída estruturada da OpenAI contém sugestão inválida."
        ) from erro


class ClienteOpenAiAdequacaoHttp:
    """Implementa ``GeradorPropostaAdequacao`` por meio da Responses API.

    O cliente monta JSON conforme o contrato externo, envia-o em uma thread para
    não bloquear o loop assíncrono e mapeia apenas a saída estruturada para o
    contrato interno. Ele existe para tornar o provedor substituível e manter a
    Application independente de HTTP, credenciais e detalhes da OpenAI.
    """

    def __init__(
        self,
        api_key: str,
        url_responses: str = URL_RESPONSES_OPENAI,
        executor_http: Callable[[str, bytes, str], bytes] | None = None,
    ) -> None:
        """Recebe a credencial já composta e o transporte HTTP substituível.

        O construtor não lê ambiente nem registra a chave; ele guarda somente a
        credencial recebida pela composição externa e permite um executor falso
        em testes. Ele existe para manter segredo e mecanismo de rede fora do
        caso de uso e tornar a unidade testável sem conexões reais.
        """
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("A chave da API OpenAI deve ser informada.")
        if not isinstance(url_responses, str) or not url_responses.strip():
            raise ValueError("A URL da Responses API deve ser informada.")
        self._api_key = api_key.strip()
        self._url_responses = url_responses.strip()
        self._executor_http = executor_http or self._executar_requisicao_padrao

    async def gerar(
        self, contexto: ContextoAdequacaoCurriculoVaga
    ) -> tuple[SugestaoAdequacao, ...]:
        """Envia o contexto reduzido e devolve sugestões tipadas da OpenAI.

        O método serializa a requisição, executa a chamada bloqueante em thread,
        decodifica o envelope JSON e delega o mapeamento à fronteira externa. Ele
        existe para cumprir a porta interna sem expor HTTP ou payload bruto à
        Application.
        """
        corpo = json.dumps(montar_requisicao_openai(contexto), ensure_ascii=False).encode(
            "utf-8"
        )
        try:
            resposta_bruta = await asyncio.to_thread(
                self._executor_http, self._url_responses, corpo, self._api_key
            )
        except (OSError, URLError) as erro:
            raise GeracaoPropostaAdequacaoIndisponivel(
                "Não foi possível comunicar com a OpenAI."
            ) from erro
        try:
            resposta = json.loads(resposta_bruta.decode("utf-8"))
        except (AttributeError, UnicodeDecodeError, json.JSONDecodeError) as erro:
            raise GeracaoPropostaAdequacaoIndisponivel(
                "A resposta da OpenAI não contém JSON válido."
            ) from erro
        try:
            return mapear_resposta_openai_para_sugestoes(resposta)
        except RespostaOpenAiAdequacaoInvalida as erro:
            raise GeracaoPropostaAdequacaoIndisponivel(
                "A resposta da OpenAI não pôde ser processada."
            ) from erro

    def _executar_requisicao_padrao(
        self, url: str, corpo: bytes, api_key: str
    ) -> bytes:
        """Executa um POST JSON autenticado na Responses API.

        O método constrói a requisição HTTP com os cabeçalhos exigidos e devolve
        somente seus bytes de resposta, sem logar credencial ou conteúdo. Ele
        existe para isolar a operação de rede substituível pelo executor injetado.
        """
        requisicao = urllib.request.Request(
            url,
            data=corpo,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(requisicao) as resposta:
            return resposta.read()


def _serializar_referencia(referencia: ReferenciaCurriculo) -> dict[str, str]:
    """Converte uma referência de domínio em identificador externo estável.

    A função associa o tipo concreto do identificador a um rótulo fechado e
    serializa seu UUID sem dados do proprietário. Ela existe para que o modelo
    possa apontar somente para os itens autorizados no contexto recebido.
    """
    tipos = {
        ExperienciaProfissionalId: "experiencia",
        ProjetoAcademicoId: "projeto",
        CompetenciaId: "competencia",
    }
    tipo = tipos.get(type(referencia.item_id))
    if tipo is None:
        raise RespostaOpenAiAdequacaoInvalida("Tipo de referência não suportado.")
    return {"tipo": tipo, "id": str(referencia.item_id.valor)}


def _mapear_sugestao(item: object) -> SugestaoAdequacao:
    """Converte uma sugestão JSON validada no value object de domínio.

    A função exige os campos estruturais definidos pelo schema e reconstrói uma
    referência opcional antes de instanciar a sugestão. Ela existe para que a
    resposta do provedor não seja usada como objeto de domínio sem validação.
    """
    if not isinstance(item, dict):
        raise ValueError("A sugestão deve ser um objeto JSON.")
    referencia_bruta = item["referencia_item"]
    referencia = (
        None if referencia_bruta is None else _desserializar_referencia(referencia_bruta)
    )
    return SugestaoAdequacao(
        codigo=item["codigo"],
        tipo=TipoSugestaoAdequacao(item["tipo"]),
        referencia_item=referencia,
        texto_sugerido=item["texto_sugerido"],
        justificativa=item["justificativa"],
    )


def _desserializar_referencia(valor: object) -> ReferenciaCurriculo:
    """Reconstrói uma referência tipada a partir da forma JSON da OpenAI.

    A função aceita somente os três tipos profissionais que entram no contexto
    e converte o UUID textual pelo value object correspondente. Ela existe para
    impedir que uma resposta externa aponte para documentos ou dados pessoais.
    """
    if not isinstance(valor, dict):
        raise ValueError("A referência da sugestão deve ser um objeto.")
    tipo = valor.get("tipo")
    identificador = valor.get("id")
    tipos = {
        "experiencia": ExperienciaProfissionalId,
        "projeto": ProjetoAcademicoId,
        "competencia": CompetenciaId,
    }
    classe_id = tipos.get(tipo)
    if classe_id is None or not isinstance(identificador, str):
        raise ValueError("A referência da sugestão é inválida.")
    from uuid import UUID

    return ReferenciaCurriculo(classe_id(UUID(identificador)))


def _extrair_texto_saida(resposta: dict[str, Any]) -> str:
    """Localiza o primeiro texto final entre os itens do envelope Responses.

    A função percorre mensagens e conteúdos sem assumir índices fixos, aceitando
    somente um texto de saída não vazio. Ela existe para proteger o adapter de
    envelopes com itens adicionais que não representam a proposta estruturada.
    """
    saida = resposta.get("output")
    if not isinstance(saida, list):
        raise RespostaOpenAiAdequacaoInvalida("A resposta da OpenAI não possui saída.")
    for item in saida:
        if not isinstance(item, dict) or not isinstance(item.get("content"), list):
            continue
        for conteudo in item["content"]:
            if (
                isinstance(conteudo, dict)
                and conteudo.get("type") == "output_text"
                and isinstance(conteudo.get("text"), str)
                and conteudo["text"].strip()
            ):
                return conteudo["text"]
    raise RespostaOpenAiAdequacaoInvalida(
        "A resposta da OpenAI não possui texto estruturado."
    )


def _schema_resposta_adequacao() -> dict[str, Any]:
    """Define o JSON Schema transportado para estruturar sugestões externas.

    A função descreve somente os campos que o domínio consegue representar e
    restringe tipos de sugestão e referências ao vocabulário permitido. Ela
    existe para que o provedor devolva uma forma verificável antes do mapeamento.
    """
    referencia = {
        "type": "object",
        "properties": {
            "tipo": {"type": "string", "enum": ["experiencia", "projeto", "competencia"]},
            "id": {"type": "string"},
        },
        "required": ["tipo", "id"],
        "additionalProperties": False,
    }
    sugestao = {
        "type": "object",
        "properties": {
            "codigo": {"type": "string"},
            "tipo": {
                "type": "string",
                "enum": [tipo.value for tipo in TipoSugestaoAdequacao],
            },
            "referencia_item": {"anyOf": [referencia, {"type": "null"}]},
            "texto_sugerido": {"type": "string"},
            "justificativa": {"type": "string"},
        },
        "required": [
            "codigo",
            "tipo",
            "referencia_item",
            "texto_sugerido",
            "justificativa",
        ],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {"sugestoes": {"type": "array", "items": sugestao}},
        "required": ["sugestoes"],
        "additionalProperties": False,
    }
