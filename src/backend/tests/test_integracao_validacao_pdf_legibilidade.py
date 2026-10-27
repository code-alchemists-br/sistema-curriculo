# Proveniência: decision-analysis prompts/backend/20261026-082930-validacao-pdf-paginacao-v001.md#v001
"""Testes de integração para validação de legibilidade, geometria e paginação do PDF gerado."""

import io
import unittest
from dataclasses import replace
from typing import Any
from uuid import UUID

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4

from backend.api.exportacao_curriculo import (
    CAMINHO_EXPORTACAO_PDF,
)
from backend.api.factory import create_app
from backend.api.sessoes import COOKIE_SESSAO
from backend.application import (
    FORMATO_PDF,
    CurriculoNaoEncontrado,
    ExportarCurriculo,
    GerarPreviaVersaoCurriculoEntrada,
    PreviaVersaoCurriculo,
)
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.domain import Documento, DocumentoId
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.exportacao.renderizador_pdf import (
    ESTILO_CLASSICO,
    ESTILO_COMPACTO,
    SEPARADOR_CONTATOS,
    RenderizadorDocumentoCurriculoPdf,
)
from backend.tests.fixtures.curriculo_exportacao import (
    ID_CURRICULO_ESTAVEL,
    ID_USUARIO_ESTAVEL,
    obter_curriculo_exportacao_fixture,
)

CREDENCIAL_AUTENTICADA_PDF = "token-integracao-pdf-valido"
URL_ARMAZENAMENTO_PRIVADO_PDF = "armazenamento/interno/documentos/privado-segredo.pdf"


