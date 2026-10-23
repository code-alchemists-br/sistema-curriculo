"""Orquestra a consulta paginada das associações próprias de um estudante.

O módulo valida os parâmetros de página e delega a leitura do usuário e sua
ordenação ao port de associações. Ele existe para disponibilizar os agregados
de domínio sem acoplar a consulta a HTTP ou persistência.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md#v001
from backend.application.ports import RepositorioAssociacaoCurriculoVaga
from backend.domain.associacao_curriculo_vaga import AssociacaoCurriculoVaga
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md#v001
@dataclass(frozen=True, slots=True)
class ListarAssociacoesCurriculoVagaEntrada:
    """Agrupa o proprietário e os parâmetros da página solicitada.

    A entrada valida offset não negativo e limite inteiro positivo, sem impor
    teto de página não definido pelo projeto. Ela existe para manter os
    parâmetros internos válidos antes de consultar o repositório.
    """

    usuario_id: UsuarioId
    offset: int
    limit: int

    def __post_init__(self) -> None:
        """Rejeita parâmetros que não descrevem uma página válida.

        A validação exige inteiros estritos, offset não negativo e limite maior
        que zero, incluindo rejeição de bools apesar de serem subclasses de int.
        Ela existe para evitar consultas ambíguas ou inválidas ao repositório.
        """
        if type(self.offset) is not int or self.offset < 0:
            raise ValueError("offset deve ser um inteiro não negativo.")
        if type(self.limit) is not int or self.limit <= 0:
            raise ValueError("limit deve ser um inteiro positivo.")


# Proveniência: decision-analysis prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md#v001
class ListarAssociacoesCurriculoVaga:
    """Lista uma página das associações pertencentes a um estudante.

    O caso encaminha proprietário e parâmetros validados ao port, cuja consulta
    filtra antes de paginar e ordena pela chave composta. Ele existe para expor
    a intenção de leitura em Application e retornar agregados de domínio.
    """

    def __init__(self, repositorio: RepositorioAssociacaoCurriculoVaga) -> None:
        """Armazena a porta de consulta substituível por doubles.

        O construtor recebe somente a abstração interna necessária à leitura.
        Ele existe para manter a Application independente da persistência.
        """
        self._repositorio = repositorio

    async def executar(
        self, entrada: ListarAssociacoesCurriculoVagaEntrada
    ) -> tuple[AssociacaoCurriculoVaga, ...]:
        """Retorna os agregados da página do usuário solicitado.

        O método encaminha ao port o usuário e os parâmetros já validados,
        deixando a filtragem do proprietário e a paginação no mesmo pedido de
        persistência para garantir a ordem correta das operações.
        """
        return await self._repositorio.listar_por_usuario(
            entrada.usuario_id,
            offset=entrada.offset,
            limit=entrada.limit,
        )
