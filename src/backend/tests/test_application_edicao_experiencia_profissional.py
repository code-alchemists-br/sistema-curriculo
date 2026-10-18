"""Testa a orquestração do caso de uso de edição de experiência profissional.

Os cenários usam um repositório em memória que só devolve experiências cuja
identidade e proprietário coincidem, mantendo o teste limitado ao núcleo da
aplicação. Eles existem para verificar a validação de proprietário e que apenas
estados válidos são encaminhados à atualização.
"""

from datetime import date
from unittest import IsolatedAsyncioTestCase
from uuid import UUID

from backend.application import (
    EditarExperienciaProfissional,
    EditarExperienciaProfissionalEntrada,
    ExperienciaProfissionalNaoEncontrada,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import (
    ExperienciaProfissionalId,
    Periodo,
    UsuarioId,
)

DONO = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))
OUTRO_USUARIO = UsuarioId(UUID("00000000-0000-0000-0000-000000000002"))
ID_EXPERIENCIA = ExperienciaProfissionalId(UUID("00000000-0000-0000-0000-0000000000e1"))


class RepositorioExperienciaEmMemoria:
    """Substitui a porta de experiência por estado controlado pelo teste.

    O double indexa experiências por identidade, só as devolve quando o
    proprietário coincide e registra as consultas e atualizações recebidas,
    podendo simular uma atualização sem efeito. Ele existe para observar a
    orquestração do caso de uso sem ORM, banco ou adapter produtivo.
    """

    def __init__(
        self,
        experiencias: list[ExperienciaProfissional] | None = None,
        atualizacao_afeta_linha: bool = True,
    ) -> None:
        """Prepara o índice em memória e os históricos de chamadas.

        O construtor copia as experiências fornecidas por identidade e guarda
        o resultado configurado para ``atualizar``. Ele existe para que cada
        cenário controle presença, propriedade e concorrência.
        """
        self._por_id = {item.id: item for item in (experiencias or [])}
        self._atualizacao_afeta_linha = atualizacao_afeta_linha
        self.consultas: list[tuple[ExperienciaProfissionalId, UsuarioId]] = []
        self.atualizadas: list[ExperienciaProfissional] = []

    async def salvar(self, experiencia: ExperienciaProfissional) -> None:
        """Rejeita salvamento, que não faz parte do fluxo de edição.

        O método falha imediatamente se for chamado. Ele existe para tornar
        visível qualquer tentativa indevida de criar registro durante a edição.
        """
        raise AssertionError("A edição não deve salvar nova experiência.")

    async def obter_por_id_e_usuario(
        self, experiencia_id: ExperienciaProfissionalId, usuario_id: UsuarioId
    ) -> ExperienciaProfissional | None:
        """Registra a consulta e devolve a experiência apenas ao proprietário.

        O método consulta somente o dicionário do teste e devolve ``None`` para
        ID desconhecido ou dono diferente. Ele existe para reproduzir o contrato
        da porta que oculta experiências alheias.
        """
        self.consultas.append((experiencia_id, usuario_id))
        experiencia = self._por_id.get(experiencia_id)
        if experiencia is None or experiencia.usuario_id != usuario_id:
            return None
        return experiencia

    async def atualizar(self, experiencia: ExperienciaProfissional) -> bool:
        """Registra a experiência recebida e devolve o efeito configurado.

        O método não persiste nada e apenas acumula a entidade. Ele existe para
        tornar observável o que o caso de uso pediu para atualizar e para
        simular uma atualização concorrente sem linhas afetadas.
        """
        self.atualizadas.append(experiencia)
        return self._atualizacao_afeta_linha


def _experiencia(usuario_id: UsuarioId = DONO) -> ExperienciaProfissional:
    """Cria a experiência original com identidade e dados determinísticos.

    A função permite escolher o proprietário e fixa os demais campos. Ela
    existe para reduzir repetição entre cenários de dono e de terceiro.
    """
    return ExperienciaProfissional(
        id=ID_EXPERIENCIA,
        usuario_id=usuario_id,
        empresa="Instituto Exemplo",
        cargo="Estagiária",
        descricao="Construiu integrações internas.",
        periodo=Periodo(date(2022, 1, 1), date(2023, 6, 1)),
    )


