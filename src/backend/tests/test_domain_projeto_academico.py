"""Testa as invariantes da entidade de projeto acadêmico.

Os cenários exercitam somente objetos de domínio e verificam que projetos não
podem ser criados sem textos apresentáveis. Eles existem para manter a regra
próxima do modelo, sem banco, rede ou framework.
"""

from unittest import TestCase
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import (
    TAMANHO_MAXIMO_DESCRICAO_PROJETO,
    TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO,
    TAMANHO_MAXIMO_TITULO_PROJETO,
    TAMANHO_MINIMO_TEXTO_PROJETO,
    ProjetoAcademico,
)
from backend.domain.value_objects import ProjetoAcademicoId, UsuarioId


# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
class ProjetoAcademicoTestCase(TestCase):
    """Verifica invariantes de criação de projetos acadêmicos no domínio.

    A suíte constrói identificadores determinísticos e instancia a entidade
    diretamente, sem recursos externos. Ela existe para proteger o conteúdo
    mínimo que será apresentado e reutilizado em currículos.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    def test_cria_projeto_com_textos_obrigatorios_preenchidos(self) -> None:
        """Aceita um projeto quando todos os textos essenciais existem.

        O cenário constrói a entidade com dados válidos e verifica a preservação
        dos campos. Ele existe para documentar o caminho de sucesso da regra.
        """
        projeto = self._criar_projeto()

        self.assertEqual(projeto.titulo, "Sistema Currículo")
        self.assertEqual(projeto.descricao, "Organiza informações acadêmicas.")
        self.assertEqual(projeto.tecnologias, "Python, FastAPI")

    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    def test_normaliza_textos_com_strip_antes_de_devolver_a_entidade(self) -> None:
        """Remove espaços externos dos três campos aceitos.

        O cenário cria uma entidade com bordas contendo espaços e compara os
        valores armazenados. Ele existe para garantir que só texto canônico
        atravesse a fronteira do domínio e chegue à persistência.
        """
        projeto = self._criar_projeto(
            titulo="  Sistema Currículo  ",
            descricao="  Organiza informações acadêmicas.  ",
            tecnologias="  Python, FastAPI  ",
        )

        self.assertEqual(projeto.titulo, "Sistema Currículo")
        self.assertEqual(projeto.descricao, "Organiza informações acadêmicas.")
        self.assertEqual(projeto.tecnologias, "Python, FastAPI")

    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    def test_aceita_tamanho_minimo_e_limite_maximo_de_cada_campo(self) -> None:
        """Aceita o mínimo e o máximo definidos para cada texto.

        O teste varia um campo por vez nos comprimentos de fronteira e confirma
        que a entidade conserva o valor. Ele existe para impedir divergência
        dos limites públicos entre os três atributos.
        """
        limites = {
            "titulo": TAMANHO_MAXIMO_TITULO_PROJETO,
            "descricao": TAMANHO_MAXIMO_DESCRICAO_PROJETO,
            "tecnologias": TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO,
        }
        for campo, tamanho_maximo in limites.items():
            for tamanho in (TAMANHO_MINIMO_TEXTO_PROJETO, tamanho_maximo):
                with self.subTest(campo=campo, tamanho=tamanho):
                    dados = self._dados_validos()
                    dados[campo] = "x" * tamanho

                    projeto = self._criar_projeto(**dados)

                    self.assertEqual(getattr(projeto, campo), "x" * tamanho)

    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    def test_rejeita_tamanho_acima_do_limite_de_cada_campo(self) -> None:
        """Recusa textos que excedam o máximo específico de cada atributo.

        O cenário testa um caractere além de cada limite de Domain. Ele existe
        para evitar que entradas maiores sigam até a gravação do projeto.
        """
        limites = {
            "titulo": TAMANHO_MAXIMO_TITULO_PROJETO,
            "descricao": TAMANHO_MAXIMO_DESCRICAO_PROJETO,
            "tecnologias": TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO,
        }
        for campo, tamanho_maximo in limites.items():
            with self.subTest(campo=campo):
                dados = self._dados_validos()
                dados[campo] = "x" * (tamanho_maximo + 1)

                with self.assertRaises(RegraDeDominioViolada):
                    self._criar_projeto(**dados)

    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    def test_rejeita_valor_vazio_ou_composto_somente_por_espacos(self) -> None:
        """Recusa textos que ficam vazios depois de remover espaços externos.

        O teste aplica string vazia e espaços a cada campo obrigatório. Ele
        existe para garantir o mínimo de conteúdo apresentável no projeto.
        """
        for campo in ("titulo", "descricao", "tecnologias"):
            for valor in ("", "   "):
                with self.subTest(campo=campo, valor=repr(valor)):
                    dados = self._dados_validos()
                    dados[campo] = valor

                    with self.assertRaises(RegraDeDominioViolada):
                        self._criar_projeto(**dados)

    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    def test_rejeita_caracteres_de_controle_unicode_em_cada_campo(self) -> None:
        """Recusa qualquer texto que contenha caractere Unicode categoria Cc.

        O cenário injeta um controle dentro de cada texto e observa a falha de
        domínio. Ele existe para impedir conteúdo de controle no perfil/currículo.
        """
        for campo in ("titulo", "descricao", "tecnologias"):
            with self.subTest(campo=campo):
                dados = self._dados_validos()
                dados[campo] = "válido\x85"

                with self.assertRaises(RegraDeDominioViolada):
                    self._criar_projeto(**dados)

    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    def test_rejeita_tipo_diferente_de_texto_em_cada_campo(self) -> None:
        """Recusa valores que não sejam strings nos campos de projeto.

        O teste substitui cada campo por um inteiro e observa a exceção de
        domínio. Ele existe para manter os atributos tipados no modelo.
        """
        for campo in ("titulo", "descricao", "tecnologias"):
            with self.subTest(campo=campo):
                dados = self._dados_validos()
                dados[campo] = 1

                with self.assertRaises(RegraDeDominioViolada):
                    self._criar_projeto(**dados)

    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    def _dados_validos(self) -> dict[str, str]:
        """Devolve um conjunto mutável de textos válidos para os cenários.

        O helper prepara os três atributos obrigatórios com valores curtos e
        estáveis. Ele existe para que cada teste altere somente o campo sob
        observação.
        """
        return {
            "titulo": "Sistema Currículo",
            "descricao": "Organiza informações acadêmicas.",
            "tecnologias": "Python, FastAPI",
        }

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    def _criar_projeto(
        self,
        titulo: str = "Sistema Currículo",
        descricao: str = "Organiza informações acadêmicas.",
        tecnologias: str = "Python, FastAPI",
    ) -> ProjetoAcademico:
        """Monta um projeto válido com identificadores determinísticos.

        O auxiliar centraliza dados estáveis e permite variar um texto por vez.
        Ele existe para manter os cenários focados na invariante observada.
        """
        return ProjetoAcademico(
            id=ProjetoAcademicoId(UUID("30000000-0000-0000-0000-000000000001")),
            usuario_id=UsuarioId(UUID("30000000-0000-0000-0000-000000000002")),
            titulo=titulo,
            descricao=descricao,
            tecnologias=tecnologias,
        )
