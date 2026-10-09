"""Expõe DTOs e o handler HTTP da listagem de versões de currículo.

O módulo converte a identidade de rota em entrada da Application e traduz as
versões devolvidas em DTOs públicos, sem expor entidades de domínio nem as
referências aos itens. Ele existe para manter transporte e apresentação de dados
fora das regras de domínio e do caso de uso de listagem.
"""

# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.application import ListarVersoesCurriculoEntrada
from backend.domain import Curriculo, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
class ListagemVersoesCurriculoExecutor(Protocol):
    """Define a capacidade de listar versões de currículo que o router invoca.

    O contrato recebe a entrada da Application e devolve as versões do estudante
    já filtradas e ordenadas, sem acoplar o handler a banco ou implementação
    concreta. Ele existe para tornar a interface HTTP testável com doubles que
    exercitam a mesma intenção do caso de uso real.
    """

    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    async def executar(self, entrada: ListarVersoesCurriculoEntrada) -> tuple[Curriculo, ...]:
        """Executa a listagem interna e devolve as versões em ordem determinística.

        Implementações aplicam as regras de propriedade e de ordem sem definir
        respostas HTTP. O método existe para que o router se concentre em
        traduzir fronteiras.
        """


# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
class VersaoCurriculoResumoResposta(BaseModel):
    """Representa o resumo público de uma versão de currículo na listagem.

    O DTO expõe identidade, título, layout, visibilidade e a quantidade de itens
    selecionados, sem serializar o agregado, o proprietário nem as referências.
    Ele existe para que o cliente escolha entre versões sem consulta adicional e
    para manter a saída HTTP estável mesmo se o agregado interno evoluir.
    """

    id: UUID
    titulo_versao: str
    layout: str
    is_public: bool
    total_itens: int


# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
class ListagemVersoesCurriculoResposta(BaseModel):
    """Representa a listagem das versões de currículo de um estudante.

    O DTO reúne os resumos em um objeto, e não em uma lista solta, para que
    paginação ou totais possam ser acrescentados depois sem quebrar clientes.
    Ele existe para devolver ao cliente todas as versões do estudante em uma
    única resposta.
    """

    versoes: list[VersaoCurriculoResumoResposta]


# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
def criar_router(listar_versoes: ListagemVersoesCurriculoExecutor | None) -> APIRouter:
    """Cria a rota HTTP de listagem usando o caso de uso injetado.

    A função converte a identidade de rota em entrada da Application e monta a
    resposta pública a partir das versões devolvidas. Ela existe para registrar a
    API e permitir testes unitários com doubles, sem sessão de banco real.

    Nota: a identidade do solicitante ainda é recebida pela própria rota
    (``usuario_id`` no caminho), e não derivada de uma sessão autenticada;
    autenticação e autorização de entrada permanecem um handoff pendente,
    conforme prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md.
    """
    router = APIRouter()

    @router.get(
        "/estudantes/{usuario_id}/curriculos",
        response_model=ListagemVersoesCurriculoResposta,
    )
    async def listar(usuario_id: UUID) -> ListagemVersoesCurriculoResposta:
        """Executa a listagem HTTP e devolve o resumo público das versões.

        O handler monta a entrada da Application a partir da rota, aguarda o caso
        de uso e converte cada versão em resumo, preservando a ordem recebida.
        Estudante sem versões resulta em lista vazia, e não em erro. Ele existe
        para expor a consulta sem levar HTTP à Application.
        """
        if listar_versoes is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Listagem indisponível.")
        curriculos = await listar_versoes.executar(ListarVersoesCurriculoEntrada(usuario_id=UsuarioId(usuario_id)))
        return ListagemVersoesCurriculoResposta(
            versoes=[
                VersaoCurriculoResumoResposta(
                    id=curriculo.id.valor,
                    titulo_versao=curriculo.titulo_versao,
                    layout=curriculo.layout,
                    is_public=curriculo.is_public,
                    total_itens=len(curriculo.referencias),
                )
                for curriculo in curriculos
            ]
        )

    return router
