"""Testa unitariamente a orquestração do cadastro de links profissionais."""

from unittest import IsolatedAsyncioTestCase
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.application.cadastro_link_profissional import (
    CadastrarLinkProfissional,
    CadastrarLinkProfissionalEntrada,
    LinkProfissionalJaCadastrado,
)
from backend.domain import LinkProfissional, LinkProfissionalId, UsuarioId
from backend.domain.exceptions import RegraDeDominioViolada

ID_LINK = UUID("00000000-0000-0000-0000-0000000000a1")
ID_USUARIO = UUID("00000000-0000-0000-0000-000000000001")


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class RepositorioLinkProfissionalSpy:
    """Substitui a porta de link profissional e registra suas interações em memória.

    O double devolve a existência configurada para uma chave e acumula entidades
    salvas, sem usar adapter ou banco. Ele existe para tornar observável a
    sequência do caso de uso em testes unitários determinísticos.
    """

    def __init__(self, ja_existe: bool = False) -> None:
        """Inicializa o resultado de consulta e o histórico de persistência.

        O construtor recebe a resposta que simulará para a chave de duplicidade
        e cria coleções locais de observação. Ele existe para variar somente o
        estado relevante de cada cenário sem infraestrutura externa.
        """
        self.ja_existe = ja_existe
        self.chaves_consultadas: list[tuple[UsuarioId, str]] = []
        self.links_salvos: list[LinkProfissional] = []

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        url_normalizada: str,
    ) -> bool:
        """Registra a chave recebida e devolve a existência pré-configurada.

        O método mantém o contrato assíncrono da porta e não executa I/O. Ele
        existe para permitir que o teste observe a chave canônica consultada.
        """
        self.chaves_consultadas.append((usuario_id, url_normalizada))
        return self.ja_existe

    async def salvar(self, link: LinkProfissional) -> None:
        """Acumula o link entregue pelo caso de uso em memória.

        O método registra a entidade após a decisão de não duplicidade e mantém
        a assinatura da porta. Ele existe para provar que a orquestração só
        solicita persistência no caminho permitido.
        """
        self.links_salvos.append(link)


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class GeradorLinkProfissionalIdStub:
    """Entrega uma identidade de link profissional determinística para os cenários.

    O stub retorna sempre o mesmo value object, sem gerar UUID ou acessar
    serviços. Ele existe para isolar o cadastro da estratégia externa de
    identidade e permitir asserções estáveis.
    """

    def __init__(self, identificador: LinkProfissionalId) -> None:
        """Armazena a identidade que será devolvida pelo contrato da porta.

        O construtor recebe um value object pronto e o conserva imutavelmente.
        Ele existe para configurar cada cenário sem aleatoriedade.
        """
        self._identificador = identificador

    def gerar(self) -> LinkProfissionalId:
        """Devolve a identidade determinística configurada para o cadastro.

        O método implementa a porta sem gerar dados novos. Ele existe para que
        o caso de uso receba uma identidade válida e testável.
        """
        return self._identificador


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class CadastrarLinkProfissionalTestCase(IsolatedAsyncioTestCase):
    """Verifica decisões do caso de uso com todas as portas substituídas.

    A suíte combina spy e stub em memória para exercitar criação, chave
    normalizada, duplicidade e invariantes sem banco, API ou framework. Ela
    existe para proteger a orquestração interna do cadastro.
    """

    async def test_cria_e_salva_link_profissional_com_chave_normalizada(self) -> None:
        """Cria e salva link válido consultando a URL normalizada antes de salvar.

        O cenário exercita o fluxo completo de sucesso, inspeciona a consulta de
        duplicidade com a chave canônica e certifica que o link foi persistido.
        Ele existe para provar o caminho principal do caso de uso.
        """
        repositorio = RepositorioLinkProfissionalSpy(ja_existe=False)
        gerador = GeradorLinkProfissionalIdStub(LinkProfissionalId(ID_LINK))
        caso_de_uso = CadastrarLinkProfissional(repositorio, gerador)

        entrada = CadastrarLinkProfissionalEntrada(
            usuario_id=UsuarioId(ID_USUARIO),
            rotulo="  GitHub Perfil  ",
            url="  HTTPS://GITHUB.COM/usuario/  ",
        )

        link_criado = await caso_de_uso.executar(entrada)

        self.assertEqual(link_criado.id.valor, ID_LINK)
        self.assertEqual(link_criado.usuario_id.valor, ID_USUARIO)
        self.assertEqual(link_criado.rotulo, "GitHub Perfil")
        self.assertEqual(link_criado.url, "https://GITHUB.COM/usuario/")
        self.assertEqual(link_criado.url_normalizada, "https://github.com/usuario")

        self.assertEqual(
            repositorio.chaves_consultadas,
            [(UsuarioId(ID_USUARIO), "https://github.com/usuario")],
        )
        self.assertEqual(repositorio.links_salvos, [link_criado])

    async def test_interrompe_quando_link_ja_cadastrado_para_usuario(self) -> None:
        """Lança LinkProfissionalJaCadastrado e não persiste quando já existe o link.

        O cenário configura o spy para indicar duplicidade e valida o lançamento
        da exceção sem que salvar seja invocado. Ele existe para garantir que
        links duplicados não sejam aceitos.
        """
        repositorio = RepositorioLinkProfissionalSpy(ja_existe=True)
        gerador = GeradorLinkProfissionalIdStub(LinkProfissionalId(ID_LINK))
        caso_de_uso = CadastrarLinkProfissional(repositorio, gerador)

        entrada = CadastrarLinkProfissionalEntrada(
            usuario_id=UsuarioId(ID_USUARIO),
            rotulo="Meu GitHub",
            url="https://github.com/usuario",
        )

        with self.assertRaises(LinkProfissionalJaCadastrado):
            await caso_de_uso.executar(entrada)

        self.assertEqual(len(repositorio.chaves_consultadas), 1)
        self.assertEqual(len(repositorio.links_salvos), 0)

    async def test_rejeita_rotulo_invalido_antes_de_consultar_ou_salvar(self) -> None:
        """Rejeita rótulo inválido antes de acessar o repositório.

        O cenário passa rótulo vazio e certifica que o erro de domínio é lançado
        na construção da entidade sem qualquer interação com as portas.
        Ele existe para blindar as portas contra dados inconsistentes.
        """
        repositorio = RepositorioLinkProfissionalSpy()
        gerador = GeradorLinkProfissionalIdStub(LinkProfissionalId(ID_LINK))
        caso_de_uso = CadastrarLinkProfissional(repositorio, gerador)

        entrada = CadastrarLinkProfissionalEntrada(
            usuario_id=UsuarioId(ID_USUARIO),
            rotulo="   ",
            url="https://github.com/usuario",
        )

        with self.assertRaises(RegraDeDominioViolada):
            await caso_de_uso.executar(entrada)

        self.assertEqual(repositorio.chaves_consultadas, [])
        self.assertEqual(repositorio.links_salvos, [])

    async def test_rejeita_url_invalida_antes_de_consultar_ou_salvar(self) -> None:
        """Rejeita URL com esquema proibido antes de acessar o repositório.

        O cenário passa URL com esquema javascript e verifica que a regra é
        disparada imediatamente sem consultar duplicidade.
        Ele existe para assegurar fail-fast com segurança.
        """
        repositorio = RepositorioLinkProfissionalSpy()
        gerador = GeradorLinkProfissionalIdStub(LinkProfissionalId(ID_LINK))
        caso_de_uso = CadastrarLinkProfissional(repositorio, gerador)

        entrada = CadastrarLinkProfissionalEntrada(
            usuario_id=UsuarioId(ID_USUARIO),
            rotulo="Script",
            url="javascript:alert(1)",
        )

        with self.assertRaises(RegraDeDominioViolada):
            await caso_de_uso.executar(entrada)

        self.assertEqual(repositorio.chaves_consultadas, [])
        self.assertEqual(repositorio.links_salvos, [])


