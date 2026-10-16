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
