"""Testa unitariamente o registro e a consulta da decisão sobre recomendações."""

import unittest
from datetime import UTC, datetime
from uuid import uuid4

# Proveniência: decision-analysis prompts/backend/20261025-140000-expor-decisao-recomendacao-v001.md#v001
from backend.application import (
    ConsultarDecisoesRecomendacao,
    ConsultarDecisoesRecomendacaoEntrada,
    CurriculoNaoEncontrado,
    RecomendacaoNaoEncontrada,
    RegistrarDecisaoRecomendacao,
    RegistrarDecisaoRecomendacaoEntrada,
    RevisarVersaoCurriculoEntrada,
)
from backend.domain import (
    Curriculo,
    CurriculoId,
    DecisaoEstudante,
    DecisaoRecomendacao,
    PendenciaRevisao,
    ResultadoRevisao,
    SecaoRevisao,
    SeveridadePendencia,
    UsuarioId,
)

DONO = UsuarioId(uuid4())
OUTRO = UsuarioId(uuid4())
CURRICULO_ID = CurriculoId(uuid4())
INSTANTE = datetime(2026, 10, 25, 14, 0, tzinfo=UTC)
OUTRO_INSTANTE = datetime(2026, 10, 26, 9, 30, tzinfo=UTC)

AVISO = PendenciaRevisao(
    codigo="PROJETO_AUSENTE",
    secao=SecaoRevisao.PROJETOS_ACADEMICOS,
    mensagem="Considere incluir um projeto acadêmico na versão.",
    severidade=SeveridadePendencia.AVISO,
)
ERRO = PendenciaRevisao(
    codigo="CONTATO_AUSENTE",
    secao=SecaoRevisao.DADOS_PESSOAIS,
    mensagem="Informe o endereço e ao menos um telefone de contato.",
    severidade=SeveridadePendencia.ERRO,
)


class RevisorStub:
    """Substitui a revisão da versão e registra as entradas recebidas.

    O double devolve o resultado configurado ou levanta o erro configurado, sem
    prévia, banco ou regras de domínio. Ele existe para testar a decisão
    isolada da revisão.
    """

    def __init__(
        self,
        resultado: ResultadoRevisao | None = None,
        erro: Exception | None = None,
    ) -> None:
        """Guarda o comportamento configurado e inicia o histórico de chamadas.

        O construtor não acessa recursos externos. Ele existe para que cada teste
        configure sucesso ou falha de forma explícita.
        """
        self._resultado = resultado
        self._erro = erro
        self.entradas: list[RevisarVersaoCurriculoEntrada] = []

    async def executar(self, entrada: RevisarVersaoCurriculoEntrada) -> ResultadoRevisao:
        """Registra a entrada e devolve o resultado ou levanta o erro configurado.

        O método não faz I/O. Ele existe para tornar observável o que a decisão
        pediu à revisão.
        """
        self.entradas.append(entrada)
        if self._erro is not None:
            raise self._erro
        assert self._resultado is not None
        return self._resultado


class RepositorioDecisaoMemoria:
    """Substitui a persistência das decisões guardando-as em um dicionário.

    O double mantém uma decisão por versão e código, como o adapter real, e
    conta as operações. Ele existe para observar o que é gravado e consultado
    sem banco.
    """

    def __init__(self) -> None:
        """Inicia o armazenamento vazio e o contador de consultas.

        O construtor não acessa recursos externos. Ele existe para isolar o
        estado de cada teste.
        """
        self.decisoes: dict[tuple[CurriculoId, str], DecisaoRecomendacao] = {}
        self.consultas = 0

    async def salvar(self, decisao: DecisaoRecomendacao) -> None:
        """Grava a decisão, substituindo a anterior do mesmo par.

        O método usa a versão e o código como chave. Ele existe para reproduzir a
        regra de uma decisão por par.
        """
        self.decisoes[(decisao.curriculo_id, decisao.codigo)] = decisao

    async def listar_por_curriculo(
        self, curriculo_id: CurriculoId
    ) -> tuple[DecisaoRecomendacao, ...]:
        """Lista as decisões da versão em ordem do código e conta a consulta.

        O método filtra pela versão e ordena pelo código. Ele existe para
        observar se a consulta chegou a ler decisões.
        """
        self.consultas += 1
        return tuple(
            decisao
            for (versao, _), decisao in sorted(
                self.decisoes.items(), key=lambda item: item[0][1]
            )
            if versao == curriculo_id
        )


