"""Testa o documento renderizado do currículo, independente do formato de exportação."""

import dataclasses
import json
import unittest
from dataclasses import FrozenInstanceError, replace
from datetime import date
from uuid import UUID

from backend.application import (
    BlocoDocumento,
    DocumentoCurriculoRenderizado,
    PreviaVersaoCurriculo,
    montar_documento_renderizado,
)
from backend.domain import (
    Documento,
    DocumentoId,
    FormacaoAcademica,
    FormacaoAcademicaId,
    NivelFormacaoAcademica,
    Periodo,
    StatusFormacaoAcademica,
)
from backend.domain.secao_curriculo import ORDEM_PADRAO_SECOES, SecaoCurriculo
from backend.tests.fixtures.curriculo_exportacao import (
    obter_curriculo_exportacao_fixture,
)

URL_ARMAZENAMENTO = "armazenamento/interno/documento-privado.pdf"


def _previa(documentos: tuple[Documento, ...] = ()) -> PreviaVersaoCurriculo:
    """Monta a prévia a partir da fixture estável de exportação.

    A função usa os itens da fixture como itens selecionados da versão e permite
    acrescentar documentos complementares. Ela existe para testar o documento
    renderizado com o mesmo conteúdo que a visualização exibiria.
    """
    fixture = obter_curriculo_exportacao_fixture()
    return PreviaVersaoCurriculo(
        usuario=fixture.usuario,
        curriculo=fixture.curriculo,
        formacoes=(fixture.formacao_academica,),
        experiencias=(fixture.experiencia_profissional,),
        projetos=(fixture.projeto_academico,),
        competencias=fixture.competencias,
        idiomas=fixture.idiomas,
        documentos=documentos,
    )


def _documento_complementar() -> Documento:
    """Cria um documento complementar com caminho de armazenamento sensível.

    A função usa identificadores fixos do estudante da fixture. Ela existe para
    verificar que o local de armazenamento nunca chega ao arquivo exportado.
    """
    fixture = obter_curriculo_exportacao_fixture()
    return Documento(
        id=DocumentoId(UUID("88888888-8888-4888-8888-888888888888")),
        usuario_id=fixture.usuario.id,
        nome_arquivo="certificado-ingles.pdf",
        tipo_arquivo="application/pdf",
        url_armazenamento=URL_ARMAZENAMENTO,
    )


def _textos(documento: DocumentoCurriculoRenderizado) -> str:
    """Serializa todos os textos do documento para buscas simples.

    A função converte o DTO em dicionário e depois em JSON. Ela existe para
    procurar dados que não podem aparecer em nenhum campo.
    """
    return json.dumps(dataclasses.asdict(documento), ensure_ascii=False, default=str)


