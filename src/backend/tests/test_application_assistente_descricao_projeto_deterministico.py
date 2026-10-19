"""Testa a estratégia determinística padrão do assistente de descrição de projeto."""

import socket
import unittest
from unittest.mock import patch
from uuid import UUID

from backend.application import (
    AssistenteDescricaoProjeto,
    AssistenteDescricaoProjetoDeterministico,
    AssistenteDescricaoProjetoEntrada,
    AssistenteDescricaoProjetoSaida,
)
from backend.domain import (
    TAMANHO_MAXIMO_DESCRICAO_PROJETO,
    TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO,
    TAMANHO_MAXIMO_TITULO_PROJETO,
    ProjetoAcademico,
    ProjetoAcademicoId,
    RegraDeDominioViolada,
    UsuarioId,
)


def _entrada(
    titulo: object = "Sistema de Currículos", tecnologias: object = "Python, FastAPI"
) -> AssistenteDescricaoProjetoEntrada:
    """Cria a entrada do assistente com valores padrão válidos.

    A função permite variar título e tecnologias em cada cenário. Ela existe
    para manter os testes focados no comportamento observado.
    """
    return AssistenteDescricaoProjetoEntrada(
        titulo=titulo,  # type: ignore[arg-type]
        tecnologias=tecnologias,  # type: ignore[arg-type]
    )


class AssistenteDescricaoProjetoDeterministicoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a sugestão gerada pela estratégia padrão, sem inteligência artificial.

    Os cenários chamam a estratégia diretamente, sem rede, banco ou relógio. A
    classe existe para proteger o determinismo, o conteúdo e os limites da
    orientação oferecida pelo RF04.
    """

    def setUp(self) -> None:
        """Cria a estratégia sob teste.

        O setup instancia a classe sem dependências. Ele existe para reduzir
        repetição entre os cenários.
        """
        self.assistente = AssistenteDescricaoProjetoDeterministico()

    async def test_cumpre_o_contrato_do_assistente(self) -> None:
        """Implementa a porta e devolve a saída tipada do contrato.

        O teste usa a estratégia como ``AssistenteDescricaoProjeto`` e confere o
        tipo do retorno. Ele existe para garantir que ela seja substituível por
        outras estratégias sem mudar os consumidores.
        """
        assistente: AssistenteDescricaoProjeto = self.assistente

        saida = await assistente.sugerir_descricao(_entrada())

        self.assertIsInstance(saida, AssistenteDescricaoProjetoSaida)

    async def test_mesma_entrada_gera_sempre_a_mesma_sugestao(self) -> None:
        """Produz texto idêntico em chamadas repetidas e em instâncias novas.

        O teste gera a sugestão várias vezes com a mesma entrada. Ele existe
        para garantir a natureza determinística exigida pelo card.
        """
        sugestoes = {
            (await AssistenteDescricaoProjetoDeterministico().sugerir_descricao(_entrada())).descricao
            for _ in range(5)
        }

        self.assertEqual(len(sugestoes), 1)

    async def test_sugestao_inclui_titulo_tecnologias_e_estrutura_de_orientacao(self) -> None:
        """Monta o rascunho com título, tecnologias e os tópicos a completar.

        O teste compara o texto gerado com o esperado. Ele existe para fixar a
        orientação clara e objetiva pedida pelo RF04.
        """
        saida = await self.assistente.sugerir_descricao(_entrada())

        self.assertEqual(
            saida.descricao,
            "Sistema de Currículos é um projeto acadêmico desenvolvido com Python e "
            "FastAPI. Objetivo: [descreva o objetivo do projeto]. Problema resolvido: "
            "[explique o problema ou a necessidade atendida]. Minha contribuição: "
            "[indique suas responsabilidades e decisões]. Resultados: [apresente os "
            "resultados ou aprendizados obtidos].",
        )

    async def test_normaliza_titulo_e_lista_de_tecnologias(self) -> None:
        """Remove espaços extras, vazios e tecnologias repetidas.

        O teste usa título com espaços sobrando e tecnologias separadas por
        vírgula e ponto e vírgula, com itens vazios e repetidos em caixas
        diferentes. Ele existe para que a sugestão liste os itens de forma limpa
        e na ordem informada.
        """
        saida = await self.assistente.sugerir_descricao(
            _entrada(
                titulo="  Sistema   de  Currículos ",
                tecnologias=" Python ;FastAPI,, python ; React ",
            )
        )

        self.assertTrue(
            saida.descricao.startswith(
                "Sistema de Currículos é um projeto acadêmico desenvolvido com "
                "Python, FastAPI e React."
            )
        )

    async def test_tecnologia_unica_e_ausente(self) -> None:
        """Usa a tecnologia sozinha ou o modelo sem tecnologias quando vazio.

        O teste cobre uma tecnologia única e o campo em branco. Ele existe para
        que a sugestão continue útil antes de o estudante informar tecnologias.
        """
        unica = await self.assistente.sugerir_descricao(_entrada(tecnologias="Python"))
        ausente = await self.assistente.sugerir_descricao(_entrada(tecnologias="  ,  "))

        self.assertIn("desenvolvido com Python.", unica.descricao)
        self.assertTrue(
            ausente.descricao.startswith("Sistema de Currículos é um projeto acadêmico. ")
        )
        self.assertNotIn("desenvolvido com", ausente.descricao)

    async def test_entrada_maxima_cabe_na_descricao_do_projeto(self) -> None:
        """Mantém a sugestão dentro do limite e aceitável pelo projeto acadêmico.

        O teste usa título e tecnologias no tamanho máximo do cadastro e cria um
        ``ProjetoAcademico`` com a sugestão. Ele existe para que aceitar a
        sugestão nunca gere erro ao salvar o projeto.
        """
        tecnologias = ", ".join(f"T{indice}" for indice in range(100))[
            :TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO
        ]
        titulo = "A" * TAMANHO_MAXIMO_TITULO_PROJETO

        saida = await self.assistente.sugerir_descricao(
            _entrada(titulo=titulo, tecnologias=tecnologias)
        )

        self.assertLessEqual(len(saida.descricao), TAMANHO_MAXIMO_DESCRICAO_PROJETO)
        projeto = ProjetoAcademico(
            id=ProjetoAcademicoId(UUID(int=1)),
            usuario_id=UsuarioId(UUID(int=2)),
            titulo=titulo,
            descricao=saida.descricao,
            tecnologias=tecnologias,
        )
        self.assertEqual(projeto.descricao, saida.descricao)

    async def test_rejeita_entrada_invalida_de_forma_controlada(self) -> None:
        """Levanta ``RegraDeDominioViolada`` para título ausente ou dados inválidos.

        O teste cobre título vazio, tipos não textuais, caracteres de controle e
        textos acima dos limites do projeto. Ele existe para que a estratégia
        nunca devolva um rascunho quebrado.
        """
        cenarios = {
            "título vazio": _entrada(titulo="   "),
            "título não textual": _entrada(titulo=123),
            "tecnologias não textuais": _entrada(tecnologias=None),
            "controle no título": _entrada(titulo="Sistema\x00Currículos"),
            "título acima do limite": _entrada(titulo="A" * (TAMANHO_MAXIMO_TITULO_PROJETO + 1)),
            "tecnologias acima do limite": _entrada(
                tecnologias="A" * (TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO + 1)
            ),
        }
        for descricao, entrada in cenarios.items():
            with self.subTest(cenario=descricao):
                with self.assertRaises(RegraDeDominioViolada):
                    await self.assistente.sugerir_descricao(entrada)

    async def test_funciona_sem_rede(self) -> None:
        """Gera a sugestão mesmo com qualquer acesso à rede bloqueado.

        O teste substitui a criação de conexões por uma função que falha. Ele
        existe para cobrir o CT-RF04-03: o assistente não depende de serviço
        externo nem de inteligência artificial.
        """

        def bloquear_rede(*_args: object, **_kwargs: object) -> None:
            """Falha imediatamente se alguém tentar abrir uma conexão."""
            raise AssertionError("O assistente não pode acessar a rede.")

        with patch.object(socket, "create_connection", bloquear_rede), patch.object(
            socket.socket, "connect", bloquear_rede
        ):
            saida = await self.assistente.sugerir_descricao(_entrada())

        self.assertIn("Sistema de Currículos", saida.descricao)
