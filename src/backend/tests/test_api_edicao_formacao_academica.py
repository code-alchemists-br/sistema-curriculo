"""Testa unitariamente a tradução HTTP da edição de formação acadêmica."""

import unittest
from datetime import date
from uuid import UUID

from fastapi import HTTPException
from pydantic import ValidationError
from starlette.requests import Request

from backend.api.formacao_academica import (
    EdicaoFormacaoAcademicaRequisicao,
    criar_router,
)
from backend.application.perfil_estudante import (
    EditarFormacaoAcademicaEntrada,
    FormacaoAcademicaNaoEncontrada,
)
from backend.domain import (
    FormacaoAcademica,
    FormacaoAcademicaId,
    NivelFormacaoAcademica,
    Periodo,
    RegraDeDominioViolada,
    StatusFormacaoAcademica,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_USUARIO_CLIENTE = UUID("00000000-0000-0000-0000-000000000002")
ID_FORMACAO = UUID("00000000-0000-0000-0000-0000000000f1")


# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
class EditarFormacaoAcademicaStub:
    """Substitui o caso de uso e registra entradas recebidas pela API.

    O double devolve uma entidade controlada ou lança uma falha configurada,
    sem persistência ou rede. Ele existe para isolar a tradução entre DTO,
    identidade da sessão e contrato de Application.
    """

    def __init__(self, erro: Exception | None = None) -> None:
        """Armazena falha opcional e inicia o histórico vazio.

        O construtor mantém apenas estado em memória. Ele existe para preparar
        respostas determinísticas sem executar o caso de uso real.
        """
        self.erro = erro
        self.entradas: list[EditarFormacaoAcademicaEntrada] = []

    async def executar(
        self, entrada: EditarFormacaoAcademicaEntrada
    ) -> FormacaoAcademica:
        """Registra a entrada e devolve uma formação atualizada ou falha.

        O método simula o contrato assíncrono da Application usando somente
        valores do teste. Ele existe para verificar o mapeamento do handler.
        """
        self.entradas.append(entrada)
        if self.erro is not None:
            raise self.erro
        return FormacaoAcademica(
            id=entrada.formacao_id,
            usuario_id=entrada.usuario_id,
            instituicao=entrada.instituicao,
            curso=entrada.curso,
            nivel=entrada.nivel,
            periodo=entrada.periodo,
            status=entrada.status,
        )


# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
def _rota_edicao(executor: EditarFormacaoAcademicaStub | None):
    """Localiza diretamente o handler PUT sem iniciar a aplicação ASGI.

    A função percorre as rotas registradas no router e seleciona caminho e
    método exatos. Ela existe para testar o adapter sem servidor ou framework
    iniciado.
    """
    for rota in criar_router(None, executor).routes:
        if (
            rota.path == "/formacoes-academicas/{formacao_id}"
            and "PUT" in rota.methods
        ):
            return rota.endpoint
    raise AssertionError("Rota PUT de edição de formação não encontrada.")


# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
def _request(usuario_id: UUID | None) -> Request:
    """Cria requisição mínima com principal autenticado opcional.

    O escopo ASGI local instala somente o estado que o middleware validado
    forneceria ao handler. Ele existe para testar a origem do proprietário sem
    instanciar autenticação ou aplicação.
    """
    request = Request(
        {
            "type": "http",
            "method": "PUT",
            "path": f"/formacoes-academicas/{ID_FORMACAO}",
            "headers": [],
        }
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
def _payload(**alteracoes: object) -> dict[str, object]:
    """Monta substituição completa válida com alterações pontuais.

    O dicionário usa enums e datas canônicos e permite sobrescrever campos em
    cada cenário. Ele existe para manter os testes focados no contrato HTTP.
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


# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
class EdicaoFormacaoAcademicaApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica DTO e handler PUT isolados do caso de uso e da persistência.

    Os cenários chamam diretamente a rota com executor substituído e request
    sintética. Eles existem para proteger tradução, identidade de sessão e
    respostas HTTP sem iniciar servidor ou banco.
    """

    async def test_put_responde_200_e_envia_todos_os_campos_com_usuario_da_sessao(
        self,
    ) -> None:
        """Retorna DTO explícito e encaminha a substituição completa.

        O teste envia `usuario_id` extra conflitante e compara a entrada com a
        sessão e os seis campos editáveis. Ele existe para impedir troca de
        proprietário e perda no mapeamento do request.
        """
        executor = EditarFormacaoAcademicaStub()
        editar = _rota_edicao(executor)
        requisicao = EdicaoFormacaoAcademicaRequisicao.model_validate(
            _payload(usuario_id=str(ID_USUARIO_CLIENTE))
        )

        resposta = await editar(ID_FORMACAO, requisicao, _request(ID_USUARIO))

        self.assertEqual(resposta.id, ID_FORMACAO)
        self.assertEqual(resposta.usuario_id, ID_USUARIO)
        self.assertEqual(resposta.instituicao, "FATEC")
        self.assertEqual(resposta.curso, "ADS")
        self.assertIs(resposta.nivel, NivelFormacaoAcademica.TECNOLOGO)
        self.assertEqual(resposta.data_inicio, date(2024, 2, 1))
        self.assertEqual(resposta.data_fim, date(2030, 12, 1))
        self.assertIs(resposta.status, StatusFormacaoAcademica.EM_ANDAMENTO)
        entrada = executor.entradas[0]
        self.assertEqual(entrada.usuario_id, UsuarioId(ID_USUARIO))
        self.assertEqual(entrada.formacao_id, FormacaoAcademicaId(ID_FORMACAO))
        self.assertEqual(entrada.instituicao, "FATEC")
        self.assertEqual(entrada.curso, "ADS")
        self.assertIs(entrada.nivel, NivelFormacaoAcademica.TECNOLOGO)
        self.assertEqual(entrada.periodo, Periodo(date(2024, 2, 1), date(2030, 12, 1)))
        self.assertIs(entrada.status, StatusFormacaoAcademica.EM_ANDAMENTO)
        self.assertFalse(hasattr(requisicao, "usuario_id"))

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    async def test_ausencia_e_propriedade_alheia_resultam_no_mesmo_404(self) -> None:
        """Apresenta uma mensagem pública única para ausência ou propriedade.

        O teste injeta a mesma falha uniforme para os dois resultados do caso
        de uso e compara status e detalhe HTTP. Ele existe para não revelar a
        existência de formações de terceiros.
        """
        respostas: list[tuple[int, str]] = []
        for _ in ("inexistente", "alheia"):
            executor = EditarFormacaoAcademicaStub(
                erro=FormacaoAcademicaNaoEncontrada(
                    "Formação acadêmica não encontrada."
                )
            )
            editar = _rota_edicao(executor)
            with self.assertRaises(HTTPException) as contexto:
                await editar(
                    ID_FORMACAO,
                    EdicaoFormacaoAcademicaRequisicao.model_validate(_payload()),
                    _request(ID_USUARIO),
                )
            respostas.append(
                (contexto.exception.status_code, contexto.exception.detail)
            )
        self.assertEqual(respostas[0], respostas[1])
        self.assertEqual(respostas[0], (404, "Formação acadêmica não encontrada."))

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    async def test_violacao_de_dominio_vira_422_com_mensagem_segura(self) -> None:
        """Mapeia falha de domínio a detalhe estável sem conteúdo interno.

        O executor lança regra com texto confidencial e o handler substitui a
        mensagem por uma descrição segura. Ele existe para estabilizar a
        resposta pública da fronteira HTTP.
        """
        executor = EditarFormacaoAcademicaStub(
            erro=RegraDeDominioViolada("detalhe interno confidencial")
        )
        editar = _rota_edicao(executor)

        with self.assertRaises(HTTPException) as contexto:
            await editar(
                ID_FORMACAO,
                EdicaoFormacaoAcademicaRequisicao.model_validate(_payload()),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(
            contexto.exception.detail,
            "A formação informada viola as regras de edição.",
        )
        self.assertNotIn("confidencial", contexto.exception.detail)

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    async def test_sem_estado_de_sessao_responde_401_sem_chamar_executor(self) -> None:
        """Recusa chamada sem principal autenticado antes da Application.

        O teste chama o handler com request sem `usuario_id` e inspeciona o
        histórico vazio do executor. Ele existe para preservar a pré-condição
        de sessão no adapter além da proteção anterior do middleware.
        """
        executor = EditarFormacaoAcademicaStub()
        editar = _rota_edicao(executor)

        with self.assertRaises(HTTPException) as contexto:
            await editar(
                ID_FORMACAO,
                EdicaoFormacaoAcademicaRequisicao.model_validate(_payload()),
                _request(None),
            )

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    async def test_executor_indisponivel_responde_503(self) -> None:
        """Sinaliza indisponibilidade de composição sem tentar executar.

        O teste cria o router sem executor e chama a rota com sessão válida.
        Ele existe para manter explícito o estado operacional da dependência.
        """
        editar = _rota_edicao(None)

        with self.assertRaises(HTTPException) as contexto:
            await editar(
                ID_FORMACAO,
                EdicaoFormacaoAcademicaRequisicao.model_validate(_payload()),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 503)

    def test_dto_rejeita_enum_e_textos_invalidos(self) -> None:
        """Aplica no DTO de edição os mesmos enums e limites do cadastro.

        O teste valida valores por meio do DTO derivado, que herda os
        validadores existentes. Ele existe para impedir regras divergentes
        entre criação e substituição.
        """
        for alteracao in (
            {"nivel": "nivel_invalido"},
            {"instituicao": "   "},
            {"curso": "x" * 201},
            {"curso": "x\ny"},
        ):
            with self.subTest(alteracao=alteracao):
                with self.assertRaises(ValidationError):
                    EdicaoFormacaoAcademicaRequisicao.model_validate(
                        _payload(**alteracao)
                    )

    def test_data_fim_precisa_estar_presente_mas_aceita_null(self) -> None:
        """Distingue omissão de campo de limpeza explícita com null.

        O teste valida a substituição sem `data_fim` e com valor nulo. Ele
        existe para evitar que uma edição incompleta apague previsão sem
        intenção explícita.
        """
        dados_sem_data_fim = _payload()
        del dados_sem_data_fim["data_fim"]
        with self.assertRaises(ValidationError):
            EdicaoFormacaoAcademicaRequisicao.model_validate(dados_sem_data_fim)

        requisicao = EdicaoFormacaoAcademicaRequisicao.model_validate(
            _payload(data_fim=None)
        )
        self.assertIsNone(requisicao.data_fim)
        self.assertIn("null", EdicaoFormacaoAcademicaRequisicao.model_fields["data_fim"].description)

    def test_router_registra_put_no_caminho_da_formacao(self) -> None:
        """Confirma método e caminho que identificam a edição.

        O teste inspeciona a configuração local do router sem iniciar servidor.
        Ele existe para proteger o contrato de rota implementado pelo adapter.
        """
        rota = next(
            rota
            for rota in criar_router(None, EditarFormacaoAcademicaStub()).routes
            if rota.path == "/formacoes-academicas/{formacao_id}"
        )
        self.assertIn("PUT", rota.methods)
