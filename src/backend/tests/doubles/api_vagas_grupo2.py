"""Simula deterministicamente a API externa de vagas do Grupo 2 para testes.

O módulo define contratos, DTOs e um test double configurável capaz de reproduzir
respostas de sucesso, buscas vazias, erros de formato de resposta e indisponibilidade
de rede (RNF06). Ele existe para permitir que casos de uso e testes de integração
avaliem a comunicação com o Grupo 2 sem realizar requisições HTTP reais.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol


# Proveniência: decision-analysis prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md#v001
class ErroIntegracaoApiVagas(Exception):
    """Sinaliza uma falha genérica na comunicação com a API de vagas do Grupo 2.

    A classe herda de ``Exception`` e serve como raiz hierárquica para todas as
    falhas decorrentes da integração externa. Ela existe para permitir que a
    aplicação capture qualquer erro de integração sob um mesmo bloco de exceção.
    """


# Proveniência: decision-analysis prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md#v001
class ApiVagasIndisponivel(ErroIntegracaoApiVagas):
    """Representa a indisponibilidade física ou timeout na conexão com a API de vagas.

    A exceção armazena a mensagem de falha e indica ausência de resposta da rede.
    Ela existe para validar o requisito não funcional RNF06, assegurando que o
    sistema trate timeouts e falhas de infraestrutura externa com resiliência.
    """


# Proveniência: decision-analysis prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md#v001
class RespostaInvalidaApiVagas(ErroIntegracaoApiVagas):
    """Representa erro de formato, status 500 ou resposta corrompida da API de vagas.

    A classe especializa a exceção de integração indicando que a resposta recebida
    não pôde ser processada ou violou o contrato JSON esperado. Ela existe para
    testar a tolerância do sistema a retornos malformados da ferramenta externa.
    """


# Proveniência: decision-analysis prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md#v001
class ModoDoubleApiVagas(str, Enum):
    """Define os modos de operação determinísticos suportados pelo double da API de vagas.

    A enumeração lista os quatro estados canônicos de simulação: sucesso, lista vazia,
    erro de resposta e indisponibilidade de rede. Ela existe para dar controle
    declarativo aos testes sobre o comportamento esperado da integração externa.
    """

    SUCESSO = "sucesso"
    LISTA_VAZIA = "lista_vazia"
    ERRO_RESPOSTA = "erro_resposta"
    INDISPONIBILIDADE = "indisponibilidade"


# Proveniência: decision-analysis prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md#v001
@dataclass(frozen=True, slots=True)
class VagaExternaDto:
    """Transporta dados tipados e imutáveis de uma vaga de emprego ou estágio externa.

    O DTO armazena identificador, título, empresa, descrição, requisitos, modalidade,
    localização e link de candidatura. Ele existe para representar o modelo canônico de
    vaga externa retornado pelo Grupo 2 sem acoplar regras de negócio internas da aplicação.
    """

    id: str
    titulo: str
    empresa: str
    descricao: str
    requisitos: tuple[str, ...]
    localizacao: str
    modalidade: str
    url_candidatura: str

    def para_dicionario(self) -> dict[str, Any]:
        """Converte a vaga externa em um dicionário compatível com serialização JSON.

        O método transforma a tupla de requisitos e os atributos textuais em uma
        estrutura de chave-valor nativa do Python. Ele existe para facilitar a
        simulação de payloads JSON brutos recebidos da API do Grupo 2.
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "empresa": self.empresa,
            "descricao": self.descricao,
            "requisitos": list(self.requisitos),
            "localizacao": self.localizacao,
            "modalidade": self.modalidade,
            "url_candidatura": self.url_candidatura,
        }


