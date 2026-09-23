"""Orquestra o cadastro de experiências profissionais de estudantes.

O módulo transforma dados já tipados em uma entidade de domínio e a encaminha
por uma porta de persistência, sem depender de transporte ou infraestrutura.
Ele existe para concentrar o fluxo de criação reutilizável por futuras bordas
autenticadas da aplicação.
"""

# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from dataclasses import dataclass

from backend.application.ports import (
    GeradorExperienciaProfissionalId,
    RepositorioExperienciaProfissional,
)
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import Periodo, UsuarioId


# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
@dataclass(frozen=True, slots=True)
class CadastrarExperienciaProfissionalEntrada:
    """Agrupa os dados necessários para cadastrar uma experiência profissional.

    A entrada conserva a identidade tipada do estudante, os textos informados
    e o período já construído pelo domínio, sem transportar tipos de HTTP. Ela
    existe para tornar explícito e testável o contrato do caso de uso interno.
    """

    usuario_id: UsuarioId
    empresa: str
    cargo: str
    descricao: str
    periodo: Periodo


# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
class CadastrarExperienciaProfissional:
    """Cria e persiste uma experiência profissional válida para um estudante.

    O caso de uso obtém uma identidade pela porta apropriada, constrói a
    entidade para aplicar suas invariantes e a salva pelo repositório
    assíncrono. Ele existe para manter o fluxo de cadastro coeso e livre de
    dependências de API, autorização e banco de dados.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def __init__(
        self,
        repositorio: RepositorioExperienciaProfissional,
        gerador_id: GeradorExperienciaProfissionalId,
    ) -> None:
        """Recebe as portas necessárias para gerar e salvar a experiência.

        O construtor armazena abstrações injetadas para que a execução dependa
        apenas de contratos internos e possa ser isolada em testes. Ele existe
        para inverter a dependência da orquestração em relação à infraestrutura.
        """
        self._repositorio = repositorio
        self._gerador_id = gerador_id

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    async def executar(
        self, entrada: CadastrarExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Cria uma experiência validada e solicita seu armazenamento.

        O método gera o identificador tipado, delega as regras dos textos à
        entidade e só chama o repositório após a construção bem-sucedida. Ele
        existe para assegurar que apenas experiências válidas sejam persistidas.
        """
        experiencia = ExperienciaProfissional(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            empresa=entrada.empresa,
            cargo=entrada.cargo,
            descricao=entrada.descricao,
            periodo=entrada.periodo,
        )
        await self._repositorio.salvar(experiencia)
        return experiencia
