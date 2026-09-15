"""Orquestra o cadastro interno de uma conta de estudante.

O módulo compõe value objects e o aggregate root ``Usuario`` por meio de portas
internas, sem receber dados de HTTP nem conhecer persistência. Ele existe para
proteger a unicidade de e-mail no fluxo de cadastro sem implementar login,
autenticação ou autorização.
"""

from dataclasses import dataclass

from backend.application.ports import GeradorUsuarioId, RepositorioUsuario
from backend.domain.entities import Usuario
from backend.domain.value_objects import Email, HashSenha, Nome


# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
class EmailJaCadastrado(ValueError):
    """Sinaliza que o cadastro encontrou uma conta com o mesmo e-mail.

    A falha representa uma regra de negócio do fluxo de cadastro e não contém
    detalhes de transporte ou persistência. Ela existe para que adaptadores
    futuros possam traduzir a duplicidade sem o caso de uso decidir uma resposta
    HTTP ou acessar banco diretamente.
    """


# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
@dataclass(frozen=True, slots=True)
class CadastrarEstudanteEntrada:
    """Agrupa os value objects necessários para cadastrar uma conta de estudante.

    A entrada recebe somente nome, e-mail e hash de senha já derivados por uma
    fronteira de segurança externa, sem aceitar senha em texto claro. Ela existe
    para manter o contrato do caso de uso independente de HTTP e impedir que o
    cadastro implemente autenticação.
    """

    nome: Nome
    email: Email
    hash_senha: HashSenha


# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
class CadastrarEstudante:
    """Cria e persiste um usuário quando seu e-mail ainda não está cadastrado.

    O caso de uso consulta a porta de repositório, solicita uma identidade à
    porta de geração, constrói o aggregate root existente e então pede o
    salvamento. Ele existe para centralizar a regra de duplicidade sem importar
    adapter, banco, API ou comportamento de autenticação.
    """

    def __init__(
        self,
        repositorio_usuario: RepositorioUsuario,
        gerador_usuario_id: GeradorUsuarioId,
    ) -> None:
        """Recebe as portas internas que o fluxo de cadastro precisa coordenar.

        O construtor armazena apenas abstrações de consulta, salvamento e geração
        de identidade, que podem ser substituídas por doubles. Ele existe para
        preservar as dependências apontadas para dentro e tornar a orquestração
        unitariamente testável.
        """
        self._repositorio_usuario = repositorio_usuario
        self._gerador_usuario_id = gerador_usuario_id

    def executar(self, entrada: CadastrarEstudanteEntrada) -> Usuario:
        """Cadastra um estudante e devolve o agregado persistido pelo fluxo.

        O método consulta primeiro a existência do e-mail; se houver duplicidade,
        lança ``EmailJaCadastrado`` e não salva nada. Caso contrário, gera a
        identidade, constrói ``Usuario`` com os value objects recebidos e delega
        o salvamento à porta. Ele existe para realizar UC01 sem efetuar login,
        processar senha ou conceder acesso.
        """
        if self._repositorio_usuario.existe_por_email(entrada.email):
            raise EmailJaCadastrado("Já existe uma conta cadastrada com este e-mail.")

        usuario = Usuario(
            id=self._gerador_usuario_id.gerar(),
            nome=entrada.nome,
            email=entrada.email,
            hash_senha=entrada.hash_senha,
        )
        self._repositorio_usuario.salvar(usuario)
        return usuario
