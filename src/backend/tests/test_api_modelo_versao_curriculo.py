"""Testa unitariamente a seleção do modelo no contrato HTTP de edição de versão."""

import unittest
from uuid import uuid4

from fastapi import APIRouter
from pydantic import ValidationError

# Proveniência: decision-analysis prompts/backend/20261017-140000-modelo-curriculo-edicao-versao-v001.md#v001
from backend.api.factory import create_app
from backend.api.versao_curriculo import EditarVersaoCurriculoRequisicao, criar_router
from backend.application import EditarVersaoCurriculo
from backend.domain import Curriculo, CurriculoId, UsuarioId

CAMINHO = "/estudantes/{usuario_id}/curriculos/{curriculo_id}"


class RepositorioCurriculoSpy:
    """Substitui a porta de currículo e registra atualizações solicitadas.

    O double consulta agregados em memória por ID e acumula os estados
    atualizados. Ele existe para exercitar o caso de uso real de edição através
    da rota, sem ORM, banco ou rede.
    """

    def __init__(self, curriculo: Curriculo) -> None:
        """Guarda a versão que o double devolverá e inicia o histórico vazio.

        O construtor não acessa recursos externos. Ele existe para controlar a
        versão existente no cenário testado.
        """
        self._curriculo = curriculo
        self.curriculos_atualizados: list[Curriculo] = []

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Devolve por coroutine a versão guardada se o ID coincidir.

        O método compara somente em memória e não faz I/O. Ele existe para
        simular a leitura aguardável exigida pelo caso de uso.
        """
        return self._curriculo if self._curriculo.id == curriculo_id else None

    async def atualizar(self, curriculo: Curriculo) -> None:
        """Registra por coroutine o novo estado solicitado pela Application.

        O método acumula o agregado sem persistir. Ele existe para tornar
        observável o estado gravado pela rota.
        """
        self.curriculos_atualizados.append(curriculo)


def _rota(router: APIRouter, caminho: str, metodo: str):
    """Localiza o endpoint de uma rota registrada para chamada direta em teste.

    A função varre as rotas do router por caminho e método HTTP e devolve a
    função assíncrona decorada. Ela existe para exercitar o handler sem
    iniciar servidor ASGI.
    """
    for rota in router.routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota.endpoint
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


class ModeloVersaoCurriculoApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica como a API recebe e expõe o modelo na edição da versão.

    Os testes cobrem a validação do corpo, o texto simples que chega ao caso de
    uso e a listagem dos modelos no OpenAPI. A classe existe para proteger o
    contrato HTTP de seleção do modelo.
    """

    def test_corpo_recusa_modelo_desconhecido(self) -> None:
        """Confirma que o DTO recusa um modelo fora do vocabulário.

        O teste constrói o corpo com um modelo inexistente e espera a falha de
        validação da fronteira. Ele existe para que a recusa ocorra antes do
        caso de uso.
        """
        with self.assertRaises(ValidationError):
            EditarVersaoCurriculoRequisicao(
                titulo_versao="Gestão", layout="moderno", is_public=True
            )

    def test_corpo_aceita_cada_modelo_suportado(self) -> None:
        """Confirma que o DTO aceita os modelos clássico e compacto.

        O teste constrói o corpo com cada identificador e confere o valor
        textual. Ele existe para garantir o caminho de sucesso da fronteira.
        """
        for modelo in ("classico", "compacto"):
            with self.subTest(modelo=modelo):
                corpo = EditarVersaoCurriculoRequisicao(
                    titulo_versao="Gestão", layout=modelo, is_public=True
                )

                self.assertEqual(corpo.layout.value, modelo)

    async def test_rota_grava_o_modelo_escolhido_como_texto_simples(self) -> None:
        """Confirma que a rota grava o modelo escolhido como texto simples.

        O teste edita a versão pelo handler com o caso de uso real e confere o
        modelo gravado e devolvido, e que o valor é ``str`` e não a enumeração.
        Ele existe para que o agregado e a persistência continuem recebendo
        texto.
        """
        usuario_id = UsuarioId(uuid4())
        curriculo = Curriculo(
            id=CurriculoId(uuid4()),
            usuario_id=usuario_id,
            titulo_versao="Estágio em TI",
            layout="classico",
            is_public=False,
        )
        repositorio = RepositorioCurriculoSpy(curriculo)
        editar = _rota(criar_router(EditarVersaoCurriculo(repositorio)), CAMINHO, "PUT")

        resposta = await editar(
            usuario_id=usuario_id.valor,
            curriculo_id=curriculo.id.valor,
            requisicao=EditarVersaoCurriculoRequisicao(
                titulo_versao="Gestão", layout="compacto", is_public=True
            ),
        )

        self.assertEqual(resposta.layout, "compacto")
        self.assertIs(type(repositorio.curriculos_atualizados[0].layout), str)

    def test_openapi_lista_os_modelos_aceitos(self) -> None:
        """Confirma que o OpenAPI expõe os modelos aceitos na edição.

        O teste lê o esquema gerado pela aplicação e confere os valores da
        enumeração de modelos e o uso dela no corpo da edição. Ele existe para
        que o contrato publique quais modelos podem ser escolhidos.
        """
        esquemas = create_app().openapi()["components"]["schemas"]

        self.assertEqual(
            sorted(esquemas["ModeloCurriculo"]["enum"]), ["classico", "compacto"]
        )
        self.assertIn(
            "ModeloCurriculo",
            str(esquemas["EditarVersaoCurriculoRequisicao"]["properties"]["layout"]),
        )
