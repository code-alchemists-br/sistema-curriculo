"""Orquestra a manutenção dos dados pessoais e de contato do estudante.

O módulo localiza o agregado por identidade e delega a atualização de
endereço, telefones e links profissionais à transição do domínio, sem
conhecer HTTP ou persistência concreta. Ele existe para reaproveitar as
mesmas regras de perfil ativo ao manter dados de contato separados de
identidade e credencial.
"""

from dataclasses import dataclass

from backend.application.perfil_estudante import PerfilExcluido, PerfilNaoEncontrado
from backend.application.ports import RepositorioUsuario
from backend.domain.usuario import Usuario
from backend.domain.value_objects import DadosContato, UsuarioId

# Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001

@dataclass(frozen=True, slots=True)
class AtualizarDadosContatoEntrada:
    """Agrupa identidade e dados de contato válidos para atualizar um perfil.

        A entrada transporta um ``DadosContato`` já validado pelo domínio,
        independente de HTTP. Ela existe para dar contrato explícito ao caso de
        uso sem misturar identidade, senha ou demais itens de currículo.
        """

    usuario_id: UsuarioId
    dados_contato: DadosContato


class AtualizarDadosContato:
    """Atualiza endereço, telefones e links de contato de um perfil ativo.

        O caso busca o agregado, rejeita ausência ou exclusão e persiste a
        transição produzida pelo domínio. Ele existe para coordenar a manutenção
        de dados de contato sem acoplar regras a API ou repositório real.
        """

    def __init__(self, repositorio_usuario: RepositorioUsuario) -> None:
        """Recebe a porta usada para consultar e atualizar perfis.

                O construtor armazena somente a abstração interna que será aguardada
                durante a execução e pode ser substituída por double. Ele existe para
                manter a orquestração independente da infraestrutura.
                """
        self._repositorio_usuario = repositorio_usuario

    async def executar(self, entrada:AtualizarDadosContatoEntrada) -> Usuario:
        """Aplica a atualização válida e devolve o novo estado persistido.

                O método localiza o usuário, rejeita ausência ou exclusão e delega a
                transição ao domínio antes de solicitar a atualização. Ele existe para
                preservar identidade e credencial no fluxo de manutenção de contato.
                """
        usuario = await self._repositorio_usuario.obter_por_id(entrada.usuario_id)
        if usuario is None:
            raise PerfilNaoEncontrado("Perfil não encontrado")
        if usuario.excluido:
            raise PerfilExcluido("Perfil excluído não pode atualiza dados de contato")

        usuario_atualizado = usuario.atualizar_dados_contato(entrada.dados_contato)
        await self ._repositorio_usuario.atualizar(usuario_atualizado)
        return usuario_atualizado
