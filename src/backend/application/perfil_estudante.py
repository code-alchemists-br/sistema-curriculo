"""Orquestra operações de perfil do estudante/candidato e suas formações.

O módulo coordena o agregado ``Usuario`` e entidades reutilizáveis de perfil
com portas assíncronas, sem conhecer transporte ou persistência. Ele existe para
manter as intenções de perfil testáveis e separadas de currículos e credenciais.
"""

from dataclasses import dataclass

from backend.application.cadastro_estudante import EmailJaCadastrado
# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
from backend.application.ports import (
    GeradorFormacaoAcademicaId,
    Relogio,
    RepositorioFormacaoAcademica,
    RepositorioUsuario,
)
# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.usuario import Usuario
from backend.domain.value_objects import Email, Nome, UsuarioId

# Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
from backend.domain.itens_perfil import FormacaoAcademica
from backend.domain.value_objects import Periodo


class PerfilNaoEncontrado(LookupError):
    """Sinaliza que a identidade informada não corresponde a um perfil.

    A falha é produzida antes de qualquer transição ou atualização quando a
    porta devolve ausência. Ela existe para distinguir falta do perfil das
    demais regras sem revelar detalhes de armazenamento.
    """


# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
class PerfilExcluido(ValueError):
    """Sinaliza que um perfil logicamente excluído não aceita operações ativas.

    A falha traduz o estado do agregado antes de editar seus dados ou cadastrar
    uma formação. Ela existe para impedir que operações de perfil reativem ou
    ampliem implicitamente um estudante/candidato removido.
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


# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
@dataclass(frozen=True, slots=True)
class CadastrarFormacaoAcademicaEntrada:
    """Agrupa os dados de domínio para cadastrar uma formação de um perfil.

    A entrada transporta o proprietário tipado, textos já recebidos por uma
    fronteira externa e um ``Periodo`` validado, sem incluir HTTP ou ORM. Ela
    existe para dar contrato explícito ao caso de uso e preservar as invariantes
    locais da formação no domínio.
    """

    usuario_id: UsuarioId
    instituicao: str
    curso: str
    nivel: str
    periodo: Periodo
    status: str


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


# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
class CadastrarFormacaoAcademica:
    """Cria e solicita o salvamento de uma formação para um perfil ativo.

    O caso consulta o proprietário por porta, rejeita ausência ou exclusão,
    gera uma identidade tipada e constrói a entidade antes de delegar o
    salvamento à porta específica. Ele existe para coordenar a associação entre
    perfil e formação sem acoplar domínio ou Application à persistência.
    """

    def __init__(
        self,
        repositorio_usuario: RepositorioUsuario,
        repositorio_formacao: RepositorioFormacaoAcademica,
        gerador_formacao_id: GeradorFormacaoAcademicaId,
    ) -> None:
        """Recebe as portas necessárias à validação e ao cadastro da formação.

        O construtor armazena abstrações para consultar o perfil, persistir a
        entidade e gerar sua identidade, sem executar I/O. Ele existe para que
        a orquestração seja injetável e determinística em testes unitários.
        """
        self._repositorio_usuario = repositorio_usuario
        self._repositorio_formacao = repositorio_formacao
        self._gerador_formacao_id = gerador_formacao_id

    async def executar(
        self, entrada: CadastrarFormacaoAcademicaEntrada
    ) -> FormacaoAcademica:
        """Cadastra uma formação vinculada a perfil existente e ainda ativo.

        O método obtém o proprietário, interrompe o fluxo para ausência ou
        exclusão e então cria a entidade com os value objects fornecidos antes
        de solicitar o salvamento assíncrono. Ele existe para impedir formação
        órfã ou atribuída a perfil removido sem fazer I/O diretamente.
        """
        usuario = await self._repositorio_usuario.obter_por_id(entrada.usuario_id)
        if usuario is None:
            raise PerfilNaoEncontrado("Perfil não encontrado.")
        if usuario.excluido:
            raise PerfilExcluido("Perfil excluído não pode cadastrar formação.")

        formacao = FormacaoAcademica(
            id=self._gerador_formacao_id.gerar(),
            usuario_id=entrada.usuario_id,
            instituicao=entrada.instituicao,
            curso=entrada.curso,
            nivel=entrada.nivel,
            periodo=entrada.periodo,
            status=entrada.status,
        )
        await self._repositorio_formacao.salvar(formacao)
        return formacao


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
