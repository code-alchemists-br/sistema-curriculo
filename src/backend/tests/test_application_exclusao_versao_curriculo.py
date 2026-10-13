"""Testa unitariamente o caso de uso de exclusão de versão de currículo."""

import unittest
from uuid import uuid4

from backend.application import (
    CurriculoNaoEncontrado,
    ExcluirVersaoCurriculo,
    ExcluirVersaoCurriculoEntrada,
)
from backend.domain import Curriculo, CurriculoId, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001


class RepositorioCurriculoSpy:
    """Substitui a porta de currículo e registra consultas e remoções solicitadas.

    O double consulta agregados em memória por ID e acumula as versões cuja
    remoção foi pedida, além de qualquer escrita indevida. Ele existe para
    testar a orquestração assíncrona sem ORM, banco, rede ou adapter produtivo.
    """

    def __init__(self, curriculos: list[Curriculo] | None = None) -> None:
        """Prepara um índice em memória e históricos vazios de uso.

        O construtor copia os currículos fornecidos em um dicionário por
        identidade. Ele existe para controlar ausência e propriedade em cada
        cenário testado.
        """
        self._por_id = {curriculo.id: curriculo for curriculo in (curriculos or [])}
        self.excluidos: list[Curriculo] = []
        self.escritas: list[Curriculo] = []

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Devolve por coroutine a versão associada ao ID informado.

        O método consulta somente o dicionário controlado pelo teste e não faz
        I/O. Ele existe para simular a leitura aguardável exigida pelo caso.
        """
        return self._por_id.get(curriculo_id)

    async def excluir(self, curriculo: Curriculo) -> None:
        """Registra por coroutine a remoção solicitada pela Application.

        O método acumula o agregado sem remover nada. Ele existe para tornar
        observável se e quantas vezes houve pedido de exclusão.
        """
        self.excluidos.append(curriculo)

    async def atualizar(self, curriculo: Curriculo) -> None:
        """Registra por coroutine uma tentativa indevida de atualização.

        O método acumula o agregado sem persistir. Ele existe para tornar
        observável qualquer escrita que a exclusão não deveria fazer.
        """
        self.escritas.append(curriculo)

    async def salvar(self, curriculo: Curriculo) -> None:
        """Registra por coroutine uma tentativa indevida de salvamento.

        O método acumula o agregado sem persistir. Ele existe para tornar
        observável qualquer escrita que a exclusão não deveria fazer.
        """
        self.escritas.append(curriculo)


def _criar_curriculo(usuario_id: UsuarioId) -> Curriculo:
    """Cria uma versão válida do usuário com identidade nova.

    A função fixa título, layout e visibilidade com valores neutros. Ela existe
    para montar o cenário de cada teste sem repetir a construção do agregado.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id,
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


class ExcluirVersaoCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``ExcluirVersaoCurriculo``.

    A classe substitui a porta de currículo por estado em memória e observa
    falhas e pedidos de remoção. Ela existe para testar a unidade Application
    sem adapter, framework ou infraestrutura.
    """

    async def test_exclui_a_versao_do_proprietario_pedindo_a_remocao_uma_vez(self) -> None:
        """Confirma que o dono consegue excluir e que a remoção é pedida uma vez.

        O teste fornece uma versão do próprio usuário e compara o agregado
        entregue ao double. Ele existe para proteger o contrato básico da
        exclusão.
        """
        usuario_id = UsuarioId(uuid4())
        curriculo = _criar_curriculo(usuario_id)
        repositorio = RepositorioCurriculoSpy([curriculo])

        resultado = await ExcluirVersaoCurriculo(repositorio).executar(
            ExcluirVersaoCurriculoEntrada(usuario_id=usuario_id, curriculo_id=curriculo.id)
        )

        self.assertIsNone(resultado)
        self.assertEqual(len(repositorio.excluidos), 1)
        self.assertIs(repositorio.excluidos[0], curriculo)

    async def test_versao_inexistente_falha_sem_pedir_remocao(self) -> None:
        """Confirma que a ausência interrompe o fluxo antes de qualquer efeito.

        O teste usa um repositório vazio e observa a falha e o histórico sem
        remoção. Ele existe para impedir exclusão de algo que não existe.
        """
        repositorio = RepositorioCurriculoSpy()

        with self.assertRaises(CurriculoNaoEncontrado):
            await ExcluirVersaoCurriculo(repositorio).executar(
                ExcluirVersaoCurriculoEntrada(usuario_id=UsuarioId(uuid4()), curriculo_id=CurriculoId(uuid4()))
            )

        self.assertEqual(repositorio.excluidos, [])

    async def test_versao_de_outro_usuario_falha_como_inexistente_sem_pedir_remocao(self) -> None:
        """Confirma que posse alheia produz a mesma falha da ausência.

        O teste fornece uma versão de outro estudante e observa a falha idêntica
        à de ausência, inclusive na mensagem, e a ausência de remoção. Ele existe
        para proteger a versão alheia sem revelar que ela existe (RNF04).
        """
        dono = UsuarioId(uuid4())
        curriculo = _criar_curriculo(dono)
        repositorio = RepositorioCurriculoSpy([curriculo])
        entrada = ExcluirVersaoCurriculoEntrada(usuario_id=UsuarioId(uuid4()), curriculo_id=curriculo.id)

        with self.assertRaises(CurriculoNaoEncontrado) as alheia:
            await ExcluirVersaoCurriculo(repositorio).executar(entrada)
        with self.assertRaises(CurriculoNaoEncontrado) as ausente:
            await ExcluirVersaoCurriculo(RepositorioCurriculoSpy()).executar(entrada)

        self.assertEqual(str(alheia.exception), str(ausente.exception))
        self.assertEqual(repositorio.excluidos, [])

    async def test_nao_atualiza_nem_salva_ao_excluir(self) -> None:
        """Confirma que excluir não faz nenhuma outra escrita.

        O teste exclui uma versão própria e observa o histórico de escritas do
        double. Ele existe para proteger a exclusão de efeitos colaterais.
        """
        usuario_id = UsuarioId(uuid4())
        curriculo = _criar_curriculo(usuario_id)
        repositorio = RepositorioCurriculoSpy([curriculo])

        await ExcluirVersaoCurriculo(repositorio).executar(
            ExcluirVersaoCurriculoEntrada(usuario_id=usuario_id, curriculo_id=curriculo.id)
        )

        self.assertEqual(repositorio.escritas, [])
