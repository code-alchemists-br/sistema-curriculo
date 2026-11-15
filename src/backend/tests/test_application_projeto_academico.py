"""Verifica entidades e orquestração de projetos sem recursos externos.

Usa IDs e instantes fixos e mocks das portas para proteger limites, identidade,
leitura própria e exclusão idempotente, inclusive decisões de concorrência.
"""

# Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from backend.application import (
    ConsultarProjetoAcademico,
    ConsultarProjetoAcademicoEntrada,
    EditarProjetoAcademico,
    EditarProjetoAcademicoEntrada,
    ExcluirProjetoAcademico,
    ExcluirProjetoAcademicoEntrada,
    ProjetoAcademicoNaoEncontrado,
    Relogio,
    RepositorioProjetoAcademico,
)
from backend.domain import (
    ProjetoAcademico,
    ProjetoAcademicoId,
    RegraDeDominioViolada,
    UsuarioId,
)

INSTANTE = datetime(2026, 11, 8, 12, tzinfo=timezone.utc)


def criar_projeto() -> ProjetoAcademico:
    """Constrói um projeto válido com identidades fixas e textos curtos.

    Centraliza dados determinísticos sem I/O para que os testes alterem apenas
    o estado relevante à regra ou decisão de fluxo observada.
    """
    return ProjetoAcademico(
        ProjetoAcademicoId(UUID(int=1)), UsuarioId(UUID(int=2)),
        "Projeto", "Descrição", "Python",
    )


class ProjetoAcademicoTransicoesTestCase(TestCase):
    """Protege edição e exclusão exercitando somente a entidade imutável.

    Varia textos e instantes determinísticos para verificar reuso das
    invariantes do construtor e preservação da identidade e primeiro marcador.
    """

    def test_editar_preserva_identidade_dono_marcador_e_original(self) -> None:
        """Edita ativo e excluído e compara os metadados e o objeto original.

        Usa ambas as formas do projeto para garantir que editar reaplique as
        invariantes sem apagar marcador nem mutar o estado anterior.
        """
        for marcador in (None, INSTANTE):
            with self.subTest(marcador=marcador):
                projeto = replace(criar_projeto(), deleted_at=marcador)
                editado = projeto.editar("  Novo  ", "  Descrição á🙂  ", "  Rust  ")
                self.assertEqual((editado.id, editado.usuario_id, editado.deleted_at),
                                 (projeto.id, projeto.usuario_id, marcador))
                self.assertEqual((editado.titulo, editado.descricao, editado.tecnologias),
                                 ("Novo", "Descrição á🙂", "Rust"))
                self.assertEqual(projeto.titulo, "Projeto")
                self.assertIsNot(editado, projeto)

    def test_construcao_e_edicao_aplicam_as_mesmas_fronteiras_unicode(self) -> None:
        """Compara construção e edição nos limites normalizados dos três textos.

        Varia zero, um, máximo, excesso, espaços, Unicode e controles para
        garantir que nenhuma via aceite texto inválido ou conte bytes.
        """
        projeto = criar_projeto()
        for campo, limite in (("titulo", 200), ("descricao", 2000), ("tecnologias", 300)):
            for valor, valido in (
                ("", False), ("   ", False), ("á", True),
                ("🙂" * limite, True), ("á" * (limite + 1), False),
                ("  " + "á" * limite + "  ", True),
                ("\u2003e\u0301🙂\u2003", True),
                ("texto\n", False), ("texto\x85", False), ("\ttexto", False),
                (None, False), (12, False),
            ):
                with self.subTest(campo=campo, valor=repr(valor)):
                    dados = {"titulo": "Título", "descricao": "Descrição", "tecnologias": "Go"}
                    dados[campo] = valor
                    if valido:
                        construido = replace(projeto, **dados)
                        editado = projeto.editar(**dados)
                        self.assertEqual(editado, construido)
                        self.assertEqual(getattr(editado, campo), valor.strip())
                    else:
                        with self.assertRaises(RegraDeDominioViolada):
                            replace(projeto, **dados)
                        with self.assertRaises(RegraDeDominioViolada):
                            projeto.editar(**dados)

    def test_excluir_exige_fuso_e_preserva_primeiro_instante(self) -> None:
        """Recusa instante ingênuo e preserva primeira exclusão em repetições.

        Aplica transições com horários fixos para garantir que exclusão não
        dependa do tempo real nem altere identidade, conteúdo ou objeto ativo.
        """
        projeto = criar_projeto()
        with self.assertRaises(RegraDeDominioViolada):
            projeto.excluir(INSTANTE.replace(tzinfo=None))
        excluido = projeto.excluir(INSTANTE)
        self.assertEqual(excluido, replace(projeto, deleted_at=INSTANTE))
        self.assertIsNone(projeto.deleted_at)
        self.assertIs(excluido.excluir(INSTANTE + timedelta(days=1)), excluido)
        self.assertIs(excluido.excluir(INSTANTE.replace(tzinfo=None)), excluido)


