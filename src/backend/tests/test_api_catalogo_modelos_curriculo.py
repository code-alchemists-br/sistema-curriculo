"""Testa o catálogo fechado também no fluxo HTTP de criação de currículo."""

import unittest
from uuid import uuid4

from fastapi import APIRouter
from pydantic import ValidationError

from backend.api.versao_curriculo import (
    CriarVersaoCurriculoRequisicao,
    VersaoCurriculoResposta,
    criar_router,
)
from backend.application import CriarVersaoCurriculoEntrada
from backend.domain import Curriculo, CurriculoId, UsuarioId

CAMINHO = "/estudantes/{usuario_id}/curriculos"


class CriarVersaoExecutorSpy:
    """Registra a entrada de criação e devolve o currículo configurado."""

    def __init__(self, resultado: Curriculo) -> None:
        """Guarda o resultado e inicia o histórico de entradas recebidas."""
        self._resultado = resultado
        self.entradas: list[CriarVersaoCurriculoEntrada] = []

    async def executar(self, entrada: CriarVersaoCurriculoEntrada) -> Curriculo:
        """Registra a entrada sem I/O e devolve o resultado pré-configurado."""
        self.entradas.append(entrada)
        return self._resultado


def _rota(router: APIRouter):
    """Obtém o endpoint POST de criação sem iniciar um servidor ASGI."""
    for rota in router.routes:
        if rota.path == CAMINHO and "POST" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota POST de criação não encontrada.")


class CatalogoModelosNaCriacaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Garante que criação e edição partilham o mesmo catálogo de modelos."""

    def test_requisicao_aceita_o_catalogo_e_recusa_valor_desconhecido(self) -> None:
        """Valida cada identificador e a recusa antes de o caso de uso ser chamado."""
        for modelo in (
            "classico",
            "compacto",
            "ats-simples",
            "criativo",
            "moderno",
            "academico",
            "primeiro-emprego",
        ):
            with self.subTest(modelo=modelo):
                requisicao = CriarVersaoCurriculoRequisicao(
                    titulo_versao="Estágio em TI",
                    layout=modelo,
                )

                self.assertEqual(requisicao.layout.value, modelo)

        with self.assertRaises(ValidationError):
            CriarVersaoCurriculoRequisicao(
                titulo_versao="Estágio em TI",
                layout="inexistente",
            )

    async def test_rota_entrega_o_identificador_textual_ao_caso_de_uso(self) -> None:
        """Confirma que a enumeração HTTP não vaza para a entrada da Application."""
        usuario_id = UsuarioId(uuid4())
        curriculo = Curriculo(
            id=CurriculoId(uuid4()),
            usuario_id=usuario_id,
            titulo_versao="Estágio em TI",
            layout="primeiro-emprego",
            is_public=False,
        )
        executor = CriarVersaoExecutorSpy(curriculo)
        criar = _rota(criar_router(None, executor))

        resposta: VersaoCurriculoResposta = await criar(
            usuario_id=usuario_id.valor,
            requisicao=CriarVersaoCurriculoRequisicao(
                titulo_versao="Estágio em TI",
                layout="primeiro-emprego",
            ),
        )

        self.assertEqual(executor.entradas[0].layout, "primeiro-emprego")
        self.assertEqual(resposta.layout, "primeiro-emprego")
