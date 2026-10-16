"""Verifica o agrupamento e a autenticação documentados no schema OpenAPI."""

import unittest

from backend.api.documentacao_openapi import (
    ESQUEMA_SESSAO,
    METADADOS_TAGS,
    TAG_CADASTRO_ACESSO,
    TAG_SESSOES,
    TAG_VERSOES_CURRICULO,
)
from backend.api.factory import create_app
from backend.api.sessoes import COOKIE_SESSAO
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.domain.value_objects import UsuarioId


class AutenticadorSessaoNulo(AutenticadorSessao):
    """Rejeita qualquer token sem consultar persistência.

    O double apenas devolve `None`. Ele existe para ativar o middleware de
    autenticação na fábrica e observar o schema OpenAPI resultante.
    """

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Devolve ausência de identidade para qualquer token recebido.

        O método não realiza I/O. Ele existe para satisfazer a porta exigida
        pela fábrica sem influenciar a geração da documentação.
        """
        return None


def _operacoes(schema: dict) -> dict[tuple[str, str], dict]:
    """Indexa as operações do schema por método em maiúsculas e caminho.

    A função percorre `paths` e achata os métodos de cada caminho. Ela existe
    para simplificar as asserções sobre operações específicas.
    """
    return {
        (metodo.upper(), caminho): operacao
        for caminho, metodos in schema["paths"].items()
        for metodo, operacao in metodos.items()
    }


class DocumentacaoOpenApiTest(unittest.TestCase):
    """Garante que o Swagger agrupa rotas e indica a exigência de sessão.

    Os testes geram o schema em memória pela fábrica, sem servidor. Eles
    existem para evitar regressões na organização e na segurança documentadas.
    """

    def test_toda_operacao_pertence_a_um_grupo_declarado(self) -> None:
        """Toda rota deve ter exatamente uma tag presente nos metadados."""
        schema = create_app().openapi()
        nomes_declarados = [tag["name"] for tag in METADADOS_TAGS]
        declaradas = set(nomes_declarados)

        self.assertEqual([tag["name"] for tag in schema["tags"]], nomes_declarados)
        for chave, operacao in _operacoes(schema).items():
            with self.subTest(operacao=chave):
                self.assertEqual(len(operacao["tags"]), 1)
                self.assertIn(operacao["tags"][0], declaradas)

    def test_rotas_sao_agrupadas_pelo_recurso(self) -> None:
        """Login, logout e listagem de versões devem cair nos grupos esperados."""
        operacoes = _operacoes(create_app().openapi())

        self.assertEqual(operacoes[("POST", "/acessos")]["tags"], [TAG_CADASTRO_ACESSO])
        self.assertEqual(operacoes[("DELETE", "/sessao/atual")]["tags"], [TAG_SESSOES])
        self.assertIn(
            [TAG_VERSOES_CURRICULO],
            [
                operacao["tags"]
                for (metodo, caminho), operacao in operacoes.items()
                if metodo == "GET" and caminho.endswith("/curriculos")
            ],
        )

    def test_com_autenticador_rotas_privadas_exigem_cookie_de_sessao(self) -> None:
        """Rotas privadas devem exigir o esquema de cookie e as públicas não."""
        schema = create_app(autenticador_sessao=AutenticadorSessaoNulo()).openapi()
        operacoes = _operacoes(schema)

        esquema = schema["components"]["securitySchemes"][ESQUEMA_SESSAO]
        self.assertEqual(
            (esquema["type"], esquema["in"], esquema["name"]),
            ("apiKey", "cookie", COOKIE_SESSAO),
        )
        for publica in [("POST", "/estudantes"), ("POST", "/acessos"), ("DELETE", "/sessao/atual")]:
            with self.subTest(publica=publica):
                self.assertNotIn("security", operacoes[publica])
        self.assertEqual(
            operacoes[("PUT", "/estudantes/me/perfil")]["security"],
            [{ESQUEMA_SESSAO: []}],
        )

    def test_sem_autenticador_nenhuma_rota_exige_sessao(self) -> None:
        """Sem middleware, a documentação não deve anunciar autenticação."""
        schema = create_app().openapi()

        self.assertNotIn(ESQUEMA_SESSAO, schema.get("components", {}).get("securitySchemes", {}))
        for chave, operacao in _operacoes(schema).items():
            with self.subTest(operacao=chave):
                self.assertNotIn("security", operacao)


if __name__ == "__main__":
    unittest.main()
