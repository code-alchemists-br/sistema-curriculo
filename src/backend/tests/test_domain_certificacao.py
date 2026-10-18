"""Testa invariantes e normalização da entidade de certificação e seu value object."""

import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
from backend.domain import (
    Certificacao,
    CertificacaoId,
    FormacaoAcademicaId,
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

    def test_aceita_textos_nos_limites_minimo_e_maximo(self) -> None:
        """Aceita nome e emissor com exatamente 1 e exatamente 200 caracteres.

        O cenário constrói certificações nos dois limites para cada campo e
        confere que o valor é preservado. Ele existe para que uma alteração de
        comparação nos limites seja detectada, já que o lado de rejeição sozinho
        não cobre a fronteira.
        """
        for tamanho in (1, 200):
            with self.subTest(tamanho=tamanho):
                texto = "A" * tamanho
                certificacao = self._criar_certificacao(
                    nome=texto, organizacao_emissora=texto
                )
                self.assertEqual(certificacao.nome, texto)
                self.assertEqual(certificacao.organizacao_emissora, texto)

    def test_limite_e_medido_depois_de_aparar_espacos(self) -> None:
        """Aceita 200 caracteres úteis mesmo com espaços externos excedentes.

        O cenário envolve um texto de 200 caracteres em espaços laterais, que
        são removidos antes da medição. Ele existe para fixar que o limite vale
        para o conteúdo normalizado, e não para a entrada bruta.
        """
        texto = "A" * 200

        certificacao = self._criar_certificacao(nome=f"   {texto}   ")

        self.assertEqual(certificacao.nome, texto)

    def test_rejeita_caracteres_de_controle_na_organizacao_emissora(self) -> None:
        """Impede caracteres de controle também no campo do emissor.

        O cenário injeta um caractere nulo no emissor e espera rejeição. Ele
        existe para que a regra de higiene textual valha para os dois campos.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_certificacao(organizacao_emissora="Amazon\x00Web Services")

    def test_rejeita_quebra_de_linha_interna(self) -> None:
        """Impede quebra de linha no meio do nome da certificação.

        O cenário usa um texto válido nas pontas com ``\\n`` interno, que não é
        removido pelo aparo lateral. Ele existe para impedir que nomes
        multilinha cheguem à apresentação do currículo.
        """
        with self.assertRaises(RegraDeDominioViolada):
            self._criar_certificacao(nome="AWS\nCertified")

    def test_chave_normalizada_preserva_acentos(self) -> None:
        """Gera a mesma chave para variações de caixa sem perder acentuação.

        O cenário compara nomes em minúsculas e maiúsculas com "ç" e "ã". Ele
        existe para que a deduplicação não confunda palavras acentuadas com
        versões sem acento.
        """
        minuscula = self._criar_certificacao(nome="Certificação em Gestão")
        maiuscula = self._criar_certificacao(nome="CERTIFICAÇÃO EM GESTÃO")

        self.assertEqual(minuscula.nome_normalizado, "certificação em gestão")
        self.assertEqual(maiuscula.nome_normalizado, minuscula.nome_normalizado)

    def test_variacoes_de_caixa_e_espacos_produzem_as_mesmas_chaves(self) -> None:
        """Identifica como duplicadas certificações com escrita diferente.

        O cenário cria duas certificações cujo nome e emissor diferem apenas em
        caixa e espaços internos. Ele existe para sustentar a detecção de
        duplicidade usada pelo cadastro.
        """
        primeira = self._criar_certificacao(
            nome="Scrum Master", organizacao_emissora="Scrum Alliance"
        )
        segunda = self._criar_certificacao(
            nome="  scrum   MASTER ", organizacao_emissora="SCRUM   alliance"
        )

        self.assertEqual(
            (primeira.nome_normalizado, primeira.organizacao_emissora_normalizada),
            (segunda.nome_normalizado, segunda.organizacao_emissora_normalizada),
        )

    def test_entidade_e_imutavel(self) -> None:
        """Impede alterar os campos depois da construção.

        O cenário tenta atribuir um novo nome à certificação criada. Ele existe
        para garantir que as invariantes validadas na criação não sejam
        contornadas por mutação posterior.
        """
        certificacao = self._criar_certificacao()

        with self.assertRaises(FrozenInstanceError):
            certificacao.nome = "Outro nome"  # type: ignore[misc]

    def test_rejeita_identidade_de_outro_tipo(self) -> None:
        """Impede usar como identidade um ID de outro item ou um UUID cru.

        O cenário fornece um ``FormacaoAcademicaId`` e um ``UUID`` no lugar do
        ``CertificacaoId``. Ele existe para que uma certificação nunca seja
        criada com a identidade de outro tipo de item do perfil.
        """
        for identidade in (
            FormacaoAcademicaId(UUID("70000000-0000-0000-0000-000000000001")),
            UUID("70000000-0000-0000-0000-000000000001"),
        ):
            with self.subTest(identidade=type(identidade).__name__):
                with self.assertRaises(RegraDeDominioViolada):
                    self._criar_certificacao(id=identidade)  # type: ignore[arg-type]

    def test_rejeita_proprietario_ausente_ou_de_outro_tipo(self) -> None:
        """Impede certificação sem dono ou com dono não tipado.

        O cenário fornece ``None`` e um ``UUID`` cru no lugar do ``UsuarioId``.
        Ele existe para que toda certificação pertença a um estudante válido,
        base do isolamento de dados entre estudantes.
        """
        for proprietario in (None, UUID("70000000-0000-0000-0000-000000000002")):
            with self.subTest(proprietario=proprietario):
                with self.assertRaises(RegraDeDominioViolada):
                    self._criar_certificacao(usuario_id=proprietario)  # type: ignore[arg-type]

    def _criar_certificacao(self, **alteracoes: object) -> Certificacao:
        """Constrói uma certificação com identificadores válidos para os testes.

        O método parte de campos padrão determinísticos e permite substituir
        qualquer um deles por argumento nomeado, isolando as asserções em cada
        regra específica. Ele existe para evitar redundância nos testes.
        """
        campos: dict[str, object] = {
            "id": CertificacaoId(UUID("70000000-0000-0000-0000-000000000001")),
            "usuario_id": UsuarioId(UUID("70000000-0000-0000-0000-000000000002")),
            "nome": "Certificação Python",
            "organizacao_emissora": "Python Software Foundation",
        }
        campos.update(alteracoes)
        return Certificacao(**campos)  # type: ignore[arg-type]
