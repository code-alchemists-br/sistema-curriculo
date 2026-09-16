"""Testa unitariamente o caso de uso de cadastro de estudante."""

import unittest
from uuid import uuid4

from backend.application import (
    CadastrarEstudante,
    CadastrarEstudanteEntrada,
    EmailJaCadastrado,
)
from backend.domain import Email, HashSenha, Nome, Usuario, UsuarioId


# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260916-cadastro-acesso-estudante-v002.md#v002
class RepositorioUsuarioSpy:
    """Substitui assincronamente a porta e registra interações do caso de uso.

    O double responde por coroutines a uma coleção em memória e guarda agregados
    enviados a ``salvar``. Ele existe para testar o fluxo aguardável sem usar
    adapter real, banco ou filesystem.
    """

    def __init__(self, emails_existentes: set[Email] | None = None) -> None:
        """Prepara o double com e-mails existentes e nenhum usuário salvo.

        O construtor copia a coleção opcional e inicia o histórico de salvamentos
        vazio, isolando cada teste. Ele existe para permitir cenários válidos e
        duplicados com o mesmo contrato da porta interna.
        """
        self._emails_existentes = emails_existentes or set()
        self.usuarios_salvos: list[Usuario] = []

    async def existe_por_email(self, email: Email) -> bool:
        """Informa por coroutine se o e-mail aparece no estado simulado.

        O método compara value objects em memória e devolve o booleano do
        contrato aguardável. Ele existe para controlar duplicidade sem consultar
        armazenamento externo.
        """
        return email in self._emails_existentes

    async def salvar(self, usuario: Usuario) -> None:
        """Registra por coroutine o agregado solicitado para persistência.

        O método adiciona o usuário à lista de observação sem executar I/O. Ele
        existe para que os testes confirmem se o fluxo solicitou ou evitou o
        salvamento conforme a regra de e-mail duplicado.
        """
        self.usuarios_salvos.append(usuario)


# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
class GeradorUsuarioIdStub:
    """Substitui a geração de ID por uma identidade determinística de teste.

    O double retorna sempre o ID recebido e conta suas invocações, sem depender
    de fonte aleatória ou infraestrutura. Ele existe para permitir verificar que
    o cadastro gera identidade somente no caminho não duplicado.
    """

    def __init__(self, usuario_id: UsuarioId) -> None:
        """Armazena a identidade que o double deverá devolver.

        O construtor recebe um value object pronto e zera o contador de chamadas.
        Ele existe para que cada teste controle completamente a identidade usada
        ao construir o agregado ``Usuario``.
        """
        self._usuario_id = usuario_id
        self.chamadas = 0

    def gerar(self) -> UsuarioId:
        """Devolve a identidade preparada e registra uma chamada de geração.

        O método incrementa o contador antes de retornar o mesmo value object.
        Ele existe para tornar observável a decisão do caso de uso de gerar ou
        não uma identidade dependendo da existência do e-mail.
        """
        self.chamadas += 1
        return self._usuario_id


# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260916-cadastro-acesso-estudante-v002.md#v002
class CadastrarEstudanteTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a orquestração de cadastro sem framework ou persistência real.

    A classe usa os doubles locais de repositório e gerador de ID para exercitar
    o caso de uso em memória. Ela existe para proteger a criação de usuário e a
    interrupção de duplicidade como comportamentos observáveis da Application.
    """

    async def test_cadastra_usuario_e_solicita_salvamento_quando_email_e_novo(self) -> None:
        """Confirma a construção e o salvamento de um usuário com e-mail inédito.

        O teste fornece entrada válida e doubles controlados, então compara o
        agregado retornado com o usuário observado pelo repositório. Ele existe
        para assegurar que UC01 coordene domínio e porta sem usar infraestrutura.
        """
        usuario_id = UsuarioId(uuid4())
        repositorio = RepositorioUsuarioSpy()
        gerador = GeradorUsuarioIdStub(usuario_id)
        caso_de_uso = CadastrarEstudante(repositorio, gerador)
        entrada = _criar_entrada()

        usuario = await caso_de_uso.executar(entrada)

        self.assertEqual(usuario.id, usuario_id)
        self.assertEqual(usuario.nome, entrada.nome)
        self.assertEqual(usuario.email, entrada.email)
        self.assertEqual(repositorio.usuarios_salvos, [usuario])
        self.assertEqual(gerador.chamadas, 1)

    async def test_rejeita_email_ja_cadastrado_sem_gerar_id_ou_salvar(self) -> None:
        """Confirma que duplicidade interrompe o fluxo antes de qualquer salvamento.

        O teste configura o repositório para reconhecer o e-mail da entrada e
        observa a falha de negócio e os doubles sem efeitos posteriores. Ele
        existe para preservar a regra de unicidade no ponto de orquestração.
        """
        entrada = _criar_entrada()
        repositorio = RepositorioUsuarioSpy({entrada.email})
        gerador = GeradorUsuarioIdStub(UsuarioId(uuid4()))
        caso_de_uso = CadastrarEstudante(repositorio, gerador)

        with self.assertRaises(EmailJaCadastrado):
            await caso_de_uso.executar(entrada)

        self.assertEqual(repositorio.usuarios_salvos, [])
        self.assertEqual(gerador.chamadas, 0)


# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
def _criar_entrada() -> CadastrarEstudanteEntrada:
    """Cria uma entrada válida para manter os testes focados na orquestração.

    A função constrói value objects com dados estáveis e fornece um hash já
    derivado, sem processar senha. Ela existe para evitar repetição de preparação
    e reafirmar que a camada Application não recebe credencial em texto claro.
    """
    return CadastrarEstudanteEntrada(
        nome=Nome("Ana Silva"),
        email=Email("ana.silva@fatec.sp.gov.br"),
        hash_senha=HashSenha("hash-ja-derivado"),
    )
