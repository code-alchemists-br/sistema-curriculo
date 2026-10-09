"""Orquestra a listagem das versões de currículo de um estudante.

O módulo consulta as versões do proprietário por porta, descarta qualquer uma
que não lhe pertença e as devolve em ordem determinística, sem conhecer HTTP ou
persistência. Ele existe para concentrar a intenção de listar as versões, e a
garantia de que só as do solicitante aparecem, fora de controllers e adapters.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
from backend.application.ports import RepositorioCurriculo
from backend.domain.curriculo import Curriculo
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
@dataclass(frozen=True, slots=True)
class ListarVersoesCurriculoEntrada:
    """Agrupa a identidade do estudante cujas versões de currículo são pedidas.

    A entrada transporta somente o tipo de domínio do proprietário, independente
    de HTTP. Ela existe para dar contrato explícito ao caso de uso e para
    permitir que ele cresça com filtros ou paginação sem mudar a assinatura.
    """

    usuario_id: UsuarioId


# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
class ListarVersoesCurriculo:
    """Lista as versões de currículo de um estudante, sem alterar nenhum estado.

    O caso consulta as versões do proprietário por porta, mantém somente as que
    pertencem ao solicitante e as ordena por título e identificador. Ele existe
    para que o estudante escolha entre suas versões sem que a versão de outro
    estudante possa aparecer, mesmo que o adapter a devolva por engano.
    """

    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    def __init__(self, repositorio_curriculo: RepositorioCurriculo) -> None:
        """Recebe a porta usada para consultar as versões do estudante.

        O construtor armazena somente a abstração interna, que será usada
        durante a execução e pode ser substituída por double. Ele existe para
        manter a orquestração independente da infraestrutura.
        """
        self._repositorio_curriculo = repositorio_curriculo

    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    async def executar(self, entrada: ListarVersoesCurriculoEntrada) -> tuple[Curriculo, ...]:
        """Devolve as versões do solicitante em ordem determinística.

        O método consulta o repositório pelo proprietário, descarta qualquer
        versão cujo dono seja outro usuário e ordena o restante pelo título, sem
        diferenciar maiúsculas de minúsculas, usando o identificador como
        desempate. Estudante sem versões resulta em tupla vazia. Ele existe para
        impedir que dados alheios sejam listados e para que a mesma seleção sempre
        produza a mesma ordem, independentemente do armazenamento.
        """
        curriculos = await self._repositorio_curriculo.listar_por_usuario(entrada.usuario_id)
        proprios = (curriculo for curriculo in curriculos if curriculo.usuario_id == entrada.usuario_id)
        return tuple(sorted(proprios, key=lambda curriculo: (curriculo.titulo_versao.casefold(), str(curriculo.id.valor))))
