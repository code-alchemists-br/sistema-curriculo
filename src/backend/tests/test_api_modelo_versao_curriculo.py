"""Testa unitariamente a seleção do modelo no contrato HTTP de edição de versão."""

import unittest
from uuid import uuid4

from fastapi import APIRouter
from pydantic import ValidationError

from backend.api.factory import create_app
from backend.api.versao_curriculo import (
    EditarVersaoCurriculoRequisicao,
    criar_router,
)
from backend.application import EditarVersaoCurriculo
from backend.domain import Curriculo, CurriculoId, UsuarioId

CAMINHO = "/estudantes/{usuario_id}/curriculos/{curriculo_id}"


class RepositorioCurriculoSpy:
    """Substitui a porta de currículo e registra atualizações solicitadas."""

    def __init__(self, curriculo: Curriculo) -> None:
        """Guarda a versão que o double devolverá e inicia o histórico vazio."""
        self._curriculo = curriculo
        self.curriculos_atualizados: list[Curriculo] = []

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Devolve por coroutine a versão guardada se o ID coincidir."""
        return self._curriculo if self._curriculo.id == curriculo_id else None

    async def atualizar(self, curriculo: Curriculo) -> None:
        """Registra por coroutine o novo estado solicitado pela Application."""
        self.curriculos_atualizados.append(curriculo)


def _rota(router: APIRouter, caminho: str, metodo: str):
    """Localiza o endpoint de uma rota registrada para chamada direta em teste."""
    for rota in router.routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota.endpoint
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


class ModeloVersaoCurriculoApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica como a API recebe e expõe o modelo na edição da versão."""

    def test_corpo_recusa_modelo_desconhecido(self) -> None:
        """Confirma que o DTO recusa um modelo fora do vocabulário."""
        with self.assertRaises(ValidationError):
            EditarVersaoCurriculoRequisicao(
                titulo_versao="Gestão",
                layout="inexistente",
                is_public=True,
            )

    def test_corpo_aceita_cada_modelo_suportado(self) -> None:
        """Confirma que o DTO de edição aceita o catálogo completo."""
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
                corpo = EditarVersaoCurriculoRequisicao(
                    titulo_versao="Gestão",
                    layout=modelo,
                    is_public=True,
                )

                self.assertEqual(corpo.layout.value, modelo)

    async def test_rota_grava_o_modelo_escolhido_como_texto_simples(self) -> None:
        """Confirma que a rota grava o modelo escolhido como texto simples."""
        usuario_id = UsuarioId(uuid4())
        curriculo = Curriculo(
            id=CurriculoId(uuid4()),
            usuario_id=usuario_id,
            titulo_versao="Estágio em TI",
            layout="classico",
            is_public=False,
        )
        repositorio = RepositorioCurriculoSpy(curriculo)
        editar = _rota(
            criar_router(EditarVersaoCurriculo(repositorio)),
            CAMINHO,
            "PUT",
        )

        resposta = await editar(
            usuario_id=usuario_id.valor,
            curriculo_id=curriculo.id.valor,
            requisicao=EditarVersaoCurriculoRequisicao(
                titulo_versao="Gestão",
                layout="academico",
                is_public=True,
            ),
        )

        self.assertEqual(resposta.layout, "academico")
        self.assertIs(type(repositorio.curriculos_atualizados[0].layout), str)

    def test_openapi_lista_os_modelos_aceitos(self) -> None:
        """Confirma que o OpenAPI expõe todos os modelos aceitos na edição."""
        esquemas = create_app().openapi()["components"]["schemas"]

        self.assertEqual(
            sorted(esquemas["ModeloCurriculo"]["enum"]),
            [
                "academico",
                "ats-simples",
                "classico",
                "compacto",
                "criativo",
                "moderno",
                "primeiro-emprego",
            ],
        )
        self.assertIn(
            "ModeloCurriculo",
            str(
                esquemas["EditarVersaoCurriculoRequisicao"]["properties"][
                    "layout"
                ]
            ),
        )
