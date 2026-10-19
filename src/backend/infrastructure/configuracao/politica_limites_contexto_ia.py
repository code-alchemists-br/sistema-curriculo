"""Lê e recarrega a política local de limites para contexto de IA.

O adapter observa um arquivo JSON mantido no servidor, valida seu conteúdo e
preserva a última versão válida durante uma edição inválida. Ele existe para
permitir ajuste operacional sem expor escrita pela API ou reiniciar o processo.
"""

import json
import logging
from pathlib import Path
from threading import Lock
from typing import Any, Mapping

from backend.application.politica_limites_contexto_ia import (
    FontePoliticaLimitesContextoIa,
    LimitesContextoIa,
    PoliticaLimitesContextoIa,
    SobrescritaLimitesContextoIa,
)

_LOGGER = logging.getLogger(__name__)


def caminho_politica_limites_contexto_ia_padrao() -> Path:
    """Informa o arquivo de política distribuído junto ao servidor do backend.

    A função resolve o caminho a partir deste adapter, sem depender do diretório
    de trabalho do processo. Ela existe para que a composição use uma fonte
    local estável e operadores alterem somente o arquivo do servidor.
    """
    return Path(__file__).resolve().parents[2] / "config" / "limites_contexto_ia.json"


class PoliticaLimitesContextoIaInvalida(ValueError):
    """Indica que o arquivo local não contém uma política utilizável.

    A exceção normaliza falhas de leitura, JSON e validação de esquema. Ela
    existe para que a composição trate uma configuração inicial inválida como
    falha explícita, sem iniciar com limites desconhecidos.
    """


class FonteArquivoPoliticaLimitesContextoIa(FontePoliticaLimitesContextoIa):
    """Fornece a política vigente a partir de um arquivo JSON interno ao servidor.

    A classe identifica alterações pela assinatura do arquivo antes de cada
    leitura, recarrega uma nova versão válida sob lock e mantém a última válida
    se a nova estiver incompleta ou inválida. Ela existe para aplicar ajustes
    operacionais sem endpoint administrativo nem reinicialização da aplicação.
    """

    def __init__(self, caminho: Path) -> None:
        """Prepara a fonte para observar o arquivo indicado pelo servidor.

        O construtor apenas guarda o caminho e inicializa o cache protegido por
        lock; a primeira leitura ocorre sob demanda. Ele existe para que a
        composição possa criar a fonte sem I/O ou falha prematura no startup.
        """
        self._caminho = caminho
        self._lock = Lock()
        self._politica: PoliticaLimitesContextoIa | None = None
        self._assinatura_carregada: tuple[int, int, int] | None = None
        self._assinatura_rejeitada: tuple[int, int, int] | None = None

    def obter(self) -> PoliticaLimitesContextoIa:
        """Devolve a política válida mais recente disponível no arquivo observado.

        O método compara a assinatura do arquivo com o cache e só o interpreta
        quando houve mudança. Em falha posterior a uma carga válida, registra o
        problema uma vez e conserva a política anterior; na primeira carga,
        propaga uma exceção explícita. Ele existe para evitar interrupções e
        comportamento inseguro durante atualizações manuais do arquivo.
        """
        with self._lock:
            assinatura = self._obter_assinatura()
            if self._politica is not None and assinatura == self._assinatura_carregada:
                return self._politica
            if self._politica is not None and assinatura == self._assinatura_rejeitada:
                return self._politica
            try:
                politica = self._ler_politica()
            except PoliticaLimitesContextoIaInvalida as erro:
                if self._politica is None:
                    raise
                self._assinatura_rejeitada = assinatura
                _LOGGER.warning(
                    "Política de limites de IA inválida; a última versão válida será mantida.",
                    extra={"arquivo_configuracao": str(self._caminho), "erro": str(erro)},
                )
                return self._politica
            self._politica = politica
            self._assinatura_carregada = assinatura
            self._assinatura_rejeitada = None
            return politica

    def _obter_assinatura(self) -> tuple[int, int, int] | None:
        """Calcula a assinatura estável usada para decidir se o arquivo mudou.

        O método usa inode, tamanho e nanosegundos de modificação, retornando
        ausência quando o arquivo não existir. Ele existe para evitar parsing
        repetido da mesma política sem depender de observadores do sistema.
        """
        try:
            status = self._caminho.stat()
        except OSError:
            return None
        return status.st_ino, status.st_size, status.st_mtime_ns

    def _ler_politica(self) -> PoliticaLimitesContextoIa:
        """Lê, interpreta e converte o JSON em uma política imutável validada.

        O método traduz erros de I/O, sintaxe e esquema para a exceção pública
        do adapter. Ele existe para assegurar que o cache só seja trocado por
        uma política completamente validada.
        """
        try:
            conteudo = self._caminho.read_text(encoding="utf-8")
            dados = json.loads(conteudo)
            return _converter_politica(dados)
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as erro:
            raise PoliticaLimitesContextoIaInvalida(
                f"Arquivo de política inválido em {self._caminho}."
            ) from erro


