"""Verifica autorização de perfil pela aplicação ASGI com middleware ativo.

A suíte integra transporte, middleware, routers, casos de uso e domínio reais
com portas em memória para detectar acesso cruzado sem banco ou rede externa.
"""

import asyncio
import hashlib
import json
import unittest
from unittest.mock import AsyncMock, patch
from uuid import UUID

from backend.api.factory import create_app
from backend.application import AtualizarDadosContato
from backend.application.perfil_estudante import ConsultarPerfilEstudante, EditarPerfil
from backend.application.ports import RepositorioUsuario
from backend.domain import (
    DadosContato,
    Email,
    Endereco,
    HashSenha,
    Nome,
    Telefone,
    Usuario,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261016-221632-recusa-perfil-alheio-middleware-ativo-v001.md#v001

TOKEN_A = "token-sintetico-a"
TOKEN_INVALIDO = "token-sintetico-invalido"
CORPO_PERFIL = {"nome": "Estudante Atualizado", "email": "atualizado@example.test"}
CORPO_CONTATO = {
    "endereco": "Rua Nova, 300",
    "telefones": ["11999990003"],
    "linkedin": "https://www.linkedin.com/in/atualizado",
    "curriculo_lattes": "http://lattes.cnpq.br/3333333333333333",
}


class RepositorioUsuariosEmMemoria(RepositorioUsuario):
    """Implementa a porta de usuários com agregados indexados em memória.

    As operações consultam e substituem o índice por identidade para permitir
    casos de uso reais e observação de seus efeitos sem persistência externa.
    """

    def __init__(self, usuarios: tuple[Usuario, ...]) -> None:
        """Indexa usuários novos por ID, isolando o estado de cada cenário."""
        self.usuarios = {usuario.id: usuario for usuario in usuarios}

    async def obter_por_id(self, usuario_id: UsuarioId) -> Usuario | None:
        """Consulta o índice por ID para atender à leitura real da aplicação."""
        return self.usuarios.get(usuario_id)

    async def obter_por_email(self, email: Email) -> Usuario | None:
        """Filtra agregados por e-mail para preservar a verificação de unicidade."""
        return next((usuario for usuario in self.usuarios.values() if usuario.email == email), None)

    async def existe_por_email(self, email: Email) -> bool:
        """Consulta e-mail pela própria porta para informar sua existência."""
        return await self.obter_por_email(email) is not None

    async def salvar(self, usuario: Usuario) -> None:
        """Insere o agregado por ID para completar a porta de persistência local."""
        self.usuarios[usuario.id] = usuario

    async def atualizar(self, usuario: Usuario) -> None:
        """Substitui o agregado por ID para tornar atualizações reais observáveis."""
        self.usuarios[usuario.id] = usuario


def _usuario(numero: int, letra: str) -> Usuario:
    """Constrói agregado e contato sintéticos distintos para isolar cada ator.

    Usa IDs fixos e value objects válidos sem consultar relógio ou banco para
    tornar a matriz reproduzível e os dados privados identificáveis.
    """
    return Usuario(
        id=UsuarioId(UUID(int=numero)),
        nome=Nome(f"MARCADOR PRIVADO {letra}"),
        email=Email(f"estudante-{letra.lower()}@example.test"),
        hash_senha=HashSenha("hash-sintetico"),
        dados_contato=DadosContato(
            endereco=Endereco(f"Rua Privada {letra}, {numero}"),
            telefones=(Telefone(f"1199999000{numero}"),),
            cidade=f"Cidade Privada {letra}",
            linkedin=f"https://www.linkedin.com/in/estudante-{letra.lower()}",
            curriculo_lattes=f"http://lattes.cnpq.br/{str(numero) * 16}",
        ),
    )


def _snapshot(usuario: Usuario) -> dict:
    """Copia campos de conta e contato em valores para detectar efeitos indevidos.

    Extrai primitivas e resumo da credencial, sem referências mutáveis nem
    segredo em mensagens de comparação, para verificar preservação do agregado.
    """
    contato = usuario.dados_contato
    return {
        "id": str(usuario.id.valor),
        "nome": usuario.nome.valor,
        "email": usuario.email.valor,
        "credencial": hashlib.sha256(usuario.hash_senha.valor.encode()).hexdigest(),
        "deleted_at": usuario.deleted_at,
        "contato": None if contato is None else {
            "endereco": contato.endereco.valor,
            "telefones": tuple(telefone.valor for telefone in contato.telefones),
            "cidade": contato.cidade.valor if contato.cidade else None,
            "linkedin": contato.linkedin,
            "curriculo_lattes": contato.curriculo_lattes,
        },
    }


class AutenticadorDeterministico:
    """Resolve apenas o cookie sintético conhecido e registra tokens recebidos.

    Um mapa fechado fornece A ou ausência de identidade para exercitar o
    middleware real sem afirmar validação de sessões persistidas.
    """

    def __init__(self, usuario_a: UsuarioId) -> None:
        """Associa o token conhecido a A e zera o histórico para isolar cenários."""
        self.identidades = {TOKEN_A: usuario_a}
        self.tokens = []

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Registra o token e consulta o mapa para negar credenciais desconhecidas."""
        self.tokens.append(token)
        return self.identidades.get(token)


async def _requisitar(app, metodo: str, caminho: str, token: str | None, corpo=None):
    """Executa HTTP ASGI em memória e devolve status com JSON completo.

    Mantém receive aberto até o último fragmento, usando um evento e HTTPS,
    para não truncar respostas transmitidas pelo BaseHTTPMiddleware.
    """
    dados = json.dumps(corpo).encode() if corpo is not None else b""
    # Bearer conhecido nunca deve substituir o cookie ausente ou inválido.
    cabecalhos = [(b"host", b"testserver"),
                  (b"authorization", f"Bearer {TOKEN_A}".encode())]
    if token is not None:
        cabecalhos.append((b"cookie", f"__Host-sessao={token}".encode()))
    if corpo is not None:
        cabecalhos.extend([(b"content-type", b"application/json"),
                           (b"content-length", str(len(dados)).encode())])
    escopo = {
        "type": "http", "asgi": {"version": "3.0", "spec_version": "2.4"},
        "http_version": "1.1", "method": metodo, "scheme": "https",
        "path": caminho, "raw_path": caminho.encode(), "query_string": b"",
        "root_path": "", "headers": cabecalhos,
        "client": ("testclient", 50000), "server": ("testserver", 443),
    }
    entregue = False
    concluida = asyncio.Event()
    status = None
    partes = []

    async def receber():
        """Entrega o corpo uma vez e aguarda o fim para preservar a conexão ASGI."""
        nonlocal entregue
        if not entregue:
            entregue = True
            return {"type": "http.request", "body": dados, "more_body": False}
        await concluida.wait()
        return {"type": "http.disconnect"}

    async def enviar(evento):
        """Acumula fragmentos e sinaliza o último para observar a resposta inteira."""
        nonlocal status
        if evento["type"] == "http.response.start":
            status = evento["status"]
        elif evento["type"] == "http.response.body":
            partes.append(evento.get("body", b""))
            if not evento.get("more_body", False):
                concluida.set()

    await asyncio.wait_for(app(escopo, receber, enviar), timeout=5)
    if not concluida.is_set() or status is None:
        raise AssertionError("Aplicação não concluiu a resposta HTTP ASGI.")
    return status, json.loads(b"".join(partes))


class RecusaPerfilAlheioIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Integra autenticação e autorização de perfis com controles A/B.

    Compõe a fábrica oficial e observa casos de uso reais para demonstrar
    acesso próprio e recusa cruzada sem efeitos nem dados privados.
    """

    def _preparar(self):
        """Compõe aplicação e portas novas, envolvendo executores reais com spies.

        Mantém a lógica via wraps e registra chamadas/awaits para distinguir
        bloqueio anterior ao caso de uso de simples ausência de persistência.
        """
        self.a, self.b = _usuario(1, "A"), _usuario(2, "B")
        self.repo = RepositorioUsuariosEmMemoria((self.a, self.b))
        self.autenticador = AutenticadorDeterministico(self.a.id)
        casos = (ConsultarPerfilEstudante(self.repo), EditarPerfil(self.repo),
                 AtualizarDadosContato(self.repo))
        self.spies = tuple(self.enterContext(patch.object(
            caso, "executar", new=AsyncMock(wraps=caso.executar)
        )) for caso in casos)
        self.app = create_app(
            autenticador_sessao=self.autenticador,
            consultar_perfil=casos[0], editar_perfil=casos[1],
            atualizar_dados_contato=casos[2],
        )

    async def _verificar_matriz(self, operacao: str):
        """Executa quatro estados de acesso por operação com isolamento e spies.

        Compara histórico e valores antes/depois de cada request real para
        demonstrar autorização, origem da identidade e ausência de efeitos.
        """
        for identidade, token, proprio in (
            ("cookie A, alvo A", TOKEN_A, True),
            ("cookie A, alvo B", TOKEN_A, False),
            ("sem cookie, Bearer ignorado", None, False),
            ("cookie inválido, Bearer ignorado", TOKEN_INVALIDO, False),
        ):
            with self.subTest(operacao=operacao, identidade=identidade):
                self._preparar()
                alvo = self.a if proprio else self.b
                metodo = "GET" if operacao == "consulta" else "PUT"
                caminho = f"/estudantes/{alvo.id.valor}"
                entrada = None
                if operacao == "perfil":
                    entrada = CORPO_PERFIL
                elif operacao == "contato":
                    caminho += "/dados-contato"
                    entrada = CORPO_CONTATO
                esperado = (200 if proprio else
                            401 if token != TOKEN_A else
                            404 if operacao == "consulta" else 403)
                estados_antes = tuple(_snapshot(self.repo.usuarios[u.id]) for u in (self.a, self.b))
                historicos_antes = tuple(
                    (list(spy.call_args_list), list(spy.await_args_list),
                     spy.call_count, spy.await_count) for spy in self.spies
                )
                tokens_antes = list(self.autenticador.tokens)

                status, corpo = await _requisitar(self.app, metodo, caminho, token, entrada)

                self.assertEqual(status, esperado, f"{metodo} {caminho}: {identidade}")
                self.assertEqual(self.autenticador.tokens,
                                 tokens_antes + ([] if token is None else [token]))
                texto = json.dumps(corpo, ensure_ascii=False)
                dados_b = estados_antes[1]
                for privado in (
                    dados_b["id"], dados_b["nome"], dados_b["email"],
                    dados_b["contato"]["endereco"], dados_b["contato"]["cidade"],
                    *dados_b["contato"]["telefones"],
                    dados_b["contato"]["linkedin"], dados_b["contato"]["curriculo_lattes"],
                ):
                    self.assertNotIn(privado, texto, "Resposta expôs dados privados de B")
                self.assertNotIn("hash_senha", texto)
                estados_depois = tuple(_snapshot(self.repo.usuarios[u.id]) for u in (self.a, self.b))
                self.assertEqual(estados_depois[1], estados_antes[1], "B foi alterado")

                if not proprio:
                    self.assertEqual(estados_depois, estados_antes, "Recusa alterou estado")
                    self.assertEqual(set(corpo), {"detail"})
                    self.assertEqual(corpo["detail"], {
                        401: "Sessão ausente ou inválida.",
                        403: "A sessão não pode acessar este recurso.",
                        404: "Perfil não encontrado.",
                    }[esperado])
                else:
                    self._verificar_sucesso(operacao, corpo, estados_antes, estados_depois)

                indice_esperado = ("consulta", "perfil", "contato").index(operacao)
                for indice, spy in enumerate(self.spies):
                    chamadas, awaits, total, total_awaits = historicos_antes[indice]
                    if proprio and indice == indice_esperado:
                        self.assertEqual(spy.call_count, total + 1)
                        self.assertEqual(spy.await_count, total_awaits + 1)
                        self.assertEqual(spy.call_args_list[:-1], chamadas)
                        self.assertEqual(spy.await_args_list[:-1], awaits)
                        self.assertEqual(spy.call_args, spy.await_args)
                        self.assertEqual(spy.await_args.args[0].usuario_id, self.a.id)
                    else:
                        self.assertEqual(spy.call_args_list, chamadas, "Executor chamado na recusa ou operação incorreta")
                        self.assertEqual(spy.await_args_list, awaits, "Executor aguardado na recusa ou operação incorreta")
                        self.assertEqual(spy.call_count, total)
                        self.assertEqual(spy.await_count, total_awaits)

    def _verificar_sucesso(self, operacao, corpo, antes, depois):
        """Compara DTO e agregado com valores esperados do controle próprio.

        Verifica leitura completa ou atualização real preservando outros campos
        para excluir falso sucesso causado por executor indisponível ou inerte.
        """
        esperado = dict(antes[0])
        if operacao == "consulta":
            contato = antes[0]["contato"]
            self.assertEqual(corpo, {
                "nome": "MARCADOR PRIVADO A", "email": antes[0]["email"],
                "telefones": list(contato["telefones"]), "cidade": contato["cidade"],
                "linkedin": contato["linkedin"], "curriculo_lattes": contato["curriculo_lattes"],
            })
        elif operacao == "perfil":
            esperado.update(CORPO_PERFIL)
            self.assertEqual(corpo, {"id": str(self.a.id.valor), **CORPO_PERFIL})
        else:
            esperado["contato"] = {
                **CORPO_CONTATO, "telefones": tuple(CORPO_CONTATO["telefones"]),
                "cidade": antes[0]["contato"]["cidade"],
            }
            self.assertEqual(corpo, {"id": str(self.a.id.valor), **CORPO_CONTATO})
        self.assertEqual(depois[0], esperado)

    async def test_consulta_perfil(self):
        """Exercita GET com quatro identidades via ASGI para proteger a consulta."""
        await self._verificar_matriz("consulta")

    async def test_edicao_perfil(self):
        """Exercita PUT com quatro identidades via ASGI para proteger nome e e-mail."""
        await self._verificar_matriz("perfil")

    async def test_edicao_contato(self):
        """Exercita PUT de contato em quatro estados via ASGI para impedir escrita alheia."""
        await self._verificar_matriz("contato")
