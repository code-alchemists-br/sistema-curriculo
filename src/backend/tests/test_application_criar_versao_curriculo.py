"""Testa unitariamente o caso de uso de criação de versão de currículo."""

import unittest
from uuid import uuid4

from backend.application import CriarVersaoCurriculo, CriarVersaoCurriculoEntrada
from backend.domain import Curriculo, CurriculoId, RegraDeDominioViolada, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001


class RepositorioCurriculoSpy:
    """Substitui a porta de currículo e registra as versões entregues para salvar.

    O double acumula em memória os agregados recebidos, sem banco ou ORM. Ele
    existe para tornar observável o efeito do caso de uso de criação de forma
    unitária.
    """

    def __init__(self) -> None:
        """Inicializa o registro vazio de chamadas de persistência.

        O construtor cria uma lista local que receberá os agregados salvos. Ele
        existe para permitir que o teste observe a persistência e sua ausência.
        """
        self.curriculos_salvos: list[Curriculo] = []

    async def salvar(self, curriculo: Curriculo) -> None:
        """Armazena localmente o agregado recebido pelo contrato da porta.

        O método acrescenta o agregado à lista e mantém a assinatura assíncrona.
        Ele existe para substituir a infraestrutura no teste do caso de uso.
        """
        self.curriculos_salvos.append(curriculo)


class GeradorCurriculoIdStub:
    """Entrega um identificador de currículo previamente definido e conta chamadas.

    O stub devolve sempre o mesmo value object e elimina aleatoriedade. Ele
    existe para permitir asserções determinísticas sobre a identidade da versão
    criada e sobre quantas vezes ela foi solicitada.
    """

    def __init__(self, identificador: CurriculoId) -> None:
        """Recebe o identificador que devolverá nas chamadas seguintes.

        O construtor conserva o value object do cenário sem gerar UUIDs e inicia
        o contador de chamadas. Ele existe para controlar a identidade atribuída
        em cada teste.
        """
        self._identificador = identificador
        self.chamadas = 0

    def gerar(self) -> CurriculoId:
        """Devolve o identificador configurado e registra a chamada.

        O método implementa a porta retornando o mesmo valor a cada chamada. Ele
        existe para isolar o caso de uso da estratégia concreta de UUID.
        """
        self.chamadas += 1
        return self._identificador


class CriarVersaoCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``CriarVersaoCurriculo``.

    A classe substitui o repositório e o gerador de identidade por doubles e
    observa efeitos e falhas. Ela existe para testar a unidade Application sem
    qualquer adapter, framework ou infraestrutura.
    """

    async def test_cria_e_salva_versao_com_identidade_gerada(self) -> None:
        """Confirma a construção, o salvamento e o retorno da versão criada.

        O teste executa a criação com dados válidos e compara o agregado devolvido
        com o efeito observado no spy e no stub de identidade.
        """
        identificador = CurriculoId(uuid4())
        usuario_id = UsuarioId(uuid4())
        repositorio = RepositorioCurriculoSpy()
        gerador = GeradorCurriculoIdStub(identificador)
        entrada = CriarVersaoCurriculoEntrada(
            usuario_id=usuario_id,
            titulo_versao="Estágio em TI",
            layout="classico",
            is_public=False,
        )

        resultado = await CriarVersaoCurriculo(repositorio, gerador).executar(entrada)

        self.assertEqual(resultado.id, identificador)
        self.assertEqual(resultado.usuario_id, usuario_id)
        self.assertEqual(resultado.titulo_versao, "Estágio em TI")
        self.assertEqual(resultado.layout, "classico")
        self.assertFalse(resultado.is_public)
        self.assertEqual(resultado.referencias, frozenset())
        self.assertEqual(len(repositorio.curriculos_salvos), 1)
        self.assertIs(repositorio.curriculos_salvos[0], resultado)
        self.assertEqual(gerador.chamadas, 1)

    async def test_preserva_a_visibilidade_informada(self) -> None:
        """Confirma que a visibilidade solicitada chega intacta ao agregado salvo.

        O teste repete a criação para os dois valores booleanos e compara o
        agregado devolvido. Ele existe para garantir que a orquestração não
        altere a escolha do estudante.
        """
        for visibilidade in (True, False):
            with self.subTest(is_public=visibilidade):
                repositorio = RepositorioCurriculoSpy()
                entrada = CriarVersaoCurriculoEntrada(
                    usuario_id=UsuarioId(uuid4()),
                    titulo_versao="Gestão de Projetos",
                    layout="moderno",
                    is_public=visibilidade,
                )

                resultado = await CriarVersaoCurriculo(
                    repositorio, GeradorCurriculoIdStub(CurriculoId(uuid4()))
                ).executar(entrada)

                self.assertEqual(resultado.is_public, visibilidade)
                self.assertEqual(repositorio.curriculos_salvos, [resultado])

    async def test_nao_salva_versao_quando_titulo_eh_em_branco(self) -> None:
        """Interrompe o fluxo antes da persistência quando o título é inválido.

        O teste envia título formado só por espaços e observa a violação de
        domínio sem nenhuma chamada de salvamento. Ele existe para assegurar que
        a porta não receba versão incompleta.
        """
        repositorio = RepositorioCurriculoSpy()
        entrada = CriarVersaoCurriculoEntrada(
            usuario_id=UsuarioId(uuid4()),
            titulo_versao="   ",
            layout="classico",
            is_public=False,
        )

        with self.assertRaises(RegraDeDominioViolada):
            await CriarVersaoCurriculo(
                repositorio, GeradorCurriculoIdStub(CurriculoId(uuid4()))
            ).executar(entrada)

        self.assertEqual(repositorio.curriculos_salvos, [])

    async def test_nao_salva_versao_quando_visibilidade_nao_eh_booleana(self) -> None:
        """Interrompe o fluxo antes da persistência quando a visibilidade é inválida.

        O teste envia um valor não booleano e observa a violação de domínio sem
        salvamento. Ele existe para provar que a regra do agregado vale também
        na criação.
        """
        repositorio = RepositorioCurriculoSpy()
        entrada = CriarVersaoCurriculoEntrada(
            usuario_id=UsuarioId(uuid4()),
            titulo_versao="Estágio em TI",
            layout="classico",
            is_public="sim",  # type: ignore[arg-type]
        )

        with self.assertRaises(RegraDeDominioViolada):
            await CriarVersaoCurriculo(
                repositorio, GeradorCurriculoIdStub(CurriculoId(uuid4()))
            ).executar(entrada)

        self.assertEqual(repositorio.curriculos_salvos, [])
