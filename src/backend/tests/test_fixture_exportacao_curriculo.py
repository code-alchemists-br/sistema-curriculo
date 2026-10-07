"""Testa a integridade, validade e determinismo da fixture de exportação de currículo."""

import unittest
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261006-215500-fixture-teste-exportacao-curriculo-v001.md#v001
from backend.domain.value_objects import ReferenciaCurriculo
from backend.tests.fixtures.curriculo_exportacao import (
    ID_CURRICULO_ESTAVEL,
    ID_EXPERIENCIA_ESTAVEL,
    ID_FORMACAO_ESTAVEL,
    ID_PROJETO_ESTAVEL,
    ID_USUARIO_ESTAVEL,
    CurriculoExportacaoFixture,
    obter_curriculo_exportacao_fixture,
)


class CurriculoExportacaoFixtureTestCase(unittest.TestCase):
    """Verifica se a fixture atende às invariantes de domínio e aos requisitos de exportação.

    A classe executa asserções sobre os dados estruturados da fixture sem acessar
    rede, persistência ou dependências externas. Ela existe para garantir que a base
    de testes de geração de arquivos (PDF e DOCX) seja consistente, completa e estável.
    """

    def test_obter_fixture_retorna_dados_completos_e_validos(self) -> None:
        """Confirma que todos os blocos do currículo estão instanciados e preenchidos.

        O teste inspeciona cada atributo da fixture garantindo dados não vazios e
        conformidade das entidades com as regras de negócio. Ele existe para evitar
        que futuros motores de exportação recebam dados ausentes ou inválidos.
        """
        fixture = obter_curriculo_exportacao_fixture()

        self.assertIsInstance(fixture, CurriculoExportacaoFixture)
        self.assertEqual(fixture.usuario.id, ID_USUARIO_ESTAVEL)
        self.assertEqual(fixture.usuario.nome.valor, "Ana Carolina da Silva")
        self.assertEqual(fixture.usuario.email.valor, "ana.silva@fatec.sp.gov.br")

        contato = fixture.usuario.dados_contato
        self.assertIsNotNone(contato)
        assert contato is not None
        self.assertTrue(contato.endereco.valor.strip())
        self.assertGreaterEqual(len(contato.telefones), 1)
        self.assertIsNotNone(contato.linkedin)

        self.assertEqual(fixture.curriculo.id, ID_CURRICULO_ESTAVEL)
        self.assertEqual(fixture.curriculo.usuario_id, ID_USUARIO_ESTAVEL)
        self.assertTrue(fixture.curriculo.is_public)

        self.assertEqual(fixture.formacao_academica.id, ID_FORMACAO_ESTAVEL)
        self.assertEqual(fixture.formacao_academica.usuario_id, ID_USUARIO_ESTAVEL)

        self.assertEqual(fixture.experiencia_profissional.id, ID_EXPERIENCIA_ESTAVEL)
        self.assertEqual(fixture.experiencia_profissional.usuario_id, ID_USUARIO_ESTAVEL)

        self.assertEqual(fixture.projeto_academico.id, ID_PROJETO_ESTAVEL)
        self.assertEqual(fixture.projeto_academico.usuario_id, ID_USUARIO_ESTAVEL)

        self.assertGreaterEqual(len(fixture.competencias), 2)
        self.assertGreaterEqual(len(fixture.idiomas), 2)

    def test_curriculo_contem_referencias_para_todos_os_itens(self) -> None:
        """Confirma que o aggregate root Curriculo referencia todos os itens do perfil.

        O teste extrai as referências contidas no agregado e verifica a presença
        explícita de formação, experiência, projeto, competências e idiomas. Ele
        existe para assegurar a consistência referencial entre os itens e a versão.
        """
        fixture = obter_curriculo_exportacao_fixture()
        referencias = fixture.curriculo.referencias

        self.assertIn(ReferenciaCurriculo(fixture.formacao_academica.id), referencias)
        self.assertIn(ReferenciaCurriculo(fixture.experiencia_profissional.id), referencias)
        self.assertIn(ReferenciaCurriculo(fixture.projeto_academico.id), referencias)

        for comp in fixture.competencias:
            self.assertIn(ReferenciaCurriculo(comp.id), referencias)

        for idioma in fixture.idiomas:
            self.assertIn(ReferenciaCurriculo(idioma.id), referencias)

    def test_fixture_e_deterministica_entre_chamadas(self) -> None:
        """Garante que sucessivas invocações da fábrica produzam valores e IDs idênticos.

        O teste compara duas instâncias geradas em momentos distintos e afere a
        identidade de seus UUIDs e dados textuais. Ele existe para evitar oscilações
        em testes de snapshot ou checagens de checksum de exportação.
        """
        fixture_a = obter_curriculo_exportacao_fixture()
        fixture_b = obter_curriculo_exportacao_fixture()

        self.assertEqual(fixture_a.usuario.id, fixture_b.usuario.id)
        self.assertEqual(fixture_a.curriculo.id, fixture_b.curriculo.id)
        self.assertEqual(fixture_a.formacao_academica.id, fixture_b.formacao_academica.id)
        self.assertEqual(
            fixture_a.experiencia_profissional.id,
            fixture_b.experiencia_profissional.id,
        )
        self.assertEqual(fixture_a.projeto_academico.id, fixture_b.projeto_academico.id)
        self.assertEqual(fixture_a.para_dicionario(), fixture_b.para_dicionario())

    def test_para_dicionario_serializa_estrutura_corretamente(self) -> None:
        """Verifica se a conversão para dicionário produz chaves e tipos primitivos esperados.

        O teste invoca ``para_dicionario`` e inspeciona a presença de seções principais
        e formatos textuais de datas e IDs. Ele existe para certificar que a estrutura
        está pronta para consumo direto por geradores de documentos (PDF/DOCX).
        """
        fixture = obter_curriculo_exportacao_fixture()
        dados = fixture.para_dicionario()

        self.assertIn("usuario", dados)
        self.assertIn("curriculo", dados)
        self.assertIn("formacao_academica", dados)
        self.assertIn("experiencia_profissional", dados)
        self.assertIn("projeto_academico", dados)
        self.assertIn("competencias", dados)
        self.assertIn("idiomas", dados)

        # Checa formatação serializável dos identificadores e datas
        self.assertIsInstance(UUID(dados["usuario"]["id"]), UUID)
        self.assertIsInstance(UUID(dados["curriculo"]["id"]), UUID)
        self.assertEqual(dados["curriculo"]["titulo_versao"], "Currículo de Estágio - Engenharia de Software")
        self.assertEqual(dados["curriculo"]["total_referencias"], 7)
        self.assertIn("Tiradentes", dados["usuario"]["dados_contato"]["endereco"])
