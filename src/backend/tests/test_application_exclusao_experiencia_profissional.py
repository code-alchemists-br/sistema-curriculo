"""Testa a orquestração do caso de uso de exclusão lógica de experiência.

Os cenários usam um repositório em memória que só devolve experiências cuja
identidade e proprietário coincidem e um relógio fixo, mantendo o teste
limitado ao núcleo da aplicação. Eles existem para verificar a validação de
proprietário, a idempotência e o tratamento de exclusão concorrente.
"""

from datetime import date, datetime, timezone
from unittest import IsolatedAsyncioTestCase
from uuid import UUID

from backend.application import (
    ExcluirExperienciaProfissional,
    ExcluirExperienciaProfissionalEntrada,
    ExperienciaProfissionalNaoEncontrada,
)
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import (
    ExperienciaProfissionalId,
    Periodo,
    UsuarioId,
)

DONO = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))
OUTRO_USUARIO = UsuarioId(UUID("00000000-0000-0000-0000-000000000002"))
ID_EXPERIENCIA = ExperienciaProfissionalId(UUID("00000000-0000-0000-0000-0000000000e1"))
AGORA = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
ANTES = datetime(2026, 10, 16, 8, 0, tzinfo=timezone.utc)


class RelogioFixo:
    """Substitui a porta de relógio por um instante fixo e conta as leituras.

    O double devolve sempre o mesmo ``datetime`` com fuso. Ele existe para
    tornar o instante de exclusão determinístico e observar quando é lido.
    """

    def __init__(self, instante: datetime) -> None:
        """Guarda o instante devolvido e zera o contador de leituras.

        O construtor não acessa o relógio do sistema. Ele existe para que cada
        teste controle o tempo aplicado à exclusão.
        """
        self._instante = instante
        self.leituras = 0

    def agora(self) -> datetime:
        """Devolve o instante configurado e registra a leitura.

        O método não depende do relógio real. Ele existe para provar que o
        caso de uso só consulta o tempo na primeira transição.
        """
        self.leituras += 1
        return self._instante


class RepositorioExperienciaEmMemoria:
    """Substitui a porta de experiência por estado controlado pelo teste.

    O double guarda experiências por identidade, só as devolve ao dono, marca a
    exclusão de forma condicional e pode simular uma exclusão concorrente feita
    por outra requisição. Ele existe para observar a orquestração sem ORM.
    """

    def __init__(
        self,
        experiencias: list[ExperienciaProfissional] | None = None,
        exclusao_concorrente: datetime | None = None,
    ) -> None:
        """Prepara o índice em memória e os históricos de chamadas.

        O construtor copia as experiências por identidade e, quando informado,
        guarda o instante de uma exclusão concorrente aplicada antes da
        marcação. Ele existe para que cada cenário controle o estado inicial.
        """
        self._por_id = {item.id: item for item in (experiencias or [])}
        self._exclusao_concorrente = exclusao_concorrente
        self.consultas = 0
        self.marcacoes: list[tuple[ExperienciaProfissionalId, UsuarioId, datetime]] = []

    async def salvar(self, experiencia: ExperienciaProfissional) -> None:
        """Rejeita salvamento, que não faz parte do fluxo de exclusão.

        O método falha imediatamente se for chamado. Ele existe para tornar
        visível qualquer tentativa indevida de criar registro.
        """
        raise AssertionError("A exclusão não deve salvar experiência.")

    async def obter_por_id_e_usuario(self, experiencia_id, usuario_id):
        """Rejeita a busca de ativas, que não faz parte do fluxo de exclusão.

        O método falha se for chamado. Ele existe para garantir que a exclusão
        use a busca que inclui experiências já excluídas.
        """
        raise AssertionError("A exclusão deve buscar incluindo excluídas.")

    async def atualizar(self, experiencia: ExperienciaProfissional) -> bool:
        """Rejeita atualização de dados, que não faz parte da exclusão.

        O método falha se for chamado. Ele existe para garantir que a exclusão
        altere somente o marcador por ``marcar_excluida``.
        """
        raise AssertionError("A exclusão não deve atualizar os dados.")

    async def obter_por_id_e_usuario_incluindo_excluidas(
        self, experiencia_id: ExperienciaProfissionalId, usuario_id: UsuarioId
    ) -> ExperienciaProfissional | None:
        """Devolve a experiência do dono, ativa ou excluída, e conta a consulta.

        O método devolve ``None`` para ID desconhecido ou dono diferente. Ele
        existe para reproduzir o contrato que oculta experiências alheias.
        """
        self.consultas += 1
        experiencia = self._por_id.get(experiencia_id)
        if experiencia is None or experiencia.usuario_id != usuario_id:
            return None
        return experiencia

    async def marcar_excluida(
        self,
        experiencia_id: ExperienciaProfissionalId,
        usuario_id: UsuarioId,
        deleted_at: datetime,
    ) -> bool:
        """Marca a experiência ativa do dono ou informa que nada mudou.

        Quando há exclusão concorrente configurada, ela é aplicada primeiro e
        a marcação não altera nada. O método existe para simular o UPDATE
        condicional do adapter.
        """
        self.marcacoes.append((experiencia_id, usuario_id, deleted_at))
        atual = self._por_id[experiencia_id]
        if self._exclusao_concorrente is not None:
            self._por_id[experiencia_id] = atual.excluir(self._exclusao_concorrente)
            return False
        if atual.excluida or atual.usuario_id != usuario_id:
            return False
        self._por_id[experiencia_id] = atual.excluir(deleted_at)
        return True


