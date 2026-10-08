"""Expõe DTOs e o handler HTTP da prévia de uma versão de currículo.

O módulo converte identidades de rota em entrada da Application, traduz o modelo
de leitura da prévia em DTOs públicos agrupados por seção e converte falhas
conhecidas em respostas HTTP, sem expor entidades de domínio. Ele existe para
manter transporte e apresentação de dados fora das regras de domínio e do caso
de uso de prévia.
"""

# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
from datetime import date
from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.application import (
    CurriculoNaoEncontrado,
    GerarPreviaVersaoCurriculoEntrada,
    PreviaVersaoCurriculo,
)
from backend.domain import CurriculoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class PreviaVersaoCurriculoExecutor(Protocol):
    """Define a capacidade de gerar a prévia que o router invoca.

    O contrato recebe a entrada da Application e devolve o modelo de leitura da
    prévia, sem acoplar o handler a banco ou implementação concreta. Ele existe
    para tornar a interface HTTP testável com doubles que exercitam a mesma
    intenção do caso de uso real.
    """

    # Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
    async def executar(self, entrada: GerarPreviaVersaoCurriculoEntrada) -> PreviaVersaoCurriculo:
        """Executa a geração interna e devolve a prévia agrupada por seção.

        Implementações aplicam as regras de propriedade sem definir respostas
        HTTP. O método existe para que o router se concentre em traduzir
        fronteiras.
        """


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class ContatoPreviaResposta(BaseModel):
    """Representa os dados de contato do estudante exibidos na prévia.

    O DTO expõe endereço, telefones e links como texto simples, sem serializar
    value objects. Ele existe para manter a saída HTTP estável mesmo se a
    representação interna do contato evoluir.
    """

    endereco: str
    telefones: list[str]
    linkedin: str | None
    curriculo_lattes: str | None


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class EstudantePreviaResposta(BaseModel):
    """Representa a identificação do estudante exibida na prévia.

    O DTO expõe somente nome, e-mail e contato opcional, sem identidade interna,
    credencial nem estado de exclusão. Ele existe para minimizar os dados
    pessoais devolvidos ao cliente.
    """

    nome: str
    email: str
    contato: ContatoPreviaResposta | None


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class FormacaoPreviaResposta(BaseModel):
    """Representa uma formação acadêmica exibida na prévia.

    O DTO expõe os campos descritivos e as datas do período como valores
    simples. Ele existe para separar o transporte da entidade de domínio.
    """

    id: UUID
    instituicao: str
    curso: str
    nivel: str
    status: str
    inicio: date
    fim: date | None


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class ExperienciaPreviaResposta(BaseModel):
    """Representa uma experiência profissional exibida na prévia.

    O DTO expõe os campos descritivos e as datas do período como valores
    simples. Ele existe para separar o transporte da entidade de domínio.
    """

    id: UUID
    empresa: str
    cargo: str
    descricao: str
    inicio: date
    fim: date | None


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class ProjetoPreviaResposta(BaseModel):
    """Representa um projeto acadêmico exibido na prévia.

    O DTO expõe título, descrição e tecnologias como texto. Ele existe para
    separar o transporte da entidade de domínio.
    """

    id: UUID
    titulo: str
    descricao: str
    tecnologias: str


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class CompetenciaPreviaResposta(BaseModel):
    """Representa uma competência exibida na prévia.

    O DTO expõe descrição e nível como texto. Ele existe para separar o
    transporte da entidade de domínio.
    """

    id: UUID
    descricao: str
    nivel: str


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class IdiomaPreviaResposta(BaseModel):
    """Representa um idioma exibido na prévia.

    O DTO expõe o nome do idioma e o nível como texto. Ele existe para separar
    o transporte da entidade de domínio.
    """

    id: UUID
    idioma: str
    nivel: str


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class DocumentoPreviaResposta(BaseModel):
    """Representa os metadados públicos de um documento exibido na prévia.

    O DTO expõe somente nome e tipo do arquivo e omite deliberadamente o caminho
    de armazenamento. Ele existe para não vazar detalhe interno de
    armazenamento ao cliente.
    """

    id: UUID
    nome_arquivo: str
    tipo_arquivo: str


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class PreviaVersaoCurriculoResposta(BaseModel):
    """Representa a prévia completa de uma versão de currículo.

    O DTO reúne os dados da versão, a identificação do estudante e as seis
    seções de itens já ordenadas. Ele existe para que o cliente apresente o
    currículo conforme o layout informado sem consultas adicionais.
    """

    curriculo_id: UUID
    titulo_versao: str
    layout: str
    estudante: EstudantePreviaResposta
    formacoes: list[FormacaoPreviaResposta]
    experiencias: list[ExperienciaPreviaResposta]
    projetos: list[ProjetoPreviaResposta]
    competencias: list[CompetenciaPreviaResposta]
    idiomas: list[IdiomaPreviaResposta]
    documentos: list[DocumentoPreviaResposta]


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
def _para_resposta(previa: PreviaVersaoCurriculo) -> PreviaVersaoCurriculoResposta:
    """Converte o modelo de leitura da Application na resposta pública da prévia.

    A função copia os campos permitidos de cada entidade para os DTOs,
    preservando a ordem recebida e omitindo credencial, proprietário e caminho
    de armazenamento. Ela existe para garantir que nenhuma entidade de domínio
    ou dado interno chegue ao cliente.
    """
    contato = previa.usuario.dados_contato
    return PreviaVersaoCurriculoResposta(
        curriculo_id=previa.curriculo.id.valor,
        titulo_versao=previa.curriculo.titulo_versao,
        layout=previa.curriculo.layout,
        estudante=EstudantePreviaResposta(
            nome=previa.usuario.nome.valor,
            email=previa.usuario.email.valor,
            contato=(
                None
                if contato is None
                else ContatoPreviaResposta(
                    endereco=contato.endereco.valor,
                    telefones=[telefone.valor for telefone in contato.telefones],
                    linkedin=contato.linkedin,
                    curriculo_lattes=contato.curriculo_lattes,
                )
            ),
        ),
        formacoes=[
            FormacaoPreviaResposta(
                id=item.id.valor,
                instituicao=item.instituicao,
                curso=item.curso,
                nivel=item.nivel,
                status=item.status,
                inicio=item.periodo.inicio,
                fim=item.periodo.fim,
            )
            for item in previa.formacoes
        ],
        experiencias=[
            ExperienciaPreviaResposta(
                id=item.id.valor,
                empresa=item.empresa,
                cargo=item.cargo,
                descricao=item.descricao,
                inicio=item.periodo.inicio,
                fim=item.periodo.fim,
            )
            for item in previa.experiencias
        ],
        projetos=[
            ProjetoPreviaResposta(
                id=item.id.valor, titulo=item.titulo, descricao=item.descricao, tecnologias=item.tecnologias
            )
            for item in previa.projetos
        ],
        competencias=[
            CompetenciaPreviaResposta(id=item.id.valor, descricao=item.descricao, nivel=item.nivel)
            for item in previa.competencias
        ],
        idiomas=[IdiomaPreviaResposta(id=item.id.valor, idioma=item.idioma, nivel=item.nivel) for item in previa.idiomas],
        documentos=[
            DocumentoPreviaResposta(id=item.id.valor, nome_arquivo=item.nome_arquivo, tipo_arquivo=item.tipo_arquivo)
            for item in previa.documentos
        ],
    )


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
def criar_router(gerar_previa: PreviaVersaoCurriculoExecutor | None) -> APIRouter:
    """Cria a rota HTTP de prévia usando o caso de uso injetado.

    A função converte identidades de rota em entrada da Application e traduz a
    ausência da versão em status seguro. Ela existe para registrar a API e
    permitir testes unitários com doubles, sem sessão de banco real.

    Nota: a identidade do solicitante ainda é recebida pela própria rota
    (``usuario_id`` no caminho), e não derivada de uma sessão autenticada, e o
    adapter real de leitura dos itens depende das áreas que os mantêm; ambos
    permanecem handoffs pendentes, conforme
    prompts/backend/20261008-183601-previa-versao-curriculo-v001.md.
    """
    router = APIRouter()

    @router.get(
        "/estudantes/{usuario_id}/curriculos/{curriculo_id}/previa",
        response_model=PreviaVersaoCurriculoResposta,
    )
    async def gerar(usuario_id: UUID, curriculo_id: UUID) -> PreviaVersaoCurriculoResposta:
        """Executa a geração HTTP e devolve a prévia pública da versão.

        O handler monta a entrada da Application a partir da rota, aguarda o
        caso de uso e traduz ausência ou propriedade alheia da versão sem expor
        detalhes internos. Ele existe para expor a consulta sem levar HTTP à
        Application.
        """
        if gerar_previa is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Prévia indisponível.")
        entrada = GerarPreviaVersaoCurriculoEntrada(
            usuario_id=UsuarioId(usuario_id),
            curriculo_id=CurriculoId(curriculo_id),
        )
        try:
            previa = await gerar_previa.executar(entrada)
        except CurriculoNaoEncontrado as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
        return _para_resposta(previa)

    return router
