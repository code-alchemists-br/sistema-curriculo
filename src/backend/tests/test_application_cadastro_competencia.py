"""Testa unitariamente a orquestração do cadastro de competências."""

from unittest import IsolatedAsyncioTestCase
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
from backend.application.cadastro_competencia import (
    CadastrarCompetencia,
    CadastrarCompetenciaEntrada,
    CompetenciaJaCadastrada,
)
from backend.domain import CategoriaCompetencia, Competencia, CompetenciaId, UsuarioId
from backend.domain.exceptions import RegraDeDominioViolada


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class RepositorioCompetenciaSpy:
    """Substitui a porta de competência e registra suas interações em memória.

    O double devolve a existência configurada para uma chave e acumula entidades
    salvas, sem usar adapter ou banco. Ele existe para tornar observável a
    sequência do caso de uso em testes unitários determinísticos.
    """

    def __init__(self, ja_existe: bool = False) -> None:
        """Inicializa o resultado de consulta e o histórico de persistência.

        O construtor recebe a resposta que simulará para a chave de duplicidade
        e cria coleções locais de observação. Ele existe para variar somente o
        estado relevante de cada cenário sem infraestrutura externa.
        """
        self.ja_existe = ja_existe
        self.chaves_consultadas: list[tuple[UsuarioId, CategoriaCompetencia, str]] = []
        self.competencias_salvas: list[Competencia] = []

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        categoria: CategoriaCompetencia,
        descricao_normalizada: str,
    ) -> bool:
        """Registra a chave recebida e devolve a existência pré-configurada.

        O método mantém o contrato assíncrono da porta e não executa I/O. Ele
        existe para permitir que o teste observe a chave canônica consultada.
        """
        self.chaves_consultadas.append((usuario_id, categoria, descricao_normalizada))
        return self.ja_existe

    async def salvar(self, competencia: Competencia) -> None:
        """Acumula a competência entregue pelo caso de uso em memória.

        O método registra a entidade após a decisão de não duplicidade e mantém
        a assinatura da porta. Ele existe para provar que a orquestração só
        solicita persistência no caminho permitido.
        """
        self.competencias_salvas.append(competencia)


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class GeradorCompetenciaIdStub:
    """Entrega uma identidade de competência determinística para os cenários.

    O stub retorna sempre o mesmo value object, sem gerar UUID ou acessar
    serviços. Ele existe para isolar o cadastro da estratégia externa de
    identidade e permitir asserções estáveis.
    """

    def __init__(self, identificador: CompetenciaId) -> None:
        """Armazena a identidade que será devolvida pelo contrato da porta.

        O construtor recebe um value object pronto e o conserva imutavelmente.
        Ele existe para configurar cada cenário sem aleatoriedade.
        """
        self._identificador = identificador

    def gerar(self) -> CompetenciaId:
        """Devolve a identidade determinística configurada para o cadastro.

        O método implementa a porta sem gerar dados novos. Ele existe para que
        o caso de uso receba uma identidade válida e testável.
        """
        return self._identificador


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class CadastrarCompetenciaTestCase(IsolatedAsyncioTestCase):
    """Verifica decisões do caso de uso com todas as portas substituídas.

    A suíte combina spy e stub em memória para exercitar criação, chave
    normalizada, duplicidade e invariantes sem banco, API ou framework. Ela
    existe para proteger a orquestração interna do cadastro.
    """

    async def test_cria_e_salva_competencia_com_chave_normalizada(self) -> None:
        """Consulta a chave canônica e persiste competência que não existe.

        O cenário usa caixa e espaços variados, executa o caso de uso e compara
        retorno, consulta e spy. Ele existe para verificar que a política de
        duplicidade antecede a persistência e preserva a descrição exibida.
        """
        repositorio = RepositorioCompetenciaSpy()
        caso_de_uso = self._criar_caso_de_uso(repositorio)
        entrada = self._criar_entrada(descricao="  Power   BI  ")

        competencia = await caso_de_uso.executar(entrada)

        self.assertEqual(competencia.descricao, "Power   BI")
        self.assertEqual(
            repositorio.chaves_consultadas,
            [(entrada.usuario_id, CategoriaCompetencia.TECNICA, "power bi")],
        )
        self.assertEqual(repositorio.competencias_salvas, [competencia])

    async def test_recusa_duplicata_sem_persistir(self) -> None:
        """Interrompe o cadastro quando a porta encontra a mesma chave lógica.

        O cenário simula uma competência existente e observa a falha específica
        sem entidade salva. Ele existe para impedir registros paralelos de uma
        competência que difere apenas por caixa ou espaços.
        """
        repositorio = RepositorioCompetenciaSpy(ja_existe=True)
        caso_de_uso = self._criar_caso_de_uso(repositorio)

        with self.assertRaises(CompetenciaJaCadastrada):
            await caso_de_uso.executar(self._criar_entrada(descricao=" python "))

        self.assertEqual(repositorio.chaves_consultadas[0][2], "python")
        self.assertEqual(repositorio.competencias_salvas, [])

    async def test_consulta_chave_delimitada_por_usuario_e_categoria_sem_nivel(
        self,
    ) -> None:
        """Preserva proprietário e categoria, mas exclui nível da chave lógica.

        O cenário cadastra uma competência com outro proprietário, categoria e
        nível e inspeciona os argumentos do spy. Ele existe para proteger a
        regra de que apenas proprietário, categoria e descrição normalizada
        definem a possível duplicidade.
        """
        repositorio = RepositorioCompetenciaSpy()
        caso_de_uso = self._criar_caso_de_uso(repositorio)
        usuario_id = UsuarioId(UUID("60000000-0000-0000-0000-000000000003"))
        entrada = CadastrarCompetenciaEntrada(
            usuario_id=usuario_id,
            categoria=CategoriaCompetencia.COMPORTAMENTAL,
            descricao="  Comunicação  ",
            nivel="Intermediário",
        )

        await caso_de_uso.executar(entrada)

        self.assertEqual(
            repositorio.chaves_consultadas,
            [(usuario_id, CategoriaCompetencia.COMPORTAMENTAL, "comunicação")],
        )

    async def test_nao_consulta_nem_salva_quando_entidade_eh_invalida(self) -> None:
        """Valida o domínio antes de consultar ou persistir a competência.

        O cenário fornece descrição sem termos e exige a falha de domínio antes
        de observar qualquer colaboração com o repositório. Ele existe para
        manter invariantes próximas à entidade e evitar I/O desnecessário.
        """
        repositorio = RepositorioCompetenciaSpy()
        caso_de_uso = self._criar_caso_de_uso(repositorio)

        with self.assertRaises(RegraDeDominioViolada):
            await caso_de_uso.executar(self._criar_entrada(descricao=" \t "))

        self.assertEqual(repositorio.chaves_consultadas, [])
        self.assertEqual(repositorio.competencias_salvas, [])

    def _criar_caso_de_uso(
        self, repositorio: RepositorioCompetenciaSpy
    ) -> CadastrarCompetencia:
        """Compõe o caso de uso com doubles que pertencem a este teste.

        O auxiliar injeta spy e stub, sem usar adapter produtivo. Ele existe para
        manter cada cenário focado na decisão observada pela orquestração.
        """
        return CadastrarCompetencia(
            repositorio=repositorio,
            gerador_id=GeradorCompetenciaIdStub(
                CompetenciaId(UUID("60000000-0000-0000-0000-000000000001"))
            ),
        )

    def _criar_entrada(
        self,
        descricao: str = "Python",
        categoria: CategoriaCompetencia = CategoriaCompetencia.TECNICA,
        nivel: str = "Avançado",
    ) -> CadastrarCompetenciaEntrada:
        """Produz entrada válida e permite variar campos relevantes ao cenário.

        O auxiliar fixa o proprietário e os valores usuais, deixando cada teste
        mudar descrição, categoria ou nível. Ele existe para tornar os casos
        curtos e concentrados na regra exercitada.
        """
        return CadastrarCompetenciaEntrada(
            usuario_id=UsuarioId(UUID("60000000-0000-0000-0000-000000000002")),
            categoria=categoria,
            descricao=descricao,
            nivel=nivel,
        )
