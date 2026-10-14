"""Testa unitariamente a rota HTTP de exclusão de versão de currículo."""

import unittest
from uuid import uuid4

from fastapi import HTTPException

from backend.api.exclusao_versao_curriculo import criar_router
from backend.api.factory import create_app
from backend.application import CurriculoNaoEncontrado, ExcluirVersaoCurriculoEntrada
from backend.domain import CurriculoId, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001

CAMINHO_EXCLUSAO = "/estudantes/{usuario_id}/curriculos/{curriculo_id}"


class ExclusaoExecutorDouble:
    """Substitui o caso de uso de exclusão e registra as entradas recebidas.

    O double devolve sucesso ou levanta um erro pré-configurado, sem tocar
    portas, banco ou domínio de verdade. Ele existe para testar a tradução HTTP
    da rota isoladamente da orquestração da Application.
    """

    def __init__(self, erro: Exception | None = None) -> None:
        """Guarda o erro configurado e inicia o histórico de chamadas.

        O construtor não acessa recursos externos. Ele existe para permitir que
        cada teste configure sucesso ou falha de forma explícita.
        """
        self._erro = erro
        self.entradas: list[ExcluirVersaoCurriculoEntrada] = []

    async def executar(self, entrada: ExcluirVersaoCurriculoEntrada) -> None:
        """Registra a entrada recebida e levanta o erro configurado, se houver.

        O método aguarda de forma trivial, sem I/O real. Ele existe para tornar
        observável o que o handler HTTP enviou ao caso de uso.
        """
        self.entradas.append(entrada)
        if self._erro is not None:
            raise self._erro


def _rota(executor: ExclusaoExecutorDouble | None):
    """Localiza a rota DELETE de exclusão para inspeção e chamada direta em teste.

    A função cria o router com o executor dado e varre suas rotas por caminho e
    método HTTP, devolvendo o objeto da rota, que expõe o endpoint e a
    configuração declarada. Ela existe para exercitar o handler sem iniciar
    servidor ASGI ou cliente HTTP real.
    """
    for rota in criar_router(executor).routes:
        if rota.path == CAMINHO_EXCLUSAO and "DELETE" in rota.methods:
            return rota
    raise AssertionError(f"Rota DELETE {CAMINHO_EXCLUSAO} não encontrada.")


class ExclusaoVersaoCurriculoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP da exclusão de versão pela rota DELETE.

    A classe substitui o caso de uso por um double e observa o que a rota envia
    e devolve. Ela existe para testar a unidade de interface isoladamente da
    Application e da infraestrutura.
    """

    async def test_exclui_enviando_a_entrada_correta_e_respondendo_sem_conteudo(self) -> None:
        """Confirma a entrada enviada ao caso de uso e a ausência de corpo.

        O teste chama o handler com as duas identidades e compara a entrada
        registrada no double, além do retorno vazio. Ele existe para proteger o
        contrato de exclusão.
        """
        usuario_id, curriculo_id = uuid4(), uuid4()
        executor = ExclusaoExecutorDouble()
        excluir = _rota(executor).endpoint

        resultado = await excluir(usuario_id=usuario_id, curriculo_id=curriculo_id)

        self.assertIsNone(resultado)
        self.assertEqual(
            executor.entradas,
            [ExcluirVersaoCurriculoEntrada(UsuarioId(usuario_id), CurriculoId(curriculo_id))],
        )

    async def test_declara_status_204(self) -> None:
        """Confirma o status de sucesso sem conteúdo declarado na rota.

        O teste inspeciona a configuração da rota registrada, já que a chamada
        direta ao handler não passa pela camada que aplica o status. Ele existe
        para proteger o contrato HTTP da exclusão.
        """
        self.assertEqual(_rota(None).status_code, 204)

    async def test_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum caso de uso de exclusão foi injetado.

        O teste chama o handler sem executor e observa a indisponibilidade
        explícita antes de qualquer outra decisão.
        """
        excluir = _rota(None).endpoint

        with self.assertRaises(HTTPException) as contexto:
            await excluir(usuario_id=uuid4(), curriculo_id=uuid4())

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_ausencia_ou_propriedade_alheia_vira_404(self) -> None:
        """Confirma 404 quando o caso de uso sinaliza versão não encontrada.

        O teste configura o double para a falha de não encontrado e observa a
        tradução HTTP preservando a mensagem. Ele existe para proteger a negação
        sem revelar a diferença entre ausência e propriedade alheia.
        """
        erro = CurriculoNaoEncontrado("Versão de currículo não encontrada.")
        excluir = _rota(ExclusaoExecutorDouble(erro)).endpoint

        with self.assertRaises(HTTPException) as contexto:
            await excluir(usuario_id=uuid4(), curriculo_id=uuid4())

        self.assertEqual(contexto.exception.status_code, 404)
        self.assertEqual(contexto.exception.detail, str(erro))

    async def test_fabrica_registra_a_exclusao_junto_da_edicao_no_mesmo_caminho(self) -> None:
        """Confirma que a fábrica expõe DELETE e PUT no caminho da versão.

        O teste monta a aplicação com o executor de exclusão e lê, no esquema
        OpenAPI, os métodos documentados para o caminho, sem iniciar servidor. Ele
        existe para garantir que o novo router esteja ligado e não oculte a rota
        de edição.
        """
        app = create_app(excluir_versao_curriculo=ExclusaoExecutorDouble())

        metodos = set(app.openapi()["paths"][CAMINHO_EXCLUSAO])

        self.assertTrue({"delete", "put"} <= metodos)
