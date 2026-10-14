"""Verifica o cadastro HTTP autenticado de experiências profissionais."""

import unittest
from datetime import date
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from backend.api.experiencia_profissional import (
    CadastroExperienciaProfissionalRequisicao,
    criar_router,
)
from backend.api.factory import create_app
from backend.application.cadastro_experiencia_profissional import (
    CadastrarExperienciaProfissionalEntrada,
)
from backend.domain import (
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    Periodo,
    UsuarioId,
)

ID_USUARIO_TESTE = UUID("00000000-0000-0000-0000-000000000001")
ID_EXPERIENCIA_TESTE = UUID("00000000-0000-0000-0000-0000000000e1")


class CadastroExperienciaStub:
    """Substitui o caso de uso e registra a entrada recebida pela rota.

    O double constrói uma entidade em memória a partir da entrada e não acessa
    banco ou serviços externos. Ele existe para testar a conversão HTTP e o
    vínculo obrigatório com o principal autenticado.
    """

    def __init__(self) -> None:
        """Prepara o histórico de entradas executadas pelo double.

        O estado fica inteiramente em memória e determinístico. Ele existe para
        permitir que cada cenário observe a chamada feita pela rota.
        """
        self.entradas: list[CadastrarExperienciaProfissionalEntrada] = []

    async def executar(
        self, entrada: CadastrarExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Registra a entrada e devolve a experiência criada em memória.

        O método preserva os campos do comando e atribui um UUID fixo. Ele existe
        para simular o caso de uso sem introduzir persistência no teste da API.
        """
        self.entradas.append(entrada)
        return ExperienciaProfissional(
            id=ExperienciaProfissionalId(ID_EXPERIENCIA_TESTE),
            usuario_id=entrada.usuario_id,
            empresa=entrada.empresa,
            cargo=entrada.cargo,
            descricao=entrada.descricao,
            periodo=entrada.periodo,
        )


def _rota(router: APIRouter, caminho: str):
    """Localiza o handler POST associado ao caminho informado.

    A função percorre a tabela de rotas construída pelo FastAPI e devolve o
    endpoint decorado. Ela existe para exercitar a fronteira HTTP sem servidor.
    """
    for rota in router.routes:
        if rota.path == caminho and "POST" in rota.methods:
            return rota.endpoint
    raise AssertionError(f"Rota POST {caminho} não encontrada.")


def _request(usuario_id: UUID | None) -> Request:
    """Cria uma requisição com o principal opcional produzido pelo middleware.

    O helper constrói o escopo ASGI mínimo e instala a identidade apenas quando
    informada. Ele existe para verificar que a rota aceita somente estado do
    servidor, nunca identidade declarada no corpo da requisição.
    """
    request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/experiencias-profissionais",
            "headers": [],
        }
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


class CadastroExperienciaProfissionalRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica autenticação e conversão HTTP do cadastro de experiência.

    A classe chama o handler com executor em memória e um escopo ASGI mínimo.
    Ela existe para proteger a fronteira sem iniciar servidor ou banco.
    """

    async def test_vincula_experiencia_ao_usuario_instalado_pelo_middleware(
        self,
    ) -> None:
        """Usa o principal da requisição, e não um identificador do cliente.

        O cenário instala um UUID em ``request.state`` e compara o proprietário
        recebido pelo caso de uso. Ele existe para impedir cadastro em nome de
        outro estudante.
        """
        executor = CadastroExperienciaStub()
        cadastrar = _rota(criar_router(executor), "/experiencias-profissionais")

        resposta = await cadastrar(
            CadastroExperienciaProfissionalRequisicao(
                empresa="Instituto Exemplo",
                cargo="Desenvolvedora",
                descricao="Construiu integrações.",
                data_inicio=date(2023, 1, 1),
            ),
            _request(ID_USUARIO_TESTE),
        )

        self.assertEqual(resposta.usuario_id, ID_USUARIO_TESTE)
        self.assertEqual(executor.entradas[0].usuario_id, UsuarioId(ID_USUARIO_TESTE))
        self.assertEqual(executor.entradas[0].periodo, Periodo(date(2023, 1, 1)))

    async def test_rejeita_requisicao_sem_principal_autenticado(self) -> None:
        """Retorna 401 e não executa cadastro sem identidade confiável.

        O cenário omite o estado instalado pelo middleware e observa que o
        executor não recebe comandos. Ele existe para bloquear chamadas anônimas.
        """
        executor = CadastroExperienciaStub()
        cadastrar = _rota(criar_router(executor), "/experiencias-profissionais")
        requisicao = CadastroExperienciaProfissionalRequisicao(
            empresa="Empresa",
            cargo="Cargo",
            descricao="Descrição",
            data_inicio=date(2024, 1, 1),
        )

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(requisicao, _request(None))

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    async def test_retorna_503_quando_o_executor_nao_esta_composto(self) -> None:
        """Retorna 503 sem afirmar que há persistência disponível.

        O cenário usa uma identidade válida, mas não injeta o caso de uso. Ele
        existe para preservar a indisponibilidade explícita da composição atual.
        """
        cadastrar = _rota(criar_router(None), "/experiencias-profissionais")
        requisicao = CadastroExperienciaProfissionalRequisicao(
            empresa="Empresa",
            cargo="Cargo",
            descricao="Descrição",
            data_inicio=date(2024, 1, 1),
        )

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(requisicao, _request(ID_USUARIO_TESTE))

        self.assertEqual(contexto.exception.status_code, 503)

    def test_fabrica_registra_a_rota_de_experiencias(self) -> None:
        """Mantém a rota disponível mesmo antes da composição do executor.

        O cenário constrói a aplicação com suas dependências opcionais e
        consulta o contrato OpenAPI gerado. Ele existe para garantir que a
        fábrica inclua a nova fronteira no aplicativo ASGI.
        """
        app = create_app()

        self.assertIn("/experiencias-profissionais", app.openapi()["paths"])
