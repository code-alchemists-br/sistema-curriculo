"""Define a revisão de campos obrigatórios de uma versão de currículo.

O módulo reúne o resultado da revisão, formado por pendências com código,
seção, mensagem e severidade, e a regra que confere se o conteúdo da versão
cobre as seções obrigatórias, sem conhecer banco, rotas ou formatos de saída.
Ele existe para manter em um único ponto do domínio a decisão do que falta para
um currículo estar completo.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
from backend.domain.itens_perfil import (
    Competencia,
    ExperienciaProfissional,
    FormacaoAcademica,
    Idioma,
    ProjetoAcademico,
)
from backend.domain.usuario import Usuario


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
class SecaoRevisao(str, Enum):
    """Identifica a seção do currículo a que uma pendência se refere.

    Os valores textuais coincidem com os identificadores de seção que o
    front-end já usa na validação final, acrescidos de projetos e idiomas. A
    enumeração existe para que a seção seja um vocabulário fechado e para que a
    ordem de declaração defina a ordem de apresentação das pendências.
    """

    DADOS_PESSOAIS = "dados-pessoais"
    FORMACAO_ACADEMICA = "formacao-academica"
    EXPERIENCIAS_PROFISSIONAIS = "experiencias-profissionais"
    COMPETENCIAS = "competencias"
    PROJETOS_ACADEMICOS = "projetos-academicos"
    IDIOMAS = "idiomas"


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
class SeveridadePendencia(str, Enum):
    """Classifica uma pendência como erro, que reprova, ou aviso, que só recomenda.

    A enumeração distingue o que impede o currículo de ser considerado completo
    do que é apenas uma sugestão de melhoria. Ela existe para que o cliente trate
    cada caso de forma diferente sem interpretar o texto da mensagem.
    """

    ERRO = "erro"
    AVISO = "aviso"


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
@dataclass(frozen=True, slots=True)
class PendenciaRevisao:
    """Representa uma informação que falta no currículo revisado.

    A pendência reúne um código estável, a seção afetada, uma mensagem legível e
    a severidade, sem referenciar entidades. Ela existe para dar ao estudante e
    ao front-end um contrato simples do que precisa ser corrigido.
    """

    codigo: str
    secao: SecaoRevisao
    mensagem: str
    severidade: SeveridadePendencia


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
@dataclass(frozen=True, slots=True)
class ResultadoRevisao:
    """Agrupa as pendências encontradas na revisão de uma versão de currículo.

    O resultado guarda as pendências em ordem determinística e deriva delas se o
    currículo está aprovado. Ele existe para que quem consome a revisão tenha um
    único objeto com o veredito e os motivos.
    """

    pendencias: tuple[PendenciaRevisao, ...]

    @property
    def aprovado(self) -> bool:
        """Informa se a revisão não encontrou nenhuma pendência de erro.

        A propriedade percorre as pendências e só reprova quando alguma tem
        severidade de erro; avisos não reprovam. Ela existe para que o veredito
        seja derivado das pendências, e não guardado à parte.
        """
        return all(
            pendencia.severidade is not SeveridadePendencia.ERRO
            for pendencia in self.pendencias
        )


_ORDEM_DAS_SECOES = tuple(SecaoRevisao)


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
def _chave_de_ordem(pendencia: PendenciaRevisao) -> tuple[int, int, str]:
    """Calcula a chave que ordena as pendências de forma previsível.

    A chave coloca os erros antes dos avisos, depois segue a ordem de declaração
    das seções e, por fim, o código da pendência. Ela existe para que a mesma
    revisão sempre produza a mesma lista, independentemente da ordem das regras.
    """
    eh_erro = pendencia.severidade is SeveridadePendencia.ERRO
    return (
        0 if eh_erro else 1,
        _ORDEM_DAS_SECOES.index(pendencia.secao),
        pendencia.codigo,
    )


# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
def revisar_curriculo(
    usuario: Usuario,
    formacoes: Sequence[FormacaoAcademica],
    experiencias: Sequence[ExperienciaProfissional],
    projetos: Sequence[ProjetoAcademico],
    competencias: Sequence[Competencia],
    idiomas: Sequence[Idioma],
) -> ResultadoRevisao:
    """Confere se o conteúdo da versão cobre as seções obrigatórias do currículo.

    A função verifica se o estudante tem dados de contato e se cada seção
    recebida tem ao menos um item: formação, experiência e competência geram erro
    quando vazias, e projetos e idiomas geram apenas aviso. O resultado vem
    ordenado. Ela existe para concentrar no domínio a regra do que falta, sem
    depender de banco, rota ou formato de saída; os campos de cada item já são
    garantidos pelas próprias entidades.
    """
    pendencias: list[PendenciaRevisao] = []

    if usuario.dados_contato is None:
        pendencias.append(
            PendenciaRevisao(
                codigo="CONTATO_AUSENTE",
                secao=SecaoRevisao.DADOS_PESSOAIS,
                mensagem="Informe o endereço e ao menos um telefone de contato.",
                severidade=SeveridadePendencia.ERRO,
            )
        )

    exigencias = (
        (
            formacoes,
            "FORMACAO_AUSENTE",
            SecaoRevisao.FORMACAO_ACADEMICA,
            SeveridadePendencia.ERRO,
            "Inclua ao menos uma formação acadêmica na versão.",
        ),
        (
            experiencias,
            "EXPERIENCIA_AUSENTE",
            SecaoRevisao.EXPERIENCIAS_PROFISSIONAIS,
            SeveridadePendencia.ERRO,
            "Inclua ao menos uma experiência profissional na versão.",
        ),
        (
            competencias,
            "COMPETENCIA_AUSENTE",
            SecaoRevisao.COMPETENCIAS,
            SeveridadePendencia.ERRO,
            "Inclua ao menos uma competência na versão.",
        ),
        (
            projetos,
            "PROJETO_AUSENTE",
            SecaoRevisao.PROJETOS_ACADEMICOS,
            SeveridadePendencia.AVISO,
            "Considere incluir um projeto acadêmico na versão.",
        ),
        (
            idiomas,
            "IDIOMA_AUSENTE",
            SecaoRevisao.IDIOMAS,
            SeveridadePendencia.AVISO,
            "Considere incluir um idioma na versão.",
        ),
    )
    for itens, codigo, secao, severidade, mensagem in exigencias:
        if len(itens) == 0:
            pendencias.append(
                PendenciaRevisao(
                    codigo=codigo,
                    secao=secao,
                    mensagem=mensagem,
                    severidade=severidade,
                )
            )

    return ResultadoRevisao(pendencias=tuple(sorted(pendencias, key=_chave_de_ordem)))