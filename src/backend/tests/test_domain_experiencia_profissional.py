"""Testa as invariantes da entidade de experiência profissional.

Os testes exercitam apenas objetos do domínio e verificam que o currículo não
aceita experiências sem seus textos essenciais. Eles existem para proteger as
regras antes que a entidade seja usada pela camada de aplicação.
"""

# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from datetime import date, datetime, timezone
from unittest import TestCase
from uuid import UUID

from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import (
    ExperienciaProfissionalId,
    Periodo,
    UsuarioId,
)


# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
class ExperienciaProfissionalTestCase(TestCase):
    """Verifica a criação de experiências profissionais no núcleo de domínio.

    A suíte constrói value objects determinísticos e cria a entidade diretamente
    para observar suas invariantes, sem usar serviços externos. Ela existe para
    assegurar que regras obrigatórias permaneçam próximas ao modelo.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def test_cria_experiencia_com_dados_obrigatorios_preenchidos(self) -> None:
        """Aceita uma experiência quando todos os textos obrigatórios existem.

        O teste constrói a entidade com identificadores e período válidos e
        confirma a preservação dos dados recebidos. Ele existe para documentar
        o caminho de sucesso da invariante de cadastro profissional.
        """
        experiencia = self._criar_experiencia()

        self.assertEqual(experiencia.empresa, "Instituto Exemplo")
        self.assertEqual(experiencia.cargo, "Desenvolvedora")
        self.assertEqual(experiencia.descricao, "Construiu integrações internas.")

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def test_rejeita_textos_obrigatorios_vazios(self) -> None:
        """Recusa empresa, cargo ou descrição formados apenas por espaços.

        O teste substitui cada texto por um valor vazio e verifica a exceção de
        domínio gerada na construção. Ele existe para impedir o registro de
        experiências que não possam ser apresentadas no currículo.
        """
        for campo in ("empresa", "cargo", "descricao"):
            with self.subTest(campo=campo):
                dados = {
                    "empresa": "Instituto Exemplo",
                    "cargo": "Desenvolvedora",
                    "descricao": "Construiu integrações internas.",
                }
                dados[campo] = "   "

                with self.assertRaises(RegraDeDominioViolada):
                    self._criar_experiencia(**dados)

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def test_rejeita_periodo_com_termino_anterior_ao_inicio(self) -> None:
        """Recusa um período cuja data final antecede a inicial.

        O teste solicita a construção do value object que compõe a experiência
        com datas invertidas e observa a regra de domínio. Ele existe para
        garantir que o cadastro profissional dependa de uma cronologia válida.
        """
        with self.assertRaises(RegraDeDominioViolada):
            Periodo(inicio=date(2025, 2, 1), fim=date(2025, 1, 31))

    def test_editar_substitui_dados_preservando_identidade_e_proprietario(self) -> None:
        """Devolve nova experiência com os dados editados e a mesma identidade.

        O teste edita todos os campos editáveis e compara o resultado com a
        entidade original, que deve permanecer inalterada. Ele existe para
        garantir que a edição não troque o dono nem mute a entidade imutável.
        """
        original = self._criar_experiencia()
        periodo = Periodo(inicio=date(2024, 3, 1))

        editada = original.editar(
            empresa="Nova Empresa",
            cargo="Analista",
            descricao="Mantém APIs em produção.",
            periodo=periodo,
        )

        self.assertEqual(
            (editada.id, editada.usuario_id), (original.id, original.usuario_id)
        )
        self.assertEqual(
            (editada.empresa, editada.cargo, editada.descricao, editada.periodo),
            ("Nova Empresa", "Analista", "Mantém APIs em produção.", periodo),
        )
        self.assertEqual(original.empresa, "Instituto Exemplo")

    def test_editar_rejeita_textos_obrigatorios_vazios(self) -> None:
        """Recusa edição que deixe empresa, cargo ou descrição em branco.

        O teste edita cada texto para um valor formado por espaços e observa a
        mesma regra aplicada na criação. Ele existe para impedir que a edição
        produza uma experiência impossível de apresentar no currículo.
        """
        original = self._criar_experiencia()
        for campo in ("empresa", "cargo", "descricao"):
            with self.subTest(campo=campo):
                dados = {
                    "empresa": "Nova Empresa",
                    "cargo": "Analista",
                    "descricao": "Mantém APIs em produção.",
                    "periodo": original.periodo,
                }
                dados[campo] = "   "

                with self.assertRaises(RegraDeDominioViolada):
                    original.editar(**dados)

    def test_experiencia_nova_nao_esta_excluida(self) -> None:
        """Cria experiências ativas por padrão.

        O teste constrói a entidade sem ``deleted_at`` e observa o estado
        derivado. Ele existe para garantir que cadastros existentes continuem
        ativos após a introdução da exclusão lógica.
        """
        experiencia = self._criar_experiencia()

        self.assertIsNone(experiencia.deleted_at)
        self.assertFalse(experiencia.excluida)

    def test_excluir_registra_instante_e_preserva_os_dados(self) -> None:
        """Marca a exclusão com o instante informado sem mutar a original.

        O teste exclui uma experiência ativa e compara identidade, textos e o
        novo ``deleted_at``. Ele existe para proteger a transição de exclusão
        lógica no ponto mais próximo dos dados.
        """
        original = self._criar_experiencia()
        instante = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)

        excluida = original.excluir(instante)

        self.assertTrue(excluida.excluida)
        self.assertEqual(excluida.deleted_at, instante)
        self.assertEqual((excluida.id, excluida.empresa), (original.id, original.empresa))
        self.assertFalse(original.excluida)

    def test_excluir_novamente_preserva_o_primeiro_instante(self) -> None:
        """Devolve a mesma entidade quando a experiência já está excluída.

        A segunda chamada usa outro instante e não deve sobrescrever o
        primeiro. O teste existe para tornar a exclusão idempotente.
        """
        primeiro = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
        excluida = self._criar_experiencia().excluir(primeiro)

        repetida = excluida.excluir(datetime(2026, 10, 18, 9, 0, tzinfo=timezone.utc))

        self.assertIs(repetida, excluida)
        self.assertEqual(repetida.deleted_at, primeiro)

    def test_excluir_exige_instante_com_fuso_horario(self) -> None:
        """Recusa instante de exclusão sem fuso horário.

        O teste fornece um datetime ingênuo e espera a regra de domínio. Ele
        existe para evitar instantes ambíguos no registro de exclusão.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_experiencia().excluir(datetime(2026, 10, 17, 12, 0))

    def test_editar_preserva_estado_de_exclusao(self) -> None:
        """Mantém ``deleted_at`` ao editar uma experiência.

        O teste edita uma experiência já excluída e confere que o marcador é
        conservado. Ele existe para que a edição nunca reative implicitamente
        um item removido.
        """
        instante = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
        excluida = self._criar_experiencia().excluir(instante)

        editada = excluida.editar(
            empresa="Nova Empresa",
            cargo="Analista",
            descricao="Mantém APIs em produção.",
            periodo=excluida.periodo,
        )

        self.assertEqual(editada.deleted_at, instante)

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def _criar_experiencia(
        self,
        empresa: str = "Instituto Exemplo",
        cargo: str = "Desenvolvedora",
        descricao: str = "Construiu integrações internas.",
    ) -> ExperienciaProfissional:
        """Monta uma experiência com identificadores e período determinísticos.

        O auxiliar concentra os dados válidos compartilhados pelos cenários e
        permite alterar um campo de cada vez em cada teste. Ele existe para
        tornar as verificações de invariantes legíveis e independentes de I/O.
        """
        return ExperienciaProfissional(
            id=ExperienciaProfissionalId(UUID("10000000-0000-0000-0000-000000000001")),
            usuario_id=UsuarioId(UUID("10000000-0000-0000-0000-000000000002")),
            empresa=empresa,
            cargo=cargo,
            descricao=descricao,
            periodo=Periodo(inicio=date(2024, 1, 1), fim=None),
        )
