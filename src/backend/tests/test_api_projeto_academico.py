"""Testa unitariamente a rota HTTP de cadastro de projetos acadêmicos."""

import unittest
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from backend.api.projeto_academico import CadastroProjetoAcademicoRequisicao, criar_router
from backend.application import CadastrarProjetoAcademico
from backend.domain import ProjetoAcademico, ProjetoAcademicoId

# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001


class RepositorioProjetoAcademicoSpy:
    """Registra em memória os projetos entregues pela Application.

    O double implementa a porta assíncrona acumulando argumentos, sem banco.
    Ele existe para exercitar o caso de uso real através da rota HTTP, sem
    ORM, banco, rede ou adapter produtivo.
    """

    def __init__(self) -> None:
        """Inicializa o registro vazio de chamadas de persistência.

        O construtor cria uma lista local que receberá entidades salvas. Ele
        existe para permitir que o teste observe persistência e sua ausência.
        """
        self.projetos_salvos: list[ProjetoAcademico] = []

    async def salvar(self, projeto: ProjetoAcademico) -> None:
        """Armazena localmente o projeto recebido pelo contrato da porta.

        O método acrescenta a entidade à lista e mantém a assinatura
        assíncrona. Ele existe para substituir infraestrutura no teste da rota.
        """
        self.projetos_salvos.append(projeto)


class GeradorProjetoAcademicoIdStub:
    """Entrega um identificador de projeto previamente definido.

    O stub devolve sempre o mesmo value object e elimina aleatoriedade. Ele
    existe para permitir asserções determinísticas sobre a entidade criada
    pela rota.
    """

    def __init__(self, identificador: ProjetoAcademicoId) -> None:
        """Recebe o identificador que devolverá nas chamadas seguintes.

        O construtor conserva o value object do cenário sem gerar UUIDs. Ele
        existe para controlar a identidade atribuída em cada teste.
        """
        self._identificador = identificador

    def gerar(self) -> ProjetoAcademicoId:
        """Devolve o identificador determinístico configurado no double.

        O método implementa a porta retornando o mesmo valor a cada chamada.
        Ele existe para isolar a rota da estratégia concreta de geração de UUID.
        """
        return self._identificador


def _rota(router: APIRouter, caminho: str, metodo: str):
    """Localiza o endpoint de uma rota registrada para chamada direta em teste.

    A função varre as rotas do router por caminho e método HTTP e devolve a
    função assíncrona decorada. Ela existe para exercitar o handler sem
    iniciar servidor ASGI ou depender de cliente HTTP real.
    """
    for rota in router.routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota.endpoint
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


class CadastroProjetoAcademicoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a rota POST integrada ao caso de uso real ``CadastrarProjetoAcademico``."""

    async def test_cadastra_projeto_e_devolve_dados_publicos(self) -> None:
        """Confirma 201 com dados públicos e persistência real via double.

        O teste chama o handler HTTP e compara a resposta pública com o
        efeito observado no double de repositório.
        """
        identificador = ProjetoAcademicoId(uuid4())
        repositorio = RepositorioProjetoAcademicoSpy()
        caso_de_uso = CadastrarProjetoAcademico(
            repositorio=repositorio,
            gerador_id=GeradorProjetoAcademicoIdStub(identificador),
        )
        cadastrar = _rota(criar_router(caso_de_uso), "/estudantes/{usuario_id}/projetos-academicos", "POST")
        usuario_id = uuid4()

        resposta = await cadastrar(
            usuario_id,
            CadastroProjetoAcademicoRequisicao(
                titulo="Sistema Currículo",
                descricao="Organiza informações acadêmicas.",
                tecnologias="Python, FastAPI",
            ),
        )

        self.assertEqual(resposta.id, identificador.valor)
        self.assertEqual(resposta.usuario_id, usuario_id)
        self.assertEqual(resposta.titulo, "Sistema Currículo")
        self.assertEqual(len(repositorio.projetos_salvos), 1)

    async def test_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum caso de uso foi injetado."""
        cadastrar = _rota(criar_router(None), "/estudantes/{usuario_id}/projetos-academicos", "POST")

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                uuid4(),
                CadastroProjetoAcademicoRequisicao(titulo="X", descricao="Y", tecnologias="Z"),
            )

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_titulo_em_branco_vira_422_sem_efeito_no_repositorio(self) -> None:
        """Confirma 422 quando o título fere a regra de domínio, sem persistir nada.

        O teste envia um título só com espaços e observa que o repositório
        double permanece intocado, provando que a validação de domínio
        interrompe o fluxo antes da persistência.
        """
        repositorio = RepositorioProjetoAcademicoSpy()
        caso_de_uso = CadastrarProjetoAcademico(
            repositorio=repositorio,
            gerador_id=GeradorProjetoAcademicoIdStub(ProjetoAcademicoId(uuid4())),
        )
        cadastrar = _rota(criar_router(caso_de_uso), "/estudantes/{usuario_id}/projetos-academicos", "POST")

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                uuid4(),
                CadastroProjetoAcademicoRequisicao(titulo="   ", descricao="Y", tecnologias="Z"),
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(repositorio.projetos_salvos, [])