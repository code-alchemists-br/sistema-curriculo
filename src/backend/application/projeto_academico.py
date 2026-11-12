"""Coordena consulta, edição completa e exclusão lógica de projetos.

Os casos usam entidades e portas internas com IDs tipados, sem transporte ou
persistência concreta, para administrar projetos reutilizáveis do estudante.
"""

# Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
from dataclasses import dataclass

from backend.application.ports import Relogio, RepositorioProjetoAcademico
from backend.domain import ProjetoAcademico, ProjetoAcademicoId, UsuarioId


class ProjetoAcademicoNaoEncontrado(LookupError):
    """Indica ausência uniforme do projeto solicitado.

    Usa uma falha interna comum para ausente, alheio e excluído nas operações
    ativas, permitindo à borda tratar ausência sem revelar dados de terceiros.
    """


@dataclass(frozen=True, slots=True)
class ConsultarProjetoAcademicoEntrada:
    """Identifica o detalhe próprio que deve ser consultado.

    Transporta IDs tipados de projeto e usuário sem HTTP, para explicitar a
    consulta de um único projeto ativo pela porta interna.
    """

    usuario_id: UsuarioId
    projeto_id: ProjetoAcademicoId


@dataclass(frozen=True, slots=True)
class EditarProjetoAcademicoEntrada:
    """Agrupa IDs e os três textos da substituição completa do projeto.

    Conserva dados primitivos e identidades tipadas sem transporte, para que
    o caso de uso delegue à entidade a validação do novo estado completo.
    """

    usuario_id: UsuarioId
    projeto_id: ProjetoAcademicoId
    titulo: str
    descricao: str
    tecnologias: str


@dataclass(frozen=True, slots=True)
class ExcluirProjetoAcademicoEntrada:
    """Identifica o projeto próprio a excluir logicamente.

    Agrupa somente IDs tipados sem detalhes de transporte, para expressar a
    intenção de exclusão e deixar o instante a cargo da porta de relógio.
    """

    usuario_id: UsuarioId
    projeto_id: ProjetoAcademicoId


class ConsultarProjetoAcademico:
    """Obtém o detalhe de um projeto próprio ativo pela porta interna.

    Consulta por ID e usuário e traduz ausência em falha uniforme, para
    oferecer leitura sem acoplar a Application ao armazenamento.
    """

    def __init__(self, repositorio: RepositorioProjetoAcademico) -> None:
        """Guarda a porta de consulta recebida sem iniciar I/O.

        Conserva a abstração injetada para permitir leitura independente de
        tecnologia e testes determinísticos com doubles.
        """
        self._repositorio = repositorio

    async def executar(self, entrada: ConsultarProjetoAcademicoEntrada) -> ProjetoAcademico:
        """Devolve o projeto ativo ou informa ausência uniforme.

        Busca pelos dois IDs e confirma dono e estado, para não devolver
        projetos alheios ou excluídos mesmo diante de uma porta inconsistente.
        """
        projeto = await self._repositorio.obter_por_id_e_usuario(
            entrada.projeto_id, entrada.usuario_id
        )
        if projeto is None or projeto.usuario_id != entrada.usuario_id or projeto.excluido:
            raise ProjetoAcademicoNaoEncontrado("Projeto acadêmico não encontrado.")
        return projeto


class EditarProjetoAcademico:
    """Substitui textos de um projeto próprio ativo e persiste o novo estado.

    Busca pela porta, aplica invariantes na entidade e solicita atualização
    condicional, para impedir escrita inválida ou ressurreição concorrente.
    """

    def __init__(self, repositorio: RepositorioProjetoAcademico) -> None:
        """Guarda a porta usada para ler e atualizar sem iniciar I/O.

        Recebe uma abstração interna para manter a orquestração isolável e
        independente do adapter concreto de armazenamento.
        """
        self._repositorio = repositorio

    async def executar(self, entrada: EditarProjetoAcademicoEntrada) -> ProjetoAcademico:
        """Valida os três textos e devolve o projeto atualizado.

        Obtém somente projeto ativo, edita pela entidade e traduz atualização
        sem efeito em ausência, para preservar invariantes e concorrência.
        """
        projeto = await self._repositorio.obter_por_id_e_usuario(
            entrada.projeto_id, entrada.usuario_id
        )
        if projeto is None or projeto.usuario_id != entrada.usuario_id or projeto.excluido:
            raise ProjetoAcademicoNaoEncontrado("Projeto acadêmico não encontrado.")
        editado = projeto.editar(entrada.titulo, entrada.descricao, entrada.tecnologias)
        if not await self._repositorio.atualizar(editado):
            raise ProjetoAcademicoNaoEncontrado("Projeto acadêmico não encontrado.")
        return editado


class ExcluirProjetoAcademico:
    """Exclui logicamente projeto próprio com repetição idempotente.

    Lê inclusive excluídos, usa relógio só na primeira transição e relê após
    disputa, para preservar o primeiro instante sem alterar seleções de currículo.
    """

    def __init__(self, repositorio: RepositorioProjetoAcademico, relogio: Relogio) -> None:
        """Guarda as portas de projeto e relógio sem executar recursos externos.

        Recebe abstrações substituíveis por doubles para tornar exclusão e
        disputa concorrente independentes de banco e tempo real.
        """
        self._repositorio = repositorio
        self._relogio = relogio

    async def executar(self, entrada: ExcluirProjetoAcademicoEntrada) -> ProjetoAcademico:
        """Exclui o projeto ou devolve o estado já excluído do mesmo dono.

        Marca apenas ativo, relê se a escrita perder a disputa e exige um
        tombstone próprio na releitura, para preservar idempotência sem
        confundir falha concorrente com exclusão bem-sucedida.
        """
        projeto = await self._repositorio.obter_por_id_e_usuario_incluindo_excluidas(
            entrada.projeto_id, entrada.usuario_id
        )
        if projeto is None or projeto.usuario_id != entrada.usuario_id:
            raise ProjetoAcademicoNaoEncontrado("Projeto acadêmico não encontrado.")
        if projeto.excluido:
            return projeto
        instante = self._relogio.agora()
        excluido = projeto.excluir(instante)
        if await self._repositorio.marcar_excluida(
            entrada.projeto_id, entrada.usuario_id, instante
        ):
            return excluido
        recarregado = await self._repositorio.obter_por_id_e_usuario_incluindo_excluidas(
            entrada.projeto_id, entrada.usuario_id
        )
        if (
            recarregado is None
            or recarregado.usuario_id != entrada.usuario_id
            or not recarregado.excluido
        ):
            raise ProjetoAcademicoNaoEncontrado("Projeto acadêmico não encontrado.")
        return recarregado
