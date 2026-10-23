"""Define o documento renderizado do currículo, independente do formato de exportação.

O módulo descreve, apenas com textos já formatados, tudo o que um arquivo de
currículo precisa mostrar (cabeçalho do estudante e seções com seus blocos) e
monta esse documento a partir da prévia da versão. Ele existe para que os
geradores de PDF e DOCX desenhem exatamente o mesmo conteúdo da visualização
(RF09, CT-RF09-03), sem conhecer entidades de domínio nem repetir regras de
seleção, ordenação ou formatação.
"""

import re
import unicodedata
from dataclasses import dataclass
from datetime import date

from backend.application.previa_versao_curriculo import PreviaVersaoCurriculo
from backend.domain.itens_perfil import (
    CategoriaCompetencia,
    Competencia,
    Documento,
    ExperienciaProfissional,
    FormacaoAcademica,
    Idioma,
    NivelFormacaoAcademica,
    ProjetoAcademico,
    StatusFormacaoAcademica,
)
from backend.domain.secao_curriculo import SecaoCurriculo
from backend.domain.value_objects import Cidade, Periodo

TITULOS_SECOES: dict[SecaoCurriculo, str] = {
    SecaoCurriculo.FORMACAO_ACADEMICA: "Formação acadêmica",
    SecaoCurriculo.EXPERIENCIAS_PROFISSIONAIS: "Experiência profissional",
    SecaoCurriculo.PROJETOS_ACADEMICOS: "Projetos acadêmicos",
    SecaoCurriculo.COMPETENCIAS: "Competências",
    SecaoCurriculo.IDIOMAS: "Idiomas",
    SecaoCurriculo.DOCUMENTOS_COMPLEMENTARES: "Documentos complementares",
}

ROTULOS_NIVEL_FORMACAO: dict[NivelFormacaoAcademica, str] = {
    NivelFormacaoAcademica.ENSINO_FUNDAMENTAL: "Ensino fundamental",
    NivelFormacaoAcademica.ENSINO_MEDIO: "Ensino médio",
    NivelFormacaoAcademica.TECNICO: "Técnico",
    NivelFormacaoAcademica.TECNOLOGO: "Tecnólogo",
    NivelFormacaoAcademica.GRADUACAO: "Graduação",
    NivelFormacaoAcademica.ESPECIALIZACAO: "Especialização",
    NivelFormacaoAcademica.MESTRADO: "Mestrado",
    NivelFormacaoAcademica.DOUTORADO: "Doutorado",
}

ROTULOS_STATUS_FORMACAO: dict[StatusFormacaoAcademica, str] = {
    StatusFormacaoAcademica.EM_ANDAMENTO: "Em andamento",
    StatusFormacaoAcademica.CONCLUIDO: "Concluído",
    StatusFormacaoAcademica.INTERROMPIDO: "Interrompido",
}

ROTULOS_CATEGORIA_COMPETENCIA: dict[CategoriaCompetencia, str] = {
    CategoriaCompetencia.TECNICA: "Técnica",
    CategoriaCompetencia.COMPORTAMENTAL: "Comportamental",
}

TAMANHO_MAXIMO_NOME_ARQUIVO = 120


@dataclass(frozen=True, slots=True)
class CabecalhoDocumento:
    """Reúne a identificação e os contatos do estudante exibidos no topo do arquivo.

    O DTO guarda apenas textos prontos para exibição, com campos opcionais
    vazios quando o estudante não os informou, sem identificadores internos nem
    credenciais. Ele existe para que todo formato mostre a mesma identificação
    que a prévia apresenta.
    """

    nome: str
    email: str
    telefones: tuple[str, ...] = ()
    endereco: str | None = None
    cidade: str | None = None
    linkedin: str | None = None
    curriculo_lattes: str | None = None


