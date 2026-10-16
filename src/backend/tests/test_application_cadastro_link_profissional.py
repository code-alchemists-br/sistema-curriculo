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