class ProjetoAcademicoCasosDeUsoTestCase(IsolatedAsyncioTestCase):
    """Verifica cada caso de uso isolado com doubles de repositório e relógio.

    Programa retornos e disputas das portas e observa saídas e chamadas para
    garantir ausência uniforme, ordem de validação e exclusão idempotente.
    """

    def setUp(self) -> None:
        """Prepara portas mockadas e dados fixos sem acessar adapters reais.

        Configura retorno ativo e sucesso de escrita como padrão para isolar
        em cada cenário somente a decisão de fluxo sob teste.
        """
        self.projeto = criar_projeto()
        self.repositorio = AsyncMock(spec=RepositorioProjetoAcademico)
        self.repositorio.obter_por_id_e_usuario.return_value = self.projeto
        self.repositorio.obter_por_id_e_usuario_incluindo_excluidas.return_value = self.projeto
        self.repositorio.atualizar.return_value = True
        self.repositorio.marcar_excluida.return_value = True
        self.relogio = Mock(spec=Relogio)
        self.relogio.agora.return_value = INSTANTE
        self.consulta = ConsultarProjetoAcademicoEntrada(self.projeto.usuario_id, self.projeto.id)
        self.edicao = EditarProjetoAcademicoEntrada(
            self.projeto.usuario_id, self.projeto.id, " Novo ", " Descrição nova ", " Rust ",
        )
        self.exclusao = ExcluirProjetoAcademicoEntrada(self.projeto.usuario_id, self.projeto.id)

    async def test_consulta_propria_retorna_detalhe_sem_escrita(self) -> None:
        """Obtém o projeto próprio e confere a busca com ambos os IDs.

        Observa a entidade retornada e ausência de escrita para manter consulta
        de detalhe independente de mutações ou relógio.
        """
        resultado = await ConsultarProjetoAcademico(self.repositorio).executar(self.consulta)
        self.assertIs(resultado, self.projeto)
        self.repositorio.obter_por_id_e_usuario.assert_awaited_once_with(
            self.projeto.id, self.projeto.usuario_id,
        )
        self.repositorio.atualizar.assert_not_awaited()
        self.repositorio.marcar_excluida.assert_not_awaited()

    async def test_consulta_e_edicao_confundem_ausente_alheio_excluido(self) -> None:
        """Recusa os três estados com a mesma falha interna e sem escrita.

        Simula None contratual e retornos inconsistentes de dono e estado para
        proteger o resultado ativo próprio mesmo com uma porta incorreta.
        """
        for projeto in (None, replace(self.projeto, usuario_id=UsuarioId(UUID(int=3))),
                        self.projeto.excluir(INSTANTE)):
            with self.subTest(projeto=projeto):
                self.repositorio.obter_por_id_e_usuario.return_value = projeto
                for caso, entrada in (
                    (ConsultarProjetoAcademico(self.repositorio), self.consulta),
                    (EditarProjetoAcademico(self.repositorio), self.edicao),
                ):
                    with self.assertRaisesRegex(ProjetoAcademicoNaoEncontrado,
                                                "Projeto acadêmico não encontrado"):
                        await caso.executar(entrada)
                self.repositorio.atualizar.assert_not_awaited()

    async def test_edicao_persiste_novos_textos_preservando_metadados(self) -> None:
        """Confere entidade editada e enviada à porta após validação.

        Usa entrada com espaços para verificar normalização e preservação de
        ID, dono e marcador sem mutação do projeto previamente carregado.
        """
        editado = await EditarProjetoAcademico(self.repositorio).executar(self.edicao)
        self.assertEqual(editado, self.projeto.editar("Novo", "Descrição nova", "Rust"))
        self.assertEqual((editado.id, editado.usuario_id, editado.deleted_at),
                         (self.projeto.id, self.projeto.usuario_id, None))
        self.assertEqual(self.projeto.titulo, "Projeto")
        self.repositorio.obter_por_id_e_usuario.assert_awaited_once_with(
            self.projeto.id, self.projeto.usuario_id,
        )
        self.repositorio.atualizar.assert_awaited_once_with(editado)

    async def test_edicao_invalida_nao_chama_atualizar(self) -> None:
        """Varia violações nos três campos e observa ausência de atualização.

        Exerce fronteiras, espaços, tipos e controles para garantir que o caso
        delegue as invariantes à entidade antes de solicitar escrita.
        """
        for campo, limite in (("titulo", 200), ("descricao", 2000), ("tecnologias", 300)):
            for valor in ("", "  ", "á" * (limite + 1), "\x00ok", "ok\n", None, 1):
                with self.subTest(campo=campo, valor=repr(valor)):
                    with self.assertRaises(RegraDeDominioViolada):
                        await EditarProjetoAcademico(self.repositorio).executar(
                            replace(self.edicao, **{campo: valor})
                        )
                    self.repositorio.atualizar.assert_not_awaited()

    async def test_edicao_sem_linha_atualizada_vira_nao_encontrado(self) -> None:
        """Simula exclusão concorrente por atualização sem efeito.

        Faz a porta retornar False após leitura válida para impedir que o caso
        anuncie sucesso ou tente ressuscitar o projeto.
        """
        self.repositorio.atualizar.return_value = False
        with self.assertRaises(ProjetoAcademicoNaoEncontrado):
            await EditarProjetoAcademico(self.repositorio).executar(self.edicao)
        self.repositorio.atualizar.assert_awaited_once()

    async def test_primeira_exclusao_usa_relogio_e_marcacao_condicional(self) -> None:
        """Exclui o ativo com instante injetado e confere os IDs da escrita.

        Observa retorno e chamadas para garantir uso único do relógio e somente
        marcação lógica, sem atualização genérica nem purga de seleções.
        """
        resultado = await ExcluirProjetoAcademico(self.repositorio, self.relogio).executar(
            self.exclusao
        )
        self.assertEqual(resultado, self.projeto.excluir(INSTANTE))
        self.relogio.agora.assert_called_once_with()
        self.repositorio.marcar_excluida.assert_awaited_once_with(
            self.projeto.id, self.projeto.usuario_id, INSTANTE,
        )
        self.repositorio.obter_por_id_e_usuario_incluindo_excluidas.assert_awaited_once_with(
            self.projeto.id, self.projeto.usuario_id,
        )
        self.repositorio.atualizar.assert_not_awaited()

    async def test_exclusao_repetida_nao_consulta_relogio_nem_escreve(self) -> None:
        """Devolve tombstone próprio já existente sem novos efeitos.

        Prepara projeto excluído e compara identidade e ausência de chamadas
        para preservar o primeiro instante e o contrato idempotente.
        """
        excluido = self.projeto.excluir(INSTANTE)
        self.repositorio.obter_por_id_e_usuario_incluindo_excluidas.return_value = excluido
        resultado = await ExcluirProjetoAcademico(self.repositorio, self.relogio).executar(
            self.exclusao
        )
        self.assertIs(resultado, excluido)
        self.relogio.agora.assert_not_called()
        self.repositorio.marcar_excluida.assert_not_awaited()
        self.repositorio.atualizar.assert_not_awaited()

    async def test_exclusao_ausente_ou_alheia_nao_consulta_relogio_nem_escreve(self) -> None:
        """Recusa ausência e outro dono inclusive quando já excluído.

        Programa a leitura incluindo excluídos para garantir falha uniforme
        sem obter tempo ou solicitar mutação de dados alheios.
        """
        alheio = replace(self.projeto, usuario_id=UsuarioId(UUID(int=3)))
        for projeto in (None, alheio, alheio.excluir(INSTANTE)):
            with self.subTest(projeto=projeto):
                self.repositorio.obter_por_id_e_usuario_incluindo_excluidas.return_value = projeto
                with self.assertRaises(ProjetoAcademicoNaoEncontrado):
                    await ExcluirProjetoAcademico(self.repositorio, self.relogio).executar(
                        self.exclusao
                    )
                self.relogio.agora.assert_not_called()
                self.repositorio.marcar_excluida.assert_not_awaited()

    async def test_exclusao_concorrente_rele_e_preserva_instante_vencedor(self) -> None:
        """Aceita tombstone próprio após perder a marcação condicional.

        Retorna ativo e depois exclusão por outro fluxo para garantir releitura
        pelos mesmos IDs e preservação do instante efetivamente persistido.
        """
        vencedor = self.projeto.excluir(INSTANTE - timedelta(seconds=1))
        leitura = self.repositorio.obter_por_id_e_usuario_incluindo_excluidas
        leitura.side_effect = [self.projeto, vencedor]
        self.repositorio.marcar_excluida.return_value = False
        resultado = await ExcluirProjetoAcademico(self.repositorio, self.relogio).executar(
            self.exclusao
        )
        self.assertIs(resultado, vencedor)
        self.assertEqual(leitura.await_count, 2)
        for chamada in leitura.await_args_list:
            self.assertEqual(chamada.args, (self.projeto.id, self.projeto.usuario_id))
        self.repositorio.marcar_excluida.assert_awaited_once()
        self.relogio.agora.assert_called_once_with()

    async def test_disputa_sem_tombstone_proprio_vira_nao_encontrado(self) -> None:
        """Recusa releitura ausente, ativa ou alheia após escrita sem efeito.

        Varia a segunda leitura para garantir que perder a disputa somente
        seja sucesso quando existir exclusão própria efetivamente observada.
        """
        alheio = replace(self.projeto.excluir(INSTANTE), usuario_id=UsuarioId(UUID(int=3)))
        for recarregado in (None, self.projeto, alheio):
            with self.subTest(recarregado=recarregado):
                leitura = self.repositorio.obter_por_id_e_usuario_incluindo_excluidas
                leitura.side_effect = [self.projeto, recarregado]
                self.repositorio.marcar_excluida.return_value = False
                with self.assertRaises(ProjetoAcademicoNaoEncontrado):
                    await ExcluirProjetoAcademico(self.repositorio, self.relogio).executar(
                        self.exclusao
                    )

    async def test_relogio_sem_fuso_impede_escrita(self) -> None:
        """Recusa instante inválido antes de chamar a marcação lógica.

        Injeta datetime sem fuso para confirmar que a invariante temporal do
        domínio interrompa o fluxo sem persistir marcador inválido.
        """
        self.relogio.agora.return_value = INSTANTE.replace(tzinfo=None)
        with self.assertRaises(RegraDeDominioViolada):
            await ExcluirProjetoAcademico(self.repositorio, self.relogio).executar(self.exclusao)
        self.repositorio.marcar_excluida.assert_not_awaited()
