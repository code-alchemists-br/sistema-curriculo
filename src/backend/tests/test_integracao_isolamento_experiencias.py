"""Verifica o isolamento A/B de experiências profissionais pela API integrada.

Os cenários compõem a aplicação ASGI com os casos de uso reais de edição e
exclusão, autenticação por cookie, um relógio fixo e um repositório em memória
com estado. Eles existem para confirmar que um estudante altera e remove apenas
as próprias experiências e que as de outro estudante permanecem intactas.
"""

import json
import unittest
from datetime import date, datetime, timezone
from uuid import UUID

from backend.api.factory import create_app
from backend.api.sessoes import COOKIE_SESSAO
from backend.application import (
    EditarExperienciaProfissional,
    ExcluirExperienciaProfissional,
)
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.domain import (
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    Periodo,
    UsuarioId,
)

CREDENCIAL_ESTUDANTE_A = "credencial-sintetica-estudante-a"
CREDENCIAL_INVALIDA = "credencial-sintetica-invalida"
INSTANTE_EXCLUSAO = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
CORPO_EDICAO = {
    "empresa": "Empresa Atualizada",
    "cargo": "Desenvolvedora",
    "descricao": "Mantém APIs em produção.",
    "data_inicio": "2023-07-01",
    "data_fim": None,
}
CAMINHO_EXPERIENCIA = "/experiencias-profissionais/{experiencia_id}"


