"""Expõe cadastro, sugestão, detalhe, edição e exclusão de projetos por HTTP.

O módulo valida o JSON por DTO, obtém o proprietário da sessão e converte a
entidade em resposta explícita; também oferece a sugestão de descrição do
assistente, traduzindo sua indisponibilidade em falha controlada. Ele existe
para oferecer o cadastro e a orientação do RF04 sem expor o domínio nem aceitar
a identidade do proprietário pelo cliente. As operações por ID delegam aos
casos existentes, com tradução de ausência uniforme e exclusão sem conteúdo.
"""

# Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
from __future__ import annotations

from json import JSONDecodeError
from typing import Protocol
from unicodedata import category
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    ValidationInfo,
    field_validator,
)

# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
from backend.application import (
    AssistenteDescricaoProjeto,
    AssistenteDescricaoProjetoEntrada,
    AssistenteDescricaoProjetoIndisponivel,
    CadastrarProjetoAcademicoEntrada,
    # Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
    ConsultarProjetoAcademicoEntrada,
    EditarProjetoAcademicoEntrada,
    ExcluirProjetoAcademicoEntrada,
    ProjetoAcademicoNaoEncontrado,
)
from backend.domain import (
    TAMANHO_MAXIMO_DESCRICAO_PROJETO,
    TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO,
    TAMANHO_MAXIMO_TITULO_PROJETO,
    TAMANHO_MINIMO_TEXTO_PROJETO,
    ProjetoAcademico,
    ProjetoAcademicoId,
    RegraDeDominioViolada,
    UsuarioId,
)


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class CadastroProjetoAcademicoExecutor(Protocol):
    """Define a capacidade interna de cadastrar projeto acadêmico.

    O contrato recebe entrada tipada e devolve a entidade criada, sem expor
    repositório ou detalhes de armazenamento. Ele existe para manter o handler
    independente da implementação do caso de uso.
    """

    async def executar(
        self, entrada: CadastrarProjetoAcademicoEntrada
    ) -> ProjetoAcademico:
        """Executa o cadastro e devolve o projeto persistido.

        A implementação aplica invariantes do Domain e persiste pela porta
        correspondente. O método existe para separar HTTP da Application.
        """


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class CadastroProjetoAcademicoRequisicao(BaseModel):
    """Representa os três textos aceitos no corpo do cadastro.

    O DTO ignora campos desconhecidos e verifica tipo e comprimento normalizado
    usando limites do Domain, preservando os textos originais para que a entidade
    faça a normalização autoritativa. Ele existe para validar a forma do JSON.
    """

    model_config = ConfigDict(extra="ignore")

    titulo: str
    descricao: str
    tecnologias: str

    @field_validator("titulo", "descricao", "tecnologias", mode="before")
    @classmethod
    def validar_formato_e_tamanho(
        cls, valor: object, info: ValidationInfo
    ) -> str:
        """Valida string e comprimento sem normalizar o valor recebido.

        O método rejeita tipos diferentes de texto e mede o valor após remover
        espaços apenas para comparação. Ele existe para manter o formato do
        request alinhado aos limites públicos sem duplicar a entidade.
        """
        if not isinstance(valor, str):
            raise ValueError("Campo de texto inválido.")

        limite_por_campo = {
            "titulo": TAMANHO_MAXIMO_TITULO_PROJETO,
            "descricao": TAMANHO_MAXIMO_DESCRICAO_PROJETO,
            "tecnologias": TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO,
        }
        tamanho = len(valor.strip())
        if not TAMANHO_MINIMO_TEXTO_PROJETO <= tamanho <= limite_por_campo[info.field_name]:
            raise ValueError("Tamanho de campo inválido.")
        return valor


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class ProjetoAcademicoResposta(BaseModel):
    """Define os campos públicos devolvidos ao criar um projeto.

    O DTO contém UUIDs e textos primitivos extraídos explicitamente da entidade.
    Ele existe para estabilizar o contrato HTTP sem serializar o objeto Domain.
    """

    id: UUID
    usuario_id: UUID
    titulo: str
    descricao: str
    tecnologias: str


