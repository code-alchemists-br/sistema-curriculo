"""Testa unitariamente a rota HTTP de atualização de dados de contato."""

from datetime import datetime, timezone
import unittest
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from backend.api.dados_contato import DadosContatoRequisicao, criar_router
from backend.application import AtualizarDadosContato
from backend.domain import Email, HashSenha, Nome, Usuario, UsuarioId

# Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001


class RepositorioUsuarioSpy:
    """Substitui a porta de usuário e registra atualizações solicitadas.

    O double consulta agregados em memória por ID e acumula os novos estados
    recebidos. Ele existe para exercitar o caso de uso real de dados de
    contato através da rota HTTP, sem ORM, banco, rede ou adapter produtivo.
    """

    def __init__(self, usuarios: list[Usuario] | None = None) -> None:
        """Prepara um índice em memória e um histórico vazio de atualizações.

        O construtor copia os usuários fornecidos em um dicionário por
        identidade. Ele existe para controlar ausência e estado excluído em
        cada cenário testado pela rota.
        """
        self._por_id = {usuario.id: usuario for usuario in (usuarios or [])}
        self.usuarios_atualizados: list[Usuario] = []

    async def obter_por_id(self, usuario_id: UsuarioId) -> Usuario | None:
        """Devolve por coroutine o usuário associado ao ID informado.

        O método consulta somente o dicionário controlado pelo teste e não faz
        I/O. Ele existe para simular a leitura aguardável exigida pelo caso.
        """
        return self._por_id.get(usuario_id)

    async def atualizar(self, usuario: Usuario) -> None:
        """Registra por coroutine o novo estado solicitado pela Application.

        O método acumula o agregado sem persistir ou iniciar transação. Ele
        existe para tornar observável se e quando a rota gerou efeito real.
        """
        self.usuarios_atualizados.append(usuario)


def _rota(router: APIRouter, caminho: str, metodo: str):
    """Localiza o endpoint de uma rota registrada para chamada direta em teste.

    A função varre as rotas do router por caminho e método HTTP e devolve a
    função assíncrona decorada. Ela existe para exercitar o handler sem
    iniciar servidor ASGI ou depender de cliente HTTP real.
    """
    for rota in router.routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota.endpoint
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


def _criar_usuario() -> Usuario:
    """Cria um perfil ativo válido para popular o repositório double.

    A função monta o agregado sem acessar gerador, banco ou relógio. Ela
    existe para reduzir repetição mantendo cada teste focado na tradução HTTP.
    """
    return Usuario(
        id=UsuarioId(uuid4()),
        nome=Nome("Ana Silva"),
        email=Email("ana@example.com"),
        hash_senha=HashSenha("hash-ja-derivado"),
    )


def _instante_exclusao() -> datetime:
    """Fornece instante UTC fixo para comparar a exclusão lógica pela rota.

    A função retorna um valor estável sem consultar recurso externo. Ela
    existe para manter os testes determinísticos em qualquer data de execução.
    """
    return datetime(2026, 9, 20, tzinfo=timezone.utc)


class AtualizarDadosContatoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a rota PUT integrada ao caso de uso real ``AtualizarDadosContato``."""

    async def test_atualiza_dados_contato_e_devolve_dados_publicos(self) -> None:
        """Confirma resposta pública e atualização real via repositório double.

        O teste monta um perfil ativo, chama o handler HTTP e compara a
        resposta pública com o efeito observado no double de repositório.
        """
        usuario = _criar_usuario()
        repositorio = RepositorioUsuarioSpy([usuario])
        atualizar = _rota(
            criar_router(AtualizarDadosContato(repositorio)),
            "/estudantes/{usuario_id}/dados-contato",
            "PUT",
        )

        resposta = await atualizar(
            usuario.id.valor,
            DadosContatoRequisicao(
                endereco="Rua Um, 100",
                telefones=["11999990000"],
                linkedin="https://linkedin.com/in/ana",
            ),
        )

        self.assertEqual(resposta.id, usuario.id.valor)
        self.assertEqual(resposta.endereco, "Rua Um, 100")
        self.assertEqual(resposta.telefones, ["11999990000"])
        self.assertEqual(len(repositorio.usuarios_atualizados), 1)
        self.assertIsNotNone(repositorio.usuarios_atualizados[0].dados_contato)

    async def test_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum caso de uso foi injetado."""
        atualizar = _rota(criar_router(None), "/estudantes/{usuario_id}/dados-contato", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            await atualizar(uuid4(), DadosContatoRequisicao(endereco="Rua Um, 100", telefones=["11999990000"]))

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_endereco_vazio_vira_422_sem_efeito_no_repositorio(self) -> None:
        """Confirma 422 quando o endereço fere a regra de domínio, sem atualizar nada.

        O teste envia um endereço só com espaços e observa que o repositório
        double permanece intocado, provando que a validação de domínio
        interrompe o fluxo antes do caso de uso real.
        """
        usuario = _criar_usuario()
        repositorio = RepositorioUsuarioSpy([usuario])
        atualizar = _rota(
            criar_router(AtualizarDadosContato(repositorio)),
            "/estudantes/{usuario_id}/dados-contato",
            "PUT",
        )

        with self.assertRaises(HTTPException) as contexto:
            await atualizar(usuario.id.valor, DadosContatoRequisicao(endereco="   ", telefones=["11999990000"]))

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(repositorio.usuarios_atualizados, [])

    async def test_perfil_nao_encontrado_vira_404(self) -> None:
        """Confirma 404 quando o repositório double não conhece o ID informado."""
        repositorio = RepositorioUsuarioSpy()
        atualizar = _rota(
            criar_router(AtualizarDadosContato(repositorio)),
            "/estudantes/{usuario_id}/dados-contato",
            "PUT",
        )

        with self.assertRaises(HTTPException) as contexto:
            await atualizar(uuid4(), DadosContatoRequisicao(endereco="Rua Um, 100", telefones=["11999990000"]))

        self.assertEqual(contexto.exception.status_code, 404)

    async def test_perfil_excluido_vira_409(self) -> None:
        """Confirma 409 quando o perfil já está logicamente excluído."""
        usuario = _criar_usuario().excluir(_instante_exclusao())
        repositorio = RepositorioUsuarioSpy([usuario])
        atualizar = _rota(
            criar_router(AtualizarDadosContato(repositorio)),
            "/estudantes/{usuario_id}/dados-contato",
            "PUT",
        )

        with self.assertRaises(HTTPException) as contexto:
            await atualizar(usuario.id.valor, DadosContatoRequisicao(endereco="Rua Um, 100", telefones=["11999990000"]))

        self.assertEqual(contexto.exception.status_code, 409)