"""Testa unitariamente os casos de uso de seleção e desseleção de itens da versão."""

import unittest
from uuid import uuid4

from backend.application import (
    CurriculoNaoEncontrado,
    DesselecionarItemVersaoCurriculo,
    DesselecionarItemVersaoCurriculoEntrada,
    ItemNaoEncontrado,
    SelecionarItemVersaoCurriculo,
    SelecionarItemVersaoCurriculoEntrada,
)
from backend.domain import (
    CompetenciaId,
    Curriculo,
    CurriculoId,
    DocumentoId,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    IdiomaId,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    RegraDeDominioViolada,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001


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


class ConsultaProprietarioItemStub:
    """Substitui a porta de consulta de dono e registra as referências consultadas.

    O stub devolve proprietários previamente definidos por referência e guarda
    cada consulta recebida. Ele existe para controlar a propriedade dos itens e
    provar quando a verificação não deveria ocorrer.
    """

    def __init__(self, proprietarios: dict[ReferenciaCurriculo, UsuarioId] | None = None) -> None:
        """Guarda os proprietários configurados e inicia o histórico de consultas.

        O construtor não acessa recursos externos. Ele existe para que cada teste
        defina quais itens existem e a quem pertencem.
        """
        self._proprietarios = proprietarios or {}
        self.consultas: list[ReferenciaCurriculo] = []

    async def obter_proprietario(self, referencia: ReferenciaCurriculo) -> UsuarioId | None:
        """Devolve por coroutine o dono configurado para a referência, ou ausência.

        O método registra a consulta e lê somente o dicionário do teste. Ele
        existe para simular a leitura aguardável exigida pela porta.
        """
        self.consultas.append(referencia)
        return self._proprietarios.get(referencia)


def _criar_curriculo(usuario_id: UsuarioId | None = None) -> Curriculo:
    """Cria uma versão de currículo válida e independente de I/O.

    A função monta o agregado sem acessar gerador, banco ou relógio e permite
    informar o proprietário. Ela existe para reduzir repetição mantendo cada
    teste focado na decisão de fluxo.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id or UsuarioId(uuid4()),
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


def _criar_referencia() -> ReferenciaCurriculo:
    """Cria uma referência válida a um projeto acadêmico com identidade nova.

    A função escolhe um dos seis tipos de item apenas para compor o cenário. Ela
    existe para reduzir repetição nos testes que não dependem do tipo do item.
    """
    return ReferenciaCurriculo(ProjetoAcademicoId(uuid4()))


class SelecionarItemVersaoCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``SelecionarItemVersaoCurriculo``.

    A classe substitui o repositório e a consulta de proprietário por doubles e
    observa efeitos e falhas. Ela existe para testar a unidade Application sem
    qualquer adapter, framework ou infraestrutura.
    """

    async def test_seleciona_item_do_proprio_usuario_e_solicita_atualizacao(self) -> None:
        """Confirma a inclusão e a persistência quando versão e item são do solicitante.

        O teste fornece uma versão e um item do mesmo usuário e compara o
        agregado devolvido com o efeito observado nos doubles.
        """
        curriculo = _criar_curriculo()
        referencia = _criar_referencia()
        repositorio = RepositorioCurriculoSpy([curriculo])
        consulta = ConsultaProprietarioItemStub({referencia: curriculo.usuario_id})
        entrada = SelecionarItemVersaoCurriculoEntrada(curriculo.usuario_id, curriculo.id, referencia)

        resultado = await SelecionarItemVersaoCurriculo(repositorio, consulta).executar(entrada)

        self.assertIs(resultado, curriculo)
        self.assertEqual(resultado.referencias, frozenset({referencia}))
        self.assertEqual(repositorio.curriculos_atualizados, [curriculo])
        self.assertEqual(consulta.consultas, [referencia])

    async def test_seleciona_cada_tipo_de_item_do_perfil(self) -> None:
        """Confirma que os seis tipos de item podem ser selecionados.

        O teste repete a seleção para cada tipo de identificador aceito pela
        referência. Ele existe para garantir que a orquestração não depende do
        tipo concreto do item.
        """
        tipos = (
            FormacaoAcademicaId,
            ExperienciaProfissionalId,
            ProjetoAcademicoId,
            CompetenciaId,
            IdiomaId,
            DocumentoId,
        )
        for tipo in tipos:
            with self.subTest(tipo=tipo.__name__):
                curriculo = _criar_curriculo()
                referencia = ReferenciaCurriculo(tipo(uuid4()))
                repositorio = RepositorioCurriculoSpy([curriculo])
                consulta = ConsultaProprietarioItemStub({referencia: curriculo.usuario_id})
                entrada = SelecionarItemVersaoCurriculoEntrada(curriculo.usuario_id, curriculo.id, referencia)

                resultado = await SelecionarItemVersaoCurriculo(repositorio, consulta).executar(entrada)

                self.assertEqual(resultado.referencias, frozenset({referencia}))

    async def test_rejeita_versao_inexistente_sem_consultar_item_nem_atualizar(self) -> None:
        """Confirma que a ausência da versão interrompe o fluxo antes de qualquer outro efeito.

        O teste usa repositório vazio e observa a falha, a ausência de consulta
        de dono e o histórico sem atualização.
        """
        repositorio = RepositorioCurriculoSpy()
        consulta = ConsultaProprietarioItemStub()
        entrada = SelecionarItemVersaoCurriculoEntrada(
            UsuarioId(uuid4()), CurriculoId(uuid4()), _criar_referencia()
        )

        with self.assertRaises(CurriculoNaoEncontrado):
            await SelecionarItemVersaoCurriculo(repositorio, consulta).executar(entrada)

        self.assertEqual(consulta.consultas, [])
        self.assertEqual(repositorio.curriculos_atualizados, [])

    async def test_rejeita_versao_de_outro_usuario_sem_consultar_item_nem_atualizar(self) -> None:
        """Confirma que a versão alheia é negada como se não existisse.

        O teste usa um solicitante diferente do dono da versão e exige a mesma
        falha da ausência, sem consulta de dono, alteração nem atualização.
        """
        curriculo = _criar_curriculo()
        referencia = _criar_referencia()
        repositorio = RepositorioCurriculoSpy([curriculo])
        consulta = ConsultaProprietarioItemStub()
        entrada = SelecionarItemVersaoCurriculoEntrada(UsuarioId(uuid4()), curriculo.id, referencia)

        with self.assertRaises(CurriculoNaoEncontrado):
            await SelecionarItemVersaoCurriculo(repositorio, consulta).executar(entrada)

        self.assertEqual(curriculo.referencias, frozenset())
        self.assertEqual(consulta.consultas, [])
        self.assertEqual(repositorio.curriculos_atualizados, [])

    async def test_rejeita_item_inexistente_sem_alterar_nem_atualizar(self) -> None:
        """Confirma que um item ausente é recusado antes de alterar a versão.

        O teste faz a consulta de dono devolver ausência e observa a falha, a
        seleção intacta e o histórico sem atualização.
        """
        curriculo = _criar_curriculo()
        repositorio = RepositorioCurriculoSpy([curriculo])
        consulta = ConsultaProprietarioItemStub()
        entrada = SelecionarItemVersaoCurriculoEntrada(curriculo.usuario_id, curriculo.id, _criar_referencia())

        with self.assertRaises(ItemNaoEncontrado):
            await SelecionarItemVersaoCurriculo(repositorio, consulta).executar(entrada)

        self.assertEqual(curriculo.referencias, frozenset())
        self.assertEqual(repositorio.curriculos_atualizados, [])

    async def test_rejeita_item_de_outro_usuario_sem_alterar_nem_atualizar(self) -> None:
        """Confirma que o item de outro usuário é negado como se não existisse.

        O teste atribui o item a um dono diferente do solicitante e exige a mesma
        falha da ausência, sem alteração da versão nem atualização. Ele existe
        para impedir a exposição de dados alheios em uma exportação.
        """
        curriculo = _criar_curriculo()
        referencia = _criar_referencia()
        repositorio = RepositorioCurriculoSpy([curriculo])
        consulta = ConsultaProprietarioItemStub({referencia: UsuarioId(uuid4())})
        entrada = SelecionarItemVersaoCurriculoEntrada(curriculo.usuario_id, curriculo.id, referencia)

        with self.assertRaises(ItemNaoEncontrado):
            await SelecionarItemVersaoCurriculo(repositorio, consulta).executar(entrada)

        self.assertEqual(curriculo.referencias, frozenset())
        self.assertEqual(repositorio.curriculos_atualizados, [])

    async def test_rejeita_item_ja_selecionado_sem_atualizar(self) -> None:
        """Confirma que a duplicidade é recusada pelo domínio antes da persistência.

        O teste inclui o item previamente e tenta selecioná-lo de novo, então
        observa a violação de domínio, a seleção inalterada e nenhuma
        atualização.
        """
        curriculo = _criar_curriculo()
        referencia = _criar_referencia()
        curriculo.incluir_referencia(referencia)
        repositorio = RepositorioCurriculoSpy([curriculo])
        consulta = ConsultaProprietarioItemStub({referencia: curriculo.usuario_id})
        entrada = SelecionarItemVersaoCurriculoEntrada(curriculo.usuario_id, curriculo.id, referencia)

        with self.assertRaises(RegraDeDominioViolada):
            await SelecionarItemVersaoCurriculo(repositorio, consulta).executar(entrada)

        self.assertEqual(curriculo.referencias, frozenset({referencia}))
        self.assertEqual(repositorio.curriculos_atualizados, [])


class DesselecionarItemVersaoCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``DesselecionarItemVersaoCurriculo``.

    A classe substitui o repositório por um double e observa efeitos e falhas.
    Ela existe para testar a unidade Application sem qualquer adapter,
    framework ou infraestrutura.
    """

    async def test_remove_item_selecionado_e_solicita_atualizacao(self) -> None:
        """Confirma a remoção e a persistência quando a versão é do solicitante.

        O teste fornece uma versão com um item selecionado e compara o agregado
        devolvido com o efeito observado no double.
        """
        curriculo = _criar_curriculo()
        referencia = _criar_referencia()
        curriculo.incluir_referencia(referencia)
        repositorio = RepositorioCurriculoSpy([curriculo])
        entrada = DesselecionarItemVersaoCurriculoEntrada(curriculo.usuario_id, curriculo.id, referencia)

        resultado = await DesselecionarItemVersaoCurriculo(repositorio).executar(entrada)

        self.assertIs(resultado, curriculo)
        self.assertEqual(resultado.referencias, frozenset())
        self.assertEqual(repositorio.curriculos_atualizados, [curriculo])

    async def test_rejeita_versao_inexistente_sem_atualizar(self) -> None:
        """Confirma que a ausência da versão interrompe o fluxo antes de qualquer efeito.

        O teste usa repositório vazio e observa a falha e o histórico sem
        atualização.
        """
        repositorio = RepositorioCurriculoSpy()
        entrada = DesselecionarItemVersaoCurriculoEntrada(
            UsuarioId(uuid4()), CurriculoId(uuid4()), _criar_referencia()
        )

        with self.assertRaises(CurriculoNaoEncontrado):
            await DesselecionarItemVersaoCurriculo(repositorio).executar(entrada)

        self.assertEqual(repositorio.curriculos_atualizados, [])

    async def test_rejeita_versao_de_outro_usuario_sem_alterar_nem_atualizar(self) -> None:
        """Confirma que a versão alheia é negada como se não existisse.

        O teste usa um solicitante diferente do dono e exige a falha da
        ausência, com a seleção da versão intacta e sem atualização.
        """
        curriculo = _criar_curriculo()
        referencia = _criar_referencia()
        curriculo.incluir_referencia(referencia)
        repositorio = RepositorioCurriculoSpy([curriculo])
        entrada = DesselecionarItemVersaoCurriculoEntrada(UsuarioId(uuid4()), curriculo.id, referencia)

        with self.assertRaises(CurriculoNaoEncontrado):
            await DesselecionarItemVersaoCurriculo(repositorio).executar(entrada)

        self.assertEqual(curriculo.referencias, frozenset({referencia}))
        self.assertEqual(repositorio.curriculos_atualizados, [])

    async def test_rejeita_item_nao_selecionado_sem_atualizar(self) -> None:
        """Confirma que remover item ausente da seleção é recusado pelo domínio.

        O teste tenta desselecionar um item que não compõe a versão e observa a
        violação de domínio, a seleção inalterada e nenhuma atualização.
        """
        curriculo = _criar_curriculo()
        selecionado = _criar_referencia()
        curriculo.incluir_referencia(selecionado)
        repositorio = RepositorioCurriculoSpy([curriculo])
        entrada = DesselecionarItemVersaoCurriculoEntrada(curriculo.usuario_id, curriculo.id, _criar_referencia())

        with self.assertRaises(RegraDeDominioViolada):
            await DesselecionarItemVersaoCurriculo(repositorio).executar(entrada)

        self.assertEqual(curriculo.referencias, frozenset({selecionado}))
        self.assertEqual(repositorio.curriculos_atualizados, [])
