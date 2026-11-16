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


class SecaoSubstituivel(StrEnum):
    """Enumera as seções do currículo que podem ser substituídas de uma vez.

    O valor de cada membro é o trecho usado na rota ``PUT .../{secao}`` e chave
    do mapeamento para o modelo de item. O enum existe para recusar seções
    desconhecidas já na fronteira HTTP.
    """

    FORMACOES = "formacoes"
    EXPERIENCIAS = "experiencias"
    PROJETOS = "projetos"
    COMPETENCIAS = "competencias"
    IDIOMAS = "idiomas"
    CURSOS = "cursos"
    CERTIFICACOES = "certificacoes"


class FormacaoItem(BaseModel):
    """Representa uma formação acadêmica como o frontend envia e recebe.

    O DTO valida tipos e vocabulários (nível e status) na fronteira; as regras
    de texto e período ficam na entidade ``FormacaoAcademica``. Existe para
    transportar a seção de formações sem expor a entidade de domínio.
    """

    instituicao: str
    curso: str
    nivel: NivelFormacaoAcademica
    status: StatusFormacaoAcademica
    data_inicio: date
    data_fim: date | None = None


class ExperienciaItem(BaseModel):
    """Representa uma experiência profissional como o frontend envia e recebe.

    Sem ``data_fim``, a experiência é o emprego atual; as regras de período e
    de datas futuras ficam na entidade ``ExperienciaProfissional``. Existe para
    transportar a seção de experiências sem expor a entidade de domínio.
    """

    empresa: str
    cargo: str
    descricao: str
    data_inicio: date
    data_fim: date | None = None


class ProjetoItem(BaseModel):
    """Representa um projeto acadêmico como o frontend envia e recebe.

    O DTO carrega título, descrição e tecnologias; tamanhos e conteúdo são
    validados pela entidade ``ProjetoAcademico``. Existe para transportar a
    seção de projetos sem expor a entidade de domínio.
    """

    titulo: str
    descricao: str
    tecnologias: str


class CompetenciaItem(BaseModel):
    """Representa uma competência técnica ou comportamental.

    A categoria é validada pelo enum do domínio e o nível tem valor padrão,
    pois a tela não pede nível. Existe para transportar a seção de
    competências sem expor a entidade de domínio.
    """

    categoria: CategoriaCompetencia
    descricao: str
    nivel: str = "padrao"


class IdiomaItem(BaseModel):
    """Representa um idioma e o nível de proficiência do estudante.

    O DTO carrega os textos recebidos; normalização e obrigatoriedade ficam na
    entidade ``Idioma``. Existe para transportar a seção de idiomas sem expor
    a entidade de domínio.
    """

    idioma: str
    nivel: str


class CursoItem(BaseModel):
    """Representa um curso complementar e sua carga horária opcional.

    O DTO valida o tipo da carga horária; nome e instituição são validados pela
    entidade ``Curso``. Existe para transportar a seção de cursos sem expor a
    entidade de domínio.
    """

    nome: str
    instituicao: str
    carga_horaria: int | None = None


class CertificacaoItem(BaseModel):
    """Representa uma certificação e a organização que a emitiu.

    O DTO carrega os textos recebidos; normalização e obrigatoriedade ficam na
    entidade ``Certificacao``. Existe para transportar a seção de
    certificações sem expor a entidade de domínio.
    """

    nome: str
    organizacao_emissora: str


ITEM_POR_SECAO: dict[SecaoSubstituivel, type[BaseModel]] = {
    SecaoSubstituivel.FORMACOES: FormacaoItem,
    SecaoSubstituivel.EXPERIENCIAS: ExperienciaItem,
    SecaoSubstituivel.PROJETOS: ProjetoItem,
    SecaoSubstituivel.COMPETENCIAS: CompetenciaItem,
    SecaoSubstituivel.IDIOMAS: IdiomaItem,
    SecaoSubstituivel.CURSOS: CursoItem,
    SecaoSubstituivel.CERTIFICACOES: CertificacaoItem,
}


