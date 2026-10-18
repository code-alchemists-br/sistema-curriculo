"""Expõe cadastro, edição e exclusão autenticados de formações acadêmicas.

O módulo traduz DTOs e identidades da sessão para os casos de uso, e apresenta
um DTO público explícito para operações com resposta. Ele existe para expor
essas capacidades sem permitir que o cliente escolha o proprietário.
"""

from datetime import date
from typing import Protocol
from unicodedata import category
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator

from backend.application.perfil_estudante import (
    CadastrarFormacaoAcademicaEntrada,
    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    EditarFormacaoAcademicaEntrada,
    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    ExcluirFormacaoAcademicaEntrada,
    FormacaoAcademicaNaoEncontrada,
)
from backend.domain import (
    TAMANHO_MAXIMO_TEXTO_FORMACAO,
    TAMANHO_MINIMO_TEXTO_FORMACAO,
    FormacaoAcademica,
    NivelFormacaoAcademica,
    Periodo,
    RegraDeDominioViolada,
    StatusFormacaoAcademica,
)
from backend.domain.value_objects import FormacaoAcademicaId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
class CadastroFormacaoAcademicaRequisicao(BaseModel):
    """Define o corpo HTTP aceito para criar uma formação acadêmica.

    O DTO tipa os enums, normaliza textos e rejeita controles antes da chamada
    interna; `data_fim` é previsão em andamento e data efetiva nos demais
    status. Ele existe para validar o contrato JSON e manter o proprietário
    fora dos campos controlados pelo cliente.
    """

    instituicao: str
    curso: str
    nivel: NivelFormacaoAcademica
    data_inicio: date
    data_fim: date | None = Field(
        default=None,
        description=(
            "Previsão de conclusão quando status for em_andamento; data efetiva "
            "de conclusão ou interrupção nos demais status."
        ),
    )
    status: StatusFormacaoAcademica

    @field_validator("instituicao", "curso", mode="before")
    @classmethod
    def validar_texto_formacao(cls, valor: object) -> str:
        """Normaliza e valida o conteúdo textual recebido pela API.

        A validação exige string, rejeita controles, aplica `strip` uma vez e
        mede o texto normalizado pelos limites públicos do Domain. Ela existe
        para rejeitar payloads inválidos antes da conversão para Application.
        """
        if not isinstance(valor, str):
            raise ValueError("O campo deve ser texto.")
        if any(category(caractere) == "Cc" for caractere in valor):
            raise ValueError("O campo não pode conter caracteres de controle.")
        normalizado = valor.strip()
        if not TAMANHO_MINIMO_TEXTO_FORMACAO <= len(normalizado) <= TAMANHO_MAXIMO_TEXTO_FORMACAO:
            raise ValueError(
                "O campo deve ter entre "
                f"{TAMANHO_MINIMO_TEXTO_FORMACAO} e "
                f"{TAMANHO_MAXIMO_TEXTO_FORMACAO} caracteres após remover espaços externos."
            )
        return normalizado


# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
class EdicaoFormacaoAcademicaRequisicao(CadastroFormacaoAcademicaRequisicao):
    """Define o corpo completo aceito para editar uma formação acadêmica.

    O DTO herda enums e validação dos textos do cadastro e torna `data_fim`
    obrigatória, embora anulável; `null` limpa a previsão ou data efetiva. Ele
    existe para impedir que uma substituição incompleta apague dados sem
    intenção do estudante.
    """

    data_fim: date | None = Field(
        description=(
            "Previsão de conclusão em em_andamento e data efetiva em concluido "
            "ou interrompido; envie null para limpar o valor."
        )
    )


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
class FormacaoAcademicaResposta(BaseModel):
    """Define os campos públicos devolvidos após cadastrar uma formação.

    O DTO expõe valores primitivos e enums sem serializar a entidade; `data_fim`
    é previsão em andamento e data efetiva nos demais status. Ele existe para
    manter a resposta HTTP explícita e independente da representação interna.
    """

    id: UUID
    usuario_id: UUID
    instituicao: str
    curso: str
    nivel: NivelFormacaoAcademica
    data_inicio: date
    data_fim: date | None = Field(
        description=(
            "Previsão de conclusão quando status for em_andamento; data efetiva "
            "de conclusão ou interrupção nos demais status."
        )
    )
    status: StatusFormacaoAcademica


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
class CadastroFormacaoAcademicaExecutor(Protocol):
    """Define o caso de uso consumido pela rota de cadastro.

    O contrato recebe uma entrada tipada e devolve a entidade persistida sem
    expor repositórios à API. Ele existe para permitir composição externa e
    testes unitários isolados do handler.
    """

    async def executar(
        self, entrada: CadastrarFormacaoAcademicaEntrada
    ) -> FormacaoAcademica:
        """Cadastra uma formação para o proprietário da entrada autenticada.

        A implementação verifica o perfil, constrói a entidade e solicita sua
        persistência. O método existe para separar transporte HTTP da
        orquestração de Application.
        """


# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
class EdicaoFormacaoAcademicaExecutor(Protocol):
    """Define o caso de uso de edição consumido pela rota HTTP.

    O contrato recebe a entrada completa e devolve a entidade editada, sem
    expor o repositório à API. Ele existe para permitir composição externa e
    testes isolados da tradução de transporte.
    """

    async def executar(
        self, entrada: EditarFormacaoAcademicaEntrada
    ) -> FormacaoAcademica:
        """Edita uma formação própria a partir da identidade autenticada.

        A implementação aplica a transição de domínio e persiste pela porta.
        O método existe para manter as regras e a orquestração fora do handler.
        """


# Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
class ExclusaoFormacaoAcademicaExecutor(Protocol):
    """Define o caso de uso de exclusão lógica consumido pela API.

    O contrato recebe o proprietário autenticado e a formação solicitada sem
    expor a persistência ao handler; ele existe para isolar o transporte HTTP.
    """

    async def executar(self, entrada: ExcluirFormacaoAcademicaEntrada) -> FormacaoAcademica:
        """Exclui logicamente uma formação própria e devolve seu estado.

        O caso de uso garante idempotência e propriedade. O método existe para
        que a API delegue a operação sem incorporar regras de negócio.
        """


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
def criar_router(
    cadastrar_formacao: CadastroFormacaoAcademicaExecutor | None,
    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    editar_formacao: EdicaoFormacaoAcademicaExecutor | None = None,
    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    excluir_formacao: ExclusaoFormacaoAcademicaExecutor | None = None,
) -> APIRouter:
    """Cria as rotas protegidas de formação acadêmica.

    Os handlers obtêm o proprietário do estado autenticado, traduzem as
    entradas e convertem falhas conhecidas em respostas HTTP. A função existe
    para expor cadastro, edição e exclusão com contratos públicos explícitos.
    """
    router = APIRouter()

    @router.post(
        "/formacoes-academicas",
        response_model=FormacaoAcademicaResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def cadastrar(
        requisicao: CadastroFormacaoAcademicaRequisicao,
        request: Request,
    ) -> FormacaoAcademicaResposta:
        """Cadastra a formação vinculada à sessão autenticada.

        O endpoint exige executor e UUID autenticado, monta o período e envia
        enums tipados para Application; violações são convertidas em 422 com
        mensagem segura. Ele existe para preservar propriedade e invariantes.
        """
        if cadastrar_formacao is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cadastro indisponível.",
            )
        usuario_id = getattr(request.state, "usuario_id", None)
        if not isinstance(usuario_id, UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária.",
            )
        try:
            entrada = CadastrarFormacaoAcademicaEntrada(
                usuario_id=UsuarioId(usuario_id),
                instituicao=requisicao.instituicao,
                curso=requisicao.curso,
                nivel=requisicao.nivel,
                periodo=Periodo(requisicao.data_inicio, requisicao.data_fim),
                status=requisicao.status,
            )
            formacao = await cadastrar_formacao.executar(entrada)
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="A formação informada viola as regras de cadastro.",
            ) from erro
        return FormacaoAcademicaResposta(
            id=formacao.id.valor,
            usuario_id=formacao.usuario_id.valor,
            instituicao=formacao.instituicao,
            curso=formacao.curso,
            nivel=formacao.nivel,
            data_inicio=formacao.periodo.inicio,
            data_fim=formacao.periodo.fim,
            status=formacao.status,
        )

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    @router.put(
        "/formacoes-academicas/{formacao_id}",
        response_model=FormacaoAcademicaResposta,
    )
    async def editar(
        formacao_id: UUID,
        requisicao: EdicaoFormacaoAcademicaRequisicao,
        request: Request,
    ) -> FormacaoAcademicaResposta:
        """Substitui os dados editáveis de uma formação da sessão atual.

        O handler obtém o proprietário do estado autenticado, cria a entrada
        completa e traduz ausência e violações em respostas estáveis. Ele
        existe para expor a edição sem permitir troca de identidade ou dono.
        """
        if editar_formacao is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Edição indisponível.",
            )
        usuario_id = getattr(request.state, "usuario_id", None)
        if not isinstance(usuario_id, UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária.",
            )
        try:
            entrada = EditarFormacaoAcademicaEntrada(
                usuario_id=UsuarioId(usuario_id),
                formacao_id=FormacaoAcademicaId(formacao_id),
                instituicao=requisicao.instituicao,
                curso=requisicao.curso,
                nivel=requisicao.nivel,
                periodo=Periodo(requisicao.data_inicio, requisicao.data_fim),
                status=requisicao.status,
            )
            formacao = await editar_formacao.executar(entrada)
        except FormacaoAcademicaNaoEncontrada as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Formação acadêmica não encontrada.",
            ) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="A formação informada viola as regras de edição.",
            ) from erro

        return FormacaoAcademicaResposta(
            id=formacao.id.valor,
            usuario_id=formacao.usuario_id.valor,
            instituicao=formacao.instituicao,
            curso=formacao.curso,
            nivel=formacao.nivel,
            data_inicio=formacao.periodo.inicio,
            data_fim=formacao.periodo.fim,
            status=formacao.status,
        )

    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    @router.delete(
        "/formacoes-academicas/{formacao_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def excluir(formacao_id: UUID, request: Request) -> None:
        """Exclui formação do proprietário da sessão e não retorna conteúdo.

        O handler obtém o dono exclusivamente do estado autenticado, delega a
        exclusão e converte ausência uniforme em 404. Ele existe para expor a
        operação idempotente sem aceitar identidade do cliente.
        """
        if excluir_formacao is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Exclusão indisponível.",
            )
        usuario_id = getattr(request.state, "usuario_id", None)
        if not isinstance(usuario_id, UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária.",
            )
        try:
            await excluir_formacao.executar(
                ExcluirFormacaoAcademicaEntrada(
                    usuario_id=UsuarioId(usuario_id),
                    formacao_id=FormacaoAcademicaId(formacao_id),
                )
            )
        except FormacaoAcademicaNaoEncontrada as erro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Formação acadêmica não encontrada.",
            ) from erro

    return router
