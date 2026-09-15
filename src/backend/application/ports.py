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
class RepositorioUsuario(Protocol):
    """Define a capacidade interna de consultar e persistir usuários.

    A porta recebe e devolve conceitos de domínio, e expõe apenas a consulta por
    e-mail e o salvamento necessários ao cadastro. Ela existe para impedir que
    o caso de uso conheça um banco ou implementação concreta de repositório.
    """

    def existe_por_email(self, email: Email) -> bool:
        """Informa se já existe um usuário com o e-mail normalizado fornecido.

        Implementações consultam o mecanismo de armazenamento apropriado, mas
        preservam o contrato booleano do núcleo. O método existe para que o caso
        de uso interrompa cadastros duplicados antes de solicitar persistência.
        """

    def salvar(self, usuario: Usuario) -> None:
        """Solicita a persistência de um agregado de usuário válido.

        Implementações escolhem como armazenar o agregado sem alterar sua regra
        de negócio. O método existe para separar a decisão de cadastro da
        infraestrutura Code First que será implementada em outro card.
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
