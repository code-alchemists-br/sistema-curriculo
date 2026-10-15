"""Orquestra o cadastro de certificações reutilizáveis de estudantes.

O módulo constrói a entidade de domínio, verifica sua chave lógica por uma
porta e solicita persistência sem importar transporte, ORM ou banco. Ele existe
para concentrar a regra de criação e duplicidade em uma unidade testável.
"""

from dataclasses import dataclass

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
from backend.application.ports import (
    GeradorCertificacaoId,
    RepositorioCertificacao,
)
from backend.domain.itens_perfil import Certificacao
from backend.domain.value_objects import UsuarioId


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class CertificacaoJaCadastrada(ValueError):
    """Sinaliza tentativa de cadastrar uma certificação já existente para o estudante.

    A falha representa uma colisão da chave formada por proprietário, nome e
    organização emissora normalizados, sem transportar detalhes de armazenamento.
    Ela existe para que fronteiras externas possam responder conflito de forma
    segura e o caso de uso não persista uma duplicata.
    """


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
@dataclass(frozen=True, slots=True)
class CadastrarCertificacaoEntrada:
    """Agrupa os dados internos necessários ao cadastro de uma certificação.

    A entrada conserva proprietário tipado, nome e organização emissora sem
    transportar tipos HTTP ou detalhes de persistência. Ela existe para tornar
    explícito e testável o contrato do caso de uso de cadastro.
    """

    usuario_id: UsuarioId
    nome: str
    organizacao_emissora: str


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class CadastrarCertificacao:
    """Cria e persiste uma certificação não duplicada para um estudante.

    O caso de uso gera identidade por porta, constrói a entidade para aplicar
    invariantes, consulta a chave de duplicidade e só então solicita salvar.
    Ele existe para coordenar a regra entre entidades independentes sem acoplar
    o núcleo a armazenamento ou interface.
    """

    def __init__(
        self,
        repositorio: RepositorioCertificacao,
        gerador_id: GeradorCertificacaoId,
    ) -> None:
        """Recebe as portas usadas para verificar e persistir a certificação.

        O construtor conserva somente abstrações internas injetadas, permitindo
        que o fluxo seja exercitado com doubles determinísticos. Ele existe para
        inverter a dependência da orquestração em relação à infraestrutura.
        """
        self._repositorio = repositorio
        self._gerador_id = gerador_id

    async def executar(self, entrada: CadastrarCertificacaoEntrada) -> Certificacao:
        """Cria a certificação e a salva quando sua chave ainda não existe.

        O método constrói a entidade para validar os campos, consulta o
        repositório usando sua chave canônica composta e interrompe em caso de
        colisão; somente depois solicita salvar. Ele existe para impedir
        duplicatas lógicas sem delegar regras de negócio ao adapter.
        """
        certificacao = Certificacao(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            nome=entrada.nome,
            organizacao_emissora=entrada.organizacao_emissora,
        )
        existe = await self._repositorio.existe_por_chave_de_duplicidade(
            certificacao.usuario_id,
            certificacao.nome_normalizado,
            certificacao.organizacao_emissora_normalizada,
        )
        if existe:
            raise CertificacaoJaCadastrada("A certificação já está cadastrada.")
        await self._repositorio.salvar(certificacao)
        return certificacao
