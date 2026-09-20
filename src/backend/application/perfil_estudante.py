"""Orquestra a edição e a exclusão lógica do perfil do estudante/candidato.

O módulo coordena o agregado ``Usuario`` com portas assíncronas e um relógio
substituível, sem conhecer transporte ou persistência. Ele existe para manter
as intenções de perfil testáveis e separadas de currículos e credenciais.
"""

from dataclasses import dataclass

from backend.application.cadastro_estudante import EmailJaCadastrado
from backend.application.ports import Relogio, RepositorioUsuario
from backend.domain.entities import Usuario
from backend.domain.value_objects import Email, Nome, UsuarioId

# Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001


class PerfilNaoEncontrado(LookupError):
    """Sinaliza que a identidade informada não corresponde a um perfil.

    A falha é produzida antes de qualquer transição ou atualização quando a
    porta devolve ausência. Ela existe para distinguir falta do perfil das
    demais regras sem revelar detalhes de armazenamento.
    """


class PerfilExcluido(ValueError):
    """Sinaliza que um perfil logicamente excluído não aceita edição.

    A falha traduz o estado do agregado antes de consultar conflito de e-mail
    ou atualizar o repositório. Ela existe para impedir a reativação implícita
    de um estudante/candidato removido.
    """


@dataclass(frozen=True, slots=True)
class EditarPerfilEntrada:
    """Agrupa identidade e novos dados válidos para editar um perfil.

    A entrada transporta value objects independentes de HTTP e mantém somente
    nome e e-mail no escopo inicial. Ela existe para dar contrato explícito ao
    caso de uso sem misturar senha, currículo ou itens profissionais.
    """

    usuario_id: UsuarioId
    nome: Nome
    email: Email


@dataclass(frozen=True, slots=True)
class ExcluirPerfilEntrada:
    """Agrupa a identidade do perfil solicitado para exclusão lógica.

    A entrada usa um ``UsuarioId`` já obtido por uma fronteira confiável e não
    recebe data ou política de retenção. Ela existe para limitar o comando à
    intenção do estudante/candidato e deixar o instante sob controle do caso.
    """

    usuario_id: UsuarioId


class EditarPerfil:
    """Edita nome e e-mail de um perfil existente e ainda ativo.

    O caso busca o agregado, rejeita ausência ou exclusão, compara eventual
    proprietário do e-mail e persiste a transição produzida pelo domínio. Ele
    existe para coordenar a edição sem acoplar regras a API ou repositório real.
    """

    def __init__(self, repositorio_usuario: RepositorioUsuario) -> None:
        """Recebe a porta usada para consultar e atualizar perfis.

        O construtor armazena somente a abstração interna que será aguardada
        durante a execução e pode ser substituída por double. Ele existe para
        manter a orquestração independente da infraestrutura.
        """
        self._repositorio_usuario = repositorio_usuario

    async def executar(self, entrada: EditarPerfilEntrada) -> Usuario:
        """Aplica a edição válida e devolve o novo estado persistido do perfil.

        O método localiza o usuário, protege seu estado, aceita o próprio e-mail
        e rejeita o e-mail de outro ID antes de atualizar. Ele existe para
        preservar identidade, credencial e unicidade no fluxo de edição.
        """
        usuario = await self._repositorio_usuario.obter_por_id(entrada.usuario_id)
        if usuario is None:
            raise PerfilNaoEncontrado("Perfil não encontrado.")
        if usuario.excluido:
            raise PerfilExcluido("Perfil excluído não pode ser editado.")

        proprietario_email = await self._repositorio_usuario.obter_por_email(
            entrada.email
        )
        if (
            proprietario_email is not None
            and proprietario_email.id != entrada.usuario_id
        ):
            raise EmailJaCadastrado("Já existe uma conta cadastrada com este e-mail.")

        usuario_editado = usuario.editar_perfil(entrada.nome, entrada.email)
        await self._repositorio_usuario.atualizar(usuario_editado)
        return usuario_editado


class ExcluirPerfil:
    """Marca logicamente como excluído um perfil existente de forma idempotente.

    O caso busca o agregado e, quando ativo, obtém o instante pela porta, aplica
    a transição e solicita atualização; perfis já excluídos retornam intactos.
    Ele existe para bloquear o perfil sem executar purga física nesta camada.
    """

    def __init__(
        self,
        repositorio_usuario: RepositorioUsuario,
        relogio: Relogio,
    ) -> None:
        """Recebe as portas de persistência e tempo necessárias à exclusão.

        O construtor guarda abstrações substituíveis sem consultar recursos
        externos. Ele existe para que a orquestração e o instante aplicado sejam
        completamente determinísticos em testes unitários.
        """
        self._repositorio_usuario = repositorio_usuario
        self._relogio = relogio

    async def executar(self, entrada: ExcluirPerfilEntrada) -> Usuario:
        """Exclui logicamente o perfil ou devolve seu estado excluído existente.

        O método falha para identidade ausente, evita novo efeito quando o
        agregado já está excluído e atualiza apenas a primeira transição. Ele
        existe para tornar repetição segura sem redefinir a data de exclusão.
        """
        usuario = await self._repositorio_usuario.obter_por_id(entrada.usuario_id)
        if usuario is None:
            raise PerfilNaoEncontrado("Perfil não encontrado.")
        if usuario.excluido:
            return usuario

        usuario_excluido = usuario.excluir(self._relogio.agora())
        await self._repositorio_usuario.atualizar(usuario_excluido)
        return usuario_excluido
