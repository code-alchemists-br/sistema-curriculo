"""Testa o caso de uso de recomendação do modelo de currículo."""

import unittest
from uuid import UUID

from backend.application.recomendacao_modelo import (
    InformacaoPerfil,
    RecomendacaoModelo,
    RecomendarModeloCurriculo,
)
from backend.domain.modelo_curriculo import ModeloCurriculo

USUARIO = UUID("00000000-0000-0000-0000-0000000000a1")


class LeitorFalso:
    """Substitui a leitura do perfil por uma lista fixa em memória.

    O double registra para quem leu e devolve as informações configuradas.
    Existe para isolar o caso de uso do banco.
    """

    def __init__(self, informacoes: list[InformacaoPerfil]) -> None:
        """Guarda as informações a devolver e prepara o histórico.

        Existe para que cada teste escolha o perfil salvo simulado.
        """
        self._informacoes = informacoes
        self.lidos: list[UUID] = []

    async def informacoes(self, usuario_id: UUID) -> list[InformacaoPerfil]:
        """Registra o usuário e devolve as informações configuradas.

        Existe para conferir que o caso de uso lê o perfil do estudante certo.
        """
        self.lidos.append(usuario_id)
        return list(self._informacoes)


class RecomendadorFalso:
    """Substitui o provedor de IA por uma recomendação fixa em memória.

    O double guarda o perfil recebido. Existe para conferir o que o caso de
    uso enviou à IA sem chamar a rede.
    """

    def __init__(self) -> None:
        """Prepara o histórico de perfis recebidos.

        Existe para que os testes inspecionem a última chamada.
        """
        self.perfis: list[list[InformacaoPerfil]] = []

    async def recomendar(self, perfil: list[InformacaoPerfil]) -> RecomendacaoModelo:
        """Registra o perfil e devolve sempre o modelo moderno.

        Existe para simular uma resposta válida da IA.
        """
        self.perfis.append(perfil)
        return RecomendacaoModelo(
            modelo=ModeloCurriculo.MODERNO, motivo="Perfil técnico.", alternativa=None
        )


class RecomendarModeloCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a composição do perfil e a recusa de perfil vazio.

    Usa leitor e recomendador falsos. Existe para garantir que a IA receba o
    perfil salvo somado aos extras e só seja chamada quando há dados.
    """

    async def test_junta_perfil_salvo_e_extras(self) -> None:
        """Envia à IA o perfil do banco seguido dos dados extras da tela.

        Existe para que o objetivo informado na tela pese na recomendação.
        """
        salvo = [InformacaoPerfil("Formação", "ADS")]
        extra = InformacaoPerfil("Objetivo do currículo", "Estágio")
        leitor, recomendador = LeitorFalso(salvo), RecomendadorFalso()

        resultado = await RecomendarModeloCurriculo(recomendador, leitor).executar(
            USUARIO, [extra]
        )

        self.assertEqual(resultado.modelo, ModeloCurriculo.MODERNO)
        self.assertEqual(leitor.lidos, [USUARIO])
        self.assertEqual(recomendador.perfis, [[salvo[0], extra]])

    async def test_recusa_perfil_vazio_sem_chamar_a_ia(self) -> None:
        """Lança ``ValueError`` quando não há perfil salvo nem extras.

        Existe para não pedir à IA uma recomendação sem base.
        """
        recomendador = RecomendadorFalso()

        with self.assertRaises(ValueError):
            await RecomendarModeloCurriculo(recomendador, LeitorFalso([])).executar(USUARIO)

        self.assertEqual(recomendador.perfis, [])


if __name__ == "__main__":
    unittest.main()
