"""Organiza a documentação OpenAPI (Swagger) da interface HTTP.

O módulo define os grupos de rotas exibidos no Swagger e descreve o esquema
de autenticação por cookie de sessão. Ele existe para manter a documentação
interativa navegável e fiel ao contrato de autenticação da API, sem alterar
handlers, casos de uso ou o domínio.
"""

from collections.abc import Callable, Iterable
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from backend.api.sessoes import COOKIE_SESSAO

TAG_CADASTRO_ACESSO = "Cadastro e acesso"
TAG_SESSOES = "Sessões"
TAG_PERFIL_ESTUDANTE = "Perfil do estudante"
TAG_DADOS_CONTATO = "Dados de contato"
TAG_FORMACOES_ACADEMICAS = "Formações acadêmicas"
TAG_EXPERIENCIAS_PROFISSIONAIS = "Experiências profissionais"
TAG_PROJETOS_ACADEMICOS = "Projetos acadêmicos"
TAG_COMPETENCIAS = "Competências"
TAG_IDIOMAS = "Idiomas"
TAG_CURSOS = "Cursos"
TAG_CERTIFICACOES = "Certificações"
TAG_LINKS_PROFISSIONAIS = "Links profissionais"
TAG_DOCUMENTOS_COMPLEMENTARES = "Documentos complementares"
TAG_VERSOES_CURRICULO = "Versões de currículo"
TAG_ITENS_VERSAO_CURRICULO = "Itens da versão de currículo"
TAG_PREVIA_VERSAO_CURRICULO = "Prévia da versão de currículo"
# Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
TAG_VAGAS = "Vagas"
TAG_SAUDE = "Saúde"

ESQUEMA_SESSAO = "sessaoCookie"

METADADOS_TAGS: list[dict[str, str]] = [
    {
        "name": TAG_CADASTRO_ACESSO,
        "description": (
            "Cadastro do estudante e login. Use `POST /acessos` para "
            "autenticar: o navegador guarda o cookie de sessão e o envia "
            "automaticamente nas demais requisições do Swagger."
        ),
    },
    {"name": TAG_SESSOES, "description": "Encerramento da sessão atual (logout)."},
    {
        "name": TAG_SAUDE,
        "description": "Verificação agregada de disponibilidade da aplicação.",
    },
    {
        "name": TAG_PERFIL_ESTUDANTE,
        "description": "Consulta, edição e exclusão do perfil do estudante.",
    },
    {"name": TAG_DADOS_CONTATO, "description": "Dados de contato do estudante."},
    {
        "name": TAG_FORMACOES_ACADEMICAS,
        "description": "Cadastro, edição e exclusão de formações acadêmicas.",
    },
    {
        "name": TAG_EXPERIENCIAS_PROFISSIONAIS,
        "description": "Cadastro de experiências profissionais.",
    },
    {
        "name": TAG_PROJETOS_ACADEMICOS,
        "description": "Cadastro de projetos acadêmicos.",
    },
    {"name": TAG_COMPETENCIAS, "description": "Cadastro de competências."},
    {"name": TAG_IDIOMAS, "description": "Cadastro de idiomas."},
    {"name": TAG_CURSOS, "description": "Cadastro de cursos."},
    {"name": TAG_CERTIFICACOES, "description": "Cadastro de certificações."},
    {
        "name": TAG_LINKS_PROFISSIONAIS,
        "description": "Cadastro de links profissionais.",
    },
    {
        "name": TAG_DOCUMENTOS_COMPLEMENTARES,
        "description": "Armazenamento de documentos complementares.",
    },
    {
        "name": TAG_VERSOES_CURRICULO,
        "description": "Criação, edição, listagem e exclusão de versões de currículo.",
    },
    {
        "name": TAG_ITENS_VERSAO_CURRICULO,
        "description": "Seleção e remoção de itens do perfil em uma versão de currículo.",
    },
    {
        "name": TAG_PREVIA_VERSAO_CURRICULO,
        "description": "Prévia de uma versão de currículo.",
    },
    # Proveniência: decision-analysis prompts/backend/20261018-095612-expor-busca-vagas-api-v001.md#v001
    {
        "name": TAG_VAGAS,
        "description": "Consulta e listagem de vagas de emprego externas.",
    },
]

