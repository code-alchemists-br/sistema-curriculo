"""Testa o adaptador HTTP de integração com a API de vagas do Grupo 2."""

import json
import unittest
import urllib.error

from backend.application.consulta_vagas import (
    RespostaInvalidaVagas,
    TimeoutIntegracaoVagas,
)
from backend.application.ports import VagaExternaDto
from backend.infrastructure.integrations.cliente_vagas_grupo2 import (
    ClienteApiVagasGrupo2Http,
    mapear_vaga_grupo2_para_dto,
)


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
class MapeadorVagasGrupo2TestCase(unittest.TestCase):
    """Testa a função pura de mapeamento de JSON do Grupo 2 para VagaExternaDto.

    A classe verifica conversão de formatos válidos, tolerância a dados parciais
    ou nulos e rejeição de estruturas inválidas. Ela existe para cobrir as subtarefas #237 e #238.
    """

    def test_mapeia_vaga_completa_com_sucesso(self) -> None:
        """Confirma o mapeamento de um payload completo com todos os campos preenchidos.

        O teste submete um dicionário com todos os atributos especificados no Contrato 2
        e compara os valores atribuídos no DTO resultante. Ele existe para atestar o caminho feliz.
        """
        payload = {
            "id": "vaga-101",
            "titulo": "Estágio Backend Python",
            "empresa": "Tech Solutions",
            "descricao": "Atuação com FastAPI e testes",
            "requisitos": ["Python", "SQL"],
            "localizacao": "São Paulo - SP",
            "modalidade": "HIBRIDO",
            "url_candidatura": "https://grupo2.exemplo.com/vagas/101",
        }

        dto = mapear_vaga_grupo2_para_dto(payload)

        self.assertEqual(dto.id, "vaga-101")
        self.assertEqual(dto.titulo, "Estágio Backend Python")
        self.assertEqual(dto.empresa, "Tech Solutions")
        self.assertEqual(dto.descricao, "Atuação com FastAPI e testes")
        self.assertEqual(dto.requisitos, ("Python", "SQL"))
        self.assertEqual(dto.localizacao, "São Paulo - SP")
        self.assertEqual(dto.modalidade, "HIBRIDO")
        self.assertEqual(dto.url_candidatura, "https://grupo2.exemplo.com/vagas/101")

    def test_mapeia_vaga_com_campos_opcionais_ausentes_e_nulos(self) -> None:
        """Confirma que campos opcionais ausentes ou nulos são normalizados com segurança.

        O teste submete um payload sem localização e modalidade, e com requisitos e url nulos,
        verificando que o DTO é construído com tupla vazia e strings vazias sem lançar erros.
        Ele existe para certificar o cumprimento estrito da subtarefa #238.
        """
        payload = {
            "id": "vaga-102",
            "titulo": "Desenvolvedor Júnior",
            "empresa": "Inovação SA",
            "descricao": "Desenvolvimento web",
            "requisitos": None,
            "url_candidatura": None,
        }

        dto = mapear_vaga_grupo2_para_dto(payload)

        self.assertEqual(dto.id, "vaga-102")
        self.assertEqual(dto.requisitos, ())
        self.assertEqual(dto.localizacao, "")
        self.assertEqual(dto.modalidade, "")
        self.assertEqual(dto.url_candidatura, "")

    def test_mapeia_vaga_aninhada_sob_chave_vaga(self) -> None:
        """Confirma que objetos envelopados no formato de associação são desembalados corretamente.

        O teste envia um dicionário contendo curriculo_id e o objeto aninhado 'vaga',
        verificando que o extrator identifica a estrutura. Ele existe para suportar o Contrato 3.
        """
        payload = {
            "curriculo_id": "curriculo-uuid",
            "vaga": {
                "id": "vaga-201",
                "titulo": "Estágio QA",
                "empresa": "Qualidade Tech",
                "descricao": "Automação de testes",
                "requisitos": ["Selenium"],
            },
        }

        dto = mapear_vaga_grupo2_para_dto(payload)
        self.assertEqual(dto.id, "vaga-201")
        self.assertEqual(dto.titulo, "Estágio QA")

    def test_rejeita_item_que_nao_seja_dicionario(self) -> None:
        """Confirma que entradas inválidas não-dicionário lançam ValueError.

        O teste passa uma string em vez de dicionário e espera ValueError.
        Ele existe para evitar falhas de execução no mapeamento.
        """
        with self.assertRaises(ValueError):
            mapear_vaga_grupo2_para_dto("formato-invalido")

    def test_rejeita_vaga_sem_campos_obrigatorios(self) -> None:
        """Confirma que a falta de id, titulo ou empresa acarreta ValueError.

        O teste submete dicionários incompletos e verifica a rejeição.
        Ele existe para garantir a integridade dos DTOs gerados.
        """
        with self.assertRaises(ValueError):
            mapear_vaga_grupo2_para_dto(
                {"id": "1", "titulo": "Dev"}
            )  # falta empresa e descricao


