"""Testa unitariamente a rota HTTP de prévia de versão de currículo."""

import unittest
from datetime import date
from uuid import uuid4

from fastapi import HTTPException

from backend.api.previa_versao_curriculo import PreviaVersaoCurriculoResposta, criar_router
from backend.application import (
    CurriculoNaoEncontrado,
    GerarPreviaVersaoCurriculoEntrada,
    PreviaVersaoCurriculo,
)
from backend.domain import (
    Competencia,
    CompetenciaId,
    Curriculo,
    CurriculoId,
    DadosContato,
    Documento,
    DocumentoId,
    Email,
    Endereco,
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    FormacaoAcademica,
    FormacaoAcademicaId,
    HashSenha,
    Idioma,
    IdiomaId,
    Nome,
    Periodo,
    ProjetoAcademico,
    ProjetoAcademicoId,
    Telefone,
    Usuario,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001

CAMINHO_PREVIA = "/estudantes/{usuario_id}/curriculos/{curriculo_id}/previa"
HASH_SENHA = "$scrypt$ln=16,r=8,p=1$fakehashparaestudantedeteste"
URL_ARMAZENAMENTO = "armazenamento/interno/arquivo"


class PreviaExecutorDouble:
    """Substitui o caso de uso de prévia e registra as entradas recebidas.

    O double devolve um resultado ou levanta um erro pré-configurado, sem tocar
    portas, banco ou domínio de verdade. Ele existe para testar a tradução HTTP
    da rota isoladamente da orquestração da Application.
    """

    def __init__(self, resultado: PreviaVersaoCurriculo | None = None, erro: Exception | None = None) -> None:
        """Guarda o comportamento configurado e inicia o histórico de chamadas.

        O construtor não acessa recursos externos. Ele existe para permitir que
        cada teste configure sucesso ou falha de forma explícita.
        """
        self._resultado = resultado
        self._erro = erro
        self.entradas: list[GerarPreviaVersaoCurriculoEntrada] = []

    async def executar(self, entrada: GerarPreviaVersaoCurriculoEntrada) -> PreviaVersaoCurriculo:
        """Registra a entrada recebida e devolve o resultado ou levanta o erro.

        O método aguarda de forma trivial, sem I/O real. Ele existe para tornar
        observável o que o handler HTTP enviou ao caso de uso.
        """
        self.entradas.append(entrada)
        if self._erro is not None:
            raise self._erro
        if self._resultado is None:
            raise AssertionError("O double não recebeu resultado nem erro configurado.")
        return self._resultado


def _rota(caminho: str, metodo: str, executor: PreviaExecutorDouble | None):
    """Localiza a rota registrada para inspeção e chamada direta em teste.

    A função cria o router com o executor dado e varre suas rotas por caminho e
    método HTTP, devolvendo o objeto da rota, que expõe o endpoint e a
    configuração declarada. Ela existe para exercitar o handler sem iniciar
    servidor ASGI ou cliente HTTP real.
    """
    for rota in criar_router(executor).routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


def _criar_previa(com_contato: bool = True, completa: bool = True) -> PreviaVersaoCurriculo:
    """Cria um modelo de leitura de prévia válido para o double devolver.

    A função monta estudante, versão e, quando pedido, um item de cada seção
    com valores reconhecíveis, incluindo dados que não podem aparecer na
    resposta. Ela existe para reduzir repetição mantendo cada teste focado na
    tradução HTTP.
    """
    usuario_id = UsuarioId(uuid4())
    contato = DadosContato(
        endereco=Endereco("Avenida Tiradentes, 615"),
        telefones=(Telefone("(11) 98765-4321"), Telefone("(11) 3322-1100")),
        linkedin="https://linkedin.com/in/estudante",
        curriculo_lattes=None,
    )
    usuario = Usuario(
        id=usuario_id,
        nome=Nome("Ana Carolina da Silva"),
        email=Email("ana.silva@fatec.sp.gov.br"),
        hash_senha=HashSenha(HASH_SENHA),
        dados_contato=contato if com_contato else None,
    )
    curriculo = Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id,
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )
    if not completa:
        return PreviaVersaoCurriculo(usuario, curriculo, (), (), (), (), (), ())
    return PreviaVersaoCurriculo(
        usuario=usuario,
        curriculo=curriculo,
        formacoes=(
            FormacaoAcademica(
                id=FormacaoAcademicaId(uuid4()),
                usuario_id=usuario_id,
                instituicao="FATEC",
                curso="ADS",
                nivel="Graduação",
                periodo=Periodo(inicio=date(2023, 2, 1), fim=date(2025, 12, 20)),
                status="Em andamento",
            ),
        ),
        experiencias=(
            ExperienciaProfissional(
                id=ExperienciaProfissionalId(uuid4()),
                usuario_id=usuario_id,
                empresa="Empresa",
                cargo="Estagiária",
                descricao="Desenvolvimento de APIs.",
                periodo=Periodo(inicio=date(2024, 1, 15)),
            ),
        ),
        projetos=(
            ProjetoAcademico(
                id=ProjetoAcademicoId(uuid4()),
                usuario_id=usuario_id,
                titulo="Sistema de currículo",
                descricao="Plataforma de currículos.",
                tecnologias="Python, FastAPI",
            ),
        ),
        competencias=(
            Competencia(id=CompetenciaId(uuid4()), usuario_id=usuario_id, descricao="Python", nivel="Avançado"),
        ),
        idiomas=(Idioma(id=IdiomaId(uuid4()), usuario_id=usuario_id, idioma="Inglês", nivel="Avançado"),),
        documentos=(
            Documento(
                id=DocumentoId(uuid4()),
                usuario_id=usuario_id,
                nome_arquivo="historico.pdf",
                tipo_arquivo="application/pdf",
                url_armazenamento=URL_ARMAZENAMENTO,
            ),
        ),
    )


class PreviaVersaoCurriculoRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP da prévia pela rota GET.

    A classe substitui o caso de uso por um double e observa o que a rota envia
    e devolve. Ela existe para testar a unidade de interface isoladamente da
    Application e da infraestrutura.
    """

    async def test_devolve_a_previa_publica_e_envia_a_entrada_correta(self) -> None:
        """Confirma a resposta por seção e a entrada enviada ao caso de uso.

        O teste configura um double de sucesso com um item de cada seção, chama
        o handler e compara a resposta pública, preservando a ordem recebida, e
        a entrada registrada. Ele existe para proteger o contrato da prévia.
        """
        previa = _criar_previa()
        executor = PreviaExecutorDouble(resultado=previa)
        gerar = _rota(CAMINHO_PREVIA, "GET", executor).endpoint

        resposta = await gerar(usuario_id=previa.usuario.id.valor, curriculo_id=previa.curriculo.id.valor)

        self.assertIsInstance(resposta, PreviaVersaoCurriculoResposta)
        self.assertEqual(resposta.curriculo_id, previa.curriculo.id.valor)
        self.assertEqual((resposta.titulo_versao, resposta.layout), ("Estágio em TI", "classico"))
        self.assertEqual(resposta.estudante.nome, "Ana Carolina da Silva")
        self.assertEqual(resposta.estudante.email, "ana.silva@fatec.sp.gov.br")
        self.assertEqual(resposta.estudante.contato.endereco, "Avenida Tiradentes, 615")
        self.assertEqual(resposta.estudante.contato.telefones, ["(11) 98765-4321", "(11) 3322-1100"])
        self.assertEqual(resposta.estudante.contato.linkedin, "https://linkedin.com/in/estudante")
        self.assertIsNone(resposta.estudante.contato.curriculo_lattes)
        formacao, experiencia = resposta.formacoes[0], resposta.experiencias[0]
        self.assertEqual((formacao.id, formacao.curso, formacao.inicio, formacao.fim), (
            previa.formacoes[0].id.valor, "ADS", date(2023, 2, 1), date(2025, 12, 20)
        ))
        self.assertEqual((experiencia.cargo, experiencia.inicio, experiencia.fim), ("Estagiária", date(2024, 1, 15), None))
        self.assertEqual(resposta.projetos[0].tecnologias, "Python, FastAPI")
        self.assertEqual(resposta.competencias[0].descricao, "Python")
        self.assertEqual(resposta.idiomas[0].idioma, "Inglês")
        self.assertEqual(
            (resposta.documentos[0].nome_arquivo, resposta.documentos[0].tipo_arquivo),
            ("historico.pdf", "application/pdf"),
        )
        self.assertEqual(
            executor.entradas,
            [GerarPreviaVersaoCurriculoEntrada(previa.usuario.id, previa.curriculo.id)],
        )

    async def test_resposta_nao_expoe_credencial_nem_armazenamento_nem_identidades_internas(self) -> None:
        """Confirma que a resposta serializada omite dados internos e sensíveis.

        O teste serializa a resposta completa e procura o hash de senha, o
        caminho de armazenamento e o identificador do estudante. Ele existe para
        proteger a minimização de dados da fronteira.
        """
        previa = _criar_previa()
        gerar = _rota(CAMINHO_PREVIA, "GET", PreviaExecutorDouble(resultado=previa)).endpoint

        resposta = await gerar(usuario_id=previa.usuario.id.valor, curriculo_id=previa.curriculo.id.valor)

        texto = resposta.model_dump_json()
        self.assertNotIn(HASH_SENHA, texto)
        self.assertNotIn(URL_ARMAZENAMENTO, texto)
        self.assertNotIn(str(previa.usuario.id.valor), texto)

    async def test_estudante_sem_contato_e_versao_vazia_geram_resposta_valida(self) -> None:
        """Confirma contato nulo e seções vazias na resposta.

        O teste usa um estudante sem dados de contato e uma versão sem itens e
        observa o contato ausente e as listas vazias. Ele existe para proteger
        os casos de perfil incompleto e de versão recém-criada.
        """
        previa = _criar_previa(com_contato=False, completa=False)
        gerar = _rota(CAMINHO_PREVIA, "GET", PreviaExecutorDouble(resultado=previa)).endpoint

        resposta = await gerar(usuario_id=previa.usuario.id.valor, curriculo_id=previa.curriculo.id.valor)

        self.assertIsNone(resposta.estudante.contato)
        self.assertEqual(
            (resposta.formacoes, resposta.experiencias, resposta.projetos,
             resposta.competencias, resposta.idiomas, resposta.documentos),
            ([], [], [], [], [], []),
        )

    async def test_declara_modelo_de_resposta_publico(self) -> None:
        """Confirma o modelo de resposta declarado na rota registrada.

        O teste inspeciona a configuração da rota, já que a chamada direta ao
        handler não passa pela camada que aplica o modelo. Ele existe para
        proteger o contrato HTTP da prévia.
        """
        rota = _rota(CAMINHO_PREVIA, "GET", None)

        self.assertIs(rota.response_model, PreviaVersaoCurriculoResposta)

    async def test_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum caso de uso de prévia foi injetado.

        O teste chama o handler sem executor e observa a indisponibilidade
        explícita antes de qualquer outra decisão.
        """
        gerar = _rota(CAMINHO_PREVIA, "GET", None).endpoint

        with self.assertRaises(HTTPException) as contexto:
            await gerar(usuario_id=uuid4(), curriculo_id=uuid4())

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_ausencia_ou_propriedade_alheia_vira_404(self) -> None:
        """Confirma 404 quando o caso de uso sinaliza versão não encontrada.

        O teste configura o double para a falha de não encontrado e observa a
        tradução HTTP preservando a mensagem. Ele existe para proteger a negação
        sem revelar a diferença entre ausência e propriedade alheia.
        """
        erro = CurriculoNaoEncontrado("Versão de currículo não encontrada.")
        gerar = _rota(CAMINHO_PREVIA, "GET", PreviaExecutorDouble(erro=erro)).endpoint

        with self.assertRaises(HTTPException) as contexto:
            await gerar(usuario_id=uuid4(), curriculo_id=uuid4())

        self.assertEqual(contexto.exception.status_code, 404)
        self.assertEqual(contexto.exception.detail, str(erro))
