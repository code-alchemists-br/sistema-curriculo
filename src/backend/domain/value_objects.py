"""Modela valores imutáveis e identidades tipadas do domínio de currículos.

Os tipos deste módulo validam dados que têm significado próprio, como e-mail,
período e identificadores. Eles existem para impedir trocas acidentais de
identidade e estados estruturalmente inválidos antes que entidades os utilizem.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re
from uuid import UUID

from backend.domain.exceptions import RegraDeDominioViolada


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class UsuarioId:
    """Representa a identidade imutável de um usuário.

    O value object aceita somente um ``UUID`` e o preserva sem transformação.
    Ele existe para impedir que identidades de outros conceitos sejam usadas no
    lugar do proprietário de dados e currículos.
    """

    valor: UUID

    def __post_init__(self) -> None:
        """Confirma que a identidade usa UUID para preservar seu tipo de domínio.

        A validação ocorre na construção e rejeita valores de transporte ou
        persistência ainda não convertidos. Ela existe para manter a fronteira
        entre a identidade do usuário e valores textuais ou de outras entidades.
        """
        _validar_uuid(self.valor, "UsuarioId")


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class CurriculoId:
    """Representa a identidade imutável de uma versão de currículo.

    O value object armazena exclusivamente um ``UUID`` já criado. Ele existe
    para separar a identidade de currículo das demais entidades reutilizáveis.
    """

    valor: UUID

    def __post_init__(self) -> None:
        """Valida o UUID recebido para impedir uma identidade de currículo inválida.

        A checagem é local, não consulta persistência e acontece antes do uso
        pelo agregado. Ela existe para que o currículo tenha identidade válida
        mesmo quando é criado e testado inteiramente em memória.
        """
        _validar_uuid(self.valor, "CurriculoId")


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class FormacaoAcademicaId:
    """Representa a identidade imutável de uma formação acadêmica.

    O value object armazena exclusivamente um ``UUID`` e o valida na criação.
    Ele existe para distinguir formações dos demais itens de perfil nas relações
    que um currículo pode compor.
    """

    valor: UUID

    def __post_init__(self) -> None:
        """Valida o UUID para separar formações de outras identidades do perfil.

        A validação é executada na criação e mantém o valor pronto para uso por
        entidades e referências de currículo. Ela existe para evitar que outro
        identificador seja associado a uma formação por engano.
        """
        _validar_uuid(self.valor, "FormacaoAcademicaId")


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class ExperienciaProfissionalId:
    """Representa a identidade imutável de uma experiência profissional.

    O value object conserva somente um ``UUID`` validado durante a construção.
    Ele existe para que referências de currículo não confundam experiências com
    outros itens reutilizáveis do perfil.
    """

    valor: UUID

    def __post_init__(self) -> None:
        """Valida o UUID para preservar a identidade específica da experiência.

        A checagem ocorre sem recurso externo e rejeita valores que não possam
        identificar uma experiência. Ela existe para proteger associações de
        currículo contra mistura de tipos de item.
        """
        _validar_uuid(self.valor, "ExperienciaProfissionalId")


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class ProjetoAcademicoId:
    """Representa a identidade imutável de um projeto acadêmico.

    O value object armazena exclusivamente um ``UUID`` e valida seu tipo ao ser
    criado. Ele existe para separar projetos acadêmicos dos demais conceitos
    que o usuário pode selecionar em uma versão de currículo.
    """

    valor: UUID

    def __post_init__(self) -> None:
        """Valida o UUID para manter o identificador de projeto bem formado.

        A validação acontece ao construir o value object e não depende de banco
        de dados. Ela existe para que referências possam distinguir projetos de
        outros itens do perfil.
        """
        _validar_uuid(self.valor, "ProjetoAcademicoId")


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class CompetenciaId:
    """Representa a identidade imutável de uma competência.

    O value object encapsula um ``UUID`` validado na construção, sem detalhes de
    persistência. Ele existe para preservar a identidade específica de uma
    competência quando ela é reutilizada por currículos distintos.
    """

    valor: UUID

    def __post_init__(self) -> None:
        """Valida o UUID para conservar a identidade específica da competência.

        A checagem é local e impede criação de referências com valores de tipo
        inadequado. Ela existe para manter a linguagem do domínio explícita nas
        relações de currículo.
        """
        _validar_uuid(self.valor, "CompetenciaId")


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class IdiomaId:
    """Representa a identidade imutável de um idioma cadastrado pelo usuário.

    O value object guarda um ``UUID`` e confirma seu tipo ao ser criado. Ele
    existe para que relações de currículo expressem claramente que selecionam um
    idioma, e não qualquer outro item de perfil.
    """

    valor: UUID

    def __post_init__(self) -> None:
        """Valida o UUID para preservar a identidade do item de idioma.

        A validação ocorre na criação, sem detalhes de persistência, e rejeita
        valores não UUID. Ela existe para evitar que uma referência de idioma
        seja confundida com qualquer outro item de perfil.
        """
        _validar_uuid(self.valor, "IdiomaId")


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class DocumentoId:
    """Representa a identidade imutável de um documento do usuário.

    O value object encapsula um ``UUID`` validado e não acessa o arquivo nem seu
    armazenamento. Ele existe para permitir referência a documentos sem acoplar
    o domínio a adaptadores externos de upload ou persistência.
    """

    valor: UUID

    def __post_init__(self) -> None:
        """Valida o UUID para distinguir um documento dos demais itens do perfil.

        A validação é deliberadamente independente do armazenamento do arquivo.
        Ela existe para que o domínio possa referenciar documentos sem importar
        adaptadores de upload ou persistência.
        """
        _validar_uuid(self.valor, "DocumentoId")


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class Email:
    """Representa um e-mail normalizado e estruturalmente válido.

    O value object remove espaços nas extremidades, normaliza letras para
    minúsculas e valida uma estrutura local simples. Ele existe para impedir que
    entidades de usuário sejam criadas com um e-mail vazio ou malformado.
    """

    valor: str

    def __post_init__(self) -> None:
        """Normaliza e valida o e-mail ao construir o value object.

        A validação exige uma parte local, um domínio e um ponto no domínio, sem
        tentar confirmar a existência do endereço. Ela existe para proteger a
        invariante estrutural sem introduzir rede ou política de autenticação.
        """
        valor_normalizado = self.valor.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor_normalizado):
            raise RegraDeDominioViolada("E-mail deve possuir formato válido.")
        object.__setattr__(self, "valor", valor_normalizado)


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class Nome:
    """Representa um nome não vazio do domínio de usuário.

    O value object remove espaços periféricos e preserva o conteúdo informado.
    Ele existe para assegurar que a identidade legível de um usuário não seja
    composta somente por espaços.
    """

    valor: str

    def __post_init__(self) -> None:
        """Normaliza espaços periféricos e rejeita um nome vazio.

        A checagem é realizada no momento da criação e não aplica políticas de
        apresentação ou internacionalização ainda não especificadas. Ela existe
        para garantir uma invariante mínima para a entidade ``Usuario``.
        """
        valor_normalizado = self.valor.strip()
        if not valor_normalizado:
            raise RegraDeDominioViolada("Nome não pode ser vazio.")
        object.__setattr__(self, "valor", valor_normalizado)


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class Periodo:
    """Representa um intervalo de datas com fim opcional e cronologia válida.

    O value object aceita períodos em andamento por meio de ``fim`` ausente e
    compara as datas quando ambas existem. Ele existe para proteger formação e
    experiência contra intervalos que terminem antes de começar.
    """

    inicio: date
    fim: date | None = None

    def __post_init__(self) -> None:
        """Garante tipos de data e a ordem cronológica do intervalo.

        A validação acontece em memória, permitindo que entidades reutilizem o
        período sem conhecer banco ou relógio do sistema. Ela existe para manter
        a regra de cronologia junto aos dados que ela governa.
        """
        if not isinstance(self.inicio, date):
            raise RegraDeDominioViolada("Início do período deve ser uma data.")
        if self.fim is not None and not isinstance(self.fim, date):
            raise RegraDeDominioViolada("Fim do período deve ser uma data.")
        if self.fim is not None and self.fim < self.inicio:
            raise RegraDeDominioViolada("Fim do período não pode anteceder o início.")


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class HashSenha:
    """Representa um hash de senha já derivado, sem implementar criptografia.

    O value object aceita um valor não vazio produzido por uma política externa
    de segurança. Ele existe para impedir que a entidade de usuário receba uma
    credencial ausente, sem escolher algoritmo, salt ou comparação de senha.
    """

    valor: str

    def __post_init__(self) -> None:
        """Rejeita um hash ausente sem processar ou comparar credenciais.

        A validação limita-se à presença estrutural do valor e deixa operações
        criptográficas para uma decisão de segurança posterior. Ela existe para
        preservar o limite desta camada de domínio inicial.
        """
        if not self.valor.strip():
            raise RegraDeDominioViolada("Hash de senha não pode ser vazio.")


IdItemPerfil = (
    FormacaoAcademicaId
    | ExperienciaProfissionalId
    | ProjetoAcademicoId
    | CompetenciaId
    | IdiomaId
    | DocumentoId
)


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class ReferenciaCurriculo:
    """Representa uma referência tipada de um currículo a um item do perfil.

    O value object aceita apenas identificadores dos seis tipos de itens
    reutilizáveis definidos no DER. Ele existe para que o agregado ``Curriculo``
    controle inclusão e duplicidade sem converter tabelas de associação em
    entidades de domínio.
    """

    item_id: IdItemPerfil

    def __post_init__(self) -> None:
        """Valida que a referência aponta para um tipo permitido de item de perfil.

        A verificação usa os value objects de identidade e não consulta outros
        agregados ou repositórios. Ela existe para manter o currículo independente
        da infraestrutura e das regras transagregados de propriedade.
        """
        tipos_permitidos = (
            FormacaoAcademicaId,
            ExperienciaProfissionalId,
            ProjetoAcademicoId,
            CompetenciaId,
            IdiomaId,
            DocumentoId,
        )
        if not isinstance(self.item_id, tipos_permitidos):
            raise RegraDeDominioViolada("Referência deve apontar para um item de perfil.")


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
def _validar_uuid(valor: UUID, nome_do_tipo: str) -> None:
    """Valida a representação UUID compartilhada pelos identificadores tipados.

    A função recebe o valor e o nome do tipo para produzir uma falha clara sem
    duplicar a mesma regra em cada value object. Ela existe para manter todas as
    identidades do domínio estritamente baseadas em UUID.
    """
    if not isinstance(valor, UUID):
        raise RegraDeDominioViolada(f"{nome_do_tipo} deve receber um UUID.")
