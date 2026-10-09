"""Fornece perfis híbridos para testes integrados do backend.

Usuários e currículos são persistidos e lidos por SQLAlchemy em SQLite;
formações e experiências são reconstruídas como entidades válidas em memória.
O módulo existe para preparar cenários repetíveis sem alegar persistência de
itens que ainda não possuem mapping.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

# Proveniência: decision-analysis prompts/backend/20261009-160234-dados-reutilizaveis-perfis-testes-integracao-e2e-v003.md#v003
from backend.domain import (
    Curriculo,
    CurriculoId,
    Email,
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    FormacaoAcademica,
    FormacaoAcademicaId,
    HashSenha,
    Nome,
    Periodo,
    ReferenciaCurriculo,
    Usuario,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.curriculo import (
    CurriculoRegistro,
    para_curriculo,
    para_registro as curriculo_para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.usuario import (
    UsuarioRegistro,
    para_registro as usuario_para_registro,
    para_usuario,
)

ID_ESTUDANTE_ANA = UUID("10000000-0000-4000-8000-000000000001")
ID_ESTUDANTE_BRUNO = UUID("10000000-0000-4000-8000-000000000002")
ID_CURRICULO_ANA_COMPLETO = UUID("20000000-0000-4000-8000-000000000001")
ID_CURRICULO_ANA_BORDA = UUID("20000000-0000-4000-8000-000000000002")
ID_CURRICULO_BRUNO = UUID("20000000-0000-4000-8000-000000000003")

_ID_FORMACAO_ANA = UUID("30000000-0000-4000-8000-000000000001")
_ID_EXPERIENCIA_ANA = UUID("40000000-0000-4000-8000-000000000001")
_ID_FORMACAO_BRUNO = UUID("30000000-0000-4000-8000-000000000002")
_ID_EXPERIENCIA_BRUNO = UUID("40000000-0000-4000-8000-000000000002")
_CURRICULOS_COM_ITENS = {ID_CURRICULO_ANA_COMPLETO, ID_CURRICULO_BRUNO}


@dataclass(frozen=True, slots=True)
class PerfilIntegracaoFake:
    """Agrupa os dados de um estudante para cenários integrados.

    A estrutura mantém o usuário e os currículos recuperados do banco junto às
    entidades de formação e experiência construídas em memória. Ela existe para
    deixar explícita a origem de cada dado ao compartilhar o cenário entre testes.
    """

    usuario: Usuario
    formacao_academica: FormacaoAcademica
    experiencia_profissional: ExperienciaProfissional
    curriculos: tuple[Curriculo, ...]
    curriculo_selecionado_id: UUID | None = None


def popular_perfis_fake(session: Session) -> None:
    """Insere os usuários e currículos fake na sessão SQLite recebida.

    A função converte agregados de domínio com identificadores fixos para os
    mappings SQLAlchemy atuais e deixa commit/rollback sob controle do teste.
    Ela existe para fornecer perfis repetíveis sem criar tabelas ou migrations.
    Deve ser chamada em banco vazio; uma segunda inserção é recusada pelas
    constraints normais do schema.
    """

    perfis = _criar_perfis_de_seed()
    session.add_all(usuario_para_registro(perfil.usuario) for perfil in perfis)
    session.flush()
    for perfil in perfis:
        session.add_all(curriculo_para_registro(curriculo) for curriculo in perfil.curriculos)
    session.flush()


def ler_perfis_fake(session: Session) -> tuple[PerfilIntegracaoFake, ...]:
    """Lê os perfis seedados do SQLite e compõe as entidades ainda não persistidas.

    A função consulta usuários e currículos com SQLAlchemy, converte os registros
    aos agregados de domínio e associa formação/experiência válidas em memória.
    Ela existe para injetar uma visão de cenário reutilizável nos testes sem
    sugerir que as entidades sem mapping foram lidas do banco.
    """

    ids_fakes = (ID_ESTUDANTE_ANA, ID_ESTUDANTE_BRUNO)
    registros_usuario = session.scalars(
        select(UsuarioRegistro).where(UsuarioRegistro.id.in_(ids_fakes)).order_by(UsuarioRegistro.id)
    ).all()
    perfis: list[PerfilIntegracaoFake] = []
    for registro_usuario in registros_usuario:
        usuario = para_usuario(registro_usuario)
        formacao, experiencia = _criar_itens_em_memoria(usuario.id)
        registros_curriculo = session.scalars(
            select(CurriculoRegistro)
            .where(CurriculoRegistro.usuario_id == usuario.id.valor)
            .order_by(CurriculoRegistro.id)
        ).all()
        curriculos = tuple(_com_referencias_de_cenario(para_curriculo(item), formacao, experiencia) for item in registros_curriculo)
        perfis.append(
            PerfilIntegracaoFake(
                usuario=usuario,
                formacao_academica=formacao,
                experiencia_profissional=experiencia,
                curriculos=curriculos,
            )
        )
    return tuple(perfis)


def _criar_perfis_de_seed() -> tuple[PerfilIntegracaoFake, ...]:
    """Monta dois estudantes válidos e três currículos determinísticos.

    O primeiro estudante recebe uma versão completa e uma versão sem itens; o
    segundo recebe uma versão própria para servir de dado de outro proprietário.
    A composição é feita só com objetos de domínio e existe como fonte estável
    para a gravação SQLite da fixture.
    """

    dados_ana = _criar_dados_estudante(
        ID_ESTUDANTE_ANA,
        _ID_FORMACAO_ANA,
        _ID_EXPERIENCIA_ANA,
        "Ana Exemplo",
        "ana@example.test",
    )
    dados_bruno = _criar_dados_estudante(
        ID_ESTUDANTE_BRUNO,
        _ID_FORMACAO_BRUNO,
        _ID_EXPERIENCIA_BRUNO,
        "Bruno Exemplo",
        "bruno@example.test",
    )
    ana_completo = _criar_curriculo(
        ID_CURRICULO_ANA_COMPLETO,
        dados_ana.usuario.id,
        "Currículo completo de teste",
    )
    ana_borda = _criar_curriculo(
        ID_CURRICULO_ANA_BORDA,
        dados_ana.usuario.id,
        "Currículo sem itens selecionados",
    )
    bruno_curriculo = _criar_curriculo(
        ID_CURRICULO_BRUNO,
        dados_bruno.usuario.id,
        "Currículo de outro estudante",
    )
    return (
        PerfilIntegracaoFake(
            dados_ana.usuario,
            dados_ana.formacao_academica,
            dados_ana.experiencia_profissional,
            (ana_completo, ana_borda),
        ),
        PerfilIntegracaoFake(
            dados_bruno.usuario,
            dados_bruno.formacao_academica,
            dados_bruno.experiencia_profissional,
            (bruno_curriculo,),
        ),
    )


def _criar_dados_estudante(
    usuario_id: UUID,
    formacao_id: UUID,
    experiencia_id: UUID,
    nome: str,
    email: str,
) -> PerfilIntegracaoFake:
    """Constrói usuário, formação e experiência coerentes para um proprietário.

    A função usa IDs fornecidos e períodos fixos, criando o usuário com hash
    sintético e entidades de perfil válidas em memória. Ela existe para manter
    os três conceitos associados antes de seedar apenas o subconjunto persistido.
    """

    dono = UsuarioId(usuario_id)
    usuario = Usuario(
        id=dono,
        nome=Nome(nome),
        email=Email(email),
        hash_senha=HashSenha("hash-fake-nao-utilizavel-em-autenticacao"),
    )
    formacao = FormacaoAcademica(
        id=FormacaoAcademicaId(formacao_id),
        usuario_id=dono,
        instituicao="Instituto de Tecnologia de Exemplo",
        curso="Análise e Desenvolvimento de Sistemas",
        nivel="Graduação tecnológica",
        periodo=Periodo(inicio=date(2023, 2, 1), fim=None),
        status="Em andamento",
    )
    experiencia = ExperienciaProfissional(
        id=ExperienciaProfissionalId(experiencia_id),
        usuario_id=dono,
        empresa="Laboratório de Software de Exemplo",
        cargo="Estagiário de desenvolvimento",
        descricao="Implementação de funcionalidades e testes automatizados.",
        periodo=Periodo(inicio=date(2024, 1, 15), fim=None),
    )
    return PerfilIntegracaoFake(usuario, formacao, experiencia, ())


def _criar_curriculo(curriculo_id: UUID, usuario_id: UsuarioId, titulo: str) -> Curriculo:
    """Cria uma versão válida sem referências persistidas no schema atual.

    O construtor usa identidade estável, layout textual e proprietário tipado.
    Ele existe para fornecer currículos recuperáveis do SQLite, inclusive a
    versão vazia usada como estado de borda válido.
    """

    return Curriculo(
        id=CurriculoId(curriculo_id),
        usuario_id=usuario_id,
        titulo_versao=titulo,
        layout="classico",
        is_public=False,
    )


def _criar_itens_em_memoria(usuario_id: UsuarioId) -> tuple[FormacaoAcademica, ExperienciaProfissional]:
    """Reconstrói formação e experiência para um dos proprietários de teste.

    A função escolhe IDs fixos conforme o usuário e usa os mesmos dados válidos
    empregados pelo seed. Ela existe para compor o perfil após a leitura SQL,
    sem atribuir persistência a entidades sem mapping.
    """

    if usuario_id.valor == ID_ESTUDANTE_ANA:
        formacao_id, experiencia_id = _ID_FORMACAO_ANA, _ID_EXPERIENCIA_ANA
    elif usuario_id.valor == ID_ESTUDANTE_BRUNO:
        formacao_id, experiencia_id = _ID_FORMACAO_BRUNO, _ID_EXPERIENCIA_BRUNO
    else:
        raise ValueError(f"O usuário {usuario_id.valor} não pertence ao conjunto de perfis fake.")
    perfil = _criar_dados_estudante(
        usuario_id.valor,
        formacao_id,
        experiencia_id,
        "Ana Exemplo" if usuario_id.valor == ID_ESTUDANTE_ANA else "Bruno Exemplo",
        "ana@example.test" if usuario_id.valor == ID_ESTUDANTE_ANA else "bruno@example.test",
    )
    return perfil.formacao_academica, perfil.experiencia_profissional


def _com_referencias_de_cenario(
    curriculo: Curriculo,
    formacao: FormacaoAcademica,
    experiencia: ExperienciaProfissional,
) -> Curriculo:
    """Aplica itens em memória às versões completas do cenário.

    Somente IDs de currículos completos recebem referências; a versão de borda
    fica sem itens. A regra representa estados distintos de testes sem persistir
    associações que o mapping de currículo ainda não suporta.
    """

    if curriculo.id.valor in _CURRICULOS_COM_ITENS:
        curriculo.incluir_referencia(ReferenciaCurriculo(formacao.id))
        curriculo.incluir_referencia(ReferenciaCurriculo(experiencia.id))
    return curriculo
