"""Testa a orquestração do caso de uso de cadastro profissional.

Os cenários usam doubles determinísticos para as portas de identidade e
persistência, mantendo o teste limitado ao núcleo da aplicação. Eles existem
para verificar que somente entidades válidas são encaminhadas ao repositório.
"""

# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from datetime import date
from unittest import IsolatedAsyncioTestCase
from uuid import UUID

from backend.application.cadastro_experiencia_profissional import (
    CadastrarExperienciaProfissional,
    CadastrarExperienciaProfissionalEntrada,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import (
    ExperienciaProfissionalId,
    Periodo,
    UsuarioId,
)


# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
class RepositorioExperienciaSpy:
    """Registra em memória as experiências entregues pela aplicação.

    O double implementa o contrato assíncrono de persistência acumulando os
    argumentos recebidos, sem acessar qualquer banco. Ele existe para tornar
    observável o efeito do caso de uso em testes unitários.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def __init__(self) -> None:
        """Inicializa o registro vazio de chamadas de persistência.

        O construtor cria uma lista local que receberá cada entidade salva pelo
        double durante o cenário. Ele existe para que os testes possam afirmar
        tanto a persistência quanto a ausência dela em falhas de domínio.
        """
        self.experiencias_salvas: list[ExperienciaProfissional] = []

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    async def salvar(self, experiencia: ExperienciaProfissional) -> None:
        """Armazena localmente a experiência recebida pelo contrato da porta.

        O método apenas acrescenta a entidade à lista em memória e preserva a
        assinatura assíncrona esperada pelo caso de uso. Ele existe para
        substituir a infraestrutura de persistência no teste unitário.
        """
        self.experiencias_salvas.append(experiencia)


# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
class GeradorExperienciaProfissionalIdStub:
    """Entrega um identificador de experiência previamente definido.

    O stub devolve sempre o mesmo value object, eliminando aleatoriedade da
    geração de identidade durante os testes. Ele existe para permitir asserções
    determinísticas sobre a entidade criada pelo caso de uso.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def __init__(self, identificador: ExperienciaProfissionalId) -> None:
        """Recebe o identificador que será devolvido nas chamadas subsequentes.

        O construtor conserva o value object fornecido pelo cenário, sem gerar
        UUIDs ou acessar serviços externos. Ele existe para controlar a
        identidade atribuída à experiência profissional em cada teste.
        """
        self._identificador = identificador

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def gerar(self) -> ExperienciaProfissionalId:
        """Devolve o identificador determinístico configurado para o double.

        O método implementa a porta de geração retornando o mesmo value object
        a cada invocação. Ele existe para isolar o caso de uso de estratégias
        concretas de criação de UUIDs.
        """
        return self._identificador


# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
class CadastrarExperienciaProfissionalTestCase(IsolatedAsyncioTestCase):
    """Verifica efeitos e falhas do cadastro profissional com doubles locais.

    A suíte compõe o caso de uso com spy e stub, executando apenas a regra de
    orquestração e as invariantes do domínio. Ela existe para proteger o fluxo
    sem exigir adaptadores, banco de dados ou transporte HTTP.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    async def test_cria_e_salva_experiencia_com_identidade_gerada(self) -> None:
        """Persiste a entidade válida recebida pelo caso de uso.

        O cenário executa o cadastro com dados completos e confere que o spy
        recebeu a mesma entidade devolvida, com a identidade do stub. Ele
        existe para validar a colaboração entre geração, domínio e persistência.
        """
        repositorio = RepositorioExperienciaSpy()
        identificador = ExperienciaProfissionalId(
            UUID("20000000-0000-0000-0000-000000000001")
        )
        caso_de_uso = CadastrarExperienciaProfissional(
            repositorio=repositorio,
            gerador_id=GeradorExperienciaProfissionalIdStub(identificador),
        )
        entrada = self._criar_entrada()

        experiencia = await caso_de_uso.executar(entrada)

        self.assertEqual(experiencia.id, identificador)
        self.assertEqual(experiencia.usuario_id, entrada.usuario_id)
        self.assertEqual(repositorio.experiencias_salvas, [experiencia])

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    async def test_nao_salva_experiencia_quando_texto_obrigatorio_eh_invalido(
        self,
    ) -> None:
        """Interrompe o fluxo antes da persistência quando a entidade é inválida.

        O cenário fornece uma empresa em branco e observa a exceção da regra de
        domínio antes de consultar o registro do spy. Ele existe para assegurar
        que a porta não receba entidades incompletas.
        """
        repositorio = RepositorioExperienciaSpy()
        caso_de_uso = CadastrarExperienciaProfissional(
            repositorio=repositorio,
            gerador_id=GeradorExperienciaProfissionalIdStub(
                ExperienciaProfissionalId(UUID("20000000-0000-0000-0000-000000000002"))
            ),
        )
        entrada = self._criar_entrada(empresa="  ")

        with self.assertRaises(RegraDeDominioViolada):
            await caso_de_uso.executar(entrada)

        self.assertEqual(repositorio.experiencias_salvas, [])

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def _criar_entrada(
        self, empresa: str = "Instituto Exemplo"
    ) -> CadastrarExperienciaProfissionalEntrada:
        """Produz uma entrada válida e determinística para os cenários assíncronos.

        O auxiliar concentra os campos estáveis do formulário e permite variar
        apenas a empresa nas verificações de falha. Ele existe para manter os
        testes do caso de uso focados na orquestração relevante.
        """
        return CadastrarExperienciaProfissionalEntrada(
            usuario_id=UsuarioId(UUID("20000000-0000-0000-0000-000000000003")),
            empresa=empresa,
            cargo="Desenvolvedora",
            descricao="Construiu integrações internas.",
            periodo=Periodo(inicio=date(2024, 1, 1), fim=None),
        )
