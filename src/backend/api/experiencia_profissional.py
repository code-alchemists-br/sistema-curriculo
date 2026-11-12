"""Expõe cadastro, leitura, edição e exclusão de experiências por HTTP autenticado."""

from datetime import date
from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator

# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
from backend.api.rota_gravacao_experiencia import (
    ErroGravacaoExperienciaResposta,
    RotaGravacaoExperiencia,
)
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

# Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
from backend.application.perfil_estudante import ListarExperienciasProfissionaisEntrada
from backend.domain import ExperienciaProfissional, Periodo, RegraDeDominioViolada

# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
from backend.domain.itens_perfil import (
    TAMANHO_MAXIMO_CARGO_EXPERIENCIA,
    TAMANHO_MAXIMO_DESCRICAO_EXPERIENCIA,
    TAMANHO_MAXIMO_EMPRESA_EXPERIENCIA,
    TAMANHO_MINIMO_TEXTO_EXPERIENCIA,
)
from backend.domain.value_objects import ExperienciaProfissionalId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
class CadastroExperienciaProfissionalRequisicao(BaseModel):
    """Representa os campos de transporte necessários para criar experiência.

    Pydantic exige strings estritas, normaliza com strip antes dos limites e
    valida o formato das datas. A Application aplica a regra temporal com
    relógio injetado. O DTO existe para separar JSON do contrato interno sem
    permitir que o cliente escolha dono, hoje ou o fuso da validação.
    """

    empresa: str = Field(strict=True, min_length=TAMANHO_MINIMO_TEXTO_EXPERIENCIA,
                         max_length=TAMANHO_MAXIMO_EMPRESA_EXPERIENCIA)
    cargo: str = Field(strict=True, min_length=TAMANHO_MINIMO_TEXTO_EXPERIENCIA,
                       max_length=TAMANHO_MAXIMO_CARGO_EXPERIENCIA)
    descricao: str = Field(strict=True, min_length=TAMANHO_MINIMO_TEXTO_EXPERIENCIA,
                           max_length=TAMANHO_MAXIMO_DESCRICAO_EXPERIENCIA)
    data_inicio: date = Field(description=(
        "Início da experiência, não posterior ao dia atual em America/Sao_Paulo. "
        "A validação usa o relógio do servidor a cada gravação."
    ))
    data_fim: date | None = Field(default=None, description=(
        "Término da experiência, não posterior ao dia atual em America/Sao_Paulo. "
        "Null indica experiência em andamento; pode ser omitido no cadastro."
    ))

    @field_validator("empresa", "cargo", "descricao", mode="before")
    @classmethod
    def normalizar_texto(cls, valor: object) -> str:
        """Exige texto e aplica strip antes da validação declarativa de tamanho.

        Rejeita conversões de outros tipos e preserva Unicode, espaços e linhas
        internas para medir os limites do domínio sem truncar o dado recebido.
        """
        if not isinstance(valor, str):
            raise ValueError("O campo deve ser texto.")
        return valor.strip()


# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
class EdicaoExperienciaProfissionalRequisicao(CadastroExperienciaProfissionalRequisicao):
    """Define o corpo completo aceito para editar uma experiência profissional.

    O DTO herda os campos do cadastro e torna ``data_fim`` obrigatória, embora
    anulável: ``null`` indica experiência em andamento. Ele existe para impedir
    que uma substituição incompleta apague o término sem intenção do estudante.
    """

    data_fim: date | None = Field(
        description=(
            "Término não posterior ao dia atual em America/Sao_Paulo, validado "
            "a cada gravação pelo relógio do servidor. Campo obrigatório na "
            "edição; envie null para experiência em andamento."
        )
    )


# Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
class ExperienciaProfissionalResposta(BaseModel):
    """Representa dados públicos de cadastro, edição e leitura da experiência.

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


# Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
class ListagemExperienciasProfissionaisResposta(BaseModel):
    """Apresenta a coleção própria usando o DTO público existente por item.

    Agrupa os itens em experiencias, inclusive vazia, para transportar a ordem
    recebida sem expor entidades ou marcadores internos de exclusão.
    """

    experiencias: list[ExperienciaProfissionalResposta]


# Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
class ListagemExperienciasProfissionaisExecutor(Protocol):
    """Define a consulta tipada de experiências consumida pela fronteira HTTP.

    Recebe o dono resolvido pela fronteira e retorna a coleção já ordenada para
    permitir injeção da leitura sem expor persistência ao handler.
    """

    async def executar(
        self, entrada: ListarExperienciasProfissionaisEntrada
    ) -> tuple[ExperienciaProfissional, ...]:
        """Consulta as ativas do dono e devolve a ordem pronta para apresentação.

        A implementação delega consulta e ordem à Application para permitir que
        o handler apenas converta as entidades em respostas públicas.
        """


# Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
def _resposta(experiencia: ExperienciaProfissional) -> ExperienciaProfissionalResposta:
    """Projeta a entidade nos campos públicos da resposta HTTP.

    A função extrai UUIDs, textos e datas do período sem serializar a entidade.
    Ela existe para que cadastro, edição e leitura usem o mesmo contrato.
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
    # Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
    listar_experiencias: ListagemExperienciasProfissionaisExecutor | None = None,
) -> APIRouter:
    """Cria as rotas POST, GET, PUT e DELETE protegidas por sessão.

    As rotas recebem o principal que o middleware autenticador instalou em
    ``request.state``, convertem rota e corpo em entrada de Application e
    invocam o executor injetado; edição e exclusão convertem ausência ou
    propriedade alheia em 404, e a edição converte violações de domínio em 422
    com mensagem genérica. A função existe para impedir que o cliente escolha o
    dono da experiência, sem acoplar a API à persistência ou à sessão concreta.
    """
    # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
    router = APIRouter(route_class=RotaGravacaoExperiencia)

    # Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
    @router.get(
        "/experiencias-profissionais",
        response_model=ListagemExperienciasProfissionaisResposta,
        status_code=status.HTTP_200_OK,
        summary="Listar experiências profissionais do estudante autenticado",
        description=(
            "Requer cookie de sessão válido e lista somente experiências ativas "
            "do estudante autenticado, sem corpo, parâmetros ou paginação. "
            "Preserva a ordem do domínio: início decrescente; no empate de "
            "início, término nulo primeiro, depois término decrescente e ID. "
            "data_fim nulo significa experiência em andamento. Coleção vazia "
            "retorna 200 com experiencias vazia."
        ),
        responses={
            200: {"description": "Coleção própria ordenada, inclusive vazia."},
            401: {"description": "Sessão ausente ou inválida."},
            503: {"description": "Listagem indisponível."},
        },
    )
    async def listar(request: Request) -> ListagemExperienciasProfissionaisResposta:
        """Apresenta a coleção ativa do dono obtido exclusivamente da sessão.

        Reutiliza a resolução de identidade existente, monta a entrada interna
        e projeta a sequência recebida por _resposta sem reordenar para expor
        somente os campos públicos e impedir escolha do dono pelo cliente.
        """
        if listar_experiencias is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Listagem indisponível.",
            )
        usuario_id = _usuario_autenticado(request)
        experiencias = await listar_experiencias.executar(
            ListarExperienciasProfissionaisEntrada(usuario_id=UsuarioId(usuario_id))
        )
        return ListagemExperienciasProfissionaisResposta(
            experiencias=[_resposta(experiencia) for experiencia in experiencias]
        )

    @router.post(
        "/experiencias-profissionais",
        response_model=ExperienciaProfissionalResposta,
        status_code=status.HTTP_201_CREATED,
        # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
        responses={422: {"model": ErroGravacaoExperienciaResposta,
                         "description": "Dados inválidos; mensagem sem refletir o conteúdo recebido."}},
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
        except RegraDeDominioViolada:
            raise HTTPException(
                # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="A experiência informada viola as regras de cadastro.",
            ) from None
        return _resposta(experiencia)

    @router.put(
        "/experiencias-profissionais/{experiencia_id}",
        response_model=ExperienciaProfissionalResposta,
        # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
        responses={422: {"model": ErroGravacaoExperienciaResposta,
                         "description": "Dados inválidos; mensagem sem refletir o conteúdo recebido."}},
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
        # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
        except RegraDeDominioViolada:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="A experiência informada viola as regras de edição.",
            ) from None
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
