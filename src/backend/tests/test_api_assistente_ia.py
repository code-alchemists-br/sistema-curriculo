"""Testa a fronteira HTTP do assistente de IA (revisão e recomendação)."""

import unittest
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from backend.api.assistente_ia import (
    InformacaoRequisicao,
    RecomendacaoRequisicao,
    RevisaoRequisicao,
    criar_router,
)
from backend.application.recomendacao_modelo import (
    RecomendacaoModelo,
    RecomendadorModeloIndisponivel,
)
from backend.application.revisao_texto import (
    CampoRevisavel,
    RevisaoTexto,
    RevisorTextoIndisponivel,
    SituacaoTexto,
)
from backend.domain.modelo_curriculo import ModeloCurriculo

USUARIO = UUID("00000000-0000-0000-0000-0000000000c1")


def _rota(router: APIRouter, caminho: str):
    """Localiza o handler POST registrado no caminho informado.

    Existe para chamar o handler diretamente, sem servidor.
    """
    for rota in router.routes:
        if rota.path == caminho and "POST" in rota.methods:
            return rota.endpoint
    raise AssertionError(f"Rota POST {caminho} não encontrada.")


def _request() -> Request:
    """Monta uma requisição mínima com o estudante autenticado no estado.

    Existe para simular o que o middleware de sessão instala.
    """
    request = Request({"type": "http", "method": "POST", "path": "/", "headers": []})
    request.state.usuario_id = USUARIO
    return request


class RevisarFalso:
    """Substitui o caso de uso de revisão por resposta ou falha configurada.

    Existe para testar a tradução HTTP sem IA real.
    """

    def __init__(self, falhar: bool = False) -> None:
        """Escolhe se a revisão falha e prepara o histórico de chamadas.

        Existe para que cada teste simule sucesso ou indisponibilidade.
        """
        self.falhar = falhar
        self.chamadas: list[tuple] = []

    async def executar(self, campo, texto, pergunta=None, contexto=None) -> RevisaoTexto:
        """Registra a chamada e devolve uma revisão válida ou falha.

        Existe para conferir os argumentos repassados pelo handler.
        """
        self.chamadas.append((campo, texto, pergunta, contexto))
        if self.falhar:
            raise RevisorTextoIndisponivel("Sem chave.")
        return RevisaoTexto(
            situacao=SituacaoTexto.VALIDO, motivo="Ok.", sugestoes=[], pode_manter_texto=True
        )


class RecomendarFalso:
    """Substitui o caso de uso de recomendação por resposta ou falha configurada.

    Existe para testar a tradução HTTP de sucesso, perfil vazio e indisponível.
    """

    def __init__(self, erro: Exception | None = None) -> None:
        """Escolhe a falha simulada e prepara o histórico de chamadas.

        Existe para que cada teste simule um resultado diferente.
        """
        self.erro = erro
        self.chamadas: list[tuple] = []

    async def executar(self, usuario_id, extras=None) -> RecomendacaoModelo:
        """Registra a chamada e devolve uma recomendação ou lança a falha.

        Existe para conferir que o handler usa o estudante da sessão.
        """
        self.chamadas.append((usuario_id, extras))
        if self.erro:
            raise self.erro
        return RecomendacaoModelo(
            modelo=ModeloCurriculo.CLASSICO, motivo="Perfil formal.", alternativa=None
        )


class RevisaoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica ``POST /assistente/revisoes``.

    Existe para garantir o repasse dos dados e a tradução das falhas em 503.
    """

    async def test_repassa_campo_texto_pergunta_e_contexto(self) -> None:
        """Encaminha os dados do corpo ao caso de uso e devolve a revisão.

        Existe para proteger o contrato entre tela e caso de uso.
        """
        caso = RevisarFalso()
        revisar = _rota(criar_router(caso, None), "/assistente/revisoes")

        resposta = await revisar(
            RevisaoRequisicao(
                campo=CampoRevisavel.DESCRICAO_PROJETO,
                texto="Fiz um app.",
                pergunta="O que você fez?",
                contexto={"titulo": "App"},
            )
        )

        self.assertEqual(resposta.situacao, SituacaoTexto.VALIDO)
        self.assertEqual(
            caso.chamadas,
            [(CampoRevisavel.DESCRICAO_PROJETO, "Fiz um app.", "O que você fez?", {"titulo": "App"})],
        )

    async def test_ia_indisponivel_vira_503(self) -> None:
        """Responde 503 quando o provedor de IA falha.

        Existe para que a tela siga sem revisão em vez de travar.
        """
        revisar = _rota(criar_router(RevisarFalso(falhar=True), None), "/assistente/revisoes")

        with self.assertRaises(HTTPException) as contexto:
            await revisar(RevisaoRequisicao(campo=CampoRevisavel.OUTRO, texto="x"))

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_sem_caso_de_uso_responde_503(self) -> None:
        """Responde 503 quando a composição não injetou a revisão.

        Existe para que a API suba mesmo sem o assistente configurado.
        """
        revisar = _rota(criar_router(None, None), "/assistente/revisoes")

        with self.assertRaises(HTTPException) as contexto:
            await revisar(RevisaoRequisicao(campo=CampoRevisavel.OUTRO, texto="x"))

        self.assertEqual(contexto.exception.status_code, 503)


class RecomendacaoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica ``POST /assistente/recomendacao-modelo``.

    Existe para garantir o uso do estudante da sessão e a tradução de erros.
    """

    async def test_usa_estudante_da_sessao_e_extras(self) -> None:
        """Encaminha o usuário da sessão e converte os extras do corpo.

        Existe para impedir que o dono venha do payload.
        """
        caso = RecomendarFalso()
        recomendar = _rota(criar_router(None, caso), "/assistente/recomendacao-modelo")

        resposta = await recomendar(
            RecomendacaoRequisicao(extras=[InformacaoRequisicao(pergunta="Objetivo", resposta="Estágio")]),
            _request(),
        )

        self.assertEqual(resposta.modelo, ModeloCurriculo.CLASSICO)
        usuario, extras = caso.chamadas[0]
        self.assertEqual(usuario, USUARIO)
        self.assertEqual((extras[0].pergunta, extras[0].resposta), ("Objetivo", "Estágio"))

    async def test_perfil_vazio_vira_422_e_ia_indisponivel_vira_503(self) -> None:
        """Traduz perfil vazio em 422 e falha do provedor em 503.

        Existe para que a tela mostre o motivo certo ao estudante.
        """
        for erro, status in ((ValueError("vazio"), 422), (RecomendadorModeloIndisponivel("off"), 503)):
            with self.subTest(status=status):
                recomendar = _rota(
                    criar_router(None, RecomendarFalso(erro)), "/assistente/recomendacao-modelo"
                )
                with self.assertRaises(HTTPException) as contexto:
                    await recomendar(RecomendacaoRequisicao(), _request())
                self.assertEqual(contexto.exception.status_code, status)


if __name__ == "__main__":
    unittest.main()
