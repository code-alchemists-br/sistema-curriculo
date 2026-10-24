"""Testa o caso de uso de exportação de uma versão de currículo."""

import unittest

from backend.application import (
    FORMATO_DOCX,
    CurriculoNaoEncontrado,
    DocumentoCurriculoRenderizado,
    ExportarCurriculo,
    ExportarCurriculoEntrada,
    FalhaGeracaoArquivoCurriculo,
    GerarPreviaVersaoCurriculoEntrada,
    PreviaVersaoCurriculo,
)
from backend.tests.fixtures.curriculo_exportacao import (
    ID_CURRICULO_ESTAVEL,
    ID_USUARIO_ESTAVEL,
    obter_curriculo_exportacao_fixture,
)


def previa_da_fixture() -> PreviaVersaoCurriculo:
    """Monta a prévia a partir da fixture estável de exportação.

    A função usa os itens da fixture como itens selecionados da versão. Ela
    existe para exercitar a exportação com um currículo completo e fixo.
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
        documentos=(),
    )


class GeradorPreviaStub:
    """Substitui a prévia devolvendo a fixture ou sinalizando versão alheia.

    O double registra as entradas e, quando configurado, levanta
    ``CurriculoNaoEncontrado``. Ele existe para isolar a exportação da
    persistência e controlar a verificação de propriedade.
    """

    def __init__(self, nao_encontrada: bool = False) -> None:
        """Guarda o comportamento configurado e inicia o histórico.

        O construtor mantém apenas estado em memória. Ele existe para cada
        cenário escolher sucesso ou versão não encontrada.
        """
        self.nao_encontrada = nao_encontrada
        self.entradas: list[GerarPreviaVersaoCurriculoEntrada] = []

    async def executar(self, entrada: GerarPreviaVersaoCurriculoEntrada) -> PreviaVersaoCurriculo:
        """Registra a entrada e devolve a prévia ou levanta a falha.

        O método não acessa banco. Ele existe para reproduzir o contrato do caso
        de uso de prévia.
        """
        self.entradas.append(entrada)
        if self.nao_encontrada:
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")
        return previa_da_fixture()


class RenderizadorStub:
    """Substitui o gerador de arquivo devolvendo bytes fixos ou falhando.

    O double registra os documentos recebidos e pode levantar um erro ou
    devolver conteúdo vazio. Ele existe para testar a tradução de falhas sem
    biblioteca de formato.
    """

    def __init__(self, conteudo: bytes = b"ARQUIVO", erro: Exception | None = None) -> None:
        """Guarda o resultado configurado e inicia o histórico.

        O construtor mantém apenas estado em memória. Ele existe para cada
        cenário escolher sucesso, falha ou arquivo vazio.
        """
        self.conteudo = conteudo
        self.erro = erro
        self.documentos: list[DocumentoCurriculoRenderizado] = []

    def renderizar(self, documento: DocumentoCurriculoRenderizado) -> bytes:
        """Registra o documento e devolve os bytes ou levanta o erro.

        O método não gera arquivo real. Ele existe para observar o que o caso de
        uso entregou ao gerador.
        """
        self.documentos.append(documento)
        if self.erro is not None:
            raise self.erro
        return self.conteudo


ENTRADA = ExportarCurriculoEntrada(usuario_id=ID_USUARIO_ESTAVEL, curriculo_id=ID_CURRICULO_ESTAVEL)


class ExportarCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a orquestração da exportação de currículo com doubles.

    Os cenários controlam a prévia e o gerador de arquivo. A classe existe para
    proteger nome, tipo MIME, verificação de propriedade e falha controlada.
    """

    async def test_exporta_com_nome_e_tipo_mime_do_formato(self) -> None:
        """Devolve os bytes do gerador com o nome-base e a extensão do formato.

        O teste confere o arquivo devolvido e a entrada repassada à prévia. Ele
        existe para que o download tenha nome e tipo corretos.
        """
        previa = GeradorPreviaStub()
        renderizador = RenderizadorStub()

        arquivo = await ExportarCurriculo(previa, renderizador, FORMATO_DOCX).executar(ENTRADA)

        self.assertEqual(arquivo.conteudo, b"ARQUIVO")
        self.assertEqual(
            arquivo.nome_arquivo,
            "curriculo-ana-carolina-da-silva-curriculo-de-estagio-engenharia-de-software.docx",
        )
        self.assertEqual(
            arquivo.tipo_mime,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        self.assertEqual(
            previa.entradas,
            [GerarPreviaVersaoCurriculoEntrada(ID_USUARIO_ESTAVEL, ID_CURRICULO_ESTAVEL)],
        )
        self.assertEqual(renderizador.documentos[0].cabecalho.nome, "Ana Carolina da Silva")

    async def test_versao_alheia_ou_inexistente_nao_chama_o_gerador(self) -> None:
        """Propaga a versão não encontrada sem gerar arquivo.

        A prévia sinaliza ``CurriculoNaoEncontrado``. O teste existe para que
        nenhum arquivo seja gerado para versão de outro estudante (CT-RF15-01).
        """
        renderizador = RenderizadorStub()

        with self.assertRaises(CurriculoNaoEncontrado):
            await ExportarCurriculo(
                GeradorPreviaStub(nao_encontrada=True), renderizador, FORMATO_DOCX
            ).executar(ENTRADA)

        self.assertEqual(renderizador.documentos, [])

    async def test_falha_do_gerador_vira_falha_controlada(self) -> None:
        """Converte erro ou arquivo vazio do gerador em falha de geração.

        Os cenários simulam exceção da biblioteca e retorno vazio. O teste
        existe para nunca entregar arquivo inválido (CT-RF09-05).
        """
        for renderizador in (
            RenderizadorStub(erro=ValueError("falha interna da biblioteca")),
            RenderizadorStub(conteudo=b""),
        ):
            with self.subTest(erro=renderizador.erro):
                with self.assertRaises(FalhaGeracaoArquivoCurriculo):
                    await ExportarCurriculo(
                        GeradorPreviaStub(), renderizador, FORMATO_DOCX
                    ).executar(ENTRADA)
