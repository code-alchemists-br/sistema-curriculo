"""Testa invariantes unitárias dos value objects do domínio."""

from datetime import date
import unittest

from backend.domain import Email, Nome, Periodo, RegraDeDominioViolada, UsuarioId


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
class ValueObjectsDoDominioTestCase(unittest.TestCase):
    """Verifica regras locais de valores sem dependência externa.

    A classe constrói value objects em memória e observa suas validações e
    normalizações. Ela existe para proteger as invariantes que entidades e
    agregados reutilizarão sem iniciar framework, banco ou rede.
    """

    def test_email_normaliza_espacos_e_maiusculas(self) -> None:
        """Confirma que o e-mail é normalizado ao ser criado.

        O teste fornece espaços e letras maiúsculas, então inspeciona o valor
        interno normalizado. Ele existe para garantir que usuários compartilhem
        uma representação estrutural consistente de e-mail.
        """
        self.assertEqual(Email("  ALUNA@FATEC.SP.GOV.BR ").valor, "aluna@fatec.sp.gov.br")

    def test_email_invalido_e_rejeitado(self) -> None:
        """Confirma que um e-mail sem domínio válido viola a regra de domínio.

        O teste tenta construir o value object com formato incompleto e espera a
        falha específica. Ele existe para impedir que entidades recebam e-mails
        estruturalmente inválidos.
        """
        with self.assertRaises(RegraDeDominioViolada):
            Email("aluna@fatec")

    def test_periodo_rejeita_fim_anterior_ao_inicio(self) -> None:
        """Confirma que o intervalo não aceita ordem cronológica invertida.

        O teste fornece uma data final anterior à inicial e observa a falha de
        domínio. Ele existe para proteger formação e experiência contra períodos
        impossíveis antes que sejam associados a uma entidade.
        """
        with self.assertRaises(RegraDeDominioViolada):
            Periodo(date(2026, 2, 1), date(2026, 1, 31))

    def test_identificador_rejeita_valor_que_nao_e_uuid(self) -> None:
        """Confirma que uma identidade de usuário não aceita texto livre.

        O teste informa uma string no lugar de UUID e espera a falha de domínio.
        Ele existe para manter a separação entre valores de transporte e as
        identidades tipadas que os agregados utilizam.
        """
        with self.assertRaises(RegraDeDominioViolada):
            UsuarioId("nao-e-uuid")  # type: ignore[arg-type]

    def test_nome_remove_espacos_e_rejeita_vazio(self) -> None:
        """Confirma a normalização e a presença obrigatória do nome.

        O teste observa a remoção de espaços e exercita a falha para texto vazio.
        Ele existe para assegurar que a identidade legível do usuário não seja
        perdida por entrada composta apenas de espaços.
        """
        self.assertEqual(Nome("  Ana Silva ").valor, "Ana Silva")
        with self.assertRaises(RegraDeDominioViolada):
            Nome("   ")
