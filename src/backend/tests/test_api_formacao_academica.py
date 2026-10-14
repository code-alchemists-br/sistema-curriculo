"""Testa unitariamente a fronteira HTTP de cadastro de formação acadêmica."""

import unittest
from datetime import date
from uuid import UUID

from fastapi import HTTPException
from pydantic import ValidationError
from starlette.requests import Request

from backend.api.factory import create_app
from backend.api.formacao_academica import (
    CadastroFormacaoAcademicaRequisicao,
    criar_router,
)
from backend.application.perfil_estudante import CadastrarFormacaoAcademicaEntrada
from backend.domain import (
    FormacaoAcademica,
    FormacaoAcademicaId,
    NivelFormacaoAcademica,
    RegraDeDominioViolada,
    StatusFormacaoAcademica,
)

# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_USUARIO_CLIENTE = UUID("00000000-0000-0000-0000-000000000002")
ID_FORMACAO = UUID("00000000-0000-0000-0000-0000000000f1")


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
class CadastroFormacaoAcademicaStub:
    """Substitui o caso de uso e registra chamadas recebidas pela API.

    O double devolve uma entidade controlada ou lança uma falha configurada,
    sem persistência, rede ou domínio adicional. Ele existe para isolar a
    tradução entre DTO e contrato de Application.
    """

    def __init__(self, erro: Exception | None = None) -> None:
        """Guarda a falha opcional e inicia o histórico de entradas.

        O construtor cria apenas estado em memória. Ele existe para preparar
        respostas determinísticas sem dependências externas.
        """
        self.erro = erro
        self.entradas: list[CadastrarFormacaoAcademicaEntrada] = []

    async def executar(
        self, entrada: CadastrarFormacaoAcademicaEntrada
    ) -> FormacaoAcademica:
        """Registra a entrada e devolve uma formação ou a falha configurada.

        O método simula o contrato assíncrono do caso de uso. Ele existe para
        verificar parâmetros e tradução HTTP sem executar Application real.
        """
        self.entradas.append(entrada)
        if self.erro is not None:
            raise self.erro
        return FormacaoAcademica(
            id=FormacaoAcademicaId(ID_FORMACAO),
            usuario_id=entrada.usuario_id,
            instituicao=entrada.instituicao,
            curso=entrada.curso,
            nivel=entrada.nivel,
            periodo=entrada.periodo,
            status=entrada.status,
        )


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
def _rota(executor: CadastroFormacaoAcademicaStub):
    """Obtém diretamente o handler de cadastro registrado no router.

    A função localiza a rota por caminho e método sem iniciar servidor ASGI.
    Ela existe para manter os testes limitados à unidade da fronteira HTTP.
    """
    for rota in criar_router(executor).routes:
        if rota.path == "/formacoes-academicas" and "POST" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota POST /formacoes-academicas não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
