"""Testa a orquestração interna da recomendação de modelo de currículo."""

import unittest
from uuid import uuid4

from backend.application.recomendacao_modelo_curriculo import (
    RecomendarModeloCurriculo,
    RecomendarModeloCurriculoEntrada,
)
from backend.application.versao_curriculo import CurriculoNaoEncontrado
from backend.domain import (
    Curriculo,
    CurriculoId,
    ModeloCurriculo,
    ObjetivoCurriculo,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261102-235645-adequacao-semantica-gpt-nano-v003.md#v003


class RepositorioCurriculoStub:
    """Substitui a leitura de versões por uma resposta controlada em memória.

    O double devolve apenas a versão configurada para sua identidade e registra
    consultas, sem banco nem adapter produtivo. Ele existe para isolar a regra
    de propriedade do caso de uso de recomendação.
    """

    def __init__(self, curriculo: Curriculo | None) -> None:
        """Guarda a versão de teste e inicia o histórico de consultas.

        O construtor recebe presença ou ausência previamente definida pelo
        cenário. Ele existe para tornar verificável o fluxo sem infraestrutura.
        """
        self.curriculo = curriculo
        self.consultas: list[CurriculoId] = []

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Registra a consulta e devolve a versão apenas para o ID correspondente.

        O método simula a porta assíncrona sem fazer I/O e representa ausência
        quando a identidade não coincide. Ele existe para testar a ocultação de
        currículos inexistentes ou alheios.
        """
        self.consultas.append(curriculo_id)
        if self.curriculo is not None and self.curriculo.id == curriculo_id:
            return self.curriculo
        return None


def _curriculo(usuario_id: UsuarioId) -> Curriculo:
    """Cria uma versão própria válida para os cenários de orquestração.

    A função instancia o agregado inteiramente em memória, com layout existente
    e sem itens. Ela existe para os testes controlarem propriedade sem banco ou
    efeitos de escrita.
    """
    return Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id,
        titulo_versao="Tecnologia",
        layout=ModeloCurriculo.CLASSICO.value,
        is_public=False,
    )


class RecomendarModeloCurriculoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica propriedade, recomendação e ausência de escrita no caso de uso.

    Os cenários usam somente um double da porta de currículos e a política pura
    de domínio. A classe existe para garantir que a recomendação seja leitura
    autorizada, sem alterar layout ou persistir objetivo.
    """

    async def test_recomenda_para_versao_propria_sem_alterar_agregado(self) -> None:
        """Devolve orientação de tecnologia sem modificar o layout da versão.

        O cenário usa uma versão pertencente ao solicitante e compara seu estado
        antes e depois da execução. Ele existe para assegurar que recomendar não
        aplica automaticamente um modelo ao currículo.
        """
        usuario_id = UsuarioId(uuid4())
        curriculo = _curriculo(usuario_id)
        repositorio = RepositorioCurriculoStub(curriculo)
        caso_de_uso = RecomendarModeloCurriculo(repositorio)

        recomendacao = await caso_de_uso.executar(
            RecomendarModeloCurriculoEntrada(
                usuario_id=usuario_id,
                curriculo_id=curriculo.id,
                objetivo=ObjetivoCurriculo.TECNOLOGIA,
            )
        )

        self.assertEqual(recomendacao.modelo_recomendado, ModeloCurriculo.MODERNO)
        self.assertEqual(curriculo.layout, ModeloCurriculo.CLASSICO.value)
        self.assertEqual(repositorio.consultas, [curriculo.id])

    async def test_oculta_curriculo_alheio_sem_produzir_recomendacao(self) -> None:
        """Recusa a consulta de uma versão cujo proprietário é outro estudante.

        O cenário informa uma identidade solicitante distinta e espera a mesma
        falha usada para ausência. Ele existe para impedir que a recomendação
        revele a existência ou a apresentação de currículos de terceiros.
        """
        dono = UsuarioId(uuid4())
        curriculo = _curriculo(dono)
        caso_de_uso = RecomendarModeloCurriculo(RepositorioCurriculoStub(curriculo))

        with self.assertRaises(CurriculoNaoEncontrado):
            await caso_de_uso.executar(
                RecomendarModeloCurriculoEntrada(
                    usuario_id=UsuarioId(uuid4()),
                    curriculo_id=curriculo.id,
                    objetivo=ObjetivoCurriculo.OUTRO,
                )
            )
