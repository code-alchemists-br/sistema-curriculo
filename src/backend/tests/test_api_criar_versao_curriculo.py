"""Testa unitariamente a rota HTTP de criação de versão de currículo."""

import unittest
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from backend.api.versao_curriculo import (
    CriarVersaoCurriculoRequisicao,
    VersaoCurriculoResposta,
    criar_router,
)
from backend.application import CriarVersaoCurriculoEntrada
from backend.domain import Curriculo, CurriculoId, RegraDeDominioViolada, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001

CAMINHO = "/estudantes/{usuario_id}/curriculos"


class CriarVersaoCurriculoExecutorDouble:
    """Substitui o caso de uso de criação e registra as entradas recebidas.

    O double devolve um resultado ou levanta um erro pré-configurado, sem tocar
    portas, banco ou domínio de verdade. Ele existe para testar a tradução HTTP
    da rota isoladamente da orquestração da Application.
    """

    def __init__(self, resultado: Curriculo | None = None, erro: Exception | None = None) -> None:
        """Guarda o comportamento configurado e inicia o histórico de chamadas.

        O construtor não acessa recursos externos. Ele existe para permitir que
        cada teste configure sucesso ou falha de forma explícita.
        """
        self._resultado = resultado
        self._erro = erro
        self.entradas: list[CriarVersaoCurriculoEntrada] = []

    async def executar(self, entrada: CriarVersaoCurriculoEntrada) -> Curriculo:
        """Registra a entrada recebida e devolve o resultado ou levanta o erro.

        O método aguarda de forma trivial, sem I/O real. Ele existe para tornar
        observável o que o handler HTTP enviou ao caso de uso.
        """
        self.entradas.append(entrada)
        if self._erro is not None:
            raise self._erro
        if self._resultado is None:
            raise AssertionError("O double não recebeu resultado nem erro configurado.")
        return self._resultado


def _rota(router: APIRouter, caminho: str, metodo: str):
    """Localiza a rota registrada para inspeção e chamada direta em teste.

    A função varre as rotas do router por caminho e método HTTP e devolve o
    objeto da rota, que expõe o endpoint e a configuração declarada. Ela existe
    para exercitar o handler sem iniciar servidor ASGI ou cliente HTTP real.
    """
    for rota in router.routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


