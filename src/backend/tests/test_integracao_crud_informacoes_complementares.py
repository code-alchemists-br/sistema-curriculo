"""Testes de integração para o CRUD de informações complementares.

O módulo compõe a aplicação ASGI com os casos de uso reais de documentos
complementares (armazenamento e exclusão) e cursos complementares (cadastro),
middleware de autenticação ativo e adaptadores em memória com estado.
Ele existe para garantir o funcionamento integrado dos endpoints de informações
complementares e verificar rigorosamente os oráculos de respostas válidas e inválidas.
"""

from __future__ import annotations

import base64
import json
import unittest
from uuid import UUID, uuid4

# Proveniência: decision-analysis prompts/backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md#v001
from backend.api.factory import create_app
from backend.api.sessoes import COOKIE_SESSAO
from backend.application.autenticacao_sessao import AutenticadorSessao
from backend.application.cadastro_curso import CadastrarCurso
from backend.application.cadastro_documento import ArmazenarDocumento
from backend.application.exclusao_documento import ExcluirDocumento
from backend.application.ports import (
    ArmazenadorDocumentos,
    GeradorCursoId,
    GeradorDocumentoId,
    RepositorioCurso,
    RepositorioDocumento,
)
from backend.domain.itens_perfil import Curso, Documento
from backend.domain.value_objects import CursoId, DocumentoId, UsuarioId

TOKEN_ESTUDANTE_A = "sessao-sintetica-estudante-a"
TOKEN_ESTUDANTE_B = "sessao-sintetica-estudante-b"
TOKEN_INVALIDO = "sessao-invalida-desconhecida"

ID_ESTUDANTE_A = UUID("00000000-0000-4000-8000-0000000000a1")
ID_ESTUDANTE_B = UUID("00000000-0000-4000-8000-0000000000b2")


# Proveniência: decision-analysis prompts/backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md#v001
class AutenticadorSessaoMultiUsuario(AutenticadorSessao):
    """Autentica tokens sintéticos de múltiplos estudantes conhecidos.

    O double consulta um dicionário estático mapeando tokens fixos para suas
    respectivas identidades de usuário e retorna None para credenciais desconhecidas.
    Ele existe para viabilizar testes de controle de acesso e validação de anti-IDOR.
    """

    def __init__(self, mapa_usuarios: dict[str, UsuarioId]) -> None:
        """Inicializa o mapeamento de credenciais conhecidas.

        Armazena os tokens e suas identidades associadas para consulta durante o teste.
        O método existe para permitir isolar múltiplos atores em testes de integração.
        """
        self._mapa = mapa_usuarios

    async def autenticar(self, token: str) -> UsuarioId | None:
        """Resolve a identidade associada ao token de sessão fornecido.

        Compara o token recebido contra o índice de credenciais válidas registradas.
        O método existe para implementar o contrato assíncrono da porta AutenticadorSessao.
        """
        return self._mapa.get(token)


# Proveniência: decision-analysis prompts/backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md#v001
class RepositorioDocumentoEmMemoriaComEstado(RepositorioDocumento):
    """Armazena documentos complementares em memória com controle de estado.

    Mantém um dicionário interno de documentos ativos indexados por identidade
    e registra entidades excluídas em uma lista para observabilidade.
    Ele existe para reproduzir o comportamento do adapter de persistência de documentos.
    """

    def __init__(self) -> None:
        """Inicializa as coleções de documentos ativos e histórico de exclusões.

        Cria o dicionário de documentos e a lista de exclusões vazios.
        O método existe para fornecer isolamento de estado por cenário de teste.
        """
        self.documentos: dict[DocumentoId, Documento] = {}
        self.exclusoes: list[Documento] = []

    async def salvar(self, documento: Documento) -> None:
        """Adiciona ou atualiza um documento no índice em memória.

        Grava a entidade de documento diretamente no dicionário interno.
        O método existe para satisfazer a porta de persistência de documentos complementares.
        """
        self.documentos[documento.id] = documento

    async def obter_por_id(self, documento_id: DocumentoId) -> Documento | None:
        """Recupera um documento ativo pelo seu identificador único.

        Busca a chave fornecida no dicionário de documentos ativos.
        O método existe para permitir a verificação de existência e posse de documentos.
        """
        return self.documentos.get(documento_id)

    async def excluir(self, documento: Documento) -> None:
        """Remove logicamente o documento e registra a operação.

        Retira o documento do índice ativo e o anexa à lista de exclusões realizadas.
        O método existe para simular a exclusão de documentos e permitir asserções no teste.
        """
        self.documentos.pop(documento.id, None)
        self.exclusoes.append(documento)