class DadosPessoaisSalvos(BaseModel):
    """Representa os dados pessoais e de contato gravados na conta.

    O DTO é só de leitura: a gravação continua em ``PUT /estudantes/me/perfil``.
    Existe para que a tela preencha os dados pessoais a partir do banco ao
    abrir o sistema.
    """

    nome: str
    email: str
    endereco: str | None = None
    cidade: str | None = None
    telefones: list[str] = []
    linkedin: str | None = None
    curriculo_lattes: str | None = None


class CurriculoCompleto(BaseModel):
    """Reúne tudo o que o estudante já salvou, pronto para preencher as telas.

    O DTO agrupa dados pessoais, cada seção do currículo e o modelo escolhido
    (``None`` quando ainda não há). Existe para que o frontend carregue o
    currículo inteiro do banco numa única chamada.
    """

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
    """Sinaliza que a conta da sessão não existe mais ou foi excluída.

    A exceção é traduzida pela API em não encontrado (404). Existe para não
    devolver um currículo vazio para uma conta que deixou de existir.
    """


class DadosRepetidos(Exception):
    """Sinaliza itens repetidos onde o banco exige itens únicos.

    Competências, idiomas, cursos e certificações não aceitam duplicatas por
    estudante; a exceção é traduzida pela API em conflito (409). Existe para
    explicar a recusa sem expor o erro de integridade do banco.
    """


class RepositorioCurriculoCompleto(ABC):
    """Define a porta de leitura e gravação do currículo completo.

    Implementações leem todas as seções da conta e trocam uma seção inteira
    numa transação. A porta existe para que o caso de uso não dependa do ORM.
    """

    @abstractmethod
    async def ler(self, usuario_id: UUID) -> CurriculoCompleto | None:
        """Lê o currículo salvo do estudante.

        Devolve ``None`` quando a conta não existe ou foi excluída. Existe para
        o caso de uso decidir como tratar a ausência da conta.
        """

    @abstractmethod
    async def substituir(
        self,
        usuario_id: UUID,
        secao: SecaoSubstituivel,
        entidades: list,
        curriculo_lattes: str | None = None,
    ) -> None:
        """Troca, numa transação, os itens da seção pelas entidades recebidas.

        Os itens atuais são removidos e os novos gravados juntos; se algo
        falhar, nada muda. Na seção de formações também grava o Lattes. Lança
        ``DadosRepetidos`` em violação de unicidade. Existe para que salvar de
        novo uma etapa substitua os itens em vez de duplicá-los.
        """

    @abstractmethod
    async def salvar_modelo(self, usuario_id: UUID, modelo: ModeloCurriculo) -> None:
        """Guarda o modelo visual escolhido para o currículo.

        Cria o currículo do estudante na primeira vez e só atualiza o modelo
        nas seguintes. Existe para que o modelo escolhido sobreviva entre
        sessões e dispositivos.
        """


