"""Testa unitariamente os casos de uso de listagem e exclusão de competências.

O módulo valida que a listagem de competências recupere as entidades associadas
ao estudante e que a exclusão exija correspondência com o usuário autenticado,
levantando CompetenciaNaoEncontrada quando o registro não existir ou pertencer a
terceiros. Ele existe para proteger a reversibilidade e o isolamento de dados
do estudante no nível da Application.
"""

import unittest
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from backend.application.competencia import (
    CompetenciaNaoEncontrada,
    ExcluirCompetencia,
    ExcluirCompetenciaEntrada,
    ListarCompetencias,
    ListarCompetenciasEntrada,
)
from backend.application.ports import RepositorioCompetencia
from backend.domain.itens_perfil import CategoriaCompetencia, Competencia
from backend.domain.value_objects import CompetenciaId, UsuarioId

ID_COMPETENCIA = CompetenciaId(UUID("11111111-1111-4111-8111-111111111111"))
ID_USUARIO = UsuarioId(UUID("22222222-2222-4222-8222-222222222222"))


def _criar_competencia() -> Competencia:
    """Cria uma competência determinística para testes unitários.

    Como faz: instancia Competencia com IDs fixos, categoria técnica e nível.
    Qual finalidade atende: isola testes de aplicação sem depender de geradores.
    """
    return Competencia(
        id=ID_COMPETENCIA,
        usuario_id=ID_USUARIO,
        categoria=CategoriaCompetencia.TECNICA,
        descricao="Python",
        nivel="Avançado",
    )


class ListarCompetenciasTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o caso de uso de listagem de competências do estudante."""

    async def test_lista_competencias_pertencentes_ao_estudante(self) -> None:
        """Verifica que o caso de uso repassa a tupla de competências do repositório.

        Como faz: instancia o caso com double de RepositorioCompetencia e
        valida que o retorno corresponde exatamente aos itens obtidos.
        Qual finalidade atende: garante que a Application entregue a lista
        de habilidades do estudante sem mutações indevidas.
        """
        repositorio = Mock(spec=RepositorioCompetencia)
        esperado = (_criar_competencia(),)
        repositorio.listar_por_usuario = AsyncMock(return_value=esperado)

        caso = ListarCompetencias(repositorio)
        resultado = await caso.executar(ListarCompetenciasEntrada(ID_USUARIO))

        self.assertEqual(resultado, esperado)
        repositorio.listar_por_usuario.assert_awaited_once_with(ID_USUARIO)


class ExcluirCompetenciaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o caso de uso de exclusão de competência com garantia de autoria."""

    async def test_exclui_competencia_com_sucesso_quando_pertence_ao_estudante(
        self,
    ) -> None:
        """Verifica a exclusão quando o repositório confirma remoção da linha.

        Como faz: configura o double para retornar True no método excluir()
        e verifica a chamada assíncrona com os IDs corretos.
        Qual finalidade atende: confirma que o fluxo de deleção tem êxito
        quando os critérios de propriedade são atendidos.
        """
        repositorio = Mock(spec=RepositorioCompetencia)
        repositorio.excluir = AsyncMock(return_value=True)

        caso = ExcluirCompetencia(repositorio)
        await caso.executar(ExcluirCompetenciaEntrada(ID_COMPETENCIA, ID_USUARIO))

        repositorio.excluir.assert_awaited_once_with(ID_COMPETENCIA, ID_USUARIO)

    async def test_lanca_competencia_nao_encontrada_quando_registro_nao_existe(
        self,
    ) -> None:
        """Verifica que falha de remoção é traduzida em CompetenciaNaoEncontrada.

        Como faz: simula retorno False do repositório e verifica que o caso
        de uso dispara CompetenciaNaoEncontrada.
        Qual finalidade atende: impede respostas falsas de sucesso para IDs
        inexistentes ou de terceiros.
        """
        repositorio = Mock(spec=RepositorioCompetencia)
        repositorio.excluir = AsyncMock(return_value=False)

        caso = ExcluirCompetencia(repositorio)
        with self.assertRaises(CompetenciaNaoEncontrada) as contexto:
            await caso.executar(ExcluirCompetenciaEntrada(ID_COMPETENCIA, ID_USUARIO))

        self.assertEqual(str(contexto.exception), "Competência não encontrada.")
        repositorio.excluir.assert_awaited_once_with(ID_COMPETENCIA, ID_USUARIO)