def _criar_curriculo(usuario_id: UsuarioId, is_public: bool = True) -> Curriculo:
    """Cria uma versão de currículo válida para servir de resultado do double.

    A função monta o agregado sem acessar gerador, banco ou relógio e permite
    informar o proprietário e a visibilidade. Ela existe para reduzir repetição
    mantendo cada teste focado na tradução HTTP.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id,
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=is_public,
    )


class CriarVersaoCurriculoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP da criação de versão pela rota POST.

    A classe substitui o caso de uso por um double e observa o que a rota envia
    e devolve. Ela existe para testar a unidade de interface isoladamente da
    Application e da infraestrutura.
    """

    async def test_cria_versao_e_devolve_dados_publicos(self) -> None:
        """Confirma resposta pública e a entrada correta enviada ao caso de uso.

        O teste configura um double de sucesso, chama o handler diretamente e
        compara a resposta com o agregado devolvido e a entrada registrada.
        """
        usuario_id = uuid4()
        curriculo = _criar_curriculo(UsuarioId(usuario_id), is_public=True)
        executor = CriarVersaoCurriculoExecutorDouble(resultado=curriculo)
        criar = _rota(criar_router(None, executor), CAMINHO, "POST").endpoint

        resposta = await criar(
            usuario_id=usuario_id,
            requisicao=CriarVersaoCurriculoRequisicao(titulo_versao="Estágio em TI", layout="classico", is_public=True),
        )

        self.assertEqual(resposta.id, curriculo.id.valor)
        self.assertEqual(resposta.titulo_versao, "Estágio em TI")
        self.assertEqual(resposta.layout, "classico")
        self.assertTrue(resposta.is_public)
        self.assertEqual(
            executor.entradas,
            [
                CriarVersaoCurriculoEntrada(
                    usuario_id=UsuarioId(usuario_id),
                    titulo_versao="Estágio em TI",
                    layout="classico",
                    is_public=True,
                )
            ],
        )

    async def test_declara_status_201_e_resposta_publica(self) -> None:
        """Confirma o status de sucesso e o modelo de resposta declarados na rota.

        O teste inspeciona a configuração da rota registrada, já que a chamada
        direta ao handler não passa pela camada que aplica o status. Ele existe
        para proteger o contrato HTTP de criação.
        """
        rota = _rota(criar_router(None, None), CAMINHO, "POST")

        self.assertEqual(rota.status_code, 201)
        self.assertIs(rota.response_model, VersaoCurriculoResposta)

    async def test_visibilidade_padrao_eh_privada(self) -> None:
        """Confirma que a omissão da visibilidade resulta em versão privada.

        O teste cria a requisição sem informar a visibilidade e observa o valor
        enviado ao caso de uso. Ele existe para proteger o padrão de privacidade
        da criação.
        """
        usuario_id = uuid4()
        executor = CriarVersaoCurriculoExecutorDouble(
            resultado=_criar_curriculo(UsuarioId(usuario_id), is_public=False)
        )
        criar = _rota(criar_router(None, executor), CAMINHO, "POST").endpoint

        resposta = await criar(
            usuario_id=usuario_id,
            requisicao=CriarVersaoCurriculoRequisicao(titulo_versao="Estágio em TI", layout="classico"),
        )

        self.assertFalse(executor.entradas[0].is_public)
        self.assertFalse(resposta.is_public)

    async def test_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum caso de uso de criação foi injetado.

        O teste chama o handler sem executor e observa a indisponibilidade
        explícita antes de qualquer outra decisão.
        """
        criar = _rota(criar_router(None, None), CAMINHO, "POST").endpoint

        with self.assertRaises(HTTPException) as contexto:
            await criar(
                usuario_id=uuid4(),
                requisicao=CriarVersaoCurriculoRequisicao(titulo_versao="Estágio em TI", layout="classico"),
            )

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_violacao_de_dominio_vira_422(self) -> None:
        """Confirma 422 quando o caso de uso sinaliza violação de regra de domínio.

        O teste configura o double para levantar a falha de domínio e observa a
        tradução HTTP preservando a mensagem. Ele existe para proteger o
        mapeamento de erro da fronteira.
        """
        executor = CriarVersaoCurriculoExecutorDouble(
            erro=RegraDeDominioViolada("Título da versão do currículo não pode ser vazio.")
        )
        criar = _rota(criar_router(None, executor), CAMINHO, "POST").endpoint

        with self.assertRaises(HTTPException) as contexto:
            await criar(
                usuario_id=uuid4(),
                requisicao=CriarVersaoCurriculoRequisicao(titulo_versao="   ", layout="classico"),
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(contexto.exception.detail, "Título da versão do currículo não pode ser vazio.")
        self.assertEqual(len(executor.entradas), 1)


class CriarVersaoCurriculoRequisicaoTestCase(unittest.TestCase):
    """Verifica a validação estrutural do DTO de criação na fronteira.

    A classe constrói o DTO com dados fora do formato esperado. Ela existe para
    proteger campos obrigatórios e limites de tamanho antes de qualquer chamada
    ao caso de uso.
    """

    def test_rejeita_titulo_vazio_e_layout_ausente(self) -> None:
        """Confirma que título vazio ou layout ausente não formam uma requisição.

        O teste tenta construir o DTO sem os campos obrigatórios e observa a
        falha de validação estrutural, que o framework traduziria em 422.
        """
        with self.assertRaises(ValidationError):
            CriarVersaoCurriculoRequisicao(titulo_versao="", layout="classico")
        with self.assertRaises(ValidationError):
            CriarVersaoCurriculoRequisicao(titulo_versao="Estágio em TI")  # type: ignore[call-arg]
