"""Descreve o isolamento A/B de versões de currículo pela API integrada.

Os cenários compõem a aplicação ASGI com os casos de uso reais e um repositório
em memória com estado observável. Eles existem para manter ativo o acesso
próprio e registrar as garantias de autenticação ainda ausentes.
"""

import json
import unittest
from uuid import UUID

from backend.api.factory import create_app
from backend.application import EditarVersaoCurriculo, ListarVersoesCurriculo
from backend.domain import Curriculo, CurriculoId, UsuarioId

# Proveniência: decision-analysis prompts/backend/20261010-183257-isolamento-dados-estudantes-integracao-v004.md#v004

MOTIVO_FALHA_AUTENTICACAO = "identidade vem do usuario_id da rota; falta dependência de autenticação injetável"
CREDENCIAL_ESTUDANTE_A = "credencial-sintetica-estudante-a"
CREDENCIAL_INVALIDA = "credencial-sintetica-invalida"
CORPO_EDICAO = {"titulo_versao": "Currículo atualizado por A", "layout": "moderno", "is_public": False}


class RepositorioCurriculoEmMemoriaComEstado:
    """Armazena currículos por identidade e expõe estado para as asserções.

    O double mantém os próprios agregados em um dicionário, implementando as
    operações de leitura, listagem e atualização usadas pelos casos de uso. Ele
    existe para tornar efeitos de escrita observáveis sem banco externo.
    """

    def __init__(self, curriculos: tuple[Curriculo, ...]) -> None:
        """Indexa os agregados iniciais para uma execução isolada do cenário.

        O construtor recebe a massa sintética de A e B e a indexa por ID. Ele
        existe para que cada teste controle e inspecione seu próprio estado.
        """
        self._por_id = {curriculo.id: curriculo for curriculo in curriculos}

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Devolve o agregado identificado para a operação de edição.

        A busca consulta somente o dicionário local. Ela existe para satisfazer
        a porta do caso de uso real sem substituir a lógica de aplicação.
        """
        return self._por_id.get(curriculo_id)

    async def listar_por_usuario(self, usuario_id: UsuarioId) -> tuple[Curriculo, ...]:
        """Lista os currículos do proprietário pedido pelo caso de uso.

        O método filtra os agregados pelo usuário e os devolve como tupla. Ele
        existe para permitir que a rota e o caso de uso reais componham a leitura.
        """
        return tuple(curriculo for curriculo in self._por_id.values() if curriculo.usuario_id == usuario_id)

    async def atualizar(self, curriculo: Curriculo) -> None:
        """Mantém no repositório o agregado depois de uma atualização válida.

        O método substitui o valor indexado pela mesma identidade. Ele existe
        para que o teste observe a pós-condição no estado do repositório.
        """
        self._por_id[curriculo.id] = curriculo

    def estado(self, curriculo_id: CurriculoId) -> tuple[str, str, bool]:
        """Retorna os campos persistidos relevantes para comparar antes/depois.

        A função lê o agregado atualmente indexado e extrai título, layout e
        visibilidade. Ela existe para detectar qualquer alteração cruzada em B.
        """
        curriculo = self._por_id[curriculo_id]
        return curriculo.titulo_versao, curriculo.layout, curriculo.is_public


def _cabecalhos_de_identidade(credencial: str | None) -> list[tuple[bytes, bytes]]:
    """Centraliza a representação HTTP da identidade usada pelo cenário.

    Atualmente a helper envia a credencial sintética em Authorization ou não
    envia cabeçalho quando ausente; ela existe como único ponto de substituição
    quando a API passar a derivar o ator por autenticação injetável.
    """
    if credencial is None:
        return []
    return [(b"authorization", f"Bearer {credencial}".encode())]


def _criar_curriculo(curriculo_id: int, usuario_id: int, titulo: str) -> Curriculo:
    """Cria um agregado sintético identificável para o estudante indicado.

    A função transforma inteiros constantes em IDs de domínio e configura uma
    versão privada. Ela existe para distinguir recurso e proprietário nos dois
    lados do cenário A/B.
    """
    return Curriculo(
        id=CurriculoId(UUID(int=curriculo_id)),
        usuario_id=UsuarioId(UUID(int=usuario_id)),
        titulo_versao=titulo,
        layout="classico",
        is_public=False,
    )


def _criar_app(repo: RepositorioCurriculoEmMemoriaComEstado):
    """Compõe FastAPI com os casos de uso reais e a porta de teste.

    A fábrica recebe os casos de listagem e edição que compartilham o repositório
    stateful. Ela existe para exercitar rotas HTTP reais sem infraestrutura externa.
    """
    return create_app(
        editar_versao_curriculo=EditarVersaoCurriculo(repo),
        listar_versoes_curriculo=ListarVersoesCurriculo(repo),
    )


async def _requisitar(
    app: object,
    metodo: str,
    caminho: str,
    cabecalhos: list[tuple[bytes, bytes]],
    corpo: dict[str, object] | None = None,
) -> tuple[int, object]:
    """Envia uma chamada diretamente à aplicação ASGI e coleta a resposta.

    A função prepara escopo HTTP e serializa JSON opcional, depois captura status
    e corpo emitidos pelo FastAPI. Ela existe para cobrir a fronteira HTTP sem
    servidor ou cliente externo.
    """
    corpo_bytes = json.dumps(corpo).encode() if corpo is not None else b""
    headers = list(cabecalhos)
    if corpo is not None:
        headers.extend(
            [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(corpo_bytes)).encode()),
            ]
        )
    escopo = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": metodo,
        "scheme": "http",
        "path": caminho,
        "raw_path": caminho.encode(),
        "query_string": b"",
        "headers": headers,
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }
    recebido = False
    status = 0
    partes: list[bytes] = []

    async def receber() -> dict[str, object]:
        """Entrega o corpo da chamada ASGI uma única vez."""
        nonlocal recebido
        if recebido:
            return {"type": "http.disconnect"}
        recebido = True
        return {"type": "http.request", "body": corpo_bytes, "more_body": False}

    async def enviar(mensagem: dict[str, object]) -> None:
        """Captura status e fragmentos do corpo de resposta ASGI."""
        nonlocal status
        if mensagem["type"] == "http.response.start":
            status = int(mensagem["status"])
        elif mensagem["type"] == "http.response.body":
            partes.append(mensagem.get("body", b""))  # type: ignore[arg-type]

    await app(escopo, receber, enviar)  # type: ignore[operator]
    payload = b"".join(partes)
    return status, json.loads(payload) if payload else {}


class IsolamentoDadosEstudantesIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica acesso próprio e descreve as recusas esperadas entre A e B.

    Cada teste compõe a API e casos de uso reais com estado sintético privado.
    A classe existe para manter o contrato de isolamento visível até a entrada
    de autenticação na fronteira HTTP.
    """

    def setUp(self) -> None:
        """Cria estudantes e currículos independentes para cada caso.

        O setup gera IDs fixos exclusivos dentro de cada instância e monta a
        aplicação com repositório novo. Ele existe para evitar dependência de
        ordem e permitir comparar separadamente o estado de A e B.
        """
        self.usuario_a = UsuarioId(UUID(int=101))
        self.usuario_b = UsuarioId(UUID(int=102))
        self.curriculo_a = _criar_curriculo(201, 101, "MARCADOR-PRIVADO-A")
        self.curriculo_b = _criar_curriculo(202, 102, "MARCADOR-PRIVADO-B")
        self.repo = RepositorioCurriculoEmMemoriaComEstado((self.curriculo_a, self.curriculo_b))
        self.app = _criar_app(self.repo)

    async def test_estudante_a_le_e_altera_o_proprio_curriculo(self) -> None:
        """Confirma que o controle positivo lê e atualiza dados próprios.

        O caso envia credencial sintética de A às rotas de A, lê o marcador
        privado e atualiza a versão pelo caso de uso real. Ele existe para provar
        que a aplicação não está simplesmente bloqueando todas as operações.
        """
        caminho_lista = f"/estudantes/{self.usuario_a.valor}/curriculos"
        status_leitura, corpo_leitura = await _requisitar(
            self.app,
            "GET",
            caminho_lista,
            _cabecalhos_de_identidade(CREDENCIAL_ESTUDANTE_A),
        )
        self.assertEqual(status_leitura, 200)
        self.assertIn("MARCADOR-PRIVADO-A", json.dumps(corpo_leitura))

        caminho_edicao = f"{caminho_lista}/{self.curriculo_a.id.valor}"
        status_edicao, corpo_edicao = await _requisitar(
            self.app,
            "PUT",
            caminho_edicao,
            _cabecalhos_de_identidade(CREDENCIAL_ESTUDANTE_A),
            CORPO_EDICAO,
        )

        self.assertEqual(status_edicao, 200)
        self.assertEqual(corpo_edicao["titulo_versao"], CORPO_EDICAO["titulo_versao"])  # type: ignore[index]
        self.assertEqual(self.repo.estado(self.curriculo_a.id), ("Currículo atualizado por A", "moderno", False))

    # Motivo esperado: MOTIVO_FALHA_AUTENTICACAO.
    @unittest.expectedFailure
    async def test_estudante_a_nao_le_curriculo_de_b(self) -> None:
        """Exige que A não leia o recurso privado de B.

        A credencial de A é enviada à rota do recurso de B, e asserções verificam
        recusa e ausência do marcador de B. O caso existe para documentar a
        autorização de leitura ainda ausente na API.
        """
        caminho_b = f"/estudantes/{self.usuario_b.valor}/curriculos"
        status, corpo = await _requisitar(
            self.app,
            "GET",
            caminho_b,
            _cabecalhos_de_identidade(CREDENCIAL_ESTUDANTE_A),
        )

        acesso_negado = status >= 400
        conteudo_de_b_exposto = "MARCADOR-PRIVADO-B" in json.dumps(corpo)
        self.assertTrue(acesso_negado and not conteudo_de_b_exposto)

    # Motivo esperado: MOTIVO_FALHA_AUTENTICACAO.
    @unittest.expectedFailure
    async def test_estudante_a_nao_altera_curriculo_de_b(self) -> None:
        """Exige recusa da edição cruzada e preservação do estado de B.

        A credencial de A é enviada ao caminho e currículo de B; o repositório
        stateful é consultado depois da chamada. O caso existe para detectar
        mudança mesmo quando a resposta de erro, sozinha, fosse enganosa.
        """
        estado_inicial_b = self.repo.estado(self.curriculo_b.id)
        caminho_b = f"/estudantes/{self.usuario_b.valor}/curriculos/{self.curriculo_b.id.valor}"
        corpo_tentativa = {**CORPO_EDICAO, "titulo_versao": "ALTERAÇÃO-CRUZADA"}

        status, _ = await _requisitar(
            self.app,
            "PUT",
            caminho_b,
            _cabecalhos_de_identidade(CREDENCIAL_ESTUDANTE_A),
            corpo_tentativa,
        )

        acesso_negado = status >= 400
        estado_b_preservado = self.repo.estado(self.curriculo_b.id) == estado_inicial_b
        self.assertTrue(acesso_negado and estado_b_preservado)

    # Motivo esperado: MOTIVO_FALHA_AUTENTICACAO.
    @unittest.expectedFailure
    async def test_requisicao_sem_credencial_nao_le_curriculo_de_b(self) -> None:
        """Exige que chamada sem credencial não receba dados privados de B.

        A requisição acessa a rota de B sem cabeçalho de autenticação e verifica
        status negado e ausência do marcador. O caso existe para registrar a
        exigência de autenticação antes da consulta.
        """
        caminho_b = f"/estudantes/{self.usuario_b.valor}/curriculos"
        status, corpo = await _requisitar(
            self.app,
            "GET",
            caminho_b,
            _cabecalhos_de_identidade(None),
        )

        acesso_negado = status >= 400
        conteudo_de_b_exposto = "MARCADOR-PRIVADO-B" in json.dumps(corpo)
        self.assertTrue(acesso_negado and not conteudo_de_b_exposto)

    # Motivo esperado: MOTIVO_FALHA_AUTENTICACAO.
    @unittest.expectedFailure
    async def test_credencial_invalida_nao_le_curriculo_de_b(self) -> None:
        """Exige recusa quando a requisição apresenta credencial inválida.

        A chamada envia a credencial sintética inválida à rota de B e verifica
        recusa sem divulgar o marcador privado. O caso existe para distinguir
        credenciais inválidas de chamadas autenticadas válidas.
        """
        caminho_b = f"/estudantes/{self.usuario_b.valor}/curriculos"
        status, corpo = await _requisitar(
            self.app,
            "GET",
            caminho_b,
            _cabecalhos_de_identidade(CREDENCIAL_INVALIDA),
        )

        acesso_negado = status >= 400
        conteudo_de_b_exposto = "MARCADOR-PRIVADO-B" in json.dumps(corpo)
        self.assertTrue(acesso_negado and not conteudo_de_b_exposto)
