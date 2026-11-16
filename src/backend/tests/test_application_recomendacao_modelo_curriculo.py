"""Testa a orquestração interna da recomendação de modelo por IA."""

import unittest
from datetime import date
from uuid import uuid4

from backend.application.adequacao_semantica import (
    ContextoAdequacaoCurriculoVaga,
    PreparadorContextoAssistenciaCurriculo,
    SolicitarAdequacaoCurriculoVagaEntrada,
)
from backend.application.politica_limites_contexto_ia import (
    LimitesContextoIa,
    PoliticaLimitesContextoIa,
    SobrescritaLimitesContextoIa,
)
from backend.application.recomendacao_modelo_curriculo import RecomendarModeloCurriculo
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain import (
    AcaoAdequacaoSemantica,
    Curriculo,
    CurriculoId,
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    ModeloCurriculo,
    Periodo,
    RecomendacaoModeloCurriculo,
    ReferenciaCurriculo,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261105-181751-adequacao-semantica-gpt-nano-v005.md#v005


class RepositorioCurriculoStub:
    """Substitui a consulta de versão por uma resposta controlada em memória.

    O double devolve somente a versão configurada para o identificador pedido,
    sem banco ou adapter. Ele existe para isolar propriedade no preparo comum.
    """

    def __init__(self, curriculo: Curriculo | None) -> None:
        """Guarda a versão configurada para os cenários do caso de uso.

        O construtor conserva uma única resposta previsível. Ele existe para
        representar versão própria, ausente ou pertencente a outro estudante.
        """
        self.curriculo = curriculo

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Devolve a versão quando sua identidade coincide com a consulta.

        O método não faz I/O e retorna ausência para outro identificador. Ele
        existe para exercitar a porta de consulta sem infraestrutura produtiva.
        """
        if self.curriculo is not None and self.curriculo.id == curriculo_id:
            return self.curriculo
        return None


class ConsultaItemStub:
    """Substitui a busca de itens profissionais por mapa em memória.

    O double responde somente pelos itens preparados pelo cenário. Ele existe
    para verificar que o preparador compartilha a seleção autorizada.
    """

    def __init__(self, itens: dict[ReferenciaCurriculo, object]) -> None:
        """Armazena os itens disponíveis sem acessar persistência.

        O construtor recebe respostas imutáveis definidas pelo teste. Ele existe
        para manter os casos determinísticos e independentes de adapters.
        """
        self.itens = itens

    async def obter_item(self, referencia: ReferenciaCurriculo) -> object | None:
        """Devolve o item associado à referência solicitada.

        O método não valida propriedade nem conteúdo, pois essas regras são da
        unidade em teste. Ele existe para simular a porta interna de consulta.
        """
        return self.itens.get(referencia)


class FontePoliticaStub:
    """Fornece política de limites fixa sem ler configuração externa.

    O double devolve o mesmo objeto em memória. Ele existe para testar a ação
    de recomendação sem filesystem ou infraestrutura de configuração.
    """

    def __init__(self, politica: PoliticaLimitesContextoIa) -> None:
        """Guarda a política previamente validada pelo cenário.

        O construtor não altera os limites recebidos. Ele existe para tornar a
        resolução de política observável na orquestração isolada.
        """
        self.politica = politica

    def obter(self) -> PoliticaLimitesContextoIa:
        """Devolve a política fixa para a preparação de contexto.

        O método não acessa recursos externos. Ele existe para substituir a
        fonte configurável por uma dependência determinística de teste.
        """
        return self.politica


class GeradorRecomendacaoSpy:
    """Registra contexto e devolve recomendação controlada sem chamar IA.

    O double modela a porta interna e conserva as chamadas recebidas. Ele existe
    para provar que o caso de uso não altera o agregado antes da sugestão.
    """

    def __init__(self, recomendacao: RecomendacaoModeloCurriculo) -> None:
        """Define a recomendação devolvida nos cenários do teste.

        O construtor recebe value object já validado pelo domínio. Ele existe
        para isolar o fluxo da futura implementação do provedor externo.
        """
        self.recomendacao = recomendacao
        self.contextos: list[ContextoAdequacaoCurriculoVaga] = []

    async def gerar(
        self, contexto: ContextoAdequacaoCurriculoVaga
    ) -> RecomendacaoModeloCurriculo:
        """Registra o contexto autorizado e devolve resultado tipado.

        O método não aplica qualquer alteração no currículo. Ele existe para
        verificar a fronteira entre preparação interna e porta de recomendação.
        """
        self.contextos.append(contexto)
        return self.recomendacao


def _politica() -> PoliticaLimitesContextoIa:
    """Cria política que identifica a ação de recomendação no teste.

    A função usa limites válidos e uma versão estável em memória. Ela existe
    para confirmar que o preparador resolve a ação nova sem adapter externo.
    """
    limites = LimitesContextoIa(
        limites_campos={
            "empresa": 120,
            "cargo": 120,
            "descricao_experiencia": 1000,
            "descricao_competencia": 100,
            "nivel_competencia": 50,
            "descricao_vaga": 6000,
        },
        orcamento_total_caracteres=10000,
    )
    return PoliticaLimitesContextoIa(
        versao="recomendacao-1",
        padrao=limites,
        teto_seguranca=limites,
        por_acao={
            AcaoAdequacaoSemantica.RECOMENDAR_MODELO_CURRICULO.value: SobrescritaLimitesContextoIa(
                limites_campos={"cargo": 7}
            )
        },
        por_modelo={},
        por_acao_modelo={},
    )


def _experiencia(usuario_id: UsuarioId) -> ExperienciaProfissional:
    """Cria uma experiência própria mínima para o contexto autorizado.

    A função instancia uma entidade válida inteiramente em memória. Ela existe
    para testar seleção de item sem banco ou dependência de framework.
    """
    return ExperienciaProfissional(
        id=ExperienciaProfissionalId(uuid4()),
        usuario_id=usuario_id,
        empresa="Empresa",
        cargo="Desenvolvedora",
        descricao="Construí APIs e integrações.",
        periodo=Periodo(inicio=date(2024, 1, 1), fim=None),
    )


def _curriculo(usuario_id: UsuarioId, referencia: ReferenciaCurriculo) -> Curriculo:
    """Cria versão própria contendo a referência selecionável no cenário.

    A função monta o agregado e inclui a referência pela sua raiz. Ela existe
    para verificar pertencimento sem persistência e sem aplicar recomendação.
    """
    curriculo = Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id,
        titulo_versao="Tecnologia",
        layout=ModeloCurriculo.CLASSICO.value,
        is_public=False,
    )
    curriculo.incluir_referencia(referencia)
    return curriculo


class RecomendarModeloCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica contexto compartilhado, proposta tipada e ausência de escrita.

    Os cenários usam apenas doubles das portas e entidades em memória. A classe
    existe para garantir que sugerir não antecipa o aceite nem modifica layout.
    """

    async def test_gera_recomendacao_com_mesma_entrada_e_sem_alterar_layout(
        self,
    ) -> None:
        """Entrega contexto autorizado ao gerador e devolve proposta revisável.

        O cenário usa a mesma entrada da adequação, confirma ação de política e
        compara o layout antes e depois. Ele existe para proteger a autonomia do
        estudante enquanto a interface decide aceitar ou recusar a sugestão.
        """
        usuario_id = UsuarioId(uuid4())
        experiencia = _experiencia(usuario_id)
        referencia = ReferenciaCurriculo(experiencia.id)
        curriculo = _curriculo(usuario_id, referencia)
        preparador = PreparadorContextoAssistenciaCurriculo(
            RepositorioCurriculoStub(curriculo),
            ConsultaItemStub({referencia: experiencia}),
            FontePoliticaStub(_politica()),
            "gpt-5-nano",
            AcaoAdequacaoSemantica.RECOMENDAR_MODELO_CURRICULO,
        )
        gerador = GeradorRecomendacaoSpy(
            RecomendacaoModeloCurriculo(
                ModeloCurriculo.MODERNO, "Compatível com o contexto informado."
            )
        )
        caso_de_uso = RecomendarModeloCurriculo(preparador, gerador)

        recomendacao = await caso_de_uso.executar(
            SolicitarAdequacaoCurriculoVagaEntrada(
                usuario_id=usuario_id,
                curriculo_id=curriculo.id,
                cargo_alvo="Desenvolvedora",
                descricao_vaga="Vaga para APIs.",
                referencias_selecionadas=(referencia,),
                consentimento_explicito=True,
            )
        )

        self.assertEqual(recomendacao.modelo_recomendado, ModeloCurriculo.MODERNO)
        self.assertEqual(curriculo.layout, ModeloCurriculo.CLASSICO.value)
        self.assertEqual(len(gerador.contextos), 1)
        self.assertEqual(gerador.contextos[0].versao_politica, "recomendacao-1")
        self.assertEqual(gerador.contextos[0].cargo_alvo, "Desenvo")

    async def test_recusa_curriculo_alheio_antes_de_chamar_gerador(self) -> None:
        """Oculta versão alheia sem produzir recomendação por IA.

        O cenário usa dono distinto e espera a falha de consulta conhecida. Ele
        existe para assegurar que o contexto não seja preparado para terceiros.
        """
        dono = UsuarioId(uuid4())
        solicitante = UsuarioId(uuid4())
        experiencia = _experiencia(dono)
        referencia = ReferenciaCurriculo(experiencia.id)
        curriculo = _curriculo(dono, referencia)
        preparador = PreparadorContextoAssistenciaCurriculo(
            RepositorioCurriculoStub(curriculo),
            ConsultaItemStub({referencia: experiencia}),
            FontePoliticaStub(_politica()),
            "gpt-5-nano",
            AcaoAdequacaoSemantica.RECOMENDAR_MODELO_CURRICULO,
        )
        gerador = GeradorRecomendacaoSpy(
            RecomendacaoModeloCurriculo(
                ModeloCurriculo.MODERNO, "Justificativa válida."
            )
        )

        with self.assertRaises(CurriculoNaoEncontrado):
            await RecomendarModeloCurriculo(preparador, gerador).executar(
                SolicitarAdequacaoCurriculoVagaEntrada(
                    usuario_id=solicitante,
                    curriculo_id=curriculo.id,
                    cargo_alvo="Desenvolvedora",
                    descricao_vaga=None,
                    referencias_selecionadas=(referencia,),
                    consentimento_explicito=True,
                )
            )

        self.assertEqual(gerador.contextos, [])
