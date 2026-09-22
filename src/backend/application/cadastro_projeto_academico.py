"""Orquestra o cadastro de projetos acadêmicos de estudantes.

O módulo transforma dados já tipados em uma entidade de domínio e a encaminha
por uma porta de persistência, sem depender de transporte ou infraestrutura.
Ele existe para concentrar o fluxo reutilizável por futuras bordas autenticadas.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
from backend.application.ports import (
    GeradorProjetoAcademicoId,
    RepositorioProjetoAcademico,
)
from backend.domain.itens_perfil import ProjetoAcademico
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
@dataclass(frozen=True, slots=True)
class CadastrarProjetoAcademicoEntrada:
    """Agrupa os dados necessários para cadastrar um projeto acadêmico.

    A entrada conserva a identidade tipada do estudante e os textos informados,
    sem transportar tipos de HTTP. Ela existe para tornar explícito e testável
    o contrato interno do caso de uso.
    """

    usuario_id: UsuarioId
    titulo: str
    descricao: str
    tecnologias: str


# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
class CadastrarProjetoAcademico:
    """Cria e persiste um projeto acadêmico válido para um estudante.

    O caso de uso obtém uma identidade por porta, constrói a entidade para
    aplicar invariantes e a salva pelo repositório assíncrono. Ele existe para
    manter esse fluxo coeso e livre de dependências de API e banco de dados.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    def __init__(
        self,
        repositorio: RepositorioProjetoAcademico,
        gerador_id: GeradorProjetoAcademicoId,
    ) -> None:
        """Recebe as portas necessárias para gerar e salvar o projeto.

        O construtor armazena abstrações injetadas para que a execução dependa
        somente de contratos internos e possa ser isolada em testes. Ele existe
        para inverter a dependência em relação à infraestrutura.
        """
        self._repositorio = repositorio
        self._gerador_id = gerador_id

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    async def executar(
        self, entrada: CadastrarProjetoAcademicoEntrada
    ) -> ProjetoAcademico:
        """Cria um projeto validado e solicita seu armazenamento.

        O método gera a identidade tipada, delega as regras de texto à entidade
        e só chama o repositório após construção bem-sucedida. Ele existe para
        assegurar que somente projetos válidos sejam persistidos.
        """
        projeto = ProjetoAcademico(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            titulo=entrada.titulo,
            descricao=entrada.descricao,
            tecnologias=entrada.tecnologias,
        )
        await self._repositorio.salvar(projeto)
        return projeto
