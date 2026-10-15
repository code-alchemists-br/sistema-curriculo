"""Testa invariantes e normalização da entidade de certificação e seu value object."""

import unittest
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
from backend.domain import (
    Certificacao,
    CertificacaoId,
    RegraDeDominioViolada,
    UsuarioId,
    normalizar_chave_certificacao,
    normalizar_texto_certificacao,
)


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class CertificacaoIdTestCase(unittest.TestCase):
    """Verifica a validação estrutural do Value Object CertificacaoId.

    A suíte testa a aceitação de UUIDs legítimos e a rejeição de outros tipos
    ou valores malformados. Ela existe para garantir que identidades inválidas
    sejam bloqueadas antes de serem associadas a uma certificação.
    """

    def test_aceita_uuid_valido(self) -> None:
        """Instancia o value object com UUID válido.

        O cenário fornece um UUID nativo e valida se o valor interno é preservado.
        Ele existe para assegurar a construção regular da identidade.
        """
        raw_uuid = UUID("70000000-0000-0000-0000-000000000001")
        cert_id = CertificacaoId(raw_uuid)
        self.assertEqual(cert_id.valor, raw_uuid)

    def test_rejeita_tipo_invalido(self) -> None:
        """Impede a instanciação de CertificacaoId com tipos não UUID.

        O teste passa uma string e verifica o disparo de RegraDeDominioViolada.
        Ele existe para proteger a integridade tipada do domínio.
        """
        with self.assertRaises(RegraDeDominioViolada):
            CertificacaoId("70000000-0000-0000-0000-000000000001")  # type: ignore[arg-type]


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class CertificacaoTestCase(unittest.TestCase):
    """Verifica as invariantes e a chave canônica de certificações em memória.

    A suíte constrói entidades apenas com value objects e compara a política de
    normalização e validação de textos. Ela existe para proteger as regras de
    negócio que antecedem o cadastro e a deduplicação.
    """

    def test_apara_textos_e_expoe_chaves_normalizadas(self) -> None:
        """Apara espaços e calcula chaves canônicas para nome e emissor.

        O cenário instancia uma certificação com espaços laterais e múltiplos
        espaços internos e compara com os valores aparados e as chaves calculadas.
        Ele existe para garantir que a deduplicação seja determinística e insensível
        a caixa e espaços redundantes.
        """
        certificacao = self._criar_certificacao(
            nome="  AWS   Certified   Solutions   Architect  ",
            organizacao_emissora="  Amazon   Web   Services  ",
        )

        self.assertEqual(certificacao.nome, "AWS   Certified   Solutions   Architect")
        self.assertEqual(
            certificacao.organizacao_emissora, "Amazon   Web   Services"
        )
        self.assertEqual(
            certificacao.nome_normalizado,
            "aws certified solutions architect",
        )
        self.assertEqual(
            certificacao.organizacao_emissora_normalizada,
            "amazon web services",
        )

    def test_rejeita_nome_vazio_ou_apenas_espacos(self) -> None:
        """Impede certificação com nome em branco ou contendo apenas caracteres de espaço.

        O teste fornece variações de espaços e quebras de linha e exige falha de domínio.
        Ele existe para garantir que toda certificação possua denominação identificável.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_certificacao(nome="   \t\n  ")

    def test_rejeita_organizacao_emissora_vazia(self) -> None:
        """Impede certificação cuja organização emissora esteja em branco.

        O cenário fornece string vazia para a instituição emissora e exige exceção.
        Ele existe para assegurar a presença obrigatória da entidade certificadora.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_certificacao(organizacao_emissora="   ")

    def test_rejeita_tipo_nao_textual_nos_campos(self) -> None:
        """Rejeita valores numéricos ou não textuais nos campos descritivos.

        O teste passa tipos inválidos em tempo de execução e verifica o disparo da exceção.
        Ele existe para manter a higienização contra dados corrompidos.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_certificacao(nome=123)  # type: ignore[arg-type]

        with self.assertRaises(RegraDeDominioViolada):
            self._criar_certificacao(organizacao_emissora=None)  # type: ignore[arg-type]

    def test_rejeita_caracteres_de_controle(self) -> None:
        """Impede a inclusão de caracteres de controle invisíveis nos campos.

        O cenário injeta o caractere de controle de quebra nula e espera rejeição.
        Ele existe para prevenir corrupção e vulnerabilidades de injeção em camadas externas.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_certificacao(nome="Certificado\x00Invalido")

    def test_rejeita_texto_acima_do_limite_maximo(self) -> None:
        """Impede que o nome ou o emissor ultrapassem 200 caracteres.

        O cenário fornece texto com 201 caracteres e valida a violação da regra de domínio.
        Ele existe para proteger os limites dimensionais do domínio e do banco de dados.
        """
        texto_longo = "A" * 201
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_certificacao(nome=texto_longo)

        with self.assertRaises(RegraDeDominioViolada):
            self._criar_certificacao(organizacao_emissora=texto_longo)

    def test_normalizadores_isolados(self) -> None:
        """Valida a execução direta das funções utilitárias puras de normalização.

        O teste chama normalizar_texto_certificacao e normalizar_chave_certificacao
        diretamente para comparar a saída canônica. Ele existe para garantir consistência
        no uso compartilhado entre domínio e camadas externas.
        """
        texto_limpo = normalizar_texto_certificacao("  Scrum Master  ", "nome")
        self.assertEqual(texto_limpo, "Scrum Master")

        chave = normalizar_chave_certificacao("  SCRUM   MASTER   PROFESSIONAL  ")
        self.assertEqual(chave, "scrum master professional")

    def _criar_certificacao(
        self,
        nome: str = "Certificação Python",
        organizacao_emissora: str = "Python Software Foundation",
    ) -> Certificacao:
        """Constrói uma certificação com identificadores válidos para os testes.

        O método encapsula a instanciação padrão determinística para isolar as
        asserções em cada regra específica. Ele existe para evitar redundância nos testes.
        """
        return Certificacao(
            id=CertificacaoId(UUID("70000000-0000-0000-0000-000000000001")),
            usuario_id=UsuarioId(UUID("70000000-0000-0000-0000-000000000002")),
            nome=nome,
            organizacao_emissora=organizacao_emissora,
        )