def _entrada(
    usuario_id: UsuarioId = DONO,
    experiencia_id: ExperienciaProfissionalId = ID_EXPERIENCIA,
    empresa: str = "Nova Empresa",
) -> EditarExperienciaProfissionalEntrada:
    """Cria a entrada de edição com os novos dados padrão do cenário.

    A função permite variar solicitante, experiência e empresa. Ela existe para
    manter cada teste focado na decisão observada.
    """
    return EditarExperienciaProfissionalEntrada(
        usuario_id=usuario_id,
        experiencia_id=experiencia_id,
        empresa=empresa,
        cargo="Desenvolvedora",
        descricao="Mantém APIs em produção.",
        periodo=Periodo(date(2023, 7, 1)),
    )


class EditarExperienciaProfissionalTestCase(IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``EditarExperienciaProfissional``.

    A classe substitui o repositório por estado em memória e observa resultado,
    consultas e atualizações. Ela existe para testar a validação de proprietário
    e a persistência apenas de estados válidos, sem infraestrutura.
    """

    async def test_edita_experiencia_propria_e_devolve_novo_estado(self) -> None:
        """Atualiza a experiência do solicitante e devolve a versão editada.

        O cenário usa o dono da experiência e confere a consulta conjunta, a
        entidade enviada a ``atualizar`` e o retorno. Ele existe para proteger o
        caminho de sucesso da edição.
        """
        repositorio = RepositorioExperienciaEmMemoria([_experiencia()])

        resultado = await EditarExperienciaProfissional(repositorio).executar(_entrada())

        self.assertEqual(repositorio.consultas, [(ID_EXPERIENCIA, DONO)])
        self.assertEqual(repositorio.atualizadas, [resultado])
        self.assertEqual((resultado.id, resultado.usuario_id), (ID_EXPERIENCIA, DONO))
        self.assertEqual(
            (resultado.empresa, resultado.cargo, resultado.descricao),
            ("Nova Empresa", "Desenvolvedora", "Mantém APIs em produção."),
        )
        self.assertEqual(resultado.periodo, Periodo(date(2023, 7, 1)))

    async def test_experiencia_de_outro_estudante_e_tratada_como_nao_encontrada(
        self,
    ) -> None:
        """Rejeita edição de experiência alheia sem atualizar nada.

        O repositório guarda a experiência de outro usuário e o dono da
        requisição tenta editá-la pelo mesmo ID. O teste existe para garantir
        que um estudante não altere nem descubra dados de terceiros.
        """
        repositorio = RepositorioExperienciaEmMemoria([_experiencia(OUTRO_USUARIO)])

        with self.assertRaises(ExperienciaProfissionalNaoEncontrada):
            await EditarExperienciaProfissional(repositorio).executar(_entrada())

        self.assertEqual(repositorio.consultas, [(ID_EXPERIENCIA, DONO)])
        self.assertEqual(repositorio.atualizadas, [])

    async def test_experiencia_inexistente_e_tratada_como_nao_encontrada(self) -> None:
        """Rejeita edição de ID desconhecido com a mesma falha uniforme.

        O repositório está vazio e o caso de uso não deve chamar ``atualizar``.
        O teste existe para que ausência e propriedade alheia sejam
        indistinguíveis para o cliente.
        """
        repositorio = RepositorioExperienciaEmMemoria()

        with self.assertRaises(ExperienciaProfissionalNaoEncontrada):
            await EditarExperienciaProfissional(repositorio).executar(_entrada())

        self.assertEqual(repositorio.atualizadas, [])

    async def test_atualizacao_sem_linha_afetada_vira_nao_encontrada(self) -> None:
        """Trata atualização sem efeito como experiência não encontrada.

        A busca encontra a experiência, mas o repositório informa que nenhuma
        linha foi alterada, como numa remoção concorrente. O teste existe para
        não devolver ao cliente um estado que não foi persistido.
        """
        repositorio = RepositorioExperienciaEmMemoria(
            [_experiencia()], atualizacao_afeta_linha=False
        )

        with self.assertRaises(ExperienciaProfissionalNaoEncontrada):
            await EditarExperienciaProfissional(repositorio).executar(_entrada())

        self.assertEqual(len(repositorio.atualizadas), 1)

    async def test_dados_invalidos_violam_regra_sem_atualizar(self) -> None:
        """Propaga a regra de domínio e não solicita atualização.

        A edição tenta deixar a empresa em branco para uma experiência própria.
        O teste existe para garantir que apenas estados válidos cheguem à
        persistência.
        """
        repositorio = RepositorioExperienciaEmMemoria([_experiencia()])

        with self.assertRaises(RegraDeDominioViolada):
            await EditarExperienciaProfissional(repositorio).executar(
                _entrada(empresa="   ")
            )

        self.assertEqual(repositorio.atualizadas, [])
