"""Orquestra pedidos e confirmações da recuperação de senha."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Protocol

from backend.application.ports import Relogio, RepositorioUsuario
from backend.domain.usuario import Usuario
from backend.domain.value_objects import Email, HashSenha, UsuarioId


@dataclass(frozen=True, slots=True)
class TokenRecuperacaoGerado:
    """Carrega o token de uso único e seu resumo para persistência segura.

    O token em claro é entregue somente ao adapter de e-mail, enquanto o
    resumo é gravado no banco. A estrutura existe para impedir que a camada de
    aplicação escolha o algoritmo criptográfico do token.
    """

    token: str
    resumo: str


@dataclass(frozen=True, slots=True)
class EnvioRecuperacaoSenha:
    """Representa o envio pendente após o token ter sido persistido.

    O adapter usa o e-mail e o token em claro para montar a mensagem fora da
    transação de banco. O DTO existe para separar a entrega externa da regra
    que cria uma solicitação válida.
    """

    email: Email
    token: str


class GeradorTokenRecuperacao(Protocol):
    """Define a geração segura e o resumo irreversível de tokens."""

    def gerar(self) -> TokenRecuperacaoGerado:
        """Gera um token imprevisível e seu resumo persistível.

        A implementação usa fonte criptográfica segura e não persiste o valor
        bruto. Ela existe para manter aleatoriedade e hashing fora do caso de
        uso.
        """

    def resumir(self, token: str) -> str:
        """Resume um token recebido para consulta sem armazená-lo em claro.

        O algoritmo deve coincidir com o resumo produzido por ``gerar``. O
        método existe para consultar a solicitação sem expor a credencial.
        """


class RepositorioTokensRecuperacao(Protocol):
    """Define operações transacionais sobre solicitações de redefinição."""

    async def criar(
        self,
        usuario_id: UsuarioId,
        resumo: str,
        criada_em: datetime,
        expira_em: datetime,
    ) -> bool:
        """Persiste um token quando o intervalo mínimo entre envios foi atendido.

        A implementação invalida solicitações anteriores do usuário na mesma
        transação e devolve ``False`` durante o intervalo de contenção. Ela
        existe para limitar spam e manter apenas um token utilizável.
        """

    async def consumir(self, resumo: str, instante: datetime) -> UsuarioId | None:
        """Consome atomicamente um token ainda válido e devolve seu proprietário.

        A implementação bloqueia a linha, exige expiração futura e ausência de
        consumo anterior. Ela existe para garantir uso único mesmo com pedidos
        concorrentes.
        """


class RevogadorSessoesUsuario(Protocol):
    """Define a revogação de todas as sessões de uma conta após troca de senha."""

    async def revogar_todas(self, usuario_id: UsuarioId, instante: datetime) -> None:
        """Revoga sessões ativas do usuário no instante recebido.

        A implementação atualiza apenas sessões sem revogação prévia. Ela
        existe para impedir que credenciais antigas continuem autenticadas.
        """


class EnviadorLinkRecuperacao(Protocol):
    """Define o envio externo do link sem expor transporte à aplicação."""

    async def enviar(self, email: Email, token: str) -> None:
        """Envia o link temporário sem registrar o token em logs.

        A implementação entrega a mensagem ao provedor configurado. O método
        existe para separar a regra de recuperação do serviço de e-mail.
        """


@dataclass(frozen=True, slots=True)
class EntradaRedefinicaoSenha:
    """Agrupa o token apresentado e a senha já derivada pela fronteira.

    A Application recebe somente ``HashSenha`` e nunca senha em texto claro.
    O DTO existe para manter criptografia e transporte fora da regra de uso.
    """

    token: str
    hash_senha: HashSenha


class SolicitarRecuperacaoSenha:
    """Cria uma solicitação de recuperação sem revelar a existência da conta.

    O caso consulta somente contas ativas, cria token com validade limitada e
    delega a persistência ao repositório. Ele existe para atender pedidos de
    recuperação sem expor informação de cadastro na API.
    """

    DURACAO_TOKEN = timedelta(minutes=15)

    def __init__(
        self,
        usuarios: RepositorioUsuario,
        tokens: RepositorioTokensRecuperacao,
        gerador: GeradorTokenRecuperacao,
        relogio: Relogio,
    ) -> None:
        """Recebe as portas necessárias sem abrir banco, e-mail ou relógio global.

        A injeção permite controlar persistência, aleatoriedade e tempo nos
        testes. Ela existe para manter a regra independente de infraestrutura.
        """
        self._usuarios = usuarios
        self._tokens = tokens
        self._gerador = gerador
        self._relogio = relogio

    async def executar(self, email: Email) -> EnvioRecuperacaoSenha | None:
        """Persiste o token de uma conta ativa e retorna dados ao adapter de e-mail.

        Conta ausente, excluída ou sob intervalo de contenção produz ``None``;
        contas elegíveis recebem token com expiração de quinze minutos. O
        retorno existe para permitir o envio posterior ao commit sem revelar a
        decisão à resposta HTTP.
        """
        usuario = await self._usuarios.obter_por_email(email)
        if usuario is None or usuario.excluido:
            return None

        token = self._gerador.gerar()
        criada_em = self._relogio.agora()
        persistido = await self._tokens.criar(
            usuario.id,
            token.resumo,
            criada_em,
            criada_em + self.DURACAO_TOKEN,
        )
        if not persistido:
            return None
        return EnvioRecuperacaoSenha(usuario.email, token.token)


class RedefinirSenha:
    """Valida token, altera a credencial e revoga sessões em uma transação.

    O caso consome o token, recupera a conta, aplica a transição do agregado e
    revoga sessões ativas. Ele existe para fazer a troca de senha atômica e
    impedir reutilização do link.
    """

    def __init__(
        self,
        usuarios: RepositorioUsuario,
        tokens: RepositorioTokensRecuperacao,
        sessoes: RevogadorSessoesUsuario,
        gerador: GeradorTokenRecuperacao,
        relogio: Relogio,
    ) -> None:
        """Recebe repositórios e serviços que participam da mesma transação.

        As dependências mantêm o caso de uso independente de ORM e tornam
        verificáveis expiração, consumo e revogação. Ele existe para preservar
        consistência entre senha, token e sessões.
        """
        self._usuarios = usuarios
        self._tokens = tokens
        self._sessoes = sessoes
        self._gerador = gerador
        self._relogio = relogio

    async def executar(self, entrada: EntradaRedefinicaoSenha) -> bool:
        """Aplica a nova senha somente se o token puder ser consumido.

        Resume o token, consome sua linha válida, atualiza o aggregate root e
        revoga sessões no mesmo contexto transacional. Devolve ``False`` para
        tokens inválidos ou contas ausentes/excluídas, sem indicar qual falhou.
        """
        instante = self._relogio.agora()
        usuario_id = await self._tokens.consumir(
            self._gerador.resumir(entrada.token), instante
        )
        if usuario_id is None:
            return False

        usuario: Usuario | None = await self._usuarios.obter_por_id(usuario_id)
        if usuario is None or usuario.excluido:
            return False

        await self._usuarios.atualizar(usuario.redefinir_senha(entrada.hash_senha))
        await self._sessoes.revogar_todas(usuario_id, instante)
        return True
