"""Testa unitariamente as rotas HTTP de edição e exclusão do perfil."""

import unittest
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Request

from backend.api.factory import create_app
from backend.api.perfil_estudante import (
    AtualizarPerfilCompletoRequisicao,
    EditarPerfilRequisicao,
    criar_router,
)
from backend.application import (
    AtualizarPerfilCompletoEntrada,
    EditarPerfilEntrada,
    EmailJaCadastrado,
    ExcluirPerfilEntrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)
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


class AtualizarPerfilCompletoExecutorDouble:
    """Registra comandos integrais e devolve resultado ou erro configurado.

    O double não persiste nem aplica regras próprias. Ele existe para testar a
    conversão do novo contrato HTTP e a proteção antes do caso de uso.
    """

    def __init__(self, resultado: Usuario | None = None) -> None:
        """Armazena o resultado que será apresentado pela rota.

        O construtor mantém o cenário em memória e inicia entradas vazias. Ele
        existe para observar o único comando enviado pelo handler.
        """
        self._resultado = resultado
        self.entradas: list[AtualizarPerfilCompletoEntrada] = []

    async def executar(self, entrada: AtualizarPerfilCompletoEntrada) -> Usuario:
        """Registra o comando e devolve o agregado preparado pelo cenário.

        O método não realiza I/O nem altera o agregado. Ele existe para tornar
        verificável a identidade e os valores convertidos pela API.
        """
        self.entradas.append(entrada)
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


def _requisicao_autenticada(usuario_id: UUID | None) -> Request:
    """Monta o state que a autenticação de sessão instala na requisição.

    O helper permite chamar o endpoint diretamente com uma identidade
    comprovada, sem depender de servidor ASGI ou de um autenticador real.
    """
    return Request(
        {
            "type": "http",
            "method": "PUT",
            "path": "/estudantes/perfil",
            "headers": [],
            "state": {} if usuario_id is None else {"usuario_id": usuario_id},
        }
    )


class EditarPerfilRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP da edição de perfil pela rota PUT."""

    async def test_edicao_sem_identidade_autenticada_vira_401(self) -> None:
        """Bloqueia edição quando a aplicação não instalou identidade confiável.

        O teste chama o handler com state vazio para garantir que a rota também
        se proteja quando o middleware não estiver composto na aplicação.
        """
        executor = EditarPerfilExecutorDouble(resultado=_criar_usuario())
        editar = _rota(criar_router(executor, None), "/estudantes/{usuario_id}", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            await editar(
                uuid4(),
                EditarPerfilRequisicao(nome="Ana", email="ana@example.com"),
                _requisicao_autenticada(None),
            )

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

    async def test_edicao_de_outro_estudante_vira_403(self) -> None:
        """Bloqueia escrita cruzada mesmo quando o handler é chamado diretamente.

        O principal autenticado difere do UUID do recurso. O teste existe para
        provar que nenhum caso de uso é chamado para o perfil alheio.
        """
        executor = EditarPerfilExecutorDouble(resultado=_criar_usuario())
        editar = _rota(criar_router(executor, None), "/estudantes/{usuario_id}", "PUT")
        usuario_a = uuid4()
        usuario_b = uuid4()

        with self.assertRaises(HTTPException) as contexto:
            await editar(
                usuario_b,
                EditarPerfilRequisicao(nome="Ana", email="ana@example.com"),
                _requisicao_autenticada(usuario_a),
            )

        self.assertEqual(contexto.exception.status_code, 403)
        self.assertEqual(executor.entradas, [])

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
            _requisicao_autenticada(usuario.id.valor),
        )

        self.assertEqual(resposta.id, usuario.id.valor)
        self.assertEqual(resposta.nome, usuario.nome.valor)
        self.assertEqual(executor.entradas[0].usuario_id, UsuarioId(usuario.id.valor))
        self.assertEqual(executor.entradas[0].nome, Nome("Ana Souza"))

    async def test_editar_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum executor de edição foi injetado."""
        editar = _rota(criar_router(None, None), "/estudantes/{usuario_id}", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            usuario_id = uuid4()
            await editar(usuario_id, EditarPerfilRequisicao(nome="Ana", email="ana@example.com"), _requisicao_autenticada(usuario_id))

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_email_malformado_vira_422_sem_chamar_executor(self) -> None:
        """Confirma 422 quando o e-mail fere a regra de domínio, sem invocar o caso de uso."""
        executor = EditarPerfilExecutorDouble(resultado=_criar_usuario())
        editar = _rota(criar_router(executor, None), "/estudantes/{usuario_id}", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            usuario_id = uuid4()
            await editar(usuario_id, EditarPerfilRequisicao(nome="Ana", email="sem-arroba"), _requisicao_autenticada(usuario_id))

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(executor.entradas, [])

    async def test_perfil_nao_encontrado_vira_404(self) -> None:
        """Confirma 404 quando o caso de uso sinaliza perfil inexistente."""
        executor = EditarPerfilExecutorDouble(erro=PerfilNaoEncontrado("Perfil não encontrado."))
        editar = _rota(criar_router(executor, None), "/estudantes/{usuario_id}", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            usuario_id = uuid4()
            await editar(usuario_id, EditarPerfilRequisicao(nome="Ana", email="ana@example.com"), _requisicao_autenticada(usuario_id))

        self.assertEqual(contexto.exception.status_code, 404)

    async def test_perfil_excluido_vira_409(self) -> None:
        """Confirma 409 quando o caso de uso rejeita edição de perfil excluído."""
        executor = EditarPerfilExecutorDouble(erro=PerfilExcluido("Perfil excluído não pode ser editado."))
        editar = _rota(criar_router(executor, None), "/estudantes/{usuario_id}", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            usuario_id = uuid4()
            await editar(usuario_id, EditarPerfilRequisicao(nome="Ana", email="ana@example.com"), _requisicao_autenticada(usuario_id))

        self.assertEqual(contexto.exception.status_code, 409)

    async def test_email_ja_cadastrado_vira_409(self) -> None:
        """Confirma 409 quando o e-mail pertence a outro perfil."""
        executor = EditarPerfilExecutorDouble(erro=EmailJaCadastrado("Já existe uma conta cadastrada com este e-mail."))
        editar = _rota(criar_router(executor, None), "/estudantes/{usuario_id}", "PUT")

        with self.assertRaises(HTTPException) as contexto:
            usuario_id = uuid4()
            await editar(usuario_id, EditarPerfilRequisicao(nome="Ana", email="ana@example.com"), _requisicao_autenticada(usuario_id))

        self.assertEqual(contexto.exception.status_code, 409)


class AtualizacaoPerfilCompletoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica contrato, autenticação e composição do novo PUT integral.

    Os cenários chamam o endpoint com estado de sessão controlado e observam
    o comando enviado à Application. A classe existe para proteger a nova
    fronteira HTTP e manter as rotas legadas independentes.
    """

    async def test_fabrica_registra_a_nova_rota(self) -> None:
        """Confirma que a composição principal publica o novo caminho PUT.

        O teste instancia a fábrica com o executor e inspeciona suas rotas. Ele
        existe para detectar esquecimento de wiring entre a composição e o
        router que implementa a operação.
        """
        app = create_app(
            atualizar_perfil_completo=AtualizarPerfilCompletoExecutorDouble(
                _criar_usuario()
            )
        )

        operacoes = app.openapi()["paths"]["/estudantes/me/perfil"]
        self.assertIn("put", operacoes)

    async def test_atualiza_dados_completos_do_proprietario_autenticado(self) -> None:
        """Converte todos os campos, deriva o proprietário da sessão e responde.

        O teste chama a rota com o principal no request state e compara os
        campos do comando e da resposta. Ele existe para verificar o contrato
        integral sem interferir nos PUTs anteriores.
        """
        usuario_id = uuid4()
        contato = DadosContato(
            endereco=Endereco("Av. Central, 300"),
            telefones=(Telefone("11988887777"),),
            linkedin="https://linkedin.com/in/ana-souza",
            curriculo_lattes="http://lattes.cnpq.br/123",
            cidade="São Paulo",
        )
        usuario = Usuario(
            id=UsuarioId(usuario_id),
            nome=Nome("Ana Souza"),
            email=Email("ana.souza@example.com"),
            hash_senha=HashSenha("hash-secreto"),
            dados_contato=contato,
        )
        executor = AtualizarPerfilCompletoExecutorDouble(usuario)
        atualizar = _rota(
            criar_router(None, None, executor), "/estudantes/me/perfil", "PUT"
        )

        resposta = await atualizar(
            AtualizarPerfilCompletoRequisicao(
                nome="Ana Souza",
                email="ana.souza@example.com",
                endereco="Av. Central, 300",
                cidade=" São Paulo ",
                telefones=["11988887777"],
                linkedin="https://linkedin.com/in/ana-souza",
                curriculo_lattes="http://lattes.cnpq.br/123",
            ),
            _requisicao_autenticada(usuario_id),
        )

        self.assertEqual(resposta.id, usuario_id)
        self.assertEqual(resposta.nome, "Ana Souza")
        self.assertEqual(resposta.email, "ana.souza@example.com")
        self.assertEqual(resposta.endereco, "Av. Central, 300")
        self.assertEqual(resposta.cidade, "São Paulo")
        self.assertEqual(resposta.telefones, ["11988887777"])
        self.assertNotIn("hash_senha", resposta.model_dump())
        self.assertEqual(executor.entradas[0].usuario_id, UsuarioId(usuario_id))
        self.assertEqual(executor.entradas[0].dados_contato, contato)

    async def test_rejeita_atualizacao_integral_sem_sessao(self) -> None:
        """Retorna 401 e não chama o caso de uso quando falta o principal.

        A rota é chamada com request state vazio, cobrindo a proteção mesmo
        quando o middleware de autenticação não foi composto na aplicação.
        """
        executor = AtualizarPerfilCompletoExecutorDouble(_criar_usuario())
        atualizar = _rota(
            criar_router(None, None, executor), "/estudantes/me/perfil", "PUT"
        )
        requisicao = AtualizarPerfilCompletoRequisicao(
            nome="Ana Souza",
            email="ana.souza@example.com",
            endereco="Rua Um, 100",
            cidade="São Paulo",
            telefones=["11999990000"],
        )

        with self.assertRaises(HTTPException) as contexto:
            await atualizar(requisicao, _requisicao_autenticada(None))

        self.assertEqual(contexto.exception.status_code, 401)
        self.assertEqual(executor.entradas, [])

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