ESTUDANTE_A = UsuarioId(UUID("00000000-0000-0000-0000-0000000000a5"))
ESTUDANTE_B = UsuarioId(UUID("00000000-0000-0000-0000-0000000000b5"))


class RepositorioLinkProfissionalEmMemoria:
    """Substitui a porta de link profissional guardando os links de cada estudante.

    O double responde à consulta de duplicidade a partir dos links já salvos,
    comparando proprietário e URL normalizada, e registra as consultas
    recebidas. Ele existe para provar que a duplicidade é avaliada por
    estudante e pela URL canônica, e não por um resultado fixo.
    """

    def __init__(self) -> None:
        """Inicia sem links salvos e sem consultas registradas.

        O construtor cria apenas coleções em memória. Ele existe para que cada
        cenário monte seu estado cadastrando links pelo próprio caso de uso.
        """
        self.links_salvos: list[LinkProfissional] = []
        self.chaves_consultadas: list[tuple[UsuarioId, str]] = []

    async def existe_por_chave_de_duplicidade(
        self, usuario_id: UsuarioId, url_normalizada: str
    ) -> bool:
        """Informa se o estudante já tem link com a mesma URL normalizada.

        O método registra a consulta e procura, entre os salvos, um do mesmo
        proprietário com a mesma chave. Ele existe para reproduzir o contrato da
        porta sem banco.
        """
        self.chaves_consultadas.append((usuario_id, url_normalizada))
        return any(
            link.usuario_id == usuario_id and link.url_normalizada == url_normalizada
            for link in self.links_salvos
        )

    async def salvar(self, link: LinkProfissional) -> None:
        """Guarda o link para consultas de duplicidade posteriores.

        O método apenas acumula a entidade em memória. Ele existe para que
        cadastros seguintes enxerguem os links já registrados.
        """
        self.links_salvos.append(link)


