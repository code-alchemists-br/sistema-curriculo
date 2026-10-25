"""Monta busca ASGI de teste com transporte registrado, sem banco nem rede.

Compõe aplicação, middleware, caso de uso e adapter reais com identidade sintética
e fila de bytes/exceções para provar contratos locais. Não é E2E integrado:
não há navegador, rota de vagas no App nem schemas frontend/backend compatíveis;
main não liga o executor e o provedor é simulado. Não certifica produção.
"""

# Proveniência: decision-analysis prompts/frontend/20261024-181303-cenario-busca-vagas-tres-desfechos-v001.md#v001

from collections import deque
from dataclasses import dataclass
from json import dumps
from typing import Any
from uuid import UUID

from fastapi import FastAPI

from backend.api.factory import create_app
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.application.consulta_vagas import ConsultarVagas, ErroIntegracaoVagas
from backend.application.ports import VagaExternaDto
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.integrations.cliente_vagas_grupo2 import (
    ClienteApiVagasGrupo2Http,
)

TOKEN_ACEITO = "sessao-sintetica-vagas"
URL_PROVEDOR = "https://provedor.invalid/vagas"


def vagas_sinteticas() -> list[dict[str, Any]]:
    """Fornece vagas artificiais copiadas por construção para isolar cada teste.

    Monta os oito campos externos, incluindo opcionais nulos na segunda vaga,
    para verificar serialização e normalização sem dados pessoais ou parceiro.
    """
    return [
        {"id": "vaga-e2e-001", "titulo": "Estágio Python Sintético",
         "empresa": "Empresa Sintética", "descricao": "Atividades sintéticas de teste.",
         "requisitos": ["Python", "Git"], "localizacao": "Cidade Sintética",
         "modalidade": "REMOTO", "url_candidatura": "https://vagas.invalid/001"},
        {"id": "vaga-e2e-002", "titulo": "QA Sintético",
         "empresa": "Empresa Sintética", "descricao": "Atividades sintéticas de teste.",
         "requisitos": [], "localizacao": None, "modalidade": "REMOTO",
         "url_candidatura": None},
    ]


def bytes_resultado() -> bytes:
    """Serializa a massa externa em JSON UTF-8 para exercitar o mapper real.

    Codifica uma lista nova de vagas sintéticas, sem normalizar previamente,
    para que o teste observe a conversão feita pelo adapter de produção.
    """
    return dumps(vagas_sinteticas(), ensure_ascii=False).encode("utf-8")


@dataclass(frozen=True)
class ChamadaTransporte:
    """Preserva URL, timeout e ordem como registro imutável de cada consulta.

    Usa dataclass congelada com valores escalares para permitir espionagem
    sem expor referências mutáveis que falsifiquem a passagem pelo adapter.
    """

    url: str
    timeout: float
    ordem: int


class TransporteVagasRegistrado:
    """Simula apenas I/O externo, consumindo bytes ou exceções em uma fila.

    Registra cada invocação antes de responder, sem espera ou socket, para
    provar parâmetros e recuperação através do caso de uso e adapter reais.
    """

    def __init__(self, *respostas: bytes | Exception) -> None:
        """Inicializa fila e histórico vazios ou previamente configurados.

        Copia os argumentos em deque e separa os registros para garantir
        que cada instância represente um único cenário independente.
        """
        self._fila = deque(respostas)
        self._chamadas: list[ChamadaTransporte] = []

    @property
    def chamadas(self) -> tuple[ChamadaTransporte, ...]:
        """Expõe o histórico como tupla de registros congelados para asserções.

        Copia a coleção sem permitir edição dos elementos, mantendo evidência
        independente da fila para provar a ordem e os parâmetros recebidos.
        """
        return tuple(self._chamadas)

    def enfileirar(self, *respostas: bytes | Exception) -> None:
        """Acrescenta respostas em ordem para controlar buscas e recusas.

        Estende a fila local sem alterar registros anteriores, permitindo
        preparar recuperação determinística sem modificar o produto.
        """
        self._fila.extend(respostas)

    def __call__(self, url: str, timeout: float) -> bytes:
        """Registra a consulta e devolve bytes ou lança a próxima falha prevista.

        Consome exatamente uma posição sem sleep; fila esgotada é erro de
        preparação, impedindo sucesso fabricado para chamadas inesperadas.
        """
        self._chamadas.append(ChamadaTransporte(url, timeout, len(self._chamadas) + 1))
        if not self._fila:
            raise AssertionError("Transporte de vagas recebeu chamada sem resposta prevista.")
        resposta = self._fila.popleft()
        if isinstance(resposta, Exception):
            raise resposta
        return resposta


class AutenticadorVagasFake(AutenticadorSessao):
    """Fornece identidade sintética somente ao token aceito e registra consultas.

    Substitui a porta de identidade sem banco ou state manual, permitindo
    verificar o middleware real sem alegar login ou sessão persistidos.
    """

    def __init__(self) -> None:
        """Reserva um histórico por instância para isolar a prova de autenticação.

        Inicia lista local sem credenciais reais para distinguir ausência de
        cookie de token rejeitado por consulta efetiva à porta.
        """
        self.consultas: list[str] = []

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Registra o token sintético e aceita somente o valor previsto.

        Retorna UUID fixo ou None para exercitar a decisão do middleware,
        sem reproduzir expiração, hash ou persistência de sessões reais.
        """
        self.consultas.append(token)
        return UsuarioId(UUID(int=101)) if token == TOKEN_ACEITO else None


def criar_app_busca_vagas(
    transporte: TransporteVagasRegistrado, autenticador: AutenticadorVagasFake,
) -> FastAPI:
    """Compõe ASGI com middleware, caso de uso e adapter HTTP de produção.

    Injeta apenas autenticador sintético e executor HTTP registrado na factory,
    permitindo provar a cadeia de busca sem importar main ou conectar rede.
    """
    return create_app(
        autenticador_sessao=autenticador,
        consultar_vagas=ConsultarVagas(ClienteApiVagasGrupo2Http(
            url_base=URL_PROVEDOR, executor_http=transporte,
        )),
    )


class PortaVagasCanonicaFake:
    """Alterna DTOs e erro canônico para a exceção base não criada pelo HTTP.

    Registra cópias dos critérios e devolve uma massa fixa ou levanta a falha,
    para testar A06 sem alegar cobertura do adapter HTTP nesse cenário.
    """

    def __init__(self) -> None:
        """Prepara modo saudável e histórico local para controle causal.

        Mantém falha opcional separada dos registros para alternar sucesso,
        erro e recuperação na mesma rota sem usar o double compartilhado.
        """
        self.erro: ErroIntegracaoVagas | None = None
        self.chamadas: list[tuple[str, dict[str, Any]]] = []

    async def buscar_vagas(
        self, termo: str = "", filtros: dict[str, Any] | None = None,
    ) -> list[VagaExternaDto]:
        """Registra os critérios e responde com DTO ou exceção canônica prevista.

        Copia filtros antes de decidir a falha para provar propagação e
        recuperação da camada de aplicação sem simular transporte HTTP.
        """
        self.chamadas.append((termo, dict(filtros or {})))
        if self.erro is not None:
            raise self.erro
        return [
            VagaExternaDto(
                id=vaga["id"], titulo=vaga["titulo"], empresa=vaga["empresa"],
                descricao=vaga["descricao"], requisitos=tuple(vaga["requisitos"]),
                localizacao=vaga["localizacao"] or "", modalidade=vaga["modalidade"],
                url_candidatura=vaga["url_candidatura"] or "",
            )
            for vaga in vagas_sinteticas()
        ]
