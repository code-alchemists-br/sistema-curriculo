"""Implementa a estratégia determinística padrão do assistente de descrição.

O módulo gera a sugestão de descrição de um projeto acadêmico a partir de um
modelo de texto fixo, preenchido com o título e as tecnologias informados, sem
rede, sem aleatoriedade e sem inteligência artificial. Ele existe para atender
ao RF04 e ao CT-RF04-03 com uma orientação sempre disponível, mantendo a porta
``AssistenteDescricaoProjeto`` livre para estratégias externas no futuro.
"""

import re
from unicodedata import category

from backend.application.assistente_descricao_projeto import (
    AssistenteDescricaoProjetoEntrada,
    AssistenteDescricaoProjetoSaida,
)
from backend.domain import (
    TAMANHO_MAXIMO_DESCRICAO_PROJETO,
    TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO,
    TAMANHO_MAXIMO_TITULO_PROJETO,
    RegraDeDominioViolada,
)

SEPARADORES_TECNOLOGIAS = re.compile(r"[,;]")

MODELO_DESCRICAO_COM_TECNOLOGIAS = (
    "{titulo} é um projeto acadêmico desenvolvido com {tecnologias}. "
    "Objetivo: [descreva o objetivo do projeto]. "
    "Problema resolvido: [explique o problema ou a necessidade atendida]. "
    "Minha contribuição: [indique suas responsabilidades e decisões]. "
    "Resultados: [apresente os resultados ou aprendizados obtidos]."
)

MODELO_DESCRICAO_SEM_TECNOLOGIAS = (
    "{titulo} é um projeto acadêmico. "
    "Objetivo: [descreva o objetivo do projeto]. "
    "Problema resolvido: [explique o problema ou a necessidade atendida]. "
    "Minha contribuição: [indique suas responsabilidades e decisões]. "
    "Resultados: [apresente os resultados ou aprendizados obtidos]."
)


class AssistenteDescricaoProjetoDeterministico:
    """Sugere a descrição de um projeto por modelo fixo, sem inteligência artificial.

    A estratégia normaliza título e tecnologias, escolhe o modelo com ou sem
    tecnologias e devolve um rascunho estruturado em objetivo, problema,
    contribuição e resultados, com marcadores entre colchetes para o estudante
    completar. É a estratégia padrão do assistente: a mesma entrada produz
    sempre a mesma saída e cabe no limite de descrição do projeto acadêmico.
    Ela existe para oferecer orientação clara e objetiva sem depender de
    serviço externo.
    """

    async def sugerir_descricao(
        self,
        entrada: AssistenteDescricaoProjetoEntrada,
    ) -> AssistenteDescricaoProjetoSaida:
        """Monta a sugestão de descrição a partir do título e das tecnologias.

        O método valida e normaliza os dois campos, formata a lista de
        tecnologias em linguagem natural e preenche o modelo correspondente;
        entradas inválidas levantam ``RegraDeDominioViolada``. Ele existe para
        implementar a porta do assistente de forma determinística e verificável.
        """
        titulo = _normalizar_titulo(entrada.titulo)
        tecnologias = _normalizar_tecnologias(entrada.tecnologias)
        if tecnologias:
            descricao = MODELO_DESCRICAO_COM_TECNOLOGIAS.format(
                titulo=titulo, tecnologias=_juntar_em_lista(tecnologias)
            )
        else:
            descricao = MODELO_DESCRICAO_SEM_TECNOLOGIAS.format(titulo=titulo)
        if len(descricao) > TAMANHO_MAXIMO_DESCRICAO_PROJETO:
            raise RegraDeDominioViolada(
                "A sugestão de descrição excede o tamanho máximo do projeto."
            )
        return AssistenteDescricaoProjetoSaida(descricao=descricao)


def _validar_texto(valor: object, campo: str, tamanho_maximo: int) -> str:
    """Valida tipo, caracteres de controle e tamanho de um campo da entrada.

    A função exige texto, recusa caracteres de controle, colapsa espaços
    repetidos e mede o resultado contra o limite do projeto acadêmico. Ela
    existe para que a sugestão só seja gerada a partir de dados aceitáveis
    pelo cadastro de projeto.
    """
    if not isinstance(valor, str):
        raise RegraDeDominioViolada(f"O campo {campo} do assistente deve ser texto.")
    if any(category(caractere) == "Cc" for caractere in valor):
        raise RegraDeDominioViolada(
            f"O campo {campo} do assistente não pode conter caracteres de controle."
        )
    normalizado = " ".join(valor.split())
    if len(normalizado) > tamanho_maximo:
        raise RegraDeDominioViolada(
            f"O campo {campo} do assistente deve ter no máximo {tamanho_maximo} caracteres."
        )
    return normalizado


def _normalizar_titulo(titulo: object) -> str:
    """Normaliza o título e exige que ele esteja preenchido.

    A função reaproveita a validação comum e recusa título vazio, que deixaria
    a sugestão sem identificação do projeto. Ela existe para garantir que todo
    rascunho comece pelo nome do projeto.
    """
    normalizado = _validar_texto(titulo, "título", TAMANHO_MAXIMO_TITULO_PROJETO)
    if not normalizado:
        raise RegraDeDominioViolada(
            "O título é obrigatório para sugerir a descrição do projeto."
        )
    return normalizado


def _normalizar_tecnologias(tecnologias: object) -> list[str]:
    """Separa as tecnologias em itens únicos, na ordem em que foram informadas.

    A função divide o texto por vírgula ou ponto e vírgula, apara cada item,
    descarta vazios e remove repetições sem diferenciar caixa, mantendo a
    primeira grafia. Ela existe para que a sugestão liste as tecnologias de
    forma limpa e estável.
    """
    texto = _validar_texto(
        tecnologias, "tecnologias", TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO
    )
    vistas: set[str] = set()
    itens: list[str] = []
    for parte in SEPARADORES_TECNOLOGIAS.split(texto):
        item = parte.strip()
        chave = item.casefold()
        if item and chave not in vistas:
            vistas.add(chave)
            itens.append(item)
    return itens


def _juntar_em_lista(itens: list[str]) -> str:
    """Junta itens em uma lista em português, com "e" antes do último.

    A função devolve o item único, "A e B" para dois itens e "A, B e C" para
    três ou mais. Ela existe para que a frase gerada soe natural ao leitor do
    currículo.
    """
    if len(itens) == 1:
        return itens[0]
    return f"{', '.join(itens[:-1])} e {itens[-1]}"
