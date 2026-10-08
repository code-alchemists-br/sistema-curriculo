"""Orquestra a prévia de uma versão de currículo de um estudante.

O módulo reúne a versão, o estudante e o conteúdo dos itens selecionados em um
modelo de leitura agrupado por seção, conferindo a propriedade de tudo o que
entra nele e sem conhecer HTTP ou persistência. Ele existe para concentrar a
intenção de visualizar o currículo antes da exportação fora de controllers e
adapters.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
from backend.application.ports import (
    ConsultaItemPerfil,
    RepositorioCurriculo,
    RepositorioUsuario,
)
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain.curriculo import Curriculo
from backend.domain.itens_perfil import (
    Competencia,
    Documento,
    ExperienciaProfissional,
    FormacaoAcademica,
    Idioma,
    ProjetoAcademico,
)
from backend.domain.usuario import Usuario
from backend.domain.value_objects import CurriculoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
@dataclass(frozen=True, slots=True)
class GerarPreviaVersaoCurriculoEntrada:
    """Agrupa a identidade do solicitante e da versão cuja prévia é pedida.

    A entrada transporta somente tipos de domínio, independentes de HTTP. Ela
    existe para dar contrato explícito ao caso de uso, mantendo juntos o usuário
    que pede e a versão que deseja visualizar.
    """

    usuario_id: UsuarioId
    curriculo_id: CurriculoId


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
@dataclass(frozen=True, slots=True)
class PreviaVersaoCurriculo:
    """Representa o conteúdo da versão pronto para apresentação, agrupado por seção.

    O modelo guarda o estudante, a versão e as entidades dos itens selecionados
    já filtradas e ordenadas em tuplas por tipo. Ele existe para entregar à
    interface um resultado determinístico, sem que ela precise conhecer portas
    de leitura nem decidir ordem ou propriedade.
    """

    usuario: Usuario
    curriculo: Curriculo
    formacoes: tuple[FormacaoAcademica, ...]
    experiencias: tuple[ExperienciaProfissional, ...]
    projetos: tuple[ProjetoAcademico, ...]
    competencias: tuple[Competencia, ...]
    idiomas: tuple[Idioma, ...]
    documentos: tuple[Documento, ...]


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class GerarPreviaVersaoCurriculo:
    """Gera a prévia de uma versão de currículo própria, sem alterar nenhum estado.

    O caso localiza a versão e o estudante, lê cada item referenciado por porta,
    descarta o que estiver ausente ou pertencer a outro usuário e ordena o
    resultado por seção. Ele existe para que o estudante confira o currículo
    antes de exportar sem que dados alheios possam aparecer.
    """

    # Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
    def __init__(
        self,
        repositorio_curriculo: RepositorioCurriculo,
        repositorio_usuario: RepositorioUsuario,
        consulta_item: ConsultaItemPerfil,
    ) -> None:
        """Recebe as portas usadas para ler a versão, o estudante e os itens.

        O construtor armazena somente abstrações internas, que serão usadas
        durante a execução e podem ser substituídas por doubles. Ele existe para
        manter a orquestração independente da infraestrutura.
        """
        self._repositorio_curriculo = repositorio_curriculo
        self._repositorio_usuario = repositorio_usuario
        self._consulta_item = consulta_item

    # Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
    async def executar(self, entrada: GerarPreviaVersaoCurriculoEntrada) -> PreviaVersaoCurriculo:
        """Monta a prévia da versão do solicitante e a devolve agrupada por seção.

        O método trata versão ausente, versão alheia e estudante ausente ou
        excluído como a mesma falha, antes de consultar qualquer item. Em
        seguida lê cada referência, mantém apenas o item existente que pertence
        ao solicitante e corresponde à referência pedida, e ordena cada seção.
        Ele existe para impedir que a prévia exiba dados de outro estudante e
        para que a mesma versão sempre produza a mesma saída.
        """
        curriculo = await self._repositorio_curriculo.obter_por_id(entrada.curriculo_id)
        if curriculo is None or curriculo.usuario_id != entrada.usuario_id:
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")

        usuario = await self._repositorio_usuario.obter_por_id(entrada.usuario_id)
        if usuario is None or usuario.excluido:
            raise CurriculoNaoEncontrado("Versão de currículo não encontrada.")

        itens = []
        for referencia in curriculo.referencias:
            item = await self._consulta_item.obter_item(referencia)
            if item is None or item.usuario_id != entrada.usuario_id or item.id != referencia.item_id:
                continue
            itens.append(item)

        return PreviaVersaoCurriculo(
            usuario=usuario,
            curriculo=curriculo,
            formacoes=_ordenar_por_periodo(item for item in itens if isinstance(item, FormacaoAcademica)),
            experiencias=_ordenar_por_periodo(item for item in itens if isinstance(item, ExperienciaProfissional)),
            projetos=_ordenar_por_texto((item for item in itens if isinstance(item, ProjetoAcademico)), "titulo"),
            competencias=_ordenar_por_texto((item for item in itens if isinstance(item, Competencia)), "descricao"),
            idiomas=_ordenar_por_texto((item for item in itens if isinstance(item, Idioma)), "idioma"),
            documentos=_ordenar_por_texto((item for item in itens if isinstance(item, Documento)), "nome_arquivo"),
        )


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
def _ordenar_por_periodo(itens):
    """Ordena itens com período do início mais recente para o mais antigo.

    A função usa a data de início do período como chave principal, em ordem
    decrescente, e o identificador como desempate estável. Ela existe para que
    formações e experiências apareçam sempre da mais recente para a mais antiga,
    independentemente da ordem do conjunto de referências.
    """
    return tuple(sorted(itens, key=lambda item: (-item.periodo.inicio.toordinal(), str(item.id.valor))))


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
def _ordenar_por_texto(itens, campo: str):
    """Ordena itens alfabeticamente por um campo de texto, sem diferenciar caixa.

    A função compara o campo indicado em minúsculas e usa o identificador como
    desempate estável. Ela existe para que projetos, competências, idiomas e
    documentos tenham ordem determinística, já que as referências formam um
    conjunto sem ordem.
    """
    return tuple(sorted(itens, key=lambda item: (getattr(item, campo).casefold(), str(item.id.valor))))
