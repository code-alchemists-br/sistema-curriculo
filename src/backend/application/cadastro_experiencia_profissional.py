"""Orquestra o cadastro de experiências profissionais de estudantes.

O módulo transforma dados já tipados em uma entidade de domínio e a encaminha
por uma porta de persistência, sem depender de transporte ou infraestrutura.
Ele existe para concentrar o fluxo de criação reutilizável por futuras bordas
autenticadas da aplicação.
"""

# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
from backend.application.data_gravacao_experiencia import obter_hoje_experiencia
from backend.application.ports import (
    GeradorExperienciaProfissionalId,
    # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
    Relogio,
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
    # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
    def __init__(
        self,
        repositorio: RepositorioExperienciaProfissional,
        gerador_id: GeradorExperienciaProfissionalId,
        relogio: Relogio,
    ) -> None:
        """Recebe portas para gerar identidade, resolver hoje e salvar a experiência.

        O construtor armazena abstrações injetadas para que a execução dependa
        apenas de contratos internos e possa ser isolada em testes. Ele existe
        para inverter a dependência da orquestração em relação à infraestrutura.
        """
        self._repositorio = repositorio
        self._gerador_id = gerador_id
        self._relogio = relogio

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    # Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
    async def executar(
        self, entrada: CadastrarExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Cria uma experiência validada e solicita seu armazenamento.

        O método resolve hoje uma vez em São Paulo, gera a identidade e usa a
        fábrica validada antes de salvar para impedir datas futuras e textos
        fora dos limites sem consultar relógio no domínio.
        """
        hoje = obter_hoje_experiencia(self._relogio)
        experiencia = ExperienciaProfissional.criar_para_gravacao(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            empresa=entrada.empresa,
            cargo=entrada.cargo,
            descricao=entrada.descricao,
            periodo=entrada.periodo,
            hoje=hoje,
        )
        await self._repositorio.salvar(experiencia)
        return experiencia