# Proveniência: decision-analysis prompts/backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md#v001
class ArmazenadorDocumentosFake(ArmazenadorDocumentos):
    """Simula o armazenamento de arquivos binários em memória.

    Registra os bytes recebidos e metadados em uma lista e gera URLs públicas simuladas.
    Ele existe para desacoplar os testes de serviços de armazenamento externo como S3 ou GCS.
    """

    def __init__(self) -> None:
        """Inicializa o histórico de arquivos recebidos pelo fake de armazenamento.

        Cria uma lista interna para acumular as gravações realizadas.
        O método existe para preparar um estado limpo a cada cenário de teste.
        """
        self.arquivos_salvos: list[dict[str, object]] = []

    async def armazenar(
        self,
        conteudo: bytes,
        nome_arquivo: str,
        tipo_arquivo: str,
    ) -> str:
        """Armazena o binário em memória e devolve a URL pública do arquivo.

        Adiciona um registro com conteúdo e metadados à lista e constrói uma URL sintética.
        O método existe para implementar o contrato da porta ArmazenadorDocumentos.
        """
        self.arquivos_salvos.append(
            {
                "conteudo": conteudo,
                "nome_arquivo": nome_arquivo,
                "tipo_arquivo": tipo_arquivo,
            }
        )
        return f"https://storage.local/{nome_arquivo}"


# Proveniência: decision-analysis prompts/backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md#v001
class GeradorDocumentoIdSequencial(GeradorDocumentoId):
    """Gera identificadores de documento determinísticos e únicos.

    Cria novos identificadores UUID versão 4 a cada chamada da porta.
    Ele existe para atender à porta de identificação de novos documentos complementares.
    """

    def gerar(self) -> DocumentoId:
        """Produz uma nova identidade tipada de documento.

        Instancia um novo DocumentoId encapsulando um UUID aleatório gerado no momento.
        O método existe para satisfazer o contrato da porta GeradorDocumentoId.
        """
        return DocumentoId(uuid4())


# Proveniência: decision-analysis prompts/backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md#v001
class RepositorioCursoEmMemoriaComEstado(RepositorioCurso):
    """Armazena cursos complementares em memória com verificação de unicidade.

    Mantém cursos indexados por tuplas de chave única (usuario_id, nome, instituição)
    e pela identidade do curso.
    Ele existe para reproduzir fielmente o adapter de banco de dados de cursos complementares.
    """

    def __init__(self) -> None:
        """Inicializa os índices de cursos por chave lógica e por identidade.

        Cria dicionários vazios para suportar consultas de duplicidade e armazenamento.
        O método existe para fornecer um ambiente de teste isolado e previsível.
        """
        self.cursos_por_id: dict[CursoId, Curso] = {}
        self.chaves_cadastradas: set[tuple[UsuarioId, str, str]] = set()

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        nome_normalizado: str,
        instituicao_normalizada: str,
    ) -> bool:
        """Verifica se já existe curso cadastrado para o estudante nesta instituição.

        Consulta o conjunto de chaves compostas normalizadas já registradas.
        O método existe para permitir que a aplicação previna duplicidades de cursos.
        """
        return (
            usuario_id,
            nome_normalizado,
            instituicao_normalizada,
        ) in self.chaves_cadastradas

    async def salvar(self, curso: Curso) -> None:
        """Persiste o curso no repositório em memória.

        Registra a entidade pelo seu identificador e adiciona sua chave lógica ao índice.
        O método existe para cumprir o contrato de persistência da porta RepositorioCurso.
        """
        self.cursos_por_id[curso.id] = curso
        self.chaves_cadastradas.add(
            (curso.usuario_id, curso.nome_normalizado, curso.instituicao_normalizada)
        )


