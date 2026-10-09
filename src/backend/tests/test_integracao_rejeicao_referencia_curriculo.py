"""Testa a rejeição de referências de currículo inválidas pela aplicação HTTP completa.

Os cenários atravessam roteamento, validação de entrada do FastAPI, handler e o
caso de uso real ``EditarVersaoCurriculo``, trocando apenas a porta de
repositório por um double em memória. Eles existem para garantir que IDs
inexistentes, de outro proprietário, malformados ou corpos inválidos sejam
rejeitados com status e estrutura de erro estáveis, sem efeito de escrita.
"""

import json
import unittest
from uuid import uuid4

from backend.api.factory import create_app
from backend.application import EditarVersaoCurriculo
from backend.domain import Curriculo, CurriculoId, UsuarioId

# Proveniência: Issue #419 (F9.3) — cenário de rejeição de referência de currículo inválida.

CORPO_VALIDO = {"titulo_versao": "Gestão de Projetos", "layout": "moderno", "is_public": True}


class RepositorioCurriculoEmMemoria:
    """Substitui a porta de currículo registrando consultas e atualizações.

    O double guarda agregados por ID e conta leituras e escritas solicitadas.
    Ele existe para provar que rejeições de fronteira ocorrem antes de qualquer
    acesso ao repositório e que rejeições de negócio não persistem nada.
    """

    def __init__(self, curriculos: list[Curriculo] | None = None) -> None:
        """Indexa os currículos informados e zera os contadores de uso.

        O construtor monta um dicionário por identidade. Ele existe para
        controlar a existência e a propriedade de cada cenário.
        """
        self._por_id = {curriculo.id: curriculo for curriculo in (curriculos or [])}
        self.consultas = 0
        self.atualizacoes: list[Curriculo] = []

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Devolve o currículo conhecido e contabiliza a consulta.

        O método lê somente o dicionário em memória. Ele existe para simular a
        porta exigida pelo caso de uso e tornar a leitura observável.
        """
        self.consultas += 1
        return self._por_id.get(curriculo_id)

    async def atualizar(self, curriculo: Curriculo) -> None:
        """Registra a tentativa de persistir um novo estado do currículo.

        O método apenas acumula o agregado. Ele existe para detectar efeitos de
        escrita indevidos em requisições rejeitadas.
        """
        self.atualizacoes.append(curriculo)


def _criar_curriculo() -> Curriculo:
    """Cria uma versão de currículo válida com proprietário próprio.

    A função monta o agregado sem gerador ou banco. Ela existe para reduzir
    repetição e deixar cada teste focado na rejeição observada.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=UsuarioId(uuid4()),
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


async def _requisitar(
    repositorio: RepositorioCurriculoEmMemoria, caminho: str, corpo: bytes
) -> tuple[int, dict]:
    """Executa um PUT na aplicação ASGI completa e devolve status e JSON.

    A função compõe ``create_app`` com o caso de uso real de edição, monta o
    escopo ASGI manualmente e coleta a resposta enviada. Ela existe para
    exercitar roteamento e validação reais sem depender de cliente HTTP ou
    servidor externos, ausentes no ambiente do backend.
    """
    app = create_app(editar_versao_curriculo=EditarVersaoCurriculo(repositorio))
    escopo = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "PUT",
        "scheme": "http",
        "path": caminho,
        "raw_path": caminho.encode(),
        "query_string": b"",
        "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(corpo)).encode())],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }
    enviado = False

    async def receber() -> dict:
        """Entrega o corpo da requisição uma única vez ao aplicativo ASGI."""
        nonlocal enviado
        if enviado:
            return {"type": "http.disconnect"}
        enviado = True
        return {"type": "http.request", "body": corpo, "more_body": False}

    status = 0
    partes: list[bytes] = []

    async def enviar(mensagem: dict) -> None:
        """Captura o status e o corpo emitidos pelo aplicativo ASGI."""
        nonlocal status
        if mensagem["type"] == "http.response.start":
            status = mensagem["status"]
        elif mensagem["type"] == "http.response.body":
            partes.append(mensagem.get("body", b""))

    await app(escopo, receber, enviar)
    return status, json.loads(b"".join(partes))


def _caminho(usuario_id: object, curriculo_id: object) -> str:
    """Monta o caminho de edição de versão a partir das identidades dadas.

    A função interpola os dois segmentos sem validá-los. Ela existe para que os
    testes possam injetar valores válidos e malformados no mesmo formato.
    """
    return f"/estudantes/{usuario_id}/curriculos/{curriculo_id}"


class RejeicaoReferenciaCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a rejeição HTTP de referências inválidas de currículo.

    A classe usa a aplicação real com repositório em memória. Ela existe para
    proteger o contrato de erro (status e corpo) das referências inexistentes,
    alheias e malformadas.
    """

    async def test_curriculo_inexistente_retorna_404_com_detail(self) -> None:
        """Confirma 404 e corpo ``{"detail": ...}`` para ID bem formado e desconhecido.

        O teste usa repositório vazio e observa a estrutura de erro e a ausência
        de escrita.
        """
        repositorio = RepositorioCurriculoEmMemoria()

        status, corpo = await _requisitar(
            repositorio, _caminho(uuid4(), uuid4()), json.dumps(CORPO_VALIDO).encode()
        )

        self.assertEqual(status, 404)
        self.assertEqual(set(corpo), {"detail"})
        self.assertIsInstance(corpo["detail"], str)
        self.assertTrue(corpo["detail"])
        self.assertEqual(repositorio.atualizacoes, [])

    async def test_curriculo_de_outro_usuario_e_indistinguivel_do_inexistente(self) -> None:
        """Confirma que referência alheia recebe o mesmo status e corpo da inexistente.

        O teste compara as duas respostas para garantir que a API não revela a
        existência de currículos de terceiros.
        """
        curriculo = _criar_curriculo()
        repositorio = RepositorioCurriculoEmMemoria([curriculo])
        corpo_json = json.dumps(CORPO_VALIDO).encode()

        status_alheio, corpo_alheio = await _requisitar(
            repositorio, _caminho(uuid4(), curriculo.id.valor), corpo_json
        )
        status_inexistente, corpo_inexistente = await _requisitar(
            repositorio, _caminho(uuid4(), uuid4()), corpo_json
        )

        self.assertEqual(status_alheio, 404)
        self.assertEqual((status_alheio, corpo_alheio), (status_inexistente, corpo_inexistente))
        self.assertEqual(curriculo.titulo_versao, "Estágio em TI")
        self.assertEqual(repositorio.atualizacoes, [])

    async def test_curriculo_id_malformado_retorna_422_sem_tocar_o_repositorio(self) -> None:
        """Confirma 422 apontando ``curriculo_id`` quando o ID não é UUID.

        O teste cobre texto arbitrário, UUID truncado e UUID com caractere
        inválido, exigindo erro de validação e nenhuma consulta ao repositório.
        """
        for invalido in ("nao-e-um-uuid", str(uuid4())[:-1], str(uuid4())[:-1] + "z"):
            with self.subTest(curriculo_id=invalido):
                repositorio = RepositorioCurriculoEmMemoria()

                status, corpo = await _requisitar(
                    repositorio, _caminho(uuid4(), invalido), json.dumps(CORPO_VALIDO).encode()
                )

                self.assertEqual(status, 422)
                self.assertIsInstance(corpo["detail"], list)
                self.assertEqual(corpo["detail"][0]["loc"], ["path", "curriculo_id"])
                self.assertEqual(repositorio.consultas, 0)
                self.assertEqual(repositorio.atualizacoes, [])

    async def test_usuario_id_malformado_retorna_422_sem_tocar_o_repositorio(self) -> None:
        """Confirma 422 apontando ``usuario_id`` quando o solicitante não é UUID.

        O teste envia um proprietário inválido com currículo bem formado e
        observa a rejeição na fronteira.
        """
        repositorio = RepositorioCurriculoEmMemoria()

        status, corpo = await _requisitar(
            repositorio, _caminho("abc", uuid4()), json.dumps(CORPO_VALIDO).encode()
        )

        self.assertEqual(status, 422)
        self.assertEqual(corpo["detail"][0]["loc"], ["path", "usuario_id"])
        self.assertEqual(repositorio.consultas, 0)

    async def test_corpo_invalido_retorna_422_antes_de_resolver_a_referencia(self) -> None:
        """Confirma 422 para JSON quebrado, campos ausentes e tipos incompatíveis.

        O teste usa um currículo existente para provar que a rejeição ocorre na
        fronteira, sem consulta nem atualização, e que a estrutura de erro lista
        a localização do problema.
        """
        curriculo = _criar_curriculo()
        casos = {
            "json_quebrado": b"{nao-e-json",
            "campos_ausentes": b"{}",
            "tipo_incompativel": json.dumps({**CORPO_VALIDO, "is_public": "talvez"}).encode(),
            "titulo_vazio": json.dumps({**CORPO_VALIDO, "titulo_versao": ""}).encode(),
        }
        for nome, corpo_requisicao in casos.items():
            with self.subTest(caso=nome):
                repositorio = RepositorioCurriculoEmMemoria([curriculo])

                status, corpo = await _requisitar(
                    repositorio, _caminho(curriculo.usuario_id.valor, curriculo.id.valor), corpo_requisicao
                )

                self.assertEqual(status, 422)
                self.assertIsInstance(corpo["detail"], list)
                self.assertTrue(all({"loc", "msg", "type"} <= set(erro) for erro in corpo["detail"]))
                self.assertEqual(repositorio.consultas, 0)
                self.assertEqual(repositorio.atualizacoes, [])
                self.assertEqual(curriculo.titulo_versao, "Estágio em TI")

    async def test_referencia_valida_e_aceita_como_controle_positivo(self) -> None:
        """Confirma 200 e atualização para referência existente do proprietário.

        O teste serve de controle: garante que as rejeições anteriores não
        decorrem de uma rota sempre falha.
        """
        curriculo = _criar_curriculo()
        repositorio = RepositorioCurriculoEmMemoria([curriculo])

        status, corpo = await _requisitar(
            repositorio,
            _caminho(curriculo.usuario_id.valor, curriculo.id.valor),
            json.dumps(CORPO_VALIDO).encode(),
        )

        self.assertEqual(status, 200)
        self.assertEqual(corpo["id"], str(curriculo.id.valor))
        self.assertEqual(corpo["titulo_versao"], "Gestão de Projetos")
        self.assertEqual(len(repositorio.atualizacoes), 1)


if __name__ == "__main__":
    unittest.main()
