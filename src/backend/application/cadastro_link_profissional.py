"""Orquestra o cadastro de links profissionais reutilizáveis de estudantes.

O módulo constrói a entidade de domínio, verifica sua chave lógica por uma
porta e solicita persistência sem importar transporte, ORM ou banco. Ele existe
para concentrar a regra de criação e duplicidade em uma unidade testável.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.application.ports import (
    GeradorLinkProfissionalId,
    RepositorioLinkProfissional,
)
from backend.domain.itens_perfil import LinkProfissional
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class LinkProfissionalJaCadastrado(ValueError):
    """Sinaliza tentativa de cadastrar um link profissional já existente para o estudante.

    A falha representa uma colisão da chave lógica formada por proprietário e
    URL normalizada, sem transportar detalhes de armazenamento. Ela existe para
    que fronteiras externas possam responder conflito de forma segura e o caso
    de uso não persista uma duplicata.
    """


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
@dataclass(frozen=True, slots=True)
class CadastrarLinkProfissionalEntrada:
    """Agrupa os dados internos necessários ao cadastro de um link profissional.

    A entrada conserva proprietário tipado, rótulo descritivo e URL web
    sem transportar tipos HTTP ou detalhes de persistência. Ela existe
    para tornar explícito e testável o contrato do caso de uso de cadastro.
    """

    usuario_id: UsuarioId
    rotulo: str
    url: str


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class CadastrarLinkProfissional:
    """Cria e persiste um link profissional não duplicado para um estudante.

    O caso de uso gera identidade por porta, constrói a entidade para aplicar
    invariantes de segurança e integridade, consulta a chave de duplicidade e
    só então solicita salvar. Ele existe para coordenar a regra entre entidades
    independentes sem acoplar o núcleo a armazenamento ou interface.
    """

    def __init__(
        self,
        repositorio: RepositorioLinkProfissional,
        gerador_id: GeradorLinkProfissionalId,
    ) -> None:
        """Recebe as portas usadas para verificar e persistir o link profissional.

        O construtor conserva somente abstrações internas injetadas, permitindo
        que o fluxo seja exercitado com doubles determinísticos. Ele existe para
        inverter a dependência da orquestração em relação à infraestrutura.
        """
        self._repositorio = repositorio
        self._gerador_id = gerador_id

    async def executar(
        self, entrada: CadastrarLinkProfissionalEntrada
    ) -> LinkProfissional:
        """Cria o link profissional e o salva quando sua chave ainda não existe.

        O método constrói a entidade para validar rótulo e sanitizar a URL, consulta
        o repositório usando a chave canônica url_normalizada e interrompe em caso
        de colisão; somente depois solicita salvar. Ele existe para impedir
        duplicatas lógicas sem delegar regras de negócio ao adapter.
        """
        link = LinkProfissional(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            rotulo=entrada.rotulo,
            url=entrada.url,
        )
        existe = await self._repositorio.existe_por_chave_de_duplicidade(
            usuario_id=link.usuario_id,
            url_normalizada=link.url_normalizada,
        )
        if existe:
            raise LinkProfissionalJaCadastrado(
                "Link profissional já cadastrado para este usuário."
            )
        await self._repositorio.salvar(link)
        return link