class SugestaoDescricaoProjetoRequisicao(BaseModel):
    """Representa o título e as tecnologias usados para pedir uma sugestão.

    O DTO ignora campos desconhecidos, exige texto sem caracteres de controle,
    título com 1 a 200 caracteres e tecnologias com até 300 caracteres após
    aparar espaços, usando os limites do projeto acadêmico. Ele existe para
    barrar requisições malformadas antes de acionar o assistente.
    """

    model_config = ConfigDict(extra="ignore")

    titulo: str
    tecnologias: str

    @field_validator("titulo", "tecnologias", mode="before")
    @classmethod
    def validar_texto(cls, valor: object, info: ValidationInfo) -> str:
        """Valida tipo, caracteres de controle e tamanho de um campo.

        O método exige texto, recusa caracteres de controle e mede o valor sem
        espaços externos; o título é obrigatório e as tecnologias podem vir
        vazias. Ele existe para alinhar a fronteira aos limites do projeto sem
        normalizar o texto, que fica a cargo do assistente.
        """
        if not isinstance(valor, str):
            raise ValueError("Campo de texto inválido.")
        if any(category(caractere) == "Cc" for caractere in valor):
            raise ValueError("Campo de texto inválido.")
        minimo, maximo = {
            "titulo": (TAMANHO_MINIMO_TEXTO_PROJETO, TAMANHO_MAXIMO_TITULO_PROJETO),
            "tecnologias": (0, TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO),
        }[info.field_name]
        if not minimo <= len(valor.strip()) <= maximo:
            raise ValueError("Tamanho de campo inválido.")
        return valor