def _experiencia(
    usuario_id: UsuarioId = DONO, deleted_at: datetime | None = None
) -> ExperienciaProfissional:
    """Cria a experiência inicial com identidade e dados determinísticos.

    A função permite escolher o proprietário e o estado de exclusão. Ela existe
    para reduzir repetição entre os cenários.
    """
    return ExperienciaProfissional(
        id=ID_EXPERIENCIA,
        usuario_id=usuario_id,
        empresa="Instituto Exemplo",
        cargo="Estagiária",
        descricao="Construiu integrações internas.",
        periodo=Periodo(date(2022, 1, 1), date(2023, 6, 1)),
        deleted_at=deleted_at,
    )


def _entrada(usuario_id: UsuarioId = DONO) -> ExcluirExperienciaProfissionalEntrada:
    """Cria a entrada de exclusão para a experiência padrão do cenário.

    A função permite variar o solicitante. Ela existe para manter os testes
    focados na decisão observada.
    """
    return ExcluirExperienciaProfissionalEntrada(
        usuario_id=usuario_id, experiencia_id=ID_EXPERIENCIA
    )


class ExcluirExperienciaProfissionalTestCase(IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``ExcluirExperienciaProfissional``.

    A classe substitui repositório e relógio por doubles e observa resultado,
    marcações e leituras do relógio. Ela existe para testar propriedade,
    idempotência e concorrência sem infraestrutura.
    """

    async def test_exclui_experiencia_propria_com_instante_do_relogio(self) -> None:
        """Marca a experiência do solicitante com o instante da porta de tempo.

        O teste confere a marcação condicional enviada e a experiência
        devolvida já excluída. Ele existe para proteger o caminho de sucesso.
        """
        repositorio = RepositorioExperienciaEmMemoria([_experiencia()])
        relogio = RelogioFixo(AGORA)

        resultado = await ExcluirExperienciaProfissional(repositorio, relogio).executar(
            _entrada()
        )

        self.assertEqual(repositorio.marcacoes, [(ID_EXPERIENCIA, DONO, AGORA)])
        self.assertEqual(resultado.deleted_at, AGORA)
        self.assertEqual(relogio.leituras, 1)

    async def test_experiencia_de_outro_estudante_e_tratada_como_nao_encontrada(
        self,
    ) -> None:
        """Rejeita exclusão de experiência alheia sem marcar nada.

        O repositório guarda a experiência de outro usuário e o solicitante
        tenta excluí-la pelo mesmo ID. O teste existe para que um estudante não
        remova nem descubra dados de terceiros.
        """
        repositorio = RepositorioExperienciaEmMemoria([_experiencia(OUTRO_USUARIO)])
        relogio = RelogioFixo(AGORA)

        with self.assertRaises(ExperienciaProfissionalNaoEncontrada):
            await ExcluirExperienciaProfissional(repositorio, relogio).executar(_entrada())

        self.assertEqual(repositorio.marcacoes, [])
        self.assertEqual(relogio.leituras, 0)

    async def test_experiencia_inexistente_e_tratada_como_nao_encontrada(self) -> None:
        """Rejeita ID desconhecido com a mesma falha uniforme.

        O repositório está vazio e nenhuma marcação deve ocorrer. O teste
        existe para que ausência e propriedade alheia sejam indistinguíveis.
        """
        repositorio = RepositorioExperienciaEmMemoria()

        with self.assertRaises(ExperienciaProfissionalNaoEncontrada):
            await ExcluirExperienciaProfissional(
                repositorio, RelogioFixo(AGORA)
            ).executar(_entrada())

        self.assertEqual(repositorio.marcacoes, [])

    async def test_experiencia_ja_excluida_e_devolvida_sem_nova_marcacao(self) -> None:
        """Trata a repetição da exclusão como sucesso sem efeito.

        A experiência já está excluída com um instante anterior; o caso de uso
        a devolve como está, sem ler o relógio nem marcar de novo. O teste
        existe para tornar a exclusão idempotente.
        """
        repositorio = RepositorioExperienciaEmMemoria([_experiencia(deleted_at=ANTES)])
        relogio = RelogioFixo(AGORA)

        resultado = await ExcluirExperienciaProfissional(repositorio, relogio).executar(
            _entrada()
        )

        self.assertEqual(resultado.deleted_at, ANTES)
        self.assertEqual(repositorio.marcacoes, [])
        self.assertEqual(relogio.leituras, 0)

    async def test_exclusao_concorrente_relê_e_preserva_primeiro_instante(self) -> None:
        """Relê a experiência quando outra requisição a excluiu antes.

        A marcação não altera linha alguma porque uma exclusão concorrente com
        instante anterior chegou primeiro; o caso de uso relê e devolve esse
        estado. O teste existe para não sobrescrever o primeiro instante.
        """
        repositorio = RepositorioExperienciaEmMemoria(
            [_experiencia()], exclusao_concorrente=ANTES
        )

        resultado = await ExcluirExperienciaProfissional(
            repositorio, RelogioFixo(AGORA)
        ).executar(_entrada())

        self.assertEqual(resultado.deleted_at, ANTES)
        self.assertEqual(repositorio.consultas, 2)
