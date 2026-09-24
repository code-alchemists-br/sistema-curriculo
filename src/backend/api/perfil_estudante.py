"""Expõe DTOs e handlers HTTP para edição e exclusão do perfil do estudante.

O módulo converte JSON e identidade de rota em tipos da Application e traduz
falhas conhecidas em respostas HTTP sem expor entidades, hash de senha ou
detalhes de persistência. Ele existe para manter transporte e segurança fora
das regras de domínio e dos casos de uso de perfil.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from backend.application import (
    EditarPerfilEntrada,
    EmailJaCadastrado,
    ExcluirPerfilEntrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)
from backend.domain import Email, Nome, RegraDeDominioViolada, Usuario, UsuarioId


class EdicaoPerfilExecutor(Protocol):
    """Define a capacidade de editar perfil que o router precisa invocar.

    O contrato recebe a entrada da Application e devolve o agregado com o novo
    estado, sem acoplar o handler a banco ou implementação concreta. Ele existe
    para tornar a interface HTTP testável com doubles que exercitam a mesma
    intenção do caso de uso real.
    """

    async def executar(self, entrada: EditarPerfilEntrada) -> Usuario:
        """Executa a edição interna e devolve o agregado atualizado.

        Implementações aplicam regras de perfil sem definir respostas HTTP. O
        método existe para que o router se concentre em traduzir fronteiras.
        """


class ExclusaoPerfilExecutor(Protocol):
    """Define a capacidade de excluir perfil que o router precisa invocar.

    O contrato recebe a entrada da Application e devolve o agregado já marcado
    como excluído, sem acoplar o handler a relógio ou repositório concreto. Ele
    existe para tornar a interface HTTP testável com doubles.
    """

    async def executar(self, entrada: ExcluirPerfilEntrada) -> Usuario:
        """Executa a exclusão lógica interna e devolve o estado resultante.

        Implementações aplicam a transição idempotente sem definir resposta
        HTTP. O método existe para que o router traduza apenas a fronteira.
        """


class EditarPerfilRequisicao(BaseModel):
    """Representa o JSON aceito para editar nome e e-mail de um perfil.

    O DTO limita presença e tamanho na fronteira antes da conversão a VOs e não
    aceita senha, hash ou identidade — que permanecem fora deste contrato. Ele
    existe para separar transporte do núcleo de edição de perfil.
    """

    nome: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=320)


class PerfilResposta(BaseModel):
    """Representa somente os dados públicos devolvidos após editar um perfil.

    O DTO extrai identidade, nome e e-mail sem serializar hash de senha, data
    de exclusão ou a entidade de domínio. Ele existe para proteger credenciais
    e detalhes internos na saída HTTP.
    """

    id: UUID
    nome: str
    email: str


def criar_router(
    editar_perfil: EdicaoPerfilExecutor | None,
    excluir_perfil: ExclusaoPerfilExecutor | None,
) -> APIRouter:
    """Cria rotas HTTP de perfil usando casos de uso injetados pela composição.

    A função converte identidade de rota e JSON em entradas da Application e
    traduz exceções conhecidas em status seguros. Ela existe para registrar a
    API e permitir testes unitários com doubles, sem sessão de banco real.

    Nota: a identidade do perfil ainda é recebida pela própria rota
    (``usuario_id`` no caminho), e não derivada de uma sessão autenticada.
    Autenticação e autorização de entrada permanecem um handoff pendente,
    conforme prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md.
    """
    router = APIRouter()

    @router.put("/estudantes/{usuario_id}", response_model=PerfilResposta)
    async def editar(usuario_id: UUID, requisicao: EditarPerfilRequisicao) -> PerfilResposta:
        """Executa edição HTTP e devolve os dados públicos do perfil atualizado.

        O handler cria VOs e identidade tipada, aguarda o caso de uso e traduz
        ausência, exclusão e duplicidade sem expor detalhes internos. Ele
        existe para expor a edição sem levar HTTP à Application.
        """
        if editar_perfil is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Edição indisponível.")
        try:
            entrada = EditarPerfilEntrada(
                usuario_id=UsuarioId(usuario_id),
                nome=Nome(requisicao.nome),
                email=Email(requisicao.email),
            )
            usuario = await editar_perfil.executar(entrada)
        except RegraDeDominioViolada as erro:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro
        except PerfilNaoEncontrado as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
        except PerfilExcluido as erro:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(erro)) from erro
        except EmailJaCadastrado as erro:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(erro)) from erro
        return PerfilResposta(id=usuario.id.valor, nome=usuario.nome.valor, email=usuario.email.valor)

    @router.delete("/estudantes/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def excluir(usuario_id: UUID) -> None:
        """Executa exclusão lógica HTTP sem expor o estado resultante ao cliente.

        O handler converte a identidade de rota, aguarda o caso de uso e traduz
        ausência sem revelar se o perfil já estava excluído. Ele existe para
        tornar a exclusão idempotente também do ponto de vista HTTP.
        """
        if excluir_perfil is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Exclusão indisponível.")
        entrada = ExcluirPerfilEntrada(usuario_id=UsuarioId(usuario_id))
        try:
            await excluir_perfil.executar(entrada)
        except PerfilNaoEncontrado as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro

    return router