"""Expõe o cadastro de experiências profissionais por HTTP autenticado."""

from datetime import date
from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from backend.application.cadastro_experiencia_profissional import (
    CadastrarExperienciaProfissionalEntrada,
)
from backend.domain import ExperienciaProfissional, Periodo, RegraDeDominioViolada
from backend.domain.value_objects import UsuarioId


class CadastroExperienciaProfissionalRequisicao(BaseModel):
    """Representa os campos de transporte necessários para criar experiência.

    Pydantic valida tipos e datas antes da conversão a value objects; o DTO não
    aceita proprietário ou identificador. Ele existe para separar JSON do
    contrato interno e impedir que o cliente escolha a conta de destino.
    """

    empresa: str
    cargo: str
    descricao: str
    data_inicio: date
    data_fim: date | None = None


class ExperienciaProfissionalResposta(BaseModel):
    """Representa dados públicos devolvidos após o cadastro da experiência.

    O DTO extrai UUIDs, textos e datas sem serializar a entidade diretamente.
    Ele existe para manter o contrato HTTP desacoplado do modelo de domínio.
    """

    id: UUID
    usuario_id: UUID
    empresa: str
    cargo: str
    descricao: str
    data_inicio: date
    data_fim: date | None


class CadastroExperienciaProfissionalExecutor(Protocol):
    """Define a execução do cadastro de experiência na fronteira HTTP.

    O contrato recebe uma entrada tipada e devolve a entidade criada sem expor
    persistência à API. Ele existe para permitir injeção do caso de uso e testes
    isolados da rota.
    """

    async def executar(
        self, entrada: CadastrarExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Cadastra uma experiência válida para a identidade autenticada.

        A implementação aplica as regras de domínio e persiste pela porta
        interna apropriada. O método existe para separar o transporte HTTP da
        orquestração do caso de uso.
        """


def criar_router(
    cadastrar_experiencia: CadastroExperienciaProfissionalExecutor | None,
) -> APIRouter:
    """Cria a rota POST protegida por sessão autenticada.

    A rota recebe o principal que o middleware autenticador instalou em
    ``request.state``, converte o corpo em entrada de Application e invoca o
    executor injetado. Ela existe para impedir que o cliente escolha o dono da
    experiência, sem acoplar a API à persistência ou à sessão concreta.
    """
    router = APIRouter()

    @router.post(
        "/experiencias-profissionais",
        response_model=ExperienciaProfissionalResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def cadastrar(
        requisicao: CadastroExperienciaProfissionalRequisicao,
        request: Request,
    ) -> ExperienciaProfissionalResposta:
        """Cadastra a experiência vinculada à identidade autenticada da requisição.

        O handler exige um executor e um ``UsuarioId`` instalado pelo middleware,
        constrói ``Periodo`` e encaminha a entrada tipada ao caso de uso. Ele
        existe para proteger a propriedade do dado e traduzir falhas de domínio
        em respostas HTTP estáveis.
        """
        if cadastrar_experiencia is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cadastro indisponível.",
            )
        usuario_id = getattr(request.state, "usuario_id", None)
        if not isinstance(usuario_id, UUID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária.",
            )
        try:
            entrada = CadastrarExperienciaProfissionalEntrada(
                usuario_id=UsuarioId(usuario_id),
                empresa=requisicao.empresa,
                cargo=requisicao.cargo,
                descricao=requisicao.descricao,
                periodo=Periodo(requisicao.data_inicio, requisicao.data_fim),
            )
            experiencia = await cadastrar_experiencia.executar(entrada)
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)
            ) from erro
        return ExperienciaProfissionalResposta(
            id=experiencia.id.valor,
            usuario_id=experiencia.usuario_id.valor,
            empresa=experiencia.empresa,
            cargo=experiencia.cargo,
            descricao=experiencia.descricao,
            data_inicio=experiencia.periodo.inicio,
            data_fim=experiencia.periodo.fim,
        )

    return router
