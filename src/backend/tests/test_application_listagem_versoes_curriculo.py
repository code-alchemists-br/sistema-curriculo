"""Testa unitariamente o caso de uso de listagem de versões de currículo."""

import unittest
from uuid import uuid4

from backend.application import (
    ListarVersoesCurriculo,
    ListarVersoesCurriculoEntrada,
)
from backend.domain import Curriculo, CurriculoId, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001


class RepositorioCurriculoSpy:
    """Substitui a porta de currículo, devolve versões fixas e registra o uso.

    O double devolve exatamente as versões configuradas, sem filtrar por dono,
    para simular um adapter que erra, e acumula consultas e tentativas de
    escrita. Ele existe para testar a orquestração assíncrona sem ORM, banco,
    rede ou adapter produtivo.
    """

    def __init__(self, curriculos: list[Curriculo] | None = None) -> None:
        """Guarda as versões a devolver e inicia os históricos vazios.

        O construtor copia a lista fornecida e prepara o registro de consultas e
        de escritas. Ele existe para controlar o que cada cenário observa.
        """
        self._curriculos = list(curriculos or [])
        self.consultas: list[UsuarioId] = []
        self.escritas: list[Curriculo] = []

    async def listar_por_usuario(self, usuario_id: UsuarioId) -> tuple[Curriculo, ...]:
        """Registra a consulta e devolve por coroutine as versões configuradas.

        O método não faz I/O nem filtra por proprietário. Ele existe para
        simular a leitura aguardável exigida pelo caso de uso.
        """
        self.consultas.append(usuario_id)
        return tuple(self._curriculos)

    async def atualizar(self, curriculo: Curriculo) -> None:
        """Registra por coroutine uma tentativa indevida de atualização.

        O método acumula o agregado sem persistir. Ele existe para tornar
        observável qualquer escrita que a listagem não deveria fazer.
        """
        self.escritas.append(curriculo)

    async def salvar(self, curriculo: Curriculo) -> None:
        """Registra por coroutine uma tentativa indevida de salvamento.

        O método acumula o agregado sem persistir. Ele existe para tornar
        observável qualquer escrita que a listagem não deveria fazer.
        """
        self.escritas.append(curriculo)


