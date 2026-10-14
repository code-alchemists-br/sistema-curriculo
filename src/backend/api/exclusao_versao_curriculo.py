"""Expõe o handler HTTP da exclusão de uma versão de currículo.

O módulo converte as identidades de rota em entrada da Application e traduz a
ausência da versão em resposta HTTP segura, sem expor entidades de domínio. Ele
existe para manter transporte fora das regras de domínio e do caso de uso de
exclusão de versão.
"""

# Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.application import CurriculoNaoEncontrado, ExcluirVersaoCurriculoEntrada
from backend.domain import CurriculoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
class ExclusaoVersaoCurriculoExecutor(Protocol):
    """Define a capacidade de excluir versão de currículo que o router invoca.

    O contrato recebe a entrada da Application e não devolve conteúdo, sem
    acoplar o handler a banco ou implementação concreta. Ele existe para tornar
    a interface HTTP testável com doubles que exercitam a mesma intenção do caso
    de uso real.
    """

    # Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
    async def executar(self, entrada: ExcluirVersaoCurriculoEntrada) -> None:
        """Executa a exclusão interna da versão do solicitante.

        Implementações aplicam a verificação de propriedade sem definir respostas
        HTTP. O método existe para que o router se concentre em traduzir
        fronteiras.
        """


# Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
def criar_router(excluir_versao: ExclusaoVersaoCurriculoExecutor | None) -> APIRouter:
    """Cria a rota HTTP de exclusão usando o caso de uso injetado.

    A função converte as identidades de rota em entrada da Application e traduz
    a ausência da versão em status seguro. Ela existe para registrar a API e
    permitir testes unitários com doubles, sem sessão de banco real.

    Nota: a rota fica sob ``/estudantes/{usuario_id}/curriculos``, caminho que o
    middleware de autenticação, quando instalado, já protege exigindo sessão
    ativa do próprio estudante; a verificação de propriedade da versão continua
    no caso de uso, conforme
    prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md.
    """
    router = APIRouter()

    @router.delete(
        "/estudantes/{usuario_id}/curriculos/{curriculo_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def excluir(usuario_id: UUID, curriculo_id: UUID) -> None:
        """Executa a exclusão HTTP e responde sem conteúdo.

        O handler monta a entrada da Application a partir da rota, aguarda o caso
        de uso e traduz ausência ou propriedade alheia da versão, sem distinguir
        os dois casos. Ele existe para expor a exclusão sem levar HTTP à
        Application.
        """
        if excluir_versao is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Exclusão indisponível.")
        entrada = ExcluirVersaoCurriculoEntrada(
            usuario_id=UsuarioId(usuario_id),
            curriculo_id=CurriculoId(curriculo_id),
        )
        try:
            await excluir_versao.executar(entrada)
        except CurriculoNaoEncontrado as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro

    return router
