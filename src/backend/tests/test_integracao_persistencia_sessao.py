"""Valida migrations e persistência de sessão com SQLite assíncrono real.

Os cenários M01–M03 e P01–P03 usam banco migrado e transações externas para
verificar o contrato atual sem simular o ORM ou certificar a composição HTTP.
"""

# Proveniência: decision-analysis prompts/backend/20261018-131822-validacao-contrato-credenciais-cards-80-82-v001.md#v001

import unittest
from datetime import timedelta, timezone
from unittest.mock import patch
from uuid import UUID, uuid4

from sqlalchemy import insert, select, text
from sqlalchemy.exc import IntegrityError

from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.repositorio_sessao import (
    RepositorioSessaoSqlAlchemy,
)
from backend.infrastructure.persistence.sqlalchemy.sessao import SessaoRegistro
from backend.infrastructure.security.autenticador_sessao import (
    AutenticadorSessaoPersistida,
)
from backend.infrastructure.security.tokens_sessao import CriadorSessaoSeguro
from backend.tests.fixtures.credenciais_sessao import (
    AIOSQLITE_DISPONIVEL,
    COLUNAS_SESSAO,
    INSTANTE_T,
    MOTIVO_SEM_AIOSQLITE,
    USUARIO_A,
    BancoCredenciaisSessao,
    resumo_token,
    token_sintetico,
)