class RepositorioCurriculoStub:
    """Substitui a porta de currículo devolvendo a versão configurada.

    O double devolve a versão se o identificador coincidir. Ele existe para
    testar a verificação de propriedade da consulta sem banco.
    """

    def __init__(self, curriculo: Curriculo | None) -> None:
        """Guarda a versão que o double conhece.

        O construtor não acessa recursos externos. Ele existe para controlar a
        existência e o dono da versão em cada cenário.
        """
        self._curriculo = curriculo

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Devolve a versão guardada se o identificador coincidir.

        O método compara somente em memória. Ele existe para simular a leitura
        aguardável da porta.
        """
        if self._curriculo is not None and self._curriculo.id == curriculo_id:
            return self._curriculo
        return None


class RelogioFixo:
    """Substitui a porta de relógio por um instante configurável.

    O double devolve o instante atual guardado, que o teste pode trocar. Ele
    existe para tornar a data da decisão determinística.
    """

    def __init__(self, instante: datetime) -> None:
        """Guarda o instante devolvido pelas próximas leituras.

        O construtor não acessa o relógio do sistema. Ele existe para que cada
        teste controle o tempo.
        """
        self.instante = instante

    def agora(self) -> datetime:
        """Devolve o instante configurado.

        O método não consulta fonte de tempo externa. Ele existe para satisfazer a
        porta ``Relogio`` com um valor previsível.
        """
        return self.instante


def criar_curriculo(usuario_id: UsuarioId = DONO) -> Curriculo:
    """Cria uma versão de currículo válida do usuário informado.

    A função monta o agregado sem acessar gerador, banco ou relógio. Ela existe
    para controlar o dono da versão nos testes de consulta.
    """
    return Curriculo(
        id=CURRICULO_ID,
        usuario_id=usuario_id,
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


def _entrada(codigo: str = "PROJETO_AUSENTE", decisao=DecisaoEstudante.REJEITADA):
    """Cria a entrada de registro do dono para a versão e o código dados.

    A função monta o DTO tipado com valores padrão. Ela existe para reduzir
    repetição nos testes.
    """
    return RegistrarDecisaoRecomendacaoEntrada(DONO, CURRICULO_ID, codigo, decisao)


class RegistrarDecisaoRecomendacaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica as decisões de fluxo de ``RegistrarDecisaoRecomendacao``.

    A classe substitui a revisão, a persistência e o relógio por doubles e
    observa o resultado e o que foi gravado. Ela existe para proteger a regra de
    que só avisos da própria versão podem ser decididos.
    """

    async def test_grava_a_decisao_de_um_aviso_com_o_instante_do_relogio(self) -> None:
        """Confirma que a decisão sobre um aviso é gravada e devolvida.

        O teste decide sobre um aviso da revisão e confere o resultado, o que foi
        gravado e a entrada enviada à revisão. Ele existe para o caminho feliz.
        """
        revisor = RevisorStub(ResultadoRevisao(pendencias=(AVISO,)))
        repositorio = RepositorioDecisaoMemoria()
        caso = RegistrarDecisaoRecomendacao(revisor, repositorio, RelogioFixo(INSTANTE))

        decisao = await caso.executar(_entrada())

        esperada = DecisaoRecomendacao(
            CURRICULO_ID, "PROJETO_AUSENTE", DecisaoEstudante.REJEITADA, INSTANTE
        )
        self.assertEqual(decisao, esperada)
        self.assertEqual(list(repositorio.decisoes.values()), [esperada])
        self.assertEqual(revisor.entradas, [RevisarVersaoCurriculoEntrada(DONO, CURRICULO_ID)])

    async def test_recusa_codigo_que_nao_e_recomendacao_da_revisao(self) -> None:
        """Confirma que um código inexistente na revisão é recusado sem gravar.

        O teste decide sobre um código que a revisão não apontou. Ele existe para
        que não se grave decisão sobre recomendação inventada.
        """
        repositorio = RepositorioDecisaoMemoria()
        caso = RegistrarDecisaoRecomendacao(
            RevisorStub(ResultadoRevisao(pendencias=(AVISO,))),
            repositorio,
            RelogioFixo(INSTANTE),
        )

        with self.assertRaises(RecomendacaoNaoEncontrada):
            await caso.executar(_entrada(codigo="IDIOMA_AUSENTE"))

        self.assertEqual(repositorio.decisoes, {})

    async def test_recusa_decisao_sobre_pendencia_que_e_erro(self) -> None:
        """Confirma que um erro não pode ser aceito nem rejeitado.

        O teste decide sobre uma pendência de severidade erro. Ele existe porque
        só as recomendações (avisos) admitem decisão do estudante.
        """
        repositorio = RepositorioDecisaoMemoria()
        caso = RegistrarDecisaoRecomendacao(
            RevisorStub(ResultadoRevisao(pendencias=(ERRO, AVISO))),
            repositorio,
            RelogioFixo(INSTANTE),
        )

        with self.assertRaises(RecomendacaoNaoEncontrada):
            await caso.executar(_entrada(codigo="CONTATO_AUSENTE"))

        self.assertEqual(repositorio.decisoes, {})

    async def test_propaga_versao_ausente_ou_alheia_sem_gravar(self) -> None:
        """Confirma que a falha de versão não encontrada chega ao chamador.

        O teste faz a revisão levantar a falha. Ele existe para que nada seja
        gravado sobre versão inexistente ou de outro estudante.
        """
        repositorio = RepositorioDecisaoMemoria()
        caso = RegistrarDecisaoRecomendacao(
            RevisorStub(erro=CurriculoNaoEncontrado("Versão de currículo não encontrada.")),
            repositorio,
            RelogioFixo(INSTANTE),
        )

        with self.assertRaises(CurriculoNaoEncontrado):
            await caso.executar(_entrada())

        self.assertEqual(repositorio.decisoes, {})

    async def test_decidir_de_novo_substitui_a_decisao_anterior(self) -> None:
        """Confirma que a nova decisão do mesmo código substitui a anterior.

        O teste aceita e depois rejeita a mesma recomendação, com relógios
        diferentes. Ele existe para que haja uma só decisão por código, a mais
        recente.
        """
        relogio = RelogioFixo(INSTANTE)
        repositorio = RepositorioDecisaoMemoria()
        caso = RegistrarDecisaoRecomendacao(
            RevisorStub(ResultadoRevisao(pendencias=(AVISO,))), repositorio, relogio
        )

        await caso.executar(_entrada(decisao=DecisaoEstudante.ACEITA))
        relogio.instante = OUTRO_INSTANTE
        await caso.executar(_entrada(decisao=DecisaoEstudante.REJEITADA))

        self.assertEqual(
            list(repositorio.decisoes.values()),
            [
                DecisaoRecomendacao(
                    CURRICULO_ID,
                    "PROJETO_AUSENTE",
                    DecisaoEstudante.REJEITADA,
                    OUTRO_INSTANTE,
                )
            ],
        )


class ConsultarDecisoesRecomendacaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica as decisões de fluxo de ``ConsultarDecisoesRecomendacao``.

    A classe substitui as portas por doubles e observa o resultado e as leituras.
    Ela existe para proteger a regra de que só o dono consulta as decisões da
    versão.
    """

    async def test_lista_as_decisoes_da_versao_do_dono(self) -> None:
        """Confirma que o dono recebe as decisões da própria versão em ordem.

        O teste grava duas decisões fora de ordem e lê. Ele existe para o caminho
        feliz e para a ordem estável pelo código.
        """
        repositorio = RepositorioDecisaoMemoria()
        for codigo in ("PROJETO_AUSENTE", "IDIOMA_AUSENTE"):
            await repositorio.salvar(
                DecisaoRecomendacao(CURRICULO_ID, codigo, DecisaoEstudante.ACEITA, INSTANTE)
            )
        caso = ConsultarDecisoesRecomendacao(
            RepositorioCurriculoStub(criar_curriculo()), repositorio
        )

        decisoes = await caso.executar(ConsultarDecisoesRecomendacaoEntrada(DONO, CURRICULO_ID))

        self.assertEqual(
            [decisao.codigo for decisao in decisoes],
            ["IDIOMA_AUSENTE", "PROJETO_AUSENTE"],
        )

    async def test_versao_ausente_ou_alheia_falha_sem_ler_decisoes(self) -> None:
        """Confirma que ausência e versão de outro estudante falham do mesmo modo.

        O teste consulta com uma versão inexistente e com uma versão de outro
        dono. Ele existe para impedir a leitura das decisões de versões alheias.
        """
        casos = (
            ("inexistente", RepositorioCurriculoStub(None)),
            ("de outro estudante", RepositorioCurriculoStub(criar_curriculo(OUTRO))),
        )
        for descricao, repositorio_curriculo in casos:
            with self.subTest(versao=descricao):
                repositorio = RepositorioDecisaoMemoria()
                caso = ConsultarDecisoesRecomendacao(repositorio_curriculo, repositorio)

                with self.assertRaises(CurriculoNaoEncontrado):
                    await caso.executar(ConsultarDecisoesRecomendacaoEntrada(DONO, CURRICULO_ID))

                self.assertEqual(repositorio.consultas, 0)

    async def test_versao_sem_decisoes_devolve_tupla_vazia(self) -> None:
        """Confirma que uma versão sem decisões devolve uma tupla vazia.

        O teste consulta uma versão do dono sem nenhuma decisão. Ele existe para
        o caso de uma revisão ainda sem escolhas.
        """
        caso = ConsultarDecisoesRecomendacao(
            RepositorioCurriculoStub(criar_curriculo()), RepositorioDecisaoMemoria()
        )

        self.assertEqual(
            await caso.executar(ConsultarDecisoesRecomendacaoEntrada(DONO, CURRICULO_ID)), ()
        )
