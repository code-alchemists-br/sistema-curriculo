"""Lê e substitui o currículo completo do estudante no banco relacional."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.curriculo_completo import (
    CertificacaoItem,
    CompetenciaItem,
    CurriculoCompleto,
    CursoItem,
    DadosPessoaisSalvos,
    DadosRepetidos,
    ExperienciaItem,
    FormacaoItem,
    IdiomaItem,
    ProjetoItem,
    RepositorioCurriculoCompleto,
    SecaoCurriculo,
)
from backend.domain.modelo_curriculo import ModeloCurriculo
from backend.infrastructure.persistence.sqlalchemy import (
    certificacao,
    competencia,
    curso,
    experiencia_profissional,
    formacao_academica,
    idioma,
    projeto_academico,
)
from backend.infrastructure.persistence.sqlalchemy.curriculo import CurriculoRegistro
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro

# Tabela e conversor de entidade → registro de cada seção.
_MAPEAMENTO = {
    SecaoCurriculo.FORMACOES: (formacao_academica.FormacaoAcademicaRegistro, formacao_academica.para_registro),
    SecaoCurriculo.EXPERIENCIAS: (
        experiencia_profissional.ExperienciaProfissionalRegistro,
        experiencia_profissional.para_registro,
    ),
    SecaoCurriculo.PROJETOS: (projeto_academico.ProjetoAcademicoRegistro, projeto_academico.para_registro),
    SecaoCurriculo.COMPETENCIAS: (competencia.CompetenciaRegistro, competencia.para_registro),
    SecaoCurriculo.IDIOMAS: (idioma.IdiomaRegistro, idioma.para_registro),
    SecaoCurriculo.CURSOS: (curso.CursoRegistro, curso.para_registro),
    SecaoCurriculo.CERTIFICACOES: (certificacao.CertificacaoRegistro, certificacao.para_registro),
}


class RepositorioCurriculoCompletoSqlAlchemy(RepositorioCurriculoCompleto):
    """Implementa a porta do currículo completo com SQLAlchemy.

    - O que faz: lê todas as seções da conta e troca uma seção inteira por vez.
    - Como faz: na troca, abre uma transação, remove os itens atuais (exclusão
      lógica nas tabelas que têm ``deleted_at``, física nas demais) e insere os
      novos registros; se algo falhar, nada é gravado.
    - Qual finalidade atende: manter o banco igual ao que o estudante vê, sem
      duplicar itens quando uma etapa é salva de novo.
    """

    def __init__(self, sessoes: async_sessionmaker[AsyncSession]) -> None:
        self._sessoes = sessoes

    async def ler(self, usuario_id: UUID) -> CurriculoCompleto | None:
        async with self._sessoes() as s:
            usuario = await s.get(UsuarioRegistro, usuario_id)
            if usuario is None or usuario.deleted_at is not None:
                return None

            async def itens(secao: SecaoCurriculo):
                registro, _ = _MAPEAMENTO[secao]
                consulta = select(registro).where(registro.usuario_id == usuario_id)
                if hasattr(registro, "deleted_at"):
                    consulta = consulta.where(registro.deleted_at.is_(None))
                if hasattr(registro, "data_inicio"):
                    consulta = consulta.order_by(registro.data_inicio.desc())
                return (await s.scalars(consulta)).all()

            curriculo = await s.scalar(
                select(CurriculoRegistro).where(CurriculoRegistro.usuario_id == usuario_id).limit(1)
            )
            return CurriculoCompleto(
                dados_pessoais=DadosPessoaisSalvos(
                    nome=usuario.nome,
                    email=usuario.email,
                    endereco=usuario.endereco,
                    cidade=usuario.cidade,
                    telefones=[t for t in (usuario.telefones or []) if t != "Não informado"],
                    linkedin=usuario.linkedin,
                    curriculo_lattes=usuario.curriculo_lattes,
                ),
                formacoes=[
                    FormacaoItem(
                        instituicao=f.instituicao,
                        curso=f.curso,
                        nivel=f.nivel,
                        status=f.status,
                        data_inicio=f.data_inicio,
                        data_fim=f.data_fim,
                    )
                    for f in await itens(SecaoCurriculo.FORMACOES)
                ],
                experiencias=[
                    ExperienciaItem(
                        empresa=e.empresa,
                        cargo=e.cargo,
                        descricao=e.descricao,
                        data_inicio=e.data_inicio,
                        data_fim=e.data_fim,
                    )
                    for e in await itens(SecaoCurriculo.EXPERIENCIAS)
                ],
                projetos=[
                    ProjetoItem(titulo=p.titulo, descricao=p.descricao, tecnologias=p.tecnologias)
                    for p in await itens(SecaoCurriculo.PROJETOS)
                ],
                competencias=[
                    CompetenciaItem(categoria=c.categoria, descricao=c.descricao, nivel=c.nivel)
                    for c in await itens(SecaoCurriculo.COMPETENCIAS)
                ],
                idiomas=[IdiomaItem(idioma=i.idioma, nivel=i.nivel) for i in await itens(SecaoCurriculo.IDIOMAS)],
                cursos=[
                    CursoItem(nome=c.nome, instituicao=c.instituicao, carga_horaria=c.carga_horaria)
                    for c in await itens(SecaoCurriculo.CURSOS)
                ],
                certificacoes=[
                    CertificacaoItem(nome=c.nome, organizacao_emissora=c.organizacao_emissora)
                    for c in await itens(SecaoCurriculo.CERTIFICACOES)
                ],
                modelo=ModeloCurriculo(curriculo.layout) if curriculo else None,
            )

    async def substituir(
        self,
        usuario_id: UUID,
        secao: SecaoCurriculo,
        entidades: list,
        curriculo_lattes: str | None = None,
    ) -> None:
        registro, para_registro = _MAPEAMENTO[secao]
        try:
            async with self._sessoes.begin() as s:
                if hasattr(registro, "deleted_at"):
                    await s.execute(
                        update(registro)
                        .where(registro.usuario_id == usuario_id, registro.deleted_at.is_(None))
                        .values(deleted_at=datetime.now(timezone.utc))
                    )
                else:
                    await s.execute(delete(registro).where(registro.usuario_id == usuario_id))
                s.add_all(para_registro(e) for e in entidades)
                if secao is SecaoCurriculo.FORMACOES:
                    await s.execute(
                        update(UsuarioRegistro)
                        .where(UsuarioRegistro.id == usuario_id)
                        .values(curriculo_lattes=curriculo_lattes)
                    )
        except IntegrityError as erro:
            raise DadosRepetidos("Há itens repetidos na lista enviada.") from erro

    async def salvar_modelo(self, usuario_id: UUID, modelo: ModeloCurriculo) -> None:
        async with self._sessoes.begin() as s:
            curriculo = await s.scalar(
                select(CurriculoRegistro).where(CurriculoRegistro.usuario_id == usuario_id).limit(1)
            )
            if curriculo is None:
                s.add(
                    CurriculoRegistro(
                        id=uuid4(),
                        usuario_id=usuario_id,
                        titulo_versao="Currículo principal",
                        layout=modelo.value,
                        is_public=False,
                    )
                )
            else:
                curriculo.layout = modelo.value