class DocumentoRenderizadoTestCase(unittest.TestCase):
    """Verifica o conteúdo, a ordem e a neutralidade de formato do documento.

    Os cenários montam o documento a partir da prévia da fixture de exportação,
    sem banco, rede ou bibliotecas de arquivo. A classe existe para garantir que
    PDF e DOCX recebam o mesmo conteúdo da visualização (CT-RF09-03).
    """

    def setUp(self) -> None:
        """Monta o documento padrão a partir da prévia da fixture.

        O setup guarda prévia e documento para os cenários. Ele existe para
        reduzir repetição.
        """
        self.previa = _previa()
        self.documento = montar_documento_renderizado(self.previa)

    def test_cabecalho_traz_identificacao_e_contatos_do_estudante(self) -> None:
        """Copia nome, e-mail, telefones, endereço e links do estudante.

        O teste compara o cabeçalho com os dados da fixture. Ele existe para que
        o arquivo comece pela mesma identificação da prévia.
        """
        cabecalho = self.documento.cabecalho

        self.assertEqual(cabecalho.nome, "Ana Carolina da Silva")
        self.assertEqual(cabecalho.email, "ana.silva@fatec.sp.gov.br")
        self.assertEqual(cabecalho.telefones, ("(11) 98765-4321", "(11) 3322-1100"))
        self.assertEqual(
            cabecalho.endereco, "Avenida Tiradentes, 615 - Bom Retiro, São Paulo - SP"
        )
        self.assertEqual(cabecalho.linkedin, "https://linkedin.com/in/estudante-fatec")
        self.assertEqual(cabecalho.curriculo_lattes, "http://lattes.cnpq.br/1234567890123456")
        self.assertIsNone(cabecalho.cidade)

    def test_metadados_da_versao_e_nome_de_arquivo_seguro(self) -> None:
        """Expõe título, modelo e um nome-base de arquivo sem acentos nem espaços.

        O teste confere os metadados copiados da versão e o nome-base gerado.
        Ele existe para que o download tenha nome legível e portável.
        """
        self.assertEqual(
            self.documento.titulo_versao, "Currículo de Estágio - Engenharia de Software"
        )
        self.assertEqual(self.documento.modelo, "padrao_fatec")
        self.assertEqual(
            self.documento.nome_arquivo_base,
            "curriculo-ana-carolina-da-silva-curriculo-de-estagio-engenharia-de-software",
        )

    def test_conteudo_corresponde_aos_itens_da_previa(self) -> None:
        """Gera um bloco para cada item da prévia, sem incluir nem omitir itens.

        O teste compara a quantidade de blocos por seção com a prévia agrupada
        por seção. Ele existe para cobrir o CT-RF09-03: o arquivo mostra
        exatamente o conteúdo da visualização.
        """
        esperado = {secao: len(itens) for secao, itens in self.previa.itens_por_secao()}

        obtido = {secao.secao: len(secao.blocos) for secao in self.documento.secoes}

        self.assertEqual(obtido, esperado)

    def test_blocos_formatam_textos_de_cada_tipo_de_item(self) -> None:
        """Converte cada tipo de item em textos legíveis e prontos para exibir.

        O teste confere formação, experiência, projeto, competência e idioma da
        fixture, inclusive rótulos de nível e situação e períodos. Ele existe
        para que os formatos não precisem repetir regras de formatação.
        """
        blocos = {secao.secao: secao.blocos for secao in self.documento.secoes}

        self.assertEqual(
            blocos[SecaoCurriculo.FORMACAO_ACADEMICA][0],
            BlocoDocumento(
                titulo="Tecnologia em Análise e Desenvolvimento de Sistemas",
                subtitulo="Faculdade de Tecnologia de São Paulo (FATEC-SP) - Tecnólogo",
                periodo="02/2023 - previsão 12/2025",
                detalhes=("Situação: Em andamento",),
            ),
        )
        experiencia = blocos[SecaoCurriculo.EXPERIENCIAS_PROFISSIONAIS][0]
        self.assertEqual(experiencia.titulo, "Estagiária de Desenvolvimento de Software")
        self.assertEqual(experiencia.subtitulo, "Empresa de Soluções Tecnológicas Ltda")
        self.assertEqual(experiencia.periodo, "01/2024 - atual")
        projeto = blocos[SecaoCurriculo.PROJETOS_ACADEMICOS][0]
        self.assertEqual(projeto.titulo, "Sistema de Apoio Curricular Profissional")
        self.assertEqual(
            projeto.detalhes[1], "Tecnologias: Python, FastAPI, TypeScript, React, PostgreSQL, Nix"
        )
        self.assertEqual(
            blocos[SecaoCurriculo.COMPETENCIAS][0],
            BlocoDocumento(titulo="Python e Clean Architecture", subtitulo="Técnica - Avançado"),
        )
        self.assertEqual(
            blocos[SecaoCurriculo.IDIOMAS][0],
            BlocoDocumento(titulo="Inglês", subtitulo="Avançado"),
        )

    def test_periodos_de_formacao_concluida_e_interrompida(self) -> None:
        """Mostra o término real para concluída e só o início sem término.

        O teste troca a formação da prévia por uma concluída e por uma
        interrompida sem data final. Ele existe para que a previsão de término
        só apareça em formações em andamento.
        """
        fixture = obter_curriculo_exportacao_fixture()
        concluida = replace(
            fixture.formacao_academica,
            status=StatusFormacaoAcademica.CONCLUIDO,
            periodo=Periodo(date(2019, 2, 1), date(2022, 12, 1)),
        )
        interrompida = FormacaoAcademica(
            id=FormacaoAcademicaId(UUID("33333333-3333-4333-8333-333333333334")),
            usuario_id=fixture.usuario.id,
            instituicao="ETEC",
            curso="Técnico em Informática",
            nivel=NivelFormacaoAcademica.TECNICO,
            periodo=Periodo(date(2018, 2, 1)),
            status=StatusFormacaoAcademica.INTERROMPIDO,
        )

        documento = montar_documento_renderizado(
            replace(self.previa, formacoes=(concluida, interrompida))
        )

        formacoes = documento.secoes[0].blocos
        self.assertEqual(formacoes[0].periodo, "02/2019 - 12/2022")
        self.assertEqual(formacoes[0].detalhes, ("Situação: Concluído",))
        self.assertEqual(formacoes[1].periodo, "02/2018")
        self.assertEqual(formacoes[1].detalhes, ("Situação: Interrompido",))

    def test_secoes_seguem_a_ordem_definida_pelo_estudante(self) -> None:
        """Respeita a ordem de seções escolhida na versão, e não a ordem padrão.

        O teste inverte a ordem das seções na versão e confere a sequência das
        seções do documento. Ele existe para que o arquivo siga a organização
        definida pelo estudante (RF05).
        """
        ordem = tuple(reversed(ORDEM_PADRAO_SECOES))
        self.previa.curriculo.definir_ordem_secoes(ordem)

        documento = montar_documento_renderizado(self.previa)

        self.assertEqual(
            [secao.secao for secao in documento.secoes],
            [
                SecaoCurriculo.IDIOMAS,
                SecaoCurriculo.COMPETENCIAS,
                SecaoCurriculo.PROJETOS_ACADEMICOS,
                SecaoCurriculo.EXPERIENCIAS_PROFISSIONAIS,
                SecaoCurriculo.FORMACAO_ACADEMICA,
            ],
        )

    def test_secoes_sem_itens_e_dados_pessoais_ficam_de_fora(self) -> None:
        """Omite seções vazias e não cria seção para os dados pessoais.

        A fixture não tem documentos complementares e os dados pessoais viram
        o cabeçalho. O teste existe para que o arquivo não mostre títulos de
        seções vazias.
        """
        secoes = [secao.secao for secao in self.documento.secoes]

        self.assertNotIn(SecaoCurriculo.DOCUMENTOS_COMPLEMENTARES, secoes)
        self.assertNotIn(SecaoCurriculo.DADOS_PESSOAIS, secoes)
        self.assertEqual(
            [secao.titulo for secao in self.documento.secoes],
            [
                "Formação acadêmica",
                "Experiência profissional",
                "Projetos acadêmicos",
                "Competências",
                "Idiomas",
            ],
        )

    def test_nao_expoe_dados_internos_ou_sensiveis(self) -> None:
        """Mantém fora do documento identificadores, hash de senha e armazenamento.

        O teste inclui um documento complementar e procura, em todos os textos,
        IDs, hash e o caminho de armazenamento. Ele existe para que o arquivo
        exportado não revele dados internos.
        """
        documento = montar_documento_renderizado(_previa((_documento_complementar(),)))
        textos = _textos(documento)
        fixture = obter_curriculo_exportacao_fixture()

        self.assertIn("certificado-ingles.pdf", textos)
        self.assertNotIn(URL_ARMAZENAMENTO, textos)
        self.assertNotIn(fixture.usuario.hash_senha.valor, textos)
        self.assertNotIn(str(fixture.usuario.id.valor), textos)
        self.assertNotIn(str(fixture.formacao_academica.id.valor), textos)

    def test_documento_e_independente_de_formato_e_imutavel(self) -> None:
        """Contém apenas textos e tuplas imutáveis, sem tipos de arquivo.

        O teste percorre o DTO procurando qualquer valor que não seja texto,
        tupla, enum de seção ou DTO, e tenta alterar um campo. Ele existe para
        que PDF e DOCX usem a mesma entrada sem depender de bibliotecas.
        """
        permitidos = (str, tuple, SecaoCurriculo, type(None))

        def verificar(valor: object) -> None:
            """Falha se encontrar um valor de tipo não permitido no DTO."""
            if dataclasses.is_dataclass(valor):
                for campo in dataclasses.fields(valor):
                    verificar(getattr(valor, campo.name))
            elif isinstance(valor, tuple):
                for item in valor:
                    verificar(item)
            else:
                self.assertIsInstance(valor, permitidos)

        verificar(self.documento)
        with self.assertRaises(FrozenInstanceError):
            self.documento.titulo_versao = "Outro"  # type: ignore[misc]

    def test_mesma_previa_gera_o_mesmo_documento(self) -> None:
        """Produz documentos iguais a partir da mesma prévia.

        O teste monta o documento duas vezes e compara. Ele existe para que a
        exportação seja determinística e testável.
        """
        self.assertEqual(montar_documento_renderizado(self.previa), self.documento)