# Proveniência: decision-analysis prompts/backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md#v001
class GeradorCursoIdSequencial(GeradorCursoId):
    """Gera identificadores tipados de curso em formato UUID.

    Cria um novo CursoId com identificador UUID único a cada invocação.
    Ele existe para satisfazer a porta de geração de IDs da Application.
    """

    def gerar(self) -> CursoId:
        """Produz uma nova identidade tipada de curso complementar.

        Instancia e retorna um CursoId com UUID recém-gerado.
        O método existe para atender à porta GeradorCursoId nos testes integrados.
        """
        return CursoId(uuid4())


# Proveniência: decision-analysis prompts/backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md#v001
async def _requisitar_asgi(
    app: object,
    metodo: str,
    caminho: str,
    token: str | None = None,
    corpo: dict[str, object] | None = None,
) -> tuple[int, object]:
    """Executa uma requisição HTTP diretamente através da interface ASGI da aplicação.

    Configura o escopo ASGI, cabeçalhos de cookie de sessão e corpo JSON, emitindo
    e coletando mensagens via protocolo ASGI em memória sem conexões de rede externas.
    A função existe para exercitar a aplicação FastAPI integrada incluindo middlewares e rotas.
    """
    corpo_bytes = json.dumps(corpo).encode() if corpo is not None else b""
    cabecalhos: list[tuple[bytes, bytes]] = [(b"host", b"testserver")]
    if token is not None:
        cabecalhos.append((b"cookie", f"{COOKIE_SESSAO}={token}".encode()))
    if corpo is not None:
        cabecalhos.extend(
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
        "headers": cabecalhos,
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }

    entregue = False
    status_codigo = 0
    partes: list[bytes] = []

    async def receber() -> dict[str, object]:
        """Entrega o corpo HTTP na primeira leitura e desconecta em leituras subsequentes.

        Retorna a mensagem http.request com o payload binário uma única vez.
        A função existe para atender ao contrato de recepção do protocolo ASGI.
        """
        nonlocal entregue
        if entregue:
            return {"type": "http.disconnect"}
        entregue = True
        return {"type": "http.request", "body": corpo_bytes, "more_body": False}

    async def enviar(mensagem: dict[str, object]) -> None:
        """Captura o status HTTP inicial e acumula os fragmentos do corpo retornado.

        Armazena o código de status e anexa os bytes da resposta à lista de fragmentos.
        A função existe para cumprir o canal de resposta do protocolo ASGI.
        """
        nonlocal status_codigo
        if mensagem["type"] == "http.response.start":
            status_codigo = int(mensagem["status"])
        elif mensagem["type"] == "http.response.body":
            partes.append(mensagem.get("body", b""))

    await app(escopo, receber, enviar)

    dados_resposta = b"".join(partes)
    conteudo_decodificado = json.loads(dados_resposta) if dados_resposta else None
    return status_codigo, conteudo_decodificado


