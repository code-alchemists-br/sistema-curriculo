"""Testa unitariamente o caso de uso de revisão de campos obrigatórios."""

import unittest
from dataclasses import replace
from datetime import UTC, datetime

from backend.application import (
    CurriculoNaoEncontrado,
    GerarPreviaVersaoCurriculoEntrada,
    PreviaVersaoCurriculo,
    RevisarVersaoCurriculo,
    RevisarVersaoCurriculoEntrada,
)
from backend.tests.fixtures.curriculo_exportacao import (
    CurriculoExportacaoFixture,
    obter_curriculo_exportacao_fixture,
)

# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001

# Proveniência: decision-analysis prompts/backend/20261023-190000-consistencia-datas-revisao-v001.md#v001
# Instante em que as datas da fixture são coerentes (antes do término previsto da formação).
INSTANTE_CONSISTENTE = datetime(2025, 6, 1, 12, 0, tzinfo=UTC)


class RelogioFixo:
    """Substitui a porta de relógio por um instante fixo.

    O double devolve sempre o mesmo ``datetime`` com fuso. Ele existe para tornar
    a data de hoje determinística na revisão de datas, sem usar o relógio do
    sistema.
    """

    def __init__(self, instante: datetime) -> None:
        """Guarda o instante que será devolvido em cada leitura.

        O construtor não acessa o relógio do sistema. Ele existe para que cada
        teste controle o dia usado pela revisão.
        """
        self._instante = instante

    def agora(self) -> datetime:
        """Devolve o instante configurado.

        O método não consulta fonte de tempo externa. Ele existe para satisfazer a
        porta ``Relogio`` com um valor previsível.
        """
        return self._instante


class GeradorDePreviaStub:
    """Substitui a geração da prévia e registra as entradas recebidas.

    O double devolve a prévia configurada ou levanta o erro configurado, sem
    portas, banco ou domínio de verdade. Ele existe para testar a orquestração
    da revisão isolada da geração da prévia.
    """

    def __init__(
        self,
        previa: PreviaVersaoCurriculo | None = None,
        erro: Exception | None = None,
    ) -> None:
        """Guarda o comportamento configurado e inicia o histórico de chamadas.

        O construtor não acessa recursos externos. Ele existe para permitir que
        cada teste configure sucesso ou falha de forma explícita.
        """
        self._previa = previa
        self._erro = erro
        self.entradas: list[GerarPreviaVersaoCurriculoEntrada] = []

    async def executar(
        self, entrada: GerarPreviaVersaoCurriculoEntrada
    ) -> PreviaVersaoCurriculo:
        """Registra a entrada e devolve a prévia ou levanta o erro configurado.

        O método aguarda de forma trivial, sem I/O real. Ele existe para tornar
        observável o que a revisão pediu à geração da prévia.
        """
        self.entradas.append(entrada)
        if self._erro is not None:
            raise self._erro
        if self._previa is None:
            raise AssertionError("O stub não recebeu prévia nem erro configurado.")
        return self._previa


# Proveniência: decision-analysis prompts/backend/20261023-100000-completude-identificacao-contato-v001.md#v001
def _usuario_com_cidade(fixture: CurriculoExportacaoFixture):
    """Devolve o estudante da fixture com a cidade preenchida no contato.

    A função copia o contato da fixture acrescentando uma cidade, sem alterar a
    fixture compartilhada. Ela existe para que o currículo "completo" não receba
    o aviso de cidade ausente nos testes desta revisão.
    """
    contato = replace(fixture.usuario.dados_contato, cidade="São Paulo")
    return replace(fixture.usuario, dados_contato=contato)


def _previa_completa(fixture: CurriculoExportacaoFixture) -> PreviaVersaoCurriculo:
    """Monta a prévia de um currículo completo a partir da fixture.

    A função reúne o estudante, a versão e um item de cada seção da fixture, sem
    documentos. Ela existe para que cada teste parta de um currículo válido e
    esvazie só o que quer observar.
    """
    return PreviaVersaoCurriculo(
        usuario=_usuario_com_cidade(fixture),
        curriculo=fixture.curriculo,
        formacoes=(fixture.formacao_academica,),
        experiencias=(fixture.experiencia_profissional,),
        projetos=(fixture.projeto_academico,),
        competencias=fixture.competencias,
        idiomas=fixture.idiomas,
        documentos=(),
    )


class RevisarVersaoCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``RevisarVersaoCurriculo``.

    A classe substitui a geração da prévia por um double e observa o resultado e
    as falhas. Ela existe para testar a unidade Application sem adapter,
    framework ou infraestrutura.
    """

    async def test_aprova_a_previa_de_um_curriculo_completo(self) -> None:
        """Confirma que uma prévia completa não gera pendências.

        O teste entrega ao caso de uso a prévia completa da fixture e observa a
        aprovação e a lista vazia. Ele existe para proteger o caso feliz.
        """
        fixture = obter_curriculo_exportacao_fixture()
        stub = GeradorDePreviaStub(previa=_previa_completa(fixture))

        resultado = await RevisarVersaoCurriculo(stub, RelogioFixo(INSTANTE_CONSISTENTE)).executar(
            RevisarVersaoCurriculoEntrada(fixture.usuario.id, fixture.curriculo.id)
        )

        self.assertTrue(resultado.aprovado)
        self.assertEqual(resultado.pendencias, ())

    async def test_converte_a_previa_incompleta_em_pendencias(self) -> None:
        """Confirma que seções vazias da prévia viram pendências de erro.

        O teste esvazia experiências e competências da prévia e compara os
        códigos das pendências e o veredito. Ele existe para provar que a
        revisão realmente aplica a regra do domínio ao conteúdo da prévia.
        """
        fixture = obter_curriculo_exportacao_fixture()
        previa = replace(_previa_completa(fixture), experiencias=(), competencias=())
        stub = GeradorDePreviaStub(previa=previa)

        resultado = await RevisarVersaoCurriculo(stub, RelogioFixo(INSTANTE_CONSISTENTE)).executar(
            RevisarVersaoCurriculoEntrada(fixture.usuario.id, fixture.curriculo.id)
        )

        self.assertEqual(
            [pendencia.codigo for pendencia in resultado.pendencias],
            ["EXPERIENCIA_AUSENTE", "COMPETENCIA_AUSENTE"],
        )
        self.assertFalse(resultado.aprovado)

    # Proveniência: decision-analysis prompts/backend/20261023-190000-consistencia-datas-revisao-v001.md#v001
    async def test_usa_a_data_do_relogio_na_revisao_das_datas(self) -> None:
        """Confirma que a data de hoje vem do relógio injetado.

        O teste usa a mesma prévia completa com dois relógios: um antes e outro
        depois do término previsto da formação em andamento. Ele existe para
        provar que o resultado muda com o relógio e que o caso de uso não usa o
        relógio do sistema.
        """
        fixture = obter_curriculo_exportacao_fixture()
        previa = _previa_completa(fixture)
        entrada = RevisarVersaoCurriculoEntrada(fixture.usuario.id, fixture.curriculo.id)

        antes = await RevisarVersaoCurriculo(
            GeradorDePreviaStub(previa=previa), RelogioFixo(INSTANTE_CONSISTENTE)
        ).executar(entrada)
        depois = await RevisarVersaoCurriculo(
            GeradorDePreviaStub(previa=previa),
            RelogioFixo(datetime(2026, 10, 23, 12, 0, tzinfo=UTC)),
        ).executar(entrada)

        self.assertEqual(antes.pendencias, ())
        self.assertEqual(
            [p.codigo for p in depois.pendencias],
            ["FORMACAO_EM_ANDAMENTO_COM_FIM_PASSADO"],
        )
        self.assertTrue(depois.aprovado)

    async def test_pede_a_previa_com_o_usuario_e_a_versao_da_entrada(self) -> None:
        """Confirma a entrada enviada à geração da prévia.

        O teste compara a entrada registrada pelo double com os identificadores
        recebidos. Ele existe para proteger que a revisão peça a prévia do
        estudante e da versão certos.
        """
        fixture = obter_curriculo_exportacao_fixture()
        stub = GeradorDePreviaStub(previa=_previa_completa(fixture))

        await RevisarVersaoCurriculo(stub, RelogioFixo(INSTANTE_CONSISTENTE)).executar(
            RevisarVersaoCurriculoEntrada(fixture.usuario.id, fixture.curriculo.id)
        )

        self.assertEqual(
            stub.entradas,
            [GerarPreviaVersaoCurriculoEntrada(fixture.usuario.id, fixture.curriculo.id)],
        )

    async def test_propaga_a_falha_de_versao_ausente_ou_alheia(self) -> None:
        """Confirma que a falha de não encontrado da prévia chega ao chamador.

        O teste faz o double levantar a falha e exige que ela não seja engolida
        nem transformada em revisão. Ele existe para impedir que se revise uma
        versão inexistente ou de outro estudante.
        """
        fixture = obter_curriculo_exportacao_fixture()
        stub = GeradorDePreviaStub(
            erro=CurriculoNaoEncontrado("Versão de currículo não encontrada.")
        )

        with self.assertRaises(CurriculoNaoEncontrado):
            await RevisarVersaoCurriculo(stub, RelogioFixo(INSTANTE_CONSISTENTE)).executar(
                RevisarVersaoCurriculoEntrada(fixture.usuario.id, fixture.curriculo.id)
            )