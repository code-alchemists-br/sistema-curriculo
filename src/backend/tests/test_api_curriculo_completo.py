"""Testa a fronteira HTTP de leitura e substituição do currículo completo."""

import unittest
from datetime import date, timedelta
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from backend.api.curriculo_completo import (
    ModeloRequisicao,
    SecaoRequisicao,
    criar_router_curriculo_completo,
)
from backend.application.curriculo_completo import (
    CurriculoCompleto,
    DadosPessoaisSalvos,
    DadosRepetidos,
    GerenciarCurriculoCompleto,
    IdiomaItem,
    RepositorioCurriculoCompleto,
    SecaoSubstituivel,
)
from backend.domain.modelo_curriculo import ModeloCurriculo

USUARIO = UUID("00000000-0000-0000-0000-0000000000d1")


class RepositorioFalso(RepositorioCurriculoCompleto):
    """Substitui a persistência por memória, com falha de unicidade opcional.

    Existe para exercitar o router com o caso de uso real e sem banco.
    """

    def __init__(self, curriculo: CurriculoCompleto | None = None, repetido: bool = False) -> None:
        """Guarda o currículo da leitura, a falha simulada e os históricos.

        Existe para que cada teste configure o cenário.
        """
        self.curriculo = curriculo
        self.repetido = repetido
        self.trocas: list[tuple] = []
        self.modelos: list[tuple] = []

    async def ler(self, usuario_id: UUID) -> CurriculoCompleto | None:
        """Devolve o currículo configurado.

        Existe para simular a leitura do banco.
        """
        return self.curriculo

    async def substituir(self, usuario_id, secao, entidades, curriculo_lattes=None) -> None:
        """Registra a troca ou simula itens repetidos.

        Existe para conferir o que chegou à persistência e testar o 409.
        """
        if self.repetido:
            raise DadosRepetidos("repetidos")
        self.trocas.append((usuario_id, secao, entidades, curriculo_lattes))

    async def salvar_modelo(self, usuario_id: UUID, modelo: ModeloCurriculo) -> None:
        """Registra o modelo recebido.

        Existe para conferir a gravação do modelo.
        """
        self.modelos.append((usuario_id, modelo))


def _rota(router: APIRouter, metodo: str, caminho: str):
    """Localiza o handler registrado para o método e caminho.

    Existe para chamar o handler diretamente, sem servidor.
    """
    for rota in router.routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota.endpoint
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


def _request() -> Request:
    """Monta uma requisição mínima com o estudante autenticado no estado.

    Existe para simular o que o middleware de sessão instala.
    """
    request = Request({"type": "http", "method": "GET", "path": "/", "headers": []})
    request.state.usuario_id = USUARIO
    return request


BASE = "/estudantes/me/curriculo"


class CurriculoCompletoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica as rotas ``GET``/``PUT`` de ``/estudantes/me/curriculo``.

    Usa o caso de uso real sobre um repositório falso. Existe para proteger a
    validação por seção e a tradução de falhas em 404, 409, 422 e 503.
    """

    async def test_consultar_devolve_o_curriculo_do_estudante(self) -> None:
        """Devolve o currículo salvo e responde 404 para conta inexistente.

        Existe para que o frontend carregue o currículo do banco.
        """
        salvo = CurriculoCompleto(dados_pessoais=DadosPessoaisSalvos(nome="Ana", email="a@x.com"))
        consultar = _rota(
            criar_router_curriculo_completo(GerenciarCurriculoCompleto(RepositorioFalso(salvo))),
            "GET",
            BASE,
        )
        self.assertEqual((await consultar(_request())).dados_pessoais.nome, "Ana")

        consultar_vazio = _rota(
            criar_router_curriculo_completo(GerenciarCurriculoCompleto(RepositorioFalso(None))),
            "GET",
            BASE,
        )
        with self.assertRaises(HTTPException) as contexto:
            await consultar_vazio(_request())
        self.assertEqual(contexto.exception.status_code, 404)

    async def test_substituir_valida_itens_e_grava_a_secao(self) -> None:
        """Converte os itens pelo modelo da seção e responde 204.

        Existe para garantir que a lista inteira chegue à persistência.
        """
        repositorio = RepositorioFalso()
        substituir = _rota(
            criar_router_curriculo_completo(GerenciarCurriculoCompleto(repositorio)),
            "PUT",
            f"{BASE}/{{secao}}",
        )

        resposta = await substituir(
            _request(),
            SecaoSubstituivel.IDIOMAS,
            SecaoRequisicao(itens=[{"idioma": "Inglês", "nivel": "avancado"}]),
        )

        self.assertEqual(resposta.status_code, 204)
        usuario, secao, entidades, _ = repositorio.trocas[0]
        self.assertEqual((usuario, secao), (USUARIO, SecaoSubstituivel.IDIOMAS))
        self.assertEqual(entidades[0].idioma, "Inglês")

    async def test_item_fora_do_formato_vira_422_com_os_campos(self) -> None:
        """Responde 422 apontando o campo ausente no item.

        Existe para que a tela saiba o que corrigir.
        """
        substituir = _rota(
            criar_router_curriculo_completo(GerenciarCurriculoCompleto(RepositorioFalso())),
            "PUT",
            f"{BASE}/{{secao}}",
        )

        with self.assertRaises(HTTPException) as contexto:
            await substituir(_request(), SecaoSubstituivel.IDIOMAS, SecaoRequisicao(itens=[{"idioma": "Inglês"}]))

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(contexto.exception.detail[0]["loc"], (0, "nivel"))

    async def test_regra_de_dominio_vira_422_e_repetidos_viram_409(self) -> None:
        """Traduz regra do domínio violada em 422 e itens repetidos em 409.

        Existe para separar dado inválido de dado duplicado na resposta.
        """
        futuro = (date.today() + timedelta(days=10)).isoformat()
        cenarios = (
            (
                RepositorioFalso(),
                SecaoSubstituivel.EXPERIENCIAS,
                [{"empresa": "X", "cargo": "Dev", "descricao": "Fiz.", "data_inicio": futuro}],
                422,
            ),
            (
                RepositorioFalso(repetido=True),
                SecaoSubstituivel.IDIOMAS,
                [IdiomaItem(idioma="Inglês", nivel="basico").model_dump()],
                409,
            ),
        )
        for repositorio, secao, itens, status in cenarios:
            with self.subTest(status=status):
                substituir = _rota(
                    criar_router_curriculo_completo(GerenciarCurriculoCompleto(repositorio)),
                    "PUT",
                    f"{BASE}/{{secao}}",
                )
                with self.assertRaises(HTTPException) as contexto:
                    await substituir(_request(), secao, SecaoRequisicao(itens=itens))
                self.assertEqual(contexto.exception.status_code, status)

    async def test_salvar_modelo_e_ausencia_de_banco(self) -> None:
        """Grava o modelo com 204 e responde 503 quando não há banco.

        Existe para cobrir a rota do modelo e a falta de persistência.
        """
        repositorio = RepositorioFalso()
        salvar = _rota(
            criar_router_curriculo_completo(GerenciarCurriculoCompleto(repositorio)),
            "PUT",
            f"{BASE}/modelo",
        )
        resposta = await salvar(_request(), ModeloRequisicao(modelo=ModeloCurriculo.COMPACTO))
        self.assertEqual(resposta.status_code, 204)
        self.assertEqual(repositorio.modelos, [(USUARIO, ModeloCurriculo.COMPACTO)])

        sem_banco = _rota(criar_router_curriculo_completo(None), "PUT", f"{BASE}/modelo")
        with self.assertRaises(HTTPException) as contexto:
            await sem_banco(_request(), ModeloRequisicao(modelo=ModeloCurriculo.COMPACTO))
        self.assertEqual(contexto.exception.status_code, 503)


if __name__ == "__main__":
    unittest.main()
