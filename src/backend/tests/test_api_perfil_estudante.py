"""Testa unitariamente as rotas HTTP de edição e exclusão do perfil."""

import unittest
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from backend.api.perfil_estudante import (
    EditarPerfilRequisicao,
    criar_router,
)
from backend.application import (
    EditarPerfilEntrada,
    EmailJaCadastrado,
    ExcluirPerfilEntrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)
from backend.domain import Email, HashSenha, Nome, Usuario, UsuarioId

# Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001


class EditarPerfilExecutorDouble:
    """Substitui o caso de uso de edição e registra as entradas recebidas.

    O double devolve um resultado ou levanta um erro pré-configurado, sem
    tocar banco, ORM ou domínio de verdade. Ele existe para testar a tradução
    HTTP isoladamente da orquestração real da Application.
    """

    def __init__(self, resultado: Usuario | None = None, erro: Exception | None = None) -> None:
        """Guarda o comportamento configurado e inicia o histórico de chamadas.

        O construtor não acessa recursos externos. Ele existe para permitir
        que cada teste configure sucesso ou falha de forma explícita.
        """
        self._resultado = resultado
        self._erro = erro
        self.entradas: list[EditarPerfilEntrada] = []

    async def executar(self, entrada: EditarPerfilEntrada) -> Usuario:
        """Registra a entrada recebida e devolve o resultado ou levanta o erro.

        O método aguarda de forma trivial, sem I/O real. Ele existe para tornar
        observável o que o handler HTTP enviou ao caso de uso.
        """
        self.entradas.append(entrada)
        if self._erro is not None:
            raise self._erro
        assert self._resultado is not None
        return self._resultado


class ExcluirPerfilExecutorDouble:
    """Substitui o caso de uso de exclusão e registra as entradas recebidas.

    O double devolve um resultado ou levanta um erro pré-configurado, sem
    relógio ou repositório reais. Ele existe para testar a tradução HTTP da
    exclusão isoladamente da orquestração real da Application.
    """

    def __init__(self, resultado: Usuario | None = None, erro: Exception | None = None) -> None:
        """Guarda o comportamento configurado e inicia o histórico de chamadas.

        O construtor não acessa recursos externos. Ele existe para permitir
        que cada teste configure sucesso ou falha de forma explícita.
        """
        self._resultado = resultado
        self._erro = erro
        self.entradas: list[ExcluirPerfilEntrada] = []

    async def executar(self, entrada: ExcluirPerfilEntrada) -> Usuario:
        """Registra a entrada recebida e devolve o resultado ou levanta o erro.

        O método aguarda de forma trivial, sem I/O real. Ele existe para tornar
        observável o que o handler HTTP enviou ao caso de uso.
        """
        self.entradas.append(entrada)
        if self._erro is not None:
            raise self._erro
        assert self._resultado is not None
        return self._resultado


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
    """Cria um perfil ativo válido para compor resultados dos doubles.

    A função monta o agregado sem acessar gerador, banco ou relógio. Ela
    existe para reduzir repetição nos testes de tradução HTTP.
    """
    return Usuario(
        id=UsuarioId(uuid4()),
        nome=Nome("Ana Silva"),
        email=Email("ana@example.com"),
        hash_senha=HashSenha("hash-ja-derivado"),
    )


class EditarPerfilRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP da edição de perfil pela rota PUT."""

    async def test_edita_perfil_e_devolve_dados_publicos(self) -> None:
        """Confirma 200 com dados públicos e a entrada correta enviada.

        O teste configura um double de sucesso e chama o handler diretamente,
        comparando resposta e efeito observado no double.
        """
        usuario = _criar_usuario()
        executor = EditarPerfilExecutorDouble(resultado=usuario)
        editar = _rota(criar_router(executor, None), "/estudantes/{usuario_id}", "PUT")

        resposta = await editar(
            usuario.id.valor,
            EditarPerfilRequisicao(nome="Ana Souza", email="ana.souza@example.com"),
        )

        self.assertEqual(resposta.id, usuario.id.valor)
        self.assertEqual(resposta.nome, usuario.nome.valor)
        self.assertEqual(executor.entradas[0].usuario_id, UsuarioId(usuario.id.valor))
        self.assertEqual(executor.entradas[0].nome, Nome("Ana Souza"))

    async def test_editar_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum executor de edição foi injetado."""
        editar = _rota(criar_router(None, None), "/estudantes/{usuario_id}", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            await editar(uuid4(), EditarPerfilRequisicao(nome="Ana", email="ana@example.com"))

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_email_malformado_vira_422_sem_chamar_executor(self) -> None:
        """Confirma 422 quando o e-mail fere a regra de domínio, sem invocar o caso de uso."""
        executor = EditarPerfilExecutorDouble(resultado=_criar_usuario())
        editar = _rota(criar_router(executor, None), "/estudantes/{usuario_id}", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            await editar(uuid4(), EditarPerfilRequisicao(nome="Ana", email="sem-arroba"))

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(executor.entradas, [])

    async def test_perfil_nao_encontrado_vira_404(self) -> None:
        """Confirma 404 quando o caso de uso sinaliza perfil inexistente."""
        executor = EditarPerfilExecutorDouble(erro=PerfilNaoEncontrado("Perfil não encontrado."))
        editar = _rota(criar_router(executor, None), "/estudantes/{usuario_id}", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            await editar(uuid4(), EditarPerfilRequisicao(nome="Ana", email="ana@example.com"))

        self.assertEqual(contexto.exception.status_code, 404)

    async def test_perfil_excluido_vira_409(self) -> None:
        """Confirma 409 quando o caso de uso rejeita edição de perfil excluído."""
        executor = EditarPerfilExecutorDouble(erro=PerfilExcluido("Perfil excluído não pode ser editado."))
        editar = _rota(criar_router(executor, None), "/estudantes/{usuario_id}", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            await editar(uuid4(), EditarPerfilRequisicao(nome="Ana", email="ana@example.com"))

        self.assertEqual(contexto.exception.status_code, 409)

    async def test_email_ja_cadastrado_vira_409(self) -> None:
        """Confirma 409 quando o e-mail pertence a outro perfil."""
        executor = EditarPerfilExecutorDouble(erro=EmailJaCadastrado("Já existe uma conta cadastrada com este e-mail."))
        editar = _rota(criar_router(executor, None), "/estudantes/{usuario_id}", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            await editar(uuid4(), EditarPerfilRequisicao(nome="Ana", email="ana@example.com"))

        self.assertEqual(contexto.exception.status_code, 409)


class ExcluirPerfilRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP da exclusão lógica de perfil pela rota DELETE."""

    async def test_exclui_perfil_e_nao_devolve_conteudo(self) -> None:
        """Confirma execução sem corpo de resposta e entrada correta enviada."""
        usuario = _criar_usuario()
        executor = ExcluirPerfilExecutorDouble(resultado=usuario)
        excluir = _rota(criar_router(None, executor), "/estudantes/{usuario_id}", "DELETE")

        resultado = await excluir(usuario.id.valor)

        self.assertIsNone(resultado)
        self.assertEqual(executor.entradas[0].usuario_id, UsuarioId(usuario.id.valor))

    async def test_excluir_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum executor de exclusão foi injetado."""
        excluir = _rota(criar_router(None, None), "/estudantes/{usuario_id}", "DELETE")

        with self.assertRaises(HTTPException) as contexto:
            await excluir(uuid4())

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_perfil_nao_encontrado_vira_404(self) -> None:
        """Confirma 404 quando o caso de uso sinaliza perfil inexistente."""
        executor = ExcluirPerfilExecutorDouble(erro=PerfilNaoEncontrado("Perfil não encontrado."))
        excluir = _rota(criar_router(None, executor), "/estudantes/{usuario_id}", "DELETE")

        with self.assertRaises(HTTPException) as contexto:
            await excluir(uuid4())

        self.assertEqual(contexto.exception.status_code, 404)