class GeradorLinkProfissionalIdSequencial:
    """Entrega identidades de link distintas e previsíveis.

    O double incrementa um contador a cada chamada e o converte em UUID. Ele
    existe para que vários cadastros no mesmo cenário tenham IDs diferentes sem
    aleatoriedade.
    """

    def __init__(self) -> None:
        """Inicia o contador de identidades geradas.

        O construtor não acessa serviços externos. Ele existe para manter o
        cenário determinístico.
        """
        self._proximo = 0

    def gerar(self) -> LinkProfissionalId:
        """Devolve a próxima identidade da sequência.

        O método incrementa o contador e o usa como inteiro do UUID. Ele existe
        para implementar a porta de geração de identidade.
        """
        self._proximo += 1
        return LinkProfissionalId(UUID(int=self._proximo))


def _entrada(
    usuario_id: object = ESTUDANTE_A,
    rotulo: str = "GitHub",
    url: str = "https://github.com/usuario",
) -> CadastrarLinkProfissionalEntrada:
    """Cria a entrada de cadastro com valores padrão válidos.

    A função permite variar dono, rótulo e URL em cada cenário. Ela existe para
    manter os testes focados na regra observada.
    """
    return CadastrarLinkProfissionalEntrada(
        usuario_id=usuario_id,  # type: ignore[arg-type]
        rotulo=rotulo,
        url=url,
    )


