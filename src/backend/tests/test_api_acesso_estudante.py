"""Verifica a emissão HTTP do cookie de sessão no login."""

import unittest
from uuid import UUID

from fastapi import APIRouter, HTTPException, Response

from backend.api.cadastro_acesso import AcessoEstudanteRequisicao, criar_router
from backend.application import AcessarEstudanteEntrada, CredenciaisInvalidas
from backend.application.sessoes import CriadorSessao
from backend.domain.value_objects import UsuarioId


class AcessoExecutorStub:
    """Controla a identidade autenticada ou a falha devolvida pelo login.

    O double não acessa persistência nem verifica senha. Ele existe para isolar
    a tradução HTTP e confirmar a identidade encaminhada ao emissor.
    """

    def __init__(self, erro: Exception | None = None) -> None:
        """Armazena falha opcional e prepara a identidade de teste.

        A preparação é determinística e local. Ela existe para cobrir login
        válido e inválido sem depender de banco ou criptografia.
        """
        self.erro = erro
        self.usuario_id = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))
        self.entradas: list[AcessarEstudanteEntrada] = []

    async def executar(self, entrada: AcessarEstudanteEntrada) -> UsuarioId:
        """Registra a tentativa e devolve a identidade ou levanta erro.

        O método simula o caso de uso sem I/O. Ele existe para tornar visível o
        caminho da identidade autenticada até a criação da sessão.
        """
        self.entradas.append(entrada)
        if self.erro is not None:
            raise self.erro
        return self.usuario_id


class CriadorSessaoStub(CriadorSessao):
    """Substitui a criação de sessão e registra a identidade recebida.

    O double devolve token sintético sem aleatoriedade ou banco. Ele existe
    para validar que a API só emite cookie depois do login válido.
    """

    def __init__(self) -> None:
        """Prepara token fixo e histórico de identidades.

        O estado é mantido em memória para inspeção do teste. Ele existe para
        verificar integração entre handler e emissor.
        """
        self.usuario_ids: list[UsuarioId] = []

    async def criar(self, usuario_id: UsuarioId) -> str:
        """Registra a identidade e devolve a credencial sintética.

        O método não persiste nada. Ele existe para confirmar o valor de token
        transportado pelo handler.
        """
        self.usuario_ids.append(usuario_id)
        return "token-sintetico"


def _rota(router: APIRouter, caminho: str, metodo: str):
    """Localiza endpoint do router para chamada assíncrona direta.

    A função procura caminho e método sem iniciar servidor ASGI. Ela existe
    para testar o handler em isolamento.
    """
    for rota in router.routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota.endpoint
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


class AcessoEstudanteRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Protege criação e transporte da sessão no endpoint de login."""

    async def test_login_define_cookie_seguro_depois_de_validar_credenciais(self) -> None:
        """Emite token apenas no cookie e associa a sessão à identidade válida.

        O handler usa doubles e Response em memória para inspecionar cabeçalhos.
        O teste existe para proteger o contrato do login sem token no corpo.
        """
        acesso = AcessoExecutorStub()
        sessoes = CriadorSessaoStub()
        handler = _rota(criar_router(None, acesso, criador_sessao=sessoes), "/acessos", "POST")
        resposta = Response()

        resultado = await handler(
            AcessoEstudanteRequisicao(email="ana@example.com", senha="senha-segura"), resposta
        )

        self.assertIsNone(resultado)
        self.assertEqual(sessoes.usuario_ids, [acesso.usuario_id])
        cookie = resposta.headers["set-cookie"]
        self.assertIn("__Host-sessao=token-sintetico", cookie)
        self.assertIn("Max-Age=28800", cookie)
        self.assertIn("Path=/", cookie)
        self.assertIn("Secure", cookie)
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=lax", cookie)

    async def test_falha_de_acesso_registra_evento_sem_dados_sensiveis(self) -> None:
        """Registra a recusa sem incluir credenciais ou dados pessoais no log.

        O double levanta a falha uniforme e inclui valores sensíveis em sua
        mensagem; o handler deve registrar somente um evento categórico. O
        teste existe para auditar recusas sem vazar credenciais ou identidade.
        """
        email = "pessoa-privada@example.com"
        senha = "senha-super-secreta"
        token = "token-super-secreto"
        acesso = AcessoExecutorStub(
            CredenciaisInvalidas(f"{email} {senha} {token}")
        )
        sessoes = CriadorSessaoStub()
        handler = _rota(criar_router(None, acesso, criador_sessao=sessoes), "/acessos", "POST")
        resposta = Response()

        with self.assertLogs("backend.api.cadastro_acesso", level="WARNING") as logs:
            with self.assertRaises(HTTPException) as erro:
                await handler(AcessoEstudanteRequisicao(email=email, senha=senha), resposta)

        self.assertEqual(erro.exception.status_code, 401)
        self.assertEqual(sessoes.usuario_ids, [])
        self.assertNotIn("set-cookie", resposta.headers)
        self.assertEqual(len(logs.records), 1)
        self.assertEqual(logs.records[0].evento, "falha_autenticacao")
        self.assertEqual(logs.records[0].operacao, "acesso_estudante")
        for dado_sensivel in (email, senha, token):
            self.assertNotIn(dado_sensivel, logs.output[0])
