"""Expõe DTOs e handler HTTP para cadastro de projetos acadêmicos.

O módulo converte JSON e identidade de rota em tipos da Application e traduz
falhas conhecidas em respostas HTTP sem expor entidades de domínio. Ele existe
para manter transporte e segurança fora das regras de domínio e do caso de
uso de cadastro de projetos acadêmicos.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from backend.application import CadastrarProjetoAcademicoEntrada
from backend.domain import ProjetoAcademico, RegraDeDominioViolada, UsuarioId

# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001


class CadastroProjetoAcademicoExecutor(Protocol):
    """Define a capacidade de cadastrar projeto acadêmico que o router invoca.

    O contrato recebe a entrada da Application e devolve a entidade criada,
    sem acoplar o handler a banco ou implementação concreta. Ele existe para
    tornar a interface HTTP testável com doubles que exercitam a mesma
    intenção do caso de uso real.
    """

    async def executar(self, entrada: CadastrarProjetoAcademicoEntrada) -> ProjetoAcademico:
        """Executa o cadastro interno e devolve o projeto persistido.

        Implementações aplicam regras de domínio sem definir respostas HTTP. O
        método existe para que o router se concentre em traduzir fronteiras.
        """


class CadastroProjetoAcademicoRequisicao(BaseModel):
    """Representa o JSON aceito para cadastrar um projeto acadêmico.

    O DTO limita presença e tamanho na fronteira antes da conversão ao caso de
    uso e não é usado como entidade de domínio. Ele existe para separar
    transporte do núcleo de cadastro de projetos acadêmicos.
    """

    titulo: str = Field(min_length=1, max_length=200)
    descricao: str = Field(min_length=1, max_length=2000)
    tecnologias: str = Field(min_length=1, max_length=300)


class ProjetoAcademicoResposta(BaseModel):
    """Representa os dados públicos devolvidos após cadastrar um projeto.

    O DTO extrai identidade, proprietário e textos do projeto sem serializar a
    entidade de domínio diretamente. Ele existe para manter a saída HTTP
    estável mesmo se a entidade interna evoluir.
    """

    id: UUID
    usuario_id: UUID
    titulo: str
    descricao: str
    tecnologias: str


def criar_router(
    cadastrar_projeto_academico: CadastroProjetoAcademicoExecutor | None,
) -> APIRouter:
    """Cria a rota HTTP de cadastro de projeto acadêmico com o caso injetado.

    A função converte identidade de rota e JSON em uma entrada da Application
    e traduz exceções conhecidas em status seguros. Ela existe para registrar
    a API e permitir testes unitários com doubles, sem sessão de banco real.
    """
    router = APIRouter()

    @router.post(
        "/estudantes/{usuario_id}/projetos-academicos",
        response_model=ProjetoAcademicoResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def cadastrar(usuario_id: UUID, requisicao: CadastroProjetoAcademicoRequisicao) -> ProjetoAcademicoResposta:
        """Executa o cadastro HTTP e devolve os dados públicos do projeto criado.

        O handler monta a entrada da Application a partir da rota e do corpo,
        aguarda o caso de uso e traduz violação de domínio sem expor detalhes
        internos. Ele existe para expor o cadastro sem levar HTTP à Application.
        """
        if cadastrar_projeto_academico is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Cadastro indisponível.")
        entrada = CadastrarProjetoAcademicoEntrada(
            usuario_id=UsuarioId(usuario_id),
            titulo=requisicao.titulo,
            descricao=requisicao.descricao,
            tecnologias=requisicao.tecnologias,
        )
        try:
            projeto = await cadastrar_projeto_academico.executar(entrada)
        except RegraDeDominioViolada as erro:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro
        return ProjetoAcademicoResposta(
            id=projeto.id.valor,
            usuario_id=projeto.usuario_id.valor,
            titulo=projeto.titulo,
            descricao=projeto.descricao,
            tecnologias=projeto.tecnologias,
        )

    return router