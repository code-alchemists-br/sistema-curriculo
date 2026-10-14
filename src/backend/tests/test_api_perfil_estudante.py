"""Testa unitariamente as rotas HTTP de edição e exclusão do perfil."""

import unittest
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from backend.api.perfil_estudante import (
    DadosPessoaisResposta,
    EditarPerfilRequisicao,
    criar_router,
)
from backend.application import (
    ConsultarPerfilEstudanteEntrada,
    EditarPerfilEntrada,
    EmailJaCadastrado,
    ExcluirPerfilEntrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)
from backend.domain import (
    Cidade,
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


class ConsultarPerfilExecutorDouble:
    """Substitui a consulta de perfil e registra a identidade recebida.

    O double devolve perfil configurado ou sinaliza erro sem acessar
    persistência; ele existe para verificar autorização e projeção da rota.
    """

    def __init__(self, resultado: Usuario | None = None, erro: Exception | None = None) -> None:
        """Configura o retorno simulado e prepara o histórico de chamadas.

        O construtor guarda valores em memória sem acessar serviços externos.
        Ele existe para isolar os testes da consulta HTTP.
        """
        self._resultado = resultado
        self._erro = erro
        self.entradas: list[ConsultarPerfilEstudanteEntrada] = []

    async def executar(self, entrada: ConsultarPerfilEstudanteEntrada) -> Usuario:
        """Registra a identidade e devolve o resultado configurado ou falha.

        O método não executa persistência; somente reproduz o cenário montado.
        Ele existe para observar qual perfil o handler pediu para consultar.
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


# Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
class DadosPessoaisRespostaTestCase(unittest.TestCase):
    """Verifica a projeção HTTP sem serializar o agregado de usuário.

    Os cenários constroem entidades em memória e exercitam somente o DTO de
    saída. A classe existe para proteger o payload pessoal de credenciais e
    dados internos não aprovados.
    """

    def test_projeta_somente_campos_pessoais_e_contatos_profissionais(self) -> None:
        """Inclui os campos definidos e omite identidade e credenciais.

        O teste mapeia um perfil completo para o DTO e compara os campos e a
        representação serializada. Ele existe para impedir vazamento de hash,
        ID ou estado interno na resposta.
        """
        usuario = Usuario(
            id=UsuarioId(uuid4()),
            nome=Nome("Ana Silva"),
            email=Email("ana@example.com"),
            hash_senha=HashSenha("nao-deve-aparecer"),
            dados_contato=DadosContato(
                endereco=Endereco("Rua Um, 100"),
                telefones=(Telefone("11999990000"),),
                cidade=Cidade("São Paulo"),
                linkedin="https://linkedin.com/in/ana",
                curriculo_lattes="http://lattes.cnpq.br/123",
            ),
        )

        resposta = DadosPessoaisResposta.de_usuario(usuario)
        payload = resposta.model_dump()

        self.assertEqual(
            payload,
            {
                "nome": "Ana Silva",
                "email": "ana@example.com",
                "telefones": ["11999990000"],
                "cidade": "São Paulo",
                "linkedin": "https://linkedin.com/in/ana",
                "curriculo_lattes": "http://lattes.cnpq.br/123",
            },
        )
        self.assertNotIn("hash_senha", payload)
        self.assertNotIn("id", payload)

    def test_perfil_sem_contato_usa_lista_vazia_e_campos_opcionais_nulos(self) -> None:
        """Representa contato ausente sem expor campos adicionais.

        O cenário converte um perfil legado sem value object de contato e
        verifica os valores vazios/null do DTO. Ele existe para compatibilizar
        registros anteriores à coleta dos dados de contato.
        """
        usuario = _criar_usuario()

        resposta = DadosPessoaisResposta.de_usuario(usuario)

        self.assertEqual(resposta.telefones, [])
        self.assertIsNone(resposta.cidade)
        self.assertIsNone(resposta.linkedin)
        self.assertIsNone(resposta.curriculo_lattes)


class ConsultarPerfilRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica autorização, respostas HTTP e projeção da consulta pessoal.

    Os cenários usam um executor em memória para controlar perfis e falhas. A
    classe existe para proteger a regra de propriedade e a resposta pública.
    """

    async def test_proprietario_consulta_dados_pessoais(self) -> None:
        """Devolve o DTO permitido para o proprietário autenticado.

        O handler recebe o mesmo ID no path e no principal simulado, delega a
        consulta e retorna os dados projetados. O teste existe para validar o
        fluxo autorizado e a identidade encaminhada ao caso de uso.
        """
        usuario = _criar_usuario()
        executor = ConsultarPerfilExecutorDouble(resultado=usuario)
        consultar = _rota(criar_router(None, None, executor), "/estudantes/{usuario_id}", "GET")

        resposta = await consultar(usuario.id.valor, usuario.id.valor)

        self.assertEqual(resposta.nome, usuario.nome.valor)
        self.assertEqual(executor.entradas, [ConsultarPerfilEstudanteEntrada(usuario.id)])

    async def test_id_de_outro_perfil_e_mascarado_com_404(self) -> None:
        """Mascara acesso a outro perfil e não chama o caso de uso.

        O cenário fornece IDs diferentes para recurso e principal e observa a
        resposta e o histórico vazio. Ele existe para impedir leitura cruzada.
        """
        executor = ConsultarPerfilExecutorDouble(resultado=_criar_usuario())
        consultar = _rota(criar_router(None, None, executor), "/estudantes/{usuario_id}", "GET")

        with self.assertRaises(HTTPException) as contexto:
            await consultar(uuid4(), uuid4())

        self.assertEqual(contexto.exception.status_code, 404)
        self.assertEqual(contexto.exception.detail, "Perfil não encontrado.")
        self.assertEqual(executor.entradas, [])

    async def test_perfil_ausente_vira_404_generico(self) -> None:
        """Converte perfil ausente ou excluído em 404 genérico.

        O executor simula a falha do caso de uso e o teste compara a resposta
        pública. Ele existe para não revelar a existência da conta.
        """
        executor = ConsultarPerfilExecutorDouble(erro=PerfilNaoEncontrado("Perfil não encontrado."))
        consultar = _rota(criar_router(None, None, executor), "/estudantes/{usuario_id}", "GET")
        usuario_id = uuid4()

        with self.assertRaises(HTTPException) as contexto:
            await consultar(usuario_id, usuario_id)

        self.assertEqual(contexto.exception.status_code, 404)
        self.assertEqual(contexto.exception.detail, "Perfil não encontrado.")
