"""Verifica repositório de projeto com sessão mockada e SQL não executado.

Compila instruções e observa parâmetros, rowcount e mapeamento para proteger
predicados e fronteiras transacionais sem banco ou migration integrada.
"""

# Proveniência: decision-analysis prompts/backend/20261108-110818-consulta-atualizacao-exclusao-projeto-academico-v001.md#v001
from datetime import datetime, timezone
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain import ProjetoAcademico, ProjetoAcademicoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.projeto_academico import (
    ProjetoAcademicoRegistro,
    para_projeto_academico,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_projeto_academico import (
    RepositorioProjetoAcademicoSQLAlchemy,
)

INSTANTE = datetime(2026, 11, 8, tzinfo=timezone.utc)


def projeto():
    """Cria entidade válida com IDs fixos e marcador opcional pelo replace.

    Usa dados sintéticos estáveis para comparar mapeamentos e parâmetros SQL
    sem dependência de geradores, relógio ou armazenamento reais.
    """
    return ProjetoAcademico(ProjetoAcademicoId(UUID(int=1)), UsuarioId(UUID(int=2)),
                           "Projeto", "Descrição", "Python")


class RepositorioProjetoOperacoesTestCase(IsolatedAsyncioTestCase):
    """Isola a porta concreta usando sessão e resultados ORM doubles.

    Inspeciona SQL compilado sem execução para proteger filtros, conversão e
    sinal de escrita condicional sem assumir responsabilidade pelo banco.
    """

    def setUp(self):
        """Prepara sessão mockada e entidade determinística para cada cenário.

        Substitui execute, scalar e flush para manter toda atividade externa
        controlada e permitir observar ausência de commit no repositório.
        """
        self.sessao = Mock(spec=AsyncSession)
        self.sessao.scalar = AsyncMock()
        self.sessao.execute = AsyncMock()
        self.sessao.flush = AsyncMock()
        self.repositorio = RepositorioProjetoAcademicoSQLAlchemy(self.sessao)
        self.projeto = projeto()

    def conferir_predicados(self, instrucao, ativo):
        """Compara WHERE e parâmetros da instrução com IDs do cenário.

        Compila somente a expressão usando o dialeto PostgreSQL para garantir
        filtro por ID e dono e estado ativo quando exigido, sem conexão real.
        """
        compilado = instrucao.compile(dialect=postgresql.dialect())
        onde = str(compilado).split("WHERE ", 1)[1]
        self.assertIn("projetos_academicos.id =", onde)
        self.assertIn("projetos_academicos.usuario_id =", onde)
        self.assertEqual("deleted_at IS NULL" in onde, ativo)
        self.assertIn(self.projeto.id.valor, compilado.params.values())
        self.assertIn(self.projeto.usuario_id.valor, compilado.params.values())
        return compilado

    async def test_leituras_filtram_e_convertem_sem_commit(self):
        """Verifica leitura ativa, inclusiva e ausência com os mesmos dois IDs.

        Alterna registro e None na sessão double para conferir filtros e
        conversão do marcador sem introduzir flush ou commit na consulta.
        """
        for nome, ativo in (("obter_por_id_e_usuario", True),
                            ("obter_por_id_e_usuario_incluindo_excluidas", False)):
            for encontrado in (True, False):
                with self.subTest(nome=nome, encontrado=encontrado):
                    entidade = self.projeto if ativo else self.projeto.excluir(INSTANTE)
                    self.sessao.scalar.return_value = para_registro(entidade) if encontrado else None
                    resultado = await getattr(self.repositorio, nome)(
                        self.projeto.id, self.projeto.usuario_id
                    )
                    self.assertEqual(resultado, entidade if encontrado else None)
                    self.conferir_predicados(self.sessao.scalar.await_args.args[0], ativo)
        self.sessao.commit.assert_not_called()
        self.sessao.flush.assert_not_awaited()

    async def test_updates_condicionais_preservam_identidade_e_usam_rowcount(self):
        """Verifica UPDATEs, parâmetros e retorno para uma ou nenhuma linha.

        Alterna rowcount nos resultados doubles e inspeciona somente valores
        editáveis ou deleted_at para não permitir troca de dono ou ressurreição.
        """
        for exclusao in (False, True):
            for linhas in (0, 1, -1):
                with self.subTest(exclusao=exclusao, linhas=linhas):
                    self.sessao.execute.return_value = Mock(rowcount=linhas)
                    self.sessao.flush.reset_mock()
                    if exclusao:
                        resultado = await self.repositorio.marcar_excluida(
                            self.projeto.id, self.projeto.usuario_id, INSTANTE
                        )
                    else:
                        resultado = await self.repositorio.atualizar(self.projeto)
                    self.assertIs(resultado, linhas == 1)
                    instrucao = self.sessao.execute.await_args.args[0]
                    compilado = self.conferir_predicados(instrucao, True)
                    sql = str(compilado)
                    self.assertTrue(sql.startswith("UPDATE projetos_academicos SET"))
                    campos = sql.split(" SET ", 1)[1].split(" WHERE ", 1)[0]
                    self.assertNotIn("usuario_id", campos)
                    self.assertNotIn(" id=", campos)
                    if exclusao:
                        self.assertEqual(compilado.params["deleted_at"], INSTANTE)
                        self.assertNotIn("titulo", campos)
                    else:
                        self.assertNotIn("deleted_at", campos)
                        self.assertEqual(compilado.params["titulo"], self.projeto.titulo)
                        self.assertEqual(compilado.params["descricao"], self.projeto.descricao)
                        self.assertEqual(compilado.params["tecnologias"], self.projeto.tecnologias)
                    self.sessao.flush.assert_awaited_once_with()
        self.sessao.commit.assert_not_called()
        self.sessao.add.assert_not_called()
        self.sessao.delete.assert_not_called()


class MarcadorProjetoTestCase(TestCase):
    """Verifica mapeamento e metadata temporal sem executar schema.

    Faz roundtrip em objetos em memória e compara tipo e nulabilidade para
    preservar o marcador entre domínio e ORM sem acoplar regras ao banco.
    """

    def test_marcador_anulavel_com_fuso_e_roundtrip(self):
        """Confere DateTime com timezone e conversão de ativo e excluído.

        Examina metadata e objetos ORM em memória para proteger compatibilidade
        da coluna aditiva e preservação do primeiro instante mapeado.
        """
        coluna = ProjetoAcademicoRegistro.__table__.c.deleted_at
        self.assertTrue(coluna.nullable)
        self.assertTrue(coluna.type.timezone)
        self.assertFalse(coluna.index)
        for entidade in (projeto(), projeto().excluir(INSTANTE)):
            registro = para_registro(entidade)
            self.assertEqual(registro.deleted_at, entidade.deleted_at)
            self.assertEqual(para_projeto_academico(registro), entidade)
