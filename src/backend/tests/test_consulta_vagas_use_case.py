"""Testa o caso de uso ConsultarVagas e suas exceções canônicas de integração."""

import unittest
from typing import Any

from backend.application.consulta_vagas import (
    ConsultarVagas,
    ConsultarVagasEntrada,
    ErroIntegracaoVagas,
    RespostaInvalidaVagas,
    TimeoutIntegracaoVagas,
)
from backend.application.ports import VagaExternaDto
from backend.tests.doubles.api_vagas_grupo2 import (
    DoubleApiVagasGrupo2,
    ModoDoubleApiVagas,
)


# Double auxiliar para testes de exceções com preservação de parâmetros
# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
class DoubleBuscadorComExcecao:
    """Implementa BuscadorVagas simulando o levantamento de exceções com preservação de filtros.

    A classe reproduz falhas de integração esperadas pela Application, empacotando os filtros
    e termos recebidos na chamada. Ela existe para testar o comportamento do caso de uso sob erro.
    """

    def __init__(self, excecao_a_lancar: Exception) -> None:
        """Inicializa o double configurando a exceção a ser lançada durante a busca.

        O construtor armazena a instância da exceção que deve ser disparada. Ele existe
        para permitir a injeção determinística de falhas nos cenários de teste.
        """
        self._excecao = excecao_a_lancar

    async def buscar_vagas(
        self,
        termo: str = "",
        filtros: dict[str, Any] | None = None,
    ) -> list[VagaExternaDto]:
        """Dispara a exceção configurada simulando a falha do buscador externo.

        O método ignora os parâmetros recebidos e levanta a exceção pré-configurada.
        Ele existe para validar o repasse de erros pelo caso de uso ConsultarVagas.
        """
        raise self._excecao


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
class ConsultarVagasTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a orquestração do caso de uso de consulta de vagas.

    Os testes utilizam exclusivamente test doubles em memória, avaliando
    consultas bem-sucedidas, filtradas, vazias e propagação de erros de integração.
    A classe existe para garantir a aderência do caso de uso às regras de Application.
    """

    async def test_executa_busca_com_sucesso_retornando_vagas_do_double(self) -> None:
        """Confirma que o caso de uso recupera as vagas do buscador externo.

        O teste configura o double no modo de sucesso, executa o caso de uso com
        termo específico e verifica o retorno dos DTOs correspondentes. Ele existe
        para atestar o caminho feliz da orquestração de consulta.
        """
        double = DoubleApiVagasGrupo2(modo=ModoDoubleApiVagas.SUCESSO)
        caso_de_uso = ConsultarVagas(buscador_vagas=double)

        entrada = ConsultarVagasEntrada(termo="Python")
        resultado = await caso_de_uso.executar(entrada)

        self.assertGreaterEqual(len(resultado), 1)
        self.assertTrue(
            all(
                "python" in v.titulo.lower()
                or any("python" in r.lower() for r in v.requisitos)
                for v in resultado
            )
        )

    async def test_executa_busca_retornando_lista_vazia_quando_nenhuma_vaga_corresponde(
        self,
    ) -> None:
        """Confirma que o caso de uso devolve lista vazia quando nenhuma vaga é encontrada.

        O teste configura o double no modo de lista vazia e confere que o retorno
        é uma lista vazia sem levantar erros. Ele existe para validar buscas sem resultados.
        """
        double = DoubleApiVagasGrupo2(modo=ModoDoubleApiVagas.LISTA_VAZIA)
        caso_de_uso = ConsultarVagas(buscador_vagas=double)

        entrada = ConsultarVagasEntrada(termo="TermoInexistenteXYZ")
        resultado = await caso_de_uso.executar(entrada)

        self.assertEqual(resultado, [])

    async def test_excecao_timeout_preserva_termo_e_filtros(self) -> None:
        """Confirma que TimeoutIntegracaoVagas armazena os critérios de busca originais.

        O teste instancia a exceção de timeout com termo e filtros específicos e verifica
        suas propriedades públicas. Ele existe para certificar o cumprimento da subtarefa #240.
        """
        filtros_originais = {"modalidade": "REMOTO", "localizacao": "SP"}
        excecao = TimeoutIntegracaoVagas(
            mensagem="Tempo limite excedido na integração",
            termo="Estágio",
            filtros=filtros_originais,
        )

        self.assertIsInstance(excecao, ErroIntegracaoVagas)
        self.assertEqual(excecao.termo, "Estágio")
        self.assertEqual(excecao.filtros, filtros_originais)

        # Garantir cópia defensiva do dicionário de filtros
        filtros_originais["modalidade"] = "HIBRIDO"
        self.assertEqual(excecao.filtros["modalidade"], "REMOTO")

    async def test_excecao_resposta_invalida_preserva_termo_e_filtros(self) -> None:
        """Confirma que RespostaInvalidaVagas armazena os critérios e herda de ErroIntegracaoVagas.

        O teste instancia a exceção de resposta inválida e valida herança e atributos.
        Ele existe para validar o tratamento estruturado da subtarefa #239.
        """
        excecao = RespostaInvalidaVagas(
            mensagem="Resposta do parceiro em formato desconhecido",
            termo="QA",
            filtros={"empresa": "Tech"},
        )

        self.assertIsInstance(excecao, ErroIntegracaoVagas)
        self.assertEqual(excecao.termo, "QA")
        self.assertEqual(excecao.filtros, {"empresa": "Tech"})

    async def test_propaga_erro_de_timeout_do_buscador(self) -> None:
        """Confirma que o caso de uso propaga a falha de timeout disparada pelo buscador.

        O teste injeta um double configurado com TimeoutIntegracaoVagas e verifica
        o relançamento da exceção. Ele existe para garantir a transparência de falhas transitórias.
        """
        erro_timeout = TimeoutIntegracaoVagas(
            mensagem="Timeout",
            termo="Backend",
            filtros={"modalidade": "Remoto"},
        )
        double_com_erro = DoubleBuscadorComExcecao(erro_timeout)
        caso_de_uso = ConsultarVagas(buscador_vagas=double_com_erro)

        with self.assertRaises(TimeoutIntegracaoVagas) as contexto:
            await caso_de_uso.executar(
                ConsultarVagasEntrada(termo="Backend", filtros={"modalidade": "Remoto"})
            )

        self.assertEqual(contexto.exception.termo, "Backend")
        self.assertEqual(contexto.exception.filtros, {"modalidade": "Remoto"})
