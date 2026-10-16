"""Define entidades reutilizáveis que compõem o perfil profissional do usuário.

As entidades mantêm identidade própria e proprietário explícito, sem conhecer
ORM, tabelas ou APIs. Elas existem para separar os itens reutilizáveis das
transições da conta e permitir seu crescimento coeso fora de um módulo genérico.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum
from unicodedata import category

# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.value_objects import (
    CertificacaoId,
    CompetenciaId,
    DocumentoId,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    IdiomaId,
    Periodo,
    ProjetoAcademicoId,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
TAMANHO_MINIMO_TEXTO_FORMACAO = 1
TAMANHO_MAXIMO_TEXTO_FORMACAO = 200

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
TAMANHO_MINIMO_TEXTO_CERTIFICACAO = 1
TAMANHO_MAXIMO_TEXTO_CERTIFICACAO = 200


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
class NivelFormacaoAcademica(str, Enum):
    """Representa os níveis acadêmicos aceitos para uma formação.

    Cada membro guarda o identificador canônico em snake_case usado pelo
    domínio e por futuras fronteiras de serialização. Ele existe para impedir
    que formações mantenham rótulos livres e inconsistentes entre camadas.
    """

    ENSINO_FUNDAMENTAL = "ensino_fundamental"
    ENSINO_MEDIO = "ensino_medio"
    TECNICO = "tecnico"
    TECNOLOGO = "tecnologo"
    GRADUACAO = "graduacao"
    ESPECIALIZACAO = "especializacao"
    MESTRADO = "mestrado"
    DOUTORADO = "doutorado"


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
class StatusFormacaoAcademica(str, Enum):
    """Representa os estados de conclusão válidos para uma formação.

    O enum limita o status aos estados de andamento, conclusão ou interrupção
    aprovados pelo produto. Ele existe para que a entidade aplique regras de
    período a partir de valores de domínio explícitos.
    """

    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"
    INTERROMPIDO = "interrompido"


# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
def _normalizar_texto_formacao(valor: str, campo: str) -> str:
    """Normaliza e valida um texto descritivo de formação.

    A função calcula uma única versão sem espaços externos, rejeita controles
    no valor original e mede o texto normalizado contra os limites públicos.
    Ela existe para aplicar à instituição e ao curso a mesma regra de conteúdo.
    """
    if not isinstance(valor, str):
        raise RegraDeDominioViolada(f"O campo {campo} da formação deve ser texto.")

    normalizado = valor.strip()
    if any(category(caractere) == "Cc" for caractere in valor):
        raise RegraDeDominioViolada(
            f"O campo {campo} da formação não pode conter caracteres de controle."
        )
    if not normalizado:
        raise RegraDeDominioViolada(
            f"O campo {campo} da formação não pode ser vazio."
        )
    if not TAMANHO_MINIMO_TEXTO_FORMACAO <= len(normalizado) <= TAMANHO_MAXIMO_TEXTO_FORMACAO:
        raise RegraDeDominioViolada(
            f"O campo {campo} da formação deve ter entre "
            f"{TAMANHO_MINIMO_TEXTO_FORMACAO} e {TAMANHO_MAXIMO_TEXTO_FORMACAO} caracteres."
        )
    return normalizado


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
# Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
@dataclass(frozen=True, slots=True)
class FormacaoAcademica:
    """Representa uma formação acadêmica reutilizável pertencente a um usuário.

    A entidade combina identidade e proprietário com instituição/curso
    normalizados, enums acadêmicos e um ``Periodo`` validado segundo o status.
    Ela existe para que a formação seja reutilizável em versões de currículo e
    permaneça válida sem depender de API ou persistência.
    """

    id: FormacaoAcademicaId
    usuario_id: UsuarioId
    instituicao: str
    curso: str
    nivel: NivelFormacaoAcademica
    periodo: Periodo
    status: StatusFormacaoAcademica
    deleted_at: datetime | None = None

    def __post_init__(self) -> None:
        """Protege vocabulário, conteúdo textual e período da formação.

        A entidade exige enums do domínio, normaliza instituição e curso uma
        vez e valida que somente formações concluídas dependam de data final.
        Ela existe para impedir estados inválidos por qualquer caminho de
        criação, sem delegar invariantes de negócio à API ou persistência.
        """
        if not isinstance(self.nivel, NivelFormacaoAcademica):
            raise RegraDeDominioViolada(
                "O nível da formação deve pertencer ao vocabulário acadêmico válido."
            )
        if not isinstance(self.status, StatusFormacaoAcademica):
            raise RegraDeDominioViolada(
                "O status da formação deve pertencer ao vocabulário válido."
            )
        instituicao = _normalizar_texto_formacao(self.instituicao, "instituição")
        curso = _normalizar_texto_formacao(self.curso, "curso")
        if self.status is StatusFormacaoAcademica.CONCLUIDO and self.periodo.fim is None:
            raise RegraDeDominioViolada(
                "Formação concluída exige data final do período."
            )
        object.__setattr__(self, "instituicao", instituicao)
        object.__setattr__(self, "curso", curso)

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    def editar(
        self,
        instituicao: str,
        curso: str,
        nivel: NivelFormacaoAcademica,
        periodo: Periodo,
        status: StatusFormacaoAcademica,
    ) -> FormacaoAcademica:
        """Devolve a formação com o conjunto completo de dados editado.

        O método constrói uma nova entidade com a mesma identidade e
        proprietário, reaplicando por ``__post_init__`` as invariantes de texto,
        enum e coerência temporal. Ele existe para permitir alterações válidas
        sem mutar a entidade imutável nem duplicar suas regras de construção.
        """
        return FormacaoAcademica(
            id=self.id,
            usuario_id=self.usuario_id,
            instituicao=instituicao,
            curso=curso,
            nivel=nivel,
            periodo=periodo,
            status=status,
            deleted_at=self.deleted_at,
        )

    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    @property
    def excluida(self) -> bool:
        """Informa se a formação está logicamente excluída.

        A propriedade deriva o estado da presença de ``deleted_at`` sem
        consultar persistência ou relógio. Ela existe para orientar as
        transições de perfil e tornar exclusões repetidas explícitas.
        """
        return self.deleted_at is not None

    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    def excluir(self, excluida_em: datetime) -> FormacaoAcademica:
        """Produz a exclusão lógica da formação, preservando o primeiro instante.

        A transição exige um datetime com fuso e usa ``replace`` somente
        enquanto a entidade estiver ativa; chamadas repetidas devolvem a mesma
        entidade. Ela existe para retirar o item do perfil sem purga física.
        """
        if self.excluida:
            return self
        if excluida_em.tzinfo is None or excluida_em.utcoffset() is None:
            raise RegraDeDominioViolada(
                "O instante de exclusão deve informar um fuso horário."
            )
        return replace(self, deleted_at=excluida_em)


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class ExperienciaProfissional:
    """Representa uma experiência profissional reutilizável do usuário.

    A entidade mantém identidade, proprietário, descrição profissional e um
    intervalo cronologicamente válido. Ela existe para preservar a experiência
    como item independente que currículos distintos podem referenciar.
    """

    id: ExperienciaProfissionalId
    usuario_id: UsuarioId
    empresa: str
    cargo: str
    descricao: str
    periodo: Periodo

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def __post_init__(self) -> None:
        """Garante que a experiência profissional contenha os textos essenciais.

        A validação percorre empresa, cargo e descrição, removendo espaços para
        identificar valores ausentes antes que a entidade possa ser usada. Ela
        existe para impedir que o currículo mantenha experiências sem a
        informação mínima necessária para sua apresentação profissional.
        """
        for campo, valor in (
            ("empresa", self.empresa),
            ("cargo", self.cargo),
            ("descrição", self.descricao),
        ):
            if not isinstance(valor, str) or not valor.strip():
                raise RegraDeDominioViolada(
                    f"A experiência profissional exige {campo} preenchido."
                )


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class ProjetoAcademico:
    """Representa um projeto acadêmico reutilizável pertencente a um usuário.

    A entidade agrupa identidade, proprietário e os textos descritos no DER sem
    impor vocabulário para tecnologias. Ela existe para permitir que projetos
    sejam selecionados em diferentes versões de currículo.
    """

    id: ProjetoAcademicoId
    usuario_id: UsuarioId
    titulo: str
    descricao: str
    tecnologias: str

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    def __post_init__(self) -> None:
        """Garante que o projeto acadêmico contenha os textos essenciais.

        A validação percorre título, descrição e tecnologias, removendo espaços
        para identificar valores ausentes antes que a entidade seja utilizada.
        Ela existe para impedir que o perfil mantenha projetos sem informação
        mínima para apresentação em currículos.
        """
        for campo, valor in (
            ("título", self.titulo),
            ("descrição", self.descricao),
            ("tecnologias", self.tecnologias),
        ):
            if not isinstance(valor, str) or not valor.strip():
                raise RegraDeDominioViolada(
                    f"O projeto acadêmico exige {campo} preenchido."
                )


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class CategoriaCompetencia(str, Enum):
    """Representa as categorias válidas de uma competência do perfil.

    O enum limita o valor às categorias técnica e comportamental, sem depender
    de transporte ou persistência. Ele existe para que o domínio preserve a
    distinção solicitada ao cadastrar e deduplicar competências.
    """

    TECNICA = "tecnica"
    COMPORTAMENTAL = "comportamental"


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
def normalizar_descricao_competencia(descricao: str) -> str:
    """Produz a chave textual usada para comparar competências equivalentes.

    A função exige texto, colapsa espaços Unicode entre termos e aplica
    ``casefold`` sem remover acentos, pontuação ou símbolos. Ela existe para
    tornar a regra de duplicidade determinística e reutilizável pelo domínio e
    pela orquestração, sem depender de collation do banco.
    """
    if not isinstance(descricao, str):
        raise RegraDeDominioViolada("A competência exige descrição textual.")
    return " ".join(descricao.split()).casefold()


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class Competencia:
    """Representa uma competência reutilizável pertencente a um usuário.

    A entidade identifica a competência, registra categoria, descrição e nível
    como valores controlados ou textos validados, pois o vocabulário de níveis
    ainda não foi especificado. Ela existe para que o perfil seja independente
    de uma versão particular de currículo e diferencie habilidades técnicas e
    comportamentais.
    """

    id: CompetenciaId
    usuario_id: UsuarioId
    categoria: CategoriaCompetencia
    descricao: str
    nivel: str

    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    def __post_init__(self) -> None:
        """Valida e apará os textos obrigatórios de uma competência.

        O método confirma a categoria controlada, normaliza a descrição para
        detectar ausência e remove somente seus espaços de contorno; o nível
        também deve ser texto não vazio. Ele existe para manter toda entidade
        de competência válida antes que a Application consulte ou persista.
        """
        if not isinstance(self.categoria, CategoriaCompetencia):
            raise RegraDeDominioViolada("A competência exige categoria válida.")
        descricao_normalizada = normalizar_descricao_competencia(self.descricao)
        if not descricao_normalizada:
            raise RegraDeDominioViolada("A competência exige descrição preenchida.")
        if not isinstance(self.nivel, str) or not self.nivel.strip():
            raise RegraDeDominioViolada("A competência exige nível preenchido.")
        object.__setattr__(self, "descricao", self.descricao.strip())
        object.__setattr__(self, "nivel", self.nivel.strip())

    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    @property
    def descricao_normalizada(self) -> str:
        """Devolve a chave canônica da descrição da competência.

        A propriedade reaplica a política de colapso de espaços e ``casefold``
        sobre a descrição já validada. Ela existe para dar ao caso de uso uma
        chave estável de duplicidade sem expor detalhe de infraestrutura.
        """
        return normalizar_descricao_competencia(self.descricao)


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
def normalizar_idioma(idioma: str) -> str:
    """Colapsa espaços e aplica minúsculas à denominação do idioma.

    A função rejeita valores não textuais, agrupa sequências de espaços e aplica
    ``casefold`` sem remover acentos, pontuação ou símbolos. Ela existe para
    tornar a regra de duplicidade determinística e reutilizável pelo domínio e
    pela orquestração, sem depender de collation do banco.
    """
    if not isinstance(idioma, str):
        raise RegraDeDominioViolada("O idioma exige denominação textual.")
    return " ".join(idioma.split()).casefold()


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class Idioma:
    """Representa um idioma e nível reutilizáveis pertencentes a um usuário.

    A entidade mantém a identidade e proprietário tipados e conserva o nível
    como texto enquanto não houver vocabulário aprovado. Ela existe para que o
    mesmo idioma possa compor mais de uma versão de currículo.
    """

    id: IdiomaId
    usuario_id: UsuarioId
    idioma: str
    nivel: str

    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    def __post_init__(self) -> None:
        """Valida e apara os textos obrigatórios de um idioma.

        O método normaliza o idioma para detectar ausência e remove somente
        seus espaços de contorno; o nível também deve ser texto não vazio. Ele
        existe para manter toda entidade de idioma válida antes que a Application
        consulte ou persista.
        """
        denominacao_normalizada = normalizar_idioma(self.idioma)
        if not denominacao_normalizada:
            raise RegraDeDominioViolada("O idioma exige denominação preenchida.")
        if not isinstance(self.nivel, str) or not self.nivel.strip():
            raise RegraDeDominioViolada("O idioma exige nível preenchido.")
        object.__setattr__(self, "idioma", self.idioma.strip())
        object.__setattr__(self, "nivel", self.nivel.strip())

    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    @property
    def idioma_normalizado(self) -> str:
        """Devolve a chave canônica do nome do idioma.

        A propriedade reaplica a política de colapso de espaços e ``casefold``
        sobre o idioma já validado. Ela existe para dar ao caso de uso uma
        chave estável de duplicidade sem expor detalhe de infraestrutura.
        """
        return normalizar_idioma(self.idioma)


# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
@dataclass(frozen=True, slots=True)
class Documento:
    """Representa metadados de um documento reutilizável do usuário.

    A entidade guarda identidade, proprietário e metadados descritos no DER sem
    abrir arquivo ou acessar armazenamento. Ela existe para que currículos
    referenciem documentos sem depender de adaptadores de upload ou arquivos.
    """

    id: DocumentoId
    usuario_id: UsuarioId
    nome_arquivo: str
    tipo_arquivo: str
    url_armazenamento: str


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
def normalizar_texto_certificacao(valor: str, campo: str) -> str:
    """Normaliza e valida um campo textual de certificação.

    A função rejeita tipos não textuais ou caracteres de controle, remove
    espaços laterais e verifica se o comprimento resultante cumpre os limites
    estabelecidos. Ela existe para unificar as regras de integridade e higiene
    textual para nome e organização emissora de certificações.
    """
    if not isinstance(valor, str):
        raise RegraDeDominioViolada(f"O campo {campo} da certificação deve ser texto.")

    normalizado = valor.strip()
    if any(category(caractere) == "Cc" for caractere in valor):
        raise RegraDeDominioViolada(
            f"O campo {campo} da certificação não pode conter caracteres de controle."
        )
    if not normalizado:
        raise RegraDeDominioViolada(
            f"O campo {campo} da certificação não pode ser vazio."
        )
    if (
        not TAMANHO_MINIMO_TEXTO_CERTIFICACAO
        <= len(normalizado)
        <= TAMANHO_MAXIMO_TEXTO_CERTIFICACAO
    ):
        raise RegraDeDominioViolada(
            f"O campo {campo} da certificação deve ter entre "
            f"{TAMANHO_MINIMO_TEXTO_CERTIFICACAO} e {TAMANHO_MAXIMO_TEXTO_CERTIFICACAO} caracteres."
        )
    return normalizado


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
def normalizar_chave_certificacao(texto: str) -> str:
    """Colapsa sequências de espaços e aplica minúsculas a um texto de certificação.

    A função agrupa espaços em branco repetidos e converte as letras via
    ``casefold()`` preservando acentuação. Ela existe para gerar chaves
    canônicas determinísticas para detecção de duplicidades.
    """
    return " ".join(texto.split()).casefold()


# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
@dataclass(frozen=True, slots=True)
class Certificacao:
    """Representa uma certificação profissional ou acadêmica do usuário.

    A entidade combina identidade tipada, proprietário, nome da certificação e
    organização emissora já normalizados e aparados. Ela existe para modelar de
    forma íntegra as certificações no perfil do estudante sem depender de ORM
    ou de camadas externas.
    """

    id: CertificacaoId
    usuario_id: UsuarioId
    nome: str
    organizacao_emissora: str

    def __post_init__(self) -> None:
        """Valida e apara os campos textuais de uma certificação.

        O método valida e remove espaços excedentes de nome e organização
        emissora, aplicando invariantes de preenchimento e controle. Ele existe
        para assegurar que nenhuma entidade de certificação seja instanciada com
        dados inválidos ou corrompidos.
        """
        nome_validado = normalizar_texto_certificacao(self.nome, "nome")
        emissor_validado = normalizar_texto_certificacao(
            self.organizacao_emissora, "organização emissora"
        )
        object.__setattr__(self, "nome", nome_validado)
        object.__setattr__(self, "organizacao_emissora", emissor_validado)

    @property
    def nome_normalizado(self) -> str:
        """Devolve a versão canônica do nome da certificação para deduplicação.

        A propriedade reaplica o colapso de espaços e ``casefold`` sobre o nome
        validado. Ela existe para fornecer uma chave determinística de busca e
        prevenção de duplicatas lógicas.
        """
        return normalizar_chave_certificacao(self.nome)

    @property
    def organizacao_emissora_normalizada(self) -> str:
        """Devolve a versão canônica da organização emissora para deduplicação.

        A propriedade reaplica o colapso de espaços e ``casefold`` sobre a
        organização emissora validada. Ela existe para permitir comparação exata
        entre emissores sem depender de collations de banco.
        """
        return normalizar_chave_certificacao(self.organizacao_emissora)