class GerenciarCurriculoCompleto:
    """Casos de uso de leitura e substituição do currículo do estudante.

    - O que faz: lê o currículo salvo, troca uma seção inteira e guarda o modelo.
    - Como faz: converte cada item recebido em entidade de domínio (que valida
      textos, datas e vocabulários) antes de pedir a troca ao repositório.
    - Qual finalidade atende: o frontend passa a salvar e ler o currículo pelo
      banco, sem duplicar itens a cada vez que o estudante revisita uma etapa.
    """

    def __init__(self, repositorio: RepositorioCurriculoCompleto) -> None:
        """Recebe a porta de persistência do currículo completo.

        A dependência é injetada pela composição, o que permite usar um double
        em testes. Existe para manter os casos de uso independentes do ORM.
        """
        self._repositorio = repositorio

    async def consultar(self, usuario_id: UUID) -> CurriculoCompleto:
        """Devolve o currículo salvo da conta da sessão.

        Lança ``CurriculoNaoEncontrado`` quando a conta não existe mais. Existe
        para que o frontend preencha as telas a partir do banco.
        """
        curriculo = await self._repositorio.ler(usuario_id)
        if curriculo is None:
            raise CurriculoNaoEncontrado("Conta não encontrada.")
        return curriculo

    async def substituir_secao(
        self,
        usuario_id: UUID,
        secao: SecaoSubstituivel,
        itens: list[BaseModel],
        curriculo_lattes: str | None = None,
    ) -> None:
        """Valida os itens no domínio e troca a seção salva por eles.

        Converte cada item na entidade da seção (que valida e normaliza) antes
        de qualquer gravação, então um item inválido impede a troca inteira.
        Lança ``RegraDeDominioViolada`` quando algum item não respeita as
        regras. Existe para salvar uma etapa do currículo sem duplicar itens.
        """
        dono = UsuarioId(usuario_id)
        entidades = [_para_entidade(secao, dono, item) for item in itens]
        await self._repositorio.substituir(usuario_id, secao, entidades, curriculo_lattes)

    async def salvar_modelo(self, usuario_id: UUID, modelo: ModeloCurriculo) -> None:
        """Guarda o modelo visual escolhido para o currículo do estudante.

        Delega ao repositório, que cria ou atualiza o currículo. Existe para
        que a escolha feita na tela de modelos seja persistida.
        """
        await self._repositorio.salvar_modelo(usuario_id, modelo)


def _para_entidade(secao: SecaoSubstituivel, dono: UsuarioId, item: BaseModel):
    """Cria a entidade de domínio correspondente a um item da seção.

    Gera uma identidade nova e chama o construtor (ou fábrica) da entidade, que
    valida e normaliza os dados; experiências também recusam datas futuras.
    Existe para que toda gravação passe pelas regras do domínio.
    """
    match secao:
        case SecaoSubstituivel.FORMACOES:
            return FormacaoAcademica(
                id=FormacaoAcademicaId(uuid4()),
                usuario_id=dono,
                instituicao=item.instituicao,
                curso=item.curso,
                nivel=item.nivel,
                periodo=Periodo(item.data_inicio, item.data_fim),
                status=item.status,
            )
        case SecaoSubstituivel.EXPERIENCIAS:
            return ExperienciaProfissional.criar_para_gravacao(
                id=ExperienciaProfissionalId(uuid4()),
                usuario_id=dono,
                empresa=item.empresa,
                cargo=item.cargo,
                descricao=item.descricao,
                periodo=Periodo(item.data_inicio, item.data_fim),
                hoje=date.today(),
            )
        case SecaoSubstituivel.PROJETOS:
            return ProjetoAcademico(
                id=ProjetoAcademicoId(uuid4()),
                usuario_id=dono,
                titulo=item.titulo,
                descricao=item.descricao,
                tecnologias=item.tecnologias,
            )
        case SecaoSubstituivel.COMPETENCIAS:
            return Competencia(
                id=CompetenciaId(uuid4()),
                usuario_id=dono,
                categoria=item.categoria,
                descricao=item.descricao,
                nivel=item.nivel,
            )
        case SecaoSubstituivel.IDIOMAS:
            return Idioma(id=IdiomaId(uuid4()), usuario_id=dono, idioma=item.idioma, nivel=item.nivel)
        case SecaoSubstituivel.CURSOS:
            return Curso(
                id=CursoId(uuid4()),
                usuario_id=dono,
                nome=item.nome,
                instituicao=item.instituicao,
                carga_horaria=item.carga_horaria,
            )
        case SecaoSubstituivel.CERTIFICACOES:
            return Certificacao(
                id=CertificacaoId(uuid4()),
                usuario_id=dono,
                nome=item.nome,
                organizacao_emissora=item.organizacao_emissora,
            )
