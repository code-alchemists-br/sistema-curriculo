"""Lê os itens profissionais salvos no banco para a IA recomendar o modelo.

Nome, e-mail, telefone, endereço e links não são lidos: a IA só precisa do
conteúdo profissional, e dados pessoais não devem sair do sistema sem motivo.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.recomendacao_modelo import InformacaoPerfil, LeitorPerfil
from backend.infrastructure.persistence.sqlalchemy.certificacao import (
    CertificacaoRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.competencia import (
    CompetenciaRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.curso import CursoRegistro
from backend.infrastructure.persistence.sqlalchemy.experiencia_profissional import (
    ExperienciaProfissionalRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.formacao_academica import (
    FormacaoAcademicaRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.idioma import IdiomaRegistro
from backend.infrastructure.persistence.sqlalchemy.projeto_academico import (
    ProjetoAcademicoRegistro,
)
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro


class LeitorPerfilSqlAlchemy(LeitorPerfil):
    """Lê do banco o perfil profissional do estudante para a recomendação.

    O adaptador descreve formação, experiências, projetos, competências,
    idiomas, cursos e certificações como pares pergunta/resposta, ignorando
    itens excluídos e dados pessoais. Existe para implementar a porta
    ``LeitorPerfil`` sobre SQLAlchemy.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        """Recebe a fábrica de sessões usada nas leituras.

        Cada leitura abre e fecha a própria sessão. Existe para que o leitor
        não dependa do ciclo transacional de outras operações.
        """
        self._sessoes = sessoes

    async def informacoes(self, usuario_id: UUID) -> list[InformacaoPerfil]:
        """Lista os itens profissionais ativos do estudante como texto.

        Consulta cada tabela do perfil filtrando pelo dono e, quando existe,
        por ``deleted_at`` nulo; do Lattes só informa que existe. Existe para
        dar à IA o conteúdo profissional sem expor dados pessoais.
        """
        async with self._sessoes() as s:

            async def do_usuario(modelo):
                """Busca os registros ativos do estudante em uma tabela do perfil.

                Filtra pelo dono e ignora excluídos logicamente. Existe para
                reaproveitar a mesma consulta em todas as tabelas.
                """
                consulta = select(modelo).where(modelo.usuario_id == usuario_id)
                if hasattr(modelo, "deleted_at"):
                    consulta = consulta.where(modelo.deleted_at.is_(None))
                return (await s.scalars(consulta)).all()

            r: list[InformacaoPerfil] = []
            usuario = await s.get(UsuarioRegistro, usuario_id)
            if usuario is not None and usuario.curriculo_lattes:
                r.append(InformacaoPerfil("Currículo Lattes", "Informado"))
            for f in await do_usuario(FormacaoAcademicaRegistro):
                r.append(InformacaoPerfil(
                    "Formação",
                    f"{f.nivel} em {f.curso}, {f.instituicao}, {f.status}, "
                    f"{_periodo(f.data_inicio, f.data_fim)}",
                ))
            for e in await do_usuario(ExperienciaProfissionalRegistro):
                r.append(InformacaoPerfil(
                    "Experiência",
                    f"{e.cargo} na {e.empresa}, {_periodo(e.data_inicio, e.data_fim)}: {e.descricao}",
                ))
            for p in await do_usuario(ProjetoAcademicoRegistro):
                r.append(InformacaoPerfil("Projeto", f"{p.titulo} ({p.tecnologias}): {p.descricao}"))
            for c in await do_usuario(CompetenciaRegistro):
                r.append(InformacaoPerfil(f"Competência ({c.categoria})", f"{c.descricao} ({c.nivel})"))
            for i in await do_usuario(IdiomaRegistro):
                r.append(InformacaoPerfil("Idioma", f"{i.idioma} ({i.nivel})"))
            for c in await do_usuario(CursoRegistro):
                r.append(InformacaoPerfil("Curso", f"{c.nome}, {c.instituicao}"))
            for c in await do_usuario(CertificacaoRegistro):
                r.append(InformacaoPerfil("Certificação", f"{c.nome}, {c.organizacao_emissora}"))
            return r


def _periodo(inicio, fim) -> str:
    """Formata um período como "mm/aaaa a mm/aaaa" ou "desde mm/aaaa".

    Sem data final, o período é tratado como em andamento. Existe para que a
    IA perceba duração e atualidade de cada item do perfil.
    """
    if fim is None:
        return f"desde {inicio:%m/%Y}"
    return f"{inicio:%m/%Y} a {fim:%m/%Y}"
