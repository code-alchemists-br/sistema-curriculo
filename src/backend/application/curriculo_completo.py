"""Lê e substitui, por seção, o currículo salvo do estudante.

O frontend preenche o currículo em etapas. Cada etapa envia a lista completa
da sua seção, e a lista salva no banco é trocada por ela. Assim, voltar a uma
etapa e avançar de novo não duplica registros, e o que está no banco é sempre
o que o estudante vê.
"""

from abc import ABC, abstractmethod
from datetime import date
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel

from backend.domain.itens_perfil import (
    CategoriaCompetencia,
    Certificacao,
    Competencia,
    Curso,
    ExperienciaProfissional,
    FormacaoAcademica,
    Idioma,
    NivelFormacaoAcademica,
    ProjetoAcademico,
    StatusFormacaoAcademica,
)
from backend.domain.modelo_curriculo import ModeloCurriculo
from backend.domain.value_objects import (
    CertificacaoId,
    CompetenciaId,
    CursoId,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    IdiomaId,
    Periodo,
    ProjetoAcademicoId,
    UsuarioId,
)


class SecaoCurriculo(StrEnum):
    """Seções do currículo que podem ser substituídas de uma vez."""

    FORMACOES = "formacoes"
    EXPERIENCIAS = "experiencias"
    PROJETOS = "projetos"
    COMPETENCIAS = "competencias"
    IDIOMAS = "idiomas"
    CURSOS = "cursos"
    CERTIFICACOES = "certificacoes"


class FormacaoItem(BaseModel):
    """Formação acadêmica como o frontend envia e recebe."""

    instituicao: str
    curso: str
    nivel: NivelFormacaoAcademica
    status: StatusFormacaoAcademica
    data_inicio: date
    data_fim: date | None = None


class ExperienciaItem(BaseModel):
    """Experiência profissional; sem ``data_fim`` é o emprego atual."""

    empresa: str
    cargo: str
    descricao: str
    data_inicio: date
    data_fim: date | None = None


class ProjetoItem(BaseModel):
    """Projeto acadêmico."""

    titulo: str
    descricao: str
    tecnologias: str


class CompetenciaItem(BaseModel):
    """Competência técnica ou comportamental."""

    categoria: CategoriaCompetencia
    descricao: str
    nivel: str = "padrao"


class IdiomaItem(BaseModel):
    """Idioma e nível de proficiência."""

    idioma: str
    nivel: str


class CursoItem(BaseModel):
    """Curso complementar."""

    nome: str
    instituicao: str
    carga_horaria: int | None = None


class CertificacaoItem(BaseModel):
    """Certificação e organização emissora."""

    nome: str
    organizacao_emissora: str


ITEM_POR_SECAO: dict[SecaoCurriculo, type[BaseModel]] = {
    SecaoCurriculo.FORMACOES: FormacaoItem,
    SecaoCurriculo.EXPERIENCIAS: ExperienciaItem,
    SecaoCurriculo.PROJETOS: ProjetoItem,
    SecaoCurriculo.COMPETENCIAS: CompetenciaItem,
    SecaoCurriculo.IDIOMAS: IdiomaItem,
    SecaoCurriculo.CURSOS: CursoItem,
    SecaoCurriculo.CERTIFICACOES: CertificacaoItem,
}


class DadosPessoaisSalvos(BaseModel):
    """Dados pessoais e de contato gravados na conta."""

    nome: str
    email: str
    endereco: str | None = None
    cidade: str | None = None
    telefones: list[str] = []
    linkedin: str | None = None
    curriculo_lattes: str | None = None


class CurriculoCompleto(BaseModel):
    """Tudo o que o estudante já salvou, pronto para preencher as telas."""

    dados_pessoais: DadosPessoaisSalvos
    formacoes: list[FormacaoItem] = []
    experiencias: list[ExperienciaItem] = []
    projetos: list[ProjetoItem] = []
    competencias: list[CompetenciaItem] = []
    idiomas: list[IdiomaItem] = []
    cursos: list[CursoItem] = []
    certificacoes: list[CertificacaoItem] = []
    modelo: ModeloCurriculo | None = None


class CurriculoNaoEncontrado(Exception):
    """A conta da sessão não existe mais ou foi excluída."""


class DadosRepetidos(Exception):
    """A lista enviada tem itens iguais onde o banco exige itens únicos."""


