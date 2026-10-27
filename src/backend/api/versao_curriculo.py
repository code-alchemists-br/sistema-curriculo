"""Expõe DTOs e handlers HTTP para criação e edição de versão de currículo.

O módulo converte JSON e identidades de rota em tipos da Application e traduz
falhas conhecidas em respostas HTTP sem expor entidades de domínio. Ele existe
para manter transporte e segurança fora das regras de domínio e dos casos de
uso de criação e edição de versão de currículo.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from backend.application import (
    AtualizarOrdemSecoesCurriculoEntrada,
    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    CriarVersaoCurriculoEntrada,
    CurriculoNaoEncontrado,
    EditarVersaoCurriculoEntrada,
)
from backend.domain import (
    Curriculo,
    CurriculoId,
    # Proveniência: decision-analysis prompts/backend/20261017-140000-modelo-curriculo-edicao-versao-v001.md#v001
    ModeloCurriculo,
    RegraDeDominioViolada,
    SecaoCurriculo,
    UsuarioId,
)

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


class AtualizacaoOrdemSecoesCurriculoExecutor(Protocol):
    """Define a capacidade de reordenar seções que o router invoca.

    O contrato recebe a entrada interna e devolve o agregado atualizado sem
    escolher HTTP, banco ou ORM. Ele existe para que a rota tenha uma fronteira
    testável e a intenção de reordenação permaneça independente do transporte.
    """

    async def executar(
        self, entrada: AtualizarOrdemSecoesCurriculoEntrada
    ) -> Curriculo:
        """Atualiza internamente a ordem das seções e devolve a versão.

        Implementações validam e persistem a ordem no núcleo da aplicação, sem
        construir respostas HTTP. O método existe para concentrar no handler só
        a conversão do contrato público para a entrada do caso de uso.
        """


class AtualizarOrdemSecoesCurriculoRequisicao(BaseModel):
    """Representa o payload mínimo para substituir a ordem das seções.

    O DTO aceita exclusivamente a lista ordenada de identificadores de seção e
    usa a enumeração do domínio para rejeitar valores desconhecidos na fronteira.
    Ele existe para reordenar a versão sem exigir nem aceitar seus demais dados.
    """

    model_config = ConfigDict(extra="forbid")

    ordem_secoes: list[SecaoCurriculo] = Field(
        min_length=len(SecaoCurriculo), max_length=len(SecaoCurriculo)
    )


class EditarVersaoCurriculoRequisicao(BaseModel):
    """Representa o JSON aceito para editar uma versão de currículo.

    O DTO limita presença e tamanho na fronteira, restringe o modelo aos valores
    de ``ModeloCurriculo`` (que o OpenAPI passa a listar) e não aceita
    identidade, proprietário nem referências, que permanecem fora deste
    contrato. Ele existe para separar transporte do núcleo de edição de versão e
    recusar um modelo desconhecido já na fronteira.
    """

    titulo_versao: str = Field(min_length=1, max_length=200)
    # Proveniência: decision-analysis prompts/backend/20261017-140000-modelo-curriculo-edicao-versao-v001.md#v001
    layout: ModeloCurriculo
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

    - O que faz: Recebe título, modelo reconhecido e visibilidade da nova versão.
    - Como faz: Usa ``ModeloCurriculo`` na fronteira e converte a enumeração em texto antes do caso de uso.
    - Qual finalidade atende: Garante que criação e edição aceitem o mesmo catálogo, sem bloquear a leitura de versões legadas já gravadas.
    """

    titulo_versao: str = Field(min_length=1, max_length=200)
    layout: ModeloCurriculo
    is_public: bool = False


def criar_router(
    editar_versao_curriculo: EdicaoVersaoCurriculoExecutor | None,
    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    criar_versao_curriculo: CriacaoVersaoCurriculoExecutor | None = None,
    atualizar_ordem_secoes_curriculo: AtualizacaoOrdemSecoesCurriculoExecutor | None = None,
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
        "/estudantes/{usuario_id}/curriculos/{curriculo_id}/ordem-secoes",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def atualizar_ordem_secoes(
        usuario_id: UUID,
        curriculo_id: UUID,
        requisicao: AtualizarOrdemSecoesCurriculoRequisicao,
    ) -> None:
        """Substitui a ordem das seções sem exigir os demais dados da versão.

        O handler converte rota e lista JSON em tipos internos, executa a
        intenção de reordenação e traduz falhas de recurso ou domínio em HTTP.
        Ele existe para publicar o payload mínimo sem expor o agregado.
        """
        if atualizar_ordem_secoes_curriculo is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Atualização da ordem indisponível.",
            )
        entrada = AtualizarOrdemSecoesCurriculoEntrada(
            usuario_id=UsuarioId(usuario_id),
            curriculo_id=CurriculoId(curriculo_id),
            ordem_secoes=tuple(requisicao.ordem_secoes),
        )
        try:
            await atualizar_ordem_secoes_curriculo.executar(entrada)
        except CurriculoNaoEncontrado as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(erro),
            ) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(erro),
            ) from erro

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
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Edição indisponível.",
            )
        entrada = EditarVersaoCurriculoEntrada(
            usuario_id=UsuarioId(usuario_id),
            curriculo_id=CurriculoId(curriculo_id),
            titulo_versao=requisicao.titulo_versao,
            layout=requisicao.layout.value,
            is_public=requisicao.is_public,
        )
        try:
            curriculo = await editar_versao_curriculo.executar(entrada)
        except CurriculoNaoEncontrado as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(erro),
            ) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(erro),
            ) from erro
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
    async def criar(
        usuario_id: UUID,
        requisicao: CriarVersaoCurriculoRequisicao,
    ) -> VersaoCurriculoResposta:
        """Executa a criação HTTP e devolve os dados públicos da versão criada.

        O handler monta a entrada da Application a partir da rota e do corpo,
        aguarda o caso de uso e traduz violação de domínio sem expor detalhes
        internos. Ele existe para expor a criação sem levar HTTP à Application.
        """
        if criar_versao_curriculo is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Criação indisponível.",
            )
        entrada = CriarVersaoCurriculoEntrada(
            usuario_id=UsuarioId(usuario_id),
            titulo_versao=requisicao.titulo_versao,
            layout=requisicao.layout.value,
            is_public=requisicao.is_public,
        )
        try:
            curriculo = await criar_versao_curriculo.executar(entrada)
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(erro),
            ) from erro
        return VersaoCurriculoResposta(
            id=curriculo.id.valor,
            titulo_versao=curriculo.titulo_versao,
            layout=curriculo.layout,
            is_public=curriculo.is_public,
        )

    return router
