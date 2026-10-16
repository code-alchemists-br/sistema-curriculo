"""Testa invariantes, value objects e normalização da entidade de curso."""

import unittest
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
from backend.domain import (
    CARGA_HORARIA_MAXIMA_CURSO,
    TAMANHO_MAXIMO_TEXTO_CURSO,
    Curso,
    CursoId,
    RegraDeDominioViolada,
    UsuarioId,
    normalizar_chave_curso,
    normalizar_texto_curso,
)

ID_VALIDO = UUID("00000000-0000-0000-0000-000000000001")
USUARIO_ID_VALIDO = UUID("00000000-0000-0000-0000-000000000002")


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class CursoIdTestCase(unittest.TestCase):
    """Verifica a integridade e construção do Value Object CursoId.

    A suíte valida que instâncias válidas de UUID sejam aceitas e que tipos
    incompatíveis sejam prontamente rejeitados na instanciação. Ela existe para
    proteger a integridade da identidade de cursos.
    """

    def test_cria_curso_id_com_uuid_valido(self) -> None:
        """Aceita UUID válido na criação de CursoId.

        O cenário instancia CursoId com um UUID padrão e confere o valor encapsulado.
        Ele existe para assegurar a construção correta do identificador de domínio.
        """
        curso_id = CursoId(ID_VALIDO)
        self.assertEqual(curso_id.valor, ID_VALIDO)

    def test_rejeita_curso_id_com_tipo_invalido(self) -> None:
        """Rejeita valor não UUID na criação de CursoId.

        O cenário passa tipos inadequados (string, inteiro) e confirma o disparo
        de RegraDeDominioViolada. Ele existe para evitar contaminação do domínio.
        """
        with self.assertRaises(RegraDeDominioViolada):
            CursoId("invalido")  # type: ignore[arg-type]


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class NormalizacaoCursoTestCase(unittest.TestCase):
    """Testa funções puras de validação e normalização de termos de curso.

    A suíte cobre limites de caracteres, detecção de caracteres de controle,
    colapso de espaços e minúsculas canônicas. Ela existe para certificar que
    a higienização de termos seja determinística.
    """

    def test_normalizar_texto_curso_apara_e_valida(self) -> None:
        """Apara espaços periféricos e aceita texto válido.

        O cenário passa texto com espaços no início e fim e valida que são removidos.
        Ele existe para manter textos limpos no domínio.
        """
        resultado = normalizar_texto_curso("  Python para Análise de Dados  ", "nome")
        self.assertEqual(resultado, "Python para Análise de Dados")

    def test_normalizar_texto_curso_rejeita_nao_string(self) -> None:
        """Rejeita valores não textuais com RegraDeDominioViolada.

        O cenário passa um número no lugar de texto e confere a exceção.
        Ele existe para barrar tipos espúrios em tempo de execução.
        """
        with self.assertRaises(RegraDeDominioViolada):
            normalizar_texto_curso(12345, "nome")  # type: ignore[arg-type]

    def test_normalizar_texto_curso_rejeita_vazio(self) -> None:
        """Rejeita strings vazias ou formadas apenas por espaços.

        O cenário passa espaços e tabulações vazias e exige a exceção.
        Ele existe para garantir preenchimento de campos obrigatórios.
        """
        with self.assertRaises(RegraDeDominioViolada):
            normalizar_texto_curso("   \t  ", "instituicao")

    def test_normalizar_texto_curso_rejeita_caracteres_de_controle(self) -> None:
        """Rejeita caracteres de controle que possam quebrar formatação ou segurança.

        O cenário insere caractere nulo ou de controle ASCII e valida a rejeição.
        Ele existe para prevenir injeções de controle invisíveis.
        """
        with self.assertRaises(RegraDeDominioViolada):
            normalizar_texto_curso("Curso\x00Inválido", "nome")

    def test_normalizar_texto_curso_rejeita_tamanho_excessivo(self) -> None:
        """Rejeita textos cujo comprimento aparado ultrapasse 200 caracteres.

        O cenário gera string de 201 caracteres e valida o disparo da regra.
        Ele existe para impor o limite máximo definido na modelagem.
        """
        texto_longo = "a" * (TAMANHO_MAXIMO_TEXTO_CURSO + 1)
        with self.assertRaises(RegraDeDominioViolada):
            normalizar_texto_curso(texto_longo, "nome")

    def test_normalizar_chave_curso_colapsa_espacos_e_aplica_casefold(self) -> None:
        """Colapsa múltiplos espaços internos e converte para minúsculas.

        O cenário entrega string despadronizada e confere a chave canônica gerada.
        Ele existe para garantir chave única para deduplicação lógica.
        """
        resultado = normalizar_chave_curso("  CURSO   DE   DOCKER  ")
        self.assertEqual(resultado, "curso de docker")

    def test_normalizar_chave_curso_rejeita_nao_string(self) -> None:
        """Rejeita tipos não textuais na geração de chave canônica.

        O cenário passa valor inadequado e valida o lançamento de RegraDeDominioViolada.
        Ele existe para blindar a geração da chave canônica.
        """
        with self.assertRaises(RegraDeDominioViolada):
            normalizar_chave_curso(None)  # type: ignore[arg-type]


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class CursoTestCase(unittest.TestCase):
    """Verifica a criação da entidade Curso e suas invariantes de domínio.

    A suíte valida a instanciação com e sem carga horária, as proteções estritas
    de tipo (rejeição de bool, float, valores negativos ou fora da faixa) e
    as propriedades canônicas de normalização. Ela existe para blindar o domínio
    de dados inconsistentes.
    """

    def test_cria_curso_com_sucesso_sem_carga_horaria(self) -> None:
        """Cria um curso com dados válidos e carga horária nula.

        O cenário instancia Curso com carga_horaria omitida/None e confere campos.
        Ele existe para comprovar a permissividade com cursos informais/livres.
        """
        curso = Curso(
            id=CursoId(ID_VALIDO),
            usuario_id=UsuarioId(USUARIO_ID_VALIDO),
            nome="Arquitetura Limpa",
            instituicao="Faculdade de Tecnologia",
        )
        self.assertEqual(curso.nome, "Arquitetura Limpa")
        self.assertEqual(curso.instituicao, "Faculdade de Tecnologia")
        self.assertIsNone(curso.carga_horaria)
        self.assertEqual(curso.nome_normalizado, "arquitetura limpa")
        self.assertEqual(curso.instituicao_normalizada, "faculdade de tecnologia")

    def test_cria_curso_com_sucesso_com_carga_horaria(self) -> None:
        """Cria um curso com dados válidos e carga horária inteira positiva.

        O cenário instancia Curso com carga horária dentro do limite permitido.
        Ele existe para assegurar aceitação de cursos com duração estipulada.
        """
        curso = Curso(
            id=CursoId(ID_VALIDO),
            usuario_id=UsuarioId(USUARIO_ID_VALIDO),
            nome="  Python   Avançado  ",
            instituicao="  Alura Cursos  ",
            carga_horaria=40,
        )
        self.assertEqual(curso.nome, "Python   Avançado")
        self.assertEqual(curso.instituicao, "Alura Cursos")
        self.assertEqual(curso.carga_horaria, 40)
        self.assertEqual(curso.nome_normalizado, "python avançado")
        self.assertEqual(curso.instituicao_normalizada, "alura cursos")

    def test_rejeita_carga_horaria_booleana(self) -> None:
        """Rejeita carga horária que seja bool (isinstance(True, int) é True).

        O cenário passa True e False como carga_horaria e exige RegraDeDominioViolada.
        Ele existe para atender o Refinamento 1 contra contorno de subtipos em Python.
        """
        with self.assertRaises(RegraDeDominioViolada) as ctx:
            Curso(
                id=CursoId(ID_VALIDO),
                usuario_id=UsuarioId(USUARIO_ID_VALIDO),
                nome="Curso",
                instituicao="Escola",
                carga_horaria=True,  # type: ignore[arg-type]
            )
        self.assertIn("deve ser um número inteiro", str(ctx.exception))

    def test_rejeita_carga_horaria_nao_inteira(self) -> None:
        """Rejeita carga horária com tipo float ou string.

        O cenário passa números de ponto flutuante e exige a regra de domínio violada.
        Ele existe para garantir que a carga horária seja sempre expressa em horas inteiras.
        """
        with self.assertRaises(RegraDeDominioViolada):
            Curso(
                id=CursoId(ID_VALIDO),
                usuario_id=UsuarioId(USUARIO_ID_VALIDO),
                nome="Curso",
                instituicao="Escola",
                carga_horaria=10.5,  # type: ignore[arg-type]
            )

    def test_rejeita_carga_horaria_abaixo_do_minimo(self) -> None:
        """Rejeita carga horária menor que 1 hora (zero ou números negativos).

        O cenário testa valores 0 e -5 e confere a exceção com mensagem instrutiva.
        Ele existe para impedir representação de durações impossíveis.
        """
        with self.assertRaises(RegraDeDominioViolada):
            Curso(
                id=CursoId(ID_VALIDO),
                usuario_id=UsuarioId(USUARIO_ID_VALIDO),
                nome="Curso",
                instituicao="Escola",
                carga_horaria=0,
            )
        with self.assertRaises(RegraDeDominioViolada):
            Curso(
                id=CursoId(ID_VALIDO),
                usuario_id=UsuarioId(USUARIO_ID_VALIDO),
                nome="Curso",
                instituicao="Escola",
                carga_horaria=-10,
            )

    def test_rejeita_carga_horaria_acima_do_maximo(self) -> None:
        """Rejeita carga horária superior ao limite estipulado de 10000 horas.

        O cenário testa valor limítrofe superior (10001) e valida o erro.
        Ele existe para manter sanidade dimensional dos registros de cursos.
        """
        with self.assertRaises(RegraDeDominioViolada):
            Curso(
                id=CursoId(ID_VALIDO),
                usuario_id=UsuarioId(USUARIO_ID_VALIDO),
                nome="Curso",
                instituicao="Escola",
                carga_horaria=CARGA_HORARIA_MAXIMA_CURSO + 1,
            )
