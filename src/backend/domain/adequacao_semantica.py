"""Define a solicitação e a proposta revisável de adequação semântica.

O módulo mantém no domínio o consentimento explícito, os itens profissionais
selecionados e as sugestões que podem ser revisadas pelo estudante. Ele não
conhece JSON, SDK, HTTP, persistência ou fornecedor de IA. Ele existe para que
a assistência a uma vaga permaneça opcional, rastreável e incapaz de alterar o
currículo automaticamente.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum

from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.value_objects import CurriculoId, ReferenciaCurriculo


# Proveniência: docs/adequacao_semantica_ia.md#papel-da-ia.
class AcaoAdequacaoSemantica(str, Enum):
    """Identifica a ação de assistência semântica suportada nesta entrega.

    A enumeração mantém a intenção de adequar o currículo a uma vaga como um
    vocabulário fechado. Ela existe para que a política de contexto, a futura
    porta de geração e a proposta usem o mesmo nome de ação sem texto solto.
    """

    ADEQUAR_CURRICULO_VAGA = "adequar_curriculo_vaga"


# Proveniência: docs/adequacao_semantica_ia.md#papel-da-ia.
class TipoSugestaoAdequacao(str, Enum):
    """Classifica a parte do currículo que uma sugestão pretende melhorar.

    Os valores distinguem reescritas de itens selecionados de orientações
    globais como resumo ou palavras-chave. A enumeração existe para que a
    revisão no cliente não precise deduzir a intenção pelo texto sugerido.
    """

    EXPERIENCIA = "experiencia"
    PROJETO = "projeto"
    COMPETENCIA = "competencia"
    RESUMO_PROFISSIONAL = "resumo_profissional"
    PALAVRAS_CHAVE = "palavras_chave"


@dataclass(frozen=True, slots=True)
class ItemSelecionadoAdequacao:
    """Representa um trecho profissional autorizado para uma adequação.

    O value object liga uma referência tipada de currículo ao conteúdo reduzido
    que poderá ser enviado ao gerador, sem carregar contato ou documentos. Ele
    existe para preservar a escolha do estudante e permitir que a proposta seja
    conferida contra exatamente os itens autorizados.
    """

    referencia: ReferenciaCurriculo
    conteudo: str

    def __post_init__(self) -> None:
        """Valida a referência tipada e o conteúdo profissional não vazio.

        O método exige uma referência de item já reconhecida pelo domínio e um
        texto com significado após remover espaços nas bordas. Ele existe para
        impedir que a solicitação envie um item sem rastreabilidade ou sem dado
        útil para a adequação.
        """
        if not isinstance(self.referencia, ReferenciaCurriculo):
            raise RegraDeDominioViolada(
                "O item selecionado deve referenciar um item do currículo."
            )
        if not isinstance(self.conteudo, str) or not self.conteudo.strip():
            raise RegraDeDominioViolada(
                "O conteúdo do item selecionado deve ser informado."
            )


@dataclass(frozen=True, slots=True)
class SolicitacaoAdequacaoCurriculoVaga:
    """Representa uma solicitação consentida de adequação a uma vaga.

    A entidade reúne o currículo, o cargo desejado, a descrição opcional da
    vaga e os itens profissionais que o estudante autorizou usar. Ela existe
    para que qualquer gerador receba uma intenção válida sem assumir que a
    sugestão será aplicada ao currículo.
    """

    curriculo_id: CurriculoId
    cargo_alvo: str
    descricao_vaga: str | None
    itens_selecionados: tuple[ItemSelecionadoAdequacao, ...]
    consentimento_explicito: bool

    acao: AcaoAdequacaoSemantica = AcaoAdequacaoSemantica.ADEQUAR_CURRICULO_VAGA

    def __post_init__(self) -> None:
        """Protege consentimento, objetivo e seleção única de itens profissionais.

        O método exige o currículo tipado, cargo não vazio, consentimento igual
        a verdadeiro e ao menos um item com referência única; a descrição da
        vaga pode faltar porque o cargo é a orientação mínima documentada. Ele
        existe para bloquear a chamada externa antes dela existir quando o
        estudante não autorizou ou não escolheu conteúdo profissional.
        """
        if not isinstance(self.curriculo_id, CurriculoId):
            raise RegraDeDominioViolada("A solicitação deve referenciar um currículo.")
        if not isinstance(self.cargo_alvo, str) or not self.cargo_alvo.strip():
            raise RegraDeDominioViolada("O cargo-alvo deve ser informado.")
        if self.descricao_vaga is not None and (
            not isinstance(self.descricao_vaga, str) or not self.descricao_vaga.strip()
        ):
            raise RegraDeDominioViolada(
                "A descrição da vaga, quando informada, não pode ser vazia."
            )
        if self.consentimento_explicito is not True:
            raise RegraDeDominioViolada(
                "A adequação semântica exige consentimento explícito."
            )
        itens = tuple(self.itens_selecionados)
        if not itens or not all(isinstance(item, ItemSelecionadoAdequacao) for item in itens):
            raise RegraDeDominioViolada(
                "A solicitação deve conter ao menos um item profissional selecionado."
            )
        referencias = {item.referencia for item in itens}
        if len(referencias) != len(itens):
            raise RegraDeDominioViolada(
                "Um item profissional só pode ser selecionado uma vez."
            )
        object.__setattr__(self, "itens_selecionados", itens)

    @property
    def referencias_selecionadas(self) -> frozenset[ReferenciaCurriculo]:
        """Expõe as referências autorizadas sem permitir alteração da solicitação.

        A propriedade deriva um conjunto imutável dos itens selecionados. Ela
        existe para que a validação de propostas confira autorização sem expor a
        coleção interna como uma estrutura mutável.
        """
        return frozenset(item.referencia for item in self.itens_selecionados)

    def criar_proposta(
        self,
        modelo: str,
        versao_politica: str,
        sugestoes: Iterable[SugestaoAdequacao],
    ) -> PropostaAdequacaoCurriculoVaga:
        """Cria uma proposta revisável, limitada aos itens previamente autorizados.

        O método materializa as sugestões recebidas do gerador, exige que toda
        sugestão com referência aponte para a seleção e preserva a solicitação
        original sem mutá-la. Ele existe para impedir que uma resposta externa
        alcance itens não autorizados ou altere o currículo automaticamente.
        """
        sugestoes_materializadas = tuple(sugestoes)
        referencias_autorizadas = self.referencias_selecionadas
        for sugestao in sugestoes_materializadas:
            if not isinstance(sugestao, SugestaoAdequacao):
                raise RegraDeDominioViolada("A proposta contém uma sugestão inválida.")
            if (
                sugestao.referencia_item is not None
                and sugestao.referencia_item not in referencias_autorizadas
            ):
                raise RegraDeDominioViolada(
                    "A proposta não pode sugerir mudança em item não selecionado."
                )
        return PropostaAdequacaoCurriculoVaga(
            curriculo_id=self.curriculo_id,
            modelo=modelo,
            versao_politica=versao_politica,
            referencias_utilizadas=tuple(
                item.referencia for item in self.itens_selecionados
            ),
            sugestoes=sugestoes_materializadas,
        )


@dataclass(frozen=True, slots=True)
class SugestaoAdequacao:
    """Representa uma mudança sugerida que o estudante pode revisar ou descartar.

    O value object registra um código estável, o tipo da sugestão, a referência
    opcional ao item afetado, o texto proposto e sua justificativa. Ele existe
    para preservar a decisão final do estudante e permitir revisão granular sem
    converter a saída de IA em uma edição automática.
    """

    codigo: str
    tipo: TipoSugestaoAdequacao
    referencia_item: ReferenciaCurriculo | None
    texto_sugerido: str
    justificativa: str

    def __post_init__(self) -> None:
        """Valida a estrutura e a rastreabilidade da sugestão revisável.

        O método exige campos textuais não vazios, tipo fechado e referência
        tipada quando a sugestão aponta para um item. Ele existe para que a
        aplicação receba uma proposta compreensível sem confiar em texto livre
        ou em identificadores externos não validados.
        """
        for nome, valor in (
            ("codigo", self.codigo),
            ("texto_sugerido", self.texto_sugerido),
            ("justificativa", self.justificativa),
        ):
            if not isinstance(valor, str) or not valor.strip():
                raise RegraDeDominioViolada(f"{nome} deve ser informado.")
        if not isinstance(self.tipo, TipoSugestaoAdequacao):
            raise RegraDeDominioViolada("A sugestão deve possuir um tipo reconhecido.")
        if self.referencia_item is not None and not isinstance(
            self.referencia_item, ReferenciaCurriculo
        ):
            raise RegraDeDominioViolada(
                "A sugestão deve referenciar um item tipado do currículo."
            )


@dataclass(frozen=True, slots=True)
class PropostaAdequacaoCurriculoVaga:
    """Agrupa a resposta revisável de uma adequação semântica a uma vaga.

    A proposta registra modelo, versão da política, itens efetivamente usados e
    sugestões únicas, mas não contém operação para gravar mudanças no currículo.
    Ela existe para tornar a assistência auditável e manter a aplicação de cada
    sugestão como uma decisão posterior e explícita do estudante.
    """

    curriculo_id: CurriculoId
    modelo: str
    versao_politica: str
    referencias_utilizadas: tuple[ReferenciaCurriculo, ...]
    sugestoes: tuple[SugestaoAdequacao, ...]

    def __post_init__(self) -> None:
        """Valida metadados, referências e códigos únicos da proposta.

        O método exige identificação tipada do currículo, metadados textuais,
        ao menos uma referência utilizada e sugestões tipadas com códigos não
        repetidos. Ele existe para que a proposta possa ser reproduzida e
        revisada sem depender de payloads brutos do provedor.
        """
        if not isinstance(self.curriculo_id, CurriculoId):
            raise RegraDeDominioViolada("A proposta deve referenciar um currículo.")
        for nome, valor in (("modelo", self.modelo), ("versao_politica", self.versao_politica)):
            if not isinstance(valor, str) or not valor.strip():
                raise RegraDeDominioViolada(f"{nome} deve ser informado.")
        referencias = tuple(self.referencias_utilizadas)
        if not referencias or not all(
            isinstance(referencia, ReferenciaCurriculo) for referencia in referencias
        ):
            raise RegraDeDominioViolada(
                "A proposta deve registrar os itens profissionais utilizados."
            )
        if len(set(referencias)) != len(referencias):
            raise RegraDeDominioViolada("A proposta não pode repetir itens utilizados.")
        sugestoes = tuple(self.sugestoes)
        if not sugestoes or not all(
            isinstance(sugestao, SugestaoAdequacao) for sugestao in sugestoes
        ):
            raise RegraDeDominioViolada("A proposta deve conter sugestões válidas.")
        if len({sugestao.codigo for sugestao in sugestoes}) != len(sugestoes):
            raise RegraDeDominioViolada("A proposta não pode repetir códigos de sugestão.")
        object.__setattr__(self, "referencias_utilizadas", referencias)
        object.__setattr__(self, "sugestoes", sugestoes)