class DuplicidadeLinkPorUsuarioTestCase(IsolatedAsyncioTestCase):
    """Verifica que a duplicidade de link considera o dono e a URL canônica.

    Os cenários cadastram links em sequência com um repositório em memória que
    avalia as chaves salvas. A classe existe para proteger a regra de que cada
    estudante não repete o mesmo destino, sem bloquear outros estudantes.
    """

    def setUp(self) -> None:
        """Monta o caso de uso com repositório em memória e IDs sequenciais.

        O setup cria estado novo por teste. Ele existe para evitar dependência
        de ordem entre os cenários.
        """
        self.repo = RepositorioLinkProfissionalEmMemoria()
        self.caso_de_uso = CadastrarLinkProfissional(
            repositorio=self.repo, gerador_id=GeradorLinkProfissionalIdSequencial()
        )

    async def test_mesma_url_escrita_diferente_e_duplicata_do_mesmo_estudante(self) -> None:
        """Bloqueia a mesma URL com esquema, host e barra final escritos diferente.

        O primeiro cadastro é salvo e as variações de escrita devem levantar
        ``LinkProfissionalJaCadastrado`` sem novo salvamento. O teste existe
        para garantir a deduplicação pela URL normalizada.
        """
        await self.caso_de_uso.executar(_entrada(url="https://github.com/usuario"))

        for variacao in (
            "HTTPS://GITHUB.COM/usuario",
            "https://github.com/usuario/",
            "  https://GitHub.com/usuario/  ",
        ):
            with self.subTest(url=variacao):
                with self.assertRaises(LinkProfissionalJaCadastrado):
                    await self.caso_de_uso.executar(_entrada(url=variacao))

        self.assertEqual(len(self.repo.links_salvos), 1)

    async def test_mesma_url_com_rotulo_diferente_e_duplicata(self) -> None:
        """Considera duplicata a mesma URL mesmo com outro rótulo.

        O estudante cadastra a URL com um rótulo e tenta repeti-la com outro. O
        teste existe para fixar que o rótulo não faz parte da chave.
        """
        await self.caso_de_uso.executar(_entrada(rotulo="GitHub"))

        with self.assertRaises(LinkProfissionalJaCadastrado):
            await self.caso_de_uso.executar(_entrada(rotulo="Meus repositórios"))

        self.assertEqual(len(self.repo.links_salvos), 1)

    async def test_outro_estudante_pode_cadastrar_a_mesma_url(self) -> None:
        """Aceita a mesma URL para um estudante diferente.

        O estudante A cadastra a URL e o estudante B cadastra a mesma com
        sucesso; a consulta de B usa o próprio dono. O teste existe para que a
        duplicidade nunca bloqueie dados entre estudantes.
        """
        await self.caso_de_uso.executar(_entrada(usuario_id=ESTUDANTE_A))

        link_b = await self.caso_de_uso.executar(_entrada(usuario_id=ESTUDANTE_B))

        self.assertEqual(link_b.usuario_id, ESTUDANTE_B)
        self.assertEqual(len(self.repo.links_salvos), 2)
        self.assertEqual(self.repo.chaves_consultadas[-1][0], ESTUDANTE_B)

    async def test_mesmo_estudante_com_outra_url_e_aceito(self) -> None:
        """Aceita um segundo link do mesmo estudante com destino diferente.

        O estudante cadastra duas URLs distintas e ambas são salvas. O teste
        existe para que a regra bloqueie só repetições, não links novos.
        """
        await self.caso_de_uso.executar(_entrada(url="https://github.com/usuario"))

        await self.caso_de_uso.executar(_entrada(url="https://linkedin.com/in/usuario"))

        self.assertEqual(len(self.repo.links_salvos), 2)


class RegrasDeDominioNoCadastroDeLinkTestCase(IsolatedAsyncioTestCase):
    """Verifica que as regras de domínio interrompem o cadastro antes do repositório.

    Os cenários enviam URLs e donos inválidos ao caso de uso real e observam
    que nenhuma consulta nem salvamento acontece. A classe existe para garantir
    que apenas links válidos e seguros cheguem à persistência.
    """

    async def test_cada_violacao_impede_consulta_e_salvamento(self) -> None:
        """Rejeita URL insegura ou sem destino e dono não tipado sem tocar no repositório.

        O teste percorre credenciais na URL, espaço, host ausente, porta
        inválida e proprietário ausente ou não tipado. Ele existe para cobrir no
        caso de uso as invariantes definidas pela entidade.
        """
        cenarios = {
            "credenciais na URL": _entrada(url="https://user:senha@site.com"),
            "espaço na URL": _entrada(url="https://exemplo.com/a b"),
            "host ausente": _entrada(url="http://:80"),
            "porta inválida": _entrada(url="https://exemplo.com:70000"),
            "dono ausente": _entrada(usuario_id=None),
            "dono não tipado": _entrada(usuario_id=UUID("00000000-0000-0000-0000-0000000000a5")),
        }
        for descricao, entrada in cenarios.items():
            with self.subTest(cenario=descricao):
                repo = RepositorioLinkProfissionalEmMemoria()
                caso_de_uso = CadastrarLinkProfissional(
                    repositorio=repo, gerador_id=GeradorLinkProfissionalIdSequencial()
                )

                with self.assertRaises(RegraDeDominioViolada):
                    await caso_de_uso.executar(entrada)

                self.assertEqual(repo.chaves_consultadas, [])
                self.assertEqual(repo.links_salvos, [])
