"""Converte a massa JSON documental em entidades válidas para testes de prévia.

O módulo lê os perfis fictícios mantidos em ``docs`` e instancia as entidades do
domínio com suas identidades, períodos e referências. Ele existe para garantir
que a massa de teste acompanhe os contratos reais antes de ser usada por APIs ou
modelos de apresentação.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from uuid import UUID

from backend.application import PreviaVersaoCurriculo
from backend.domain import (
    CategoriaCompetencia,
    Competencia,
    CompetenciaId,
    Curriculo,
    CurriculoId,
    DadosContato,
    Documento,
    DocumentoId,
    Email,
    Endereco,
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    FormacaoAcademica,
    FormacaoAcademicaId,
    HashSenha,
    Idioma,
    IdiomaId,
    NivelFormacaoAcademica,
    Nome,
    Periodo,
    ProjetoAcademico,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    StatusFormacaoAcademica,
    Telefone,
    Usuario,
    UsuarioId,
)

_ARQUIVO_MASSA = Path(__file__).resolve().parents[4] / "docs" / "massa_teste_curriculos.json"
_HASH_SENHA_FIXTURE = HashSenha("$scrypt$ln=16,r=8,p=1$massadetesteficticia")


@dataclass(frozen=True, slots=True)
class CurriculoMassaTeste:
    """Agrupa as entidades de um currículo da massa e monta sua prévia.

    A estrutura conserva as entidades tipadas criadas a partir do JSON e reúne
    todas as seções em ``PreviaVersaoCurriculo``. Ela existe para que testes
    exercitem a mesma serialização pública usada pela visualização, sem duplicar
    objetos de apresentação manualmente.
    """

    usuario: Usuario
    curriculo: Curriculo
    formacoes: tuple[FormacaoAcademica, ...]
    experiencias: tuple[ExperienciaProfissional, ...]
    projetos: tuple[ProjetoAcademico, ...]
    competencias: tuple[Competencia, ...]
    idiomas: tuple[Idioma, ...]
    documentos: tuple[Documento, ...]

    def para_previa(self) -> PreviaVersaoCurriculo:
        """Monta o modelo de leitura que a rota de prévia transforma em JSON.

        O método reúne as entidades já válidas por seção, sem acessar rede ou
        persistência e sem alterar a massa carregada. Ele existe para conectar
        diretamente a fixture ao renderizador oficial da API.
        """
        return PreviaVersaoCurriculo(
            usuario=self.usuario,
            curriculo=self.curriculo,
            formacoes=self.formacoes,
            experiencias=self.experiencias,
            projetos=self.projetos,
            competencias=self.competencias,
            idiomas=self.idiomas,
            documentos=self.documentos,
        )


def obter_curriculos_massa_teste() -> tuple[CurriculoMassaTeste, ...]:
    """Carrega os perfis JSON e produz as entidades de domínio correspondentes.

    A função lê o arquivo versionado, converte UUIDs, datas e enums canônicos e
    inclui as referências de cada item no agregado de currículo. Ela existe para
    detectar rapidamente qualquer divergência entre a massa de teste e os
    invariantes atuais do domínio.
    """
    dados = json.loads(_ARQUIVO_MASSA.read_text(encoding="utf-8"))
    return tuple(_criar_curriculo(dados_curriculo) for dados_curriculo in dados["curriculos"])


def _criar_curriculo(dados: dict[str, object]) -> CurriculoMassaTeste:
    """Instancia um currículo e seus itens a partir de um registro serializado.

    A função recria cada entidade com os value objects exigidos, associa suas
    referências ao currículo e devolve o agrupamento imutável. Ela existe para
    centralizar a tradução da massa externa para o modelo de domínio.
    """
    usuario_dados = dados["usuario"]
    curriculo_dados = dados["curriculo"]
    assert isinstance(usuario_dados, dict) and isinstance(curriculo_dados, dict)
    usuario_id = UsuarioId(UUID(str(usuario_dados["id"])))
    contato_dados = usuario_dados["dados_contato"]
    assert isinstance(contato_dados, dict)
    usuario = Usuario(
        id=usuario_id,
        nome=Nome(str(usuario_dados["nome"])),
        email=Email(str(usuario_dados["email"])),
        hash_senha=_HASH_SENHA_FIXTURE,
        dados_contato=DadosContato(
            endereco=Endereco(str(contato_dados["endereco"])),
            telefones=tuple(Telefone(str(valor)) for valor in contato_dados["telefones"]),
            linkedin=contato_dados["linkedin"],
            curriculo_lattes=contato_dados["curriculo_lattes"],
        ),
    )
    curriculo = Curriculo(
        id=CurriculoId(UUID(str(curriculo_dados["id"]))),
        usuario_id=UsuarioId(UUID(str(curriculo_dados["usuario_id"]))),
        titulo_versao=str(curriculo_dados["titulo_versao"]),
        layout=str(curriculo_dados["layout"]),
        is_public=bool(curriculo_dados["is_public"]),
    )
    formacoes = tuple(_criar_formacao(item) for item in dados["formacoes"])
    experiencias = tuple(_criar_experiencia(item) for item in dados["experiencias"])
    projetos = tuple(_criar_projeto(item) for item in dados["projetos"])
    competencias = tuple(_criar_competencia(item) for item in dados["competencias"])
    idiomas = tuple(_criar_idioma(item) for item in dados["idiomas"])
    documentos = tuple(_criar_documento(item) for item in dados["documentos"])
    for item in (*formacoes, *experiencias, *projetos, *competencias, *idiomas, *documentos):
        curriculo.incluir_referencia(ReferenciaCurriculo(item.id))
    return CurriculoMassaTeste(usuario, curriculo, formacoes, experiencias, projetos, competencias, idiomas, documentos)


def _periodo(dados: dict[str, object]) -> Periodo:
    """Converte datas ISO de um objeto serializado no value object de período.

    A função interpreta a data de início obrigatória e o fim opcional antes de
    delegar a validação cronológica ao domínio. Ela existe para reutilizar a
    mesma conversão em formações e experiências da massa.
    """
    periodo = dados["periodo"]
    assert isinstance(periodo, dict)
    fim = periodo["fim"]
    return Periodo(date.fromisoformat(str(periodo["inicio"])), None if fim is None else date.fromisoformat(str(fim)))


def _criar_formacao(dados: dict[str, object]) -> FormacaoAcademica:
    """Cria uma formação acadêmica tipada a partir do registro da massa."""
    return FormacaoAcademica(FormacaoAcademicaId(UUID(str(dados["id"]))), UsuarioId(UUID(str(dados["usuario_id"]))), str(dados["instituicao"]), str(dados["curso"]), NivelFormacaoAcademica(str(dados["nivel"])), _periodo(dados), StatusFormacaoAcademica(str(dados["status"])))


def _criar_experiencia(dados: dict[str, object]) -> ExperienciaProfissional:
    """Cria uma experiência profissional tipada a partir do registro da massa."""
    return ExperienciaProfissional(ExperienciaProfissionalId(UUID(str(dados["id"]))), UsuarioId(UUID(str(dados["usuario_id"]))), str(dados["empresa"]), str(dados["cargo"]), str(dados["descricao"]), _periodo(dados))


def _criar_projeto(dados: dict[str, object]) -> ProjetoAcademico:
    """Cria um projeto acadêmico tipado a partir do registro da massa."""
    return ProjetoAcademico(ProjetoAcademicoId(UUID(str(dados["id"]))), UsuarioId(UUID(str(dados["usuario_id"]))), str(dados["titulo"]), str(dados["descricao"]), str(dados["tecnologias"]))


def _criar_competencia(dados: dict[str, object]) -> Competencia:
    """Cria uma competência tipada a partir do registro da massa."""
    return Competencia(CompetenciaId(UUID(str(dados["id"]))), UsuarioId(UUID(str(dados["usuario_id"]))), CategoriaCompetencia(str(dados["categoria"])), str(dados["descricao"]), str(dados["nivel"]))


def _criar_idioma(dados: dict[str, object]) -> Idioma:
    """Cria um idioma tipado a partir do registro da massa."""
    return Idioma(IdiomaId(UUID(str(dados["id"]))), UsuarioId(UUID(str(dados["usuario_id"]))), str(dados["idioma"]), str(dados["nivel"]))


def _criar_documento(dados: dict[str, object]) -> Documento:
    """Cria metadados tipados de documento a partir do registro da massa."""
    return Documento(DocumentoId(UUID(str(dados["id"]))), UsuarioId(UUID(str(dados["usuario_id"]))), str(dados["nome_arquivo"]), str(dados["tipo_arquivo"]), str(dados["url_armazenamento"]))