def _converter_politica(dados: Any) -> PoliticaLimitesContextoIa:
    """Converte o documento JSON validado no value object usado pela aplicação.

    A função exige todas as chaves estruturais e transforma cada substituição
    em objeto tipado antes de validar seus tetos. Ela existe para manter o
    formato operacional do arquivo isolado do contrato interno.
    """
    raiz = _como_mapa(dados, "raiz")
    _exigir_chaves(raiz, {"versao", "padrao", "teto_seguranca", "substituicoes"}, "raiz")
    substituicoes = _como_mapa(raiz["substituicoes"], "substituicoes")
    _exigir_chaves(
        substituicoes,
        {"por_acao", "por_modelo", "por_acao_modelo"},
        "substituicoes",
    )
    politica = PoliticaLimitesContextoIa(
        versao=raiz["versao"],
        padrao=_converter_limites(raiz["padrao"], "padrao"),
        teto_seguranca=_converter_limites(raiz["teto_seguranca"], "teto_seguranca"),
        por_acao=_converter_sobrescritas(substituicoes["por_acao"], "por_acao"),
        por_modelo=_converter_sobrescritas(substituicoes["por_modelo"], "por_modelo"),
        por_acao_modelo={
            acao: _converter_sobrescritas(por_modelo, f"por_acao_modelo.{acao}")
            for acao, por_modelo in _como_mapa(
                substituicoes["por_acao_modelo"], "por_acao_modelo"
            ).items()
        },
    )
    politica.resolver(None, None)
    for acao in politica.por_acao:
        politica.resolver(acao, None)
    for modelo in politica.por_modelo:
        politica.resolver(None, modelo)
    for acao, por_modelo in politica.por_acao_modelo.items():
        for modelo in por_modelo:
            politica.resolver(acao, modelo)
    return politica


def _converter_limites(dados: Any, nome: str) -> LimitesContextoIa:
    """Converte uma seção completa de limites do documento de configuração.

    A função exige orçamento e campos limitados para produzir um value object
    completo. Ela existe para diferenciar o padrão e o teto das sobrescritas
    parciais aceitas nas seções específicas.
    """
    limites = _como_mapa(dados, nome)
    _exigir_chaves(limites, {"limites_campos", "orcamento_total_caracteres"}, nome)
    return LimitesContextoIa(
        limites_campos=_como_mapa(limites["limites_campos"], f"{nome}.limites_campos"),
        orcamento_total_caracteres=limites["orcamento_total_caracteres"],
    )


def _converter_sobrescritas(dados: Any, nome: str) -> dict[str, SobrescritaLimitesContextoIa]:
    """Converte um mapa nomeado de substituições parciais de limites.

    A função preserva cada identificador de ação ou modelo e delega a validação
    de seus valores. Ela existe para aplicar a mesma regra de esquema nos três
    níveis de precedência do arquivo.
    """
    return {
        chave: _converter_sobrescrita(valor, f"{nome}.{chave}")
        for chave, valor in _como_mapa(dados, nome).items()
    }


def _converter_sobrescrita(dados: Any, nome: str) -> SobrescritaLimitesContextoIa:
    """Converte uma substituição parcial sem permitir chaves inesperadas.

    A função admite limites de campo, orçamento ou ambos e exige pelo menos um
    deles. Ela existe para detectar erros de digitação antes que afetem o
    contexto enviado ao provedor de IA.
    """
    sobrescrita = _como_mapa(dados, nome)
    permitidas = {"limites_campos", "orcamento_total_caracteres"}
    if not sobrescrita or not set(sobrescrita).issubset(permitidas):
        raise ValueError(f"{nome} contém chaves ausentes ou não permitidas.")
    return SobrescritaLimitesContextoIa(
        limites_campos=(
            _como_mapa(sobrescrita["limites_campos"], f"{nome}.limites_campos")
            if "limites_campos" in sobrescrita
            else {}
        ),
        orcamento_total_caracteres=sobrescrita.get("orcamento_total_caracteres"),
    )


def _como_mapa(valor: Any, nome: str) -> Mapping[str, Any]:
    """Garante que uma seção JSON seja um objeto com chaves textuais.

    A função rejeita listas, escalares e chaves não textuais antes da conversão.
    Ela existe para dar erros de configuração determinísticos em vez de falhas
    incidentais durante a resolução da política.
    """
    if not isinstance(valor, dict) or not all(isinstance(chave, str) for chave in valor):
        raise ValueError(f"{nome} deve ser um objeto JSON.")
    return valor


def _exigir_chaves(dados: Mapping[str, Any], esperadas: set[str], nome: str) -> None:
    """Exige que um objeto tenha exatamente as chaves previstas no esquema.

    A função compara conjuntos para detectar omissões e erros de digitação. Ela
    existe para impedir que configurações parcialmente ignoradas aparentem ter
    sido aplicadas quando, na prática, não foram.
    """
    if set(dados) != esperadas:
        raise ValueError(f"{nome} deve conter exatamente: {', '.join(sorted(esperadas))}.")
