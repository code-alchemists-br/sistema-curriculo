"""Orquestra a exportação de uma versão de currículo para um formato de arquivo.

O módulo encadeia a prévia da versão (que garante a propriedade), a montagem do
documento renderizado e o gerador de arquivo do formato escolhido, devolvendo
os bytes com nome e tipo MIME prontos para download. Ele existe para atender ao
RF09 e ao CT-RF09-05 sem que a API conheça regras de conteúdo ou bibliotecas de
formato.
"""

from dataclasses import dataclass

from backend.application.documento_renderizado import (
    RenderizadorDocumentoCurriculo,
    montar_documento_renderizado,
)
from backend.application.previa_versao_curriculo import (
    GerarPreviaVersaoCurriculoEntrada,
)
from backend.application.revisao_versao_curriculo import GeradorDePrevia
from backend.domain.value_objects import CurriculoId, UsuarioId


@dataclass(frozen=True, slots=True)
class FormatoExportacao:
    """Descreve um formato de arquivo de exportação pela extensão e pelo tipo MIME.

    O DTO guarda a extensão sem ponto e o tipo MIME oficial do formato. Ele
    existe para que nome e cabeçalho do download venham da composição, e não de
    textos espalhados pela API.
    """

    extensao: str
    tipo_mime: str


FORMATO_DOCX = FormatoExportacao(
    extensao="docx",
    tipo_mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)


@dataclass(frozen=True, slots=True)
class ExportarCurriculoEntrada:
    """Agrupa o estudante solicitante e a versão de currículo a exportar.

    A entrada transporta apenas identidades tipadas já resolvidas pela
    fronteira. Ela existe para que somente o currículo escolhido seja exportado
    (CT-RF15-01).
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId


@dataclass(frozen=True, slots=True)
class ArquivoCurriculoExportado:
    """Representa o arquivo gerado, pronto para ser devolvido como download.

    O DTO contém os bytes, o nome com extensão e o tipo MIME do formato. Ele
    existe para que a fronteira HTTP apenas copie esses valores para a
    resposta.
    """

    conteudo: bytes
    nome_arquivo: str
    tipo_mime: str


class FalhaGeracaoArquivoCurriculo(RuntimeError):
    """Sinaliza que o arquivo do currículo não pôde ser gerado.

    A falha encapsula qualquer erro do gerador de arquivo, sem expor detalhes
    da biblioteca. Ela existe para que a interface informe o problema e permita
    nova tentativa, sem entregar arquivo inválido (CT-RF09-05).
    """


class ExportarCurriculo:
    """Exporta uma versão de currículo do próprio estudante em um formato de arquivo.

    O caso de uso gera a prévia (propagando ``CurriculoNaoEncontrado`` para
    versão ausente ou alheia), monta o documento renderizado, chama o gerador
    do formato e devolve bytes, nome e tipo MIME; erros do gerador viram
    ``FalhaGeracaoArquivoCurriculo``. Ele existe para coordenar a exportação
    com as mesmas garantias da visualização.
    """

    def __init__(
        self,
        gerador_previa: GeradorDePrevia,
        renderizador: RenderizadorDocumentoCurriculo,
        formato: FormatoExportacao,
    ) -> None:
        """Recebe a prévia, o gerador de arquivo e o formato correspondente.

        O construtor guarda abstrações substituíveis por doubles. Ele existe
        para que a mesma orquestração sirva a DOCX, PDF ou outros formatos
        apenas mudando a composição.
        """
        self._gerador_previa = gerador_previa
        self._renderizador = renderizador
        self._formato = formato

    async def executar(self, entrada: ExportarCurriculoEntrada) -> ArquivoCurriculoExportado:
        """Gera o arquivo da versão solicitada e o devolve com nome e tipo.

        O método obtém a prévia filtrada por proprietário, converte-a no
        documento renderizado e gera os bytes; qualquer falha do gerador é
        convertida em ``FalhaGeracaoArquivoCurriculo`` sem devolver conteúdo
        parcial. Ele existe para entregar à API um arquivo pronto e válido.
        """
        previa = await self._gerador_previa.executar(
            GerarPreviaVersaoCurriculoEntrada(
                usuario_id=entrada.usuario_id, curriculo_id=entrada.curriculo_id
            )
        )
        documento = montar_documento_renderizado(previa)
        try:
            conteudo = self._renderizador.renderizar(documento)
        except Exception as erro:
            raise FalhaGeracaoArquivoCurriculo(
                "Não foi possível gerar o arquivo do currículo."
            ) from erro
        if not conteudo:
            raise FalhaGeracaoArquivoCurriculo(
                "Não foi possível gerar o arquivo do currículo."
            )
        return ArquivoCurriculoExportado(
            conteudo=conteudo,
            nome_arquivo=f"{documento.nome_arquivo_base}.{self._formato.extensao}",
            tipo_mime=self._formato.tipo_mime,
        )