def _criar_curriculo(usuario_id: UsuarioId, titulo: str = "Estágio em TI") -> Curriculo:
    """Cria uma versão válida do usuário com o título informado.

    A função gera uma identidade nova a cada chamada e fixa layout e visibilidade
    com valores neutros. Ela existe para variar apenas o que cada cenário observa.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id,
        titulo_versao=titulo,
        layout="classico",
        is_public=False,
    )


class ListarVersoesCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``ListarVersoesCurriculo``.

    A classe substitui a porta de currículo por estado em memória e observa o
    resultado, a consulta e a ausência de escrita. Ela existe para testar a
    unidade Application sem adapter, framework ou infraestrutura.
    """

    async def test_lista_as_versoes_do_solicitante_consultando_o_repositorio_uma_vez(self) -> None:
        """Confirma o resultado, o tipo de retorno e a consulta pelo proprietário.

        O teste fornece duas versões do próprio usuário e compara os agregados
        devolvidos com o histórico de consultas. Ele existe para proteger o
        contrato básico da listagem.
        """
        usuario_id = UsuarioId(uuid4())
        primeira = _criar_curriculo(usuario_id, "Alfa")
        segunda = _criar_curriculo(usuario_id, "Beta")
        repositorio = RepositorioCurriculoSpy([segunda, primeira])

        resultado = await ListarVersoesCurriculo(repositorio).executar(ListarVersoesCurriculoEntrada(usuario_id))

        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)
        self.assertIs(resultado[0], primeira)
        self.assertIs(resultado[1], segunda)
        self.assertEqual(repositorio.consultas, [usuario_id])

    async def test_ordena_por_titulo_sem_diferenciar_maiusculas(self) -> None:
        """Confirma a ordem alfabética do título ignorando a caixa.

        O teste devolve os títulos fora de ordem e com caixas mistas e compara a
        sequência resultante. Ele existe para proteger a ordem que o cliente
        apresenta ao estudante.
        """
        usuario_id = UsuarioId(uuid4())
        versoes = [_criar_curriculo(usuario_id, titulo) for titulo in ("beta", "Carta", "Alfa")]
        repositorio = RepositorioCurriculoSpy(versoes)

        resultado = await ListarVersoesCurriculo(repositorio).executar(ListarVersoesCurriculoEntrada(usuario_id))

        self.assertEqual([versao.titulo_versao for versao in resultado], ["Alfa", "beta", "Carta"])

    async def test_mesma_selecao_em_ordens_diferentes_produz_a_mesma_lista(self) -> None:
        """Confirma que a ordem do repositório não altera o resultado.

        O teste usa quatro versões com o mesmo título, devolvidas em ordens
        opostas, e compara os resultados, o que depende do desempate por
        identificador. Ele existe para proteger o determinismo da listagem.
        """
        usuario_id = UsuarioId(uuid4())
        versoes = [_criar_curriculo(usuario_id, "Mesmo título") for _ in range(4)]

        direta = await ListarVersoesCurriculo(RepositorioCurriculoSpy(versoes)).executar(
            ListarVersoesCurriculoEntrada(usuario_id)
        )
        invertida = await ListarVersoesCurriculo(RepositorioCurriculoSpy(list(reversed(versoes)))).executar(
            ListarVersoesCurriculoEntrada(usuario_id)
        )

        self.assertEqual([versao.id for versao in direta], [versao.id for versao in invertida])
        self.assertEqual(
            [str(versao.id.valor) for versao in direta],
            sorted(str(versao.id.valor) for versao in versoes),
        )

    async def test_descarta_versao_de_outro_proprietario_devolvida_pelo_repositorio(self) -> None:
        """Confirma que uma versão alheia nunca aparece, mesmo vinda do adapter.

        O teste faz o double devolver uma versão do solicitante e outra de outro
        usuário e observa que só a primeira é listada. Ele existe para proteger a
        defesa em profundidade contra falha de filtro no adapter (RNF04).
        """
        usuario_id = UsuarioId(uuid4())
        propria = _criar_curriculo(usuario_id, "Minha")
        alheia = _criar_curriculo(UsuarioId(uuid4()), "Alheia")
        repositorio = RepositorioCurriculoSpy([alheia, propria])

        resultado = await ListarVersoesCurriculo(repositorio).executar(ListarVersoesCurriculoEntrada(usuario_id))

        self.assertEqual(len(resultado), 1)
        self.assertIs(resultado[0], propria)

    async def test_estudante_sem_versoes_recebe_tupla_vazia(self) -> None:
        """Confirma que a ausência de versões não é erro.

        O teste usa um repositório vazio e observa a tupla vazia. Ele existe para
        proteger o caso do estudante que ainda não criou nenhuma versão.
        """
        usuario_id = UsuarioId(uuid4())
        repositorio = RepositorioCurriculoSpy()

        resultado = await ListarVersoesCurriculo(repositorio).executar(ListarVersoesCurriculoEntrada(usuario_id))

        self.assertEqual(resultado, ())
        self.assertEqual(repositorio.consultas, [usuario_id])

    async def test_nao_solicita_nenhuma_escrita(self) -> None:
        """Confirma que listar não atualiza nem salva nenhuma versão.

        O teste executa uma listagem com versões e observa o histórico de
        escritas do double. Ele existe para proteger a natureza de consulta da
        operação.
        """
        usuario_id = UsuarioId(uuid4())
        repositorio = RepositorioCurriculoSpy([_criar_curriculo(usuario_id)])

        await ListarVersoesCurriculo(repositorio).executar(ListarVersoesCurriculoEntrada(usuario_id))

        self.assertEqual(repositorio.escritas, [])