def _request(usuario_id: UUID | None) -> Request:
    """Cria requisição mínima com UUID autenticado opcional no estado.

    O escopo ASGI é local e instala apenas o principal já validado pelo
    mecanismo de sessão. Ele existe para exercitar a origem do proprietário.
    """
    request = Request(
        {"type": "http", "method": "POST", "path": "/formacoes-academicas", "headers": []}
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
def _payload(**alteracoes: object) -> dict[str, object]:
    """Monta corpo válido com alterações pontuais para cenários de teste.

    A função fornece enums e datas canônicos, substituindo somente os campos
    indicados pelo cenário. Ela existe para manter os testes centrados na
    tradução HTTP.
    """
    dados: dict[str, object] = {
        "instituicao": " FATEC ",
        "curso": " ADS ",
        "nivel": "tecnologo",
        "data_inicio": "2024-02-01",
        "data_fim": "2030-12-01",
        "status": "em_andamento",
    }
    dados.update(alteracoes)
    return dados


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
class CadastroFormacaoAcademicaRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica request, autenticação e resposta pública da rota.

    Os testes chamam o endpoint diretamente com caso de uso substituído e
    requisições sintéticas. Eles existem para proteger o contrato HTTP sem
    iniciar framework, rede ou persistência.
    """

    async def test_responde_201_e_usa_proprietario_da_sessao(self) -> None:
        """Devolve DTO explícito e ignora proprietário fornecido no payload.

        O cenário envia um UUID conflitante no corpo e outro no estado da
        requisição. Ele existe para assegurar que somente a sessão determine
        a propriedade e que os enums sejam transportados tipados.
        """
        executor = CadastroFormacaoAcademicaStub()
        cadastrar = _rota(executor)
        requisicao = CadastroFormacaoAcademicaRequisicao.model_validate(
            _payload(usuario_id=str(ID_USUARIO_CLIENTE))
        )

        resposta = await cadastrar(requisicao, _request(ID_USUARIO))

        self.assertEqual(resposta.id, ID_FORMACAO)
        self.assertEqual(resposta.usuario_id, ID_USUARIO)
        self.assertEqual(resposta.instituicao, "FATEC")
        self.assertEqual(resposta.curso, "ADS")
        self.assertIs(resposta.nivel, NivelFormacaoAcademica.TECNOLOGO)
        self.assertIs(resposta.status, StatusFormacaoAcademica.EM_ANDAMENTO)
        self.assertEqual(executor.entradas[0].usuario_id.valor, ID_USUARIO)
        self.assertIs(executor.entradas[0].nivel, NivelFormacaoAcademica.TECNOLOGO)
        self.assertEqual(executor.entradas[0].periodo.fim, date(2030, 12, 1))

    def test_enum_invalido_rejeitado_no_dto_sem_invocar_executor(self) -> None:
        """Rejeita vocabulário desconhecido durante a validação de request.

        O teste tenta construir o DTO com nível fora do enum e confirma que a
        falha ocorre antes de existir chamada ao executor. Ele existe para
        proteger a fronteira de transporte dos valores inválidos.
        """
        executor = CadastroFormacaoAcademicaStub()

        with self.assertRaises(ValidationError):
            CadastroFormacaoAcademicaRequisicao.model_validate(
                _payload(nivel="graduacao_livre")
            )

        self.assertEqual(executor.entradas, [])

    def test_dto_normaliza_limites_e_rejeita_controle(self) -> None:
        """Aplica limites após strip e rejeita controles no transporte.

        O cenário confirma tamanho máximo normalizado e entradas inválidas em
        instituição/curso. Ele existe para manter o contrato da API alinhado
        aos valores aceitos pelo Domain e pelo schema.
        """
        requisicao = CadastroFormacaoAcademicaRequisicao.model_validate(
            _payload(instituicao=f"  {'x' * 200}  ", curso="y")
        )
        self.assertEqual(requisicao.instituicao, "x" * 200)
        for campo, valor in (
            ("instituicao", "x" * 201),
            ("curso", "   "),
            ("curso", "x\ny"),
        ):
            with self.subTest(campo=campo, valor=repr(valor)):
                with self.assertRaises(ValidationError):
                    CadastroFormacaoAcademicaRequisicao.model_validate(
                        _payload(**{campo: valor})
                    )

    async def test_regra_de_dominio_e_mapeada_para_422_com_mensagem_segura(self) -> None:
        """Mapeia violação de domínio para erro HTTP sem expor detalhes internos.

        O executor double levanta a exceção de domínio e o handler converte o
        resultado em resposta estável. Ele existe para validar a tradução da
        fronteira independentemente do caso de uso.
        """
        executor = CadastroFormacaoAcademicaStub(
            erro=RegraDeDominioViolada("mensagem interna confidencial")
        )
        cadastrar = _rota(executor)

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroFormacaoAcademicaRequisicao.model_validate(_payload()),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(
            contexto.exception.detail,
            "A formação informada viola as regras de cadastro.",
        )
        self.assertNotIn("confidencial", contexto.exception.detail)

    async def test_periodo_invalido_nao_chama_executor(self) -> None:
        """Retorna 422 antes do executor quando fim antecede início.

        O handler cria o value object de período e captura sua violação sem
        delegar ao caso de uso. Ele existe para evitar qualquer tentativa de
        persistir uma entrada cronologicamente inválida.
        """
        executor = CadastroFormacaoAcademicaStub()
        cadastrar = _rota(executor)

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroFormacaoAcademicaRequisicao.model_validate(
                    _payload(data_fim="2023-01-01")
                ),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(executor.entradas, [])

    async def test_sem_sessao_nao_invoca_executor(self) -> None:
        """Exige principal autenticado antes de delegar o cadastro.

        A requisição não recebe UUID no estado e o histórico do executor é
        observado. Ela existe para manter a propriedade derivada do mecanismo
        de sessão já existente.
        """
        executor = CadastroFormacaoAcademicaStub()
        cadastrar = _rota(executor)

        with self.assertRaises(HTTPException) as contexto:
            await cadastrar(
                CadastroFormacaoAcademicaRequisicao.model_validate(_payload()),
                _request(None),
            )

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    def test_fabrica_registra_rota(self) -> None:
        """Inclui o endpoint no contrato OpenAPI da aplicação composta.

        O teste consulta a aplicação criada pela factory sem iniciar servidor.
        Ele existe para assegurar que o router implementado seja publicado.
        """
        app = create_app()

        operacao = app.openapi()["paths"]["/formacoes-academicas"]["post"]
        self.assertIn(
            "201", operacao["responses"]
        )
        self.assertIn("422", operacao["responses"])