class SugestaoDescricaoProjetoResposta(BaseModel):
    """Define o corpo público devolvido com a sugestão de descrição.

    O DTO contém apenas o texto sugerido, sem indicar a estratégia usada nem
    dados do estudante. Ele existe para que o cliente apresente a sugestão
    para aceite, edição ou rejeição, sem que nada seja salvo.
    """

    descricao: str


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
def criar_router(
    cadastrar_projeto_academico: CadastroProjetoAcademicoExecutor | None,
    assistente_descricao: AssistenteDescricaoProjeto | None = None,
    # Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
    consultar_projeto_academico: ConsultaProjetoAcademicoExecutor | None = None,
    editar_projeto_academico: EdicaoProjetoAcademicoExecutor | None = None,
    excluir_projeto_academico: ExclusaoProjetoAcademicoExecutor | None = None,
) -> APIRouter:
    """Registra cadastro, sugestão, detalhe, edição e exclusão de projeto.

    Os handlers leem JSON sem deixar erros de validação refletirem valores
    recebidos, exigem o principal de ``request.state`` e traduzem falhas para
    HTTP; a sugestão converte a indisponibilidade do assistente em 503. Ele
    existe para expor o caso de uso e o assistente com propriedade segura.
    """
    router = APIRouter()

    @router.post(
        "/projetos-academicos/sugestao-descricao",
        response_model=SugestaoDescricaoProjetoResposta,
        status_code=status.HTTP_200_OK,
        responses={
            422: {"description": "Dados da sugestão de descrição inválidos."},
            503: {"description": "Assistente de descrição indisponível."},
        },
        openapi_extra={
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": SugestaoDescricaoProjetoRequisicao.model_json_schema()
                    }
                },
            }
        },
    )
    async def sugerir_descricao(request: Request) -> SugestaoDescricaoProjetoResposta:
        """Devolve uma sugestão de descrição sem salvar nada.

        O handler exige assistente e principal autenticado, valida título e
        tecnologias pelo DTO, delega ao assistente e devolve só o texto
        sugerido; indisponibilidade vira 503 e regra violada vira 422, ambos
        com mensagens genéricas. Ele existe para oferecer a orientação do RF04
        com falha controlada, deixando a decisão de usar a sugestão ao estudante.
        """
        if assistente_descricao is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Assistente de descrição indisponível.",
            )
        if not isinstance(getattr(request.state, "usuario_id", None), UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária.",
            )
        try:
            requisicao = SugestaoDescricaoProjetoRequisicao.model_validate(
                await request.json()
            )
        except (JSONDecodeError, UnicodeDecodeError, ValidationError) as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Dados da sugestão de descrição inválidos.",
            ) from erro

        try:
            saida = await assistente_descricao.sugerir_descricao(
                AssistenteDescricaoProjetoEntrada(
                    titulo=requisicao.titulo, tecnologias=requisicao.tecnologias
                )
            )
        except AssistenteDescricaoProjetoIndisponivel as erro:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Assistente de descrição indisponível.",
            ) from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Os dados informados não permitem sugerir uma descrição.",
            ) from erro
        return SugestaoDescricaoProjetoResposta(descricao=saida.descricao)

    @router.post(
        "/projetos-academicos",
        response_model=ProjetoAcademicoResposta,
        status_code=status.HTTP_201_CREATED,
        responses={422: {"description": "Dados do projeto acadêmico inválidos."}},
        openapi_extra={
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": CadastroProjetoAcademicoRequisicao.model_json_schema()
                    }
                },
            }
        },
    )
    async def cadastrar(request: Request) -> ProjetoAcademicoResposta:
        """Cadastra projeto para o usuário presente no estado da requisição.

        O endpoint exige executor e UUID autenticado, valida JSON pelo DTO e
        converte a entidade para resposta explícita. Ele existe para aceitar
        somente o proprietário validado pelo middleware.
        """
        if cadastrar_projeto_academico is None:
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
            requisicao = CadastroProjetoAcademicoRequisicao.model_validate(
                await request.json()
            )
        except (JSONDecodeError, UnicodeDecodeError, ValidationError) as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Dados do projeto acadêmico inválidos.",
            ) from erro

        entrada = CadastrarProjetoAcademicoEntrada(
            usuario_id=UsuarioId(usuario_id),
            titulo=requisicao.titulo,
            descricao=requisicao.descricao,
            tecnologias=requisicao.tecnologias,
        )
        try:
            projeto = await cadastrar_projeto_academico.executar(entrada)
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Os dados do projeto acadêmico violam as regras de cadastro.",
            ) from erro

        return ProjetoAcademicoResposta(
            id=projeto.id.valor,
            usuario_id=projeto.usuario_id.valor,
            titulo=projeto.titulo,
            descricao=projeto.descricao,
            tecnologias=projeto.tecnologias,
        )

    # Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
    @router.get(
        "/projetos-academicos/{projeto_id}", response_model=ProjetoAcademicoResposta,
        summary="Consultar projeto acadêmico",
        description="Obtém o detalhe de um projeto próprio ativo pelo ID, usando o dono da sessão.",
        responses=_respostas_operacao("Consulta"),
    )
    async def consultar(projeto_id: str, request: Request) -> ProjetoAcademicoResposta:
        """Traduz a consulta HTTP em entrada interna com dono da sessão.

        Valida sessão, disponibilidade e UUID, delega ao executor e converte
        entidade ou ausência uniforme para oferecer detalhe sem expor domínio.
        """
        identidade, usuario = _identificar_operacao(
            projeto_id, request, consultar_projeto_academico, "Consulta"
        )
        try:
            projeto = await consultar_projeto_academico.executar(
                ConsultarProjetoAcademicoEntrada(usuario_id=usuario, projeto_id=identidade)
            )
        except ProjetoAcademicoNaoEncontrado as erro:
            raise HTTPException(404, "Projeto acadêmico não encontrado.") from erro
        return _para_resposta(projeto)

    # Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
    @router.put(
        "/projetos-academicos/{projeto_id}", response_model=ProjetoAcademicoResposta,
        summary="Atualizar projeto acadêmico",
        description=(
            "Substitui título, descrição e tecnologias de projeto próprio ativo. "
            "ID e dono não mudam. Limites de 200, 2000 e 300 pontos de código Unicode "
            "após strip, não bytes nem grafemas; espaços externos não contam."
        ),
        responses=_respostas_operacao("Edição"),
        openapi_extra={"requestBody": {"required": True, "content": {
            "application/json": {"schema": EdicaoProjetoAcademicoRequisicao.model_json_schema()}
        }}},
    )
    async def editar(projeto_id: str, request: Request) -> ProjetoAcademicoResposta:
        """Substitui textos recebidos sem aceitar ID ou dono pelo corpo.

        Valida JSON pelo DTO pós-strip, delega ao executor e traduz falhas sem
        ecoar a entrada, para atualizar projeto próprio com contrato estável.
        """
        identidade, usuario = _identificar_operacao(
            projeto_id, request, editar_projeto_academico, "Edição"
        )
        try:
            dados = EdicaoProjetoAcademicoRequisicao.model_validate(await request.json())
        except (JSONDecodeError, UnicodeDecodeError, ValidationError) as erro:
            raise HTTPException(422, "Dados do projeto acadêmico inválidos.") from erro
        try:
            projeto = await editar_projeto_academico.executar(EditarProjetoAcademicoEntrada(
                usuario_id=usuario, projeto_id=identidade, titulo=dados.titulo,
                descricao=dados.descricao, tecnologias=dados.tecnologias,
            ))
        except ProjetoAcademicoNaoEncontrado as erro:
            raise HTTPException(404, "Projeto acadêmico não encontrado.") from erro
        except RegraDeDominioViolada as erro:
            raise HTTPException(422, "Dados do projeto acadêmico inválidos.") from erro
        return _para_resposta(projeto)

    # Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
    @router.delete(
        "/projetos-academicos/{projeto_id}", status_code=204, response_class=Response,
        summary="Excluir projeto acadêmico",
        description=("Exclui logicamente projeto próprio. Repetições do dono retornam 204; "
                     "seleções de currículo permanecem e nenhuma leitura de currículo muda."),
        responses=_respostas_operacao("Exclusão"),
    )
    async def excluir(projeto_id: str, request: Request) -> Response:
        """Delega exclusão lógica e responde sem corpo, inclusive na repetição.

        Obtém dono da sessão e UUID validado e traduz ausência em 404 uniforme
        para expor a operação idempotente sem aceitar propriedade do cliente.
        """
        identidade, usuario = _identificar_operacao(
            projeto_id, request, excluir_projeto_academico, "Exclusão"
        )
        try:
            await excluir_projeto_academico.executar(ExcluirProjetoAcademicoEntrada(
                usuario_id=usuario, projeto_id=identidade,
            ))
        except ProjetoAcademicoNaoEncontrado as erro:
            raise HTTPException(404, "Projeto acadêmico não encontrado.") from erro
        return Response(status_code=204)

    return router


# Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
class ConsultaProjetoAcademicoExecutor(Protocol):
    """Define a execução de consulta de detalhe sem dependência concreta.

    Recebe entrada interna e devolve entidade para permitir que HTTP delegue
    a leitura pela capacidade existente, independente de persistência.
    """

    async def executar(self, entrada: ConsultarProjetoAcademicoEntrada) -> ProjetoAcademico:
        """Consulta pelo contrato interno e devolve o projeto ativo.

        Delega ID e dono ao caso existente para separar tradução HTTP da leitura.
        """


class EdicaoProjetoAcademicoExecutor(Protocol):
    """Define a capacidade de edição completa consumida pela borda HTTP.

    Recebe entrada tipada com três textos e devolve entidade para manter
    o handler independente do executor transacional concreto.
    """

    async def executar(self, entrada: EditarProjetoAcademicoEntrada) -> ProjetoAcademico:
        """Edita pelo contrato interno e devolve o projeto validado.

        Encaminha a entrada ao caso existente para separar HTTP das invariantes.
        """


class ExclusaoProjetoAcademicoExecutor(Protocol):
    """Define exclusão lógica por entrada interna sem detalhes de armazenamento.

    Recebe IDs e devolve o estado excluído para conectar o handler ao caso
    idempotente existente sem expor repositório ou relógio.
    """

    async def executar(self, entrada: ExcluirProjetoAcademicoEntrada) -> ProjetoAcademico:
        """Exclui pelo contrato interno ou devolve o tombstone próprio.

        Delega a transição ao caso existente para manter HTTP sem regras de exclusão.
        """


class EdicaoProjetoAcademicoRequisicao(CadastroProjetoAcademicoRequisicao):
    """Descreve os três textos obrigatórios da substituição completa.

    Reutiliza o validator pós-strip e adiciona somente metadados de schema,
    para documentar limites sem impor comprimento bruto à validação runtime.
    """

    titulo: str = Field(json_schema_extra={"minLength": 1, "maxLength": 200})
    descricao: str = Field(json_schema_extra={"minLength": 1, "maxLength": 2000})
    tecnologias: str = Field(json_schema_extra={"minLength": 1, "maxLength": 300})


def _identificar_operacao(
    projeto_id: str, request: Request, executor: object | None, operacao: str
) -> tuple[ProjetoAcademicoId, UsuarioId]:
    """Obtém sessão e UUID sem refletir entradas inválidas na resposta.

    Confere principal, disponibilidade e conversão do caminho nessa ordem,
    para fornecer identidades tipadas aos novos handlers com erros seguros.
    """
    usuario_id = getattr(request.state, "usuario_id", None)
    if not isinstance(usuario_id, UUID):
        raise HTTPException(401, "Autenticação necessária.")
    if executor is None:
        raise HTTPException(503, f"{operacao} indisponível.")
    try:
        identidade = UUID(str(projeto_id))
    except ValueError as erro:
        raise HTTPException(422, "Identificador de projeto acadêmico inválido.") from erro
    return ProjetoAcademicoId(identidade), UsuarioId(usuario_id)


def _para_resposta(projeto: ProjetoAcademico) -> ProjetoAcademicoResposta:
    """Converte explicitamente identidade, dono e textos em DTO público.

    Extrai somente os cinco campos públicos para ocultar a entidade e marcador
    interno sem alterar o contrato já utilizado pelo cadastro.
    """
    return ProjetoAcademicoResposta(
        id=projeto.id.valor, usuario_id=projeto.usuario_id.valor, titulo=projeto.titulo,
        descricao=projeto.descricao, tecnologias=projeto.tecnologias,
    )


def _respostas_operacao(operacao: str) -> dict[int, dict[str, str]]:
    """Documenta falhas comuns e indisponibilidade específica de operação.

    Monta descrições estáveis para os novos decoradores, para que o Swagger
    informe autenticação, ausência uniforme, entrada inválida e executor ausente.
    """
    return {
        401: {"description": "Autenticação necessária."},
        404: {"description": "Projeto acadêmico não encontrado (ausente, alheio ou excluído)."},
        422: {"description": "Identificador ou dados do projeto acadêmico inválidos."},
        503: {"description": f"{operacao} indisponível."},
    }
