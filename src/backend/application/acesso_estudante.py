"""Orquestra a verificação de credenciais para acesso de estudante.

O módulo busca a conta por uma porta e delega a verificação da senha a outra
porta, sem conhecer HTTP, banco ou algoritmo criptográfico. Ele existe para
manter o acesso testável e evitar que controllers coordenem regras de uso.
"""

from dataclasses import dataclass

from backend.application.ports import RepositorioUsuario, VerificadorSenha
from backend.domain.value_objects import Email


class CredenciaisInvalidas(ValueError):
    """Sinaliza que as credenciais não permitem confirmar o acesso do estudante.

    A falha agrupa conta inexistente e senha incompatível sob a mesma resposta,
    evitando revelar qual dado falhou. Ela existe para que a borda HTTP traduza
    uma regra de acesso sem expor informação sobre contas cadastradas.
    """


@dataclass(frozen=True, slots=True)
class AcessarEstudanteEntrada:
    """Agrupa o e-mail e a senha recebidos para conferir uma tentativa de acesso.

    A entrada recebe a senha apenas durante a execução e não a persiste nem a
    devolve. Ela existe para transportar a credencial da borda ao verificador
    sem associar o caso de uso a DTOs ou ao protocolo HTTP.
    """

    email: Email
    senha: str


class AcessarEstudante:
    """Confirma credenciais por meio de repositório e verificador de senha.

    O caso de uso busca o usuário pelo e-mail e delega a comparação segura do
    segredo à porta, retornando sucesso somente quando ambos forem válidos. Ele
    existe para concentrar a intenção de acesso fora de controllers e adapters.
    """

    def __init__(self, repositorio_usuario: RepositorioUsuario, verificador_senha: VerificadorSenha) -> None:
        """Recebe as portas necessárias para localizar a conta e conferir sua senha.

        O construtor retém apenas abstrações internas, que podem ser substituídas
        por doubles em testes. Ele existe para preservar as dependências voltadas
        ao núcleo e manter a orquestração independente de infraestrutura.
        """
        self._repositorio_usuario = repositorio_usuario
        self._verificador_senha = verificador_senha

    async def executar(self, entrada: AcessarEstudanteEntrada) -> None:
        """Confirma uma tentativa de acesso ou falha sem revelar qual credencial errou.

        O método aguarda a busca da conta e compara a senha somente quando há um
        agregado correspondente. Ele existe para aplicar o fluxo de acesso sem
        criar sessão, token ou política de autorização ainda não especificados.
        """
        usuario = await self._repositorio_usuario.obter_por_email(entrada.email)
        if usuario is None or not self._verificador_senha.confere(entrada.senha, usuario.hash_senha.valor):
            raise CredenciaisInvalidas("E-mail ou senha não conferem.")
