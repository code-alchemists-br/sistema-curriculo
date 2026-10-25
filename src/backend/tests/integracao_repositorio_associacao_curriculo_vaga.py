"""Exercita a consulta paginada do adapter contra SQLite assíncrono real."""

# Proveniência: decision-analysis prompts/backend/20261019-191822-consulta-paginada-associacoes-estudante-v002.md#v002

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase
from uuid import UUID

from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.domain.associacao_curriculo_vaga import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
)
from backend.domain.value_objects import CurriculoId, UsuarioId, VagaId
from backend.infrastructure.persistence.sqlalchemy.associacao_curriculo_vaga import (
    para_registro,
    para_registros_classificacoes,
)
from backend.infrastructure.persistence.sqlalchemy.curriculo import CurriculoRegistro
from backend.infrastructure.persistence.sqlalchemy.metadata import metadata
from backend.infrastructure.persistence.sqlalchemy.repositorio_associacao_curriculo_vaga import (
    RepositorioAssociacaoCurriculoVagaSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.usuario import UsuarioRegistro


def _ativar_chaves_estrangeiras(connection, _record) -> None:
    """Ativa as chaves estrangeiras na conexão SQLite de cada cenário.

    O listener aplica o pragma antes das operações da sessão. Ele existe para
    que os dados sintéticos respeitem as relações declaradas pelo mapping.
    """
    connection.execute("PRAGMA foreign_keys=ON")


class ConsultaPaginadaAssociacaoIntegracaoTestCase(IsolatedAsyncioTestCase):
    """Verifica isolamento e páginas do adapter usando uma engine SQLite real.

    O caso cria schema descartável da metadata, persiste usuários, currículos e
    associações e consulta por AsyncSession. Ele existe para provar o efeito
    conjunto do filtro de proprietário, da ordenação e da paginação SQL.
    """

    async def asyncSetUp(self) -> None:
        """Prepara schema SQLite descartável e registra cleanup de recursos.

        A engine usa arquivo temporário, metadata atual e FKs habilitadas; a
        sessão é criada por uma fábrica local. Isso isola cada execução e
        garante a liberação da conexão mesmo quando uma asserção falha.
        """
        self._diretorio = TemporaryDirectory(prefix="associacoes-paginadas-")
        self.addCleanup(self._diretorio.cleanup)
        caminho_banco = Path(self._diretorio.name) / "integracao.sqlite3"
        self._engine = create_async_engine(f"sqlite+aiosqlite:///{caminho_banco}")
        event.listen(self._engine.sync_engine, "connect", _ativar_chaves_estrangeiras)
        self.addAsyncCleanup(self._engine.dispose)
        async with self._engine.begin() as conexao:
            await conexao.run_sync(metadata.create_all)
        self._criar_sessao = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )

    async def test_pagina_filtra_proprietario_antes_de_paginar_e_ordenar(self) -> None:
        """Retorna páginas próprias contíguas e ordenadas apesar de linha alheia.

        O cenário intercala uma associação de outro usuário entre associações
        próprias na ordem global; consulta cada página de tamanho um e também
        um usuário sem associações. Ele existe para detectar paginação anterior
        ao filtro, ordenação instável e retorno incorreto para página vazia.
        """
        usuario_proprietario = UUID(int=101)
        usuario_alheio = UUID(int=102)
        usuario_sem_associacoes = UUID(int=103)
        curriculo_inicial = UUID(int=201)
        curriculo_alheio = UUID(int=202)
        curriculo_final = UUID(int=203)

        associacoes = (
            AssociacaoCurriculoVaga(
                CurriculoId(curriculo_inicial),
                VagaId("vaga-a"),
                (ClassificacaoAssociacao.INTERESSE,),
            ),
            AssociacaoCurriculoVaga(
                CurriculoId(curriculo_alheio),
                VagaId("vaga-m"),
                (ClassificacaoAssociacao.INTERESSE,),
            ),
            AssociacaoCurriculoVaga(
                CurriculoId(curriculo_final),
                VagaId("vaga-a"),
                (ClassificacaoAssociacao.INTERESSE,),
            ),
            AssociacaoCurriculoVaga(
                CurriculoId(curriculo_final),
                VagaId("vaga-z"),
                (ClassificacaoAssociacao.INTERESSE,),
            ),
        )

        async with self._criar_sessao() as sessao:
            sessao.add_all(
                (
                    UsuarioRegistro(
                        id=usuario_proprietario,
                        nome="Estudante proprietário",
                        email="proprietario@example.test",
                        hash_senha="hash-teste",
                    ),
                    UsuarioRegistro(
                        id=usuario_alheio,
                        nome="Outro estudante",
                        email="alheio@example.test",
                        hash_senha="hash-teste",
                    ),
                    UsuarioRegistro(
                        id=usuario_sem_associacoes,
                        nome="Estudante sem associações",
                        email="vazio@example.test",
                        hash_senha="hash-teste",
                    ),
                )
            )
            await sessao.flush()
            sessao.add_all(
                (
                    CurriculoRegistro(
                        id=curriculo_inicial,
                        usuario_id=usuario_proprietario,
                        titulo_versao="Currículo inicial",
                        layout="simples",
                        is_public=False,
                    ),
                    CurriculoRegistro(
                        id=curriculo_alheio,
                        usuario_id=usuario_alheio,
                        titulo_versao="Currículo alheio",
                        layout="simples",
                        is_public=False,
                    ),
                    CurriculoRegistro(
                        id=curriculo_final,
                        usuario_id=usuario_proprietario,
                        titulo_versao="Currículo final",
                        layout="simples",
                        is_public=False,
                    ),
                )
            )
            await sessao.flush()
            for associacao in associacoes:
                sessao.add(para_registro(associacao))
                sessao.add_all(para_registros_classificacoes(associacao))
            await sessao.commit()

            repositorio = RepositorioAssociacaoCurriculoVagaSqlAlchemy(sessao)
            paginas_recebidas = []
            for offset in range(3):
                paginas_recebidas.append(
                    await repositorio.listar_por_usuario(
                        UsuarioId(usuario_proprietario),
                        offset=offset,
                        limit=1,
                    )
                )
            paginas = tuple(paginas_recebidas)
            pagina_vazia = await repositorio.listar_por_usuario(
                UsuarioId(usuario_sem_associacoes),
                offset=0,
                limit=1,
            )

        pares_obtidos = tuple(
            (associacao.curriculo_id.valor, associacao.vaga_id.valor)
            for pagina in paginas
            for associacao in pagina
        )
        self.assertEqual(
            pares_obtidos,
            (
                (curriculo_inicial, "vaga-a"),
                (curriculo_final, "vaga-a"),
                (curriculo_final, "vaga-z"),
            ),
        )
        self.assertEqual(tuple(len(pagina) for pagina in paginas), (1, 1, 1))
        self.assertEqual(pagina_vazia, ())
