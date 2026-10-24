"""Compõe o ciclo real do perfil sobre SQLite migrado e descartável.

Reutiliza Alembic, transporte HTTPS ASGI e cleanup da fixture de credenciais,
sem seu seed, para que cada conta e sessão seja criada pela interface HTTP.
O commit pertence ao harness; esta composição não certifica produção.
"""

# Proveniência: decision-analysis prompts/backend/20261024-105607-cenario-integracao-ciclo-vida-perfil-autorizado-v001.md#v001

from datetime import datetime, timezone
from unittest import SkipTest
from uuid import UUID, uuid4

from sqlalchemy import event, inspect, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.api.factory import create_app
from backend.application.acesso_estudante import AcessarEstudante
from backend.application.cadastro_estudante import CadastrarEstudante
from backend.application.perfil_completo import AtualizarPerfilCompleto
from backend.application.perfil_estudante import (
    ConsultarPerfilEstudante,
    EditarPerfil,
    ExcluirPerfil,
)
from backend.application.ports import GeradorUsuarioId, Relogio
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.repositorio_sessao import (
    RepositorioSessaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_usuario import (
    RepositorioUsuarioSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.sessao import SessaoRegistro
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro
from backend.infrastructure.security.autenticador_sessao import (
    AutenticadorSessaoPersistida,
)
from backend.infrastructure.security.senhas import DerivadorSenhaScrypt
from backend.infrastructure.security.tokens_sessao import CriadorSessaoSeguro
from backend.tests.fixtures.credenciais_sessao import (
    BancoCredenciaisSessao,
    RespostaCredenciais,
    ativar_chaves_estrangeiras,
    solicitar_asgi,
    verificar_revisoes_unicas,
)

SENHA = "Senha-Teste-123"
CADASTRO_A = {
    "nome": "Pessoa A Integração", "email": "perfil.a@example.test", "senha": SENHA,
}
CADASTRO_B = {
    "nome": "Pessoa B Controle", "email": "perfil.b@example.test", "senha": SENHA,
}
CADASTRO_C = {
    "nome": "Pessoa C Controle", "email": "perfil.c@example.test", "senha": SENHA,
}
EDICAO_A = {"nome": "Pessoa A Editada", "email": "perfil.a.editado@example.test"}
PERFIL_COMPLETO_A = {
    **EDICAO_A,
    "endereco": "Rua de Teste, 10",
    "cidade": "São Paulo",
    "telefones": ["+55 11 99999-0001"],
    "linkedin": "https://www.linkedin.com/in/perfil-a-teste",
    "curriculo_lattes": "http://lattes.cnpq.br/123456789",
}
OPERACOES_PERFIL = ("consulta", "edicao", "completo", "exclusao")


class GeradorUsuarioIdUUID4(GeradorUsuarioId):
    """Fornece identidades reais para as contas criadas pelo cenário.

    Encapsula uuid4 na porta de cadastro, sem IDs de seed ou respostas fixas,
    para preservar a geração de identidade durante a integração HTTP.
    """

    def gerar(self) -> UsuarioId:
        """Gera uma identidade tipada usando UUID aleatório da biblioteca padrão.

        Envolve uuid4 em UsuarioId para atender à porta do caso real e permitir
        que o teste capture a identidade devolvida pelo cadastro HTTP.
        """
        return UsuarioId(uuid4())


class RelogioUTC(Relogio):
    """Fornece o instante real de exclusão pela porta interna de tempo.

    Consulta o relógio UTC sem sleeps ou datas fixadas para permitir a transição
    real do agregado sem implementar política de tempo no caso de teste.
    """

    def agora(self) -> datetime:
        """Obtém datetime UTC consciente de fuso pelo relógio do sistema.

        Delega a datetime.now para que o caso real registre a primeira exclusão
        sem depender de uma implementação produtiva nova de relógio.
        """
        return datetime.now(timezone.utc)


class ObservadorCasoPerfil:
    """Observa entradas do perfil sem substituir regras ou persistência.

    Guarda somente identidades e delega integralmente ao caso recebido para
    distinguir bloqueio no middleware de execução real do perfil.
    """

    def __init__(self, caso_real) -> None:
        """Retém o caso real e inicia seu histórico vazio de identidades.

        Não realiza I/O nem configura retorno para manter a observação separada
        do comportamento exercitado e permitir contagem por requisição.
        """
        self.caso_real = caso_real
        self.identidades = []

    async def executar(self, entrada):
        """Registra o proprietário recebido e aguarda o caso real sem tradução.

        Propaga retorno e falhas da implementação para observar a fronteira
        autenticada sem fabricar sucesso ou recusa no teste integrado.
        """
        self.identidades.append(entrada.usuario_id.valor)
        return await self.caso_real.executar(entrada)


class BancoCicloVidaPerfilAutorizado(BancoCredenciaisSessao):
    """Mantém banco vazio migrado e compõe componentes reais por request.

    Herda subprocesso Alembic, snapshots e cleanup, substituindo o preparo com
    seed por migrations apenas, para provar criação das contas via HTTP.
    """

    async def preparar(self) -> None:
        """Migra um banco exclusivo sem inserir usuários ou sessões de seed.

        Valida revisões e head antes do upgrade, abre a engine com FK ativa por
        conexão e oferece sessões novas para verificar durabilidade externa.
        """
        verificar_revisoes_unicas()
        saida = await self.executar_alembic("heads")
        heads = [linha.split()[0] for linha in saida.splitlines() if "(head)" in linha]
        if len(heads) > 1:
            raise SkipTest(
                "grafo Alembic preexistente com múltiplas heads: " + ", ".join(heads)
            )
        if len(heads) != 1 or "warning" in saida.lower():
            raise AssertionError("Alembic deve fornecer uma head inequívoca sem warnings")
        self.head = heads[0]
        self.saida_migrations = await self.executar_alembic("upgrade", "head")
        self.engine = create_async_engine(self.url, hide_parameters=True)
        event.listen(self.engine.sync_engine, "connect", ativar_chaves_estrangeiras)
        self.sessoes = async_sessionmaker(self.engine, expire_on_commit=False)

    async def inspecionar_schema(self) -> dict:
        """Inspeciona versão, usuários, sessões e FK no banco realmente migrado.

        Amplia a inspeção herdada pela conexão SQL para provar a preparação do
        cenário sem usar metadata.create_all ou fixar uma revisão de produto.
        """
        schema = await super().inspecionar_schema()
        async with self.engine.connect() as conexao:
            schema["usuarios"] = await conexao.run_sync(ler_colunas_usuario)
            schema["fk_ativa"] = (await conexao.exec_driver_sql("PRAGMA foreign_keys")).scalar()
        return schema

    async def ler_usuario(self, usuario_id: UUID) -> dict:
        """Relê todas as colunas de uma conta em outra sessão de banco.

        Seleciona a linha por UUID e retorna valores primitivos apenas em memória
        para conferir persistência sem reutilizar o identity map da escrita.
        """
        async with self.sessoes() as sessao:
            resultado = await sessao.execute(
                select(UsuarioRegistro.__table__).where(UsuarioRegistro.id == usuario_id)
            )
            return dict(resultado.mappings().one())

    async def ler_sessoes(self, usuario_id: UUID) -> tuple[dict, ...]:
        """Relê metadados das sessões de uma conta por conexão de leitura nova.

        Filtra pelo UUID e devolve linhas ordenadas sem token em claro para
        conferir emissão, preservação e ausência de sessões extras no cenário.
        """
        async with self.sessoes() as sessao:
            resultado = await sessao.execute(
                select(SessaoRegistro.__table__)
                .where(SessaoRegistro.usuario_id == usuario_id)
                .order_by(SessaoRegistro.id)
            )
            return tuple(dict(linha) for linha in resultado.mappings())

    async def requisitar(
        self, metodo: str, caminho: str, *, dados: dict | None = None,
        token: str | None = None,
    ) -> RespostaCredenciais:
        """Executa HTTP com casos, autenticação, hash e repositórios reais.

        Compõe a fábrica em sessão nova, delega o transporte ao ASGI existente
        e confirma no harness após resposta; rollback redigido evita falsa prova
        de transação produtiva e exposição de segredos em falhas de infraestrutura.
        """
        async with self.sessoes() as sessao:
            usuarios = RepositorioUsuarioSqlAlchemy(sessao)
            sessoes = RepositorioSessaoSqlAlchemy(sessao)
            derivador = DerivadorSenhaScrypt()
            observadores = {
                "consulta": ObservadorCasoPerfil(ConsultarPerfilEstudante(usuarios)),
                "edicao": ObservadorCasoPerfil(EditarPerfil(usuarios)),
                "completo": ObservadorCasoPerfil(AtualizarPerfilCompleto(usuarios)),
                "exclusao": ObservadorCasoPerfil(ExcluirPerfil(usuarios, RelogioUTC())),
            }
            app = create_app(
                cadastrar_estudante=CadastrarEstudante(usuarios, GeradorUsuarioIdUUID4()),
                acessar_estudante=AcessarEstudante(usuarios, derivador),
                derivador_senha=derivador,
                criador_sessao=CriadorSessaoSeguro(sessoes),
                autenticador_sessao=AutenticadorSessaoPersistida(sessoes),
                consultar_perfil=observadores["consulta"],
                editar_perfil=observadores["edicao"],
                atualizar_perfil_completo=observadores["completo"],
                excluir_perfil=observadores["exclusao"],
            )
            try:
                resposta = await solicitar_asgi(app, metodo, caminho, dados=dados, token=token)
                await sessao.commit()
            except Exception:
                await sessao.rollback()
                raise RuntimeError("Falha HTTP/transacional integrada [REDACTED]") from None
            finally:
                self.chamadas_perfil = {
                    nome: tuple(observador.identidades)
                    for nome, observador in observadores.items()
                }
        return resposta


def ler_colunas_usuario(conexao) -> set[str]:
    """Lê nomes das colunas de usuários pelo inspetor da conexão migrada.

    Usa a ponte síncrona do SQLAlchemy para obter DDL real e demonstrar que os
    campos exercitados pelo cenário existem sem gerar schema a partir do ORM.
    """
    return {coluna["name"] for coluna in inspect(conexao).get_columns("usuarios")}
