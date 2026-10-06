"""Expõe DTOs e handlers HTTP para criação e edição de versão de currículo.

O módulo converte JSON e identidades de rota em tipos da Application e traduz
falhas conhecidas em respostas HTTP sem expor entidades de domínio. Ele existe
para manter transporte e segurança fora das regras de domínio e dos casos de
uso de criação e edição de versão de currículo.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from backend.application import (
    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    CriarVersaoCurriculoEntrada,
    CurriculoNaoEncontrado,
    EditarVersaoCurriculoEntrada,
)
from backend.domain import Curriculo, CurriculoId, RegraDeDominioViolada, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001


class EdicaoVersaoCurriculoExecutor(Protocol):
    """Define a capacidade de editar versão de currículo que o router invoca.

    O contrato recebe a entrada da Application e devolve o agregado com o novo
    estado, sem acoplar o handler a banco ou implementação concreta. Ele existe
    para tornar a interface HTTP testável com doubles que exercitam a mesma
    intenção do caso de uso real.
    """

    async def executar(self, entrada: EditarVersaoCurriculoEntrada) -> Curriculo:
        """Executa a edição interna e devolve o agregado atualizado.

        Implementações aplicam regras de currículo sem definir respostas HTTP. O
        método existe para que o router se concentre em traduzir fronteiras.
        """


class EditarVersaoCurriculoRequisicao(BaseModel):
    """Representa o JSON aceito para editar uma versão de currículo.

    O DTO limita presença e tamanho na fronteira antes da conversão ao caso de
    uso e não aceita identidade, proprietário nem referências, que permanecem
    fora deste contrato. Ele existe para separar transporte do núcleo de edição
    de versão.
    """

    titulo_versao: str = Field(min_length=1, max_length=200)
    layout: str = Field(min_length=1, max_length=100)
    is_public: bool


class VersaoCurriculoResposta(BaseModel):
    """Representa os dados públicos devolvidos após editar uma versão.

    O DTO extrai identidade, título, layout e visibilidade sem serializar o
    agregado de domínio nem suas referências. Ele existe para manter a saída
    HTTP estável mesmo se o agregado interno evoluir.
    """

    id: UUID
    titulo_versao: str
    layout: str
    is_public: bool


# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
class CriacaoVersaoCurriculoExecutor(Protocol):
    """Define a capacidade de criar versão de currículo que o router invoca.

    O contrato recebe a entrada da Application e devolve o agregado criado, sem
    acoplar o handler a banco ou implementação concreta. Ele existe para tornar
    a interface HTTP testável com doubles que exercitam a mesma intenção do caso
    de uso real.
    """

    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    async def executar(self, entrada: CriarVersaoCurriculoEntrada) -> Curriculo:
        """Executa a criação interna e devolve o agregado salvo.

        Implementações aplicam regras de currículo sem definir respostas HTTP. O
        método existe para que o router se concentre em traduzir fronteiras.
        """


# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
class CriarVersaoCurriculoRequisicao(BaseModel):
    """Representa o JSON aceito para criar uma versão de currículo.

    O DTO limita presença e tamanho na fronteira antes da conversão ao caso de
    uso, torna a visibilidade opcional com padrão privado e não aceita
    identidade, proprietário nem referências. Ele existe para separar transporte
    do núcleo de criação de versão.
    """

    titulo_versao: str = Field(min_length=1, max_length=200)
    layout: str = Field(min_length=1, max_length=100)
    is_public: bool = False


def criar_router(
    editar_versao_curriculo: EdicaoVersaoCurriculoExecutor | None,
    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    criar_versao_curriculo: CriacaoVersaoCurriculoExecutor | None = None,
) -> APIRouter:
    """Cria as rotas HTTP de edição e criação de versão com os casos de uso injetados.

    A função converte identidades de rota e JSON em entradas da Application e
    traduz exceções conhecidas em status seguros. Ela existe para registrar a
    API e permitir testes unitários com doubles, sem sessão de banco real.

    Nota: a identidade do solicitante ainda é recebida pela própria rota
    (``usuario_id`` no caminho), e não derivada de uma sessão autenticada. Na
    edição, a verificação de propriedade protege contra acesso cruzado
    acidental, mas não contra um cliente que conheça os dois identificadores. Na
    criação, o proprietário da nova versão é o ``usuario_id`` do caminho e sua
    existência não é verificada pelo caso de uso (a integridade fica a cargo da
    chave estrangeira). Autenticação e autorização de entrada permanecem um
    handoff pendente, conforme
    prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md e
    prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md.
    """
    router = APIRouter()

    @router.put(
        "/estudantes/{usuario_id}/curriculos/{curriculo_id}",
        response_model=VersaoCurriculoResposta,
    )
    async def editar(
        usuario_id: UUID,
        curriculo_id: UUID,
        requisicao: EditarVersaoCurriculoRequisicao,
    ) -> VersaoCurriculoResposta:
        """Executa a edição HTTP e devolve os dados públicos da versão atualizada.

        O handler cria as identidades tipadas, aguarda o caso de uso e traduz
        ausência, propriedade alheia e violação de domínio sem expor detalhes
        internos. Ele existe para expor a edição sem levar HTTP à Application.
        """
        if editar_versao_curriculo is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Edição indisponível.")
        entrada = EditarVersaoCurriculoEntrada(
            usuario_id=UsuarioId(usuario_id),
            curriculo_id=CurriculoId(curriculo_id),
            titulo_versao=requisicao.titulo_versao,
            layout=requisicao.layout,
            is_public=requisicao.is_public,
        )
        try:
            curriculo = await editar_versao_curriculo.executar(entrada)
        except CurriculoNaoEncontrado as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro
        return VersaoCurriculoResposta(
            id=curriculo.id.valor,
            titulo_versao=curriculo.titulo_versao,
            layout=curriculo.layout,
            is_public=curriculo.is_public,
        )

    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    @router.post(
        "/estudantes/{usuario_id}/curriculos",
        response_model=VersaoCurriculoResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def criar(usuario_id: UUID, requisicao: CriarVersaoCurriculoRequisicao) -> VersaoCurriculoResposta:
        """Executa a criação HTTP e devolve os dados públicos da versão criada.

        O handler monta a entrada da Application a partir da rota e do corpo,
        aguarda o caso de uso e traduz violação de domínio sem expor detalhes
        internos. Ele existe para expor a criação sem levar HTTP à Application.
        """
        if criar_versao_curriculo is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Criação indisponível.")
        entrada = CriarVersaoCurriculoEntrada(
            usuario_id=UsuarioId(usuario_id),
            titulo_versao=requisicao.titulo_versao,
            layout=requisicao.layout,
            is_public=requisicao.is_public,
        )
        try:
            curriculo = await criar_versao_curriculo.executar(entrada)
        except RegraDeDominioViolada as erro:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro
        return VersaoCurriculoResposta(
            id=curriculo.id.valor,
            titulo_versao=curriculo.titulo_versao,
            layout=curriculo.layout,
            is_public=curriculo.is_public,
        )

    return router
