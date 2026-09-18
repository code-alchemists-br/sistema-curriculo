"""Define portas internas necessárias ao cadastro de estudantes.

As portas descrevem somente as capacidades de que o caso de uso precisa, sem
escolher banco, ORM ou estratégia de geração de UUID. Elas existem para que a
orquestração permaneça testável com doubles e para que adapters futuros possam
depender do núcleo da aplicação.
"""

from typing import Protocol

from backend.domain.entities import Usuario
from backend.domain.value_objects import Email, UsuarioId


# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260916-cadastro-acesso-estudante-v002.md#v002
class RepositorioUsuario(Protocol):
    """Define a capacidade assíncrona de consultar e persistir usuários.

    A porta recebe e devolve conceitos de domínio e torna aguardáveis somente a
    consulta e o salvamento, que serão I/O em adapters futuros. Ela existe para
    que o caso de uso libere o fluxo durante a persistência sem conhecer banco,
    ORM ou implementação concreta.
    """

    async def existe_por_email(self, email: Email) -> bool:
        """Informa assincronamente se existe usuário com o e-mail fornecido.

        Implementações aguardam o mecanismo de armazenamento e preservam o
        contrato booleano do núcleo. O método existe para que o caso de uso
        interrompa cadastros duplicados antes de solicitar persistência.
        """

    async def salvar(self, usuario: Usuario) -> None:
        """Solicita assincronamente a persistência de usuário válido.

        Implementações aguardam o armazenamento sem alterar regra de negócio.
        O método existe para separar a decisão de cadastro da infraestrutura
        Code First que será implementada por adapter externo.
        """

    async def obter_por_email(self, email: Email) -> Usuario | None:
        """Obtém assincronamente a conta associada ao e-mail, quando ela existir.

        Implementações aguardam a leitura no armazenamento e devolvem somente o
        agregado do domínio ou ausência, sem revelar detalhes de persistência.
        O método existe para que o caso de uso de acesso confira credenciais sem
        acoplar a Application ao banco, ORM ou API.
        """


class VerificadorSenha(Protocol):
    """Define a comparação segura entre uma senha informada e um hash armazenado.

    A porta deixa o algoritmo criptográfico na infraestrutura e entrega apenas
    uma decisão booleana ao caso de uso. Ela existe para que autenticação não
    armazene senha em texto claro nem dependa de uma biblioteca de segurança.
    """

    def confere(self, senha: str, hash_senha: str) -> bool:
        """Informa se a senha em texto claro corresponde ao hash persistido.

        Implementações usam uma comparação apropriada ao formato de hash e não
        expõem dados da credencial. O método existe para separar a decisão de
        acesso da derivação criptográfica concreta.
        """


# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
class GeradorUsuarioId(Protocol):
    """Define a geração substituível da identidade de um usuário.

    A porta encapsula a origem do UUID e entrega um ``UsuarioId`` já tipado ao
    caso de uso. Ela existe para que testes controlem a identidade gerada sem
    depender de aleatoriedade ou de uma implementação externa.
    """

    def gerar(self) -> UsuarioId:
        """Gera uma identidade tipada para um novo usuário.

        Implementações podem obter um UUID de qualquer fonte compatível, mas
        retornam o value object do domínio. O método existe para manter o fluxo
        de cadastro determinístico em testes e independente da infraestrutura.
        """
