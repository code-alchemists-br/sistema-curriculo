"""Testa unitariamente o caso de uso de prévia de versão de currículo."""

import unittest
from datetime import date, datetime
from uuid import uuid4

from backend.application import (
    CurriculoNaoEncontrado,
    GerarPreviaVersaoCurriculo,
    GerarPreviaVersaoCurriculoEntrada,
)
from backend.domain import (
    Competencia,
    CompetenciaId,
    Curriculo,
    CurriculoId,
    Documento,
    DocumentoId,
    Email,
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
    ReferenciaCurriculo,
    Usuario,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001


class RepositorioCurriculoSpy:
    """Substitui a porta de currículo e registra qualquer escrita solicitada.

    O double consulta agregados em memória por ID e acumula tentativas de
    atualização ou salvamento. Ele existe para provar que a prévia é somente
    leitura, sem ORM, banco, rede ou adapter produtivo.
    """

    def __init__(self, curriculos: list[Curriculo] | None = None) -> None:
        """Prepara um índice em memória e históricos vazios de consulta e escrita.

        O construtor copia os currículos fornecidos em um dicionário por
        identidade. Ele existe para controlar ausência e propriedade em cada
        cenário testado.
        """
        self._por_id = {curriculo.id: curriculo for curriculo in (curriculos or [])}
        self.consultas: list[CurriculoId] = []
        self.escritas: list[Curriculo] = []

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Registra a consulta e devolve por coroutine a versão do ID informado.

        O método consulta somente o dicionário controlado pelo teste e não faz
        I/O. Ele existe para simular a leitura aguardável exigida pelo caso.
        """
        self.consultas.append(curriculo_id)
        return self._por_id.get(curriculo_id)

    async def atualizar(self, curriculo: Curriculo) -> None:
        """Registra por coroutine uma tentativa indevida de atualização.

        O método acumula o agregado sem persistir. Ele existe para tornar
        observável qualquer escrita que a prévia não deveria fazer.
        """
        self.escritas.append(curriculo)

    async def salvar(self, curriculo: Curriculo) -> None:
        """Registra por coroutine uma tentativa indevida de salvamento.

        O método acumula o agregado sem persistir. Ele existe para tornar
        observável qualquer escrita que a prévia não deveria fazer.
        """
        self.escritas.append(curriculo)


class RepositorioUsuarioStub:
    """Substitui a porta de usuário devolvendo estudantes controlados pelo teste.

    O double indexa usuários em memória e registra as consultas feitas. Ele
    existe para testar a identificação do estudante sem banco ou adapter.
    """

    def __init__(self, usuarios: list[Usuario] | None = None) -> None:
        """Prepara o índice de usuários e o histórico vazio de consultas.

        O construtor copia os usuários fornecidos por identidade. Ele existe
        para controlar presença e exclusão do estudante em cada cenário.
        """
        self._por_id = {usuario.id: usuario for usuario in (usuarios or [])}
        self.consultas: list[UsuarioId] = []

    async def obter_por_id(self, usuario_id: UsuarioId) -> Usuario | None:
        """Registra a consulta e devolve por coroutine o usuário do ID informado.

        O método consulta somente o dicionário do teste. Ele existe para
        simular a leitura aguardável exigida pelo caso de uso.
        """
        self.consultas.append(usuario_id)
        return self._por_id.get(usuario_id)


class ConsultaItemStub:
    """Substitui a porta de leitura de itens por respostas controladas pelo teste.

    O double devolve o item configurado para cada referência, ou ausência, e
    registra as referências consultadas. Ele existe para testar filtragem e
    ordenação sem tabelas de itens nem adapters.
    """

    def __init__(self, itens: dict[ReferenciaCurriculo, object] | None = None) -> None:
        """Guarda o mapa de respostas e inicia o histórico de consultas.

        O construtor armazena as respostas fornecidas. Ele existe para permitir
        que cada teste configure itens presentes, ausentes ou inconsistentes.
        """
        self._itens = itens or {}
        self.consultas: list[ReferenciaCurriculo] = []

    async def obter_item(self, referencia: ReferenciaCurriculo) -> object | None:
        """Registra a consulta e devolve por coroutine o item configurado.

        O método não faz I/O e não aplica regra de propriedade. Ele existe para
        simular o contrato da porta mantendo a decisão no caso de uso.
        """
        self.consultas.append(referencia)
        return self._itens.get(referencia)


def _criar_usuario(usuario_id: UsuarioId | None = None, excluido: bool = False) -> Usuario:
    """Cria um estudante válido, opcionalmente excluído, para os cenários.

    A função monta o agregado com value objects válidos e fixa ``deleted_at``
    quando pedido. Ela existe para reduzir repetição mantendo cada teste focado
    na decisão observada.
    """
    return Usuario(
        id=usuario_id or UsuarioId(uuid4()),
        nome=Nome("Ana Carolina da Silva"),
        email=Email("ana.silva@fatec.sp.gov.br"),
        hash_senha=HashSenha("$scrypt$ln=16,r=8,p=1$fakehashparaestudantedeteste"),
        deleted_at=datetime(2026, 1, 1) if excluido else None,
    )


def _criar_curriculo(usuario_id: UsuarioId, *itens: object) -> Curriculo:
    """Cria uma versão válida do usuário já com as referências dos itens dados.

    A função constrói o agregado e inclui a referência de cada item pelo seu
    identificador. Ela existe para montar a seleção da versão em cada cenário.
    """
    curriculo = Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id,
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )
    for item in itens:
        curriculo.incluir_referencia(ReferenciaCurriculo(item.id))  # type: ignore[attr-defined]
    return curriculo


def _formacao(usuario_id: UsuarioId, inicio: date, curso: str = "ADS") -> FormacaoAcademica:
    """Cria uma formação válida do usuário com o início de período indicado.

    A função fixa os demais campos com valores neutros. Ela existe para variar
    apenas o que a ordenação observa.
    """
    return FormacaoAcademica(
        id=FormacaoAcademicaId(uuid4()),
        usuario_id=usuario_id,
        instituicao="FATEC",
        curso=curso,
        nivel="Graduação",
        periodo=Periodo(inicio=inicio),
        status="Em andamento",
    )


def _experiencia(usuario_id: UsuarioId, inicio: date) -> ExperienciaProfissional:
    """Cria uma experiência válida do usuário com o início de período indicado.

    A função fixa os demais campos com valores neutros. Ela existe para variar
    apenas o que a ordenação observa.
    """
    return ExperienciaProfissional(
        id=ExperienciaProfissionalId(uuid4()),
        usuario_id=usuario_id,
        empresa="Empresa",
        cargo="Estagiária",
        descricao="Desenvolvimento de APIs.",
        periodo=Periodo(inicio=inicio),
    )


def _projeto(usuario_id: UsuarioId, titulo: str) -> ProjetoAcademico:
    """Cria um projeto válido do usuário com o título indicado.

    A função fixa os demais campos com valores neutros. Ela existe para variar
    apenas o texto observado pela ordenação.
    """
    return ProjetoAcademico(
        id=ProjetoAcademicoId(uuid4()),
        usuario_id=usuario_id,
        titulo=titulo,
        descricao="Descrição.",
        tecnologias="Python",
    )


def _competencia(usuario_id: UsuarioId, descricao: str) -> Competencia:
    """Cria uma competência do usuário com a descrição indicada.

    A função fixa o nível com valor neutro. Ela existe para variar apenas o
    texto observado pela ordenação.
    """
    return Competencia(id=CompetenciaId(uuid4()), usuario_id=usuario_id, descricao=descricao, nivel="Avançado")


def _idioma(usuario_id: UsuarioId, idioma: str) -> Idioma:
    """Cria um idioma do usuário com o nome indicado.

    A função fixa o nível com valor neutro. Ela existe para variar apenas o
    texto observado pela ordenação.
    """
    return Idioma(id=IdiomaId(uuid4()), usuario_id=usuario_id, idioma=idioma, nivel="Avançado")


def _documento(usuario_id: UsuarioId, nome_arquivo: str) -> Documento:
    """Cria um documento do usuário com o nome de arquivo indicado.

    A função fixa tipo e caminho de armazenamento com valores neutros. Ela
    existe para variar apenas o texto observado pela ordenação.
    """
    return Documento(
        id=DocumentoId(uuid4()),
        usuario_id=usuario_id,
        nome_arquivo=nome_arquivo,
        tipo_arquivo="application/pdf",
        url_armazenamento="armazenamento/interno/arquivo",
    )


def _consulta_para(*itens: object) -> ConsultaItemStub:
    """Cria o stub de leitura que devolve cada item pela sua própria referência.

    A função indexa os itens pelo identificador tipado. Ela existe para o
    cenário comum em que toda referência resolve para o item correto.
    """
    return ConsultaItemStub({ReferenciaCurriculo(item.id): item for item in itens})  # type: ignore[attr-defined]


class GerarPreviaVersaoCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``GerarPreviaVersaoCurriculo``.

    A classe substitui as portas de currículo, usuário e itens por estado em
    memória e observa resultado, filtragem e ausência de escrita. Ela existe
    para testar a unidade Application sem adapter, framework ou infraestrutura.
    """

    async def test_agrupa_os_itens_por_secao_em_ordem_deterministica(self) -> None:
        """Confirma seções preenchidas e ordenadas independentemente da seleção.

        O teste seleciona itens de todos os tipos fora de ordem e compara as
        tuplas devolvidas: períodos do mais recente ao mais antigo e textos em
        ordem alfabética sem diferenciar caixa. Ele existe para proteger o
        contrato de saída que o cliente apresenta.
        """
        usuario = _criar_usuario()
        formacao_antiga = _formacao(usuario.id, date(2018, 2, 1))
        formacao_recente = _formacao(usuario.id, date(2023, 2, 1))
        experiencia_antiga = _experiencia(usuario.id, date(2020, 1, 1))
        experiencia_recente = _experiencia(usuario.id, date(2024, 1, 1))
        projeto_b = _projeto(usuario.id, "beta")
        projeto_a = _projeto(usuario.id, "Alfa")
        competencia_b = _competencia(usuario.id, "SQL")
        competencia_a = _competencia(usuario.id, "python")
        idioma_b = _idioma(usuario.id, "Inglês")
        idioma_a = _idioma(usuario.id, "alemão")
        documento_b = _documento(usuario.id, "Certificado.pdf")
        documento_a = _documento(usuario.id, "boletim.pdf")
        itens = (
            formacao_antiga, formacao_recente, experiencia_antiga, experiencia_recente,
            projeto_b, projeto_a, competencia_b, competencia_a, idioma_b, idioma_a,
            documento_b, documento_a,
        )
        curriculo = _criar_curriculo(usuario.id, *itens)
        caso = GerarPreviaVersaoCurriculo(
            RepositorioCurriculoSpy([curriculo]),
            RepositorioUsuarioStub([usuario]),
            _consulta_para(*itens),
        )

        previa = await caso.executar(GerarPreviaVersaoCurriculoEntrada(usuario.id, curriculo.id))

        self.assertIs(previa.usuario, usuario)
        self.assertIs(previa.curriculo, curriculo)
        self.assertEqual(previa.formacoes, (formacao_recente, formacao_antiga))
        self.assertEqual(previa.experiencias, (experiencia_recente, experiencia_antiga))
        self.assertEqual(previa.projetos, (projeto_a, projeto_b))
        self.assertEqual(previa.competencias, (competencia_a, competencia_b))
        self.assertEqual(previa.idiomas, (idioma_a, idioma_b))
        self.assertEqual(previa.documentos, (documento_a, documento_b))

    async def test_mesma_selecao_em_ordens_diferentes_produz_a_mesma_previa(self) -> None:
        """Confirma que a ordem de inclusão das referências não altera a saída.

        O teste cria duas versões com os mesmos itens incluídos em ordens
        opostas e compara as duas prévias, inclusive com textos iguais que
        dependem do desempate por identificador. Ele existe para proteger o
        determinismo apesar de a seleção ser um conjunto.
        """
        usuario = _criar_usuario()
        projetos = tuple(_projeto(usuario.id, "Mesmo título") for _ in range(4))
        primeira = _criar_curriculo(usuario.id, *projetos)
        segunda = _criar_curriculo(usuario.id, *reversed(projetos))
        caso = GerarPreviaVersaoCurriculo(
            RepositorioCurriculoSpy([primeira, segunda]),
            RepositorioUsuarioStub([usuario]),
            _consulta_para(*projetos),
        )

        previa_primeira = await caso.executar(GerarPreviaVersaoCurriculoEntrada(usuario.id, primeira.id))
        previa_segunda = await caso.executar(GerarPreviaVersaoCurriculoEntrada(usuario.id, segunda.id))

        self.assertEqual(previa_primeira.projetos, previa_segunda.projetos)

    async def test_versao_sem_itens_devolve_secoes_vazias_sem_consultar_itens(self) -> None:
        """Confirma que uma versão sem seleção produz prévia vazia e sem leitura de itens.

        O teste usa uma versão sem referências e observa as tuplas vazias e o
        histórico de consultas da porta de itens. Ele existe para proteger o
        caso de uma versão recém-criada.
        """
        usuario = _criar_usuario()
        curriculo = _criar_curriculo(usuario.id)
        consulta = ConsultaItemStub()
        caso = GerarPreviaVersaoCurriculo(
            RepositorioCurriculoSpy([curriculo]), RepositorioUsuarioStub([usuario]), consulta
        )

        previa = await caso.executar(GerarPreviaVersaoCurriculoEntrada(usuario.id, curriculo.id))

        self.assertEqual(
            (previa.formacoes, previa.experiencias, previa.projetos, previa.competencias, previa.idiomas, previa.documentos),
            ((), (), (), (), (), ()),
        )
        self.assertEqual(consulta.consultas, [])

    async def test_omite_item_ausente_alheio_ou_inconsistente_sem_falhar(self) -> None:
        """Confirma que somente itens existentes, próprios e coerentes entram na prévia.

        O teste referencia um item válido, um inexistente, um de outro
        proprietário e um cuja identidade difere da referência. Ele existe para
        proteger a regra de nunca exibir dado alheio e de não quebrar a prévia
        por causa de um item excluído.
        """
        usuario = _criar_usuario()
        outro_usuario_id = UsuarioId(uuid4())
        valido = _projeto(usuario.id, "Válido")
        inexistente = _projeto(usuario.id, "Excluído")
        alheio = _projeto(outro_usuario_id, "Alheio")
        referenciado = _projeto(usuario.id, "Referenciado")
        outro_item = _projeto(usuario.id, "Outro item")
        curriculo = _criar_curriculo(usuario.id, valido, inexistente, alheio, referenciado)
        consulta = ConsultaItemStub(
            {
                ReferenciaCurriculo(valido.id): valido,
                ReferenciaCurriculo(alheio.id): alheio,
                ReferenciaCurriculo(referenciado.id): outro_item,
            }
        )
        caso = GerarPreviaVersaoCurriculo(
            RepositorioCurriculoSpy([curriculo]), RepositorioUsuarioStub([usuario]), consulta
        )

        previa = await caso.executar(GerarPreviaVersaoCurriculoEntrada(usuario.id, curriculo.id))

        self.assertEqual(previa.projetos, (valido,))
        self.assertEqual(len(consulta.consultas), 4)

    async def test_nao_solicita_nenhuma_escrita(self) -> None:
        """Confirma que gerar a prévia não atualiza nem salva nenhuma versão.

        O teste executa uma prévia com itens e observa o histórico de escritas
        do double. Ele existe para proteger a natureza de consulta da operação.
        """
        usuario = _criar_usuario()
        projeto = _projeto(usuario.id, "Alfa")
        curriculo = _criar_curriculo(usuario.id, projeto)
        repositorio = RepositorioCurriculoSpy([curriculo])
        caso = GerarPreviaVersaoCurriculo(repositorio, RepositorioUsuarioStub([usuario]), _consulta_para(projeto))

        await caso.executar(GerarPreviaVersaoCurriculoEntrada(usuario.id, curriculo.id))

        self.assertEqual(repositorio.escritas, [])

    async def test_versao_inexistente_ou_alheia_falha_sem_consultar_usuario_nem_itens(self) -> None:
        """Confirma a mesma falha para versão ausente e versão de outro usuário.

        O teste cobre os dois cenários e observa que nem o estudante nem os
        itens são consultados depois da negação. Ele existe para impedir
        vazamento de dados alheios e distinção entre ausência e posse alheia.
        """
        usuario = _criar_usuario()
        projeto = _projeto(usuario.id, "Alfa")
        curriculo_alheio = _criar_curriculo(UsuarioId(uuid4()), projeto)
        for curriculo_id in (CurriculoId(uuid4()), curriculo_alheio.id):
            with self.subTest(curriculo_id=curriculo_id):
                repositorio_usuario = RepositorioUsuarioStub([usuario])
                consulta = _consulta_para(projeto)
                caso = GerarPreviaVersaoCurriculo(
                    RepositorioCurriculoSpy([curriculo_alheio]), repositorio_usuario, consulta
                )

                with self.assertRaises(CurriculoNaoEncontrado):
                    await caso.executar(GerarPreviaVersaoCurriculoEntrada(usuario.id, curriculo_id))

                self.assertEqual(repositorio_usuario.consultas, [])
                self.assertEqual(consulta.consultas, [])

    async def test_estudante_ausente_ou_excluido_falha_sem_consultar_itens(self) -> None:
        """Confirma a falha quando o estudante não existe ou está logicamente excluído.

        O teste cobre os dois cenários com uma versão própria e observa que os
        itens não são consultados. Ele existe para proteger a identificação
        indispensável da prévia e a exclusão lógica do perfil.
        """
        usuario_id = UsuarioId(uuid4())
        projeto = _projeto(usuario_id, "Alfa")
        curriculo = _criar_curriculo(usuario_id, projeto)
        for usuarios in ([], [_criar_usuario(usuario_id, excluido=True)]):
            with self.subTest(usuarios=len(usuarios)):
                consulta = _consulta_para(projeto)
                caso = GerarPreviaVersaoCurriculo(
                    RepositorioCurriculoSpy([curriculo]), RepositorioUsuarioStub(usuarios), consulta
                )

                with self.assertRaises(CurriculoNaoEncontrado):
                    await caso.executar(GerarPreviaVersaoCurriculoEntrada(usuario_id, curriculo.id))

                self.assertEqual(consulta.consultas, [])