@dataclass(frozen=True, slots=True)
class BlocoDocumento:
    """Representa um item de uma seção já convertido em textos de exibição.

    O DTO tem título, subtítulo e período opcionais e linhas de detalhe, sem
    referência à entidade que o originou. Ele existe para que os geradores de
    arquivo desenhem qualquer item do perfil da mesma forma, sem conhecer seu
    tipo.
    """

    titulo: str
    subtitulo: str | None = None
    periodo: str | None = None
    detalhes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SecaoDocumento:
    """Representa uma seção do currículo com título e blocos na ordem final.

    O DTO conserva o identificador estável da seção, o título legível e os
    blocos já ordenados. Ele existe para que os formatos respeitem a ordem e o
    agrupamento definidos pela versão de currículo.
    """

    secao: SecaoCurriculo
    titulo: str
    blocos: tuple[BlocoDocumento, ...]


@dataclass(frozen=True, slots=True)
class DocumentoCurriculoRenderizado:
    """Descreve o currículo pronto para virar arquivo, sem depender do formato.

    O DTO combina título da versão, modelo escolhido, nome-base do arquivo,
    cabeçalho do estudante e seções não vazias na ordem da versão, contendo
    somente textos e tuplas imutáveis. Ele existe para ser a única entrada dos
    geradores de PDF e DOCX, garantindo que ambos exportem o mesmo conteúdo da
    visualização.
    """

    titulo_versao: str
    modelo: str
    nome_arquivo_base: str
    cabecalho: CabecalhoDocumento
    secoes: tuple[SecaoDocumento, ...]


def montar_documento_renderizado(
    previa: PreviaVersaoCurriculo,
) -> DocumentoCurriculoRenderizado:
    """Converte a prévia da versão no documento renderizado independente de formato.

    A função reaproveita os itens da prévia agrupados por seção, percorre a
    ordem de seções definida pela versão, ignora seções sem itens e os dados
    pessoais (que viram o cabeçalho), e transforma cada item em bloco com
    rótulos e períodos legíveis. Ela existe para concentrar em um único ponto a
    decisão sobre o que o arquivo exportado mostra.
    """
    itens_por_secao = dict(previa.itens_por_secao())
    secoes = tuple(
        SecaoDocumento(
            secao=secao,
            titulo=TITULOS_SECOES[secao],
            blocos=tuple(_bloco(item) for item in itens_por_secao[secao]),
        )
        for secao in previa.curriculo.ordem_secoes
        if itens_por_secao.get(secao)
    )
    return DocumentoCurriculoRenderizado(
        titulo_versao=previa.curriculo.titulo_versao,
        modelo=previa.curriculo.layout,
        nome_arquivo_base=_nome_arquivo_base(
            previa.usuario.nome.valor, previa.curriculo.titulo_versao
        ),
        cabecalho=_cabecalho(previa),
        secoes=secoes,
    )


def _cabecalho(previa: PreviaVersaoCurriculo) -> CabecalhoDocumento:
    """Extrai nome, e-mail e contatos do estudante como textos opcionais.

    A função lê os dados de contato quando existem e devolve campos vazios
    quando não foram informados. Ela existe para isolar a conversão dos value
    objects de contato em textos de exibição.
    """
    usuario = previa.usuario
    contato = usuario.dados_contato
    if contato is None:
        return CabecalhoDocumento(nome=usuario.nome.valor, email=usuario.email.valor)
    cidade = contato.cidade.valor if isinstance(contato.cidade, Cidade) else contato.cidade
    return CabecalhoDocumento(
        nome=usuario.nome.valor,
        email=usuario.email.valor,
        telefones=tuple(telefone.valor for telefone in contato.telefones),
        endereco=contato.endereco.valor,
        cidade=cidade or None,
        linkedin=contato.linkedin or None,
        curriculo_lattes=contato.curriculo_lattes or None,
    )


