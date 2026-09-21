"""Testa as invariantes da entidade de experiência profissional.

Os testes exercitam apenas objetos do domínio e verificam que o currículo não
aceita experiências sem seus textos essenciais. Eles existem para proteger as
regras antes que a entidade seja usada pela camada de aplicação.
"""

# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from datetime import date
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
