"""Verifica a listagem interna isolando a porta com doubles sem infraestrutura.

Exercita consulta, ausência de mutações e delegação da ordem ao domínio para
proteger o comportamento de leitura da coleção própria.
"""

# Proveniência: decision-analysis prompts/backend/20261107-171028-listar-formacoes-academicas-v001.md#v001
import unittest
from datetime import date
from itertools import permutations
from unittest.mock import create_autospec
from uuid import UUID

from backend.application import (
    ListarFormacoesAcademicas,
    ListarFormacoesAcademicasEntrada,
)
from backend.application.ports import RepositorioFormacaoAcademica
from backend.domain.itens_perfil import (
    FormacaoAcademica,
    NivelFormacaoAcademica,
    StatusFormacaoAcademica,
    ordenar_formacoes,
)
from backend.domain.value_objects import FormacaoAcademicaId, Periodo, UsuarioId


class ListarFormacoesAcademicasTestCase(unittest.IsolatedAsyncioTestCase):
    """Testa o caso com porta mockada para observar somente sua orquestração.

    Usa identidades e datas fixas para conferir consulta única e ordem estável
    sem depender de banco, relógio, geradores ou adapters produtivos.
    """

    async def test_consulta_uma_vez_com_dono_e_devolve_vazio_sem_escrever(self):
        """Confere leitura vazia usando spy da porta para impedir escritas.

        Envia o dono tipado e verifica todas as chamadas ao double, garantindo
        que ausência de formações seja representada por uma tupla vazia.
        """
        dono = UsuarioId(UUID(int=101))
        repositorio = create_autospec(RepositorioFormacaoAcademica, instance=True)
        repositorio.listar_ativas_por_usuario.return_value = []

        resultado = await ListarFormacoesAcademicas(repositorio).executar(
            ListarFormacoesAcademicasEntrada(dono)
        )

        self.assertEqual(resultado, ())
        repositorio.listar_ativas_por_usuario.assert_called_once_with(dono)
        repositorio.listar_ativas_por_usuario.assert_awaited_once_with(dono)
        repositorio.salvar.assert_not_called()
        repositorio.atualizar.assert_not_called()
        repositorio.marcar_excluida.assert_not_called()
        self.assertEqual(len(repositorio.mock_calls), 1)

    async def test_ordena_tres_status_e_empates_independente_da_ordem_da_porta(self):
        """Compara permutações à regra real com status e datas empatadas.

        Cria entidades com IDs distintos e dois itens empatados em cada status,
        verificando que a saída independe da sequência da porta e que o caso
        realiza somente a leitura, sem duplicar critérios de ordenação no teste.
        """
        dono = UsuarioId(UUID(int=102))
        formacoes = tuple(
            FormacaoAcademica(
                id=FormacaoAcademicaId(UUID(int=indice)),
                usuario_id=dono,
                instituicao="Universidade Local",
                curso="Computação",
                nivel=NivelFormacaoAcademica.GRADUACAO,
                periodo=Periodo(date(2020, 2, 1), date(2024, 12, 1)),
                status=status,
            )
            for indice, status in enumerate(
                (
                    StatusFormacaoAcademica.INTERROMPIDO,
                    StatusFormacaoAcademica.CONCLUIDO,
                    StatusFormacaoAcademica.EM_ANDAMENTO,
                    StatusFormacaoAcademica.INTERROMPIDO,
                    StatusFormacaoAcademica.CONCLUIDO,
                    StatusFormacaoAcademica.EM_ANDAMENTO,
                ),
                start=1,
            )
        )
        esperado = ordenar_formacoes(formacoes)
        entrada = ListarFormacoesAcademicasEntrada(dono)
        repositorio = create_autospec(RepositorioFormacaoAcademica, instance=True)
        caso = ListarFormacoesAcademicas(repositorio)

        for ordem in permutations(formacoes):
            with self.subTest(ids=tuple(item.id.valor.int for item in ordem)):
                repositorio.reset_mock()
                repositorio.listar_ativas_por_usuario.return_value = list(ordem)

                resultado = await caso.executar(entrada)

                self.assertEqual(resultado, esperado)
                repositorio.listar_ativas_por_usuario.assert_called_once_with(dono)
                repositorio.listar_ativas_por_usuario.assert_awaited_once_with(dono)
                repositorio.salvar.assert_not_called()
                repositorio.atualizar.assert_not_called()
                repositorio.marcar_excluida.assert_not_called()
                self.assertEqual(len(repositorio.mock_calls), 1)