# Proveniência: decision-analysis prompts/backend/20261015-160231-implementacao-consulta-vagas-externas-v001.md#v001
class ClienteApiVagasGrupo2HttpTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica as operações assíncronas do cliente HTTP adaptador para vagas do Grupo 2.

    A classe utiliza um executor simulado em memória, cobrindo respostas 200,
    listas vazias, erros de schema, JSON malformado e timeouts com preservação de filtros.
    Ela existe para validar o adaptador HTTP perante as subtarefas #238, #239 e #240.
    """

    async def test_busca_com_sucesso_retornando_lista_de_dtos(self) -> None:
        """Confirma a execução de busca bem-sucedida montando parâmetros e retornando DTOs.

        O teste define um executor que responde com JSON válido de vagas e inspeciona
        a chamada e o retorno do cliente. Ele existe para atestar a comunicação nominal.
        """
        url_chamada: list[str] = []

        def executor_falso(url: str, timeout: float) -> bytes:
            url_chamada.append(url)
            resposta = [
                {
                    "id": "vaga-g2-001",
                    "titulo": "Estágio em Desenvolvimento",
                    "empresa": "Tech Inovação",
                    "descricao": "Atuação com APIs",
                    "requisitos": ["Python"],
                }
            ]
            return json.dumps(resposta).encode("utf-8")

        cliente = ClienteApiVagasGrupo2Http(
            url_base="https://api.parceiro.test/vagas",
            executor_http=executor_falso,
        )

        resultado = await cliente.buscar_vagas(
            termo="Python", filtros={"modalidade": "Remoto"}
        )

        self.assertEqual(len(resultado), 1)
        self.assertIsInstance(resultado[0], VagaExternaDto)
        self.assertEqual(resultado[0].id, "vaga-g2-001")
        self.assertTrue(len(url_chamada) == 1)
        self.assertIn("termo=Python", url_chamada[0])
        self.assertIn("modalidade=Remoto", url_chamada[0])

    async def test_resposta_com_formato_de_associacoes_aninhadas(self) -> None:
        """Confirma que o cliente processa payloads contendo a chave 'associacoes'.

        O teste retorna um dicionário contendo associacoes com vagas aninhadas.
        Ele existe para validar a compatibilidade com a resposta descrita no Contrato 3.
        """

        def executor_falso(url: str, timeout: float) -> bytes:
            resposta = {
                "associacoes": [
                    {
                        "curriculo_id": "curriculo-1",
                        "vaga": {
                            "id": "vaga-assoc-1",
                            "titulo": "Desenvolvedor Backend",
                            "empresa": "Empresa Parceira",
                            "descricao": "Microsserviços",
                            "requisitos": ["Go", "Python"],
                        },
                    }
                ]
            }
            return json.dumps(resposta).encode("utf-8")

        cliente = ClienteApiVagasGrupo2Http(executor_http=executor_falso)
        resultado = await cliente.buscar_vagas()

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].id, "vaga-assoc-1")

    async def test_trata_json_malformado_como_resposta_invalida_vagas(self) -> None:
        """Confirma que JSON corrompido é traduzido para RespostaInvalidaVagas.

        O teste simula o recebimento de bytes não parseáveis em JSON e valida o lançamento
        de RespostaInvalidaVagas preservando os filtros. Ele atende à subtarefa #239.
        """

        def executor_falso(url: str, timeout: float) -> bytes:
            return b"<html><body>502 Bad Gateway</body></html>"

        cliente = ClienteApiVagasGrupo2Http(executor_http=executor_falso)

        with self.assertRaises(RespostaInvalidaVagas) as contexto:
            await cliente.buscar_vagas(termo="DevOps", filtros={"local": "SP"})

        self.assertEqual(contexto.exception.termo, "DevOps")
        self.assertEqual(contexto.exception.filtros, {"local": "SP"})
        self.assertIn("JSON válido", str(contexto.exception))

    async def test_trata_timeout_como_timeout_integracao_vagas_preservando_filtros(
        self,
    ) -> None:
        """Confirma que timeout de rede dispara TimeoutIntegracaoVagas com filtros e termo originais.

        O teste simula o lançamento de URLError por timeout e verifica se os parâmetros
        foram encapsulados com segurança. Ele atende expressamente à subtarefa #240.
        """

        def executor_com_timeout(url: str, timeout: float) -> bytes:
            raise urllib.error.URLError(reason=TimeoutError("Connection timed out"))

        cliente = ClienteApiVagasGrupo2Http(executor_http=executor_com_timeout)

        filtros_consulta = {"modalidade": "HIBRIDO", "nivel": "Estágio"}
        with self.assertRaises(TimeoutIntegracaoVagas) as contexto:
            await cliente.buscar_vagas(termo="Engenharia", filtros=filtros_consulta)

        self.assertEqual(contexto.exception.termo, "Engenharia")
        self.assertEqual(contexto.exception.filtros, filtros_consulta)
        self.assertIn("Tempo limite", str(contexto.exception))

    async def test_trata_falha_de_schema_como_resposta_invalida(self) -> None:
        """Confirma que itens com schema violado dentro da lista lançam RespostaInvalidaVagas.

        O teste responde com uma lista onde um dos itens não possui campos obrigatórios.
        Ele existe para atestar a blindagem perante contratos violados pelo parceiro.
        """

        def executor_falso(url: str, timeout: float) -> bytes:
            return json.dumps([{"campo_aleatorio": 123}]).encode("utf-8")

        cliente = ClienteApiVagasGrupo2Http(executor_http=executor_falso)

        with self.assertRaises(RespostaInvalidaVagas):
            await cliente.buscar_vagas(termo="Fullstack")
