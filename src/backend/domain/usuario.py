"""Define o aggregate root responsável pela conta e pelo perfil do usuário.

O módulo concentra identidade, credencial e transições locais do usuário sem
conhecer ORM, APIs ou persistência. Ele existe para que o ciclo de vida do
perfil evolua fora dos itens reutilizáveis e do agregado de currículo.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.value_objects import DadosContato, Email, HashSenha, Nome, UsuarioId


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class Usuario:
    """Representa o aggregate root da conta e identidade do usuário.

    A entidade reúne uma identidade tipada, nome, e-mail e hash de senha já
    derivado, todos validados por value objects. Ela existe como proprietário
    conceitual de currículos e itens de perfil, sem acoplar autenticação, sessão
    ou recuperação de senha à primeira fatia de domínio.
    """

    id: UsuarioId
    nome: Nome
    email: Email
    hash_senha: HashSenha
    deleted_at: datetime | None = None
    # Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
    dados_contato: DadosContato | None = None

    @property
    def excluido(self) -> bool:
        """Informa se o perfil do usuário está logicamente excluído.

        A propriedade deriva o estado exclusivamente da presença de
        ``deleted_at``, sem consultar relógio ou persistência. Ela existe para
        que regras e casos de uso interrompam operações em perfis removidos.
        """
        return self.deleted_at is not None

    def editar_perfil(self, nome: Nome, email: Email) -> Usuario:
        """Produz o estado editado do perfil preservando identidade e credencial.

        A transição rejeita perfis excluídos e usa ``replace`` para conservar o
        agregado original imutável, seu ID e hash de senha. Ela existe para que
        alterações de nome e e-mail ocorram somente pela raiz do agregado.
        """
        if self.excluido:
            raise RegraDeDominioViolada("Perfil excluído não pode ser editado.")
        return replace(self, nome=nome, email=email)

    # Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
    def atualizar_dados_contato(self, dados_contato: DadosContato) -> Usuario:
        """Produz o estado do perfil com endereço, telefones e links atualizados.

        A transição rejeita perfis excluídos e usa ``replace`` para conservar o
        agregado original imutável, sua identidade, credencial e demais dados.
        Ela existe para que a manutenção de contato siga o mesmo contrato de
        ``editar_perfil`` sem misturar identidade com dados de contato.
        """
        if self.excluido:
            raise RegraDeDominioViolada("Perfil excluído não pode ser editado.")
        return replace(self, dados_contato=dados_contato)

    def excluir(self, excluido_em: datetime) -> Usuario:
        """Produz a exclusão lógica idempotente do perfil do usuário.

        A transição registra o instante recebido somente na primeira chamada e
        devolve o próprio agregado quando ele já está excluído. Ela existe para
        bloquear o uso do perfil sem executar purga física ou acessar relógio.
        """
        if self.excluido:
            return self
        return replace(self, deleted_at=excluido_em)