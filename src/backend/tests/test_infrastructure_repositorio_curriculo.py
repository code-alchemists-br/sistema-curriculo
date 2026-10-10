"""Protege a persistência de currículos com doubles, sem conexão com banco."""

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain import (
    CompetenciaId,
    Curriculo,
    CurriculoId,
    DocumentoId,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    IdiomaId,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.curriculo import (
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    CurriculoItemRegistro,
    CurriculoRegistro,
    atualizar_registro,
    para_curriculo,
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    para_referencia,
    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    para_registro,
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    para_registros_itens,
    para_tipo_e_item_id,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_curriculo import (
    RepositorioCurriculoSqlAlchemy,
)

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001

ID_CURRICULO = UUID("00000000-0000-0000-0000-0000000000c1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")

# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
ADAPTER = "backend.infrastructure.persistence.sqlalchemy.repositorio_curriculo"
MODELO = "backend.infrastructure.persistence.sqlalchemy.curriculo"

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
ID_PROJETO = UUID("00000000-0000-0000-0000-0000000000a1")
ID_IDIOMA = UUID("00000000-0000-0000-0000-0000000000a2")
REFERENCIA_PROJETO = ReferenciaCurriculo(ProjetoAcademicoId(ID_PROJETO))
REFERENCIA_IDIOMA = ReferenciaCurriculo(IdiomaId(ID_IDIOMA))

# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
ID_CURRICULO_B = UUID("00000000-0000-0000-0000-0000000000c2")


def linha_projeto() -> SimpleNamespace:
    """Prepara uma linha de seleção simulada equivalente ao projeto de referência.

    O double expõe somente o tipo textual e o UUID, como a linha ORM, sem sessão
    ou tabela. Ele existe para controlar as seleções já persistidas em cada
    cenário.
    """
    return SimpleNamespace(tipo="projeto_academico", item_id=ID_PROJETO)


def linha_idioma() -> SimpleNamespace:
    """Prepara uma linha de seleção simulada equivalente ao idioma de referência.

    O double expõe somente o tipo textual e o UUID, como a linha ORM, sem sessão
    ou tabela. Ele existe para controlar as seleções já persistidas em cada
    cenário.
    """
    return SimpleNamespace(tipo="idioma", item_id=ID_IDIOMA)


def resultado_com(linhas: list) -> MagicMock:
    """Prepara o resultado simulado de uma consulta que devolve as linhas dadas.

    O double responde a ``all`` com a lista informada, como o resultado escalar
    da sessão. Ele existe para controlar o que a consulta de seleção devolve.
    """
    return MagicMock(all=MagicMock(return_value=linhas))


def criar_curriculo() -> Curriculo:
    """Prepara um agregado válido com identidades fixas para isolar os testes.

    Usa UUIDs determinísticos, permitindo comparar a conversão sem aleatoriedade
    ou infraestrutura externa.
    """
    return Curriculo(
        id=CurriculoId(ID_CURRICULO),
        usuario_id=UsuarioId(ID_USUARIO),
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


def criar_registro() -> MagicMock:
    """Prepara um registro ORM simulado equivalente ao agregado de ``criar_curriculo``.

    O double existe somente em memória e expõe os mesmos valores das colunas, de
    modo que a conversão seja testada sem sessão, tabela ou driver.
    """
    return MagicMock(
        id=ID_CURRICULO,
        usuario_id=ID_USUARIO,
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )


# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
def criar_registro_da_listagem(curriculo_id: UUID, titulo: str) -> MagicMock:
    """Prepara um registro ORM simulado do usuário de referência com título e id dados.

    O double existe somente em memória e expõe as colunas que o mapeador lê, sem
    sessão, tabela ou driver. Ele existe para montar várias versões distintas do
    mesmo proprietário nos cenários de listagem.
    """
    return MagicMock(
        id=curriculo_id,
        usuario_id=ID_USUARIO,
        titulo_versao=titulo,
        layout="classico",
        is_public=False,
    )


# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
def linha_da_versao(curriculo_id: UUID, tipo: str, item_id: UUID) -> SimpleNamespace:
    """Prepara uma linha de seleção simulada que informa a versão a que pertence.

    O double expõe a versão, o tipo textual e o UUID do item, como a linha ORM,
    sem sessão ou tabela. Ele existe para que o adapter agrupe as seleções de
    várias versões lidas em uma única consulta.
    """
    return SimpleNamespace(curriculo_id=curriculo_id, tipo=tipo, item_id=item_id)


class ConversaoCurriculoTestCase(unittest.TestCase):
    """Verifica a tradução entre registro ORM e agregado de currículo.

    Usa registros simulados para proteger a separação entre agregado e
    representação persistida sem executar ORM ou I/O.
    """

    def test_reconstroi_agregado_sem_referencias_a_partir_do_registro(self) -> None:
        """Confirma que a leitura transforma colunas em agregado de domínio.

        Compara o agregado reconstruído com o esperado e confirma que as
        referências, ainda não persistidas, permanecem vazias.
        """
        resultado = para_curriculo(criar_registro())

        self.assertEqual(resultado, criar_curriculo())
        self.assertEqual(resultado.referencias, frozenset())

    def test_atualiza_registro_somente_com_dados_editaveis_da_versao(self) -> None:
        """Confirma que apenas título, layout e visibilidade são copiados.

        Edita o agregado, aplica ao registro e verifica que identidade e
        proprietário permanecem inalterados.
        """
        registro = SimpleNamespace(
            id=ID_CURRICULO,
            usuario_id=ID_USUARIO,
            titulo_versao="Antigo",
            layout="antigo",
            is_public=False,
        )
        curriculo = criar_curriculo()
        curriculo.editar_versao("Gestão de Projetos", "moderno", True)

        atualizar_registro(registro, curriculo)  # type: ignore[arg-type]

        self.assertEqual(registro.titulo_versao, "Gestão de Projetos")
        self.assertEqual(registro.layout, "moderno")
        self.assertTrue(registro.is_public)
        self.assertEqual(registro.id, ID_CURRICULO)
        self.assertEqual(registro.usuario_id, ID_USUARIO)


class RepositorioCurriculoSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Exercita a porta assíncrona com sessão substituída.

    Usa mocks aguardáveis para conferir interações, erros e limites de
    transação sem banco, driver conectado ou gerenciador de sessão real.
    """

    def setUp(self) -> None:
        """Cria sessão isolada e adapter por teste usando a especificação real.

        MagicMock transforma métodos async em AsyncMock, permitindo verificar
        awaits e impedir interferência entre cenários.
        """
        self.session = MagicMock(spec=AsyncSession)
        self.session.scalars.return_value = resultado_com([])
        self.repositorio = RepositorioCurriculoSqlAlchemy(self.session)

    async def test_obtem_versao_por_id_e_a_converte_para_agregado(self) -> None:
        """Confirma consulta pela chave primária e mapeamento na leitura.

        Verifica o await de ``get`` com o modelo e o UUID corretos e compara o
        agregado devolvido com o esperado.
        """
        self.session.get.return_value = criar_registro()

        resultado = await self.repositorio.obter_por_id(CurriculoId(ID_CURRICULO))

        self.assertEqual(resultado, criar_curriculo())
        self.session.get.assert_awaited_once_with(CurriculoRegistro, ID_CURRICULO)

    async def test_retorna_ausencia_quando_registro_nao_existe(self) -> None:
        """Confirma que falta de linha não tenta construir agregado inválido.

        Faz a sessão devolver ausência e verifica que o adapter responde ``None``
        sem acionar o mapeador.
        """
        self.session.get.return_value = None

        resultado = await self.repositorio.obter_por_id(CurriculoId(ID_CURRICULO))

        self.assertIsNone(resultado)

    async def test_propaga_falha_na_consulta(self) -> None:
        """Confere que uma consulta falha não se torna ausência de versão.

        Faz a sessão levantar erro e exige que ele chegue intacto ao chamador,
        sem ser confundido com um currículo inexistente.
        """
        self.session.get.side_effect = RuntimeError("falha")

        with self.assertRaises(RuntimeError):
            await self.repositorio.obter_por_id(CurriculoId(ID_CURRICULO))

    async def test_atualiza_somente_colunas_da_versao_e_envia_flush(self) -> None:
        """Confere atualização do registro existente sem criar linha nem commit.

        Verifica a cópia dos campos editáveis, o await de ``flush`` e a ausência
        de ``add``, para proteger que a edição nunca insere uma versão nova.
        """
        registro = criar_registro()
        self.session.get.return_value = registro
        curriculo = criar_curriculo()
        curriculo.editar_versao("Gestão de Projetos", "moderno", True)

        await self.repositorio.atualizar(curriculo)

        self.session.get.assert_awaited_once_with(CurriculoRegistro, ID_CURRICULO)
        self.assertEqual(registro.titulo_versao, "Gestão de Projetos")
        self.assertEqual(registro.layout, "moderno")
        self.assertTrue(registro.is_public)
        self.session.flush.assert_awaited_once_with()
        self.session.add.assert_not_called()

    async def test_rejeita_atualizacao_quando_registro_nao_existe(self) -> None:
        """Confirma que atualizar versão inexistente falha sem enviar alteração.

        Faz a sessão devolver ausência e exige a falha de busca, sem ``flush``
        nem ``add``, para impedir criação implícita durante a atualização.
        """
        self.session.get.return_value = None

        with self.assertRaises(LookupError):
            await self.repositorio.atualizar(criar_curriculo())

        self.session.flush.assert_not_awaited()
        self.session.add.assert_not_called()

    async def test_propaga_falha_no_flush(self) -> None:
        """Confere que falhas de gravação chegam intactas ao chamador.

        Faz o envio da alteração falhar e verifica que o adapter não a mascara
        nem controla transação.
        """
        self.session.get.return_value = criar_registro()
        self.session.flush.side_effect = RuntimeError("falha")

        with self.assertRaises(RuntimeError):
            await self.repositorio.atualizar(criar_curriculo())

    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    async def test_salva_com_add_e_flush_sem_consultar_nem_controlar_transacao(self) -> None:
        """Confere inserção aguardável usando o conversor e o flush da sessão.

        Substitui o conversor para observar o registro entregue a ``add``, e
        verifica ``flush`` aguardado, ausência de consulta e de ``commit``. Ele
        existe para proteger que a criação apenas insere e deixa a transação com
        a composição externa.
        """
        curriculo = criar_curriculo()

        with patch(f"{ADAPTER}.para_registro") as conversor:
            await self.repositorio.salvar(curriculo)

        conversor.assert_called_once_with(curriculo)
        self.session.add.assert_called_once_with(conversor.return_value)
        self.session.flush.assert_awaited_once_with()
        self.session.get.assert_not_awaited()
        self.session.commit.assert_not_awaited()

    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    async def test_salvar_propaga_falha_no_flush(self) -> None:
        """Confere que falhas de inserção, como violação de chave, chegam intactas.

        Faz o envio da inserção falhar e verifica que o adapter não a mascara
        nem traduz o erro, deixando a decisão para a composição externa.
        """
        self.session.flush.side_effect = RuntimeError("falha")

        with patch(f"{ADAPTER}.para_registro"):
            with self.assertRaises(RuntimeError):
                await self.repositorio.salvar(criar_curriculo())

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def test_obtem_versao_com_a_selecao_persistida(self) -> None:
        """Confirma que a leitura reconstrói as referências a partir das linhas.

        Faz a consulta de seleção devolver duas linhas e compara as referências
        do agregado, além de inspecionar a consulta enviada à sessão. Ele existe
        para garantir que o agregado carregado reflita a seleção gravada.
        """
        self.session.get.return_value = criar_registro()
        self.session.scalars.return_value = resultado_com([linha_projeto(), linha_idioma()])

        resultado = await self.repositorio.obter_por_id(CurriculoId(ID_CURRICULO))

        self.assertEqual(resultado.referencias, frozenset({REFERENCIA_PROJETO, REFERENCIA_IDIOMA}))
        self.session.scalars.assert_awaited_once()
        consulta = str(self.session.scalars.call_args.args[0])
        self.assertIn("curriculo_itens", consulta)
        self.assertIn("WHERE", consulta)

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def test_nao_consulta_a_selecao_quando_a_versao_nao_existe(self) -> None:
        """Confirma que a ausência da versão encerra a leitura sem consultar a seleção.

        Faz a sessão devolver ausência e verifica que a consulta de seleção não
        é aguardada. Ele existe para evitar leitura inútil de linhas órfãs.
        """
        self.session.get.return_value = None

        resultado = await self.repositorio.obter_por_id(CurriculoId(ID_CURRICULO))

        self.assertIsNone(resultado)
        self.session.scalars.assert_not_awaited()

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def test_atualizar_insere_somente_os_itens_novos_da_selecao(self) -> None:
        """Confere que apenas a referência nova vira linha, sem remover nada.

        O agregado tem duas referências e uma delas já existe no armazenamento.
        Verifica o registro entregue a ``add``, a ausência de remoção e o flush.
        """
        self.session.get.return_value = criar_registro()
        self.session.scalars.return_value = resultado_com([linha_projeto()])
        curriculo = criar_curriculo()
        curriculo.incluir_referencia(REFERENCIA_PROJETO)
        curriculo.incluir_referencia(REFERENCIA_IDIOMA)

        await self.repositorio.atualizar(curriculo)

        self.session.add.assert_called_once()
        novo = self.session.add.call_args.args[0]
        self.assertIsInstance(novo, CurriculoItemRegistro)
        self.assertEqual((novo.curriculo_id, novo.tipo, novo.item_id), (ID_CURRICULO, "idioma", ID_IDIOMA))
        self.session.delete.assert_not_awaited()
        self.session.flush.assert_awaited_once_with()

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def test_atualizar_remove_somente_os_itens_que_sairam_da_selecao(self) -> None:
        """Confere que apenas a linha ausente do agregado é removida.

        O armazenamento tem duas linhas e o agregado mantém uma. Verifica a
        remoção da linha excedente, a ausência de inserção e o flush.
        """
        self.session.get.return_value = criar_registro()
        mantida, removida = linha_projeto(), linha_idioma()
        self.session.scalars.return_value = resultado_com([mantida, removida])
        curriculo = criar_curriculo()
        curriculo.incluir_referencia(REFERENCIA_PROJETO)

        await self.repositorio.atualizar(curriculo)

        self.session.delete.assert_awaited_once_with(removida)
        self.session.add.assert_not_called()
        self.session.flush.assert_awaited_once_with()

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def test_atualizar_sem_mudar_a_selecao_nao_adiciona_nem_remove_linhas(self) -> None:
        """Confere que editar a versão com a seleção intacta não toca as linhas.

        O agregado reconstruído tem as mesmas referências do armazenamento, como
        após uma edição de título. Verifica que nada é inserido nem removido, o
        que protege a seleção contra apagamento acidental.
        """
        self.session.get.return_value = criar_registro()
        self.session.scalars.return_value = resultado_com([linha_projeto(), linha_idioma()])
        curriculo = criar_curriculo()
        curriculo.incluir_referencia(REFERENCIA_PROJETO)
        curriculo.incluir_referencia(REFERENCIA_IDIOMA)
        curriculo.editar_versao("Gestão de Projetos", "moderno", True)

        await self.repositorio.atualizar(curriculo)

        self.session.add.assert_not_called()
        self.session.delete.assert_not_awaited()
        self.session.flush.assert_awaited_once_with()

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def test_atualizar_propaga_falha_ao_consultar_a_selecao(self) -> None:
        """Confere que falha na consulta da seleção chega intacta e impede o flush.

        Faz a consulta de seleção falhar e verifica que o adapter não a mascara
        nem envia alterações parciais.
        """
        self.session.get.return_value = criar_registro()
        self.session.scalars.side_effect = RuntimeError("falha")

        with self.assertRaises(RuntimeError):
            await self.repositorio.atualizar(criar_curriculo())

        self.session.flush.assert_not_awaited()

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def test_salvar_com_selecao_insere_os_itens_depois_do_flush_da_versao(self) -> None:
        """Confere a ordem entre a inserção da versão e a das linhas de seleção.

        Registra cada ``add`` e cada ``flush`` e exige que a versão seja enviada
        antes das linhas, para que a chave estrangeira desta encontre a versão.
        """
        ordem: list[str] = []

        async def registrar_flush() -> None:
            ordem.append("flush")

        self.session.flush.side_effect = registrar_flush
        self.session.add.side_effect = lambda objeto: ordem.append(type(objeto).__name__)
        curriculo = criar_curriculo()
        curriculo.incluir_referencia(REFERENCIA_PROJETO)

        await self.repositorio.salvar(curriculo)

        self.assertEqual(ordem, ["CurriculoRegistro", "flush", "CurriculoItemRegistro", "flush"])

    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    async def test_lista_as_versoes_do_usuario_com_a_selecao_de_cada_uma(self) -> None:
        """Confirma que cada versão listada volta com as suas referências.

        Faz a primeira consulta devolver duas versões e a segunda devolver
        linhas de seleção de ambas, e compara as referências de cada agregado.
        Ele existe para garantir que a listagem entregue agregados completos, no
        mesmo contrato de ``obter_por_id``.
        """
        self.session.scalars.side_effect = [
            resultado_com(
                [
                    criar_registro_da_listagem(ID_CURRICULO, "Estágio em TI"),
                    criar_registro_da_listagem(ID_CURRICULO_B, "Gestão"),
                ]
            ),
            resultado_com(
                [
                    linha_da_versao(ID_CURRICULO, "projeto_academico", ID_PROJETO),
                    linha_da_versao(ID_CURRICULO_B, "idioma", ID_IDIOMA),
                ]
            ),
        ]

        resultado = await self.repositorio.listar_por_usuario(UsuarioId(ID_USUARIO))

        self.assertIsInstance(resultado, tuple)
        self.assertEqual([curriculo.id.valor for curriculo in resultado], [ID_CURRICULO, ID_CURRICULO_B])
        self.assertEqual(resultado[0].referencias, frozenset({REFERENCIA_PROJETO}))
        self.assertEqual(resultado[1].referencias, frozenset({REFERENCIA_IDIOMA}))
        self.assertEqual(resultado[0].usuario_id, UsuarioId(ID_USUARIO))

    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    async def test_filtra_pelo_usuario_e_carrega_as_selecoes_em_uma_unica_consulta(self) -> None:
        """Confirma o filtro por proprietário e a consulta única das seleções.

        Inspeciona as duas consultas enviadas à sessão: a primeira filtra as
        versões pelo usuário informado e a segunda busca, de uma vez, as
        seleções das versões encontradas. Ele existe para proteger o isolamento
        entre estudantes e a ausência de uma consulta por versão.
        """
        self.session.scalars.side_effect = [
            resultado_com(
                [
                    criar_registro_da_listagem(ID_CURRICULO, "Estágio em TI"),
                    criar_registro_da_listagem(ID_CURRICULO_B, "Gestão"),
                ]
            ),
            resultado_com([]),
        ]

        await self.repositorio.listar_por_usuario(UsuarioId(ID_USUARIO))

        self.assertEqual(self.session.scalars.await_count, 2)
        consulta_versoes, consulta_itens = (chamada.args[0] for chamada in self.session.scalars.await_args_list)
        self.assertIn("curriculos", str(consulta_versoes))
        self.assertIn("WHERE", str(consulta_versoes))
        self.assertIn(ID_USUARIO, consulta_versoes.compile().params.values())
        self.assertIn("curriculo_itens", str(consulta_itens))
        self.assertIn("IN", str(consulta_itens))
        listas = [list(valor) for valor in consulta_itens.compile().params.values() if isinstance(valor, (list, tuple))]
        self.assertIn([ID_CURRICULO, ID_CURRICULO_B], listas)

    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    async def test_versao_sem_selecao_volta_sem_referencias(self) -> None:
        """Confirma que uma versão sem linhas de seleção não recebe referências.

        Faz a segunda consulta devolver somente a seleção de outra versão e
        observa que a versão sem linhas permanece sem referências. Ele existe
        para impedir que a seleção de uma versão vaze para outra.
        """
        self.session.scalars.side_effect = [
            resultado_com(
                [
                    criar_registro_da_listagem(ID_CURRICULO, "Estágio em TI"),
                    criar_registro_da_listagem(ID_CURRICULO_B, "Gestão"),
                ]
            ),
            resultado_com([linha_da_versao(ID_CURRICULO_B, "idioma", ID_IDIOMA)]),
        ]

        resultado = await self.repositorio.listar_por_usuario(UsuarioId(ID_USUARIO))

        self.assertEqual(resultado[0].referencias, frozenset())
        self.assertEqual(resultado[1].referencias, frozenset({REFERENCIA_IDIOMA}))

    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    async def test_usuario_sem_versoes_recebe_tupla_vazia_sem_consultar_as_selecoes(self) -> None:
        """Confirma que a ausência de versões encerra a leitura sem a segunda consulta.

        Faz a primeira consulta devolver uma lista vazia e verifica o resultado e
        que a consulta de seleções não é aguardada. Ele existe para evitar uma
        leitura inútil quando o estudante não tem versões.
        """
        self.session.scalars.side_effect = [resultado_com([])]

        resultado = await self.repositorio.listar_por_usuario(UsuarioId(ID_USUARIO))

        self.assertEqual(resultado, ())
        self.session.scalars.assert_awaited_once()

    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    async def test_listar_propaga_falha_na_consulta_das_versoes(self) -> None:
        """Confere que falha ao ler as versões chega intacta ao chamador.

        Faz a primeira consulta falhar e exige que o erro não seja confundido
        com uma lista vazia. Ele existe para impedir que uma falha de leitura
        pareça um estudante sem versões.
        """
        self.session.scalars.side_effect = RuntimeError("falha")

        with self.assertRaises(RuntimeError):
            await self.repositorio.listar_por_usuario(UsuarioId(ID_USUARIO))

    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    async def test_listar_propaga_falha_na_consulta_das_selecoes(self) -> None:
        """Confere que falha ao ler as seleções chega intacta ao chamador.

        Faz a primeira consulta devolver uma versão e a segunda falhar, e exige
        que o erro chegue sem agregados parciais. Ele existe para impedir que a
        listagem devolva versões sem a seleção por causa de uma falha.
        """
        self.session.scalars.side_effect = [
            resultado_com([criar_registro_da_listagem(ID_CURRICULO, "Estágio em TI")]),
            RuntimeError("falha"),
        ]

        with self.assertRaises(RuntimeError):
            await self.repositorio.listar_por_usuario(UsuarioId(ID_USUARIO))

    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    async def test_listar_nao_escreve_na_sessao(self) -> None:
        """Confirma que listar não adiciona, remove nem envia alterações.

        Executa uma listagem com versões e seleções e observa que a sessão não
        recebe ``add``, ``delete`` nem ``flush``. Ele existe para proteger a
        natureza de consulta da operação.
        """
        self.session.scalars.side_effect = [
            resultado_com([criar_registro_da_listagem(ID_CURRICULO, "Estágio em TI")]),
            resultado_com([linha_da_versao(ID_CURRICULO, "idioma", ID_IDIOMA)]),
        ]

        await self.repositorio.listar_por_usuario(UsuarioId(ID_USUARIO))

        self.session.add.assert_not_called()
        self.session.delete.assert_not_awaited()
        self.session.flush.assert_not_awaited()


# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
class ConversaoParaRegistroTestCase(unittest.TestCase):
    """Verifica a tradução do agregado de currículo para registro ORM.

    Substitui o construtor ORM para inspecionar os argumentos primitivos e
    proteger a separação entre agregado e representação persistida sem executar
    ORM ou I/O.
    """

    def test_converte_valores_sem_modificar_agregado(self) -> None:
        """Confere a conversão comparando argumentos recebidos pelo double.

        Preserva o agregado original e verifica UUIDs, título, layout e
        visibilidade, para evitar a persistência de value objects em vez de
        valores primitivos.
        """
        curriculo = criar_curriculo()

        with patch(f"{MODELO}.CurriculoRegistro") as registro:
            resultado = para_registro(curriculo)

        registro.assert_called_once_with(
            id=ID_CURRICULO,
            usuario_id=ID_USUARIO,
            titulo_versao="Estágio em TI",
            layout="classico",
            is_public=False,
        )
        self.assertIs(resultado, registro.return_value)
        self.assertEqual(curriculo, criar_curriculo())


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
class ConversaoItensTestCase(unittest.TestCase):
    """Verifica a tradução entre referências de domínio e linhas de seleção.

    Usa linhas simuladas e instâncias ORM sem sessão para proteger a separação
    entre agregado e representação persistida, sem executar ORM ou I/O.
    """

    def test_converte_os_seis_tipos_de_ida_e_volta(self) -> None:
        """Confirma o texto de tipo de cada identificador e o caminho de volta.

        Fixa os seis textos esperados e verifica a conversão nos dois sentidos.
        Ele existe para impedir que uma troca de texto invalide dados já
        gravados.
        """
        esperados = {
            "formacao_academica": FormacaoAcademicaId,
            "experiencia_profissional": ExperienciaProfissionalId,
            "projeto_academico": ProjetoAcademicoId,
            "competencia": CompetenciaId,
            "idioma": IdiomaId,
            "documento": DocumentoId,
        }
        for tipo, classe in esperados.items():
            with self.subTest(tipo=tipo):
                referencia = ReferenciaCurriculo(classe(ID_PROJETO))

                self.assertEqual(para_tipo_e_item_id(referencia), (tipo, ID_PROJETO))
                self.assertEqual(para_referencia(tipo, ID_PROJETO), referencia)

    def test_rejeita_tipo_de_item_desconhecido(self) -> None:
        """Confirma que um tipo gravado desconhecido falha de forma explícita.

        Tenta recriar uma referência com texto fora do vocabulário e observa o
        erro. Ele existe para que dado corrompido não vire referência inválida.
        """
        with self.assertRaises(ValueError):
            para_referencia("certificado", ID_PROJETO)

    def test_reconstroi_agregado_com_as_referencias_das_linhas(self) -> None:
        """Confirma que as linhas recebidas viram referências do agregado.

        Converte o registro da versão junto com duas linhas simuladas e compara
        as referências. Ele existe para garantir que a seleção persistida volte
        ao domínio pelo comportamento do próprio agregado.
        """
        resultado = para_curriculo(criar_registro(), [linha_projeto(), linha_idioma()])

        self.assertEqual(resultado.referencias, frozenset({REFERENCIA_PROJETO, REFERENCIA_IDIOMA}))

    def test_converte_referencias_em_linhas_ordenadas_sem_modificar_agregado(self) -> None:
        """Confirma a conversão das referências em linhas determinísticas.

        Inclui duas referências fora de ordem e verifica tipo, UUID, versão e
        a ordenação por tipo, além da ausência de linhas para uma versão sem
        seleção.
        """
        curriculo = criar_curriculo()
        curriculo.incluir_referencia(REFERENCIA_PROJETO)
        curriculo.incluir_referencia(REFERENCIA_IDIOMA)

        linhas = para_registros_itens(curriculo)

        self.assertEqual(
            [(linha.curriculo_id, linha.tipo, linha.item_id) for linha in linhas],
            [(ID_CURRICULO, "idioma", ID_IDIOMA), (ID_CURRICULO, "projeto_academico", ID_PROJETO)],
        )
        self.assertTrue(all(isinstance(linha, CurriculoItemRegistro) for linha in linhas))
        self.assertEqual(curriculo.referencias, frozenset({REFERENCIA_PROJETO, REFERENCIA_IDIOMA}))
        self.assertEqual(para_registros_itens(criar_curriculo()), [])
