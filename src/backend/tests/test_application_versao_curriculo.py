"""Testa unitariamente o caso de uso de edição de versão de currículo."""

import unittest
from uuid import uuid4

from backend.application import (
    CurriculoNaoEncontrado,
    EditarVersaoCurriculo,
    EditarVersaoCurriculoEntrada,
)
from backend.domain import Curriculo, CurriculoId, RegraDeDominioViolada, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001


class RepositorioCurriculoSpy:
    """Substitui a porta de currículo e registra atualizações solicitadas.

    O double consulta agregados em memória por ID e acumula os estados
    atualizados. Ele existe para testar a orquestração assíncrona sem ORM,
    banco, rede ou adapter produtivo.
    """

    def __init__(self, curriculos: list[Curriculo] | None = None) -> None:
        """Prepara um índice em memória e um histórico vazio de atualizações.

        O construtor copia os currículos fornecidos em um dicionário por
        identidade. Ele existe para controlar ausência e propriedade em cada
        cenário testado.
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
        existe para tornar observável se e quando houve efeito de atualização.
        """
        self.curriculos_atualizados.append(curriculo)


class EditarVersaoCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``EditarVersaoCurriculo``.

    A classe substitui a porta de currículo por estado em memória e observa
    falhas e atualizações. Ela existe para testar a unidade Application sem
    qualquer adapter, framework ou infraestrutura.
    """

    async def test_edita_versao_do_proprietario_e_solicita_atualizacao(self) -> None:
        """Confirma a edição e a persistência quando o solicitante é o dono.

        O teste fornece uma versão do próprio usuário e compara o estado
        retornado com o efeito observado no double.
        """
        curriculo = _criar_curriculo()
        repositorio = RepositorioCurriculoSpy([curriculo])
        entrada = EditarVersaoCurriculoEntrada(
            usuario_id=curriculo.usuario_id,
            curriculo_id=curriculo.id,
            titulo_versao="Gestão de Projetos",
            layout="moderno",
            is_public=True,
        )

        resultado = await EditarVersaoCurriculo(repositorio).executar(entrada)

        self.assertIs(resultado, curriculo)
        self.assertEqual(resultado.titulo_versao, "Gestão de Projetos")
        self.assertEqual(resultado.layout, "moderno")
        self.assertTrue(resultado.is_public)
        self.assertEqual(repositorio.curriculos_atualizados, [curriculo])

    async def test_rejeita_versao_inexistente_sem_atualizacao(self) -> None:
        """Confirma que ausência interrompe o fluxo antes de qualquer efeito.

        O teste usa repositório vazio e observa a falha e o histórico sem
        atualização. Ele existe para impedir criação implícita durante a edição.
        """
        repositorio = RepositorioCurriculoSpy()
        entrada = EditarVersaoCurriculoEntrada(
            usuario_id=UsuarioId(uuid4()),
            curriculo_id=CurriculoId(uuid4()),
            titulo_versao="Gestão de Projetos",
            layout="moderno",
            is_public=True,
        )

        with self.assertRaises(CurriculoNaoEncontrado):
            await EditarVersaoCurriculo(repositorio).executar(entrada)

        self.assertEqual(repositorio.curriculos_atualizados, [])

    async def test_rejeita_versao_de_outro_usuario_sem_alterar_nem_atualizar(self) -> None:
        """Confirma que a versão de outro usuário é negada como se não existisse.

        O teste usa um solicitante diferente do dono e exige a mesma falha da
        ausência, sem alteração do agregado nem atualização. Ele existe para
        proteger currículos alheios conforme a verificação de propriedade.
        """
        curriculo = _criar_curriculo()
        repositorio = RepositorioCurriculoSpy([curriculo])
        entrada = EditarVersaoCurriculoEntrada(
            usuario_id=UsuarioId(uuid4()),
            curriculo_id=curriculo.id,
            titulo_versao="Invasor",
            layout="moderno",
            is_public=True,
        )

        with self.assertRaises(CurriculoNaoEncontrado):
            await EditarVersaoCurriculo(repositorio).executar(entrada)

        self.assertEqual(curriculo.titulo_versao, "Estágio em TI")
        self.assertFalse(curriculo.is_public)
        self.assertEqual(repositorio.curriculos_atualizados, [])

    async def test_rejeita_titulo_em_branco_sem_atualizar(self) -> None:
        """Confirma que dado inválido é barrado pelo domínio antes da persistência.

        O teste envia título só com espaços para o dono da versão e observa a
        violação de domínio, o agregado intacto e nenhuma atualização.
        """
        curriculo = _criar_curriculo()
        repositorio = RepositorioCurriculoSpy([curriculo])
        entrada = EditarVersaoCurriculoEntrada(
            usuario_id=curriculo.usuario_id,
            curriculo_id=curriculo.id,
            titulo_versao="   ",
            layout="moderno",
            is_public=True,
        )

        with self.assertRaises(RegraDeDominioViolada):
            await EditarVersaoCurriculo(repositorio).executar(entrada)

        self.assertEqual(curriculo.titulo_versao, "Estágio em TI")
        self.assertEqual(repositorio.curriculos_atualizados, [])


def _criar_curriculo() -> Curriculo:
    """Cria uma versão de currículo válida e independente de I/O.

    A função monta o agregado sem acessar gerador, banco ou relógio. Ela existe
    para reduzir repetição mantendo cada teste focado na decisão de fluxo.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=UsuarioId(uuid4()),
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )
