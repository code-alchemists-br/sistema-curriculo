"""Testa unitariamente a orquestração do cadastro de certificações."""

from unittest import IsolatedAsyncioTestCase
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
from backend.application.cadastro_certificacao import (
    CadastrarCertificacao,
    CadastrarCertificacaoEntrada,
    CertificacaoJaCadastrada,
)
from backend.domain import (
    Certificacao,
    CertificacaoId,
    RegraDeDominioViolada,
    UsuarioId,
)


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class RepositorioCertificacaoSpy:
    """Substitui a porta de certificação e registra suas interações em memória.

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
        self.chaves_consultadas: list[tuple[UsuarioId, str, str]] = []
        self.certificacoes_salvas: list[Certificacao] = []

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        nome_normalizado: str,
        emissor_normalizado: str,
    ) -> bool:
        """Registra a chave recebida e devolve a existência pré-configurada.

        O método mantém o contrato assíncrono da porta e não executa I/O. Ele
        existe para permitir que o teste observe a chave canônica consultada.
        """
        self.chaves_consultadas.append(
            (usuario_id, nome_normalizado, emissor_normalizado)
        )
        return self.ja_existe

    async def salvar(self, certificacao: Certificacao) -> None:
        """Acumula a certificação entregue pelo caso de uso em memória.

        O método registra a entidade após a decisão de não duplicidade e mantém
        a assinatura da porta. Ele existe para provar que a orquestração só
        solicita persistência no caminho permitido.
        """
        self.certificacoes_salvas.append(certificacao)


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class GeradorCertificacaoIdStub:
    """Entrega uma identidade de certificação determinística para os cenários.

    O stub retorna sempre o mesmo value object, sem gerar UUID aleatório ou acessar
    serviços. Ele existe para isolar o cadastro da estratégia externa de
    identidade e permitir asserções estáveis.
    """

    def __init__(self, identificador: CertificacaoId) -> None:
        """Armazena a identidade que será devolvida pelo contrato da porta.

        O construtor recebe um value object pronto e o conserva imutavelmente.
        Ele existe para configurar cada cenário sem aleatoriedade.
        """
        self._identificador = identificador

    def gerar(self) -> CertificacaoId:
        """Devolve a identidade determinística configurada para o cadastro.

        O método implementa a porta sem gerar dados novos. Ele existe para que
        o caso de uso receba uma identidade válida e testável.
        """
        return self._identificador


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class CadastrarCertificacaoTestCase(IsolatedAsyncioTestCase):
    """Verifica decisões do caso de uso com todas as portas substituídas por doubles.

    A suíte combina spy e stub em memória para exercitar criação, chave
    normalizada, duplicidade e invariantes sem banco, API ou framework. Ela
    existe para proteger a orquestração interna do cadastro.
    """

    async def test_cria_e_salva_certificacao_com_chave_normalizada(self) -> None:
        """Consulta a chave canônica composta e persiste certificação que não existe.

        O cenário usa caixa e espaços variados, executa o caso de uso e compara
        retorno, consulta e spy. Ele existe para verificar que a política de
        duplicidade antecede a persistência e preserva os textos exibíveis.
        """
        usuario_id = UsuarioId(UUID("70000000-0000-0000-0000-000000000001"))
        cert_id = CertificacaoId(UUID("70000000-0000-0000-0000-000000000002"))
        repo = RepositorioCertificacaoSpy(ja_existe=False)
        gerador = GeradorCertificacaoIdStub(cert_id)
        caso_de_uso = CadastrarCertificacao(repositorio=repo, gerador_id=gerador)

        entrada = CadastrarCertificacaoEntrada(
            usuario_id=usuario_id,
            nome="  AWS   Solutions   Architect  ",
            organizacao_emissora="  Amazon   Web   Services  ",
        )

        resultado = await caso_de_uso.executar(entrada)

        self.assertEqual(resultado.id, cert_id)
        self.assertEqual(resultado.usuario_id, usuario_id)
        self.assertEqual(resultado.nome, "AWS   Solutions   Architect")
        self.assertEqual(resultado.organizacao_emissora, "Amazon   Web   Services")

        self.assertEqual(len(repo.chaves_consultadas), 1)
        self.assertEqual(
            repo.chaves_consultadas[0],
            (usuario_id, "aws solutions architect", "amazon web services"),
        )
        self.assertEqual(repo.certificacoes_salvas, [resultado])

    async def test_impede_cadastro_de_certificacao_duplicada(self) -> None:
        """Interrompe o fluxo e levanta erro específico quando a chave já existe.

        O teste configura o spy para indicar duplicidade prévia e valida que a
        exceção CertificacaoJaCadastrada é levantada sem disparar o método salvar.
        Ele existe para proteger a regra de negócio contra duplicatas.
        """
        usuario_id = UsuarioId(UUID("70000000-0000-0000-0000-000000000001"))
        cert_id = CertificacaoId(UUID("70000000-0000-0000-0000-000000000002"))
        repo = RepositorioCertificacaoSpy(ja_existe=True)
        gerador = GeradorCertificacaoIdStub(cert_id)
        caso_de_uso = CadastrarCertificacao(repositorio=repo, gerador_id=gerador)

        entrada = CadastrarCertificacaoEntrada(
            usuario_id=usuario_id,
            nome="Kubernetes Administrator",
            organizacao_emissora="CNCF",
        )

        with self.assertRaises(CertificacaoJaCadastrada):
            await caso_de_uso.executar(entrada)

        self.assertEqual(len(repo.chaves_consultadas), 1)
        self.assertEqual(len(repo.certificacoes_salvas), 0)

    async def test_rejeita_invariante_de_dominio_sem_consultar_ou_salvar(self) -> None:
        """Impede chamadas ao repositório se os dados violam invariantes de entidade.

        O cenário fornece dados vazios na entrada e valida que RegraDeDominioViolada
        é lançada imediatamente na instanciação da entidade, sem consultar nem salvar.
        Ele existe para garantir que o repositório receba apenas entidades válidas.
        """
        usuario_id = UsuarioId(UUID("70000000-0000-0000-0000-000000000001"))
        cert_id = CertificacaoId(UUID("70000000-0000-0000-0000-000000000002"))
        repo = RepositorioCertificacaoSpy(ja_existe=False)
        gerador = GeradorCertificacaoIdStub(cert_id)
        caso_de_uso = CadastrarCertificacao(repositorio=repo, gerador_id=gerador)

        entrada = CadastrarCertificacaoEntrada(
            usuario_id=usuario_id,
            nome="   ",
            organizacao_emissora="Emissor",
        )

        with self.assertRaises(RegraDeDominioViolada):
            await caso_de_uso.executar(entrada)

        self.assertEqual(len(repo.chaves_consultadas), 0)
        self.assertEqual(len(repo.certificacoes_salvas), 0)


ESTUDANTE_A = UsuarioId(UUID("70000000-0000-0000-0000-0000000000a1"))
ESTUDANTE_B = UsuarioId(UUID("70000000-0000-0000-0000-0000000000b2"))


class RepositorioCertificacaoEmMemoria:
    """Substitui a porta de certificação guardando as chaves de cada estudante.

    O double responde à consulta de duplicidade a partir das certificações já
    salvas, comparando proprietário, nome e emissor normalizados, e registra as
    consultas recebidas. Ele existe para provar que a duplicidade é avaliada
    por estudante e pela chave composta, e não por um resultado fixo.
    """

    def __init__(self) -> None:
        """Inicia sem certificações salvas e sem consultas registradas.

        O construtor cria apenas coleções em memória. Ele existe para que cada
        cenário monte seu estado cadastrando certificações pelo próprio caso de
        uso.
        """
        self.certificacoes_salvas: list[Certificacao] = []
        self.chaves_consultadas: list[tuple[UsuarioId, str, str]] = []

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        nome_normalizado: str,
        emissor_normalizado: str,
    ) -> bool:
        """Informa se o estudante já tem certificação com a mesma chave.

        O método registra a consulta e procura, entre as salvas, uma do mesmo
        proprietário com nome e emissor normalizados iguais. Ele existe para
        reproduzir o contrato da porta sem banco.
        """
        self.chaves_consultadas.append((usuario_id, nome_normalizado, emissor_normalizado))
        return any(
            certificacao.usuario_id == usuario_id
            and certificacao.nome_normalizado == nome_normalizado
            and certificacao.organizacao_emissora_normalizada == emissor_normalizado
            for certificacao in self.certificacoes_salvas
        )

    async def salvar(self, certificacao: Certificacao) -> None:
        """Guarda a certificação para consultas de duplicidade posteriores.

        O método apenas acumula a entidade em memória. Ele existe para que
        cadastros seguintes enxerguem as certificações já registradas.
        """
        self.certificacoes_salvas.append(certificacao)


class GeradorCertificacaoIdSequencial:
    """Entrega identidades de certificação distintas e previsíveis.

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

    def gerar(self) -> CertificacaoId:
        """Devolve a próxima identidade da sequência.

        O método incrementa o contador e o usa como inteiro do UUID. Ele existe
        para implementar a porta de geração de identidade.
        """
        self._proximo += 1
        return CertificacaoId(UUID(int=self._proximo))


def _entrada(
    usuario_id: object = ESTUDANTE_A,
    nome: str = "Kubernetes Administrator",
    organizacao_emissora: str = "CNCF",
) -> CadastrarCertificacaoEntrada:
    """Cria a entrada de cadastro com valores padrão válidos.

    A função permite variar dono, nome e emissor em cada cenário. Ela existe
    para manter os testes focados na regra observada.
    """
    return CadastrarCertificacaoEntrada(
        usuario_id=usuario_id,  # type: ignore[arg-type]
        nome=nome,
        organizacao_emissora=organizacao_emissora,
    )


class RegrasDeDominioNoCadastroTestCase(IsolatedAsyncioTestCase):
    """Verifica que cada regra de domínio interrompe o cadastro antes da persistência.

    Os cenários enviam entradas inválidas ao caso de uso real e observam que
    nenhuma consulta de duplicidade nem salvamento acontece. A classe existe
    para garantir que apenas certificações válidas cheguem ao repositório.
    """

    async def test_cada_violacao_de_dominio_impede_consulta_e_salvamento(self) -> None:
        """Rejeita textos inválidos e dono não tipado sem tocar no repositório.

        O teste percorre emissor vazio, textos acima de 200 caracteres,
        caracteres de controle e proprietário ausente ou não tipado, e exige
        ``RegraDeDominioViolada`` com o repositório intocado. Ele existe para
        cobrir no caso de uso as invariantes definidas pela entidade.
        """
        cenarios = {
            "emissor vazio": _entrada(organizacao_emissora="   "),
            "nome acima do limite": _entrada(nome="A" * 201),
            "emissor acima do limite": _entrada(organizacao_emissora="A" * 201),
            "controle no nome": _entrada(nome="Kubernetes\x00Administrator"),
            "controle no emissor": _entrada(organizacao_emissora="CN\x00CF"),
            "dono ausente": _entrada(usuario_id=None),
            "dono não tipado": _entrada(usuario_id=UUID("70000000-0000-0000-0000-0000000000a1")),
        }
        for descricao, entrada in cenarios.items():
            with self.subTest(cenario=descricao):
                repo = RepositorioCertificacaoEmMemoria()
                caso_de_uso = CadastrarCertificacao(
                    repositorio=repo, gerador_id=GeradorCertificacaoIdSequencial()
                )

                with self.assertRaises(RegraDeDominioViolada):
                    await caso_de_uso.executar(entrada)

                self.assertEqual(repo.chaves_consultadas, [])
                self.assertEqual(repo.certificacoes_salvas, [])


class DuplicidadePorEstudanteTestCase(IsolatedAsyncioTestCase):
    """Verifica que a duplicidade considera o dono e a chave composta.

    Os cenários cadastram certificações em sequência com um repositório em
    memória que avalia as chaves salvas. A classe existe para proteger a regra
    de que cada estudante não repete a mesma certificação, sem bloquear outros.
    """

    def setUp(self) -> None:
        """Monta o caso de uso com repositório em memória e IDs sequenciais.

        O setup cria estado novo por teste. Ele existe para evitar dependência
        de ordem entre os cenários.
        """
        self.repo = RepositorioCertificacaoEmMemoria()
        self.caso_de_uso = CadastrarCertificacao(
            repositorio=self.repo, gerador_id=GeradorCertificacaoIdSequencial()
        )

    async def test_mesmo_estudante_com_escrita_diferente_e_duplicata(self) -> None:
        """Bloqueia a mesma certificação do mesmo estudante com caixa e espaços diferentes.

        O primeiro cadastro é salvo e o segundo, com variação de escrita, deve
        levantar ``CertificacaoJaCadastrada`` sem novo salvamento. O teste existe
        para garantir a deduplicação pela chave normalizada.
        """
        await self.caso_de_uso.executar(_entrada())

        with self.assertRaises(CertificacaoJaCadastrada):
            await self.caso_de_uso.executar(
                _entrada(nome="  kubernetes   ADMINISTRATOR ", organizacao_emissora="cncf")
            )

        self.assertEqual(len(self.repo.certificacoes_salvas), 1)

    async def test_outro_estudante_pode_cadastrar_a_mesma_certificacao(self) -> None:
        """Aceita a mesma certificação para um estudante diferente.

        O estudante A cadastra a certificação e o estudante B cadastra a mesma
        com sucesso; a consulta de B usa o próprio dono. O teste existe para que
        a duplicidade nunca bloqueie dados entre estudantes.
        """
        await self.caso_de_uso.executar(_entrada(usuario_id=ESTUDANTE_A))

        certificacao_b = await self.caso_de_uso.executar(_entrada(usuario_id=ESTUDANTE_B))

        self.assertEqual(certificacao_b.usuario_id, ESTUDANTE_B)
        self.assertEqual(len(self.repo.certificacoes_salvas), 2)
        self.assertEqual(self.repo.chaves_consultadas[-1][0], ESTUDANTE_B)

    async def test_mesmo_nome_com_emissor_diferente_nao_e_duplicata(self) -> None:
        """Aceita o mesmo nome quando a organização emissora é outra.

        O estudante cadastra duas certificações com nome igual e emissores
        distintos, e ambas são salvas. O teste existe para fixar que a chave de
        duplicidade combina nome e emissor.
        """
        await self.caso_de_uso.executar(_entrada(organizacao_emissora="CNCF"))

        await self.caso_de_uso.executar(_entrada(organizacao_emissora="Linux Foundation"))

        self.assertEqual(len(self.repo.certificacoes_salvas), 2)
