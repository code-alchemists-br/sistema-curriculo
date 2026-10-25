"""Testa unitariamente a consulta paginada de associações currículo-vaga."""

import unittest
from uuid import uuid4

from backend.application import (
    ListarAssociacoesCurriculoVaga,
    ListarAssociacoesCurriculoVagaEntrada,
)
from backend.domain import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
    CurriculoId,
    UsuarioId,
    VagaId,
)


# Proveniência: decision-analysis prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md#v001
class RepositorioAssociacaoConsultaStub:
    """Substitui o port de consulta por resultados e registros em memória.

    O stub devolve a página configurada e registra os argumentos recebidos. Ele
    existe para verificar a orquestração da Application sem persistência real.
    """

    def __init__(self, resultado: tuple[AssociacaoCurriculoVaga, ...] = ()) -> None:
        """Prepara o resultado de teste e o histórico de consultas.

        O construtor conserva a tupla fornecida e inicia um histórico vazio. Ele
        existe para tornar observáveis delegação e retorno do caso de uso.
        """
        self._resultado = resultado
        self.consultas: list[tuple[UsuarioId, int, int]] = []

    async def listar_por_usuario(
        self, usuario_id: UsuarioId, *, offset: int, limit: int
    ) -> tuple[AssociacaoCurriculoVaga, ...]:
        """Registra a consulta e devolve a página configurada.

        A operação não executa I/O nem filtra dados, pois seu propósito é
        substituir a fronteira externa. Ela existe para testar os argumentos
        encaminhados e o resultado entregue pela Application.
        """
        self.consultas.append((usuario_id, offset, limit))
        return self._resultado


# Proveniência: decision-analysis prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md#v001
class ListarAssociacoesCurriculoVagaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica validação e delegação da consulta em isolamento.

    A classe substitui o repository por um stub em memória e usa agregados reais.
    Ela existe para proteger o contrato da Application sem abrir banco ou API.
    """

    async def test_encaminha_usuario_e_parametros_e_retorna_agregados(self) -> None:
        """Confirma a delegação de uma página válida e o retorno do domínio.

        O teste configura agregados e compara identidade, argumentos e resultado.
        Ele existe para provar que o caso de uso encaminha o escopo do estudante
        e não transforma agregados em DTOs de transporte.
        """
        usuario_id = UsuarioId(uuid4())
        primeiro = AssociacaoCurriculoVaga(
            CurriculoId(uuid4()),
            VagaId("vaga-1"),
            (ClassificacaoAssociacao.INTERESSE,),
        )
        segundo = AssociacaoCurriculoVaga(
            CurriculoId(uuid4()),
            VagaId("vaga-2"),
            (ClassificacaoAssociacao.COMPATIBILIDADE,),
        )
        pagina = (primeiro, segundo)
        repositorio = RepositorioAssociacaoConsultaStub(pagina)

        resultado = await ListarAssociacoesCurriculoVaga(repositorio).executar(
            ListarAssociacoesCurriculoVagaEntrada(
                usuario_id=usuario_id,
                offset=20,
                limit=10,
            )
        )

        self.assertEqual(resultado, pagina)
        self.assertEqual(repositorio.consultas, [(usuario_id, 20, 10)])

    async def test_retorna_tupla_vazia_quando_nao_houver_associacoes(self) -> None:
        """Confirma que resultado vazio permanece uma página vazia.

        O stub devolve a tupla vazia sem erro. O teste existe para manter explícito
        o resultado de consulta válida sem associações.
        """
        repositorio = RepositorioAssociacaoConsultaStub()

        resultado = await ListarAssociacoesCurriculoVaga(repositorio).executar(
            ListarAssociacoesCurriculoVagaEntrada(
                usuario_id=UsuarioId(uuid4()),
                offset=0,
                limit=10,
            )
        )

        self.assertEqual(resultado, ())
        self.assertEqual(len(repositorio.consultas), 1)

    def test_rejeita_offset_invalido(self) -> None:
        """Confirma que offset deve ser inteiro não negativo.

        O teste cobre negativos, bool, número fracionário e texto antes de
        qualquer chamada ao port. Ele existe para impedir páginas ambíguas.
        """
        for offset in (-1, True, 1.5, "1"):
            with (
                self.subTest(offset=offset),
                self.assertRaisesRegex(ValueError, "offset"),
            ):
                ListarAssociacoesCurriculoVagaEntrada(
                    usuario_id=UsuarioId(uuid4()),
                    offset=offset,  # type: ignore[arg-type]
                    limit=10,
                )

    def test_rejeita_limite_invalido(self) -> None:
        """Confirma que limit deve ser inteiro estritamente positivo.

        O teste cobre zero, negativo, bool, número fracionário e texto. Ele
        existe para rejeitar entradas que não representem tamanho de página.
        """
        for limit in (0, -1, True, 1.5, "10"):
            with self.subTest(limit=limit), self.assertRaisesRegex(ValueError, "limit"):
                ListarAssociacoesCurriculoVagaEntrada(
                    usuario_id=UsuarioId(uuid4()),
                    offset=0,
                    limit=limit,  # type: ignore[arg-type]
                )
