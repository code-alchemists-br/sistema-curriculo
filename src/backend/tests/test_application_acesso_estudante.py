"""Testa unitariamente a confirmação de credenciais de estudante."""

import unittest
from uuid import UUID

from backend.application import (
    AcessarEstudante,
    AcessarEstudanteEntrada,
    CredenciaisInvalidas,
)
from backend.domain import Email, HashSenha, Nome, Usuario, UsuarioId


class RepositorioUsuarioStub:
    """Substitui a busca de usuários por uma resposta controlada em memória.

    O double registra o e-mail consultado e devolve o agregado configurado, sem
    I/O ou persistência. Ele existe para isolar a orquestração do acesso.
    """

    def __init__(self, usuario: Usuario | None) -> None:
        """Prepara a resposta da consulta e limpa o histórico de chamadas.

        O construtor recebe um agregado opcional e mantém as consultas
        observáveis. Ele existe para distinguir conta existente de inexistente.
        """
        self._usuario = usuario
        self.emails_consultados: list[Email] = []

    async def obter_por_email(self, email: Email) -> Usuario | None:
        """Devolve o usuário configurado após registrar o e-mail solicitado.

        O método simula a porta assíncrona sem acessar armazenamento. Ele existe
        para verificar a consulta feita pelo caso de uso em cada cenário.
        """
        self.emails_consultados.append(email)
        return self._usuario


class VerificadorSenhaStub:
    """Controla o resultado da comparação de senha sem usar criptografia real.

    O double registra os argumentos recebidos e devolve um booleano fixo. Ele
    existe para testar decisões de acesso independentemente do adapter seguro.
    """

    def __init__(self, confere: bool) -> None:
        """Define o resultado que a comparação deverá produzir.

        O construtor armazena a decisão e inicia o histórico vazio. Ele existe
        para tornar observável quando o caso de uso deve conferir a senha.
        """
        self._confere = confere
        self.chamadas: list[tuple[str, str]] = []

    def confere(self, senha: str, hash_senha: str) -> bool:
        """Registra a comparação e devolve o resultado previamente configurado.

        O método não deriva nem inspeciona segredo além de registrá-lo no double
        local. Ele existe para substituir a porta criptográfica nos testes.
        """
        self.chamadas.append((senha, hash_senha))
        return self._confere


class AcessarEstudanteTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o uso de repositório e verificador sem infraestrutura real.

    A classe exercita sucesso, conta ausente e senha incompatível com doubles.
    Ela existe para proteger a resposta uniforme do fluxo de acesso.
    """

    async def test_confirma_acesso_quando_conta_e_senha_sao_validas(self) -> None:
        """Confirma que o caso de uso consulta e delega a senha corretamente.

        O cenário fornece conta e decisão positiva, então verifica os argumentos
        observados. Ele existe para garantir o caminho de acesso bem-sucedido.
        """
        entrada = _criar_entrada()
        usuario = _criar_usuario()
        repositorio = RepositorioUsuarioStub(usuario)
        verificador = VerificadorSenhaStub(True)

        await AcessarEstudante(repositorio, verificador).executar(entrada)

        self.assertEqual(repositorio.emails_consultados, [entrada.email])
        self.assertEqual(verificador.chamadas, [(entrada.senha, usuario.hash_senha.valor)])

    async def test_rejeita_conta_ausente_sem_conferir_senha(self) -> None:
        """Confirma que a ausência recebe a mesma falha sem tocar no verificador.

        O cenário retorna nenhum agregado e espera a exceção de credenciais. Ele
        existe para impedir enumeração de contas e trabalho criptográfico inútil.
        """
        repositorio = RepositorioUsuarioStub(None)
        verificador = VerificadorSenhaStub(True)

        with self.assertRaises(CredenciaisInvalidas):
            await AcessarEstudante(repositorio, verificador).executar(_criar_entrada())

        self.assertEqual(verificador.chamadas, [])

    async def test_rejeita_senha_incompativel_com_falha_uniforme(self) -> None:
        """Confirma que senha incompatível não revela detalhes da credencial.

        O cenário devolve conta existente e comparação negativa, esperando a
        mesma exceção. Ele existe para proteger a decisão de segurança do fluxo.
        """
        with self.assertRaises(CredenciaisInvalidas):
            await AcessarEstudante(
                RepositorioUsuarioStub(_criar_usuario()), VerificadorSenhaStub(False)
            ).executar(_criar_entrada())


def _criar_entrada() -> AcessarEstudanteEntrada:
    """Cria credenciais estáveis para manter os testes focados na orquestração.

    A função constrói o e-mail como value object e preserva a senha somente no
    escopo do teste. Ela existe para evitar repetição de preparação de cenário.
    """
    return AcessarEstudanteEntrada(Email("ana@example.com"), "senha-correta")


def _criar_usuario() -> Usuario:
    """Cria um agregado válido com hash determinístico para os testes de acesso.

    A função usa valores de domínio prontos sem derivar senha ou acessar banco.
    Ela existe para fornecer uma conta estável aos doubles de repositório.
    """
    return Usuario(
        UsuarioId(UUID("00000000-0000-0000-0000-000000000001")),
        Nome("Ana Silva"),
        Email("ana@example.com"),
        HashSenha("hash-de-teste"),
    )