def _bloco(item: object) -> BlocoDocumento:
    """Converte um item do perfil no bloco de exibição correspondente ao seu tipo.

    A função escolhe título, subtítulo, período e detalhes conforme o tipo do
    item, usando rótulos legíveis para enums e sem expor identificadores nem o
    local de armazenamento de documentos. Ela existe para padronizar a forma
    como cada tipo de item aparece em qualquer formato.
    """
    if isinstance(item, FormacaoAcademica):
        return BlocoDocumento(
            titulo=item.curso,
            subtitulo=f"{item.instituicao} - {ROTULOS_NIVEL_FORMACAO[item.nivel]}",
            periodo=_periodo_formacao(item),
            detalhes=(f"Situação: {ROTULOS_STATUS_FORMACAO[item.status]}",),
        )
    if isinstance(item, ExperienciaProfissional):
        return BlocoDocumento(
            titulo=item.cargo,
            subtitulo=item.empresa,
            periodo=_periodo(item.periodo, "atual"),
            detalhes=(item.descricao,),
        )
    if isinstance(item, ProjetoAcademico):
        return BlocoDocumento(
            titulo=item.titulo,
            detalhes=(item.descricao, f"Tecnologias: {item.tecnologias}"),
        )
    if isinstance(item, Competencia):
        return BlocoDocumento(
            titulo=item.descricao,
            subtitulo=f"{ROTULOS_CATEGORIA_COMPETENCIA[item.categoria]} - {item.nivel}",
        )
    if isinstance(item, Idioma):
        return BlocoDocumento(titulo=item.idioma, subtitulo=item.nivel)
    if isinstance(item, Documento):
        return BlocoDocumento(titulo=item.nome_arquivo)
    raise TypeError(f"Item de currículo sem representação: {type(item).__name__}.")


def _periodo_formacao(formacao: FormacaoAcademica) -> str:
    """Formata o período de uma formação conforme sua situação.

    Formações em andamento mostram "atual" sem término ou o término como
    previsão; concluídas e interrompidas mostram o término, ou só o início se
    ele faltar. A função existe para que a data final não pareça concluída
    quando é apenas uma previsão.
    """
    periodo = formacao.periodo
    if formacao.status is StatusFormacaoAcademica.EM_ANDAMENTO and periodo.fim is not None:
        return f"{_mes_ano(periodo.inicio)} - previsão {_mes_ano(periodo.fim)}"
    if formacao.status is StatusFormacaoAcademica.EM_ANDAMENTO:
        return _periodo(periodo, "atual")
    return _periodo(periodo, None)


def _periodo(periodo: Periodo, texto_sem_fim: str | None) -> str:
    """Formata um período como "MM/AAAA - MM/AAAA" ou com o texto de ausência de fim.

    Sem data final, usa o texto informado (por exemplo "atual") ou mostra só o
    início quando ele é ``None``. A função existe para padronizar a escrita de
    datas em todos os blocos.
    """
    if periodo.fim is not None:
        return f"{_mes_ano(periodo.inicio)} - {_mes_ano(periodo.fim)}"
    if texto_sem_fim is None:
        return _mes_ano(periodo.inicio)
    return f"{_mes_ano(periodo.inicio)} - {texto_sem_fim}"


def _mes_ano(data: date) -> str:
    """Formata uma data como mês e ano com dois e quatro dígitos.

    A função descarta o dia, que não costuma aparecer em currículos. Ela existe
    para manter as datas curtas e uniformes.
    """
    return f"{data.month:02d}/{data.year:04d}"


def _nome_arquivo_base(nome: str, titulo_versao: str) -> str:
    """Gera um nome-base de arquivo seguro a partir do nome e da versão.

    A função remove acentos, converte para minúsculas, troca qualquer sequência
    de caracteres não alfanuméricos por hífen e limita o tamanho, sem incluir
    extensão. Ela existe para que o download use um nome legível e portável em
    qualquer sistema operacional.
    """
    texto = unicodedata.normalize("NFKD", f"curriculo {nome} {titulo_versao}")
    sem_acentos = texto.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", sem_acentos).strip("-")
    return slug[:TAMANHO_MAXIMO_NOME_ARQUIVO].rstrip("-") or "curriculo"
