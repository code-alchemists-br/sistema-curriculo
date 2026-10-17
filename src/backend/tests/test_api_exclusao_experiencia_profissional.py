"""Testa unitariamente a tradução HTTP da exclusão de experiência profissional."""

import unittest
from datetime import date, datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from starlette.requests import Request

from backend.api.experiencia_profissional import criar_router
from backend.api.factory import create_app
from backend.application.edicao_experiencia_profissional import (
    ExperienciaProfissionalNaoEncontrada,
)
from backend.application.exclusao_experiencia_profissional import (
    ExcluirExperienciaProfissionalEntrada,
)
from backend.domain import (
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    Periodo,
    UsuarioId,
)

CAMINHO_EXCLUSAO = "/experiencias-profissionais/{experiencia_id}"
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ID_EXPERIENCIA = UUID("00000000-0000-0000-0000-0000000000e1")
ID_INEXISTENTE = UUID("00000000-0000-0000-0000-0000000000ff")
INSTANTE = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)


class ExcluirExperienciaProfissionalStub:
    """Substitui o caso de uso de exclusão e registra as entradas recebidas.

    O double devolve uma experiência excluída montada a partir da entrada ou
    lança uma falha configurada, sem persistência, relógio ou rede. Ele existe
    para isolar a tradução entre rota, identidade da sessão e Application.
    """

    def __init__(self, erro: Exception | None = None) -> None:
        """Armazena a falha opcional e inicia o histórico vazio.

        O construtor mantém apenas estado em memória. Ele existe para preparar
        respostas determinísticas sem executar o caso de uso real.
        """
        self.erro = erro
        self.entradas: list[ExcluirExperienciaProfissionalEntrada] = []

    async def executar(
        self, entrada: ExcluirExperienciaProfissionalEntrada
    ) -> ExperienciaProfissional:
        """Registra a entrada e devolve a experiência excluída ou falha.

        O método simula o contrato assíncrono e idempotente da Application. Ele
        existe para verificar o mapeamento do handler.
        """
        self.entradas.append(entrada)
        if self.erro is not None:
            raise self.erro
        return ExperienciaProfissional(
            id=entrada.experiencia_id,
            usuario_id=entrada.usuario_id,
            empresa="Instituto Exemplo",
            cargo="Estagiária",
            descricao="Construiu integrações internas.",
            periodo=Periodo(date(2022, 1, 1), date(2023, 6, 1)),
            deleted_at=INSTANTE,
        )


def _rota_exclusao(executor: ExcluirExperienciaProfissionalStub | None):
    """Localiza diretamente o handler DELETE sem iniciar a aplicação ASGI.

    A função percorre as rotas registradas no router e seleciona caminho e
    método exatos. Ela existe para testar o adapter sem servidor iniciado.
    """
    for rota in criar_router(None, None, executor).routes:
        if rota.path == CAMINHO_EXCLUSAO and "DELETE" in rota.methods:
            return rota.endpoint
    raise AssertionError("Rota DELETE de exclusão de experiência não encontrada.")


def _request(usuario_id: UUID | None) -> Request:
    """Cria requisição mínima com principal autenticado opcional.

    O escopo ASGI local instala somente o estado que o middleware de sessão
    forneceria ao handler. Ele existe para testar a origem do proprietário sem
    instanciar autenticação ou aplicação.
    """
    request = Request(
        {
            "type": "http",
            "method": "DELETE",
            "path": f"/experiencias-profissionais/{ID_EXPERIENCIA}",
            "headers": [],
        }
    )
    if usuario_id is not None:
        request.state.usuario_id = usuario_id
    return request


class ExclusaoExperienciaProfissionalApiTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica o handler DELETE isolado do caso de uso e da persistência.

    Os cenários chamam diretamente a rota com executor substituído e request
    sintética. Eles existem para proteger o caso de recurso inexistente, a
    identidade da sessão e as respostas HTTP da exclusão.
    """

    async def test_experiencia_inexistente_responde_404_generico(self) -> None:
        """Converte experiência inexistente em 404 com mensagem genérica.

        O caso de uso sinaliza que o ID informado não existe e o handler deve
        responder 404 sem repetir o detalhe interno. O teste existe para cobrir
        o recurso inexistente pedido pela tarefa.
        """
        executor = ExcluirExperienciaProfissionalStub(
            erro=ExperienciaProfissionalNaoEncontrada("detalhe interno")
        )

        with self.assertRaises(HTTPException) as contexto:
            await _rota_exclusao(executor)(ID_INEXISTENTE, _request(ID_USUARIO))

        self.assertEqual(contexto.exception.status_code, 404)
        self.assertEqual(
            contexto.exception.detail, "Experiência profissional não encontrada."
        )
        self.assertEqual(
            executor.entradas,
            [
                ExcluirExperienciaProfissionalEntrada(
                    usuario_id=UsuarioId(ID_USUARIO),
                    experiencia_id=ExperienciaProfissionalId(ID_INEXISTENTE),
                )
            ],
        )

    async def test_inexistente_e_alheia_resultam_no_mesmo_404(self) -> None:
        """Apresenta a mesma resposta para ausência ou propriedade alheia.

        O caso de uso devolve a mesma falha uniforme nos dois cenários e o
        teste compara status e detalhe. Ele existe para não revelar a
        existência de experiências de terceiros.
        """
        respostas: list[tuple[int, str]] = []
        for _ in ("inexistente", "alheia"):
            executor = ExcluirExperienciaProfissionalStub(
                erro=ExperienciaProfissionalNaoEncontrada("detalhe interno")
            )
            with self.assertRaises(HTTPException) as contexto:
                await _rota_exclusao(executor)(ID_EXPERIENCIA, _request(ID_USUARIO))
            respostas.append((contexto.exception.status_code, contexto.exception.detail))

        self.assertEqual(respostas[0], respostas[1])

    async def test_exclusao_valida_nao_devolve_corpo_e_usa_usuario_da_sessao(
        self,
    ) -> None:
        """Exclui sem corpo de resposta e envia a entrada com ID da rota e sessão.

        O teste chama o handler com sessão válida e inspeciona a entrada
        registrada. Ele existe para impedir que a exclusão aceite identidade do
        cliente.
        """
        executor = ExcluirExperienciaProfissionalStub()

        resultado = await _rota_exclusao(executor)(ID_EXPERIENCIA, _request(ID_USUARIO))

        self.assertIsNone(resultado)
        self.assertEqual(
            executor.entradas,
            [
                ExcluirExperienciaProfissionalEntrada(
                    usuario_id=UsuarioId(ID_USUARIO),
                    experiencia_id=ExperienciaProfissionalId(ID_EXPERIENCIA),
                )
            ],
        )

    async def test_repeticao_pelo_dono_tambem_responde_sem_erro(self) -> None:
        """Mantém sucesso quando a experiência já estava excluída.

        O caso de uso idempotente devolve o estado excluído nas duas chamadas e
        o handler não levanta erro em nenhuma delas. O teste existe para que
        repetir o DELETE responda 204 como a primeira exclusão.
        """
        executor = ExcluirExperienciaProfissionalStub()
        excluir = _rota_exclusao(executor)

        primeira = await excluir(ID_EXPERIENCIA, _request(ID_USUARIO))
        segunda = await excluir(ID_EXPERIENCIA, _request(ID_USUARIO))

        self.assertEqual((primeira, segunda), (None, None))
        self.assertEqual(len(executor.entradas), 2)

    async def test_sem_sessao_responde_401_sem_chamar_executor(self) -> None:
        """Recusa chamada sem principal autenticado antes da Application.

        O teste chama o handler com request sem ``usuario_id`` e inspeciona o
        histórico vazio do executor. Ele existe para preservar a pré-condição
        de sessão no adapter além da proteção do middleware.
        """
        executor = ExcluirExperienciaProfissionalStub()

        with self.assertRaises(HTTPException) as contexto:
            await _rota_exclusao(executor)(ID_EXPERIENCIA, _request(None))

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    async def test_executor_indisponivel_responde_503(self) -> None:
        """Sinaliza indisponibilidade de composição sem tentar executar.

        O router é criado sem executor de exclusão e chamado com sessão válida.
        O teste existe para manter explícito o estado da dependência.
        """
        with self.assertRaises(HTTPException) as contexto:
            await _rota_exclusao(None)(ID_EXPERIENCIA, _request(ID_USUARIO))

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(contexto.exception.detail, "Exclusão indisponível.")

    def test_fabrica_registra_delete_com_resposta_204(self) -> None:
        """Confirma que a aplicação composta expõe a rota de exclusão.

        O OpenAPI do app criado com o executor injetado é inspecionado para a
        operação DELETE e seu status de sucesso. O teste existe para impedir que
        o handler fique fora da composição.
        """
        app = create_app(
            excluir_experiencia_profissional=ExcluirExperienciaProfissionalStub()
        )

        operacao = app.openapi()["paths"][CAMINHO_EXCLUSAO]["delete"]

        self.assertIn("204", operacao["responses"])
