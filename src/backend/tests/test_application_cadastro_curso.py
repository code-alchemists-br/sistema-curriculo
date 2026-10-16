"""Testa unitariamente a orquestração do cadastro de cursos."""

from unittest import IsolatedAsyncioTestCase
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
from backend.application.cadastro_curso import (
    CadastrarCurso,
    CadastrarCursoEntrada,
    CursoJaCadastrado,
)
from backend.domain import Curso, CursoId, UsuarioId
from backend.domain.exceptions import RegraDeDominioViolada

ID_CURSO = UUID("00000000-0000-0000-0000-0000000000c1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class RepositorioCursoSpy:
    """Substitui a porta de curso e registra suas interações em memória.

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
        self.chaves_consultadas: list[tuple[UsuarioId, str, str]] = []
        self.cursos_salvos: list[Curso] = []

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        nome_normalizado: str,
        instituicao_normalizada: str,
    ) -> bool:
        """Registra a chave recebida e devolve a existência pré-configurada.

        O método mantém o contrato assíncrono da porta e não executa I/O. Ele
        existe para permitir que o teste observe a chave canônica consultada.
        """
        self.chaves_consultadas.append(
            (usuario_id, nome_normalizado, instituicao_normalizada)
        )
        return self.ja_existe

    async def salvar(self, curso: Curso) -> None:
        """Acumula o curso entregue pelo caso de uso em memória.

        O método registra a entidade após a decisão de não duplicidade e mantém
        a assinatura da porta. Ele existe para provar que a orquestração só
        solicita persistência no caminho permitido.
        """
        self.cursos_salvos.append(curso)


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class GeradorCursoIdStub:
    """Entrega uma identidade de curso determinística para os cenários.

    O stub retorna sempre o mesmo value object, sem gerar UUID ou acessar
    serviços. Ele existe para isolar o cadastro da estratégia externa de
    identidade e permitir asserções estáveis.
    """

    def __init__(self, identificador: CursoId) -> None:
        """Armazena a identidade que será devolvida pelo contrato da porta.

        O construtor recebe um value object pronto e o conserva imutavelmente.
        Ele existe para configurar cada cenário sem aleatoriedade.
        """
        self._identificador = identificador

    def gerar(self) -> CursoId:
        """Devolve a identidade determinística configurada para o cadastro.

        O método implementa a porta sem gerar dados novos. Ele existe para que
        o caso de uso receba uma identidade válida e testável.
        """
        return self._identificador


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class CadastrarCursoTestCase(IsolatedAsyncioTestCase):
    """Verifica decisões do caso de uso com todas as portas substituídas.

    A suíte combina spy e stub em memória para exercitar criação, chave
    normalizada, duplicidade e invariantes sem banco, API ou framework. Ela
    existe para proteger a orquestração interna do cadastro.
    """

    async def test_cria_e_salva_curso_com_chave_normalizada(self) -> None:
        """Consulta a chave canônica composta e persiste curso que não existe.

        O cenário usa caixa e espaços variados, executa o caso de uso e compara
        retorno, consulta e spy. Ele existe para verificar que a política de
        duplicidade antecede a persistência e preserva os textos exibidos.
        """
        repositorio = RepositorioCursoSpy(ja_existe=False)
        gerador_id = GeradorCursoIdStub(CursoId(ID_CURSO))
        caso_de_uso = CadastrarCurso(repositorio, gerador_id)

        entrada = CadastrarCursoEntrada(
            usuario_id=UsuarioId(ID_USUARIO),
            nome="  Desenvolvimento   Web   Fullstack  ",
            instituicao="  Universidade   Aberta  ",
            carga_horaria=120,
        )

        resultado = await caso_de_uso.executar(entrada)

        self.assertEqual(resultado.id, CursoId(ID_CURSO))
        self.assertEqual(resultado.usuario_id, UsuarioId(ID_USUARIO))
        self.assertEqual(resultado.nome, "Desenvolvimento   Web   Fullstack")
        self.assertEqual(resultado.instituicao, "Universidade   Aberta")
        self.assertEqual(resultado.carga_horaria, 120)

        self.assertEqual(
            repositorio.chaves_consultadas,
            [
                (
                    UsuarioId(ID_USUARIO),
                    "desenvolvimento web fullstack",
                    "universidade aberta",
                )
            ],
        )
        self.assertEqual(repositorio.cursos_salvos, [resultado])

    async def test_cria_e_salva_curso_sem_carga_horaria(self) -> None:
        """Persiste curso válido quando a carga horária é omitida.

        O cenário testa a permissividade do caso de uso com carga_horaria None.
        Ele existe para validar o suporte a cursos livres sem carga horária informada.
        """
        repositorio = RepositorioCursoSpy(ja_existe=False)
        gerador_id = GeradorCursoIdStub(CursoId(ID_CURSO))
        caso_de_uso = CadastrarCurso(repositorio, gerador_id)

        entrada = CadastrarCursoEntrada(
            usuario_id=UsuarioId(ID_USUARIO),
            nome="Git & GitHub",
            instituicao="Open Source Bootcamp",
            carga_horaria=None,
        )

        resultado = await caso_de_uso.executar(entrada)

        self.assertIsNone(resultado.carga_horaria)
        self.assertEqual(repositorio.cursos_salvos, [resultado])

    async def test_impede_duplicidade_e_nao_chama_salvar(self) -> None:
        """Interrompe a criação com CursoJaCadastrado quando o curso já existe.

        O cenário simula existência prévia no spy e confere o erro sem salvar.
        Ele existe para garantir que cursos redundantes sejam recusados.
        """
        repositorio = RepositorioCursoSpy(ja_existe=True)
        gerador_id = GeradorCursoIdStub(CursoId(ID_CURSO))
        caso_de_uso = CadastrarCurso(repositorio, gerador_id)

        entrada = CadastrarCursoEntrada(
            usuario_id=UsuarioId(ID_USUARIO),
            nome="Clean Code",
            instituicao="Escola Ágil",
        )

        with self.assertRaises(CursoJaCadastrado) as ctx:
            await caso_de_uso.executar(entrada)

        self.assertIn("já cadastrado", str(ctx.exception))
        self.assertEqual(len(repositorio.chaves_consultadas), 1)
        self.assertEqual(len(repositorio.cursos_salvos), 0)

    async def test_falha_de_dominio_nao_consulta_nem_salva(self) -> None:
        """Falha de invariante na entidade interrompe o fluxo antes do repositório.

        O cenário passa nome inválido (espaços vazios) e confere que nenhuma porta é chamada.
        Ele existe para assegurar integridade imediata de domínio antes da orquestração.
        """
        repositorio = RepositorioCursoSpy(ja_existe=False)
        gerador_id = GeradorCursoIdStub(CursoId(ID_CURSO))
        caso_de_uso = CadastrarCurso(repositorio, gerador_id)

        entrada = CadastrarCursoEntrada(
            usuario_id=UsuarioId(ID_USUARIO),
            nome="   ",
            instituicao="Escola",
        )

        with self.assertRaises(RegraDeDominioViolada):
            await caso_de_uso.executar(entrada)

        self.assertEqual(len(repositorio.chaves_consultadas), 0)
        self.assertEqual(len(repositorio.cursos_salvos), 0)
