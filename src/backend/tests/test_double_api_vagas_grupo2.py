"""Testa os modos e comportamentos do double da API de vagas do Grupo 2."""

import unittest

# Proveniência: decision-analysis prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md#v001
from backend.tests.doubles.api_vagas_grupo2 import (
    ApiVagasIndisponivel,
    DoubleApiVagasGrupo2,
    ModoDoubleApiVagas,
    RespostaInvalidaApiVagas,
    VagaExternaDto,
)


class DoubleApiVagasGrupo2TestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica todos os modos de operação determinísticos do double da API do Grupo 2.

    A classe executa testes assíncronos isolados exercitando sucesso, lista vazia,
    erro de resposta, indisponibilidade e o histórico de espionagem. Ela existe para
    assegurar que o simulador de vagas atenda com exatidão aos requisitos da Issue #151.
    """

    async def test_modo_sucesso_retorna_vagas_padrao_completas(self) -> None:
        """Confirma que o modo de sucesso retorna a lista rica e estável de vagas.

        O teste instancia o double no modo padrão e invoca a busca assíncrona sem filtros.
        Ele existe para garantir que a massa de dados padrão seja entregue corretamente
        com todos os campos essenciais preenchidos.
        """
        double = DoubleApiVagasGrupo2(modo=ModoDoubleApiVagas.SUCESSO)

        vagas = await double.buscar_vagas()

        self.assertGreaterEqual(len(vagas), 2)
        primeira_vaga = vagas[0]
        self.assertTrue(primeira_vaga.id.startswith("vaga-g2-"))
        self.assertTrue(primeira_vaga.titulo.strip())
        self.assertTrue(primeira_vaga.empresa.strip())
        self.assertGreaterEqual(len(primeira_vaga.requisitos), 1)
        self.assertTrue(primeira_vaga.url_candidatura.startswith("https://"))

    async def test_modo_sucesso_filtra_por_termo_de_busca(self) -> None:
        """Confirma que o double filtra vagas de acordo com o termo pesquisado.

        O teste realiza uma busca por palavra-chave ("Python") e checa se apenas as
        vagas aderentes ao termo foram retornadas. Ele existe para validar o suporte
        a buscas textuais parametrizadas em testes de interface ou de aplicação.
        """
        double = DoubleApiVagasGrupo2(modo=ModoDoubleApiVagas.SUCESSO)

        vagas_python = await double.buscar_vagas(termo="Python")

        self.assertTrue(all("Python" in v.requisitos or "Python" in v.titulo for v in vagas_python))

    async def test_modo_lista_vazia_retorna_colecao_vazia(self) -> None:
        """Confirma que o modo de lista vazia devolve zero vagas sem lançar exceções.

        O teste configura o double em ``LISTA_VAZIA`` e valida que o retorno é uma lista
        sem elementos. Ele existe para viabilizar testes de tela ou cenários onde o
        estudante busca termos sem nenhuma vaga correspondente.
        """
        double = DoubleApiVagasGrupo2(modo=ModoDoubleApiVagas.LISTA_VAZIA)

        vagas = await double.buscar_vagas(termo="TermoInexistente")

        self.assertEqual(vagas, [])

    async def test_modo_erro_resposta_levanta_excecao_de_formato(self) -> None:
        """Confirma que o modo de erro de resposta levanta RespostaInvalidaApiVagas.

        O teste coloca o double em ``ERRO_RESPOSTA`` e espera o lançamento explícito da
        falha de integração. Ele existe para testar como o sistema reage a falhas 500
        ou contratos corrompidos da API parceira do Grupo 2.
        """
        double = DoubleApiVagasGrupo2(modo=ModoDoubleApiVagas.ERRO_RESPOSTA)

        with self.assertRaises(RespostaInvalidaApiVagas):
            await double.buscar_vagas()

    async def test_modo_indisponibilidade_levanta_excecao_de_conexao(self) -> None:
        """Confirma que o modo de indisponibilidade simula timeout e recusa de rede.

        O teste configura ``INDISPONIBILIDADE`` e valida a propagação de ``ApiVagasIndisponivel``.
        Ele existe para testar o requisito não funcional RNF06 (tolerância a falhas externas).
        """
        double = DoubleApiVagasGrupo2(modo=ModoDoubleApiVagas.INDISPONIBILIDADE)

        with self.assertRaises(ApiVagasIndisponivel):
            await double.buscar_vagas()

    async def test_alternancia_dinamica_de_modo(self) -> None:
        """Verifica se o double permite alternar o comportamento entre chamadas sucessivas.

        O teste inicia em indisponibilidade, altera dinamicamente para sucesso e
        executa novamente a consulta. Ele existe para permitir que testes simulem
        recuperação de falhas ou retentativas (*retries*).
        """
        double = DoubleApiVagasGrupo2(modo=ModoDoubleApiVagas.INDISPONIBILIDADE)

        with self.assertRaises(ApiVagasIndisponivel):
            await double.buscar_vagas()

        double.configurar_modo(ModoDoubleApiVagas.SUCESSO)
        vagas = await double.buscar_vagas()
        self.assertGreater(len(vagas), 0)

    async def test_registro_e_limpeza_de_chamadas(self) -> None:
        """Verifica se o double atua como espia registrando os parâmetros recebidos.

        O teste executa chamadas com termos e filtros específicos, consulta o histórico
        através de ``obter_chamadas`` e o limpa com ``limpar_chamadas``. Ele existe para
        possibilitar asserções sobre como o código de produção invocou a API externa.
        """
        double = DoubleApiVagasGrupo2(modo=ModoDoubleApiVagas.SUCESSO)

        await double.buscar_vagas(termo="Estágio", filtros={"remoto": True})
        chamadas = double.obter_chamadas()

        self.assertEqual(len(chamadas), 1)
        self.assertEqual(chamadas[0]["termo"], "Estágio")
        self.assertEqual(chamadas[0]["filtros"], {"remoto": True})

        double.limpar_chamadas()
        self.assertEqual(double.obter_chamadas(), [])

    async def test_buscar_vagas_em_json_serializa_payload_corretamente(self) -> None:
        """Verifica a conversão dos dados de vagas para dicionários primitivos serializáveis.

        O teste invoca ``buscar_vagas_em_json`` e valida os tipos e campos retornados.
        Ele existe para suportar testes que processem o payload JSON bruto da API (RF10).
        """
        double = DoubleApiVagasGrupo2(modo=ModoDoubleApiVagas.SUCESSO)

        vagas_json = await double.buscar_vagas_em_json()

        self.assertIsInstance(vagas_json, list)
        self.assertIsInstance(vagas_json[0], dict)
        self.assertIn("id", vagas_json[0])
        self.assertIn("titulo", vagas_json[0])
        self.assertIn("requisitos", vagas_json[0])
        self.assertIsInstance(vagas_json[0]["requisitos"], list)

    async def test_definir_vagas_customizadas(self) -> None:
        """Confirma que é possível injetar uma lista customizada de vagas no double.

        O teste cria uma vaga específica com ``VagaExternaDto`` e a injeta com
        ``definir_vagas``. Ele existe para que testes com regras de negócio particulares
        possam controlar exatamente o conjunto de dados sob teste.
        """
        double = DoubleApiVagasGrupo2(modo=ModoDoubleApiVagas.SUCESSO)
        vaga_custom = VagaExternaDto(
            id="vaga-custom-99",
            titulo="Vaga Customizada Específica",
            empresa="Empresa Teste",
            descricao="Descrição customizada",
            requisitos=("Requisito A",),
            localizacao="Local",
            modalidade="Remoto",
            url_candidatura="https://teste.com",
        )

        double.definir_vagas([vaga_custom])
        vagas = await double.buscar_vagas()

        self.assertEqual(len(vagas), 1)
        self.assertEqual(vagas[0].id, "vaga-custom-99")