# Proveniência: decision-analysis prompts/backend/20261019-082400-integracao-crud-informacoes-complementares-v001.md#v001
class CrudInformacoesComplementaresIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a integração completa do CRUD de informações complementares pela API.

    Exercita os fluxos de criação e exclusão de documentos complementares e cadastro de cursos,
    cobrindo oráculos de resposta válida e respostas inválidas (401, 404, 409, 422).
    A classe existe para validar o cumprimento dos requisitos RF01 e RF02 na Issue #398.
    """

    def setUp(self) -> None:
        """Configura os repositórios em memória, casos de uso reais e a aplicação ASGI.

        Monta as portas de persistência e armazenamento, instancia os interactors e
        compõe a aplicação FastAPI via create_app com autenticador multi-usuário.
        O método existe para preparar um estado isolado e determinístico antes de cada teste.
        """
        self.usuario_a_id = UsuarioId(ID_ESTUDANTE_A)
        self.usuario_b_id = UsuarioId(ID_ESTUDANTE_B)

        self.repo_documentos = RepositorioDocumentoEmMemoriaComEstado()
        self.storage_documentos = ArmazenadorDocumentosFake()
        self.gerador_doc_id = GeradorDocumentoIdSequencial()

        self.caso_armazenar_documento = ArmazenarDocumento(
            repositorio_documento=self.repo_documentos,
            gerador_documento_id=self.gerador_doc_id,
            armazenador_documentos=self.storage_documentos,
        )
        self.caso_excluir_documento = ExcluirDocumento(
            repositorio_documento=self.repo_documentos
        )

        self.repo_cursos = RepositorioCursoEmMemoriaComEstado()
        self.gerador_curso_id = GeradorCursoIdSequencial()

        self.caso_cadastrar_curso = CadastrarCurso(
            repositorio=self.repo_cursos,
            gerador_id=self.gerador_curso_id,
        )

        self.autenticador = AutenticadorSessaoMultiUsuario(
            {
                TOKEN_ESTUDANTE_A: self.usuario_a_id,
                TOKEN_ESTUDANTE_B: self.usuario_b_id,
            }
        )

        self.app = create_app(
            autenticador_sessao=self.autenticador,
            armazenar_documento=self.caso_armazenar_documento,
            excluir_documento=self.caso_excluir_documento,
            cadastrar_curso=self.caso_cadastrar_curso,
        )

    # -------------------------------------------------------------------------
    # Documentos Complementares: Casos de Sucesso e Respostas Inválidas
    # -------------------------------------------------------------------------

    async def test_cadastro_documento_com_sucesso_retorna_201_e_persiste_metadados(
        self,
    ) -> None:
        """Cadastra e armazena um documento complementar válido para o estudante autenticado.

        Envia uma requisição POST com sessão ativa, payload Base64 correto e tipo PDF,
        validando o código 201 e a criação real nos índices de persistência e storage.
        O teste existe para comprovar o caminho feliz do cadastro de documentos complementares.
        """
        conteudo_bruto = b"Conteudo do certificado em PDF de teste."
        payload = {
            "nome_arquivo": "certificado_python.pdf",
            "tipo_arquivo": "application/pdf",
            "conteudo_base64": base64.b64encode(conteudo_bruto).decode("ascii"),
        }

        status, resposta = await _requisitar_asgi(
            self.app, "POST", "/documentos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )

        self.assertEqual(status, 201)
        self.assertIsInstance(resposta, dict)
        self.assertEqual(resposta["usuario_id"], str(ID_ESTUDANTE_A))
        self.assertEqual(resposta["nome_arquivo"], "certificado_python.pdf")
        self.assertEqual(resposta["tipo_arquivo"], "application/pdf")
        self.assertTrue(
            resposta["url_armazenamento"].startswith("https://storage.local/")
        )

        doc_id = DocumentoId(UUID(resposta["id"]))
        doc_salvo = await self.repo_documentos.obter_por_id(doc_id)
        self.assertIsNotNone(doc_salvo)
        self.assertEqual(doc_salvo.nome_arquivo, "certificado_python.pdf")
        self.assertEqual(len(self.storage_documentos.arquivos_salvos), 1)

    async def test_cadastro_documento_sem_sessao_retorna_401(self) -> None:
        """Rejeita o upload de documento quando não há sessão autenticada.

        Dispara POST sem cookie de sessão e verifica o retorno com código 401 Unauthorized.
        O teste existe para validar a proteção de autenticação na criação de documentos.
        """
        payload = {
            "nome_arquivo": "certificado_python.pdf",
            "tipo_arquivo": "application/pdf",
            "conteudo_base64": base64.b64encode(b"dados").decode("ascii"),
        }

        status, resposta = await _requisitar_asgi(
            self.app, "POST", "/documentos", token=None, corpo=payload
        )

        self.assertEqual(status, 401)
        self.assertEqual(len(self.repo_documentos.documentos), 0)

    async def test_cadastro_documento_com_sessao_invalida_retorna_401(self) -> None:
        """Rejeita o upload de documento quando o token de sessão é desconhecido.

        Envia uma requisição com cookie contendo credencial inexistente e verifica status 401.
        O teste existe para garantir que credenciais forjadas não tenham acesso ao recurso.
        """
        payload = {
            "nome_arquivo": "certificado_python.pdf",
            "tipo_arquivo": "application/pdf",
            "conteudo_base64": base64.b64encode(b"dados").decode("ascii"),
        }

        status, _ = await _requisitar_asgi(
            self.app, "POST", "/documentos", token=TOKEN_INVALIDO, corpo=payload
        )

        self.assertEqual(status, 401)

    async def test_cadastro_documento_payload_incompleto_retorna_422(self) -> None:
        """Rejeita requisições com campos obrigatórios ausentes na fronteira da API.

        Envia um JSON sem o campo conteudo_base64 e verifica a validação Pydantic/FastAPI com código 422.
        O teste existe para certificar que payloads malformados não atingem as regras de domínio.
        """
        payload_incompleto = {
            "nome_arquivo": "certificado.pdf",
            "tipo_arquivo": "application/pdf",
        }

        status, _ = await _requisitar_asgi(
            self.app,
            "POST",
            "/documentos",
            token=TOKEN_ESTUDANTE_A,
            corpo=payload_incompleto,
        )

        self.assertEqual(status, 422)

    async def test_cadastro_documento_base64_corrompido_retorna_422(self) -> None:
        """Rejeita payload com string Base64 não decodificável.

        Envia texto corrompido no campo conteudo_base64 e confirma a tradução do erro em 422.
        O teste existe para validar a integridade de decodificação no caso de uso.
        """
        payload = {
            "nome_arquivo": "documento.pdf",
            "tipo_arquivo": "application/pdf",
            "conteudo_base64": "!!!conteudo-invalido-nao-base64!!!",
        }

        status, resposta = await _requisitar_asgi(
            self.app, "POST", "/documentos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )

        self.assertEqual(status, 422)
        self.assertIn("Base64", str(resposta))

    async def test_cadastro_documento_tipo_arquivo_proibido_retorna_422(self) -> None:
        """Rejeita tipos MIME não suportados pelo domínio de documentos complementares.

        Envia um tipo executável ou inválido e confere a rejeição com código 422.
        O teste existe para proteger o sistema contra upload de extensões e formatos não autorizados.
        """
        payload = {
            "nome_arquivo": "script.sh",
            "tipo_arquivo": "application/x-sh",
            "conteudo_base64": base64.b64encode(b"echo 1").decode("ascii"),
        }

        status, resposta = await _requisitar_asgi(
            self.app, "POST", "/documentos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )

        self.assertEqual(status, 422)
        self.assertIn("Tipo de arquivo não permitido", str(resposta))

    async def test_cadastro_documento_nome_com_path_traversal_retorna_422(self) -> None:
        """Rejeita nomes de arquivo com referências relativas de diretório (Path Traversal).

        Submete nome contendo '../' e valida o bloqueio de segurança com código 422.
        O teste existe para impedir que caminhos inseguros sejam gravados na aplicação.
        """
        payload = {
            "nome_arquivo": "../etc/passwd.pdf",
            "tipo_arquivo": "application/pdf",
            "conteudo_base64": base64.b64encode(b"conteudo").decode("ascii"),
        }

        status, resposta = await _requisitar_asgi(
            self.app, "POST", "/documentos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )

        self.assertEqual(status, 422)
        self.assertIn("barras", str(resposta))

    async def test_exclusao_documento_proprio_com_sucesso_retorna_204(self) -> None:
        """Exclui com sucesso um documento pertencente ao estudante autenticado.

        Cadastra previamente um documento para o Estudante A e envia DELETE autenticado,
        confirmando status 204 No Content e a desativação do registro no repositório.
        O teste existe para validar a operação de exclusão legítima de informações complementares.
        """
        payload = {
            "nome_arquivo": "comprovante.png",
            "tipo_arquivo": "image/png",
            "conteudo_base64": base64.b64encode(b"imagem").decode("ascii"),
        }
        _, criado = await _requisitar_asgi(
            self.app, "POST", "/documentos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )
        doc_id = criado["id"]

        status, _ = await _requisitar_asgi(
            self.app, "DELETE", f"/documentos/{doc_id}", token=TOKEN_ESTUDANTE_A
        )

        self.assertEqual(status, 204)
        doc_consultado = await self.repo_documentos.obter_por_id(
            DocumentoId(UUID(doc_id))
        )
        self.assertIsNone(doc_consultado)
        self.assertEqual(len(self.repo_documentos.exclusoes), 1)

    async def test_exclusao_documento_sem_sessao_retorna_401(self) -> None:
        """Rejeita a exclusão de documento complementar sem sessão autenticada.

        Dispara DELETE sem cookie e verifica a recusa 401 Unauthorized.
        O teste existe para garantir a proteção de rota contra requisições anônimas.
        """
        status, _ = await _requisitar_asgi(
            self.app, "DELETE", f"/documentos/{uuid4()}", token=None
        )

        self.assertEqual(status, 401)

    async def test_exclusao_documento_inexistente_retorna_404(self) -> None:
        """Retorna código 404 quando o identificador de documento não existe.

        Envia DELETE com ID aleatório não cadastrado e confirma a resposta 404 Not Found.
        O teste existe para garantir consistência de resposta em recursos ausentes.
        """
        id_aleatorio = uuid4()
        status, _ = await _requisitar_asgi(
            self.app,
            "DELETE",
            f"/documentos/{id_aleatorio}",
            token=TOKEN_ESTUDANTE_A,
        )

        self.assertEqual(status, 404)

    async def test_exclusao_documento_alheio_retorna_404_anti_idor(self) -> None:
        """Garante que a tentativa de excluir documento de outro estudante retorne 404 uniforme.

        Cadastra documento com o Estudante B e tenta excluí-lo usando a sessão do Estudante A.
        Valida que a API responde 404 e mantém o documento de B intacto no repositório.
        O teste existe para validar a proteção contra exploração IDOR e enumeração de dados alheios.
        """
        payload = {
            "nome_arquivo": "documento_estudante_b.pdf",
            "tipo_arquivo": "application/pdf",
            "conteudo_base64": base64.b64encode(b"dados privados de B").decode("ascii"),
        }
        _, criado_b = await _requisitar_asgi(
            self.app, "POST", "/documentos", token=TOKEN_ESTUDANTE_B, corpo=payload
        )
        id_doc_b = criado_b["id"]

        status, _ = await _requisitar_asgi(
            self.app,
            "DELETE",
            f"/documentos/{id_doc_b}",
            token=TOKEN_ESTUDANTE_A,
        )

        self.assertEqual(status, 404)
        doc_b = await self.repo_documentos.obter_por_id(DocumentoId(UUID(id_doc_b)))
        self.assertIsNotNone(doc_b)
        self.assertEqual(doc_b.usuario_id, self.usuario_b_id)

    async def test_exclusao_documento_ja_removido_retorna_404(self) -> None:
        """Retorna 404 quando uma exclusão é solicitada para um documento já excluído.

        Executa a exclusão de um documento próprio (204) e repete a chamada em seguida,
        verificando a resposta 404 Not Found na segunda requisição.
        O teste existe para assegurar a consistência e transição de estado da remoção.
        """
        payload = {
            "nome_arquivo": "excluir_duas_vezes.pdf",
            "tipo_arquivo": "application/pdf",
            "conteudo_base64": base64.b64encode(b"arquivo").decode("ascii"),
        }
        _, criado = await _requisitar_asgi(
            self.app, "POST", "/documentos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )
        doc_id = criado["id"]

        status1, _ = await _requisitar_asgi(
            self.app, "DELETE", f"/documentos/{doc_id}", token=TOKEN_ESTUDANTE_A
        )
        self.assertEqual(status1, 204)

        status2, _ = await _requisitar_asgi(
            self.app, "DELETE", f"/documentos/{doc_id}", token=TOKEN_ESTUDANTE_A
        )
        self.assertEqual(status2, 404)

    # -------------------------------------------------------------------------
    # Cursos Complementares: Casos de Sucesso e Respostas Inválidas
    # -------------------------------------------------------------------------

    async def test_cadastro_curso_com_sucesso_retorna_201_e_persiste_registro(
        self,
    ) -> None:
        """Cadastra um curso complementar completo para o estudante autenticado.

        Envia requisição POST com nome, instituição e carga horária e sessão válida,
        confirmando código 201 Created e o correto armazenamento no repositório.
        O teste existe para validar o caminho feliz do cadastro de cursos complementares.
        """
        payload = {
            "nome": "Desenvolvimento com FastAPI",
            "instituicao": "Alura",
            "carga_horaria": 40,
        }

        status, resposta = await _requisitar_asgi(
            self.app, "POST", "/cursos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )

        self.assertEqual(status, 201)
        self.assertIsInstance(resposta, dict)
        self.assertEqual(resposta["usuario_id"], str(ID_ESTUDANTE_A))
        self.assertEqual(resposta["nome"], "Desenvolvimento com FastAPI")
        self.assertEqual(resposta["instituicao"], "Alura")
        self.assertEqual(resposta["carga_horaria"], 40)

        self.assertEqual(len(self.repo_cursos.cursos_por_id), 1)

    async def test_cadastro_curso_sem_carga_horaria_retorna_201(self) -> None:
        """Cadastra curso complementar com carga horária omitida.

        Envia payload apenas com nome e instituição sem carga horária e confere status 201.
        O teste existe para garantir a flexibilidade de campos opcionais no contrato de cursos.
        """
        payload = {
            "nome": "Introdução a Arquitetura Limpa",
            "instituicao": "Tech Academy",
        }

        status, resposta = await _requisitar_asgi(
            self.app, "POST", "/cursos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )

        self.assertEqual(status, 201)
        self.assertIsNone(resposta["carga_horaria"])

    async def test_cadastro_curso_sem_sessao_retorna_401(self) -> None:
        """Rejeita o cadastro de curso complementar sem autenticação.

        Envia POST para /cursos sem credencial e confirma resposta com código 401.
        O teste existe para garantir que a rota de cursos exija sessão ativa.
        """
        payload = {
            "nome": "Curso Protegido",
            "instituicao": "Universidade",
            "carga_horaria": 20,
        }

        status, _ = await _requisitar_asgi(
            self.app, "POST", "/cursos", token=None, corpo=payload
        )

        self.assertEqual(status, 401)
        self.assertEqual(len(self.repo_cursos.cursos_por_id), 0)

    async def test_cadastro_curso_duplicado_para_mesmo_estudante_retorna_409(
        self,
    ) -> None:
        """Rejeita tentativa de cadastrar curso duplicado para o mesmo estudante e instituição.

        Cadastra o curso com sucesso na primeira chamada e submete o mesmo payload na segunda,
        validando a resposta 409 Conflict decorrente de violação da chave de unicidade.
        O teste existe para certificar o tratamento de duplicidade exigido pela aplicação.
        """
        payload = {
            "nome": "Microsserviços em Go",
            "instituicao": "Cloud Academy",
            "carga_horaria": 60,
        }

        status1, _ = await _requisitar_asgi(
            self.app, "POST", "/cursos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )
        self.assertEqual(status1, 201)

        status2, resposta2 = await _requisitar_asgi(
            self.app, "POST", "/cursos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )
        self.assertEqual(status2, 409)
        self.assertIn("já cadastrado", str(resposta2))

    async def test_cadastro_curso_nome_vazio_retorna_422(self) -> None:
        """Rejeita cadastro de curso com nome vazio em violação de regra de domínio.

        Envia string vazia como nome e valida a conversão da RegraDeDominioViolada em código 422.
        O teste existe para assegurar a proteção de invariantes do domínio no transporte HTTP.
        """
        payload = {
            "nome": "   ",
            "instituicao": "Instituição Válida",
            "carga_horaria": 10,
        }

        status, _ = await _requisitar_asgi(
            self.app, "POST", "/cursos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )

        self.assertEqual(status, 422)

    async def test_cadastro_curso_carga_horaria_negativa_retorna_422(self) -> None:
        """Rejeita carga horária negativa ou fora dos limites permitidos pelo domínio.

        Envia carga_horaria=-5 e verifica o retorno 422 Unprocessable Content.
        O teste existe para garantir a integridade dos atributos numéricos de cursos.
        """
        payload = {
            "nome": "Curso Teste",
            "instituicao": "Instituição Válida",
            "carga_horaria": -5,
        }

        status, _ = await _requisitar_asgi(
            self.app, "POST", "/cursos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )

        self.assertEqual(status, 422)

    async def test_cadastro_curso_carga_horaria_tipo_invalido_retorna_422(
        self,
    ) -> None:
        """Rejeita formato inválido para carga horária na validação Pydantic de entrada.

        Envia uma string não numérica no campo de carga horária e valida status 422.
        O teste existe para comprovar a rejeição de tipo na fronteira externa da API.
        """
        payload = {
            "nome": "Curso Teste",
            "instituicao": "Instituição Válida",
            "carga_horaria": "quarenta horas",
        }

        status, _ = await _requisitar_asgi(
            self.app, "POST", "/cursos", token=TOKEN_ESTUDANTE_A, corpo=payload
        )

        self.assertEqual(status, 422)
