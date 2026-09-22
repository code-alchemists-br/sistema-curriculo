"""Testa a orquestração do caso de uso de cadastro de projetos acadêmicos.

Os cenários usam doubles determinísticos para identidade e persistência e se
limitam ao núcleo da Application. Eles existem para verificar que somente
entidades válidas são encaminhadas ao repositório.
"""

from unittest import IsolatedAsyncioTestCase
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
from backend.application.cadastro_projeto_academico import (
    CadastrarProjetoAcademico,
    CadastrarProjetoAcademicoEntrada,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import ProjetoAcademico
from backend.domain.value_objects import ProjetoAcademicoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
class RepositorioProjetoAcademicoSpy:
    """Registra em memória os projetos entregues pela Application.

    O double implementa a porta assíncrona acumulando argumentos, sem banco.
    Ele existe para tornar observável o efeito do caso de uso unitariamente.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    def __init__(self) -> None:
        """Inicializa o registro vazio de chamadas de persistência.

        O construtor cria uma lista local que receberá entidades salvas. Ele
        existe para permitir que o teste observe persistência e sua ausência.
        """
        self.projetos_salvos: list[ProjetoAcademico] = []

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    async def salvar(self, projeto: ProjetoAcademico) -> None:
        """Armazena localmente o projeto recebido pelo contrato da porta.

        O método acrescenta a entidade à lista e mantém a assinatura assíncrona.
        Ele existe para substituir infraestrutura no teste do caso de uso.
        """
        self.projetos_salvos.append(projeto)


# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
class GeradorProjetoAcademicoIdStub:
    """Entrega um identificador de projeto previamente definido.

    O stub devolve sempre o mesmo value object e elimina aleatoriedade. Ele
    existe para permitir asserções determinísticas sobre a entidade criada.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    def __init__(self, identificador: ProjetoAcademicoId) -> None:
        """Recebe o identificador que devolverá nas chamadas seguintes.

        O construtor conserva o value object do cenário sem gerar UUIDs. Ele
        existe para controlar a identidade atribuída em cada teste.
        """
        self._identificador = identificador

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    def gerar(self) -> ProjetoAcademicoId:
        """Devolve o identificador determinístico configurado no double.

        O método implementa a porta retornando o mesmo valor a cada chamada.
        Ele existe para isolar o caso de uso da estratégia concreta de UUID.
        """
        return self._identificador


# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
class CadastrarProjetoAcademicoTestCase(IsolatedAsyncioTestCase):
    """Verifica efeitos e falhas do cadastro com doubles locais.

    A suíte compõe o caso de uso com spy e stub, exercitando a orquestração e a
    invariante de domínio sem adapters. Ela existe para proteger o fluxo interno.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    async def test_cria_e_salva_projeto_com_identidade_gerada(self) -> None:
        """Persiste e devolve o projeto válido com a identidade do stub.

        O cenário executa o cadastro completo e compara o retorno com o spy.
        Ele existe para validar colaboração entre geração, domínio e porta.
        """
        repositorio = RepositorioProjetoAcademicoSpy()
        identificador = ProjetoAcademicoId(
            UUID("40000000-0000-0000-0000-000000000001")
        )
        caso_de_uso = CadastrarProjetoAcademico(
            repositorio=repositorio,
            gerador_id=GeradorProjetoAcademicoIdStub(identificador),
        )
        entrada = self._criar_entrada()

        projeto = await caso_de_uso.executar(entrada)

        self.assertEqual(projeto.id, identificador)
        self.assertEqual(projeto.usuario_id, entrada.usuario_id)
        self.assertEqual(repositorio.projetos_salvos, [projeto])

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    async def test_nao_salva_projeto_quando_texto_obrigatorio_eh_invalido(
        self,
    ) -> None:
        """Interrompe o fluxo antes da persistência quando a entidade é inválida.

        O cenário fornece título em branco e observa a regra antes de consultar
        o spy. Ele existe para assegurar que a porta não receba item incompleto.
        """
        repositorio = RepositorioProjetoAcademicoSpy()
        caso_de_uso = CadastrarProjetoAcademico(
            repositorio=repositorio,
            gerador_id=GeradorProjetoAcademicoIdStub(
                ProjetoAcademicoId(UUID("40000000-0000-0000-0000-000000000002"))
            ),
        )

        with self.assertRaises(RegraDeDominioViolada):
            await caso_de_uso.executar(self._criar_entrada(titulo="  "))

        self.assertEqual(repositorio.projetos_salvos, [])

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    def _criar_entrada(
        self, titulo: str = "Sistema Currículo"
    ) -> CadastrarProjetoAcademicoEntrada:
        """Produz entrada válida e determinística para cenários assíncronos.

        O auxiliar fixa os dados do formulário e permite variar o título. Ele
        existe para manter os testes focados na decisão de orquestração.
        """
        return CadastrarProjetoAcademicoEntrada(
            usuario_id=UsuarioId(UUID("40000000-0000-0000-0000-000000000003")),
            titulo=titulo,
            descricao="Organiza informações acadêmicas.",
            tecnologias="Python, FastAPI",
        )
