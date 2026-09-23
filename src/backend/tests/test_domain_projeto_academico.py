"""Testa as invariantes da entidade de projeto acadêmico.

Os cenários exercitam somente objetos de domínio e verificam que projetos não
podem ser criados sem textos apresentáveis. Eles existem para manter a regra
próxima do modelo, sem banco, rede ou framework.
"""

from unittest import TestCase
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import ProjetoAcademico
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

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    def test_rejeita_textos_obrigatorios_vazios_ou_nao_textuais(self) -> None:
        """Recusa cada texto obrigatório quando ausente ou de tipo inválido.

        O teste varia um campo por vez entre espaços e inteiro, observando a
        falha de domínio. Ele existe para assegurar que a entidade não aceite
        conteúdo que não possa ser apresentado no currículo.
        """
        for campo in ("titulo", "descricao", "tecnologias"):
            for valor in ("   ", 1):
                with self.subTest(campo=campo, valor=valor):
                    dados = {
                        "titulo": "Sistema Currículo",
                        "descricao": "Organiza informações acadêmicas.",
                        "tecnologias": "Python, FastAPI",
                    }
                    dados[campo] = valor

                    with self.assertRaises(RegraDeDominioViolada):
                        self._criar_projeto(**dados)

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
