"""Testa unitariamente a tradução HTTP da edição de experiência profissional."""

import unittest
from datetime import date
from uuid import UUID

from fastapi import HTTPException
from pydantic import ValidationError
from starlette.requests import Request

from backend.api.experiencia_profissional import (
    EdicaoExperienciaProfissionalRequisicao,
    criar_router,
)
from backend.api.factory import create_app
from backend.application.edicao_experiencia_profissional import (
    EditarExperienciaProfissionalEntrada,
    ExperienciaProfissionalNaoEncontrada,
)
from backend.domain import (
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    Periodo,
    RegraDeDominioViolada,
    UsuarioId,
)

CAMINHO_EDICAO = "/experiencias-profissionais/{experiencia_id}"
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_USUARIO_CLIENTE = UUID("00000000-0000-0000-0000-000000000002")
ID_EXPERIENCIA = UUID("00000000-0000-0000-0000-0000000000e1")


class EditarExperienciaProfissionalStub:
    """Substitui o caso de uso de edição e registra as entradas recebidas.

    O double devolve uma entidade montada a partir da entrada ou lança uma
    falha configurada, sem persistência ou rede. Ele existe para isolar a
    tradução entre DTO, identidade da sessão e contrato da Application.
    """

    def __init__(self, erro: Exception | None = None) -> None:
        """Armazena a falha opcional e inicia o histórico vazio.

        O construtor mantém apenas estado em memória. Ele existe para preparar
        respostas determinísticas sem executar o caso de uso real.
        """
        self.erro = erro
        self.entradas: list[EditarExperienciaProfissionalEntrada] = []

    async def executar(
        self, entrada: EditarExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Registra a entrada e devolve a experiência atualizada ou falha.

        O método simula o contrato assíncrono da Application usando somente
        valores do teste. Ele existe para verificar o mapeamento do handler.
        """
        self.entradas.append(entrada)
        if self.erro is not None:
            raise self.erro
        return ExperienciaProfissional(
            id=entrada.experiencia_id,
            usuario_id=entrada.usuario_id,
            empresa=entrada.empresa,
            cargo=entrada.cargo,
            descricao=entrada.descricao,
            periodo=entrada.periodo,
        )


def _rota_edicao(executor: EditarExperienciaProfissionalStub | None):
    """Localiza diretamente o handler PUT sem iniciar a aplicação ASGI.

    A função percorre as rotas registradas no router e seleciona caminho e
    método exatos. Ela existe para testar o adapter sem servidor iniciado.
    """
    for rota in criar_router(None, executor).routes:
        if rota.path == CAMINHO_EDICAO and "PUT" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota PUT de edição de experiência não encontrada.")


def _request(usuario_id: UUID | None) -> Request:
    """Cria requisição mínima com principal autenticado opcional.

    O escopo ASGI local instala somente o estado que o middleware de sessão
    forneceria ao handler. Ele existe para testar a origem do proprietário sem
    instanciar autenticação ou aplicação.
    """
    request = Request(
        {
            "type": "http",
            "method": "PUT",
            "path": f"/experiencias-profissionais/{ID_EXPERIENCIA}",
            "headers": [],
        }
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


def _payload(**alteracoes: object) -> dict[str, object]:
    """Monta substituição completa válida com alterações pontuais.

    O dicionário usa textos e datas canônicos e permite sobrescrever campos em
    cada cenário. Ele existe para manter os testes focados no contrato HTTP.
    """
    dados: dict[str, object] = {
        "empresa": "Nova Empresa",
        "cargo": "Desenvolvedora",
        "descricao": "Mantém APIs em produção.",
        "data_inicio": "2023-07-01",
        "data_fim": None,
    }
    dados.update(alteracoes)
    return dados


def _requisicao(**alteracoes: object) -> EdicaoExperienciaProfissionalRequisicao:
    """Valida o payload no DTO de edição.

    A função reaproveita ``_payload`` e aplica a validação do Pydantic. Ela
    existe para reduzir repetição nas chamadas diretas ao handler.
    """
    return EdicaoExperienciaProfissionalRequisicao.model_validate(_payload(**alteracoes))


class EdicaoExperienciaProfissionalApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica DTO e handler PUT isolados do caso de uso e da persistência.

    Os cenários chamam diretamente a rota com executor substituído e request
    sintética. Eles existem para proteger a tradução, a identidade da sessão e
    o mapeamento de erros de domínio para respostas HTTP.
    """

    async def test_put_responde_com_dados_e_usa_usuario_da_sessao(self) -> None:
        """Devolve o DTO público e encaminha a substituição completa.

        O teste envia um ``usuario_id`` extra conflitante no corpo e compara a
        entrada com a sessão, o ID da rota e os campos editáveis. Ele existe
        para impedir troca de proprietário e perda no mapeamento.
        """
        executor = EditarExperienciaProfissionalStub()
        editar = _rota_edicao(executor)

        resposta = await editar(
            ID_EXPERIENCIA,
            _requisicao(usuario_id=str(ID_USUARIO_CLIENTE)),
            _request(ID_USUARIO),
        )

        self.assertEqual((resposta.id, resposta.usuario_id), (ID_EXPERIENCIA, ID_USUARIO))
        self.assertEqual(
            (resposta.empresa, resposta.cargo, resposta.descricao),
            ("Nova Empresa", "Desenvolvedora", "Mantém APIs em produção."),
        )
        self.assertEqual((resposta.data_inicio, resposta.data_fim), (date(2023, 7, 1), None))
        self.assertEqual(
            executor.entradas,
            [
                EditarExperienciaProfissionalEntrada(
                    usuario_id=UsuarioId(ID_USUARIO),
                    experiencia_id=ExperienciaProfissionalId(ID_EXPERIENCIA),
                    empresa="Nova Empresa",
                    cargo="Desenvolvedora",
                    descricao="Mantém APIs em produção.",
                    periodo=Periodo(date(2023, 7, 1)),
                )
            ],
        )

    async def test_ausencia_e_propriedade_alheia_resultam_no_mesmo_404(self) -> None:
        """Apresenta uma resposta pública única para ausência ou propriedade alheia.

        O caso de uso sinaliza a mesma falha uniforme para os dois resultados e
        o teste compara status e detalhe HTTP. Ele existe para não revelar a
        existência de experiências de terceiros.
        """
        respostas: list[tuple[int, str]] = []
        for _ in ("inexistente", "alheia"):
            executor = EditarExperienciaProfissionalStub(
                erro=ExperienciaProfissionalNaoEncontrada("detalhe interno")
            )
            with self.assertRaises(HTTPException) as contexto:
                await _rota_edicao(executor)(
                    ID_EXPERIENCIA, _requisicao(), _request(ID_USUARIO)
                )
            respostas.append((contexto.exception.status_code, contexto.exception.detail))

        self.assertEqual(respostas[0], respostas[1])
        self.assertEqual(respostas[0], (404, "Experiência profissional não encontrada."))

    async def test_violacao_de_dominio_vira_422_com_mensagem_generica(self) -> None:
        """Mapeia falha de domínio a detalhe estável sem conteúdo interno.

        O executor lança uma regra com texto confidencial e o handler o
        substitui por uma mensagem genérica. O teste existe para que a resposta
        pública não exponha detalhes das regras de domínio.
        """
        executor = EditarExperienciaProfissionalStub(
            erro=RegraDeDominioViolada("detalhe interno confidencial")
        )

        with self.assertRaises(HTTPException) as contexto:
            await _rota_edicao(executor)(
                ID_EXPERIENCIA, _requisicao(), _request(ID_USUARIO)
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(
            contexto.exception.detail,
            "A experiência informada viola as regras de edição.",
        )

    async def test_periodo_invertido_vira_422_sem_chamar_executor(self) -> None:
        """Converte término anterior ao início em 422 antes da Application.

        O ``Periodo`` rejeita a cronologia ao montar a entrada, e o handler
        traduz a regra com a mesma mensagem genérica. O teste existe para
        cobrir a violação de domínio originada na própria fronteira.
        """
        executor = EditarExperienciaProfissionalStub()

        with self.assertRaises(HTTPException) as contexto:
            await _rota_edicao(executor)(
                ID_EXPERIENCIA,
                _requisicao(data_inicio="2024-05-01", data_fim="2024-01-01"),
                _request(ID_USUARIO),
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(
            contexto.exception.detail,
            "A experiência informada viola as regras de edição.",
        )
        self.assertEqual(executor.entradas, [])

    async def test_sem_estado_de_sessao_responde_401_sem_chamar_executor(self) -> None:
        """Recusa chamada sem principal autenticado antes da Application.

        O teste chama o handler com request sem ``usuario_id`` e inspeciona o
        histórico vazio do executor. Ele existe para preservar a pré-condição
        de sessão no adapter além da proteção do middleware.
        """
        executor = EditarExperienciaProfissionalStub()

        with self.assertRaises(HTTPException) as contexto:
            await _rota_edicao(executor)(ID_EXPERIENCIA, _requisicao(), _request(None))

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    async def test_executor_indisponivel_responde_503(self) -> None:
        """Sinaliza indisponibilidade de composição sem tentar executar.

        O router é criado sem executor de edição e chamado com sessão válida.
        O teste existe para manter explícito o estado da dependência.
        """
        with self.assertRaises(HTTPException) as contexto:
            await _rota_edicao(None)(ID_EXPERIENCIA, _requisicao(), _request(ID_USUARIO))

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Edição indisponível.")

    def test_data_fim_precisa_estar_presente_mas_aceita_null(self) -> None:
        """Distingue omissão de ``data_fim`` de experiência em andamento.

        O teste valida a substituição sem ``data_fim`` e com valor nulo. Ele
        existe para evitar que uma edição incompleta apague o término sem
        intenção explícita.
        """
        dados_sem_data_fim = _payload()
        del dados_sem_data_fim["data_fim"]
        with self.assertRaises(ValidationError):
            EdicaoExperienciaProfissionalRequisicao.model_validate(dados_sem_data_fim)

        self.assertIsNone(_requisicao(data_fim=None).data_fim)

    def test_fabrica_registra_put_de_experiencia(self) -> None:
        """Confirma que a aplicação composta expõe a rota de edição.

        O OpenAPI do app criado com o executor injetado é inspecionado. O
        teste existe para impedir que o handler fique fora da composição.
        """
        app = create_app(editar_experiencia_profissional=EditarExperienciaProfissionalStub())

        self.assertIn("put", app.openapi()["paths"][CAMINHO_EDICAO])