# Proveniência: decision-analysis prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md#v001
class ClienteApiVagasGrupo2(Protocol):
    """Define o contrato abstrato de busca assíncrona de vagas na API do Grupo 2.

    A porta declara a assinatura aguardável de consulta a vagas com termo de busca e
    filtros opcionais. Ela existe para permitir que a camada de aplicação dependa de
    uma abstração estável, substituível tanto pelo adapter real quanto por doubles.
    """

    async def buscar_vagas(
        self,
        termo: str = "",
        filtros: dict[str, Any] | None = None,
    ) -> list[VagaExternaDto]:
        """Busca vagas na API externa de acordo com termo e filtros informados.

        O método deve ser implementado de forma assíncrona para não bloquear o loop de
        eventos da aplicação. Ele existe para viabilizar consultas parametrizadas de vagas.
        """
        ...


# Vagas padrão ricas e estáveis para testes determinísticos
VAGAS_PADRAO_GRUPO2: tuple[VagaExternaDto, ...] = (
    VagaExternaDto(
        id="vaga-g2-001",
        titulo="Estágio em Desenvolvimento Backend Python",
        empresa="Tech Inovação Soluções",
        descricao=(
            "Oportunidade para estudantes de ADS/Engenharia atuarem no desenvolvimento "
            "de microsserviços, modelagem de banco de dados e testes automatizados."
        ),
        requisitos=("Python", "FastAPI", "SQL", "Git"),
        localizacao="São Paulo - SP",
        modalidade="Híbrido",
        url_candidatura="https://grupo2.exemplo.com/vagas/vaga-g2-001",
    ),
    VagaExternaDto(
        id="vaga-g2-002",
        titulo="Estágio em Engenharia de Software e QA",
        empresa="Qualidade & Sistemas Corporativos",
        descricao=(
            "Vaga focada em automação de testes de ponta a ponta, testes de integração "
            "e validação de acessibilidade em plataformas web modernas."
        ),
        requisitos=("Python", "Testes de Integração", "Automação", "Linux"),
        localizacao="Remoto",
        modalidade="Remoto",
        url_candidatura="https://grupo2.exemplo.com/vagas/vaga-g2-002",
    ),
    VagaExternaDto(
        id="vaga-g2-003",
        titulo="Desenvolvedor Júnior Full Stack",
        empresa="Parceira Digital FATEC",
        descricao=(
            "Atuação no desenvolvimento e manutenção de sistemas web integrados com "
            "APIs RESTful e interfaces reativas."
        ),
        requisitos=("Python", "TypeScript", "React", "PostgreSQL"),
        localizacao="São Paulo - SP",
        modalidade="Presencial",
        url_candidatura="https://grupo2.exemplo.com/vagas/vaga-g2-003",
    ),
)


