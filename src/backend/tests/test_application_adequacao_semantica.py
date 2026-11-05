"""Testa unitariamente a orquestração da adequação semântica de currículo."""

import unittest
from datetime import date
from uuid import uuid4

from backend.application.adequacao_semantica import (
    ContextoAdequacaoCurriculoVaga,
    ItemAdequacaoNaoEncontrado,
    SolicitarAdequacaoCurriculoVaga,
    SolicitarAdequacaoCurriculoVagaEntrada,
)
from backend.application.politica_limites_contexto_ia import (
    LimitesContextoIa,
    PoliticaLimitesContextoIa,
)
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain import (
    CategoriaCompetencia,
    Competencia,
    CompetenciaId,
    Curriculo,
    CurriculoId,
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    Periodo,
    ReferenciaCurriculo,
    SugestaoAdequacao,
    TipoSugestaoAdequacao,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261020-163820-adequacao-semantica-gpt-nano-v001.md#v001


class RepositorioCurriculoStub:
    """Substitui a consulta de currículo por respostas mantidas em memória.

    O double devolve somente os currículos configurados e registra as consultas,
    sem acessar banco ou adapter produtivo. Ele existe para isolar a verificação
    de propriedade feita pelo caso de uso.
    """

    def __init__(self, curriculo: Curriculo | None) -> None:
        """Guarda uma resposta controlada para a consulta por identidade.

        O construtor recebe a versão que o cenário deseja disponibilizar. Ele
        existe para representar presença, ausência ou propriedade alheia.
        """
        self.curriculo = curriculo
        self.consultas: list[CurriculoId] = []

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Registra a leitura e devolve a versão somente para seu próprio ID.

        O método simula a porta assíncrona sem I/O. Ele existe para que os testes
        observem a ordem do fluxo de orquestração.
        """
        self.consultas.append(curriculo_id)
        if self.curriculo is not None and self.curriculo.id == curriculo_id:
            return self.curriculo
        return None


class ConsultaItemStub:
    """Substitui a leitura de itens por um mapa de respostas controladas.

    O double responde pelo identificador tipado e registra cada referência, sem
    consultar persistência. Ele existe para testar seleção e minimização de
    contexto no caso de uso isolado.
    """

    def __init__(self, itens: dict[ReferenciaCurriculo, object]) -> None:
        """Armazena itens controlados pelo cenário e inicia o histórico vazio.

        O construtor usa o mapa diretamente porque os itens são imutáveis. Ele
        existe para tornar ausências e respostas alheias reproduzíveis.
        """
        self.itens = itens
        self.consultas: list[ReferenciaCurriculo] = []

    async def obter_item(self, referencia: ReferenciaCurriculo) -> object | None:
        """Registra a referência e devolve a resposta configurada para ela.

        O método não aplica decisão de proprietário nem limite de texto. Ele
        existe para deixar essas regras observáveis no caso de uso.
        """
        self.consultas.append(referencia)
        return self.itens.get(referencia)


class FontePoliticaStub:
    """Fornece uma política fixa e válida sem ler configuração externa.

    O double devolve sempre a mesma política em memória. Ele existe para que os
    testes exercitem a resolução de limites sem arquivo ou adapter real.
    """

    def __init__(self, politica: PoliticaLimitesContextoIa) -> None:
        """Guarda a política previamente construída pelo cenário de teste.

        O construtor não transforma os dados recebidos. Ele existe para manter
        a política explícita e determinística em cada teste.
        """
        self.politica = politica

    def obter(self) -> PoliticaLimitesContextoIa:
        """Devolve a política fixa configurada para a solicitação.

        O método não acessa filesystem nem altera o objeto. Ele existe para
        substituir a fonte de política na unidade sob teste.
        """
        return self.politica


class GeradorSpy:
    """Registra o contexto recebido e devolve sugestões controladas.

    O double não chama modelo, rede ou SDK; ele apenas conserva o contexto
    entregue pelo caso de uso. Ele existe para verificar consentimento e dados
    mínimos antes da futura implementação de um adapter.
    """

    def __init__(self, sugestoes: tuple[SugestaoAdequacao, ...]) -> None:
        """Define as sugestões a devolver e inicia o histórico de chamadas.

        O construtor recebe sugestões de domínio já tipadas. Ele existe para
        manter a validação final de proposta no próprio domínio.
        """
        self.sugestoes = sugestoes
        self.contextos: list[ContextoAdequacaoCurriculoVaga] = []

    async def gerar(
        self, contexto: ContextoAdequacaoCurriculoVaga
    ) -> tuple[SugestaoAdequacao, ...]:
        """Registra o contexto e devolve o resultado configurado.

        O método simula a fronteira assíncrona do gerador sem efeito externo. Ele
        existe para tornar verificável exatamente o conteúdo que seria enviado.
        """
        self.contextos.append(contexto)
        return self.sugestoes


def _politica() -> PoliticaLimitesContextoIa:
    """Cria limites pequenos e seguros para os cenários de unidade.

    A função reutiliza os mesmos limites como padrão e teto, sem sobrescritas.
    Ela existe para tornar cortes de texto e orçamento fáceis de verificar.
    """
    limites = LimitesContextoIa(
        limites_campos={
            "empresa": 6,
            "cargo": 8,
            "descricao_experiencia": 12,
            "descricao_competencia": 8,
            "nivel_competencia": 8,
            "descricao_vaga": 12,
        },
        orcamento_total_caracteres=200,
    )
    return PoliticaLimitesContextoIa(
        versao="teste-1",
        padrao=limites,
        teto_seguranca=limites,
        por_acao={},
        por_modelo={},
        por_acao_modelo={},
    )


def _experiencia(usuario_id: UsuarioId) -> ExperienciaProfissional:
    """Cria uma experiência própria com textos maiores que os limites de teste.

    A função fixa os demais atributos válidos da entidade. Ela existe para que
    os testes observem a aplicação de limites por campo no contexto.
    """
    return ExperienciaProfissional(
        id=ExperienciaProfissionalId(uuid4()),
        usuario_id=usuario_id,
        empresa="Empresa muito longa",
        cargo="Desenvolvedora",
        descricao="Descrição profissional extensa.",
        periodo=Periodo(inicio=date(2024, 1, 1), fim=None),
    )


def _competencia(usuario_id: UsuarioId) -> Competencia:
    """Cria uma competência própria para testar uma seleção múltipla.

    A função constrói os campos mínimos aceitos pelo domínio. Ela existe para
    montar um segundo tipo profissional sem depender de persistência.
    """
    return Competencia(
        id=CompetenciaId(uuid4()),
        usuario_id=usuario_id,
        categoria=CategoriaCompetencia.TECNICA,
        descricao="Arquitetura de software",
        nivel="Avançado",
    )


def _curriculo(usuario_id: UsuarioId, *referencias: ReferenciaCurriculo) -> Curriculo:
    """Cria uma versão própria já composta pelas referências fornecidas.

    A função inclui cada referência pela raiz do agregado. Ela existe para que
    os cenários controlem a seleção persistida do currículo.
    """
    curriculo = Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id,
        titulo_versao="Estágio",
        layout="classico",
        is_public=False,
    )
    for referencia in referencias:
        curriculo.incluir_referencia(referencia)
    return curriculo


class SolicitarAdequacaoCurriculoVagaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a orquestração isolada da assistência revisável a uma vaga.

    Os cenários usam somente doubles e entidades de domínio em memória. A classe
    existe para impedir envio de contexto não autorizado ou alteração automática
    antes que adapters externos sejam adicionados.
    """

    async def test_gera_proposta_com_contexto_limitado_e_sem_mutar_curriculo(self) -> None:
        """Envia somente o item escolhido e devolve proposta revisável.

        O cenário seleciona uma experiência própria, confere cortes da política
        e verifica que a versão não é persistida. Ele existe para garantir que a
        assistência seja leitura controlada, não edição automática.
        """
        usuario_id = UsuarioId(uuid4())
        experiencia = _experiencia(usuario_id)
        referencia = ReferenciaCurriculo(experiencia.id)
        curriculo = _curriculo(usuario_id, referencia)
        sugestao = SugestaoAdequacao(
            codigo="EXPERIENCIA_1",
            tipo=TipoSugestaoAdequacao.EXPERIENCIA,
            referencia_item=referencia,
            texto_sugerido="Atuei no desenvolvimento de software.",
            justificativa="Evidencia experiência relevante.",
        )
        gerador = GeradorSpy((sugestao,))
        caso_de_uso = SolicitarAdequacaoCurriculoVaga(
            RepositorioCurriculoStub(curriculo),
            ConsultaItemStub({referencia: experiencia}),
            FontePoliticaStub(_politica()),
            gerador,
            "gpt-5-nano",
        )

        proposta = await caso_de_uso.executar(
            SolicitarAdequacaoCurriculoVagaEntrada(
                usuario_id=usuario_id,
                curriculo_id=curriculo.id,
                cargo_alvo="Desenvolvedora de software",
                descricao_vaga="Vaga com integrações complexas.",
                referencias_selecionadas=(referencia,),
                consentimento_explicito=True,
            )
        )

        self.assertEqual(proposta.sugestoes, (sugestao,))
        self.assertEqual(curriculo.referencias, frozenset({referencia}))
        self.assertEqual(len(gerador.contextos), 1)
        contexto = gerador.contextos[0]
        self.assertEqual(contexto.cargo_alvo, "Desenvol")
        self.assertEqual(contexto.descricao_vaga, "Vaga com int")
        self.assertIn("Empresa: Empres", contexto.itens_selecionados[0].conteudo)
        self.assertIn("Cargo: Desenvol", contexto.itens_selecionados[0].conteudo)
        self.assertIn("Descrição: Descrição pr", contexto.itens_selecionados[0].conteudo)
        self.assertEqual(contexto.versao_politica, "teste-1")

    async def test_recusa_curriculo_alheio_sem_consultar_item_ou_gerador(self) -> None:
        """Oculta versão alheia antes de qualquer leitura de contexto.

        O cenário solicita a versão de outro estudante e verifica que nenhuma
        porta de item ou geração foi usada. Ele existe para impedir vazamento de
        conteúdo profissional por uma tentativa não autorizada.
        """
        dono = UsuarioId(uuid4())
        solicitante = UsuarioId(uuid4())
        experiencia = _experiencia(dono)
        referencia = ReferenciaCurriculo(experiencia.id)
        curriculo = _curriculo(dono, referencia)
        consulta = ConsultaItemStub({referencia: experiencia})
        gerador = GeradorSpy(())
        caso_de_uso = SolicitarAdequacaoCurriculoVaga(
            RepositorioCurriculoStub(curriculo), consulta, FontePoliticaStub(_politica()), gerador, "gpt-5-nano"
        )

        with self.assertRaises(CurriculoNaoEncontrado):
            await caso_de_uso.executar(
                SolicitarAdequacaoCurriculoVagaEntrada(
                    usuario_id=solicitante,
                    curriculo_id=curriculo.id,
                    cargo_alvo="Desenvolvedora",
                    descricao_vaga=None,
                    referencias_selecionadas=(referencia,),
                    consentimento_explicito=True,
                )
            )

        self.assertEqual(consulta.consultas, [])
        self.assertEqual(gerador.contextos, [])

    async def test_recusa_falta_de_consentimento_sem_chamar_gerador(self) -> None:
        """Deixa o domínio bloquear consentimento ausente antes da geração.

        O cenário usa item próprio e consentimento falso, esperando a falha de
        domínio e ausência de chamada à porta. Ele existe para garantir que a
        confirmação explícita seja condição anterior ao envio externo.
        """
        usuario_id = UsuarioId(uuid4())
        experiencia = _experiencia(usuario_id)
        referencia = ReferenciaCurriculo(experiencia.id)
        curriculo = _curriculo(usuario_id, referencia)
        gerador = GeradorSpy(())
        caso_de_uso = SolicitarAdequacaoCurriculoVaga(
            RepositorioCurriculoStub(curriculo),
            ConsultaItemStub({referencia: experiencia}),
            FontePoliticaStub(_politica()),
            gerador,
            "gpt-5-nano",
        )

        with self.assertRaisesRegex(Exception, "consentimento explícito"):
            await caso_de_uso.executar(
                SolicitarAdequacaoCurriculoVagaEntrada(
                    usuario_id=usuario_id,
                    curriculo_id=curriculo.id,
                    cargo_alvo="Desenvolvedora",
                    descricao_vaga=None,
                    referencias_selecionadas=(referencia,),
                    consentimento_explicito=False,
                )
            )

        self.assertEqual(gerador.contextos, [])

    async def test_recusa_referencia_nao_selecionada_no_curriculo(self) -> None:
        """Impede usar um item próprio que não integra a versão solicitada.

        O cenário configura uma competência própria fora das referências da
        versão e verifica a falha genérica. Ele existe para limitar a assistência
        exatamente ao conteúdo escolhido para aquele currículo.
        """
        usuario_id = UsuarioId(uuid4())
        experiencia = _experiencia(usuario_id)
        competencia = _competencia(usuario_id)
        referencia_experiencia = ReferenciaCurriculo(experiencia.id)
        referencia_competencia = ReferenciaCurriculo(competencia.id)
        curriculo = _curriculo(usuario_id, referencia_experiencia)
        gerador = GeradorSpy(())
        caso_de_uso = SolicitarAdequacaoCurriculoVaga(
            RepositorioCurriculoStub(curriculo),
            ConsultaItemStub({referencia_competencia: competencia}),
            FontePoliticaStub(_politica()),
            gerador,
            "gpt-5-nano",
        )

        with self.assertRaises(ItemAdequacaoNaoEncontrado):
            await caso_de_uso.executar(
                SolicitarAdequacaoCurriculoVagaEntrada(
                    usuario_id=usuario_id,
                    curriculo_id=curriculo.id,
                    cargo_alvo="Desenvolvedora",
                    descricao_vaga=None,
                    referencias_selecionadas=(referencia_competencia,),
                    consentimento_explicito=True,
                )
            )

        self.assertEqual(gerador.contextos, [])
