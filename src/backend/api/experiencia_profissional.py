"""Expõe cadastro, edição e exclusão de experiências profissionais por HTTP autenticado."""

from datetime import date
from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field

from backend.application.cadastro_experiencia_profissional import (
    CadastrarExperienciaProfissionalEntrada,
)
from backend.application.edicao_experiencia_profissional import (
    EditarExperienciaProfissionalEntrada,
    ExperienciaProfissionalNaoEncontrada,
)
from backend.application.exclusao_experiencia_profissional import (
    ExcluirExperienciaProfissionalEntrada,
)
from backend.domain import ExperienciaProfissional, Periodo, RegraDeDominioViolada
from backend.domain.value_objects import ExperienciaProfissionalId, UsuarioId


class CadastroExperienciaProfissionalRequisicao(BaseModel):
    """Representa os campos de transporte necessários para criar experiência.

    Pydantic valida tipos e datas antes da conversão a value objects; o DTO não
    aceita proprietário ou identificador. Ele existe para separar JSON do
    contrato interno e impedir que o cliente escolha a conta de destino.
    """

    empresa: str
    cargo: str
    descricao: str
    data_inicio: date
    data_fim: date | None = None


class EdicaoExperienciaProfissionalRequisicao(CadastroExperienciaProfissionalRequisicao):
    """Define o corpo completo aceito para editar uma experiência profissional.

    O DTO herda os campos do cadastro e torna ``data_fim`` obrigatória, embora
    anulável: ``null`` indica experiência em andamento. Ele existe para impedir
    que uma substituição incompleta apague o término sem intenção do estudante.
    """

    data_fim: date | None = Field(
        description=(
            "Data de término da experiência; envie null para experiência em andamento."
        )
    )


class ExperienciaProfissionalResposta(BaseModel):
    """Representa dados públicos devolvidos após o cadastro da experiência.

    O DTO extrai UUIDs, textos e datas sem serializar a entidade diretamente.
    Ele existe para manter o contrato HTTP desacoplado do modelo de domínio.
    """

    id: UUID
    usuario_id: UUID
    empresa: str
    cargo: str
    descricao: str
    data_inicio: date
    data_fim: date | None


