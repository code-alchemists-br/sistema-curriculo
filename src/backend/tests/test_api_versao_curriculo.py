"""Testa unitariamente a rota HTTP de edição de versão de currículo."""

import unittest
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from backend.api.versao_curriculo import EditarVersaoCurriculoRequisicao, criar_router
from backend.application import EditarVersaoCurriculo
from backend.domain import Curriculo, CurriculoId, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001

CAMINHO = "/estudantes/{usuario_id}/curriculos/{curriculo_id}"


class RepositorioCurriculoSpy:
    """Substitui a porta de currículo e registra atualizações solicitadas.

    O double consulta agregados em memória por ID e acumula os estados
    atualizados. Ele existe para exercitar o caso de uso real de edição através
    da rota HTTP, sem ORM, banco, rede ou adapter produtivo.
    """

    def __init__(self, curriculos: list[Curriculo] | None = None) -> None:
        """Prepara um índice em memória e um histórico vazio de atualizações.

        O construtor copia os currículos fornecidos em um dicionário por
        identidade. Ele existe para controlar ausência e propriedade em cada
        cenário testado pela rota.
        """
        self._por_id = {curriculo.id: curriculo for curriculo in (curriculos or [])}
        self.curriculos_atualizados: list[Curriculo] = []

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Devolve por coroutine a versão associada ao ID informado.

        O método consulta somente o dicionário controlado pelo teste e não faz
        I/O. Ele existe para simular a leitura aguardável exigida pelo caso.
        """
        return self._por_id.get(curriculo_id)

    async def atualizar(self, curriculo: Curriculo) -> None:
        """Registra por coroutine o novo estado solicitado pela Application.

        O método acumula o agregado sem persistir ou iniciar transação. Ele
        existe para tornar observável se e quando a rota gerou efeito real.
        """
        self.curriculos_atualizados.append(curriculo)


def _rota(router: APIRouter, caminho: str, metodo: str):
    """Localiza o endpoint de uma rota registrada para chamada direta em teste.

    A função varre as rotas do router por caminho e método HTTP e devolve a
    função assíncrona decorada. Ela existe para exercitar o handler sem
    iniciar servidor ASGI ou depender de cliente HTTP real.
    """
    for rota in router.routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota.endpoint
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


def _criar_curriculo() -> Curriculo:
    """Cria uma versão de currículo válida para popular o repositório double.

    A função monta o agregado sem acessar gerador, banco ou relógio. Ela existe
    para reduzir repetição mantendo cada teste focado na tradução HTTP.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=UsuarioId(uuid4()),
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


class EditarVersaoCurriculoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a rota PUT integrada ao caso de uso real ``EditarVersaoCurriculo``.

    A classe compõe o router com o caso de uso verdadeiro e substitui apenas a
    porta de repositório. Ela existe para comprovar que a composição feita por
    ``factory.py`` traduz corretamente o resultado e as falhas do caso de uso.
    """

    async def test_edita_versao_e_devolve_dados_publicos(self) -> None:
        """Confirma resposta pública e atualização real via repositório double.

        O teste monta uma versão do solicitante, chama o handler HTTP e compara
        a resposta pública com o efeito observado no double de repositório.
        """
        curriculo = _criar_curriculo()
        repositorio = RepositorioCurriculoSpy([curriculo])
        editar = _rota(criar_router(EditarVersaoCurriculo(repositorio)), CAMINHO, "PUT")

        resposta = await editar(
            usuario_id=curriculo.usuario_id.valor,
            curriculo_id=curriculo.id.valor,
            requisicao=EditarVersaoCurriculoRequisicao(
                titulo_versao="Gestão de Projetos",
                layout="moderno",
                is_public=True,
            ),
        )

        self.assertEqual(resposta.id, curriculo.id.valor)
        self.assertEqual(resposta.titulo_versao, "Gestão de Projetos")
        self.assertEqual(resposta.layout, "moderno")
        self.assertTrue(resposta.is_public)
        self.assertEqual(repositorio.curriculos_atualizados, [curriculo])

    async def test_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum caso de uso de edição foi injetado.

        O teste chama o handler sem compor nenhum ``EditarVersaoCurriculo`` real
        e observa a indisponibilidade explícita antes de qualquer regra.
        """
        editar = _rota(criar_router(None), CAMINHO, "PUT")

        with self.assertRaises(HTTPException) as contexto:
            await editar(
                usuario_id=uuid4(),
                curriculo_id=uuid4(),
                requisicao=EditarVersaoCurriculoRequisicao(titulo_versao="X", layout="Y", is_public=True),
            )

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_titulo_em_branco_vira_422_sem_efeito_no_repositorio(self) -> None:
        """Confirma 422 quando o título fere a regra de domínio, sem alterar nada.

        O teste envia um título só com espaços, que passa pelo DTO mas é recusado
        pelo domínio, e observa o agregado intacto e o repositório sem
        atualização.
        """
        curriculo = _criar_curriculo()
        repositorio = RepositorioCurriculoSpy([curriculo])
        editar = _rota(criar_router(EditarVersaoCurriculo(repositorio)), CAMINHO, "PUT")

        with self.assertRaises(HTTPException) as contexto:
            await editar(
                usuario_id=curriculo.usuario_id.valor,
                curriculo_id=curriculo.id.valor,
                requisicao=EditarVersaoCurriculoRequisicao(titulo_versao="   ", layout="moderno", is_public=True),
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(curriculo.titulo_versao, "Estágio em TI")
        self.assertEqual(repositorio.curriculos_atualizados, [])

    async def test_versao_inexistente_vira_404(self) -> None:
        """Confirma 404 quando o repositório double não conhece a versão.

        O teste usa um repositório vazio e observa a tradução HTTP da falha de
        ausência produzida pelo caso de uso real.
        """
        repositorio = RepositorioCurriculoSpy()
        editar = _rota(criar_router(EditarVersaoCurriculo(repositorio)), CAMINHO, "PUT")

        with self.assertRaises(HTTPException) as contexto:
            await editar(
                usuario_id=uuid4(),
                curriculo_id=uuid4(),
                requisicao=EditarVersaoCurriculoRequisicao(titulo_versao="Gestão", layout="moderno", is_public=True),
            )

        self.assertEqual(contexto.exception.status_code, 404)
        self.assertEqual(repositorio.curriculos_atualizados, [])

    async def test_versao_de_outro_usuario_vira_404_sem_alterar_nem_atualizar(self) -> None:
        """Confirma que a versão de outro usuário é negada como se não existisse.

        O teste informa na rota um solicitante diferente do dono e exige a mesma
        resposta da ausência, sem alteração do agregado nem atualização. Ele
        existe para proteger currículos alheios conforme a verificação de
        propriedade.
        """
        curriculo = _criar_curriculo()
        repositorio = RepositorioCurriculoSpy([curriculo])
        editar = _rota(criar_router(EditarVersaoCurriculo(repositorio)), CAMINHO, "PUT")

        with self.assertRaises(HTTPException) as contexto:
            await editar(
                usuario_id=uuid4(),
                curriculo_id=curriculo.id.valor,
                requisicao=EditarVersaoCurriculoRequisicao(titulo_versao="Invasor", layout="moderno", is_public=True),
            )

        self.assertEqual(contexto.exception.status_code, 404)
        self.assertEqual(curriculo.titulo_versao, "Estágio em TI")
        self.assertFalse(curriculo.is_public)
        self.assertEqual(repositorio.curriculos_atualizados, [])
