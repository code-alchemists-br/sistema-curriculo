"""Testa unitariamente a criação de associação currículo-vaga."""

import unittest
from uuid import uuid4

from backend.application import (
    AdicionarClassificacaoAssociacaoCurriculoVaga,
    AlterarClassificacaoAssociacaoCurriculoVagaEntrada,
    AssociacaoCurriculoVagaJaExiste,
    AssociacaoCurriculoVagaNaoEncontrada,
    CriarAssociacaoCurriculoVaga,
    CriarAssociacaoCurriculoVagaEntrada,
    CurriculoNaoEncontrado,
    RemoverClassificacaoAssociacaoCurriculoVaga,
)
from backend.domain import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
    Curriculo,
    CurriculoId,
    RegraDeDominioViolada,
    UsuarioId,
    VagaId,
)

# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004


class RepositorioCurriculoStub:
    """Substitui a consulta de currículo por valores controlados em memória.

    O stub devolve um agregado ou ausência e registra IDs consultados, sem usar
    persistência. Ele existe para testar ownership e a ordem de decisão do caso
    de uso sem adapter externo.
    """

    def __init__(self, curriculos: dict[CurriculoId, Curriculo] | None = None) -> None:
        """Armazena currículos de teste indexados por identidade.

        O construtor copia o mapa fornecido para isolar o estado do double. Ele
        existe para tornar determinísticos os cenários de currículo próprio,
        ausente e pertencente a outro usuário.
        """
        self._curriculos = dict(curriculos or {})
        self.consultas: list[CurriculoId] = []

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Retorna o currículo configurado e registra a consulta.

        A operação lê apenas o estado em memória preparado pelo teste. Ela
        existe para substituir a porta assíncrona de repositório.
        """
        self.consultas.append(curriculo_id)
        return self._curriculos.get(curriculo_id)


class RepositorioAssociacaoSpy:
    """Substitui consulta e salvamento de associações por estado em memória.

    O spy controla quais pares já existem e registra agregados enviados para
    persistência. Ele existe para observar as decisões da Application sem banco
    ou repository adapter.
    """

    def __init__(
        self,
        pares_existentes: set[tuple[CurriculoId, VagaId]] | None = None,
        associacoes: dict[tuple[CurriculoId, VagaId], AssociacaoCurriculoVaga]
        | None = None,
    ) -> None:
        """Prepara os pares existentes e um histórico vazio de salvamentos.

        O construtor copia os pares para manter cada cenário isolado. Ele existe
        para testar rejeição de duplicidade e criação de pares novos.
        """
        self._pares_existentes = set(pares_existentes or set())
        self._associacoes = dict(associacoes or {})
        self.consultas: list[tuple[CurriculoId, VagaId]] = []
        self.associacoes_salvas: list[AssociacaoCurriculoVaga] = []
        self.associacoes_carregadas: list[tuple[CurriculoId, VagaId]] = []
        self.associacoes_atualizadas: list[AssociacaoCurriculoVaga] = []

    async def existe_por_par(self, curriculo_id: CurriculoId, vaga_id: VagaId) -> bool:
        """Informa se o par foi configurado como existente e registra a consulta.

        A resposta consulta somente o conjunto local do teste. Ela existe para
        simular a checagem preventiva requerida pelo caso de uso.
        """
        par = (curriculo_id, vaga_id)
        self.consultas.append(par)
        return par in self._pares_existentes

    async def salvar(self, associacao: AssociacaoCurriculoVaga) -> None:
        """Registra o agregado recebido sem executar I/O.

        O método conserva a instância para permitir a verificação de
        classificações normalizadas e do número de chamadas de persistência.
        Ele existe para substituir a porta externa durante os testes unitários.
        """
        self.associacoes_salvas.append(associacao)

    async def obter_para_atualizacao(
        self, curriculo_id: CurriculoId, vaga_id: VagaId
    ) -> AssociacaoCurriculoVaga | None:
        """Retorna agregado configurado e registra a chave consultada.

        O double consulta o mapa em memória sem reproduzir lógica de domínio.
        Ele existe para verificar o fluxo de atualização pela identidade composta.
        """
        par = (curriculo_id, vaga_id)
        self.associacoes_carregadas.append(par)
        return self._associacoes.get(par)

    async def atualizar_classificacoes(
        self, associacao: AssociacaoCurriculoVaga
    ) -> None:
        """Registra o agregado atualizado sem executar I/O.

        A operação conserva a instância entregue pela Application. Ela existe
        para verificar que estados idempotentes não solicitam persistência.
        """
        self.associacoes_atualizadas.append(associacao)


def _criar_curriculo(usuario_id: UsuarioId | None = None) -> Curriculo:
    """Cria um currículo válido para cenários do caso de uso.

    A função constrói um agregado em memória com proprietário controlável. Ela
    existe para que os testes foquem nas decisões de criação da associação.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id or UsuarioId(uuid4()),
        titulo_versao="Currículo de teste",
        layout="classico",
        is_public=False,
    )