class CadastroExperienciaProfissionalExecutor(Protocol):
    """Define a execução do cadastro de experiência na fronteira HTTP.

    O contrato recebe uma entrada tipada e devolve a entidade criada sem expor
    persistência à API. Ele existe para permitir injeção do caso de uso e testes
    isolados da rota.
    """

    async def executar(
        self, entrada: CadastrarExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Cadastra uma experiência válida para a identidade autenticada.

        A implementação aplica as regras de domínio e persiste pela porta
        interna apropriada. O método existe para separar o transporte HTTP da
        orquestração do caso de uso.
        """


class EdicaoExperienciaProfissionalExecutor(Protocol):
    """Define a execução da edição de experiência na fronteira HTTP.

    O contrato recebe a entrada tipada com solicitante e experiência e devolve
    a entidade atualizada, sem expor persistência à API. Ele existe para
    permitir injeção do caso de uso e testes isolados da rota de edição.
    """

    async def executar(
        self, entrada: EditarExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Edita uma experiência do solicitante e devolve o novo estado.

        A implementação valida o proprietário, aplica as regras de domínio e
        persiste pela porta interna. O método existe para que o handler apenas
        traduza transporte e erros.
        """


class ExclusaoExperienciaProfissionalExecutor(Protocol):
    """Define a execução da exclusão lógica de experiência na fronteira HTTP.

    O contrato recebe a entrada tipada com solicitante e experiência e devolve
    a entidade no estado excluído, sem expor persistência ou relógio à API. Ele
    existe para permitir injeção do caso de uso e testes isolados da rota.
    """

    async def executar(
        self, entrada: ExcluirExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Exclui logicamente uma experiência do solicitante e devolve seu estado.

        A implementação valida o proprietário e garante idempotência. O método
        existe para que o handler apenas traduza transporte e erros.
        """


def _resposta(experiencia: ExperienciaProfissional) -> ExperienciaProfissionalResposta:
    """Projeta a entidade nos campos públicos da resposta HTTP.

    A função extrai UUIDs, textos e datas do período sem serializar a entidade.
    Ela existe para que cadastro e edição devolvam exatamente o mesmo contrato.
    """
    return ExperienciaProfissionalResposta(
        id=experiencia.id.valor,
        usuario_id=experiencia.usuario_id.valor,
        empresa=experiencia.empresa,
        cargo=experiencia.cargo,
        descricao=experiencia.descricao,
        data_inicio=experiencia.periodo.inicio,
        data_fim=experiencia.periodo.fim,
    )


def _usuario_autenticado(request: Request) -> UUID:
    """Obtém o UUID instalado pelo middleware de sessão ou responde 401.

    A função lê somente ``request.state.usuario_id`` e rejeita valores ausentes
    ou de outro tipo. Ela existe para que nenhuma rota de experiência use
    identidade fornecida pelo cliente.
    """
    usuario_id = getattr(request.state, "usuario_id", None)
    if not isinstance(usuario_id, UUID):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária.",
        )
    return usuario_id


def criar_router(
    cadastrar_experiencia: CadastroExperienciaProfissionalExecutor | None,
    editar_experiencia: EdicaoExperienciaProfissionalExecutor | None = None,
    excluir_experiencia: ExclusaoExperienciaProfissionalExecutor | None = None,
) -> APIRouter:
    """Cria as rotas POST, PUT e DELETE de experiência protegidas por sessão.

    As rotas recebem o principal que o middleware autenticador instalou em
    ``request.state``, convertem rota e corpo em entrada de Application e
    invocam o executor injetado; edição e exclusão convertem ausência ou
    propriedade alheia em 404, e a edição converte violações de domínio em 422
    com mensagem genérica. A função existe para impedir que o cliente escolha o
    dono da experiência, sem acoplar a API à persistência ou à sessão concreta.
    """
    router = APIRouter()

    @router.post(
        "/experiencias-profissionais",
        response_model=ExperienciaProfissionalResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def cadastrar(
        requisicao: CadastroExperienciaProfissionalRequisicao,
        request: Request,
    ) -> ExperienciaProfissionalResposta:
        """Cadastra a experiência vinculada à identidade autenticada da requisição.

        O handler exige um executor e um ``UsuarioId`` instalado pelo middleware,
        constrói ``Periodo`` e encaminha a entrada tipada ao caso de uso. Ele
        existe para proteger a propriedade do dado e traduzir falhas de domínio
        em respostas HTTP estáveis.
        """
        if cadastrar_experiencia is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cadastro indisponível.",
            )
        usuario_id = _usuario_autenticado(request)
        try:
            entrada = CadastrarExperienciaProfissionalEntrada(
                usuario_id=UsuarioId(usuario_id),
                empresa=requisicao.empresa,
                cargo=requisicao.cargo,
                descricao=requisicao.descricao,
                periodo=Periodo(requisicao.data_inicio, requisicao.data_fim),
            )
            experiencia = await cadastrar_experiencia.executar(entrada)
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)
            ) from erro
        return _resposta(experiencia)

    @router.put(
        "/experiencias-profissionais/{experiencia_id}",
        response_model=ExperienciaProfissionalResposta,
    )
    async def editar(
        experiencia_id: UUID,
        requisicao: EdicaoExperienciaProfissionalRequisicao,
        request: Request,
    ) -> ExperienciaProfissionalResposta:
        """Substitui os dados editáveis de uma experiência da sessão atual.

        O handler exige executor e principal autenticado, cria a entrada
        completa com o ID da rota e o dono da sessão e traduz ausência ou
        propriedade alheia em 404 e violações de domínio em 422, ambos com
        mensagens genéricas. Ele existe para expor a edição sem permitir troca
        de identidade ou dono nem revelar detalhes internos das regras.
        """
        if editar_experiencia is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Edição indisponível.",
            )
        usuario_id = _usuario_autenticado(request)
        try:
            entrada = EditarExperienciaProfissionalEntrada(
                usuario_id=UsuarioId(usuario_id),
                experiencia_id=ExperienciaProfissionalId(experiencia_id),
                empresa=requisicao.empresa,
                cargo=requisicao.cargo,
                descricao=requisicao.descricao,
                periodo=Periodo(requisicao.data_inicio, requisicao.data_fim),
            )
            experiencia = await editar_experiencia.executar(entrada)
        except ExperienciaProfissionalNaoEncontrada as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experiência profissional não encontrada.",
            ) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="A experiência informada viola as regras de edição.",
            ) from erro
        return _resposta(experiencia)

    @router.delete(
        "/experiencias-profissionais/{experiencia_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def excluir(experiencia_id: UUID, request: Request) -> None:
        """Exclui logicamente uma experiência da sessão atual sem devolver corpo.

        O handler exige executor e principal autenticado, delega a exclusão com
        o ID da rota e o dono da sessão e converte ausência ou propriedade
        alheia em 404 genérico; repetir a exclusão também responde 204. Ele
        existe para expor a operação idempotente sem aceitar identidade do
        cliente nem revelar experiências de terceiros.
        """
        if excluir_experiencia is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Exclusão indisponível.",
            )
        usuario_id = _usuario_autenticado(request)
        try:
            await excluir_experiencia.executar(
                ExcluirExperienciaProfissionalEntrada(
                    usuario_id=UsuarioId(usuario_id),
                    experiencia_id=ExperienciaProfissionalId(experiencia_id),
                )
            )
        except ExperienciaProfissionalNaoEncontrada as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experiência profissional não encontrada.",
            ) from erro

    return router
