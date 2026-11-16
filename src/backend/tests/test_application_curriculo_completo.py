"""Testa os casos de uso de leitura e substituição do currículo completo."""

import unittest
from datetime import date, timedelta
from uuid import UUID

from backend.application.curriculo_completo import (
    CompetenciaItem,
    CurriculoCompleto,
    CurriculoNaoEncontrado,
    CursoItem,
    DadosPessoaisSalvos,
    ExperienciaItem,
    FormacaoItem,
    GerenciarCurriculoCompleto,
    RepositorioCurriculoCompleto,
    SecaoSubstituivel,
)
from backend.domain import (
    CategoriaCompetencia,
    Competencia,
    Curso,
    ExperienciaProfissional,
    FormacaoAcademica,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import NivelFormacaoAcademica, StatusFormacaoAcademica
from backend.domain.modelo_curriculo import ModeloCurriculo

USUARIO = UUID("00000000-0000-0000-0000-0000000000b1")


class RepositorioFalso(RepositorioCurriculoCompleto):
    """Substitui a persistência do currículo por memória.

    O double guarda as trocas e o modelo recebidos e devolve o currículo
    configurado na leitura. Existe para testar o caso de uso sem banco.
    """

    def __init__(self, curriculo: CurriculoCompleto | None = None) -> None:
        """Guarda o currículo da leitura e prepara os históricos.

        Existe para que cada teste escolha o estado salvo simulado.
        """
        self.curriculo = curriculo
        self.trocas: list[tuple] = []
        self.modelos: list[tuple] = []

    async def ler(self, usuario_id: UUID) -> CurriculoCompleto | None:
        """Devolve o currículo configurado, ou ``None`` para conta inexistente.

        Existe para simular a leitura do banco.
        """
        return self.curriculo

    async def substituir(self, usuario_id, secao, entidades, curriculo_lattes=None) -> None:
        """Registra a troca pedida pelo caso de uso.

        Existe para que os testes inspecionem as entidades que seriam gravadas.
        """
        self.trocas.append((usuario_id, secao, entidades, curriculo_lattes))

    async def salvar_modelo(self, usuario_id: UUID, modelo: ModeloCurriculo) -> None:
        """Registra o modelo pedido pelo caso de uso.

        Existe para conferir que a escolha chega à persistência.
        """
        self.modelos.append((usuario_id, modelo))


class GerenciarCurriculoCompletoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica leitura, substituição por seção e gravação do modelo.

    Usa um repositório em memória. Existe para garantir que os itens passem
    pelas entidades do domínio antes de qualquer gravação.
    """

    async def test_consultar_devolve_o_curriculo_salvo(self) -> None:
        """Devolve o currículo lido do repositório.

        Existe para que o frontend receba o que está no banco.
        """
        salvo = CurriculoCompleto(dados_pessoais=DadosPessoaisSalvos(nome="Ana", email="a@x.com"))

        resultado = await GerenciarCurriculoCompleto(RepositorioFalso(salvo)).consultar(USUARIO)

        self.assertIs(resultado, salvo)

    async def test_consultar_conta_inexistente_lanca_erro(self) -> None:
        """Lança ``CurriculoNaoEncontrado`` quando a conta não existe.

        Existe para não devolver um currículo vazio a uma conta excluída.
        """
        with self.assertRaises(CurriculoNaoEncontrado):
            await GerenciarCurriculoCompleto(RepositorioFalso(None)).consultar(USUARIO)

    async def test_substitui_secao_com_entidades_do_dominio(self) -> None:
        """Converte cada item na entidade da seção, com dono e IDs novos.

        Existe para que toda gravação passe pelas regras do domínio.
        """
        repositorio = RepositorioFalso()
        itens = [
            FormacaoItem(
                instituicao=" Fatec ",
                curso="ADS",
                nivel=NivelFormacaoAcademica.TECNOLOGO,
                status=StatusFormacaoAcademica.EM_ANDAMENTO,
                data_inicio=date(2024, 2, 1),
            ),
            FormacaoItem(
                instituicao="USP",
                curso="Computação",
                nivel=NivelFormacaoAcademica.GRADUACAO,
                status=StatusFormacaoAcademica.CONCLUIDO,
                data_inicio=date(2019, 2, 1),
                data_fim=date(2023, 12, 1),
            ),
        ]

        await GerenciarCurriculoCompleto(repositorio).substituir_secao(
            USUARIO, SecaoSubstituivel.FORMACOES, itens, "http://lattes.cnpq.br/1"
        )

        usuario, secao, entidades, lattes = repositorio.trocas[0]
        self.assertEqual((usuario, secao, lattes), (USUARIO, SecaoSubstituivel.FORMACOES, "http://lattes.cnpq.br/1"))
        self.assertTrue(all(isinstance(e, FormacaoAcademica) for e in entidades))
        self.assertEqual(entidades[0].instituicao, "Fatec")
        self.assertNotEqual(entidades[0].id, entidades[1].id)
        self.assertTrue(all(e.usuario_id.valor == USUARIO for e in entidades))

    async def test_converte_cada_secao_na_entidade_certa(self) -> None:
        """Usa a entidade correspondente para experiências, competências e cursos.

        Existe para garantir o mapeamento seção → entidade.
        """
        repositorio = RepositorioFalso()
        caso = GerenciarCurriculoCompleto(repositorio)

        await caso.substituir_secao(
            USUARIO,
            SecaoSubstituivel.EXPERIENCIAS,
            [ExperienciaItem(empresa="X", cargo="Dev", descricao="Fiz APIs.", data_inicio=date(2024, 1, 1))],
        )
        await caso.substituir_secao(
            USUARIO,
            SecaoSubstituivel.COMPETENCIAS,
            [CompetenciaItem(categoria=CategoriaCompetencia.TECNICA, descricao="Python")],
        )
        await caso.substituir_secao(
            USUARIO, SecaoSubstituivel.CURSOS, [CursoItem(nome="Python", instituicao="Alura", carga_horaria=40)]
        )

        tipos = [type(troca[2][0]) for troca in repositorio.trocas]
        self.assertEqual(tipos, [ExperienciaProfissional, Competencia, Curso])

    async def test_item_invalido_impede_toda_a_troca(self) -> None:
        """Não grava nada quando um item viola uma regra do domínio.

        Usa uma experiência com início no futuro. Existe para que a seção nunca
        fique gravada pela metade.
        """
        repositorio = RepositorioFalso()
        futuro = date.today() + timedelta(days=30)

        with self.assertRaises(RegraDeDominioViolada):
            await GerenciarCurriculoCompleto(repositorio).substituir_secao(
                USUARIO,
                SecaoSubstituivel.EXPERIENCIAS,
                [ExperienciaItem(empresa="X", cargo="Dev", descricao="Fiz.", data_inicio=futuro)],
            )

        self.assertEqual(repositorio.trocas, [])

    async def test_lista_vazia_limpa_a_secao(self) -> None:
        """Repassa uma lista vazia para remover todos os itens da seção.

        Existe para que apagar todos os itens na tela também apague no banco.
        """
        repositorio = RepositorioFalso()

        await GerenciarCurriculoCompleto(repositorio).substituir_secao(
            USUARIO, SecaoSubstituivel.IDIOMAS, []
        )

        self.assertEqual(repositorio.trocas, [(USUARIO, SecaoSubstituivel.IDIOMAS, [], None)])

    async def test_salvar_modelo_delega_ao_repositorio(self) -> None:
        """Encaminha o modelo escolhido ao repositório.

        Existe para que a escolha do modelo seja persistida.
        """
        repositorio = RepositorioFalso()

        await GerenciarCurriculoCompleto(repositorio).salvar_modelo(USUARIO, ModeloCurriculo.MODERNO)

        self.assertEqual(repositorio.modelos, [(USUARIO, ModeloCurriculo.MODERNO)])


if __name__ == "__main__":
    unittest.main()
