"""Testa unitariamente a fronteira HTTP de cadastro de projetos acadêmicos."""

import json
import unittest
from uuid import UUID

from fastapi import HTTPException
from pydantic import ValidationError
from starlette.requests import Request

# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
from backend.api.projeto_academico import (
    CadastroProjetoAcademicoRequisicao,
    ProjetoAcademicoResposta,
    criar_router,
)
from backend.application import CadastrarProjetoAcademicoEntrada
from backend.domain import (
    ProjetoAcademico,
    ProjetoAcademicoId,
    RegraDeDominioViolada,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_USUARIO_CLIENTE = UUID("00000000-0000-0000-0000-000000000002")
ID_PROJETO = UUID("00000000-0000-0000-0000-0000000000f1")


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class CadastroProjetoAcademicoStub:
    """Substitui o caso de uso e registra entradas recebidas pela API.

    O double guarda entradas em memória e devolve projeto determinístico ou
    lança uma falha configurada. Ele existe para isolar a tradução HTTP do
    fluxo de aplicação e da persistência.
    """

    def __init__(self, erro: Exception | None = None) -> None:
        """Configura uma falha opcional e inicia o histórico de chamadas.

        O construtor prepara estado local sem recursos externos. Ele existe
        para exercitar respostas de sucesso e erro de forma determinística.
        """
        self.erro = erro
        self.entradas: list[CadastrarProjetoAcademicoEntrada] = []

    async def executar(
        self, entrada: CadastrarProjetoAcademicoEntrada
    ) -> ProjetoAcademico:
        """Registra a entrada e devolve projeto ou a falha configurada.

        O método simula o contrato assíncrono do caso de uso. Ele existe para
        testar parâmetros e traduções HTTP sem executar Application real.
        """
        self.entradas.append(entrada)
        if self.erro is not None:
            raise self.erro
        return ProjetoAcademico(
            id=ProjetoAcademicoId(ID_PROJETO),
            usuario_id=entrada.usuario_id,
            titulo=entrada.titulo,
            descricao=entrada.descricao,
            tecnologias=entrada.tecnologias,
        )


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
def _rota(executor: CadastroProjetoAcademicoStub | None):
    """Obtém o endpoint POST do router sem iniciar aplicação ASGI.

    A função procura rota e método no router criado com executor substituto.
    Ela existe para testar o handler como unidade isolada.
    """
    for rota in criar_router(executor).routes:
        if rota.path == "/projetos-academicos" and "POST" in rota.methods:
            return rota
    raise AssertionError("Rota POST /projetos-academicos não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
def _request(
    usuario_id: UUID | None,
    dados: object | None = None,
) -> Request:
    """Cria requisição sintética com body JSON e sessão opcional.

    O objeto usa apenas um escopo ASGI local e grava o principal autenticado no
    estado quando fornecido. Ele existe para validar propriedade sem middleware
    ou servidor iniciado.
    """
    corpo = b"" if dados is None else json.dumps(dados).encode("utf-8")

    async def receber() -> dict[str, object]:
        """Entrega o corpo sintético uma vez ao parser da requisição.

        A função fornece a mensagem ASGI mínima sem abrir stream real. Ela
        existe para testar a desserialização dentro do handler.
        """
        return {"type": "http.request", "body": corpo, "more_body": False}

    requisicao = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/projetos-academicos",
            "headers": [],
            "query_string": b"",
        },
        receive=receber,
    )
    if usuario_id is not None:
        requisicao.state.usuario_id = usuario_id
    return requisicao


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
def _payload(**alteracoes: object) -> dict[str, object]:
    """Monta corpo válido e aplica alterações próprias de cada cenário.

    A função define somente os três textos do contrato e acrescenta valores
    recebidos pelo teste. Ela existe para reutilizar dados seguros no exercício
    unitário do handler.
    """
    dados: dict[str, object] = {
        "titulo": "Sistema Currículo",
        "descricao": "Organiza informações acadêmicas.",
        "tecnologias": "Python, FastAPI",
    }
    dados.update(alteracoes)
    return dados


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class CadastroProjetoAcademicoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o contrato HTTP com caso de uso substituído.

    Os testes chamam diretamente o handler usando requests sintéticas e
    observam o executor double. Eles existem para proteger a borda sem iniciar
    servidor, middleware real ou armazenamento.
    """

    async def test_responde_201_e_deriva_proprietario_da_sessao(self) -> None:
        """Devolve DTO e ignora `usuario_id` desconhecido no corpo.

        O cenário envia um proprietário conflitante junto aos três textos e
        instala outro UUID no estado. Ele existe para provar que só a sessão
        controla o dono e que os campos chegam à Application.
        """
        executor = CadastroProjetoAcademicoStub()
        rota = _rota(executor)
        resposta = await rota.endpoint(
            _request(
                ID_USUARIO,
                _payload(
                    usuario_id=str(ID_USUARIO_CLIENTE),
                    titulo="  Sistema Currículo  ",
                    descricao="  Organiza informações acadêmicas.  ",
                    tecnologias="  Python, FastAPI  ",
                ),
            )
        )

        self.assertEqual(rota.status_code, 201)
        self.assertIsInstance(resposta, ProjetoAcademicoResposta)
        self.assertEqual(resposta.id, ID_PROJETO)
        self.assertEqual(resposta.usuario_id, ID_USUARIO)
        self.assertEqual(resposta.titulo, "Sistema Currículo")
        self.assertEqual(resposta.descricao, "Organiza informações acadêmicas.")
        self.assertEqual(resposta.tecnologias, "Python, FastAPI")
        self.assertEqual(len(executor.entradas), 1)
        entrada = executor.entradas[0]
        self.assertEqual(entrada.usuario_id, UsuarioId(ID_USUARIO))
        self.assertEqual(entrada.titulo, "  Sistema Currículo  ")
        self.assertEqual(entrada.descricao, "  Organiza informações acadêmicas.  ")
        self.assertEqual(entrada.tecnologias, "  Python, FastAPI  ")

    async def test_formato_invalido_vira_422_sem_refletir_entrada(self) -> None:
        """Oculta valores enviados em erros de tipo, tamanho e vazio.

        O teste tenta construir o DTO via handler com três falhas estruturais e
        verifica a resposta fixa sem ecoar os valores. Ele existe para impedir
        exposição de conteúdo fornecido pelo cliente.
        """
        casos = (
            _payload(titulo="VALOR_SECRETO", descricao=1),
            _payload(titulo="VALOR_SECRETO_" * 20),
            _payload(tecnologias="   "),
            _payload(titulo=""),
        )
        for dados in casos:
            with self.subTest(dados=dados):
                executor = CadastroProjetoAcademicoStub()
                rota = _rota(executor)
                with self.assertRaises(HTTPException) as contexto:
                    await rota.endpoint(_request(ID_USUARIO, dados))

                self.assertEqual(contexto.exception.status_code, 422)
                self.assertEqual(
                    contexto.exception.detail,
                    "Dados do projeto acadêmico inválidos.",
                )
                self.assertNotIn("VALOR_SECRETO", contexto.exception.detail)
                self.assertEqual(executor.entradas, [])

    async def test_violacao_de_dominio_vira_422_com_mensagem_segura(self) -> None:
        """Traduz controle rejeitado pelo Domain sem revelar a exceção.

        O executor double simula a exceção que a entidade lança para um
        controle Unicode. Ele existe para testar a mensagem pública da borda.
        """
        executor = CadastroProjetoAcademicoStub(
            erro=RegraDeDominioViolada("controle secreto inválido")
        )
        rota = _rota(executor)

        with self.assertRaises(HTTPException) as contexto:
            await rota.endpoint(
                _request(ID_USUARIO, _payload(titulo="texto\x85invalido"))
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(
            contexto.exception.detail,
            "Os dados do projeto acadêmico violam as regras de cadastro.",
        )
        self.assertNotIn("secreto", contexto.exception.detail)

    async def test_estado_de_sessao_ausente_falha_fechado_sem_executor(self) -> None:
        """Responde 401 e não chama Application sem UUID de sessão.

        A requisição contém conteúdo válido, mas não recebe identidade no
        estado. Ela existe para garantir que ausência de principal nunca gere
        cadastro sem proprietário.
        """
        executor = CadastroProjetoAcademicoStub()
        rota = _rota(executor)

        with self.assertRaises(HTTPException) as contexto:
            await rota.endpoint(_request(None, _payload()))

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    async def test_executor_ausente_responde_503(self) -> None:
        """Informa indisponibilidade quando não há caso de uso injetado.

        O handler recebe requisição autenticada e encontra executor ausente.
        Ele existe para manter a resposta operacional previsível.
        """
        rota = _rota(None)

        with self.assertRaises(HTTPException) as contexto:
            await rota.endpoint(_request(ID_USUARIO, _payload()))

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Cadastro indisponível.")

    def test_dto_ignora_campos_desconhecidos_e_exige_tres_textos(self) -> None:
        """Confirma o conjunto de campos do request e a regra extra-ignore.

        O teste valida payload com `usuario_id` adicional e inspeciona os
        campos reconhecidos. Ele existe para impedir que o cliente controle o
        proprietário pela desserialização.
        """
        requisicao = CadastroProjetoAcademicoRequisicao.model_validate(
            _payload(usuario_id=str(ID_USUARIO_CLIENTE))
        )

        self.assertEqual(
            set(requisicao.model_fields_set), {"titulo", "descricao", "tecnologias"}
        )
        self.assertFalse(hasattr(requisicao, "usuario_id"))
        with self.assertRaises(ValidationError):
            CadastroProjetoAcademicoRequisicao.model_validate({"titulo": "A"})