DESCRICAO_API = (
    "API do sistema de currículos.\n\n"
    "**Autenticação:** as rotas com cadeado exigem o cookie de sessão "
    f"`{COOKIE_SESSAO}`. Para obtê-lo pelo Swagger, execute `POST /acessos` "
    "com e-mail e senha; o navegador armazena o cookie e o reenvia nas "
    "chamadas seguintes. Use `DELETE /sessao/atual` para encerrar a sessão."
)


def configurar_documentacao(
    app: FastAPI, rotas_publicas: Iterable[tuple[str, str]] | None
) -> None:
    """Substitui a geração do schema OpenAPI para incluir a autenticação.

    A função instala em `app.openapi` um gerador preguiçoso que monta o schema
    padrão do FastAPI uma única vez e, quando `rotas_publicas` é informado,
    registra o esquema `apiKey` em cookie e o aplica a toda operação cujo par
    (método, caminho) não seja público. Sem rotas públicas, nenhuma exigência
    é documentada, refletindo a ausência do middleware de autenticação. Ela
    existe para que o Swagger mostre quais rotas exigem sessão a partir da
    mesma lista usada pelo middleware, evitando divergência entre ambos.
    """
    publicas = None if rotas_publicas is None else frozenset(rotas_publicas)
    app.openapi = _criar_gerador_openapi(app, publicas)  # type: ignore[method-assign]


def _criar_gerador_openapi(
    app: FastAPI, rotas_publicas: frozenset[tuple[str, str]] | None
) -> Callable[[], dict[str, Any]]:
    """Cria a função que gera e memoriza o schema OpenAPI da aplicação.

    A função devolve um fechamento que reaproveita `app.openapi_schema` quando
    já calculado; caso contrário, usa `get_openapi` com título, versão, tags e
    rotas da aplicação e acrescenta a segurança por cookie. Ela existe para
    seguir o mecanismo de customização recomendado pelo FastAPI sem gerar o
    schema a cada requisição de `/openapi.json`.
    """

    def gerar() -> dict[str, Any]:
        """Gera o schema OpenAPI com segurança por cookie nas rotas privadas.

        O fechamento monta o schema padrão, adiciona o esquema de sessão e
        marca as operações privadas, guardando o resultado na aplicação. Ele
        existe para ser chamado pelo FastAPI ao servir a documentação.
        """
        if app.openapi_schema is not None:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
            tags=app.openapi_tags,
        )
        if rotas_publicas is not None:
            _aplicar_seguranca_sessao(schema, rotas_publicas)
        app.openapi_schema = schema
        return schema

    return gerar


def _aplicar_seguranca_sessao(
    schema: dict[str, Any], rotas_publicas: frozenset[tuple[str, str]]
) -> None:
    """Registra o cookie de sessão e o exige nas operações privadas.

    A função adiciona `components.securitySchemes` com um `apiKey` no cookie
    de sessão e percorre `paths`, atribuindo `security` às operações cujo par
    (método em maiúsculas, caminho) não pertence às rotas públicas. Ela existe
    para exibir o cadeado do Swagger exatamente nas rotas protegidas pelo
    middleware de autenticação.
    """
    componentes = schema.setdefault("components", {})
    componentes.setdefault("securitySchemes", {})[ESQUEMA_SESSAO] = {
        "type": "apiKey",
        "in": "cookie",
        "name": COOKIE_SESSAO,
        "description": (
            "Cookie HttpOnly emitido por `POST /acessos`. O navegador o envia "
            "automaticamente; não é necessário preenchê-lo em *Authorize*."
        ),
    }
    for caminho, operacoes in schema.get("paths", {}).items():
        for metodo, operacao in operacoes.items():
            if (metodo.upper(), caminho) not in rotas_publicas:
                operacao["security"] = [{ESQUEMA_SESSAO: []}]
