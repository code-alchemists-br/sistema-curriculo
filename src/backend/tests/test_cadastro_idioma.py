"""Testa unitariamente o caso de uso de cadastro de idioma."""

import unittest
from uuid import uuid4

from backend.application.cadastro_idioma import (
    CadastrarIdioma,
    CadastrarIdiomaEntrada,
)
from backend.domain.itens_perfil import Idioma
from backend.domain.value_objects import IdiomaId, UsuarioId


class RepositorioIdiomaSpy:
    """Substitui assincronamente a porta e regista os idiomas persistidos."""

    def __init__(self) -> None:
        self.idiomas_salvos: list[Idioma] = []

    async def salvar(self, idioma: Idioma) -> None:
        self.idiomas_salvos.append(idioma)


class GeradorIdiomaIdStub:
    """Substitui a geração de ID por uma identidade determinística."""

    def __init__(self, idioma_id: IdiomaId) -> None:
        self._idioma_id = idioma_id
        self.chamadas = 0

    def gerar(self) -> IdiomaId:
        self.chamadas += 1
        return self._idioma_id


class CadastrarIdiomaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a orquestração do cadastro de idioma."""

    async def test_cadastra_idioma_e_solicita_salvamento_com_sucesso(self) -> None:
        idioma_id = IdiomaId(uuid4())
        usuario_id = UsuarioId(uuid4())
        repositorio = RepositorioIdiomaSpy()
        gerador = GeradorIdiomaIdStub(idioma_id)
        caso_de_uso = CadastrarIdioma(repositorio, gerador)

        entrada = CadastrarIdiomaEntrada(
            usuario_id=usuario_id,
            idioma="Inglês",
            nivel="Avançado",
        )

        idioma = await caso_de_uso.executar(entrada)

        self.assertEqual(idioma.id, idioma_id)
        self.assertEqual(idioma.usuario_id, usuario_id)
        self.assertEqual(idioma.idioma, "Inglês")
        self.assertEqual(idioma.nivel, "Avançado")
        self.assertEqual(repositorio.idiomas_salvos, [idioma])
        self.assertEqual(gerador.chamadas, 1)