class RepositorioCurriculoCompleto(ABC):
    """Porta de leitura e gravação do currículo completo."""

    @abstractmethod
    async def ler(self, usuario_id: UUID) -> CurriculoCompleto | None:
        """Devolve o currículo salvo ou ``None`` se a conta não existir."""

    @abstractmethod
    async def substituir(
        self,
        usuario_id: UUID,
        secao: SecaoCurriculo,
        entidades: list,
        curriculo_lattes: str | None = None,
    ) -> None:
        """Troca, numa transação, os itens da seção pelos itens recebidos."""

    @abstractmethod
    async def salvar_modelo(self, usuario_id: UUID, modelo: ModeloCurriculo) -> None:
        """Guarda o modelo visual escolhido para o currículo."""


class GerenciarCurriculoCompleto:
    """Casos de uso de leitura e substituição do currículo do estudante.

    - O que faz: lê o currículo salvo, troca uma seção inteira e guarda o modelo.
    - Como faz: converte cada item recebido em entidade de domínio (que valida
      textos, datas e vocabulários) antes de pedir a troca ao repositório.
    - Qual finalidade atende: o frontend passa a salvar e ler o currículo pelo
      banco, sem duplicar itens a cada vez que o estudante revisita uma etapa.
    """

    def __init__(self, repositorio: RepositorioCurriculoCompleto) -> None:
        self._repositorio = repositorio

    async def consultar(self, usuario_id: UUID) -> CurriculoCompleto:
        """Devolve o currículo salvo da conta da sessão."""
        curriculo = await self._repositorio.ler(usuario_id)
        if curriculo is None:
            raise CurriculoNaoEncontrado("Conta não encontrada.")
        return curriculo

    async def substituir_secao(
        self,
        usuario_id: UUID,
        secao: SecaoCurriculo,
        itens: list[BaseModel],
        curriculo_lattes: str | None = None,
    ) -> None:
        """Valida os itens no domínio e troca a seção salva por eles.

        Lança ``RegraDeDominioViolada`` quando algum item não respeita as regras.
        """
        dono = UsuarioId(usuario_id)
        entidades = [_para_entidade(secao, dono, item) for item in itens]
        await self._repositorio.substituir(usuario_id, secao, entidades, curriculo_lattes)

    async def salvar_modelo(self, usuario_id: UUID, modelo: ModeloCurriculo) -> None:
        """Guarda o modelo visual escolhido."""
        await self._repositorio.salvar_modelo(usuario_id, modelo)


def _para_entidade(secao: SecaoCurriculo, dono: UsuarioId, item: BaseModel):
    """Cria a entidade de domínio da seção, que valida e normaliza o item."""
    match secao:
        case SecaoCurriculo.FORMACOES:
            return FormacaoAcademica(
                id=FormacaoAcademicaId(uuid4()),
                usuario_id=dono,
                instituicao=item.instituicao,
                curso=item.curso,
                nivel=item.nivel,
                periodo=Periodo(item.data_inicio, item.data_fim),
                status=item.status,
            )
        case SecaoCurriculo.EXPERIENCIAS:
            return ExperienciaProfissional.criar_para_gravacao(
                id=ExperienciaProfissionalId(uuid4()),
                usuario_id=dono,
                empresa=item.empresa,
                cargo=item.cargo,
                descricao=item.descricao,
                periodo=Periodo(item.data_inicio, item.data_fim),
                hoje=date.today(),
            )
        case SecaoCurriculo.PROJETOS:
            return ProjetoAcademico(
                id=ProjetoAcademicoId(uuid4()),
                usuario_id=dono,
                titulo=item.titulo,
                descricao=item.descricao,
                tecnologias=item.tecnologias,
            )
        case SecaoCurriculo.COMPETENCIAS:
            return Competencia(
                id=CompetenciaId(uuid4()),
                usuario_id=dono,
                categoria=item.categoria,
                descricao=item.descricao,
                nivel=item.nivel,
            )
        case SecaoCurriculo.IDIOMAS:
            return Idioma(id=IdiomaId(uuid4()), usuario_id=dono, idioma=item.idioma, nivel=item.nivel)
        case SecaoCurriculo.CURSOS:
            return Curso(
                id=CursoId(uuid4()),
                usuario_id=dono,
                nome=item.nome,
                instituicao=item.instituicao,
                carga_horaria=item.carga_horaria,
            )
        case SecaoCurriculo.CERTIFICACOES:
            return Certificacao(
                id=CertificacaoId(uuid4()),
                usuario_id=dono,
                nome=item.nome,
                organizacao_emissora=item.organizacao_emissora,
            )