class AutenticadorEstudanteA(AutenticadorSessao):
    """Autentica somente a credencial sintética do estudante A.

    O double devolve a identidade de A para um token conhecido e ``None`` para
    qualquer outro valor. Ele existe para que o dono de cada requisição venha
    exclusivamente da sessão, nunca do ID da experiência informado na rota.
    """

    def __init__(self, usuario_id: UsuarioId) -> None:
        """Armazena a identidade aceita pelo cenário integrado.

        O construtor recebe um value object já válido sem consultar serviços.
        Ele existe para fixar o ator autenticado em cada teste.
        """
        self.usuario_id = usuario_id

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Devolve A apenas para o token sintético conhecido.

        O método compara o segredo apresentado sem ler a rota. Ele existe para
        verificar que a autorização usa a sessão autenticada.
        """
        return self.usuario_id if token == CREDENCIAL_ESTUDANTE_A else None


class RelogioFixo:
    """Fornece sempre o mesmo instante com fuso para a exclusão lógica.

    O double implementa a porta de relógio sem acessar o tempo do sistema. Ele
    existe para tornar determinístico o ``deleted_at`` gravado pelo caso de uso.
    """

    def agora(self) -> datetime:
        """Devolve o instante fixo do cenário.

        O método não tem efeitos colaterais. Ele existe para satisfazer a porta
        usada pelo caso de uso real de exclusão.
        """
        return INSTANTE_EXCLUSAO


class RepositorioExperienciaEmMemoriaComEstado:
    """Armazena experiências por identidade e expõe estado para as asserções.

    O double implementa a porta completa de experiência sempre filtrando por
    ID e proprietário, ignora excluídas nas operações ativas e faz atualizações
    e marcações condicionais. Ele existe para tornar os efeitos de escrita
    observáveis sem banco externo, com o mesmo contrato do adapter real.
    """

    def __init__(self, experiencias: tuple[ExperienciaProfissional, ...]) -> None:
        """Indexa as experiências iniciais para uma execução isolada.

        O construtor recebe a massa sintética de A e B. Ele existe para que
        cada teste controle e inspecione seu próprio estado.
        """
        self._por_id = {experiencia.id: experiencia for experiencia in experiencias}

    async def salvar(self, experiencia: ExperienciaProfissional) -> None:
        """Adiciona uma experiência ao índice em memória.

        O método substitui qualquer valor com a mesma identidade. Ele existe
        para completar a porta, embora os cenários não cadastrem experiências.
        """
        self._por_id[experiencia.id] = experiencia

    def _propria(
        self,
        experiencia_id: ExperienciaProfissionalId,
        usuario_id: UsuarioId,
        incluir_excluidas: bool,
    ) -> ExperienciaProfissional | None:
        """Localiza a experiência apenas quando ID e proprietário coincidem.

        A função devolve ``None`` para ID desconhecido, outro dono ou, quando
        pedido, experiência excluída. Ela existe para concentrar o filtro de
        propriedade aplicado por todas as operações do double.
        """
        experiencia = self._por_id.get(experiencia_id)
        if experiencia is None or experiencia.usuario_id != usuario_id:
            return None
        if experiencia.excluida and not incluir_excluidas:
            return None
        return experiencia

    async def obter_por_id_e_usuario(
        self, experiencia_id: ExperienciaProfissionalId, usuario_id: UsuarioId
    ) -> ExperienciaProfissional | None:
        """Devolve a experiência ativa do proprietário informado.

        O método aplica o filtro conjunto e ignora excluídas. Ele existe para
        servir à edição real com o mesmo contrato do adapter SQLAlchemy.
        """
        return self._propria(experiencia_id, usuario_id, incluir_excluidas=False)

    async def obter_por_id_e_usuario_incluindo_excluidas(
        self, experiencia_id: ExperienciaProfissionalId, usuario_id: UsuarioId
    ) -> ExperienciaProfissional | None:
        """Devolve a experiência do proprietário, ativa ou excluída.

        O método aplica o filtro conjunto sem restringir o marcador. Ele existe
        para servir à exclusão idempotente real.
        """
        return self._propria(experiencia_id, usuario_id, incluir_excluidas=True)

    async def atualizar(self, experiencia: ExperienciaProfissional) -> bool:
        """Substitui somente uma experiência ativa do mesmo proprietário.

        O método confere identidade, dono e ausência de exclusão antes de
        gravar e informa se alterou algo. Ele existe para reproduzir o UPDATE
        condicional do adapter.
        """
        atual = self._propria(experiencia.id, experiencia.usuario_id, incluir_excluidas=False)
        if atual is None:
            return False
        self._por_id[experiencia.id] = experiencia
        return True

    async def marcar_excluida(
        self,
        experiencia_id: ExperienciaProfissionalId,
        usuario_id: UsuarioId,
        deleted_at: datetime,
    ) -> bool:
        """Marca a exclusão somente de uma experiência ativa do proprietário.

        O método confere identidade, dono e ausência de marcador antes de
        gravar o instante e informa se alterou algo. Ele existe para reproduzir
        a marcação condicional do adapter.
        """
        atual = self._propria(experiencia_id, usuario_id, incluir_excluidas=False)
        if atual is None:
            return False
        self._por_id[experiencia_id] = atual.excluir(deleted_at)
        return True

    def estado(self, experiencia_id: ExperienciaProfissionalId) -> ExperienciaProfissional:
        """Devolve a experiência atualmente indexada para comparar antes e depois.

        A função lê o índice sem aplicar filtros. Ela existe para detectar
        qualquer alteração cruzada nos dados de B.
        """
        return self._por_id[experiencia_id]


def _cabecalhos_de_identidade(credencial: str | None) -> list[tuple[bytes, bytes]]:
    """Centraliza a representação HTTP da credencial de sessão do cenário.

    A função envia a credencial no cookie reconhecido pelo middleware ou omite
    o cabeçalho quando ausente. Ela existe para exercitar o contrato real de
    autenticação sem depender de cliente HTTP externo.
    """
    if credencial is None:
        return []
    return [(b"cookie", f"{COOKIE_SESSAO}={credencial}".encode())]


def _criar_experiencia(experiencia_id: int, usuario_id: int, empresa: str) -> ExperienciaProfissional:
    """Cria uma experiência sintética identificável para o estudante indicado.

    A função transforma inteiros constantes em IDs de domínio e usa uma empresa
    marcadora. Ela existe para distinguir recurso e proprietário nos dois lados
    do cenário A/B.
    """
    return ExperienciaProfissional(
        id=ExperienciaProfissionalId(UUID(int=experiencia_id)),
        usuario_id=UsuarioId(UUID(int=usuario_id)),
        empresa=empresa,
        cargo="Estagiária",
        descricao="Construiu integrações internas.",
        periodo=Periodo(date(2022, 1, 1), date(2023, 6, 1)),
    )


def _criar_app(repo: RepositorioExperienciaEmMemoriaComEstado, autenticador: AutenticadorSessao):
    """Compõe FastAPI com os casos de uso reais de edição e exclusão.

    A fábrica injeta casos de uso que compartilham o repositório com estado, o
    relógio fixo e o autenticador de teste. Ela existe para exercitar as rotas
    protegidas de experiência de ponta a ponta sem banco.
    """
    return create_app(
        autenticador_sessao=autenticador,
        editar_experiencia_profissional=EditarExperienciaProfissional(repo),
        excluir_experiencia_profissional=ExcluirExperienciaProfissional(repo, RelogioFixo()),
    )


async def _requisitar(
    app: object,
    metodo: str,
    caminho: str,
    cabecalhos: list[tuple[bytes, bytes]],
    corpo: dict[str, object] | None = None,
) -> tuple[int, object]:
    """Envia uma chamada diretamente à aplicação ASGI e coleta a resposta.

    A função prepara escopo HTTP e serializa JSON opcional, depois captura
    status e corpo emitidos pelo FastAPI. Ela existe para cobrir a fronteira
    HTTP sem servidor ou cliente externo.
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


class IsolamentoExperienciasIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica edição e exclusão próprias e a recusa das operações cruzadas.

    Cada teste compõe API, middleware e casos de uso reais com identidade
    autenticada e estado sintético de A e B. A classe existe para proteger a
    integridade das experiências de cada estudante.
    """

    def setUp(self) -> None:
        """Cria estudantes e experiências independentes para cada caso.

        O setup usa IDs fixos e monta a aplicação com repositório novo. Ele
        existe para evitar dependência de ordem e comparar o estado de B antes
        e depois de cada tentativa.
        """
        self.usuario_a = UsuarioId(UUID(int=101))
        self.experiencia_a = _criar_experiencia(301, 101, "MARCADOR-PRIVADO-A")
        self.experiencia_b = _criar_experiencia(302, 102, "MARCADOR-PRIVADO-B")
        self.repo = RepositorioExperienciaEmMemoriaComEstado(
            (self.experiencia_a, self.experiencia_b)
        )
        self.app = _criar_app(self.repo, AutenticadorEstudanteA(self.usuario_a))
        self.caminho_a = CAMINHO_EXPERIENCIA.format(experiencia_id=self.experiencia_a.id.valor)
        self.caminho_b = CAMINHO_EXPERIENCIA.format(experiencia_id=self.experiencia_b.id.valor)
        self.caminho_inexistente = CAMINHO_EXPERIENCIA.format(experiencia_id=UUID(int=999))

    async def test_estudante_a_edita_e_exclui_a_propria_experiencia(self) -> None:
        """Confirma que o controle positivo edita e exclui dados próprios.

        A credencial de A edita e depois exclui a experiência de A pelos casos
        de uso reais. O teste existe para provar que a aplicação não está
        simplesmente bloqueando todas as operações.
        """
        cabecalhos = _cabecalhos_de_identidade(CREDENCIAL_ESTUDANTE_A)

        status_edicao, corpo_edicao = await _requisitar(
            self.app, "PUT", self.caminho_a, cabecalhos, CORPO_EDICAO
        )
        status_exclusao, _ = await _requisitar(self.app, "DELETE", self.caminho_a, cabecalhos)

        self.assertEqual(status_edicao, 200)
        self.assertEqual(corpo_edicao["empresa"], "Empresa Atualizada")  # type: ignore[index]
        self.assertEqual(status_exclusao, 204)
        estado_a = self.repo.estado(self.experiencia_a.id)
        self.assertEqual(estado_a.empresa, "Empresa Atualizada")
        self.assertEqual(estado_a.deleted_at, INSTANTE_EXCLUSAO)

    async def test_estudante_a_nao_edita_experiencia_de_b(self) -> None:
        """Recusa a edição cruzada com 404 e preserva todos os dados de B.

        A credencial de A tenta substituir a experiência de B; o repositório
        com estado é consultado depois da chamada. O teste existe para detectar
        alteração cruzada mesmo que a resposta, sozinha, parecesse correta.
        """
        estado_inicial_b = self.repo.estado(self.experiencia_b.id)

        status, corpo = await _requisitar(
            self.app,
            "PUT",
            self.caminho_b,
            _cabecalhos_de_identidade(CREDENCIAL_ESTUDANTE_A),
            {**CORPO_EDICAO, "empresa": "ALTERACAO-CRUZADA"},
        )

        self.assertEqual(status, 404)
        self.assertNotIn("MARCADOR-PRIVADO-B", json.dumps(corpo))
        self.assertEqual(self.repo.estado(self.experiencia_b.id), estado_inicial_b)

    async def test_estudante_a_nao_exclui_experiencia_de_b(self) -> None:
        """Recusa a exclusão cruzada com 404 e mantém B ativa.

        A credencial de A tenta excluir a experiência de B e o marcador de
        exclusão de B é conferido depois. O teste existe para garantir que um
        estudante não remova dados de outro.
        """
        status, _ = await _requisitar(
            self.app,
            "DELETE",
            self.caminho_b,
            _cabecalhos_de_identidade(CREDENCIAL_ESTUDANTE_A),
        )

        self.assertEqual(status, 404)
        self.assertIsNone(self.repo.estado(self.experiencia_b.id).deleted_at)
        self.assertEqual(self.repo.estado(self.experiencia_b.id), self.experiencia_b)

    async def test_recurso_de_b_responde_igual_a_recurso_inexistente(self) -> None:
        """Torna indistinguíveis a experiência de B e um ID inexistente.

        Para edição e exclusão, o teste compara status e corpo da tentativa
        sobre B com os de um ID que não existe. Ele existe para que A não
        consiga descobrir quais experiências pertencem a outros estudantes.
        """
        cabecalhos = _cabecalhos_de_identidade(CREDENCIAL_ESTUDANTE_A)
        for metodo, corpo in (("PUT", CORPO_EDICAO), ("DELETE", None)):
            with self.subTest(metodo=metodo):
                resposta_b = await _requisitar(self.app, metodo, self.caminho_b, cabecalhos, corpo)
                resposta_inexistente = await _requisitar(
                    self.app, metodo, self.caminho_inexistente, cabecalhos, corpo
                )

                self.assertEqual(resposta_b, resposta_inexistente)
                self.assertEqual(
                    resposta_b, (404, {"detail": "Experiência profissional não encontrada."})
                )

    async def test_sem_credencial_ou_com_credencial_invalida_nao_altera_b(self) -> None:
        """Recusa com 401 edição e exclusão sem sessão válida e preserva B.

        As tentativas sobre B usam nenhuma credencial ou uma credencial
        inválida. O teste existe para que a falta de autenticação nunca chegue
        aos casos de uso nem altere o estado de outro estudante.
        """
        for credencial in (None, CREDENCIAL_INVALIDA):
            for metodo, corpo in (("PUT", CORPO_EDICAO), ("DELETE", None)):
                with self.subTest(credencial=credencial, metodo=metodo):
                    status, _ = await _requisitar(
                        self.app,
                        metodo,
                        self.caminho_b,
                        _cabecalhos_de_identidade(credencial),
                        corpo,
                    )

                    self.assertEqual(status, 401)
        self.assertEqual(self.repo.estado(self.experiencia_b.id), self.experiencia_b)
