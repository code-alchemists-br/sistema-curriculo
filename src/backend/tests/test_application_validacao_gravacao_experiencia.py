"""Testa gravações com tempo e persistência substituídos por doubles locais.

Verifica fuso civil, consulta escopada, normalização e ausência de mutações em
falhas para isolar a orquestração das gravações de qualquer infraestrutura.
"""

# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
import unittest
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from unittest.mock import Mock, call, create_autospec
from uuid import UUID

from backend.application.cadastro_experiencia_profissional import (
    CadastrarExperienciaProfissional,
    CadastrarExperienciaProfissionalEntrada,
)
from backend.application.edicao_experiencia_profissional import (
    EditarExperienciaProfissional,
    EditarExperienciaProfissionalEntrada,
    ExperienciaProfissionalNaoEncontrada,
)
from backend.application.ports import (
    GeradorExperienciaProfissionalId,
    Relogio,
    RepositorioExperienciaProfissional,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import ExperienciaProfissionalId, Periodo, UsuarioId

HOJE = date(2026, 11, 7)
INSTANTE = datetime(2026, 11, 7, 12, tzinfo=timezone.utc)
DONO = UsuarioId(UUID(int=101))
IDENTIDADE = ExperienciaProfissionalId(UUID(int=1))


def preparar_caso(modo, **alteracoes):
    """Monta um caso real com todas as portas substituídas e entrada determinística.

    Prepara uma entidade estrutural de referência e doubles com histórico para
    conferir a orquestração de cadastro ou edição sem banco, relógio ou gerador
    reais, permitindo alterar cada campo isoladamente.
    """
    repositorio = create_autospec(RepositorioExperienciaProfissional, instance=True)
    relogio = create_autospec(Relogio, instance=True)
    relogio.agora.return_value = INSTANTE
    original = ExperienciaProfissional(
        id=IDENTIDADE, usuario_id=DONO, empresa="Anterior", cargo="Cargo anterior",
        descricao="Descrição anterior", periodo=Periodo(date(2020, 1, 1)),
    )
    repositorio.obter_por_id_e_usuario.return_value = original
    repositorio.atualizar.return_value = True
    dados = {
        "usuario_id": DONO, "empresa": " Empresa  Local ", "cargo": " Cargo ",
        "descricao": "\n Primeira  linha\nSegunda linha \n",
        "periodo": Periodo(HOJE - timedelta(days=1), HOJE),
        **alteracoes,
    }
    if modo == "cadastrar":
        gerador = create_autospec(GeradorExperienciaProfissionalId, instance=True)
        gerador.gerar.return_value = IDENTIDADE
        caso = CadastrarExperienciaProfissional(repositorio, gerador, relogio)
        entrada = CadastrarExperienciaProfissionalEntrada(**dados)
    else:
        caso = EditarExperienciaProfissional(repositorio, relogio)
        entrada = EditarExperienciaProfissionalEntrada(experiencia_id=IDENTIDADE, **dados)
    return caso, entrada, repositorio, relogio, original


class ValidacaoGravacaoExperienciaTestCase(unittest.IsolatedAsyncioTestCase):
    """Confere o fluxo dos dois casos com tempo fixo e fronteiras mockadas.

    Observa resultados e chamadas para garantir política de domínio antes da
    persistência e consulta por dono antes de validar uma edição.
    """

    async def test_normaliza_antes_de_gravar_e_le_relogio_uma_vez(self):
        """Executa ambos os casos e compara a entidade enviada às portas de escrita.

        Confere textos normalizados e relógio único, além da consulta escopada
        da edição, para proteger a colaboração sem validar infraestrutura.
        """
        for modo in ("cadastrar", "editar"):
            with self.subTest(modo=modo):
                caso, entrada, repo, relogio, original = preparar_caso(modo)
                resultado = await caso.executar(entrada)
                self.assertEqual((resultado.empresa, resultado.cargo, resultado.descricao), (
                    "Empresa  Local", "Cargo", "Primeira  linha\nSegunda linha"
                ))
                self.assertEqual((resultado.id, resultado.usuario_id), (IDENTIDADE, DONO))
                relogio.agora.assert_called_once_with()
                if modo == "cadastrar":
                    repo.salvar.assert_awaited_once_with(resultado)
                    repo.atualizar.assert_not_called()
                    repo.obter_por_id_e_usuario.assert_not_called()
                else:
                    repo.obter_por_id_e_usuario.assert_awaited_once_with(IDENTIDADE, DONO)
                    repo.atualizar.assert_awaited_once_with(resultado)
                    repo.salvar.assert_not_called()
                    self.assertEqual(original.empresa, "Anterior")

    async def test_ontem_hoje_amanha_em_ambos_os_campos_sem_escrita_invalida(self):
        """Varia as datas contra um instante fixo em cadastro e edição.

        Confere que ontem e hoje persistem, amanhã não e a consulta da edição
        ocorre somente uma vez, preservando o original quando a política falha.
        """
        for modo in ("cadastrar", "editar"):
            for campo in ("inicio", "fim"):
                for dias in (-1, 0, 1):
                    with self.subTest(modo=modo, campo=campo, dias=dias):
                        data = HOJE + timedelta(days=dias)
                        periodo = Periodo(data) if campo == "inicio" else Periodo(HOJE - timedelta(days=2), data)
                        caso, entrada, repo, relogio, original = preparar_caso(modo, periodo=periodo)
                        if dias > 0:
                            with self.assertRaises(RegraDeDominioViolada):
                                await caso.executar(entrada)
                            repo.salvar.assert_not_called()
                            repo.atualizar.assert_not_called()
                            self.assertEqual(original.empresa, "Anterior")
                        else:
                            resultado = await caso.executar(entrada)
                            self.assertEqual(resultado.periodo, periodo)
                        relogio.agora.assert_called_once_with()
                        if modo == "editar":
                            repo.obter_por_id_e_usuario.assert_awaited_once_with(IDENTIDADE, DONO)

    async def test_limites_e_brancos_nao_sao_contornados_por_chamada_direta(self):
        """Envia entradas internas inválidas para provar proteção além do HTTP.

        Varia os três textos acima do máximo ou em branco nos dois casos e
        exige ausência de escrita e preservação da entidade carregada.
        """
        for modo in ("cadastrar", "editar"):
            for campo, maximo in (("empresa", 200), ("cargo", 200), ("descricao", 5000)):
                for valor in (" \n\t ", " " + "a" * (maximo + 1) + " "):
                    with self.subTest(modo=modo, campo=campo, tamanho=len(valor)):
                        caso, entrada, repo, relogio, original = preparar_caso(modo, **{campo: valor})
                        with self.assertRaises(RegraDeDominioViolada):
                            await caso.executar(entrada)
                        repo.salvar.assert_not_called()
                        repo.atualizar.assert_not_called()
                        relogio.agora.assert_called_once_with()
                        self.assertEqual(original.empresa, "Anterior")

    async def test_meia_noite_em_sao_paulo_atualiza_hoje_sem_reinicio(self):
        """Executa duas operações no mesmo caso antes e depois da meia-noite local.

        O relógio UTC passa de 02:59 a 03:00 enquanto a entrada permanece no dia
        sete, para provar a conversão explícita, a ausência de data congelada e
        uma única leitura de tempo a cada tentativa de gravação.
        """
        for modo in ("cadastrar", "editar"):
            with self.subTest(modo=modo):
                caso, entrada, repo, relogio, _ = preparar_caso(modo, periodo=Periodo(HOJE, HOJE))
                relogio.agora.side_effect = (
                    datetime(2026, 11, 7, 2, 59, tzinfo=timezone.utc),
                    datetime(2026, 11, 7, 3, 0, tzinfo=timezone.utc),
                )
                with self.assertRaises(RegraDeDominioViolada):
                    await caso.executar(entrada)
                repo.salvar.assert_not_called()
                repo.atualizar.assert_not_called()
                resultado = await caso.executar(entrada)
                self.assertEqual(resultado.periodo, Periodo(HOJE, HOJE))
                self.assertEqual(relogio.agora.call_count, 2)
                self.assertEqual(repo.salvar.await_count + repo.atualizar.await_count, 1)

    async def test_edicao_consulta_dono_antes_de_tempo_e_transicao(self):
        """Inspeciona a sequência de chamadas com repositório e relógio acoplados.

        Confere consulta única seguida da resolução temporal e atualização para
        preservar a decisão de fluxo existente sem adicionar I/O de leitura.
        """
        caso, entrada, repo, relogio, _ = preparar_caso("editar")
        ordem = Mock()
        ordem.attach_mock(repo, "repo")
        ordem.attach_mock(relogio, "relogio")
        resultado = await caso.executar(entrada)
        self.assertEqual(ordem.mock_calls, [
            call.repo.obter_por_id_e_usuario(IDENTIDADE, DONO),
            call.relogio.agora(), call.repo.atualizar(resultado),
        ])

    async def test_edicao_ausente_ou_alheia_preserva_falha_sem_outra_consulta(self):
        """Configura ausência ou retorno alheio e exige a falha uniforme existente.

        Confere que o caso não valida tempo nem escreve antes de resolver a
        propriedade para evitar mudanças na identificação do dono do recurso.
        """
        for alheia in (False, True):
            with self.subTest(alheia=alheia):
                caso, entrada, repo, relogio, original = preparar_caso("editar")
                repo.obter_por_id_e_usuario.return_value = (
                    replace(original, usuario_id=UsuarioId(UUID(int=999))) if alheia else None
                )
                with self.assertRaises(ExperienciaProfissionalNaoEncontrada):
                    await caso.executar(entrada)
                repo.obter_por_id_e_usuario.assert_awaited_once_with(IDENTIDADE, DONO)
                relogio.agora.assert_not_called()
                repo.atualizar.assert_not_called()

    async def test_edicao_corrige_legado_com_textos_longos_e_datas_futuras(self):
        """Retorna legado estrutural pelo double e edita para estado completo válido.

        Confere consulta e escrita única para provar que validar o estado novo
        não impede corrigir valores antigos fora da política de gravação.
        """
        caso, entrada, repo, _, original = preparar_caso("editar")
        legado = replace(original, empresa="e" * 201, cargo="c" * 201,
                         descricao="d" * 5001, periodo=Periodo(date(2100, 1, 1)))
        repo.obter_por_id_e_usuario.return_value = legado
        resultado = await caso.executar(entrada)
        self.assertEqual(resultado.empresa, "Empresa  Local")
        repo.atualizar.assert_awaited_once_with(resultado)
        self.assertEqual(legado.empresa, "e" * 201)

    async def test_relogio_sem_fuso_e_rejeitado_sem_usar_fuso_do_sistema(self):
        """Fornece relógio inválido e confere falha antes de persistir.

        O datetime sem fuso não pode cair na conversão implícita do SO; o teste
        exige rejeição explícita para manter o dia civil determinístico.
        """
        for modo in ("cadastrar", "editar"):
            caso, entrada, repo, relogio, _ = preparar_caso(modo)
            relogio.agora.return_value = datetime(2026, 11, 7, 12)
            with self.assertRaises(ValueError):
                await caso.executar(entrada)
            relogio.agora.assert_called_once_with()
            repo.salvar.assert_not_called()
            repo.atualizar.assert_not_called()
