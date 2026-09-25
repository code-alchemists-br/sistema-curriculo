"""Expõe DTOs e handler HTTP para manutenção de dados pessoais e de contato.

O módulo converte JSON e identidade de rota em tipos da Application e traduz
falhas conhecidas em respostas HTTP sem expor entidades ou detalhes de
persistência. Ele existe para manter transporte e segurança fora das regras
de domínio e do caso de uso de dados de contato.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from backend.application import (
    AtualizarDadosContatoEntrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)
from backend.domain import DadosContato, Endereco, RegraDeDominioViolada, Telefone, Usuario, UsuarioId

# Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001


class AtualizacaoDadosContatoExecutor(Protocol):
    """Define a capacidade de atualizar dados de contato que o router invoca.

    O contrato recebe a entrada da Application e devolve o agregado com o
    novo estado, sem acoplar o handler a banco ou implementação concreta. Ele
    existe para tornar a interface HTTP testável com doubles que exercitam a
    mesma intenção do caso de uso real.
    """

    async def executar(self, entrada: AtualizarDadosContatoEntrada) -> Usuario:
        """Executa a atualização interna e devolve o agregado atualizado.

        Implementações aplicam regras de contato sem definir respostas HTTP. O
        método existe para que o router se concentre em traduzir fronteiras.
        """


class DadosContatoRequisicao(BaseModel):
    """Representa o JSON aceito para atualizar endereço, telefones e links.

    O DTO exige ao menos um telefone e limita presença e tamanho na fronteira
    antes da conversão a VOs. Ele existe para separar transporte do núcleo de
    manutenção de dados de contato.
    """

    endereco: str = Field(min_length=1, max_length=500)
    telefones: list[str] = Field(min_length=1, max_length=5)
    linkedin: str | None = Field(default=None, max_length=300)
    curriculo_lattes: str | None = Field(default=None, max_length=300)


class DadosContatoResposta(BaseModel):
    """Representa os dados de contato públicos devolvidos após atualização.

    O DTO extrai identidade e dados de contato sem serializar hash de senha,
    nome, e-mail ou a entidade de domínio. Ele existe para proteger dados que
    não fazem parte desta operação na saída HTTP.
    """

    id: UUID
    endereco: str
    telefones: list[str]
    linkedin: str | None
    curriculo_lattes: str | None


def criar_router(
    atualizar_dados_contato: AtualizacaoDadosContatoExecutor | None,
) -> APIRouter:
    """Cria a rota HTTP de dados de contato usando o caso de uso injetado.

    A função converte identidade de rota e JSON em uma entrada da Application
    e traduz exceções conhecidas em status seguros. Ela existe para registrar
    a API e permitir testes unitários com doubles, sem sessão de banco real.

    Nota: a identidade do perfil ainda é recebida pela própria rota
    (``usuario_id`` no caminho), e não derivada de uma sessão autenticada —
    mesma limitação já documentada em ``api/perfil_estudante.py``.
    """
    router = APIRouter()

    @router.put("/estudantes/{usuario_id}/dados-contato", response_model=DadosContatoResposta)
    async def atualizar(usuario_id: UUID, requisicao: DadosContatoRequisicao) -> DadosContatoResposta:
        """Executa a atualização HTTP e devolve os dados de contato salvos.

        O handler cria VOs a partir do JSON, aguarda o caso de uso e traduz
        ausência e exclusão sem expor detalhes internos. Ele existe para expor
        a manutenção de contato sem levar HTTP à Application.
        """
        if atualizar_dados_contato is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Atualização indisponível.")
        try:
            dados_contato = DadosContato(
                endereco=Endereco(requisicao.endereco),
                telefones=tuple(Telefone(telefone) for telefone in requisicao.telefones),
                linkedin=requisicao.linkedin,
                curriculo_lattes=requisicao.curriculo_lattes,
            )
            entrada = AtualizarDadosContatoEntrada(
                usuario_id=UsuarioId(usuario_id),
                dados_contato=dados_contato,
            )
            usuario = await atualizar_dados_contato.executar(entrada)
        except RegraDeDominioViolada as erro:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro
        except PerfilNaoEncontrado as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
        except PerfilExcluido as erro:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(erro)) from erro

        assert usuario.dados_contato is not None
        return DadosContatoResposta(
            id=usuario.id.valor,
            endereco=usuario.dados_contato.endereco.valor,
            telefones=[telefone.valor for telefone in usuario.dados_contato.telefones],
            linkedin=usuario.dados_contato.linkedin,
            curriculo_lattes=usuario.dados_contato.curriculo_lattes,
        )

    return router