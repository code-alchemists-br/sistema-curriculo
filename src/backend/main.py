"""Compõe a aplicação ASGI, a readiness de persistência e o logging.

O módulo cria uma engine assíncrona quando `DATABASE_URL` está configurada,
compõe os executores persistidos, incluindo perfil do estudante, cadastro, leitura,
edição e exclusão de formações acadêmicas, projetos acadêmicos e experiências profissionais,
injeta a readiness e encerra a engine no shutdown. Sem essa variável, os fluxos
persistidos ficam indisponíveis. Ele existe para concentrar a composição de
infraestrutura fora das camadas internas.
"""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.api.configuracao_cookie_sessao import ConfiguracaoCookieSessao
from backend.api.factory import create_app
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.application.decisao_recomendacao import (
    ConsultarDecisoesRecomendacao,
    RegistrarDecisaoRecomendacao,
)
from backend.application.exclusao_versao_curriculo import ExcluirVersaoCurriculo
from backend.application.listagem_versoes_curriculo import ListarVersoesCurriculo
from backend.application.ports import GeradorUsuarioId, VerificadorSenha
from backend.application.previa_versao_curriculo import GerarPreviaVersaoCurriculo
from backend.application.revisao_versao_curriculo import RevisarVersaoCurriculo
from backend.application.saude import VerificadorPersistencia
from backend.application.selecao_itens_versao_curriculo import (
    DesselecionarItemVersaoCurriculo,
    SelecionarItemVersaoCurriculo,
)
from backend.application.sessoes import CriadorSessao
from backend.application.versao_curriculo import (
    AtualizarOrdemSecoesCurriculo,
    CriarVersaoCurriculo,
    EditarVersaoCurriculo,
)
from backend.configuracao_logging import configurar_logging
from backend.infrastructure.identificadores.geradores import (
    GeradorCurriculoIdUuid4,
    GeradorCompetenciaIdUuid4,
    GeradorExperienciaProfissionalIdUuid4,
    GeradorFormacaoAcademicaIdUuid4,
    # Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
    GeradorProjetoAcademicoIdUuid4,
    GeradorUsuarioIdUuid4,
)
from backend.infrastructure.persistence.sqlalchemy.acesso_estudante import (
    AcessarEstudanteSqlAlchemy,
    AutenticadorSessaoSqlAlchemy,
    CriadorSessaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.cadastro_estudante import (
    CadastroEstudanteSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.cadastro_experiencia_profissional import (
    CadastroExperienciaProfissionalSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.consulta_item_perfil import (
    ConsultaItemPerfilSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.consulta_proprietario_item import (
    ConsultaProprietarioItemSqlAlchemy,
)

# Proveniência: docs/decisao-executor-transacional.md
from backend.infrastructure.persistence.sqlalchemy.executor_transacional import (
    criar_executor_transacional,
)

# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
from backend.infrastructure.persistence.sqlalchemy.listar_associacoes_curriculo_vaga import (
    ListarAssociacoesCurriculoVagaSqlAlchemy,
)

# Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
from backend.infrastructure.persistence.sqlalchemy.listar_experiencias_profissionais import (
    ListarExperienciasProfissionaisSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.operacoes_competencia import (
    CadastroCompetenciaSqlAlchemy,
    ExclusaoCompetenciaSqlAlchemy,
    ListarCompetenciasSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.operacoes_experiencia_profissional import (
    EdicaoExperienciaProfissionalSqlAlchemy,
    ExclusaoExperienciaProfissionalSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.operacoes_formacao_academica import (
    CadastroFormacaoAcademicaSqlAlchemy,
    EdicaoFormacaoAcademicaSqlAlchemy,
    ExclusaoFormacaoAcademicaSqlAlchemy,
    # Proveniência: decision-analysis prompts/backend/20261107-171028-listar-formacoes-academicas-v001.md#v001
    ListarFormacoesAcademicasSqlAlchemy,
    RelogioUtc,
)
from backend.infrastructure.persistence.sqlalchemy.operacoes_perfil_estudante import (
    AtualizarPerfilCompletoSqlAlchemy,
    ConsultarPerfilSqlAlchemy,
    EdicaoPerfilSqlAlchemy,
    ExclusaoPerfilSqlAlchemy,
)

# Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
from backend.infrastructure.persistence.sqlalchemy.operacoes_projeto_academico import (
    CadastroProjetoAcademicoSqlAlchemy,
    ConsultaProjetoAcademicoSqlAlchemy,
    EdicaoProjetoAcademicoSqlAlchemy,
    ExclusaoProjetoAcademicoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_curriculo import (
    RepositorioCurriculoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_decisao_recomendacao import (
    RepositorioDecisaoRecomendacaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_usuario import (
    RepositorioUsuarioSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.verificador_persistencia import (
    VerificadorPersistenciaSqlalchemy,
)
from backend.infrastructure.security.autenticador_sessao_indisponivel import (
    AutenticadorSessaoIndisponivel,
)
from backend.infrastructure.security.senhas import DerivadorSenhaScrypt

configurar_logging()

ORIGENS_CORS_DESENVOLVIMENTO = (
    "http://127.0.0.1:5173",
    "http://localhost:5173",
)


def _obter_origens_cors(valor_configurado: str | None) -> tuple[str, ...]:
    """Define as origens permitidas para chamadas HTTP feitas pelo navegador.

    A função usa as duas origens locais do Vite quando a variável não foi
    definida e, quando foi, divide sua lista separada por vírgulas removendo
    espaços e valores vazios. Ela existe para liberar o desenvolvimento local
    sem tornar CORS aberto e permitir que cada ambiente publique suas origens.
    """
    if not valor_configurado:
        return ORIGENS_CORS_DESENVOLVIMENTO
    return tuple(
        origem.strip() for origem in valor_configurado.split(",") if origem.strip()
    )


def _criar_configuracao_cookie_sessao(
    valor_secure: str | None,
) -> ConfiguracaoCookieSessao:
    """Configura o cookie de sessão sem reduzir a segurança por padrão.

    A função exige o valor literal ``false`` para liberar cookie HTTP local;
    qualquer ausência ou outro valor mantém HTTPS obrigatório. Ela existe para
    distinguir desenvolvimento deliberado da política segura de produção.
    """
    return ConfiguracaoCookieSessao(seguro=valor_secure != "false")


def _configurar_cors(aplicacao: FastAPI, origens: tuple[str, ...]) -> None:
    """Instala a política CORS que protege e permite o frontend configurado.

    A função registra middleware com credenciais, métodos e cabeçalhos usados
    pela API, restringindo as origens à lista recebida. Ela existe para que o
    navegador possa chamar a API de outra porta sem expor a aplicação a todas
    as origens ou duplicar configuração nos controllers.
    """
    aplicacao.add_middleware(
        CORSMiddleware,
        allow_origins=list(origens),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type"],
    )


def _criar_engine_persistencia(database_url: str | None) -> AsyncEngine | None:
    """Cria a engine PostgreSQL assíncrona quando há URL de persistência.

    A função normaliza URLs PostgreSQL sem driver para `postgresql+psycopg`,
    ativa verificação de conexão e limita o tempo de conexão. Ela existe para
    fornecer à aplicação uma dependência real para o probe de readiness.
    """
    if not database_url:
        return None

    url = make_url(database_url)
    if url.drivername == "postgresql":
        url = url.set(drivername="postgresql+psycopg")
    return create_async_engine(
        url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 2},
    )


def _criar_cadastrar_estudante(
    engine: AsyncEngine | None,
    gerador_usuario_id: GeradorUsuarioId | None = None,
) -> CadastroEstudanteSqlAlchemy | None:
    """Compõe o executor transacional de cadastro quando há persistência.

    A função cria uma fábrica de sessões assíncronas e combina o adapter de
    transação com o gerador de UUID da infraestrutura; sem engine, mantém a
    ausência explícita tratada pela API. Ela existe para habilitar o cadastro
    real sem introduzir dependências de banco no controller ou na Application.
    """
    if engine is None:
        return None
    sessoes = async_sessionmaker(engine, expire_on_commit=False)
    return CadastroEstudanteSqlAlchemy(
        sessoes,
        gerador_usuario_id or GeradorUsuarioIdUuid4(),
    )


def _criar_sessoes_persistencia(
    engine: AsyncEngine | None,
) -> async_sessionmaker[AsyncSession] | None:
    """Cria a fábrica de sessões reutilizada pelos fluxos de acesso e sessão.

    A função vincula sessões assíncronas à engine disponível sem abrir conexão;
    na ausência de banco, devolve ausência explícita. Ela existe para que login
    e autenticação compartilhem uma configuração de persistência, não sessões.
    """
    if engine is None:
        return None
    return async_sessionmaker(engine, expire_on_commit=False)


def _criar_acessar_estudante(
    sessoes: async_sessionmaker[AsyncSession] | None,
    verificador_senha: VerificadorSenha,
) -> AcessarEstudanteSqlAlchemy | None:
    """Compõe o executor de login somente quando existe persistência configurada.

    A função conecta a fábrica de sessões ao adapter de acesso e mantém a
    indisponibilidade explícita sem banco. Ela existe para não expor um login
    aparentemente funcional quando as credenciais não podem ser consultadas.
    """
    return AcessarEstudanteSqlAlchemy(sessoes, verificador_senha) if sessoes else None


def _criar_criador_sessao(
    sessoes: async_sessionmaker[AsyncSession] | None,
) -> CriadorSessao | None:
    """Compõe a emissão persistida de sessão quando há banco disponível.

    A função entrega a fábrica de sessões ao adapter transacional ou devolve
    ausência para a API traduzir em indisponibilidade. Ela existe para impedir
    que login emita cookie sem armazenar sua sessão correspondente.
    """
    return CriadorSessaoSqlAlchemy(sessoes) if sessoes else None


def _criar_autenticador_sessao(
    sessoes: async_sessionmaker[AsyncSession] | None,
) -> AutenticadorSessao:
    """Escolhe o autenticador persistido ou a implementação indisponível.

    A função cria o adapter que consulta sessões por requisição quando há banco
    e preserva a negação explícita nos ambientes sem persistência. Ela existe
    para manter a proteção das rotas coerente com a capacidade de login.
    """
    return (
        AutenticadorSessaoSqlAlchemy(sessoes)
        if sessoes
        else AutenticadorSessaoIndisponivel()
    )


_engine_persistencia = _criar_engine_persistencia(os.environ.get("DATABASE_URL"))
_verificador_persistencia: VerificadorPersistencia | None = (
    VerificadorPersistenciaSqlalchemy(_engine_persistencia)
    if _engine_persistencia is not None
    else None
)
_cadastrar_estudante = _criar_cadastrar_estudante(_engine_persistencia)
_sessoes_persistencia = _criar_sessoes_persistencia(_engine_persistencia)
# Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
_listar_associacoes_curriculo_vaga = (
    ListarAssociacoesCurriculoVagaSqlAlchemy(_sessoes_persistencia)
    if _sessoes_persistencia is not None
    else None
)
# Proveniência: docs/decisao-executor-transacional.md
# Versões do currículo (onde o modelo escolhido, `layout`, é gravado). Cada
# executor abre uma transação por chamada; sem banco, ficam None e a rota
# responde 503.
_criar_versao_curriculo = criar_executor_transacional(
    _sessoes_persistencia,
    lambda sessao: CriarVersaoCurriculo(
        RepositorioCurriculoSqlAlchemy(sessao), GeradorCurriculoIdUuid4()
    ),
)
_editar_versao_curriculo = criar_executor_transacional(
    _sessoes_persistencia,
    lambda sessao: EditarVersaoCurriculo(RepositorioCurriculoSqlAlchemy(sessao)),
)
_listar_versoes_curriculo = criar_executor_transacional(
    _sessoes_persistencia,
    lambda sessao: ListarVersoesCurriculo(RepositorioCurriculoSqlAlchemy(sessao)),
)
_excluir_versao_curriculo = criar_executor_transacional(
    _sessoes_persistencia,
    lambda sessao: ExcluirVersaoCurriculo(RepositorioCurriculoSqlAlchemy(sessao)),
)
_atualizar_ordem_secoes_curriculo = criar_executor_transacional(
    _sessoes_persistencia,
    lambda sessao: AtualizarOrdemSecoesCurriculo(RepositorioCurriculoSqlAlchemy(sessao)),
)
_selecionar_item_versao_curriculo = criar_executor_transacional(
    _sessoes_persistencia,
    lambda sessao: SelecionarItemVersaoCurriculo(
        RepositorioCurriculoSqlAlchemy(sessao),
        ConsultaProprietarioItemSqlAlchemy(sessao),
    ),
)
_desselecionar_item_versao_curriculo = criar_executor_transacional(
    _sessoes_persistencia,
    lambda sessao: DesselecionarItemVersaoCurriculo(
        RepositorioCurriculoSqlAlchemy(sessao)
    ),
)
def _montar_previa_versao_curriculo(sessao: AsyncSession) -> GerarPreviaVersaoCurriculo:
    """Monta a prévia da versão ligando repositórios e leitura de itens à sessão.

    A função reúne o repositório de currículo, o de usuário e a leitura de itens
    por tipo na mesma sessão. Ela existe para que prévia e revisão compartilhem a
    montagem, já que a revisão reaproveita a prévia.
    """
    return GerarPreviaVersaoCurriculo(
        RepositorioCurriculoSqlAlchemy(sessao),
        RepositorioUsuarioSqlAlchemy(sessao),
        ConsultaItemPerfilSqlAlchemy(sessao),
    )


_gerar_previa_versao_curriculo = criar_executor_transacional(
    _sessoes_persistencia, _montar_previa_versao_curriculo
)
_revisar_versao_curriculo = criar_executor_transacional(
    _sessoes_persistencia,
    lambda sessao: RevisarVersaoCurriculo(
        _montar_previa_versao_curriculo(sessao), RelogioUtc()
    ),
)
_registrar_decisao_recomendacao = criar_executor_transacional(
    _sessoes_persistencia,
    lambda sessao: RegistrarDecisaoRecomendacao(
        RevisarVersaoCurriculo(_montar_previa_versao_curriculo(sessao), RelogioUtc()),
        RepositorioDecisaoRecomendacaoSqlAlchemy(sessao),
        RelogioUtc(),
    ),
)
_consultar_decisoes_recomendacao = criar_executor_transacional(
    _sessoes_persistencia,
    lambda sessao: ConsultarDecisoesRecomendacao(
        RepositorioCurriculoSqlAlchemy(sessao),
        RepositorioDecisaoRecomendacaoSqlAlchemy(sessao),
    ),
)
_derivador_senha = DerivadorSenhaScrypt()
_acessar_estudante = _criar_acessar_estudante(
    _sessoes_persistencia,
    _derivador_senha,
)
_criador_sessao = _criar_criador_sessao(_sessoes_persistencia)
_autenticador_sessao = _criar_autenticador_sessao(_sessoes_persistencia)
_configuracao_cookie_sessao = _criar_configuracao_cookie_sessao(
    os.environ.get("SESSION_COOKIE_SECURE")
)


@asynccontextmanager
async def _ciclo_vida_aplicacao(_aplicacao: FastAPI) -> AsyncIterator[None]:
    """Libera recursos da engine quando o processo ASGI é encerrado.

    O contexto mantém os recursos disponíveis durante a execução e descarta a
    engine assíncrona ao sair. Ele existe para evitar conexões ou pools abertos
    após o encerramento da aplicação.
    """
    try:
        yield
    finally:
        if _engine_persistencia is not None:
            await _engine_persistencia.dispose()


# Proveniência: decision-analysis prompts/backend/20260913-fundamentos-fastapi-v001.md#v001
app = create_app(
    criar_versao_curriculo=_criar_versao_curriculo,
    editar_versao_curriculo=_editar_versao_curriculo,
    listar_versoes_curriculo=_listar_versoes_curriculo,
    excluir_versao_curriculo=_excluir_versao_curriculo,
    atualizar_ordem_secoes_curriculo=_atualizar_ordem_secoes_curriculo,
    selecionar_item_versao_curriculo=_selecionar_item_versao_curriculo,
    desselecionar_item_versao_curriculo=_desselecionar_item_versao_curriculo,
    gerar_previa_versao_curriculo=_gerar_previa_versao_curriculo,
    revisar_versao_curriculo=_revisar_versao_curriculo,
    registrar_decisao_recomendacao=_registrar_decisao_recomendacao,
    consultar_decisoes_recomendacao=_consultar_decisoes_recomendacao,
    atualizar_perfil_completo=(
        AtualizarPerfilCompletoSqlAlchemy(_sessoes_persistencia)
        if _sessoes_persistencia is not None
        else None
    ),
    consultar_perfil=(
        ConsultarPerfilSqlAlchemy(_sessoes_persistencia)
        if _sessoes_persistencia is not None
        else None
    ),
    editar_perfil=(
        EdicaoPerfilSqlAlchemy(_sessoes_persistencia)
        if _sessoes_persistencia is not None
        else None
    ),
    excluir_perfil=(
        ExclusaoPerfilSqlAlchemy(_sessoes_persistencia, RelogioUtc())
        if _sessoes_persistencia is not None
        else None
    ),
    # Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
    cadastrar_projeto_academico=(
        CadastroProjetoAcademicoSqlAlchemy(
            _sessoes_persistencia, GeradorProjetoAcademicoIdUuid4()
        )
        if _sessoes_persistencia is not None
        else None
    ),
    consultar_projeto_academico=(
        ConsultaProjetoAcademicoSqlAlchemy(_sessoes_persistencia)
        if _sessoes_persistencia is not None
        else None
    ),
    editar_projeto_academico=(
        EdicaoProjetoAcademicoSqlAlchemy(_sessoes_persistencia)
        if _sessoes_persistencia is not None
        else None
    ),
    excluir_projeto_academico=(
        ExclusaoProjetoAcademicoSqlAlchemy(_sessoes_persistencia, RelogioUtc())
        if _sessoes_persistencia is not None
        else None
    ),
    editar_experiencia_profissional=(
        # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
        EdicaoExperienciaProfissionalSqlAlchemy(_sessoes_persistencia, RelogioUtc())
        if _sessoes_persistencia is not None
        else None
    ),
    excluir_experiencia_profissional=(
        ExclusaoExperienciaProfissionalSqlAlchemy(_sessoes_persistencia, RelogioUtc())
        if _sessoes_persistencia is not None
        else None
    ),
    cadastrar_experiencia_profissional=(
        CadastroExperienciaProfissionalSqlAlchemy(
            # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
            _sessoes_persistencia,
            GeradorExperienciaProfissionalIdUuid4(),
            RelogioUtc(),
        )
        if _sessoes_persistencia is not None
        else None
    ),
    # Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
    listar_experiencias_profissionais=(
        ListarExperienciasProfissionaisSqlAlchemy(_sessoes_persistencia)
        if _sessoes_persistencia is not None
        else None
    ),
    # Proveniência: decision-analysis prompts/backend/20261107-171028-listar-formacoes-academicas-v001.md#v001
    listar_formacoes_academicas=(
        ListarFormacoesAcademicasSqlAlchemy(_sessoes_persistencia)
        if _sessoes_persistencia is not None
        else None
    ),
    cadastrar_formacao_academica=(
        CadastroFormacaoAcademicaSqlAlchemy(
            _sessoes_persistencia, GeradorFormacaoAcademicaIdUuid4()
        )
        if _sessoes_persistencia is not None
        else None
    ),
    editar_formacao_academica=(
        EdicaoFormacaoAcademicaSqlAlchemy(_sessoes_persistencia)
        if _sessoes_persistencia is not None
        else None
    ),
    excluir_formacao_academica=(
        ExclusaoFormacaoAcademicaSqlAlchemy(_sessoes_persistencia, RelogioUtc())
        if _sessoes_persistencia is not None
        else None
    ),
    cadastrar_competencia=(
        CadastroCompetenciaSqlAlchemy(
            _sessoes_persistencia, GeradorCompetenciaIdUuid4()
        )
        if _sessoes_persistencia is not None
        else None
    ),
    listar_competencias=(
        ListarCompetenciasSqlAlchemy(_sessoes_persistencia)
        if _sessoes_persistencia is not None
        else None
    ),
    excluir_competencia=(
        ExclusaoCompetenciaSqlAlchemy(_sessoes_persistencia)
        if _sessoes_persistencia is not None
        else None
    ),
    cadastrar_estudante=_cadastrar_estudante,
    acessar_estudante=_acessar_estudante,
    criador_sessao=_criador_sessao,
    derivador_senha=_derivador_senha,
    autenticador_sessao=_autenticador_sessao,
    # Proveniência: decision-analysis prompts/backend/20261102-181117-expor-listagem-associacoes-curriculo-vaga-v001.md#v001
    listar_associacoes_curriculo_vaga=_listar_associacoes_curriculo_vaga,
    verificador_persistencia=_verificador_persistencia,
    lifespan=_ciclo_vida_aplicacao,
    configuracao_cookie=_configuracao_cookie_sessao,
)
_configurar_cors(app, _obter_origens_cors(os.environ.get("CORS_ALLOWED_ORIGINS")))
