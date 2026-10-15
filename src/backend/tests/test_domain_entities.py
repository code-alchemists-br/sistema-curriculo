"""Testa a construção unitária das entidades independentes do perfil."""

import unittest
from datetime import date
from uuid import uuid4

# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
from backend.domain import (
    TAMANHO_MAXIMO_TEXTO_FORMACAO,
    Email,
    FormacaoAcademica,
    FormacaoAcademicaId,
    HashSenha,
    NivelFormacaoAcademica,
    Nome,
    Periodo,
    RegraDeDominioViolada,
    StatusFormacaoAcademica,
    Usuario,
    UsuarioId,
)


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
class EntidadesDoDominioTestCase(unittest.TestCase):
    """Verifica entidades com identidade e proprietário explícitos.

    A classe constrói agregados e itens de perfil somente com value objects em
    memória. Ela existe para confirmar que esses conceitos são reutilizáveis sem
    FastAPI, ORM, persistência ou recursos externos.
    """

    def test_usuario_reune_identidade_e_dados_de_conta_tipados(self) -> None:
        """Confirma que o aggregate root de usuário preserva seus value objects.

        O teste monta uma conta válida e compara os objetos recebidos pela
        entidade. Ele existe para assegurar que a primeira fatia não reduz dados
        de conta a DTOs ou strings sem significado de domínio.
        """
        usuario_id = UsuarioId(uuid4())
        usuario = Usuario(
            id=usuario_id,
            nome=Nome("Ana Silva"),
            email=Email("ana.silva@fatec.sp.gov.br"),
            hash_senha=HashSenha("hash-ja-derivado"),
        )

        self.assertIs(usuario.id, usuario_id)
        self.assertEqual(usuario.nome.valor, "Ana Silva")

    def test_formacao_e_item_reutilizavel_com_proprietario_e_periodo(self) -> None:
        """Confirma que uma formação mantém proprietário e intervalo válidos.

        O teste constrói a entidade de perfil separadamente de qualquer currículo
        e inspeciona suas identidades. Ele existe para proteger a decisão de que
        formações podem ser reutilizadas entre versões de currículo.
        """
        usuario_id = UsuarioId(uuid4())
        formacao = FormacaoAcademica(
            id=FormacaoAcademicaId(uuid4()),
            usuario_id=usuario_id,
            instituicao="FATEC",
            curso="Análise e Desenvolvimento de Sistemas",
            nivel=NivelFormacaoAcademica.TECNOLOGO,
            periodo=Periodo(date(2024, 2, 1)),
            status=StatusFormacaoAcademica.EM_ANDAMENTO,
        )

        self.assertIs(formacao.usuario_id, usuario_id)
        self.assertIsNone(formacao.periodo.fim)

    def test_aceita_todos_os_niveis_academicos(self) -> None:
        """Confirma que o vocabulário contém e aceita cada nível aprovado.

        O teste constrói uma entidade por membro do enum sem I/O. Ele existe
        para proteger o contrato canônico usado por cadastro e currículos.
        """
        for nivel in NivelFormacaoAcademica:
            with self.subTest(nivel=nivel):
                self.assertIs(_criar_formacao(nivel=nivel).nivel, nivel)

    def test_aceita_todos_os_status_com_periodos_compativeis(self) -> None:
        """Confirma que cada status válido pode compor uma formação.

        O teste escolhe período compatível com cada membro do enum e constrói
        as entidades diretamente. Ele existe para proteger o vocabulário de
        estado e a regra de data final.
        """
        periodos = {
            StatusFormacaoAcademica.EM_ANDAMENTO: Periodo(date(2024, 1, 1)),
            StatusFormacaoAcademica.CONCLUIDO: Periodo(
                date(2024, 1, 1), date(2025, 1, 1)
            ),
            StatusFormacaoAcademica.INTERROMPIDO: Periodo(date(2024, 1, 1)),
        }
        for status in StatusFormacaoAcademica:
            with self.subTest(status=status):
                self.assertIs(_criar_formacao(status=status, periodo=periodos[status]).status, status)

    def test_rejeita_valores_que_nao_sao_enums_do_dominio(self) -> None:
        """Impede que strings ou objetos desconhecidos contornem os enums.

        O teste tenta construir entidades com valores que não são membros dos
        enums. Ele existe para manter o vocabulário fechado fora da API também.
        """
        for campo, valor in (("nivel", "tecnologo"), ("status", "em_andamento")):
            with self.subTest(campo=campo):
                with self.assertRaises(RegraDeDominioViolada):
                    _criar_formacao(**{campo: valor})

    def test_valida_as_seis_combinacoes_de_status_e_data_final(self) -> None:
        """Verifica cada presença possível de data final para os três status.

        O teste constrói os seis pares entre status e fim e compara sua
        validade com a regra do produto. Ele existe para evitar regressão nas
        previsões de conclusão e nos registros concluídos ou interrompidos.
        """
        fim = date(2025, 1, 1)
        casos = (
            (StatusFormacaoAcademica.EM_ANDAMENTO, None, True),
            (StatusFormacaoAcademica.EM_ANDAMENTO, fim, True),
            (StatusFormacaoAcademica.CONCLUIDO, None, False),
            (StatusFormacaoAcademica.CONCLUIDO, fim, True),
            (StatusFormacaoAcademica.INTERROMPIDO, None, True),
            (StatusFormacaoAcademica.INTERROMPIDO, fim, True),
        )
        for status, data_fim, valido in casos:
            with self.subTest(status=status, data_fim=data_fim):
                if valido:
                    formacao = _criar_formacao(
                        status=status,
                        periodo=Periodo(date(2024, 1, 1), data_fim),
                    )
                    self.assertEqual(formacao.periodo.fim, data_fim)
                else:
                    with self.assertRaises(RegraDeDominioViolada):
                        _criar_formacao(status=status)

    def test_aceita_previsao_futura_para_formacao_em_andamento_e_concluida(self) -> None:
        """Permite datas futuras sem conflitar com o status informado.

        O teste cria períodos futuros para estados em andamento e concluído.
        Ele existe para não impedir previsões acadêmicas válidas nem impor
        política temporal adicional ao domínio.
        """
        futuro = date(2030, 1, 1)
        for status in (
            StatusFormacaoAcademica.EM_ANDAMENTO,
            StatusFormacaoAcademica.CONCLUIDO,
        ):
            with self.subTest(status=status):
                formacao = _criar_formacao(
                    status=status,
                    periodo=Periodo(date(2024, 1, 1), futuro),
                )
                self.assertEqual(formacao.periodo.fim, futuro)

    def test_rejeita_fim_anterior_ao_inicio(self) -> None:
        """Preserva a cronologia definida pelo value object Periodo.

        O teste fornece um fim anterior ao início e observa a violação na
        construção do período. Ele existe para manter a regra temporal no
        objeto de domínio que governa as datas.
        """
        with self.assertRaises(RegraDeDominioViolada):
            Periodo(date(2025, 1, 1), date(2024, 1, 1))

    def test_normaliza_e_aceita_limites_de_um_e_duzentos_caracteres(self) -> None:
        """Aplica strip antes de medir textos de instituição e curso.

        O teste cobre os limites mínimo e máximo com espaços externos e
        verifica a forma normalizada guardada na entidade. Ele existe para
        manter os valores armazenados dentro do contrato comum das camadas.
        """
        for campo in ("instituicao", "curso"):
            for tamanho in (1, TAMANHO_MAXIMO_TEXTO_FORMACAO):
                with self.subTest(campo=campo, tamanho=tamanho):
                    texto = f"  {'x' * tamanho}  "
                    formacao = _criar_formacao(**{campo: texto})
                    self.assertEqual(getattr(formacao, campo), "x" * tamanho)

    def test_rejeita_textos_vazios_acima_do_limite_e_com_controles(self) -> None:
        """Rejeita conteúdo vazio, longo demais ou com caracteres de controle.

        O teste exercita os dois campos textuais em entradas inválidas,
        incluindo controle removível por strip. Ele existe para impedir que
        texto inválido alcance persistência ou apresentação.
        """
        valores_invalidos = ("", "   ", "x" * (TAMANHO_MAXIMO_TEXTO_FORMACAO + 1), "\tx", "x\ny")
        for campo in ("instituicao", "curso"):
            for valor in valores_invalidos:
                with self.subTest(campo=campo, valor=repr(valor)):
                    with self.assertRaises(RegraDeDominioViolada):
                        _criar_formacao(**{campo: valor})


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
def _criar_formacao(
    *,
    nivel: NivelFormacaoAcademica = NivelFormacaoAcademica.TECNOLOGO,
    status: StatusFormacaoAcademica = StatusFormacaoAcademica.EM_ANDAMENTO,
    instituicao: str = "FATEC",
    curso: str = "Análise e Desenvolvimento de Sistemas",
    periodo: Periodo | None = None,
) -> FormacaoAcademica:
    """Cria uma formação válida com campos variáveis para testes de domínio.

    A função completa os campos invariáveis com valores estáveis e permite
    alterar cada entrada relevante sem serviços externos. Ela existe para
    tornar os testes de regras concisos e independentes.
    """
    return FormacaoAcademica(
        id=FormacaoAcademicaId(uuid4()),
        usuario_id=UsuarioId(uuid4()),
        instituicao=instituicao,
        curso=curso,
        nivel=nivel,
        periodo=periodo or Periodo(date(2024, 1, 1)),
        status=status,
    )
