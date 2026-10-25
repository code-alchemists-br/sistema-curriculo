"""Monta os cabeçalhos HTTP comuns às respostas de download de arquivos.

O módulo gera o ``Content-Disposition`` conforme a RFC 6266 e acrescenta as
proteções de tipo e de cache usadas por todas as rotas que devolvem arquivos
do estudante. Ele existe para que downloads de documentos e de currículos
exportados sigam exatamente as mesmas regras, sem duplicação.
"""

from urllib.parse import quote


def cabecalho_de_download(nome_arquivo: str, nome_alternativo: str = "arquivo") -> str:
    """Monta o valor do cabeçalho ``Content-Disposition`` para baixar o arquivo.

    A função gera um ``filename`` apenas ASCII, sem aspas, como alternativa
    para clientes antigos, e o ``filename*`` com o nome original codificado em
    UTF-8; se nada sobrar em ASCII, usa o nome alternativo. Ela existe para que
    nomes com acento ou aspas cheguem ao navegador sem quebrar o cabeçalho.
    """
    alternativa = (
        nome_arquivo.encode("ascii", "ignore").decode("ascii").replace('"', "")
    ).strip() or nome_alternativo
    return f"attachment; filename=\"{alternativa}\"; filename*=UTF-8''{quote(nome_arquivo)}"


def cabecalhos_de_download(nome_arquivo: str, nome_alternativo: str = "arquivo") -> dict[str, str]:
    """Devolve os cabeçalhos completos de uma resposta de download privada.

    A função combina o ``Content-Disposition`` com ``X-Content-Type-Options:
    nosniff`` e ``Cache-Control: private, no-store``. Ela existe para impedir
    que o navegador reinterprete o tipo do arquivo e que dados pessoais fiquem
    em caches compartilhados.
    """
    return {
        "Content-Disposition": cabecalho_de_download(nome_arquivo, nome_alternativo),
        "X-Content-Type-Options": "nosniff",
        "Cache-Control": "private, no-store",
    }
