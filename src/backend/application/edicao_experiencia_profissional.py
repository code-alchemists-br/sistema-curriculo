"""Orquestra a edição de experiências profissionais pelo próprio estudante.

O módulo localiza a experiência por identidade e proprietário, aplica os novos
dados pela entidade de domínio e solicita a atualização por uma porta, sem
conhecer transporte ou infraestrutura. Ele existe para que somente o dono altere
suas experiências e para que dados alheios nunca sejam revelados.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
from backend.application.data_gravacao_experiencia import obter_hoje_experiencia
from backend.application.ports import Relogio, RepositorioExperienciaProfissional
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import ExperienciaProfissionalId, Periodo, UsuarioId


class ExperienciaProfissionalNaoEncontrada(LookupError):
    """Sinaliza que a experiência não está disponível para o solicitante.

    A falha agrupa experiência inexistente, pertencente a outro estudante ou
    alterada concorrentemente sob a mesma mensagem. Ela existe para que a borda
    externa responda de forma uniforme sem revelar a existência de dados de
    terceiros.
    """


@dataclass(frozen=True, slots=True)
class EditarExperienciaProfissionalEntrada:
    """Agrupa identidade do solicitante, da experiência e seus novos dados.

    A entrada transporta usuário e experiência tipados, os textos informados e
    o ``Periodo`` já construído pelo domínio, sem tipos de HTTP ou
    persistência. Ela existe para explicitar o contrato de substituição completa
    consumido pelo caso de uso de edição.
    """

    usuario_id: UsuarioId
    experiencia_id: ExperienciaProfissionalId
    empresa: str
    cargo: str
    descricao: str
    periodo: Periodo


class EditarExperienciaProfissional:
    """Edita uma experiência própria e solicita a persistência do novo estado.

    O caso obtém a entidade pela combinação de ID e usuário, aplica os novos
    dados pelo método de domínio e atualiza somente quando a busca encontra uma
    experiência do solicitante. Ele existe para coordenar a edição com
    validação de proprietário sem acoplar a Application ao adapter.
    """

    # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
    def __init__(self, repositorio: RepositorioExperienciaProfissional, relogio: Relogio) -> None:
        """Recebe repositório e relógio para localizar, validar e atualizar.

        O construtor armazena uma abstração substituível por double e não
        inicia I/O. Ele existe para manter a orquestração independente da
        implementação concreta do repositório.
        """
        self._repositorio = repositorio
        self._relogio = relogio

    # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
    async def executar(
        self, entrada: EditarExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Aplica a edição e devolve a experiência atualizada.

        O método consulta por ID e proprietário, traduz ausência em falha
        uniforme, delega a validação do novo estado à entidade e solicita a
        atualização após resolver hoje uma vez em São Paulo e validar o estado
        completo pela entidade; uma atualização sem efeito
        também é tratada como não encontrada. Ele existe para impedir alteração
        de experiência alheia e persistência de estado inválido.
        """
        experiencia = await self._repositorio.obter_por_id_e_usuario(
            entrada.experiencia_id, entrada.usuario_id
        )
        if experiencia is None or experiencia.usuario_id != entrada.usuario_id:
            raise ExperienciaProfissionalNaoEncontrada(
                "Experiência profissional não encontrada."
            )

        hoje = obter_hoje_experiencia(self._relogio)
        experiencia_editada = experiencia.editar(
            empresa=entrada.empresa,
            cargo=entrada.cargo,
            descricao=entrada.descricao,
            periodo=entrada.periodo,
            hoje=hoje,
        )
        atualizada = await self._repositorio.atualizar(experiencia_editada)
        if not atualizada:
            raise ExperienciaProfissionalNaoEncontrada(
                "Experiência profissional não encontrada."
            )
        return experiencia_editada