class AutenticadorSessaoIntegracaoPdfStub(AutenticadorSessao):
    """Autentica a credencial de teste para chamadas HTTP simuladas de download PDF.

    **O que faz:** Confere o token fornecido no cookie e retorna a identidade do estudante estável.
    **Como faz:** Realiza verificação de igualdade estrita sem dependência de banco de dados.
    **Qual finalidade atende:** Habilita a simulação do middleware de segurança no pipeline de exportação.
    """

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Devolve o UsuarioId se o token corresponder à credencial válida.

        **O que faz:** Autentica a sessão para o usuário padrão de teste.
        **Como faz:** Compara com `CREDENCIAL_AUTENTICADA_PDF`.
        **Qual finalidade atende:** Provê contexto seguro para o endpoint de exportação.
        """
        return ID_USUARIO_ESTAVEL if token == CREDENCIAL_AUTENTICADA_PDF else None


class GeradorPreviaPdfIntegracaoStub:
    """Monta a prévia de currículo para exportação em PDF nos múltiplos cenários de paginação.

    **O que faz:** Constrói e retorna a entidade `PreviaVersaoCurriculo` com dados padrão ou estendidos.
    **Como faz:** Utiliza a fixture oficial e pode replicar formações e experiências para provocar quebra de página controlada.
    **Qual finalidade atende:** Permite testar a integridade visual tanto em currículos de uma página quanto extensos.
    """

    def __init__(
        self,
        modelo: str = "classico",
        com_documento_sensivel: bool = False,
        extenso: bool = False,
    ) -> None:
        """Inicializa o stub de prévia com parâmetros de paginação e modelo.

        **O que faz:** Guarda as flags de configuração de teste.
        **Como faz:** Salva modelo, inclusão de documento sensível e flag de currículo extenso.
        **Qual finalidade atende:** Facilita a variação de cenários entre os testes unitários integrados.
        """
        self._modelo = modelo
        self._com_documento_sensivel = com_documento_sensivel
        self._extenso = extenso

    async def executar(
        self, entrada: GerarPreviaVersaoCurriculoEntrada
    ) -> PreviaVersaoCurriculo:
        """Gera a prévia correspondente aos parâmetros configurados.

        **O que faz:** Valida identidade e monta as seções com densidade de dados apropriada.
        **Como faz:** Checa `usuario_id` e `curriculo_id`, compondo formações e experiências extras quando `extenso=True`.
        **Qual finalidade atende:** Alimenta o renderizador ReportLab para avaliar a quebra de página.
        """
        if (entrada.usuario_id, entrada.curriculo_id) != (
            ID_USUARIO_ESTAVEL,
            ID_CURRICULO_ESTAVEL,
        ):
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")
        fixture = obter_curriculo_exportacao_fixture()
        documentos = ()
        if self._com_documento_sensivel:
            documentos = (
                Documento(
                    id=DocumentoId(UUID("66666666-6666-4666-6666-666666666666")),
                    usuario_id=fixture.usuario.id,
                    nome_arquivo="Certificado_Especializacao_Cloud.pdf",
                    tipo_arquivo="application/pdf",
                    url_armazenamento=URL_ARMAZENAMENTO_PRIVADO_PDF,
                ),
            )

        formacoes = (fixture.formacao_academica,)
        experiencias = (fixture.experiencia_profissional,)
        projetos = (fixture.projeto_academico,)

        if self._extenso:
            # Replica itens para gerar um currículo rico que naturalmente transpõe para a segunda página
            formacao_extra = replace(
                fixture.formacao_academica,
                curso="Especialização em Arquitetura de Software Distribuído",
                instituicao="Universidade de São Paulo (USP)",
            )
            exp_extra_1 = replace(
                fixture.experiencia_profissional,
                cargo="Engenheira de Software Frontend Pleno",
                empresa="Empresa Global de Soluções Digitais S/A",
                descricao="Atuação em desenvolvimento web escalável, design system, componentes acessíveis e testes integrados.",
            )
            exp_extra_2 = replace(
                fixture.experiencia_profissional,
                cargo="Desenvolvedora de Software Júnior",
                empresa="Startup de Tecnologia e Educação",
                descricao="Construção de APIs em Python e integração de dados cadastrais.",
            )
            formacoes = (fixture.formacao_academica, formacao_extra)
            experiencias = (fixture.experiencia_profissional, exp_extra_1, exp_extra_2)

        curriculo = replace(fixture.curriculo, layout=self._modelo)
        return PreviaVersaoCurriculo(
            usuario=fixture.usuario,
            curriculo=curriculo,
            formacoes=formacoes,
            experiencias=experiencias,
            projetos=projetos,
            competencias=fixture.competencias,
            idiomas=fixture.idiomas,
            documentos=documentos,
        )


def _criar_aplicacao_teste_pdf(
    modelo: str = "classico",
    com_documento_sensivel: bool = False,
    extenso: bool = False,
) -> object:
    """Cria a aplicação FastAPI com os executores reais de exportação em PDF.

    **O que faz:** Inicializa a aplicação injetando o caso de uso `ExportarCurriculo` configurado para PDF.
    **Como faz:** Instancia `RenderizadorDocumentoCurriculoPdf` real com o stub de prévia e monta o app.
    **Qual finalidade atende:** Garante que as requisições HTTP exercitem toda a cadeia do endpoint oficial.
    """
    gerador_previa = GeradorPreviaPdfIntegracaoStub(
        modelo=modelo, com_documento_sensivel=com_documento_sensivel, extenso=extenso
    )
    renderizador = RenderizadorDocumentoCurriculoPdf(invariante=True)
    caso_de_uso = ExportarCurriculo(gerador_previa, renderizador, FORMATO_PDF)
    return create_app(
        autenticador_sessao=AutenticadorSessaoIntegracaoPdfStub(),
        exportar_curriculo_pdf=caso_de_uso,  # type: ignore[arg-type]
    )


async def _executar_requisicao_get_pdf(
    app: object, caminho: str
) -> tuple[int, dict[str, str], bytes]:
    """Dispara uma requisição HTTP GET autenticada via interface ASGI.

    **O que faz:** Executa a chamada no endpoint e extrai status, headers e corpo de resposta.
    **Como faz:** Envia mensagem HTTP GET com cookie de sessão sintético para a função `app`.
    **Qual finalidade atende:** Permite auditar os bytes exatos devolvidos pela API de exportação.
    """
    headers = [(b"cookie", f"{COOKIE_SESSAO}={CREDENCIAL_AUTENTICADA_PDF}".encode())]
    escopo = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": caminho,
        "raw_path": caminho.encode(),
        "query_string": b"",
        "headers": headers,
        "client": ("127.0.0.1", 50000),
        "server": ("127.0.0.1", 80),
    }
    status = 0
    cabecalhos_resposta: dict[str, str] = {}
    partes: list[bytes] = []

    async def receber() -> dict[str, object]:
        """Entrega o corpo vazio da requisição GET."""
        return {"type": "http.request", "body": b"", "more_body": False}

    async def enviar(mensagem: dict[str, Any]) -> None:
        """Captura status, cabeçalhos e fragmentos do corpo da resposta."""
        nonlocal status
        if mensagem["type"] == "http.response.start":
            status = int(mensagem["status"])
            for nome, valor in mensagem.get("headers", []):
                cabecalhos_resposta[nome.decode("latin-1").lower()] = valor.decode(
                    "latin-1"
                )
        elif mensagem["type"] == "http.response.body":
            partes.append(mensagem.get("body", b""))

    await app(escopo, receber, enviar)  # type: ignore[operator]
    return status, cabecalhos_resposta, b"".join(partes)


class TesteIntegracaoValidacaoPdfLegibilidade(unittest.IsolatedAsyncioTestCase):
    """Testa a conformidade geométrica, paginação e legibilidade do PDF gerado (F11.12 / F1.5)."""

    async def test_geometria_a4_e_abertura_do_pdf_com_leitor_externo(self) -> None:
        """Valida que o arquivo PDF gerado abre normalmente e respeita rigorosamente as dimensões A4.

        **O que faz:** Dispara a rota de exportação, verifica headers e audita a geometria das páginas com `pypdf`.
        **Como faz:** Confere o cabeçalho `attachment`, a assinatura `%PDF-` e as dimensões de `mediabox`.
        **Qual finalidade atende:** Garante que o PDF possa ser aberto e impresso em formato padrão internacional A4.
        """
        app = _criar_aplicacao_teste_pdf(modelo="classico")
        caminho = CAMINHO_EXPORTACAO_PDF.format(
            usuario_id=ID_USUARIO_ESTAVEL.valor, curriculo_id=ID_CURRICULO_ESTAVEL.valor
        )

        status, cabecalhos, corpo = await _executar_requisicao_get_pdf(app, caminho)

        self.assertEqual(status, 200)
        self.assertEqual(cabecalhos["content-type"], "application/pdf")
        self.assertIn("attachment", cabecalhos["content-disposition"])
        self.assertEqual(cabecalhos["x-content-type-options"], "nosniff")
        self.assertEqual(cabecalhos["cache-control"], "private, no-store")

        # Assinatura de PDF válida
        self.assertTrue(corpo.startswith(b"%PDF-"))

        # Leitura com leitor externo e auditoria de dimensões da página A4 (595.27 x 841.89 pontos)
        reader = PdfReader(io.BytesIO(corpo))
        self.assertGreaterEqual(len(reader.pages), 1)

        largura_a4_pt, altura_a4_pt = A4
        for i, pagina in enumerate(reader.pages):
            largura = float(pagina.mediabox.width)
            altura = float(pagina.mediabox.height)
            self.assertAlmostEqual(
                largura,
                largura_a4_pt,
                places=1,
                msg=f"Página {i + 1} deve ter largura padrão A4 ({largura_a4_pt} pt)",
            )
            self.assertAlmostEqual(
                altura,
                altura_a4_pt,
                places=1,
                msg=f"Página {i + 1} deve ter altura padrão A4 ({altura_a4_pt} pt)",
            )

    async def test_auditoria_de_legibilidade_por_pagina_modelo_classico(self) -> None:
        """Audita o conteúdo da Página 1 garantindo legibilidade e presença de seções chave.

        **O que faz:** Extrai e avalia o texto da primeira página do Modelo Clássico.
        **Como faz:** Extrai texto por página e assegura que dados pessoais, contatos e seções iniciais estão contidos na folha.
        **Qual finalidade atende:** Comprova que os dados fundamentais do currículo não são fragmentados indevidamente.
        """
        app = _criar_aplicacao_teste_pdf(modelo="classico")
        caminho = CAMINHO_EXPORTACAO_PDF.format(
            usuario_id=ID_USUARIO_ESTAVEL.valor, curriculo_id=ID_CURRICULO_ESTAVEL.valor
        )

        status, _, corpo = await _executar_requisicao_get_pdf(app, caminho)
        self.assertEqual(status, 200)

        reader = PdfReader(io.BytesIO(corpo))
        pagina_1 = reader.pages[0]
        texto_pagina_1 = pagina_1.extract_text()

        # Identificação e contatos no topo
        self.assertIn("Ana Carolina da Silva", texto_pagina_1)
        self.assertIn("ana.silva@fatec.sp.gov.br", texto_pagina_1)
        self.assertIn(SEPARADOR_CONTATOS, texto_pagina_1)

        # Seções presentes na folha inicial
        self.assertIn("Formação acadêmica", texto_pagina_1)
        self.assertIn(
            "Tecnologia em Análise e Desenvolvimento de Sistemas", texto_pagina_1
        )
        self.assertIn("Experiência profissional", texto_pagina_1)
        self.assertIn("Estagiária de Desenvolvimento de Software", texto_pagina_1)

    async def test_auditoria_de_paginacao_em_curriculo_extenso_sem_titulos_orfaos(
        self,
    ) -> None:
        """Valida que em currículos extensos a transição para a Página 2 ocorre de forma limpa e sem títulos órfãos.

        **O que faz:** Exporta currículo com massa de dados volumosa e audita o fluxo sequencial entre as páginas.
        **Como faz:** Atesta que o documento gerado ocupa 2 páginas e que nenhuma seção fica isolada no rodapé sem seu primeiro bloco.
        **Qual finalidade atende:** Cumpre o critério de ausência de sobreposição e cortes de paginação do RNF07 / F11.12.
        """
        app = _criar_aplicacao_teste_pdf(modelo="classico", extenso=True)
        caminho = CAMINHO_EXPORTACAO_PDF.format(
            usuario_id=ID_USUARIO_ESTAVEL.valor, curriculo_id=ID_CURRICULO_ESTAVEL.valor
        )

        status, _, corpo = await _executar_requisicao_get_pdf(app, caminho)
        self.assertEqual(status, 200)

        reader = PdfReader(io.BytesIO(corpo))
        self.assertEqual(
            len(reader.pages),
            2,
            "Currículo extenso deve quebrar organizadamente em exatamente 2 páginas",
        )

        texto_pag_1 = reader.pages[0].extract_text()
        texto_pag_2 = reader.pages[1].extract_text()

        # Página 1 contém o cabeçalho, dados acadêmicos, experiências, projetos e competências
        self.assertIn("Ana Carolina da Silva", texto_pag_1)
        self.assertIn("Formação acadêmica", texto_pag_1)
        self.assertIn("Experiência profissional", texto_pag_1)
        self.assertIn("Projetos acadêmicos", texto_pag_1)
        self.assertIn("Competências", texto_pag_1)
        self.assertNotIn(
            "Idiomas", texto_pag_1, "Seção 'Idiomas' não deve ficar órfã na página 1"
        )

        # Página 2 contém a continuação do histórico: seção 'Idiomas' íntegra com títulos e descrições
        self.assertIn("Idiomas", texto_pag_2)
        self.assertIn("Inglês", texto_pag_2)
        self.assertIn("Espanhol", texto_pag_2)

        # Garantia de integridade: ambas as páginas contêm textos válidos e não vazios
        self.assertGreater(len(texto_pag_1.strip()), 100)
        self.assertGreater(len(texto_pag_2.strip()), 30)

    async def test_modelo_compacto_mantem_mesmo_texto_com_alta_densidade_e_margens_menores(
        self,
    ) -> None:
        """Comprova que o Modelo Compacto preserva 100% do conteúdo textual do clássico com margens reduzidas.

        **O que faz:** Gera os PDFs nos layouts clássico e compacto e compara o texto extraído de ponta a ponta.
        **Como faz:** Normaliza espaços e compara igualdade de strings, além de conferir as propriedades de margem.
        **Qual finalidade atende:** Garante fidelidade de conteúdo independente do template escolhido pelo estudante.
        """
        app_classico = _criar_aplicacao_teste_pdf(modelo="classico")
        app_compacto = _criar_aplicacao_teste_pdf(modelo="compacto")
        caminho = CAMINHO_EXPORTACAO_PDF.format(
            usuario_id=ID_USUARIO_ESTAVEL.valor, curriculo_id=ID_CURRICULO_ESTAVEL.valor
        )

        _, _, corpo_classico = await _executar_requisicao_get_pdf(app_classico, caminho)
        _, _, corpo_compacto = await _executar_requisicao_get_pdf(app_compacto, caminho)

        reader_classico = PdfReader(io.BytesIO(corpo_classico))
        reader_compacto = PdfReader(io.BytesIO(corpo_compacto))

        texto_classico = " ".join(
            " ".join(p.extract_text().split()) for p in reader_classico.pages
        )
        texto_compacto = " ".join(
            " ".join(p.extract_text().split()) for p in reader_compacto.pages
        )

        # O conteúdo textual extraído deve ser idêntico
        self.assertEqual(texto_classico, texto_compacto)

        # Margens do modelo clássico (2.0 cm) vs modelo compacto (1.5 cm)
        self.assertEqual(ESTILO_CLASSICO.margem_cm, 2.0)
        self.assertEqual(ESTILO_COMPACTO.margem_cm, 1.5)

    async def test_higienizacao_de_metadados_e_omissao_de_caminhos_privados(
        self,
    ) -> None:
        """Garante a privacidade dos dados do estudante e ausência de vazamento de URLs internas no PDF.

        **O que faz:** Gera o PDF contendo documento suplementar e audita o texto extraído e os metadados do leitor.
        **Como faz:** Procura o nome amigável do documento e assegura a ausência de caminhos confidenciais de storage.
        **Qual finalidade atende:** Cumpre as normas de privacidade e segurança da aplicação.
        """
        app = _criar_aplicacao_teste_pdf(com_documento_sensivel=True)
        caminho = CAMINHO_EXPORTACAO_PDF.format(
            usuario_id=ID_USUARIO_ESTAVEL.valor, curriculo_id=ID_CURRICULO_ESTAVEL.valor
        )

        status, _, corpo = await _executar_requisicao_get_pdf(app, caminho)
        self.assertEqual(status, 200)

        reader = PdfReader(io.BytesIO(corpo))
        texto_completo = " ".join(p.extract_text() for p in reader.pages)

        # 1. Nome amigável do documento deve estar visível
        self.assertIn("Certificado_Especializacao_Cloud.pdf", texto_completo)

        # 2. Caminho de armazenamento sensível NÃO deve constar no PDF
        self.assertNotIn(URL_ARMAZENAMENTO_PRIVADO_PDF, texto_completo)

        # 3. Metadados do PDF higienizados
        metadata = reader.metadata
        self.assertIsNotNone(metadata)
        if metadata:
            self.assertEqual(metadata.author or "", "")
            self.assertEqual(metadata.creator or "", "")


if __name__ == "__main__":
    unittest.main()
