"""Orquestra a consulta e a exclusão de competências do estudante.

O módulo coordena a recuperação da coleção de competências e sua remoção física
utilizando portas assíncronas do repositório, garantindo validação de posse e
isolamento em relação ao transporte ou armazenamento. Ele existe para viabilizar
a reversibilidade e a visualização das competências na aplicação.
"""

from dataclasses import dataclass

from backend.application.cadastro_competencia import (
    CadastrarCompetencia,
    CadastrarCompetenciaEntrada,
    CompetenciaJaCadastrada,
)
from backend.application.ports import RepositorioCompetencia
from backend.domain.itens_perfil import Competencia
from backend.domain.value_objects import CompetenciaId, UsuarioId


class CompetenciaNaoEncontrada(LookupError):
    """Sinaliza que a competência não existe ou pertence a outro usuário.

    A exceção traduz tanto a ausência da linha no repositório quanto a tentativa
    de acesso a registro alheio sob uma mesma mensagem genérica. Ela existe para
    impedir vazamento de informações de propriedade entre estudantes.
    """


@dataclass(frozen=True, slots=True)
class ListarCompetenciasEntrada:
    """Transporta a identidade autenticada para listar competências próprias.

    O DTO empacota apenas o UsuarioId validado pela fronteira, sem tipos HTTP
    ou paginação externa. Ele existe para expressar a intenção pura de consulta
    das competências pertencentes ao estudante.
    """

    usuario_id: UsuarioId


class ListarCompetencias:
    """Recupera todas as competências cadastradas pelo estudante autenticado.

    O caso de uso recebe o comando tipado, invoca a porta de persistência para
    o proprietário informado e devolve a tupla de entidades do domínio. Ele
    existe para fornecer a lista completa de habilidades do estudante à API.
    """

    def __init__(self, repositorio: RepositorioCompetencia) -> None:
        """Armazena a porta de repositório necessária à consulta.

        O construtor recebe uma abstração substituível por double e não realiza
        I/O. Ele existe para manter a orquestração desacoplada de tecnologia.
        """
        self._repositorio = repositorio

    async def executar(
        self, entrada: ListarCompetenciasEntrada
    ) -> tuple[Competencia, ...]:
        """Executa a busca assíncrona das competências do estudante.

        Chama o repositório repassando o identificador do estudante e retorna
        as entidades encontradas sem aplicar filtros mutáveis. Ele existe para
        desacoplar a leitura de dados do formato de serialização de transporte.
        """
        return await self._repositorio.listar_por_usuario(entrada.usuario_id)


@dataclass(frozen=True, slots=True)
class ExcluirCompetenciaEntrada:
    """Transporta os identificadores necessários para remover uma competência.

    O DTO recebe a identidade da competência e a do usuário autenticado já
    resolvidos. Ele existe para garantir que a intenção de exclusão transporte
    apenas value objects válidos sem dependência de framework.
    """

    competencia_id: CompetenciaId
    usuario_id: UsuarioId


class ExcluirCompetencia:
    """Remove uma competência própria garantindo a validação de autoria.

    O caso de uso delega a exclusão ao repositório condicionando o comando ao
    ID da competência e ao proprietário autenticado. Caso o registro não exista
    ou seja de outro usuário, lança CompetenciaNaoEncontrada. Ele existe para
    garantir reversibilidade segura da adição de competências.
    """

    def __init__(self, repositorio: RepositorioCompetencia) -> None:
        """Armazena a porta de repositório usada para a operação de exclusão.

        O construtor retém a dependência abstrata sem abrir conexões. Ele
        existe para viabilizar testes unitários isolados com doubles.
        """
        self._repositorio = repositorio

    async def executar(self, entrada: ExcluirCompetenciaEntrada) -> None:
        """Solicita a remoção da competência e valida se a exclusão ocorreu.

        Invoca o método excluir() do repositório e verifica o sinal de sucesso;
        se falso, levanta CompetenciaNaoEncontrada. O método existe para impedir
        deleção silenciosa de IDs inexistentes ou de terceiros.
        """
        removido = await self._repositorio.excluir(
            entrada.competencia_id, entrada.usuario_id
        )
        if not removido:
            raise CompetenciaNaoEncontrada("Competência não encontrada.")


__all__ = [
    "CadastrarCompetencia",
    "CadastrarCompetenciaEntrada",
    "CompetenciaJaCadastrada",
    "CompetenciaNaoEncontrada",
    "ExcluirCompetencia",
    "ExcluirCompetenciaEntrada",
    "ListarCompetencias",
    "ListarCompetenciasEntrada",
]