def _criar_entrada(
    curriculo: Curriculo,
    classificacoes: tuple[ClassificacaoAssociacao, ...] | None = None,
) -> CriarAssociacaoCurriculoVagaEntrada:
    """Monta uma entrada tipada com classificações válidas por padrão.

    A função usa o proprietário do currículo como ator e gera uma vaga de teste.
    Ela existe para reduzir preparação repetida sem esconder os dados do fluxo.
    """
    return CriarAssociacaoCurriculoVagaEntrada(
        usuario_id=curriculo.usuario_id,
        curriculo_id=curriculo.id,
        vaga_id=VagaId("vaga-teste"),
        classificacoes=(
            classificacoes
            if classificacoes is not None
            else (ClassificacaoAssociacao.INTERESSE,)
        ),
    )


class CriarAssociacaoCurriculoVagaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o fluxo interno de criação com todas as portas substituídas.

    A classe usa somente stubs/spies em memória e agrega domínio reais. Ela
    existe para proteger ownership, duplicidade, delegação das invariantes e
    solicitação de salvamento sem envolver API ou infraestrutura.
    """

    async def test_cria_associacao_para_curriculo_proprio_e_solicita_salvamento(
        self,
    ) -> None:
        """Confirma que um currículo próprio ainda não associado é criado.

        O teste fornece currículo e par inexistente, depois compara o agregado
        devolvido e o encaminhado ao port. Ele existe para validar o caminho
        normal da intenção de criação.
        """
        curriculo = _criar_curriculo()
        entrada = _criar_entrada(curriculo)
        repositorio_curriculo = RepositorioCurriculoStub({curriculo.id: curriculo})
        repositorio_associacao = RepositorioAssociacaoSpy()

        resultado = await CriarAssociacaoCurriculoVaga(
            repositorio_curriculo, repositorio_associacao
        ).executar(entrada)

        self.assertIsInstance(resultado, AssociacaoCurriculoVaga)
        self.assertEqual(resultado.curriculo_id, curriculo.id)
        self.assertEqual(resultado.vaga_id, entrada.vaga_id)
        self.assertEqual(repositorio_curriculo.consultas, [curriculo.id])
        self.assertEqual(
            repositorio_associacao.consultas, [(curriculo.id, entrada.vaga_id)]
        )
        self.assertEqual(repositorio_associacao.associacoes_salvas, [resultado])

    async def test_rejeita_curriculo_inexistente_sem_consultar_ou_salvar_associacao(
        self,
    ) -> None:
        """Confirma que currículo ausente encerra o fluxo antes de qualquer gravação.

        O teste usa o stub vazio e observa a falha e os efeitos ausentes. Ele
        existe para manter o comportamento de ausência do caso de uso explícito.
        """
        curriculo = _criar_curriculo()
        entrada = _criar_entrada(curriculo)
        repositorio_associacao = RepositorioAssociacaoSpy()

        with self.assertRaises(CurriculoNaoEncontrado):
            await CriarAssociacaoCurriculoVaga(
                RepositorioCurriculoStub(), repositorio_associacao
            ).executar(entrada)

        self.assertEqual(repositorio_associacao.consultas, [])
        self.assertEqual(repositorio_associacao.associacoes_salvas, [])


class AtualizarClassificacaoAssociacaoCurriculoVagaTestCase(
    unittest.IsolatedAsyncioTestCase
):
    """Verifica as intenções de atualização com ports substituídos.

    Os cenários usam currículo e associação em memória, observam ordem de
    ownership, delegação ao Domain e chamadas de escrita. A classe existe para
    proteger a orquestração sem HTTP ou banco.
    """

    def setUp(self) -> None:
        """Prepara proprietário, par e classificação inicial determinísticos.

        O método cria os agregados reais de Domain e os doubles dos ports. Ele
        existe para que cada teste foque em uma decisão de Application.
        """
        self.curriculo = _criar_curriculo()
        self.vaga_id = VagaId("vaga-atualizacao")
        self.par = (self.curriculo.id, self.vaga_id)
        self.associacao = AssociacaoCurriculoVaga(
            self.curriculo.id,
            self.vaga_id,
            (ClassificacaoAssociacao.INTERESSE,),
        )
        self.repositorio_curriculo = RepositorioCurriculoStub(
            {self.curriculo.id: self.curriculo}
        )
        self.repositorio_associacao = RepositorioAssociacaoSpy(
            associacoes={self.par: self.associacao}
        )
        self.entrada = AlterarClassificacaoAssociacaoCurriculoVagaEntrada(
            usuario_id=self.curriculo.usuario_id,
            curriculo_id=self.curriculo.id,
            vaga_id=self.vaga_id,
            classificacao=ClassificacaoAssociacao.COMPATIBILIDADE,
        )

    async def test_adiciona_classificacao_e_atualiza_associacao_existente(self) -> None:
        """Persiste a classificação adicionada sem substituir o agregado.

        O teste executa a intenção como proprietário e compara o estado e a
        chave consultada. Ele existe para comprovar atualização pelo par exato.
        """
        resultado = await AdicionarClassificacaoAssociacaoCurriculoVaga(
            self.repositorio_curriculo, self.repositorio_associacao
        ).executar(self.entrada)

        self.assertIs(resultado, self.associacao)
        self.assertEqual(
            resultado.classificacoes,
            frozenset(
                {
                    ClassificacaoAssociacao.INTERESSE,
                    ClassificacaoAssociacao.COMPATIBILIDADE,
                }
            ),
        )
        self.assertEqual(self.repositorio_associacao.associacoes_carregadas, [self.par])
        self.assertEqual(
            self.repositorio_associacao.associacoes_atualizadas, [resultado]
        )
        self.assertEqual(self.repositorio_associacao.associacoes_salvas, [])

    async def test_adicao_idempotente_nao_solicita_atualizacao(self) -> None:
        """Evita escrita quando a classificação já está presente.

        O teste envia novamente interesse ao agregado existente e confirma que
        o repository não recebe atualização. Ele existe para tornar retries
        idempotentes até na camada de persistência.
        """
        entrada = AlterarClassificacaoAssociacaoCurriculoVagaEntrada(
            self.curriculo.usuario_id,
            self.curriculo.id,
            self.vaga_id,
            ClassificacaoAssociacao.INTERESSE,
        )

        await AdicionarClassificacaoAssociacaoCurriculoVaga(
            self.repositorio_curriculo, self.repositorio_associacao
        ).executar(entrada)

        self.assertEqual(self.repositorio_associacao.associacoes_atualizadas, [])

    async def test_remove_classificacao_e_persiste_estado_resultante(self) -> None:
        """Remove uma classificação preservando as demais classificações.

        O teste parte de interesse e compatibilidade e remove compatibilidade.
        Ele existe para comprovar que a Application persiste a transição do
        agregado, não cria uma nova associação.
        """
        self.associacao.adicionar_classificacao(ClassificacaoAssociacao.COMPATIBILIDADE)
        entrada = AlterarClassificacaoAssociacaoCurriculoVagaEntrada(
            self.curriculo.usuario_id,
            self.curriculo.id,
            self.vaga_id,
            ClassificacaoAssociacao.COMPATIBILIDADE,
        )

        resultado = await RemoverClassificacaoAssociacaoCurriculoVaga(
            self.repositorio_curriculo, self.repositorio_associacao
        ).executar(entrada)

        self.assertEqual(
            resultado.classificacoes,
            frozenset({ClassificacaoAssociacao.INTERESSE}),
        )
        self.assertEqual(
            self.repositorio_associacao.associacoes_atualizadas, [resultado]
        )
        self.assertEqual(self.repositorio_associacao.associacoes_salvas, [])

    async def test_remocao_idempotente_nao_solicita_atualizacao(self) -> None:
        """Não grava quando a classificação a remover já está ausente.

        O teste remove candidatura de associação com somente interesse e
        confirma ausência de chamada de escrita. Ele existe para suportar
        repetição segura da operação.
        """
        entrada = AlterarClassificacaoAssociacaoCurriculoVagaEntrada(
            self.curriculo.usuario_id,
            self.curriculo.id,
            self.vaga_id,
            ClassificacaoAssociacao.CANDIDATURA,
        )

        await RemoverClassificacaoAssociacaoCurriculoVaga(
            self.repositorio_curriculo, self.repositorio_associacao
        ).executar(entrada)

        self.assertEqual(self.repositorio_associacao.associacoes_atualizadas, [])

    async def test_curriculo_alheio_nao_consulta_associacao(self) -> None:
        """Confirma ownership antes de consultar a associação.

        O teste usa identidade diferente do proprietário e observa a exceção e
        ausência de consultas ou escritas de associação. Ele existe para evitar
        enumeração ou alteração cruzada entre estudantes.
        """
        entrada = AlterarClassificacaoAssociacaoCurriculoVagaEntrada(
            UsuarioId(uuid4()),
            self.curriculo.id,
            self.vaga_id,
            ClassificacaoAssociacao.COMPATIBILIDADE,
        )

        with self.assertRaises(CurriculoNaoEncontrado):
            await AdicionarClassificacaoAssociacaoCurriculoVaga(
                self.repositorio_curriculo, self.repositorio_associacao
            ).executar(entrada)

        self.assertEqual(self.repositorio_associacao.associacoes_carregadas, [])
        self.assertEqual(self.repositorio_associacao.associacoes_atualizadas, [])

    async def test_associacao_ausente_apos_ownership_gera_erro_sem_criar(self) -> None:
        """Retorna erro específico sem criar associação quando o par não existe.

        O teste fornece currículo próprio, mas nenhum agregado no repository.
        Ele existe para impedir que atualização seja convertida em criação.
        """
        self.repositorio_associacao._associacoes.clear()

        with self.assertRaises(AssociacaoCurriculoVagaNaoEncontrada):
            await AdicionarClassificacaoAssociacaoCurriculoVaga(
                self.repositorio_curriculo, self.repositorio_associacao
            ).executar(self.entrada)

        self.assertEqual(self.repositorio_associacao.associacoes_atualizadas, [])
        self.assertEqual(self.repositorio_associacao.associacoes_salvas, [])

    async def test_regra_de_dominio_nao_persiste_remocao_invalida(self) -> None:
        """Propaga violação ao remover última classificação sem escrever.

        O teste solicita a remoção do único interesse, espera falha do Domain e
        confirma que o port de atualização não foi chamado. Ele existe para
        garantir que erros de negócio não virem estados persistidos.
        """
        entrada = AlterarClassificacaoAssociacaoCurriculoVagaEntrada(
            self.curriculo.usuario_id,
            self.curriculo.id,
            self.vaga_id,
            ClassificacaoAssociacao.INTERESSE,
        )

        with self.assertRaises(RegraDeDominioViolada):
            await RemoverClassificacaoAssociacaoCurriculoVaga(
                self.repositorio_curriculo, self.repositorio_associacao
            ).executar(entrada)

        self.assertEqual(self.repositorio_associacao.associacoes_atualizadas, [])


class CriarAssociacaoCurriculoVagaCasosAdicionaisTestCase(
    unittest.IsolatedAsyncioTestCase
):
    """Completa a cobertura do fluxo de criação existente.

    Os cenários mantêm a preparação local original e protegem ownership,
    duplicidade e propagação de falhas. A classe existe para separar esses
    testes dos novos casos de atualização.
    """

    async def test_rejeita_curriculo_de_outro_usuario_sem_consultar_ou_salvar_associacao(
        self,
    ) -> None:
        """Oculta propriedade alheia como currículo não encontrado.

        O teste autentica um ator diferente do proprietário configurado e
        observa que nenhuma consulta de duplicidade ou gravação ocorre. Ele
        existe para proteger o ownership antes da criação.
        """
        curriculo = _criar_curriculo()
        entrada = CriarAssociacaoCurriculoVagaEntrada(
            usuario_id=UsuarioId(uuid4()),
            curriculo_id=curriculo.id,
            vaga_id=VagaId("vaga-teste"),
            classificacoes=(ClassificacaoAssociacao.INTERESSE,),
        )
        repositorio_associacao = RepositorioAssociacaoSpy()

        with self.assertRaises(CurriculoNaoEncontrado):
            await CriarAssociacaoCurriculoVaga(
                RepositorioCurriculoStub({curriculo.id: curriculo}),
                repositorio_associacao,
            ).executar(entrada)

        self.assertEqual(repositorio_associacao.consultas, [])
        self.assertEqual(repositorio_associacao.associacoes_salvas, [])

    async def test_rejeita_associacao_duplicada_sem_solicitar_salvamento(self) -> None:
        """Confirma que o par existente é rejeitado sem atualizar classificações.

        O spy informa o par como existente; o teste observa a exceção específica
        e nenhum agregado enviado para salvar. Ele existe para impedir que
        criação duplicada funcione como upsert.
        """
        curriculo = _criar_curriculo()
        entrada = _criar_entrada(curriculo)
        par = (curriculo.id, entrada.vaga_id)
        repositorio_associacao = RepositorioAssociacaoSpy({par})

        with self.assertRaises(AssociacaoCurriculoVagaJaExiste):
            await CriarAssociacaoCurriculoVaga(
                RepositorioCurriculoStub({curriculo.id: curriculo}),
                repositorio_associacao,
            ).executar(entrada)

        self.assertEqual(repositorio_associacao.consultas, [par])
        self.assertEqual(repositorio_associacao.associacoes_salvas, [])

    async def test_delega_validacao_de_classificacao_vazia_ao_domain(self) -> None:
        """Confirma que classificação vazia falha antes de solicitar salvamento.

        O caso de uso passa a coleção ao agregado existente, cuja invariante
        rejeita a entrada. Ele existe para garantir que Application não repita a
        validação nem persista uma associação inválida.
        """
        curriculo = _criar_curriculo()
        entrada = _criar_entrada(curriculo, ())
        repositorio_associacao = RepositorioAssociacaoSpy()

        with self.assertRaises(RegraDeDominioViolada):
            await CriarAssociacaoCurriculoVaga(
                RepositorioCurriculoStub({curriculo.id: curriculo}),
                repositorio_associacao,
            ).executar(entrada)

        self.assertEqual(repositorio_associacao.associacoes_salvas, [])

    async def test_candidatura_reutiliza_normalizacao_do_domain_e_preserva_classificacoes(
        self,
    ) -> None:
        """Confirma interesse automático sem perder compatibilidade.

        O teste passa candidatura e compatibilidade à entrada e examina o
        agregado entregue ao port. Ele existe para garantir que Application
        delegue a normalização somente ao Domain já aprovado.
        """
        curriculo = _criar_curriculo()
        classificacoes = (
            ClassificacaoAssociacao.CANDIDATURA,
            ClassificacaoAssociacao.COMPATIBILIDADE,
        )
        entrada = _criar_entrada(curriculo, classificacoes)
        repositorio_associacao = RepositorioAssociacaoSpy()

        await CriarAssociacaoCurriculoVaga(
            RepositorioCurriculoStub({curriculo.id: curriculo}), repositorio_associacao
        ).executar(entrada)

        self.assertEqual(
            repositorio_associacao.associacoes_salvas[0].classificacoes,
            frozenset(
                {
                    ClassificacaoAssociacao.CANDIDATURA,
                    ClassificacaoAssociacao.COMPATIBILIDADE,
                    ClassificacaoAssociacao.INTERESSE,
                }
            ),
        )

    async def test_propaga_falha_do_port_de_duplicidade_sem_salvar(self) -> None:
        """Confirma que falhas da porta não se transformam em sucesso.

        O spy é configurado para falhar na consulta preventiva; o teste verifica
        a mesma exceção e a ausência de salvamento. Ele existe para manter falhas
        externas explícitas na Application.
        """

        class RepositorioQueFalha(RepositorioAssociacaoSpy):
            """Produz uma falha controlada na consulta do par.

            A implementação substitui somente o método consultado no cenário.
            Ela existe para confirmar que o caso de uso não oculta erro de I/O.
            """

            async def existe_por_par(
                self, curriculo_id: CurriculoId, vaga_id: VagaId
            ) -> bool:
                """Lança a falha de teste em vez de responder sobre o par.

                O método evita qualquer resultado de sucesso para a consulta.
                Ele existe para tornar a propagação de falha observável.
                """
                raise RuntimeError("falha simulada do repository")

        curriculo = _criar_curriculo()
        repositorio_associacao = RepositorioQueFalha()

        with self.assertRaisesRegex(RuntimeError, "falha simulada"):
            await CriarAssociacaoCurriculoVaga(
                RepositorioCurriculoStub({curriculo.id: curriculo}),
                repositorio_associacao,
            ).executar(_criar_entrada(curriculo))

        self.assertEqual(repositorio_associacao.associacoes_salvas, [])

    async def test_propaga_falha_ao_salvar_sem_devolver_sucesso(self) -> None:
        """Confirma que uma falha de salvamento interrompe a criação.

        O repository simulado registra a operação e falha; o teste exige que a
        exceção alcance o chamador. Ele existe para impedir sucesso fictício em
        falha de persistência.
        """

        class RepositorioQueFalha(RepositorioAssociacaoSpy):
            """Produz uma falha controlada durante o salvamento.

            A implementação substitui o método de escrita e não encobre a
            exceção. Ela existe para validar o resultado observável do caso.
            """

            async def salvar(self, associacao: AssociacaoCurriculoVaga) -> None:
                """Indica que o adapter não conseguiu completar o pedido.

                O método falha deliberadamente antes de confirmar a escrita. Ele
                existe para testar a propagação sem infraestrutura real.
                """
                raise RuntimeError("falha simulada ao salvar")

        curriculo = _criar_curriculo()
        repositorio_associacao = RepositorioQueFalha()

        with self.assertRaisesRegex(RuntimeError, "falha simulada ao salvar"):
            await CriarAssociacaoCurriculoVaga(
                RepositorioCurriculoStub({curriculo.id: curriculo}),
                repositorio_associacao,
            ).executar(_criar_entrada(curriculo))
