"""Integra casos reais, adapters e SQLite migrado com critérios inferidos de RF12.

O prefixo test_ difere do nome sugerido na análise por decisão explícita do
usuário: discover deve coletar e ignorar com motivo se faltar driver/grafo.
P01–P03 e N01–N06/N08 verificam SQL bruto antes de reconstruir os agregados;
N07 foi deliberadamente omitido pelo usuário por pertencer ao nível unitário.

Não é integração HTTP: não prova middleware/handler de associação, main.py,
composição de produção, cadeia original do Alembic sob experimento temporário,
PostgreSQL/lock FOR UPDATE, concorrência, indisponibilidade de banco, exclusão
integral, política de interesse/consentimento/retenção ou existência/formato da
vaga. O card não tem aceite fornecido; seu aceite oficial não é verificável.
"""

# Proveniência: decision-analysis prompts/backend/20261024-171508-integracao-associacao-candidatura-interesse-v001.md#v001

from unittest import IsolatedAsyncioTestCase, skipUnless

from backend.application.associacao_curriculo_vaga import (
    AlterarClassificacaoAssociacaoCurriculoVagaEntrada,
    AssociacaoCurriculoVagaJaExiste,
    AssociacaoCurriculoVagaNaoEncontrada,
    CriarAssociacaoCurriculoVagaEntrada,
)
from backend.application.consulta_associacao_curriculo_vaga import (
    ListarAssociacoesCurriculoVaga,
    ListarAssociacoesCurriculoVagaEntrada,
)
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain.associacao_curriculo_vaga import ClassificacaoAssociacao as Classe
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.value_objects import CurriculoId, UsuarioId, VagaId
from backend.infrastructure.persistence.sqlalchemy.repositorio_associacao_curriculo_vaga import (
    RepositorioAssociacaoCurriculoVagaSqlAlchemy,
)
from backend.tests.fixtures.associacoes_candidatura_integracao import (
    A1,
    A2,
    AIOSQLITE_DISPONIVEL,
    AUSENTE,
    B1,
    MOTIVO_SEM_AIOSQLITE,
    VAGA01,
    VAGA02,
    BancoAssociacoes,
    OperacaoObservada,
    verificar_grafo,
)
from backend.tests.fixtures.credenciais_sessao import USUARIO_A, USUARIO_B

I, C, K = Classe.INTERESSE, Classe.CANDIDATURA, Classe.COMPATIBILIDADE


