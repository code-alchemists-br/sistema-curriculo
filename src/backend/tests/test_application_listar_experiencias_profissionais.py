"""Verifica a listagem interna com porta substituída e dados determinísticos.

Exercita consulta única, ausência de mutações e delegação da ordem ao domínio
para proteger a leitura da coleção própria sem recursos externos.
"""

# Proveniência: decision-analysis prompts/backend/20261107-172902-listar-experiencias-profissionais-v001.md#v001
import unittest
from datetime import date
from itertools import permutations
from unittest.mock import create_autospec
from uuid import UUID

from backend.application import (
    ListarExperienciasProfissionais,
    ListarExperienciasProfissionaisEntrada,
)
from backend.application.ports import RepositorioExperienciaProfissional
from backend.domain.itens_perfil import ExperienciaProfissional, ordenar_experiencias
from backend.domain.value_objects import ExperienciaProfissionalId, Periodo, UsuarioId


class ListarExperienciasProfissionaisTestCase(unittest.IsolatedAsyncioTestCase):
    """Testa somente a orquestração usando um double da porta de experiências.

    Mantém datas e identidades fixas para conferir leitura única e ordem comum
    sem banco, ORM, framework, relógio ou gerador de identidades.
    """

    async def test_consulta_uma_vez_com_dono_e_devolve_vazio_sem_escrever(self):
        """Confere leitura vazia e dono da entrada usando spy da porta.

        Retorna lista vazia pelo double e verifica a tupla resultante e todas
        as chamadas para garantir que ausência de itens não cause escrita.
        """
        dono = UsuarioId(UUID(int=101))
        repositorio = create_autospec(RepositorioExperienciaProfissional, instance=True)
        repositorio.listar_ativas_por_usuario.return_value = []

        resultado = await ListarExperienciasProfissionais(repositorio).executar(
            ListarExperienciasProfissionaisEntrada(dono)
        )

        self.assertEqual(resultado, ())
        repositorio.listar_ativas_por_usuario.assert_called_once_with(dono)
        repositorio.listar_ativas_por_usuario.assert_awaited_once_with(dono)
        repositorio.salvar.assert_not_called()
        repositorio.atualizar.assert_not_called()
        repositorio.marcar_excluida.assert_not_called()
        self.assertEqual(len(repositorio.mock_calls), 1)

    async def test_ordena_por_dominio_independente_da_ordem_da_porta_sem_escrever(self):
        """Compara permutações com a ordem real usando inícios e fins variados.

        Inclui término nulo, términos diferentes e datas empatadas com IDs
        distintos; verifica que uma encerrada recente antecede uma em andamento
        antiga para impedir prioridade global indevida ao término nulo.
        """
        dono = UsuarioId(UUID(int=102))
        experiencias = tuple(
            ExperienciaProfissional(
                id=ExperienciaProfissionalId(UUID(int=indice)),
                usuario_id=dono,
                empresa="Empresa Local",
                cargo="Desenvolvedor",
                descricao="Desenvolvimento de aplicações.",
                periodo=Periodo(inicio, fim),
            )
            for indice, inicio, fim in (
                (1, date(2020, 1, 1), None),
                (2, date(2024, 1, 1), date(2025, 1, 1)),
                (3, date(2024, 1, 1), None),
                (4, date(2024, 1, 1), date(2026, 1, 1)),
                (5, date(2024, 1, 1), date(2026, 1, 1)),
            )
        )
        esperado = ordenar_experiencias(experiencias)
        entrada = ListarExperienciasProfissionaisEntrada(dono)
        repositorio = create_autospec(RepositorioExperienciaProfissional, instance=True)
        caso = ListarExperienciasProfissionais(repositorio)

        for ordem in permutations(experiencias):
            with self.subTest(ids=tuple(item.id.valor.int for item in ordem)):
                repositorio.reset_mock()
                repositorio.listar_ativas_por_usuario.return_value = list(ordem)

                resultado = await caso.executar(entrada)

                self.assertEqual(resultado, esperado)
                self.assertIsInstance(resultado, tuple)
                self.assertLess(resultado.index(experiencias[1]), resultado.index(experiencias[0]))
                repositorio.listar_ativas_por_usuario.assert_called_once_with(dono)
                repositorio.listar_ativas_por_usuario.assert_awaited_once_with(dono)
                repositorio.salvar.assert_not_called()
                repositorio.atualizar.assert_not_called()
                repositorio.marcar_excluida.assert_not_called()
                self.assertEqual(len(repositorio.mock_calls), 1)
