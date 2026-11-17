"""Testa o adaptador HTTP de integração com a API de vagas do Grupo 2."""

import json
import unittest
import urllib.error
from datetime import date
from uuid import UUID

from backend.application.consulta_vagas import (
    ErroIntegracaoVagas,
    RespostaInvalidaVagas,
    TimeoutIntegracaoVagas,
    VagaRecomendadaDto,
)
from backend.application.curriculo_completo import (
    CertificacaoItem,
    CompetenciaItem,
    CurriculoCompleto,
    CursoItem,
    DadosPessoaisSalvos,
    ExperienciaItem,
    FormacaoItem,
    IdiomaItem,
    ProjetoItem,
)
from backend.application.ports import VagaExternaDto
from backend.domain.itens_perfil import (
    CategoriaCompetencia,
    NivelFormacaoAcademica,
    StatusFormacaoAcademica,
)
from backend.infrastructure.integrations.cliente_vagas_grupo2 import (
    ClienteApiVagasGrupo2Http,
    mapear_match_cvmatch_para_dto,
    mapear_vaga_grupo2_para_dto,
    montar_payload_match_cvmatch,
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


class IntegracaoCvmatchClienteHttpTestCase(unittest.IsolatedAsyncioTestCase):
    """Testa a projeção de currículo, o mapeamento de matches e o POST /matches.

    Usa executores de transporte em memória para validar o payload enviado ao
    cvmatch, o parsing completo de MatchesResponse e a tradução de falhas HTTP.
    Existe para garantir aderência ao contrato autoritativo do cvmatch.
    """

    def _curriculo_completo(
        self, curriculo_id: UUID | None = None
    ) -> CurriculoCompleto:
        """Constrói um CurriculoCompleto sintético para exercitar a projeção.

        Preenche todas as seções, incluindo cursos, certificações e dados
        pessoais, que devem ser omitidos na projeção enviada ao cvmatch. Existe
        para evitar repetição de massa nos cenários do contrato.
        """
        return CurriculoCompleto(
            curriculo_id=curriculo_id,
            dados_pessoais=DadosPessoaisSalvos(
                nome="Estudante Teste",
                email="estudante@example.test",
                cidade="São Paulo",
            ),
            formacoes=[
                FormacaoItem(
                    instituicao="FATEC-SP",
                    curso="ADS",
                    nivel=NivelFormacaoAcademica.TECNOLOGO,
                    status=StatusFormacaoAcademica.EM_ANDAMENTO,
                    data_inicio=date(2024, 2, 1),
                    data_fim=None,
                )
            ],
            experiencias=[
                ExperienciaItem(
                    empresa="Empresa Exemplo",
                    cargo="Estagiário",
                    descricao="APIs REST em Python.",
                    data_inicio=date(2025, 1, 1),
                    data_fim=None,
                )
            ],
            projetos=[
                ProjetoItem(
                    titulo="Sistema de Apoio",
                    descricao="Plataforma acadêmica.",
                    tecnologias="Python, FastAPI",
                )
            ],
            competencias=[
                CompetenciaItem(
                    categoria=CategoriaCompetencia.TECNICA,
                    descricao="Python",
                    nivel="intermediario",
                )
            ],
            idiomas=[IdiomaItem(idioma="Inglês", nivel="B2")],
            cursos=[CursoItem(nome="Curso Extra", instituicao="Inst", carga_horaria=20)],
            certificacoes=[
                CertificacaoItem(nome="Cert", organizacao_emissora="Org")
            ],
        )

    def test_montar_payload_match_cvmatch_projeta_apenas_campos_autorizados(
        self,
    ) -> None:
        """Confirma que o payload enviado ao cvmatch respeita o schema estrito.

        Verifica o uso do curriculo_id persistido quando presente, a geração de
        UUID válido quando ausente e a omissão de dados pessoais, cursos,
        certificações e categoria de competência. Existe para prevenir 422 por
        ``extra="forbid"`` no cvmatch.
        """
        id_persistido = UUID("550e8400-e29b-41d4-a716-446655440000")
        payload = montar_payload_match_cvmatch(
            self._curriculo_completo(curriculo_id=id_persistido)
        )

        self.assertEqual(
            set(payload.keys()),
            {
                "curriculo_id",
                "formacoes",
                "experiencias",
                "projetos",
                "competencias",
                "idiomas",
            },
        )
        self.assertEqual(payload["curriculo_id"], str(id_persistido))
        self.assertEqual(
            payload["formacoes"],
            [
                {
                    "instituicao": "FATEC-SP",
                    "curso": "ADS",
                    "nivel": "tecnologo",
                    "status": "em_andamento",
                    "inicio": "2024-02-01",
                    "fim": None,
                }
            ],
        )
        self.assertEqual(
            payload["competencias"],
            [{"descricao": "Python", "nivel": "intermediario"}],
        )

        payload_sem_id = montar_payload_match_cvmatch(
            self._curriculo_completo(curriculo_id=None)
        )
        self.assertEqual(str(UUID(payload_sem_id["curriculo_id"])), payload_sem_id["curriculo_id"])

    def test_mapear_match_cvmatch_para_dto_converte_campos_completos_e_inativos(
        self,
    ) -> None:
        """Confirma a conversão de MatchesResponse com campos opcionais e elegibilidade.

        Submete um item completo de match incluindo eligibility=False e verifica
        formatação de localização, salário, skills e requisitos faltantes. Existe
        para assegurar fidelidade dos dados exibidos ao estudante.
        """
        dto = mapear_match_cvmatch_para_dto(
            {
                "rank": 1,
                "job": {
                    "id": 42,
                    "company": "Tech Corp",
                    "title": "Estágio Python",
                    "description": "Desenvolvimento backend.",
                    "keywords": ["API", "Backend"],
                    "location": {
                        "city": "São Paulo",
                        "state": "SP",
                        "country": "Brasil",
                        "raw": "São Paulo, SP",
                    },
                    "work_arrangement": "REMOTE",
                    "seniority_level": "INTERN",
                    "skills": ["Python", "SQL"],
                    "salary": {"min": 2000, "max": 2800},
                    "currency": "BRL",
                    "job_url": "https://vagas.exemplo/42",
                    "publication_date": "2026-11-01T10:00:00Z",
                },
                "score": 87.5,
                "eligibility": False,
                "matched_skills": ["Python"],
                "missing_requirements": ["SQL"],
                "embedding_model": "intfloat/multilingual-e5-small",
                "algorithm_version": "1.0.0",
            }
        )

        self.assertIsInstance(dto, VagaRecomendadaDto)
        self.assertEqual(dto.id, "42")
        self.assertEqual(dto.localizacao, "São Paulo - SP")
        self.assertEqual(dto.modalidade, "REMOTE")
        self.assertEqual(dto.nivel_senioridade, "INTERN")
        self.assertEqual(dto.salario, "R$ 2.000 – R$ 2.800")
        self.assertFalse(dto.elegivel)
        self.assertEqual(dto.pontuacao_compatibilidade, 87.5)
        self.assertEqual(dto.requisitos_atendidos, ("Python",))
        self.assertEqual(dto.requisitos_faltantes, ("SQL",))

    async def test_buscar_vagas_por_curriculo_envia_post_matches_e_trata_erros(
        self,
    ) -> None:
        """Confirma chamada POST /matches?limit=... e tradução de HTTP 429/504/inválido.

        Usa transportes falsos em memória para verificar a URL montada, o corpo
        enviado e as exceções da Application. Existe para blindar o cliente HTTP.
        """
        chamadas: list[tuple[str, dict[str, object], float]] = []

        def executor_sucesso(url: str, corpo: bytes, timeout: float) -> bytes:
            chamadas.append((url, json.loads(corpo.decode("utf-8")), timeout))
            return json.dumps(
                {
                    "matches": [
                        {
                            "rank": 1,
                            "job": {
                                "id": 7,
                                "company": None,
                                "title": "Dev Júnior",
                                "description": None,
                                "keywords": None,
                                "location": None,
                                "work_arrangement": None,
                                "seniority_level": None,
                                "skills": None,
                                "salary": None,
                                "currency": None,
                                "job_url": None,
                                "publication_date": None,
                            },
                            "score": 75.0,
                            "eligibility": True,
                            "matched_skills": [],
                            "missing_requirements": [],
                            "embedding_model": "e5",
                            "algorithm_version": "1.0",
                        }
                    ]
                }
            ).encode("utf-8")

        cliente = ClienteApiVagasGrupo2Http(
            url_base="http://127.0.0.1:8001/",
            timeout_segundos=3.5,
            executor_post_http=executor_sucesso,
        )
        resultado = await cliente.buscar_vagas_por_curriculo(
            self._curriculo_completo(), limit=15
        )

        self.assertEqual(len(chamadas), 1)
        self.assertEqual(chamadas[0][0], "http://127.0.0.1:8001/matches?limit=15")
        self.assertEqual(chamadas[0][2], 3.5)
        self.assertIn("curriculo_id", chamadas[0][1])
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].empresa, "Empresa confidencial")
        self.assertTrue(resultado[0].elegivel)

        def executor_429(url: str, corpo: bytes, timeout: float) -> bytes:
            raise urllib.error.HTTPError(url, 429, "Too Many Requests", {}, None)

        cliente_429 = ClienteApiVagasGrupo2Http(
            url_base="http://127.0.0.1:8001", executor_post_http=executor_429
        )
        with self.assertRaises(ErroIntegracaoVagas):
            await cliente_429.buscar_vagas_por_curriculo(self._curriculo_completo())

        def executor_timeout(url: str, corpo: bytes, timeout: float) -> bytes:
            raise TimeoutError("timed out")

        cliente_timeout = ClienteApiVagasGrupo2Http(
            url_base="http://127.0.0.1:8001", executor_post_http=executor_timeout
        )
        with self.assertRaises(TimeoutIntegracaoVagas):
            await cliente_timeout.buscar_vagas_por_curriculo(self._curriculo_completo())