@skipUnless(AIOSQLITE_DISPONIVEL, MOTIVO_SEM_AIOSQLITE)
class AssociacaoCandidaturaInteresseIntegracaoTestCase(IsolatedAsyncioTestCase):
    """Verifica fluxos e recusas em bancos migrados exclusivos de cada variante.

    Usa controles positivos, spies delegantes e releitura em sessões distintas
    para provar colaboração real e distinguir skip de comportamento aprovado.
    """

    async def asyncSetUp(self) -> None:
        """Valida o grafo por AST antes de instanciar qualquer banco de cenário.

        Converte somente defeitos preexistentes conhecidos em skip, permitindo
        identificar bloqueio ambiental sem ocultar falhas de SQL ou asserções.
        """
        verificar_grafo()

    async def _banco(self, *, incluir_ausente=False):
        """Prepara um arquivo SQLite próprio e registra cleanup antes de migrar.

        Revalida o grafo e usa a fixture compartilhada para contas, evitando
        recursos abandonados quando preparação, skip ou variante falhar.
        """
        verificar_grafo()
        banco = BancoAssociacoes()
        self.addAsyncCleanup(banco.fechar)
        await banco.preparar(USUARIO_A, USUARIO_B, incluir_ausente=incluir_ausente)
        return banco

    async def _conferir(self, banco, esperado):
        """Compara linhas brutas antes de listar em outra sessão por proprietário.

        Exige raízes e classificações exatas, sem normalização intermediária,
        para detectar persistência incompleta e efeitos em outro currículo.
        """
        snapshot = await banco.snapshot()
        self.assertEqual(set(snapshot["raizes"]), set(esperado))
        self.assertEqual(set(snapshot["classes"]), {
            (curriculo, vaga, classe.value)
            for (curriculo, vaga), classes in esperado.items() for classe in classes
        })
        donos = {linha[0]: linha[1] for linha in snapshot["curriculos"]}
        for usuario in (USUARIO_A, USUARIO_B):
            async with banco.base.sessoes() as sessao:
                pagina = await ListarAssociacoesCurriculoVaga(
                    RepositorioAssociacaoCurriculoVagaSqlAlchemy(sessao),
                ).executar(ListarAssociacoesCurriculoVagaEntrada(UsuarioId(usuario), 0, 100))
            self.assertEqual({
                (item.curriculo_id.valor, item.vaga_id.valor): set(item.classificacoes)
                for item in pagina
            }, {par: set(classes) for par, classes in esperado.items() if donos[par[0]] == usuario})
        return snapshot

    async def _positiva(self, banco, acao, ator, curriculo, vaga, classes, esperado, *, escreve=True):
        """Executa um caso real, confirma a transação e relê estado independente.

        Observa métodos delegantes e exige ausência de escrita nos no-ops, para
        que cada controle positivo também comprove persistência e idempotência.
        """
        anterior = await banco.snapshot()
        async with banco.base.sessoes() as sessao:
            observada = OperacaoObservada(sessao)
            try:
                entrada = self._entrada(acao, ator, curriculo, vaga, classes)
                resultado = await observada.casos[acao](entrada)
                observada.casos[acao].assert_awaited_once_with(entrada)
                metodo = "salvar" if acao == "criar" else "atualizar_classificacoes"
                self.assertEqual(observada.spies[metodo].await_count, int(escreve))
                outro = "atualizar_classificacoes" if acao == "criar" else "salvar"
                observada.spies[outro].assert_not_awaited()
                if not escreve:
                    self._sem_pendencias(sessao)
                await sessao.commit()
            finally:
                observada.fechar()
        posterior = await self._conferir(banco, esperado)
        self.assertEqual(anterior["curriculos"], posterior["curriculos"])
        self.assertEqual(set(resultado.classificacoes), set(esperado[(curriculo, vaga)]))
        if not escreve:
            self.assertEqual(anterior, posterior)

    def _entrada(self, acao, ator, curriculo, vaga, classes):
        """Converte os dados sintéticos em comandos internos tipados do caso real.

        Usa a identidade já autenticada e preserva classificações recebidas,
        permitindo exercitar a validação de domínio sem simular transporte.
        """
        if acao == "criar":
            return CriarAssociacaoCurriculoVagaEntrada(ator, CurriculoId(curriculo), VagaId(vaga), tuple(classes))
        return AlterarClassificacaoAssociacaoCurriculoVagaEntrada(ator, CurriculoId(curriculo), VagaId(vaga), classes)

    def _sem_pendencias(self, sessao):
        """Exige ausência de entidades pendentes antes de encerrar a transação.

        Inspeciona new, dirty e deleted sem rollback, para impedir que uma
        recusa seja considerada segura só porque o teste descartou a escrita.
        """
        self.assertFalse(sessao.new)
        self.assertFalse(sessao.dirty)
        self.assertFalse(sessao.deleted)

    async def _recusar(self, banco, acao, ator, curriculo, vaga, classes, erro, mensagem, *, ownership=False):
        """Executa recusa após controles e compara o estado bruto global relido.

        Exige caso chamado, escrita não chamada e commit sem pendências, para
        detectar mutações indevidas inclusive se um adapter já tivesse flushado.
        """
        anterior = await banco.snapshot()
        async with banco.base.sessoes() as sessao:
            observada = OperacaoObservada(sessao)
            try:
                entrada = self._entrada(acao, ator, curriculo, vaga, classes)
                with self.assertRaises(erro) as capturada:
                    await observada.casos[acao](entrada)
                self.assertEqual(str(capturada.exception), mensagem)
                observada.casos[acao].assert_awaited_once_with(entrada)
                observada.spies["curriculo"].assert_awaited_once_with(CurriculoId(curriculo))
                for nome in ("salvar", "atualizar_classificacoes"):
                    observada.spies[nome].assert_not_awaited()
                if ownership:
                    observada.spies["existe_por_par"].assert_not_awaited()
                    observada.spies["obter_para_atualizacao"].assert_not_awaited()
                elif acao == "criar":
                    observada.spies["existe_por_par"].assert_awaited_once_with(CurriculoId(curriculo), VagaId(vaga))
                    observada.spies["obter_para_atualizacao"].assert_not_awaited()
                else:
                    observada.spies["existe_por_par"].assert_not_awaited()
                    observada.spies["obter_para_atualizacao"].assert_awaited_once_with(CurriculoId(curriculo), VagaId(vaga))
                self._sem_pendencias(sessao)
                await sessao.commit()
            finally:
                observada.fechar()
        self.assertEqual(anterior, await banco.snapshot())

    async def test_criacao_com_candidatura_persiste_interesse_e_isola_curriculo(self):
        """P01 persiste candidatura com interesse só no currículo escolhido.

        Autentica sessões reais antes da criação e da consulta durável e relê
        SQL/listagem, para provar RN03 sem alegar envio externo ou HTTP.
        """
        banco = await self._banco()
        ator = await banco.identidade(USUARIO_A)
        esperado = {(A1, VAGA01): {C, I}}
        await self._positiva(banco, "criar", ator, A1, VAGA01, (C,), esperado)
        anterior = await banco.snapshot()
        self.assertEqual(await banco.identidade(USUARIO_A), ator)
        self.assertEqual(anterior, await self._conferir(banco, esperado))

    async def test_adicao_remocao_e_repeticao_preservam_interesse(self):
        """P02 integra transições e no-ops sem perder o interesse derivado.

        Confirma e relê cada passo em sessões novas para verificar RN03/05/06
        e observar que repetições não pedem atualização ao repositório real.
        """
        banco = await self._banco()
        ator = await banco.identidade(USUARIO_A)
        await self._positiva(banco, "criar", ator, A1, VAGA01, (K,), {(A1, VAGA01): {K}})
        for acao, classe, estado, escreve in (
            ("adicionar", C, {K, C, I}, True),
            ("adicionar", C, {K, C, I}, False),
            ("remover", C, {K, I}, True),
            ("remover", C, {K, I}, False),
            ("adicionar", I, {K, I}, False),
            ("remover", K, {I}, True),
        ):
            await self._positiva(banco, acao, ator, A1, VAGA01, classe, {(A1, VAGA01): estado}, escreve=escreve)

    async def test_interesse_isolado_e_candidatura_com_compativel_sao_permitidos(self):
        """P03 comprova combinações válidas em dois pares sem efeito cruzado.

        Cria e relê cada par por SQL antes da listagem para verificar RF12 e
        impedir que interesse isolado seja tratado como recusa sem fundamento.
        """
        banco = await self._banco()
        ator = await banco.identidade(USUARIO_A)
        esperado = {(A1, VAGA01): {I}}
        await self._positiva(banco, "criar", ator, A1, VAGA01, (I,), esperado)
        esperado[(A2, VAGA02)] = {C, K, I}
        await self._positiva(banco, "criar", ator, A2, VAGA02, (C, K), esperado)

    async def test_criacao_duplicada_nao_muda_classificacoes(self):
        """N01 rejeita repetição do par após criação positiva no mesmo recurso.

        Tenta candidatura sobre interesse já persistido e relê o snapshot para
        provar que o conflito não atua como atualização implícita.
        """
        banco = await self._banco()
        ator = await banco.identidade(USUARIO_A)
        await self._positiva(banco, "criar", ator, A1, VAGA01, (I,), {(A1, VAGA01): {I}})
        await self._recusar(banco, "criar", ator, A1, VAGA01, (C,), AssociacaoCurriculoVagaJaExiste,
                            "Já existe uma associação para este currículo e esta vaga.")

    async def test_curriculo_alheio_nao_consulta_associacao(self):
        """N02 recusa A no currículo B após controle da mesma operação por B.

        Usa banco novo em cada variante e spies delegantes para demonstrar RN07
        antes de consultar associação, mantendo o estado global persistido.
        """
        for acao in ("criar", "adicionar", "remover"):
            with self.subTest(acao=acao):
                banco = await self._banco()
                b = await banco.identidade(USUARIO_B)
                await self._positiva(banco, "criar", b, B1, VAGA01, (I, K), {(B1, VAGA01): {I, K}})
                if acao == "criar":
                    vaga, classe = VAGA02, (C,)
                    esperado = {(B1, VAGA01): {I, K}, (B1, VAGA02): {I, C}}
                else:
                    vaga, classe = VAGA01, C if acao == "adicionar" else K
                    esperado = {(B1, VAGA01): {I, K, C} if acao == "adicionar" else {I}}
                await self._positiva(banco, acao, b, B1, vaga, classe, esperado)
                a = await banco.identidade(USUARIO_A)
                await self._recusar(banco, acao, a, B1, vaga, classe, CurriculoNaoEncontrado,
                                    "Versão de currículo não encontrada.", ownership=True)

    async def test_curriculo_inexistente_recusa_antes_da_associacao(self):
        """N03 compara operações com UUID 299 presente somente no controle.

        Usa bancos independentes com a única diferença de preparo documentada,
        para provar que ausência, não rota ou operação quebrada, causa a recusa.
        """
        for acao in ("criar", "adicionar", "remover"):
            with self.subTest(acao=acao):
                controle = await self._banco(incluir_ausente=True)
                ator = await controle.identidade(USUARIO_A)
                if acao != "criar":
                    await self._positiva(controle, "criar", ator, AUSENTE, VAGA01, (I, K), {(AUSENTE, VAGA01): {I, K}})
                classe = (C,) if acao == "criar" else C if acao == "adicionar" else K
                estado = {C, I} if acao == "criar" else {C, I, K} if acao == "adicionar" else {I}
                await self._positiva(controle, acao, ator, AUSENTE, VAGA01, classe, {(AUSENTE, VAGA01): estado})
                # Única diferença no seed: UUID 299 não existe neste banco.
                banco = await self._banco()
                ator = await banco.identidade(USUARIO_A)
                await self._recusar(banco, acao, ator, AUSENTE, VAGA01, classe, CurriculoNaoEncontrado,
                                    "Versão de currículo não encontrada.", ownership=True)

    async def test_alteracao_sem_associacao_nao_cria_par(self):
        """N04 recusa alteração sem raiz depois de controle no mesmo par.

        Compara bancos independentes para adição e remoção, comprovando que os
        casos existentes não criam associação como efeito da alteração.
        """
        for acao in ("adicionar", "remover"):
            with self.subTest(acao=acao):
                controle = await self._banco()
                ator = await controle.identidade(USUARIO_A)
                await self._positiva(controle, "criar", ator, A1, VAGA01, (I, K), {(A1, VAGA01): {I, K}})
                classe, estado = (C, {C, I, K}) if acao == "adicionar" else (K, {I})
                await self._positiva(controle, acao, ator, A1, VAGA01, classe, {(A1, VAGA01): estado})
                banco = await self._banco()
                ator = await banco.identidade(USUARIO_A)
                await self._recusar(banco, acao, ator, A1, VAGA01, classe, AssociacaoCurriculoVagaNaoEncontrada,
                                    "Associação currículo-vaga não encontrada.")

    async def test_remover_interesse_com_candidatura_preserva_todas_linhas(self):
        """N05 preserva interesse com candidatura ativa conforme RN06.

        Remove candidatura e interesse no controle com compatibilidade restante,
        para provar que só a dependência ativa impede a remoção negativa.
        """
        controle = await self._banco()
        ator = await controle.identidade(USUARIO_A)
        await self._positiva(controle, "criar", ator, A1, VAGA01, (C, K), {(A1, VAGA01): {C, I, K}})
        await self._positiva(controle, "remover", ator, A1, VAGA01, C, {(A1, VAGA01): {I, K}})
        await self._positiva(controle, "remover", ator, A1, VAGA01, I, {(A1, VAGA01): {K}})
        banco = await self._banco()
        ator = await banco.identidade(USUARIO_A)
        await self._positiva(banco, "criar", ator, A1, VAGA01, (C,), {(A1, VAGA01): {C, I}})
        await self._recusar(banco, "remover", ator, A1, VAGA01, I, RegraDeDominioViolada,
                            "Não é possível remover interesse enquanto houver candidatura.")

    async def test_remover_ultima_classificacao_preserva_raiz(self):
        """N06 recusa estado vazio para interesse ou compatibilidade isolados.

        Remove a mesma classe no controle com duas classificações e relê as
        linhas para provar RN06 sem confundir recusa com erro do repositório.
        """
        for classe in (I, K):
            with self.subTest(classificacao=classe.value):
                controle = await self._banco()
                ator = await controle.identidade(USUARIO_A)
                await self._positiva(controle, "criar", ator, A1, VAGA01, (I, K), {(A1, VAGA01): {I, K}})
                await self._positiva(controle, "remover", ator, A1, VAGA01, classe, {(A1, VAGA01): {I, K} - {classe}})
                banco = await self._banco()
                ator = await banco.identidade(USUARIO_A)
                await self._positiva(banco, "criar", ator, A1, VAGA01, (classe,), {(A1, VAGA01): {classe}})
                await self._recusar(banco, "remover", ator, A1, VAGA01, classe, RegraDeDominioViolada,
                                    "Associação currículo-vaga deve possuir ao menos uma classificação.")

    async def test_classificacao_vazia_ou_invalida_na_criacao_nao_persiste(self):
        """N08 recusa classificações inválidas ao integrar o caso com banco real.

        Usa controle equivalente com candidatura e spies de ownership/duplicidade
        antes da recusa do agregado, para comprovar que nada foi persistido.
        """
        for classes, mensagem in (
            ((), "Associação currículo-vaga deve possuir ao menos uma classificação."),
            (("candidatura",), "Associação currículo-vaga recebeu classificação não reconhecida."),
        ):
            with self.subTest(classificacoes=classes):
                controle = await self._banco()
                ator = await controle.identidade(USUARIO_A)
                await self._positiva(controle, "criar", ator, A1, VAGA01, (C,), {(A1, VAGA01): {C, I}})
                banco = await self._banco()
                ator = await banco.identidade(USUARIO_A)
                await self._recusar(banco, "criar", ator, A1, VAGA01, classes, RegraDeDominioViolada, mensagem)