@unittest.skipUnless(AIOSQLITE_DISPONIVEL, MOTIVO_SEM_AIOSQLITE)
class PersistenciaSessaoIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Exercita DDL e adapters reais com um banco descartável por cenário.

    Prepara migrations até head e usa sessões novas para conferir resultados,
    distinguindo integridade persistida de chamadas unitárias com doubles.
    """

    async def asyncSetUp(self) -> None:
        """Prepara banco e registra cleanup antes de migrar ou semear dados.

        Usa fixture exclusiva por teste para garantir descarte mesmo quando
        preflight, migrations ou asserções interrompem o cenário.
        """
        self.banco = BancoCredenciaisSessao()
        self.addAsyncCleanup(self.banco.fechar)
        await self.banco.preparar()

    async def test_M01_schema_migrado_ate_head(self) -> None:
        """M01 confere schema e head reais após todas as migrations.

        Consulta o inspetor e alembic_version para provar colunas, nulabilidade,
        PK, FK e unicidade do hash sem depender da metadata como evidência.
        """
        schema = await self.banco.inspecionar_schema()
        self.assertEqual(schema["versoes"], (self.banco.head,))
        self.assertNotIn("is present more than once", self.banco.saida_migrations)
        self.assertEqual(tuple(coluna["name"] for coluna in schema["colunas"]), COLUNAS_SESSAO)
        self.assertEqual(
            {coluna["name"]: coluna["nullable"] for coluna in schema["colunas"]},
            {nome: nome == "revogada_em" for nome in COLUNAS_SESSAO},
        )
        self.assertEqual(schema["pk"]["constrained_columns"], ["id"])
        self.assertEqual(len(schema["fks"]), 1)
        fk = schema["fks"][0]
        self.assertEqual(fk["constrained_columns"], ["usuario_id"])
        self.assertEqual(fk["referred_table"], "usuarios")
        self.assertEqual(fk["referred_columns"], ["id"])
        self.assertEqual(fk["name"], "fk_sessoes_usuario_id_usuarios")
        self.assertEqual(len(schema["unicas"]), 1)
        self.assertEqual(schema["unicas"][0]["column_names"], ["token_hash"])
        self.assertEqual(schema["unicas"][0]["name"], "uq_sessoes_token_hash")

    async def test_M02_unicidade_e_campos_obrigatorios(self) -> None:
        """M02 rejeita hash repetido e NULL obrigatório com transações isoladas.

        Insere a linha de controle, tenta cada violação pelo banco e relê seu
        estado após rollback para comprovar integridade sem perder a original.
        """
        dados = {
            "id": uuid4(), "usuario_id": USUARIO_A,
            "token_hash": resumo_token(token_sintetico(1)),
            "criada_em": INSTANTE_T, "expira_em": INSTANTE_T + timedelta(hours=8),
            "revogada_em": None,
        }
        async with self.banco.sessoes() as sessao:
            await sessao.execute(insert(SessaoRegistro.__table__).values(**dados))
            await sessao.commit()
        original = await self.banco.snapshot()
        self.assertEqual(len(original["sessoes"]), 1)
        tentativas = [("hash repetido", {**dados, "id": uuid4()})]
        for campo in COLUNAS_SESSAO[:-1]:
            tentativa = {
                **dados, "id": uuid4(),
                "token_hash": resumo_token(token_sintetico(2)), campo: None,
            }
            tentativas.append((f"NULL em {campo}", tentativa))
        for rotulo, tentativa in tentativas:
            with self.subTest(violacao=rotulo):
                async with self.banco.sessoes() as sessao:
                    with self.assertRaises(IntegrityError):
                        await sessao.execute(insert(SessaoRegistro.__table__).values(**tentativa))
                        await sessao.commit()
                    await sessao.rollback()
                self.assertTrue(original == await self.banco.snapshot(), "Estado alterado após violação")

    async def test_M03_fk_rejeita_usuario_inexistente(self) -> None:
        """M03 confirma FK ativa e rejeita sessão sem conta correspondente.

        Tenta salvar pelo repositório real com UUID ausente e confere snapshot
        após rollback em sessão nova para provar que não sobra linha órfã.
        """
        original = await self.banco.snapshot()
        self.assertEqual(len(original["sessoes"]), 0)
        self.assertEqual(len(original["usuarios"]), 2)
        async with self.banco.sessoes() as sessao:
            self.assertEqual((await sessao.execute(text("PRAGMA foreign_keys"))).scalar_one(), 1)
            repositorio = RepositorioSessaoSqlAlchemy(sessao)
            with self.assertRaises(IntegrityError):
                await repositorio.salvar(
                    UsuarioId(UUID("10000000-0000-4000-8000-000000000099")),
                    resumo_token(token_sintetico(3)), INSTANTE_T,
                    INSTANTE_T + timedelta(hours=8),
                )
                await sessao.commit()
            await sessao.rollback()
        self.assertTrue(original == await self.banco.snapshot(), "Sobrou estado após violação de FK")

    async def test_P01_criador_persiste_hash_duravel_e_autentica(self) -> None:
        """P01 emite token real e relê hash e validade após commit externo.

        Controla somente datetime nos módulos de segurança e reabre sessões
        reais para provar duração, proprietário e autenticação sem expor token.
        """
        async with self.banco.sessoes() as sessao:
            with patch("backend.infrastructure.security.tokens_sessao.datetime") as relogio:
                relogio.now.return_value = INSTANTE_T
                token = await CriadorSessaoSeguro(RepositorioSessaoSqlAlchemy(sessao)).criar(
                    UsuarioId(USUARIO_A)
                )
            relogio.now.assert_called_once_with(timezone.utc)
            await sessao.commit()
        async with self.banco.sessoes() as sessao:
            resultado = await sessao.execute(select(SessaoRegistro.__table__))
            self.assertEqual(tuple(resultado.keys()), COLUNAS_SESSAO)
            linhas = resultado.mappings().all()
        self.assertEqual(len(linhas), 1)
        linha = linhas[0]
        self.assertTrue(linha["token_hash"] == resumo_token(token), "Resumo não corresponde")
        self.assertTrue(linha["token_hash"] != token, "Credencial reutilizável persistida")
        self.assertIsInstance(linha["id"], UUID)
        self.assertEqual(linha["usuario_id"], USUARIO_A)
        self.assertIsNone(linha["revogada_em"])
        # SQLite remove tzinfo no roundtrip de DateTime. A fixture gravou UTC;
        # a normalização é somente da asserção, sem alterar dados ou consultas.
        criada = linha["criada_em"].replace(tzinfo=timezone.utc)
        expira = linha["expira_em"].replace(tzinfo=timezone.utc)
        self.assertEqual(criada, INSTANTE_T)
        self.assertEqual(expira - criada, timedelta(hours=8))
        async with self.banco.sessoes() as sessao:
            with patch("backend.infrastructure.security.autenticador_sessao.datetime") as relogio:
                relogio.now.return_value = INSTANTE_T
                identidade = await AutenticadorSessaoPersistida(
                    RepositorioSessaoSqlAlchemy(sessao)
                ).autenticar(token)
            relogio.now.assert_called_once_with(timezone.utc)
        self.assertEqual(identidade, UsuarioId(USUARIO_A))

    async def test_P02_fronteira_de_expiracao_sem_mutacao(self) -> None:
        """P02 diferencia expiração antes, no instante e depois de T.

        Consulta hashes reais com T explícito e autentica com relógio fixo,
        comparando snapshots novos para garantir que leituras não renovam sessão.
        """
        tokens = [token_sintetico(indice) for indice in (4, 5, 6)]
        async with self.banco.sessoes() as sessao:
            repositorio = RepositorioSessaoSqlAlchemy(sessao)
            for token, segundos in zip(tokens, (-1, 0, 1), strict=True):
                await repositorio.salvar(
                    UsuarioId(USUARIO_A), resumo_token(token),
                    INSTANTE_T - timedelta(hours=1), INSTANTE_T + timedelta(seconds=segundos),
                )
            await sessao.commit()
        original = await self.banco.snapshot()
        self.assertEqual(len(original["sessoes"]), 3)
        for token, segundos in zip(tokens, (-1, 0, 1), strict=True):
            with self.subTest(deslocamento_segundos=segundos):
                esperado = UsuarioId(USUARIO_A) if segundos > 0 else None
                async with self.banco.sessoes() as sessao:
                    repositorio = RepositorioSessaoSqlAlchemy(sessao)
                    self.assertEqual(
                        await repositorio.obter_usuario_ativo(resumo_token(token), INSTANTE_T), esperado
                    )
                    with patch("backend.infrastructure.security.autenticador_sessao.datetime") as relogio:
                        relogio.now.return_value = INSTANTE_T
                        identidade = await AutenticadorSessaoPersistida(repositorio).autenticar(token)
                    self.assertEqual(identidade, esperado)
                    await sessao.commit()
                self.assertTrue(original == await self.banco.snapshot(), "Consulta alterou o estado")

    async def test_P03_rollback_externo_descarta_flush(self) -> None:
        """P03 caracteriza rollback externo sem prometer atomicidade HTTP.

        Confirma a linha após flush na transação corrente, desfaz a transação
        do harness e relê em sessão nova para comprovar ausência persistida.
        """
        original = await self.banco.snapshot()
        self.assertEqual(len(original["sessoes"]), 0)
        async with self.banco.sessoes() as sessao:
            await RepositorioSessaoSqlAlchemy(sessao).salvar(
                UsuarioId(USUARIO_A), resumo_token(token_sintetico(7)),
                INSTANTE_T, INSTANTE_T + timedelta(hours=8),
            )
            self.assertEqual(len((await sessao.execute(select(SessaoRegistro.id))).all()), 1)
            await sessao.rollback()
        self.assertTrue(original == await self.banco.snapshot(), "Flush persistiu após rollback")