# Proveniência: decision-analysis prompts/backend/20261007-075500-double-api-vagas-grupo-2-v001.md#v001
class DoubleApiVagasGrupo2:
    """Implementa o test double determinístico da API de vagas do Grupo 2.

    A classe opera em memória, mantém um histórico observável de chamadas recebidas e
    responde conforme o modo configurado: devolve vagas ricas em sucesso, lista vazia,
    levanta ``RespostaInvalidaApiVagas`` em falha de contrato ou ``ApiVagasIndisponivel``
    em indisponibilidade. Ela existe para viabilizar testes unitários e de integração
    sem dependência da infraestrutura externa do Grupo 2.
    """

    def __init__(
        self,
        modo: ModoDoubleApiVagas = ModoDoubleApiVagas.SUCESSO,
        vagas_iniciais: list[VagaExternaDto] | None = None,
    ) -> None:
        """Inicializa o double com o modo selecionado e a coleção de vagas desejada.

        O construtor copia as vagas padrão quando nenhuma lista específica é informada e
        inicia o histórico de chamadas vazio. Ele existe para permitir que cada teste
        inicie seu cenário de forma explícita e isolada.
        """
        self._modo = modo
        self._vagas: list[VagaExternaDto] = (
            list(vagas_iniciais) if vagas_iniciais is not None else list(VAGAS_PADRAO_GRUPO2)
        )
        self._chamadas: list[dict[str, Any]] = []

    @property
    def modo(self) -> ModoDoubleApiVagas:
        """Retorna o modo de operação configurado no double.

        A propriedade consulta o atributo interno protegido sem modificá-lo. Ela existe
        para permitir que testes verifiquem o estado atual da simulação.
        """
        return self._modo

    def configurar_modo(self, modo: ModoDoubleApiVagas) -> None:
        """Altera dinamicamente o comportamento de simulação do double.

        O método atribui o novo modo à instância, influenciando as chamadas subsequentes
        de busca. Ele existe para que um mesmo teste possa alternar entre sucesso e falha
        durante testes de resiliência e recuperação de erro.
        """
        self._modo = modo

    def definir_vagas(self, vagas: list[VagaExternaDto]) -> None:
        """Substitui o conjunto de vagas retornado no modo de sucesso.

        O método atualiza a lista interna mantendo uma cópia independente da coleção recebida.
        Ele existe para permitir que testes configurem massas de vagas específicas quando
        necessário.
        """
        self._vagas = list(vagas)

    def obter_chamadas(self) -> list[dict[str, Any]]:
        """Devolve uma cópia da lista de consultas efetuadas contra o double.

        O método retorna o histórico registrado de termos e filtros recebidos. Ele existe
        para atuar como espia (*spy*), viabilizando asserções sobre os parâmetros enviados
        pelo código de produção ao cliente externo.
        """
        return [dict(c) for c in self._chamadas]

    def limpar_chamadas(self) -> None:
        """Limpa o histórico de consultas registradas no double.

        O método redefine a lista interna de chamadas para o estado inicial vazio. Ele
        existe para facilitar a reutilização da mesma instância entre diferentes fases de
        um teste complexo.
        """
        self._chamadas.clear()

    async def buscar_vagas(
        self,
        termo: str = "",
        filtros: dict[str, Any] | None = None,
    ) -> list[VagaExternaDto]:
        """Executa a simulação assíncrona de busca de vagas conforme o modo configurado.

        O método registra os parâmetros no histórico de chamadas e, em seguida, avalia o
        modo ativo: levanta exceções em indisponibilidade ou erro de resposta, devolve lista
        vazia no modo correspondente, ou filtra a coleção determinística pelo termo em sucesso.
        Ele existe para reproduzir com fidelidade a porta ``ClienteApiVagasGrupo2``.
        """
        self._chamadas.append({"termo": termo, "filtros": filtros or {}})

        if self._modo == ModoDoubleApiVagas.INDISPONIBILIDADE:
            raise ApiVagasIndisponivel(
                "Falha na comunicação: API de vagas do Grupo 2 está temporariamente indisponível."
            )

        if self._modo == ModoDoubleApiVagas.ERRO_RESPOSTA:
            raise RespostaInvalidaApiVagas(
                "Erro de integração: resposta da API de vagas do Grupo 2 é inválida ou malformada."
            )

        if self._modo == ModoDoubleApiVagas.LISTA_VAZIA:
            return []

        # Modo SUCESSO: filtra deterministicamente caso um termo não vazio seja informado
        if not termo.strip():
            return list(self._vagas)

        termo_normalizado = termo.strip().lower()
        return [
            vaga
            for vaga in self._vagas
            if (
                termo_normalizado in vaga.titulo.lower()
                or termo_normalizado in vaga.descricao.lower()
                or any(termo_normalizado in req.lower() for req in vaga.requisitos)
            )
        ]

    async def buscar_vagas_em_json(
        self,
        termo: str = "",
        filtros: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Executa a busca e converte as vagas retornadas em uma lista de dicionários JSON.

        O método invoca ``buscar_vagas`` aguardando a execução do double e converte cada DTO
        através de ``para_dicionario``. Ele existe para simular diretamente a saída do payload
        JSON da API exigida pelo RF10.
        """
        vagas = await self.buscar_vagas(termo=termo, filtros=filtros)
        return [v.para_dicionario() for v in vagas]
