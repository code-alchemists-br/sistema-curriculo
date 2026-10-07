"""Expõe DTOs e handlers HTTP para seleção e desseleção de itens da versão de currículo.

O módulo converte JSON, identidades de rota e o texto de tipo do item em tipos da
Application e traduz falhas conhecidas em respostas HTTP sem expor entidades de
domínio. Ele existe para manter transporte e segurança fora das regras de domínio
e dos casos de uso de seleção de itens.
"""

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
from typing import Literal, Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.application import (
    CurriculoNaoEncontrado,
    DesselecionarItemVersaoCurriculoEntrada,
    ItemNaoEncontrado,
    SelecionarItemVersaoCurriculoEntrada,
)
from backend.domain import (
    CompetenciaId,
    Curriculo,
    CurriculoId,
    DocumentoId,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    IdiomaId,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    RegraDeDominioViolada,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
TipoItem = Literal[
    "formacao_academica",
    "experiencia_profissional",
    "projeto_academico",
    "competencia",
    "idioma",
    "documento",
]

_CLASSES_POR_TIPO = {
    "formacao_academica": FormacaoAcademicaId,
    "experiencia_profissional": ExperienciaProfissionalId,
    "projeto_academico": ProjetoAcademicoId,
    "competencia": CompetenciaId,
    "idioma": IdiomaId,
    "documento": DocumentoId,
}
_TIPOS_POR_CLASSE = {classe: tipo for tipo, classe in _CLASSES_POR_TIPO.items()}


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
class SelecaoItemVersaoCurriculoExecutor(Protocol):
    """Define a capacidade de selecionar item que o router invoca.

    O contrato recebe a entrada da Application e devolve o agregado com a seleção
    atualizada, sem acoplar o handler a banco ou implementação concreta. Ele
    existe para tornar a interface HTTP testável com doubles que exercitam a
    mesma intenção do caso de uso real.
    """

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def executar(self, entrada: SelecionarItemVersaoCurriculoEntrada) -> Curriculo:
        """Executa a seleção interna e devolve o agregado atualizado.

        Implementações aplicam regras de currículo sem definir respostas HTTP. O
        método existe para que o router se concentre em traduzir fronteiras.
        """


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
class DesselecaoItemVersaoCurriculoExecutor(Protocol):
    """Define a capacidade de desselecionar item que o router invoca.

    O contrato recebe a entrada da Application e devolve o agregado com a seleção
    atualizada, sem acoplar o handler a banco ou implementação concreta. Ele
    existe para tornar a interface HTTP testável com doubles que exercitam a
    mesma intenção do caso de uso real.
    """

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def executar(self, entrada: DesselecionarItemVersaoCurriculoEntrada) -> Curriculo:
        """Executa a desseleção interna e devolve o agregado atualizado.

        Implementações aplicam regras de currículo sem definir respostas HTTP. O
        método existe para que o router se concentre em traduzir fronteiras.
        """


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
class SelecionarItemRequisicao(BaseModel):
    """Representa o JSON aceito para selecionar um item do perfil na versão.

    O DTO limita o tipo ao vocabulário dos seis itens e exige o identificador do
    item, sem aceitar proprietário nem versão, que vêm da rota. Ele existe para
    separar transporte do núcleo de seleção e validar o formato na fronteira.
    """

    tipo: TipoItem
    item_id: UUID


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
class ItemSelecionadoResposta(BaseModel):
    """Representa um item selecionado na versão, como tipo textual e identificador.

    O DTO expõe somente o par público que identifica o item, sem serializar o
    value object de domínio. Ele existe para manter a saída HTTP estável mesmo se
    a referência interna evoluir.
    """

    tipo: TipoItem
    item_id: UUID


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
class SelecaoVersaoResposta(BaseModel):
    """Representa a seleção atual de itens de uma versão de currículo.

    O DTO devolve a identidade da versão e a lista ordenada de itens selecionados,
    sem expor o agregado nem dados do perfil. Ele existe para que o cliente
    conheça o estado resultante sem uma consulta adicional.
    """

    curriculo_id: UUID
    itens: list[ItemSelecionadoResposta]


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
def _para_referencia(tipo: TipoItem, item_id: UUID) -> ReferenciaCurriculo:
    """Converte o texto de tipo e o UUID do transporte em referência de domínio.

    A função escolhe a classe de identificador pelo tipo textual já validado na
    fronteira e recria a referência tipada. Ela existe para que a Application
    receba somente tipos de domínio, sem conhecer o vocabulário do transporte.
    """
    return ReferenciaCurriculo(_CLASSES_POR_TIPO[tipo](item_id))


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
def _para_resposta(curriculo: Curriculo) -> SelecaoVersaoResposta:
    """Converte a seleção do agregado na resposta pública ordenada.

    A função traduz cada referência no par tipo e UUID e ordena por tipo e
    identificador, para que a resposta seja determinística, sem expor a entidade.
    Ela existe para devolver ao cliente a seleção resultante da operação.
    """
    itens = sorted(
        (
            ItemSelecionadoResposta(
                tipo=_TIPOS_POR_CLASSE[type(referencia.item_id)],
                item_id=referencia.item_id.valor,
            )
            for referencia in curriculo.referencias
        ),
        key=lambda item: (item.tipo, str(item.item_id)),
    )
    return SelecaoVersaoResposta(curriculo_id=curriculo.id.valor, itens=itens)


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
def criar_router(
    selecionar_item: SelecaoItemVersaoCurriculoExecutor | None,
    desselecionar_item: DesselecaoItemVersaoCurriculoExecutor | None,
) -> APIRouter:
    """Cria as rotas HTTP de seleção e desseleção usando os casos de uso injetados.

    A função converte identidades de rota, JSON e o texto de tipo em entradas da
    Application e traduz exceções conhecidas em status seguros. Ela existe para
    registrar a API e permitir testes unitários com doubles, sem sessão de banco.

    Nota: a identidade do solicitante ainda é recebida pela própria rota
    (``usuario_id`` no caminho), e não derivada de uma sessão autenticada, e o
    adapter real de consulta do proprietário dos itens depende das áreas que os
    mantêm; ambos permanecem handoffs pendentes, conforme
    prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md.
    """
    router = APIRouter()

    @router.post(
        "/estudantes/{usuario_id}/curriculos/{curriculo_id}/itens",
        response_model=SelecaoVersaoResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def selecionar(
        usuario_id: UUID,
        curriculo_id: UUID,
        requisicao: SelecionarItemRequisicao,
    ) -> SelecaoVersaoResposta:
        """Executa a seleção HTTP e devolve a seleção atual da versão.

        O handler monta a entrada da Application a partir da rota e do corpo,
        aguarda o caso de uso e traduz ausência de versão ou item e violação de
        domínio sem expor detalhes internos. Ele existe para expor a seleção sem
        levar HTTP à Application.
        """
        if selecionar_item is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Seleção indisponível.")
        entrada = SelecionarItemVersaoCurriculoEntrada(
            usuario_id=UsuarioId(usuario_id),
            curriculo_id=CurriculoId(curriculo_id),
            referencia=_para_referencia(requisicao.tipo, requisicao.item_id),
        )
        try:
            curriculo = await selecionar_item.executar(entrada)
        except (CurriculoNaoEncontrado, ItemNaoEncontrado) as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro
        return _para_resposta(curriculo)

    @router.delete(
        "/estudantes/{usuario_id}/curriculos/{curriculo_id}/itens/{tipo}/{item_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def desselecionar(
        usuario_id: UUID,
        curriculo_id: UUID,
        tipo: TipoItem,
        item_id: UUID,
    ) -> None:
        """Executa a desseleção HTTP sem devolver conteúdo.

        O handler monta a entrada da Application a partir da rota, aguarda o caso
        de uso e traduz ausência de versão e violação de domínio sem expor
        detalhes internos. Ele existe para expor a desseleção sem levar HTTP à
        Application.
        """
        if desselecionar_item is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Desseleção indisponível.")
        entrada = DesselecionarItemVersaoCurriculoEntrada(
            usuario_id=UsuarioId(usuario_id),
            curriculo_id=CurriculoId(curriculo_id),
            referencia=_para_referencia(tipo, item_id),
        )
        try:
            await desselecionar_item.executar(entrada)
        except CurriculoNaoEncontrado as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro

    return router
