"""Expõe DTOs e endpoints HTTP para cadastro de itens de perfil (cursos, certificações, idiomas)."""

from typing import Protocol
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from backend.application.cadastro_certificacao import CadastrarCertificacaoEntrada
from backend.application.cadastro_curso import CadastrarCursoEntrada
from backend.application.cadastro_idioma import CadastrarIdiomaEntrada
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import Certificacao, Curso, Idioma
from backend.domain.value_objects import UsuarioId


# --- PROTOCOLOS DOS EXECUTORES (para injeção e testes desacoplados) ---

class CadastroCursoExecutor(Protocol):
    async def executar(self, entrada: CadastrarCursoEntrada) -> Curso: ...


class CadastroCertificacaoExecutor(Protocol):
    async def executar(self, entrada: CadastrarCertificacaoEntrada) -> Certificacao: ...


class CadastroIdiomaExecutor(Protocol):
    async def executar(self, entrada: CadastrarIdiomaEntrada) -> Idioma: ...


# --- SCHEMAS DE ENTRADA (REQUEST) ---

class CursoRequisicao(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    instituicao: str = Field(min_length=1, max_length=200)
    carga_horaria: int | None = Field(default=None, gt=0)


class CertificacaoRequisicao(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    organizacao_emissora: str = Field(min_length=1, max_length=200)


class IdiomaRequisicao(BaseModel):
    idioma: str = Field(min_length=1, max_length=100)
    nivel: str = Field(min_length=1, max_length=50)


# --- SCHEMAS DE SAÍDA (RESPONSE) ---

class ItemCriadoResposta(BaseModel):
    id: UUID
    usuario_id: UUID


# --- FACTORY DO ROUTER ---

def criar_router(
    cadastrar_curso: CadastroCursoExecutor | None = None,
    cadastrar_certificacao: CadastroCertificacaoExecutor | None = None,
    cadastrar_idioma: CadastroIdiomaExecutor | None = None,
) -> APIRouter:
    router = APIRouter(prefix="/estudantes/{estudante_id}", tags=["Itens do Perfil"])

    @router.post(
        "/cursos",
        response_model=ItemCriadoResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def criar_curso(
        estudante_id: UUID,
        requisicao: CursoRequisicao,
    ) -> ItemCriadoResposta:
        if cadastrar_curso is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cadastro de cursos indisponível.",
            )
        try:
            curso = await cadastrar_curso.executar(
                CadastrarCursoEntrada(
                    usuario_id=UsuarioId(estudante_id),
                    nome=requisicao.nome,
                    instituicao=requisicao.instituicao,
                    carga_horaria=requisicao.carga_horaria,
                )
            )
            return ItemCriadoResposta(
                id=curso.id.valor,
                usuario_id=curso.usuario_id.valor,
            )
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(erro),
            ) from erro

    @router.post(
        "/certificacoes",
        response_model=ItemCriadoResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def criar_certificacao(
        estudante_id: UUID,
        requisicao: CertificacaoRequisicao,
    ) -> ItemCriadoResposta:
        if cadastrar_certificacao is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cadastro de certificações indisponível.",
            )
        try:
            cert = await cadastrar_certificacao.executar(
                CadastrarCertificacaoEntrada(
                    usuario_id=UsuarioId(estudante_id),
                    nome=requisicao.nome,
                    organizacao_emissora=requisicao.organizacao_emissora,
                )
            )
            return ItemCriadoResposta(
                id=cert.id.valor,
                usuario_id=cert.usuario_id.valor,
            )
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(erro),
            ) from erro

    @router.post(
        "/idiomas",
        response_model=ItemCriadoResposta,
        status_code=status.HTTP_201_CREATED,
    )
    async def criar_idioma(
        estudante_id: UUID,
        requisicao: IdiomaRequisicao,
    ) -> ItemCriadoResposta:
        if cadastrar_idioma is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cadastro de idiomas indisponível.",
            )
        try:
            idioma = await cadastrar_idioma.executar(
                CadastrarIdiomaEntrada(
                    usuario_id=UsuarioId(estudante_id),
                    idioma=requisicao.idioma,
                    nivel=requisicao.nivel,
                )
            )
            return ItemCriadoResposta(
                id=idioma.id.valor,
                usuario_id=idioma.usuario_id.valor,
            )
        except RegraDeDominioViolada as erro:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(erro),
            ) from erro

    return router