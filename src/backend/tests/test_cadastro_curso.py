"""Testa unitariamente o caso de uso de cadastro de curso complementar."""

import unittest
from uuid import uuid4

from backend.application.cadastro_curso import (
    CadastrarCurso,
    CadastrarCursoEntrada,
)
from backend.domain.itens_perfil import Curso
from backend.domain.value_objects import CursoId, UsuarioId


class RepositorioCursoSpy:
    """Substitui assincronamente a porta e regista os cursos persistidos."""

    def __init__(self) -> None:
        self.cursos_salvos: list[Curso] = []

    async def salvar(self, curso: Curso) -> None:
        self.cursos_salvos.append(curso)


class GeradorCursoIdStub:
    """Substitui a geração de ID por uma identidade determinística."""

    def __init__(self, curso_id: CursoId) -> None:
        self._curso_id = curso_id
        self.chamadas = 0

    def gerar(self) -> CursoId:
        self.chamadas += 1
        return self._curso_id


class CadastrarCursoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a orquestração do cadastro de curso complementar."""

    async def test_cadastra_curso_e_solicita_salvamento_com_sucesso(self) -> None:
        curso_id = CursoId(uuid4())
        usuario_id = UsuarioId(uuid4())
        repositorio = RepositorioCursoSpy()
        gerador = GeradorCursoIdStub(curso_id)
        caso_de_uso = CadastrarCurso(repositorio, gerador)

        entrada = CadastrarCursoEntrada(
            usuario_id=usuario_id,
            nome="Python Avançado",
            instituicao="Escola Tech",
            carga_horaria=40,
        )

        curso = await caso_de_uso.executar(entrada)

        self.assertEqual(curso.id, curso_id)
        self.assertEqual(curso.usuario_id, usuario_id)
        self.assertEqual(curso.nome, "Python Avançado")
        self.assertEqual(curso.instituicao, "Escola Tech")
        self.assertEqual(curso.carga_horaria, 40)
        self.assertEqual(repositorio.cursos_salvos, [curso])
        self.assertEqual(gerador.chamadas, 1)