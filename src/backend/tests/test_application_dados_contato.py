"""Testa unitariamente o caso de uso de atualização de dados de contato."""

from datetime import datetime, timezone
import unittest
from uuid import uuid4

from backend.application import (
    AtualizarDadosContato,
    AtualizarDadosContatoEntrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)
from backend.domain import (
    DadosContato,
    Email,
    Endereco,
    HashSenha,
    Nome,
    Telefone,
    Usuario,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001


class RepositorioUsuarioSpy:
    """Substitui a porta de usuário e registra atualizações solicitadas.

    O double consulta agregados em memória por ID e acumula os novos estados
    recebidos. Ele existe para testar a orquestração assíncrona sem ORM,
    banco, rede ou adapter produtivo.
    """

    def __init__(self, usuarios: list[Usuario] | None = None) -> None:
        """Prepara um índice em memória e um histórico vazio de atualizações.

        O construtor copia os usuários fornecidos em um dicionário por
        identidade. Ele existe para controlar ausência e estado excluído em
        cada cenário testado.
        """
        self._por_id = {usuario.id: usuario for usuario in (usuarios or [])}
        self.usuarios_atualizados: list[Usuario] = []

    async def obter_por_id(self, usuario_id: UsuarioId) -> Usuario | None:
        """Devolve por coroutine o usuário associado ao ID informado.

        O método consulta somente o dicionário controlado pelo teste e não faz
        I/O. Ele existe para simular a leitura aguardável exigida pelo caso.
        """
        return self._por_id.get(usuario_id)

    async def atualizar(self, usuario: Usuario) -> None:
        """Registra por coroutine o novo estado solicitado pela Application.

        O método acumula o agregado sem persistir ou iniciar transação. Ele
        existe para tornar observável se e quando houve efeito de atualização.
        """
        self.usuarios_atualizados.append(usuario)


class AtualizarDadosContatoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica decisões de fluxo do caso de uso ``AtualizarDadosContato``.

    A classe substitui a porta de usuário por estado em memória e observa
    falhas e atualizações. Ela existe para testar a unidade Application sem
    qualquer adapter, framework ou infraestrutura.
    """

    async def test_atualiza_dados_contato_de_perfil_ativo(self) -> None:
        """Confirma a atualização e a persistência quando o perfil está ativo.

        O teste fornece um perfil ativo e dados de contato válidos, então
        compara o estado retornado e o efeito observado no double.
        """
        usuario = _criar_usuario()
        repositorio = RepositorioUsuarioSpy([usuario])
        dados_contato = DadosContato(
            endereco=Endereco("Rua Um, 100"),
            telefones=(Telefone("11999990000"),),
            linkedin="https://linkedin.com/in/ana",
        )
        entrada = AtualizarDadosContatoEntrada(usuario.id, dados_contato)

        resultado = await AtualizarDadosContato(repositorio).executar(entrada)

        self.assertEqual(resultado.dados_contato, dados_contato)
        self.assertEqual(resultado.id, usuario.id)
        self.assertEqual(resultado.hash_senha, usuario.hash_senha)
        self.assertEqual(repositorio.usuarios_atualizados, [resultado])

    async def test_rejeita_perfil_inexistente_sem_atualizacao(self) -> None:
        """Confirma que ausência interrompe o fluxo antes de qualquer efeito.

        O teste usa repositório vazio e observa a falha e o histórico sem
        efeito. Ele existe para impedir criação implícita de contato.
        """
        repositorio = RepositorioUsuarioSpy()
        dados_contato = DadosContato(
            endereco=Endereco("Rua Um, 100"),
            telefones=(Telefone("11999990000"),),
        )
        entrada = AtualizarDadosContatoEntrada(UsuarioId(uuid4()), dados_contato)

        with self.assertRaises(PerfilNaoEncontrado):
            await AtualizarDadosContato(repositorio).executar(entrada)

        self.assertEqual(repositorio.usuarios_atualizados, [])

    async def test_rejeita_atualizacao_de_perfil_excluido(self) -> None:
        """Confirma que um perfil excluído não recebe novos dados de contato.

        O teste fornece agregado já excluído e observa a falha antes de
        efeitos. Ele existe para preservar a transição de ciclo de vida do
        perfil também para dados de contato.
        """
        usuario = _criar_usuario().excluir(datetime(2026, 9, 20, tzinfo=timezone.utc))
        repositorio = RepositorioUsuarioSpy([usuario])
        dados_contato = DadosContato(
            endereco=Endereco("Rua Um, 100"),
            telefones=(Telefone("11999990000"),),
        )
        entrada = AtualizarDadosContatoEntrada(usuario.id, dados_contato)

        with self.assertRaises(PerfilExcluido):
            await AtualizarDadosContato(repositorio).executar(entrada)

        self.assertEqual(repositorio.usuarios_atualizados, [])


def _criar_usuario() -> Usuario:
    """Cria perfil ativo com dados válidos para os casos de uso.

    A função monta um agregado sem acessar gerador, banco ou relógio. Ela
    existe para reduzir repetição mantendo cada teste focado na decisão de
    fluxo do caso de uso.
    """
    return Usuario(
        id=UsuarioId(uuid4()),
        nome=Nome("Ana Silva"),
        email=Email("ana@example.com"),
        hash_senha=HashSenha("hash-ja-derivado"),
    )