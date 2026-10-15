"""Orquestra a atualização integral dos dados editáveis do perfil.

O caso de uso valida o proprietário, a unicidade do e-mail e o estado do
agregado antes de aplicar nome, e-mail e contato em memória e solicitar uma
única persistência. Ele existe para oferecer uma operação integral sem gravar
somente parte do perfil quando uma validação falha.
"""

from dataclasses import dataclass

from backend.application.cadastro_estudante import EmailJaCadastrado
from backend.application.perfil_estudante import PerfilExcluido, PerfilNaoEncontrado
from backend.application.ports import RepositorioUsuario
from backend.domain.usuario import Usuario
from backend.domain.value_objects import DadosContato, Email, Nome, UsuarioId


@dataclass(frozen=True, slots=True)
class AtualizarPerfilCompletoEntrada:
    """Agrupa os valores de domínio para uma edição integral de perfil.

    A entrada recebe identidade, nome, e-mail e contato já tipados, sem incluir
    credencial, identidade do transporte ou detalhes de persistência. Ela
    existe para expressar a intenção única de substituir os dados editáveis.
    """

    usuario_id: UsuarioId
    nome: Nome
    email: Email
    dados_contato: DadosContato


class AtualizarPerfilCompleto:
    """Atualiza todos os dados editáveis de um perfil ativo.

    O caso busca o agregado pela identidade autenticada, rejeita ausência,
    exclusão ou e-mail de outra conta, compõe as transições de domínio e pede
    uma única atualização ao repositório. Ele existe para manter a nova rota
    completa e consistente sem alterar as operações de edição existentes.
    """

    def __init__(self, repositorio_usuario: RepositorioUsuario) -> None:
        """Recebe a porta responsável por localizar e atualizar usuários.

        O construtor armazena somente a abstração interna, substituível por um
        double em testes. Ele existe para manter a aplicação independente do
        adapter de persistência.
        """
        self._repositorio_usuario = repositorio_usuario

    async def executar(self, entrada: AtualizarPerfilCompletoEntrada) -> Usuario:
        """Valida e persiste uma única transição integral do agregado.

        O método verifica perfil ativo e unicidade do e-mail, aplica ambas as
        transições antes de persistir e devolve o estado completo salvo. Ele
        existe para evitar uma gravação parcial entre identidade e contato.
        """
        usuario = await self._repositorio_usuario.obter_por_id(entrada.usuario_id)
        if usuario is None:
            raise PerfilNaoEncontrado("Perfil não encontrado.")
        if usuario.excluido:
            raise PerfilExcluido("Perfil excluído não pode ser editado.")

        proprietario_email = await self._repositorio_usuario.obter_por_email(
            entrada.email
        )
        if proprietario_email is not None and proprietario_email.id != entrada.usuario_id:
            raise EmailJaCadastrado("Já existe uma conta cadastrada com este e-mail.")

        usuario_atualizado = usuario.editar_perfil(
            entrada.nome, entrada.email
        ).atualizar_dados_contato(entrada.dados_contato)
        await self._repositorio_usuario.atualizar(usuario_atualizado)
        return usuario_atualizado
