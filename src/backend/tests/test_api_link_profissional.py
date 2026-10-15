"""Testa unitariamente a fronteira HTTP de cadastro de links profissionais."""

import unittest
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from starlette.requests import Request

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.api.factory import create_app
from backend.api.link_profissional import (
    CadastroLinkProfissionalRequisicao,
    criar_router,
)
from backend.application.cadastro_link_profissional import (
    CadastrarLinkProfissionalEntrada,
    LinkProfissionalJaCadastrado,
)
from backend.domain import LinkProfissional, LinkProfissionalId, RegraDeDominioViolada

ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_LINK = UUID("00000000-0000-0000-0000-0000000000a1")


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class CadastroLinkProfissionalStub:
    """Substitui o caso de uso por comportamento determinístico em memória.

    O double registra a entrada recebida e constrói a resposta sem banco,
    framework ou rede. Ele existe para isolar a conversão exercida pelo handler
    HTTP e permitir cenários de sucesso, conflito e validação.
    """

    def __init__(
        self,
        duplicado: bool = False,
        erro_dominio: str | None = None,
    ) -> None:
        """Prepara o histórico de chamadas e o resultado configurável.

        O construtor conserva apenas estado local usado pelo teste. Ele existe
        para representar o executor injetado sem introduzir dependências
        externas na unidade de interface.
        """
        self.duplicado = duplicado
        self.erro_dominio = erro_dominio
        self.entradas: list[CadastrarLinkProfissionalEntrada] = []

    async def executar(
        self, entrada: CadastrarLinkProfissionalEntrada
    ) -> LinkProfissional:
        """Registra a entrada e devolve ou rejeita o link configurado.

        O método simula o contrato público do caso de uso usando somente dados
        em memória. Ele existe para verificar que a API traduz corretamente a
        chamada e a falha sem testar regras internas.
        """
        self.entradas.append(entrada)
        if self.erro_dominio is not None:
            raise RegraDeDominioViolada(self.erro_dominio)
        if self.duplicado:
            raise LinkProfissionalJaCadastrado(
                "Link profissional já cadastrado para este usuário."
            )
        return LinkProfissional(
            id=LinkProfissionalId(ID_LINK),
            usuario_id=entrada.usuario_id,
            rotulo=entrada.rotulo,
            url=entrada.url,
        )


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def _rota(router: APIRouter) -> Any:
    """Obtém o endpoint POST de links profissionais diretamente da tabela de rotas.

    A função percorre o router já configurado e devolve o handler sem iniciar
    servidor ASGI. Ela existe para manter o teste no nível unitário da
    fronteira, com executor e requisição controlados.
    """
    for rota in router.routes:
        if getattr(rota, "path", None) == "/links-profissionais" and "POST" in getattr(
            rota, "methods", set()
        ):
            return rota.endpoint
    raise AssertionError("Rota POST /links-profissionais não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
def _request(usuario_id: UUID | None) -> Request:
    """Constrói uma requisição mínima com o principal opcional no estado.

    A função monta um escopo ASGI local e instala somente o UUID que seria
    fornecido pelo mecanismo existente. Ela existe para verificar a propriedade
    sem aceitar um identificador controlado pelo corpo HTTP.
    """
    request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/links-profissionais",
            "headers": [],
        }
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class CadastroLinkProfissionalRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução entre transporte HTTP e executor de link profissional.

    A classe chama o handler decorado com doubles locais, sem criar aplicação
    FastAPI nem servidor. Ela existe para proteger o contrato de fronteira no
    nível unitário apropriado.
    """

    async def test_vincula_o_link_ao_principal_autenticado(self) -> None:
        """Encaminha dados completos usando o UUID instalado na requisição.

        O cenário invoca o handler e inspeciona a entrada entregue ao double.
        Ele existe para impedir que a API derive o proprietário do payload ou
        exponha a entidade de domínio na resposta.
        """
        executor = CadastroLinkProfissionalStub()
        cadastrar = _rota(criar_router(executor))

        resposta = await cadastrar(
            CadastroLinkProfissionalRequisicao(
                rotulo="GitHub Perfil",
                url="https://github.com/usuario",
            ),
            _request(ID_USUARIO),
        )

        self.assertEqual(resposta.id, ID_LINK)
        self.assertEqual(resposta.usuario_id, ID_USUARIO)
        self.assertEqual(resposta.rotulo, "GitHub Perfil")
        self.assertEqual(resposta.url, "https://github.com/usuario")
        self.assertEqual(executor.entradas[0].usuario_id.valor, ID_USUARIO)
        self.assertEqual(executor.entradas[0].rotulo, "GitHub Perfil")
        self.assertEqual(executor.entradas[0].url, "https://github.com/usuario")

    async def test_traduz_duplicidade_para_conflito(self) -> None:
        """Apresenta 409 quando o executor informa link já cadastrado.

        O cenário usa o double configurado para falhar e observa a exceção HTTP
        gerada pelo handler. Ele existe para manter o conflito compreensível e
        não revelar dados persistidos de qualquer outra conta.
        """
        cadastrar = _rota(criar_router(CadastroLinkProfissionalStub(duplicado=True)))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroLinkProfissionalRequisicao(
                    rotulo="Portfólio",
                    url="https://github.com/usuario",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            contexto.exception.detail,
            "Link profissional já cadastrado para este usuário.",
        )

    async def test_traduz_regra_de_dominio_violada_para_422(self) -> None:
        """Apresenta 422 quando o domínio rejeita os dados do link.

        O cenário simula a falha de validação de domínio e observa a resposta
        HTTP unprocessable_content. Ele existe para traduzir erros de regra de negócio
        em respostas compreensíveis ao cliente HTTP sem usar o termo depreciado ENTITY.
        """
        cadastrar = _rota(
            criar_router(
                CadastroLinkProfissionalStub(
                    erro_dominio="O esquema da URL do link profissional deve ser 'http' ou 'https'."
                )
            )
        )

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroLinkProfissionalRequisicao(
                    rotulo="Script",
                    url="javascript:alert(1)",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(
            contexto.exception.status_code,
            status.HTTP_422_UNPROCESSABLE_CONTENT,
        )
        self.assertEqual(
            contexto.exception.detail,
            "O esquema da URL do link profissional deve ser 'http' ou 'https'.",
        )

    async def test_rejeita_requisicao_sem_principal(self) -> None:
        """Retorna 401 sem invocar o executor para requisição anônima.

        O cenário omite o estado de autenticação e compara o histórico do
        double. Ele existe para garantir que o endpoint depende do principal
        fornecido pelo mecanismo de borda já existente.
        """
        executor = CadastroLinkProfissionalStub()
        cadastrar = _rota(criar_router(executor))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroLinkProfissionalRequisicao(
                    rotulo="Portfólio",
                    url="https://site.com",
                ),
                _request(None),
            )

        self.assertEqual(contexto.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(contexto.exception.detail, "Autenticação necessária.")
        self.assertEqual(executor.entradas, [])

    async def test_retorna_503_quando_executor_nao_disponivel(self) -> None:
        """Retorna 503 quando o executor não foi fornecido à fábrica de router.

        O cenário instancia o router com None e tenta cadastrar um link.
        Ele existe para indicar indisponibilidade controlada do serviço quando
        a dependência não estiver disponível.
        """
        cadastrar = _rota(criar_router(None))

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroLinkProfissionalRequisicao(
                    rotulo="Portfólio",
                    url="https://site.com",
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(
            contexto.exception.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )
        self.assertEqual(contexto.exception.detail, "Cadastro indisponível.")

    def test_fabrica_registra_rota_de_links_profissionais(self) -> None:
        """Mantém o endpoint de link profissional disponível na aplicação composta.

        O teste cria somente a fábrica FastAPI e consulta o contrato OpenAPI,
        sem iniciar servidor ou injetar infraestrutura. Ele existe para evitar
        que o router seja implementado mas fique desconectado da API pública.
        """
        app = create_app()

        self.assertIn("/links-profissionais", app.openapi()["paths"])


if __name__ == "__main__":
    unittest.main()
