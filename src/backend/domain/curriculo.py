"""Define o aggregate root que compõe uma versão de currículo.

O agregado mantém somente referências tipadas aos itens do perfil e protege sua
coleção contra duplicidade. Ele existe para preservar consistência local sem
carregar outros agregados ou representar tabelas de associação no domínio.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.value_objects import CurriculoId, ReferenciaCurriculo, UsuarioId


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(slots=True)
class Curriculo:
    """Representa o aggregate root de uma versão de currículo de um usuário.

    O agregado recebe identidade e proprietário obrigatórios, mantém título,
    layout e visibilidade sem impor vocabulários não definidos, e encapsula as
    referências selecionadas. Ele existe para concentrar regras locais de
    inclusão sem conhecer persistência ou validar propriedade transagregados.
    """

    id: CurriculoId
    usuario_id: UsuarioId
    titulo_versao: str
    layout: str
    is_public: bool
    _referencias: set[ReferenciaCurriculo] = field(
        default_factory=set,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        """Valida os dados locais indispensáveis para existir uma versão de currículo.

        O método exige título não vazio e uma flag booleana, deixando layout como
        texto porque seus valores ainda não foram definidos. Ele existe para que
        o agregado não seja construído com uma versão anônima ou ambígua.
        """
        if not self.titulo_versao.strip():
            raise RegraDeDominioViolada("Título da versão do currículo não pode ser vazio.")
        if not isinstance(self.is_public, bool):
            raise RegraDeDominioViolada("Visibilidade do currículo deve ser booleana.")

    @property
    def referencias(self) -> frozenset[ReferenciaCurriculo]:
        """Expõe uma visão imutável das referências incluídas no currículo.

        A propriedade cria um ``frozenset`` a partir da coleção interna, em vez
        de devolver a coleção mutável do agregado. Ela existe para impedir que
        consumidores contornem a regra de não duplicidade definida por
        ``incluir_referencia`` e ``remover_referencia``.
        """
        return frozenset(self._referencias)

    def incluir_referencia(self, referencia: ReferenciaCurriculo) -> None:
        """Inclui uma referência tipada caso ela ainda não componha o currículo.

        O método verifica a coleção interna antes de adicionar a referência e
        rejeita repetição do mesmo tipo e identificador. Ele existe para manter
        a consistência local do agregado sem consultar outros agregados.
        """
        if referencia in self._referencias:
            raise RegraDeDominioViolada("Item já está incluído no currículo.")
        self._referencias.add(referencia)

    def remover_referencia(self, referencia: ReferenciaCurriculo) -> None:
        """Remove uma referência existente da versão de currículo.

        O método exige que a referência esteja presente antes de removê-la e
        sinaliza uma falha de domínio quando não está. Ele existe para tornar
        explícita a alteração da composição do agregado, sem definir a política
        de exclusão do item de perfil original.
        """
        if referencia not in self._referencias:
            raise RegraDeDominioViolada("Item não está incluído no currículo.")
        self._referencias.remove(referencia)
