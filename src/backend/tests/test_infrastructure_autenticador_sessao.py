"""Verifica validação de token e consulta de sessão ativa."""

import hashlib
import unittest
from datetime import datetime, timezone
from uuid import UUID

from backend.application.autenticacao_sessao import ConsultaSessaoAtiva
from backend.domain.value_objects import UsuarioId
from backend.infrastructure.persistence.sqlalchemy.repositorio_sessao import (
    RepositorioSessaoSqlAlchemy,
)
from backend.infrastructure.security.autenticador_sessao import (
    AutenticadorSessaoPersistida,
)


class ConsultaSessaoStub(ConsultaSessaoAtiva):
    """Registra resumo e instante recebidos e devolve resultado configurável.

    O double mantém estado em memória e não acessa SQL. Ele existe para
    verificar o limite entre resumo do token e consulta de sessão.
    """

    def __init__(self, usuario_id: UsuarioId | None) -> None:
        """Guarda identidade de resultado e prepara histórico de chamadas.

        A configuração é local e determinística. Ela existe para cobrir sessão
        encontrada e ausente sem depender de persistência ou relógio.
        """
        self.usuario_id = usuario_id
        self.consultas: list[tuple[str, datetime]] = []

    async def obter_usuario_ativo(self, token_hash: str, instante: datetime) -> UsuarioId | None:
        """Registra os critérios da consulta e devolve a identidade preparada.

        O método não executa I/O. Ele existe para inspecionar o resumo calculado
        e o instante fornecido pelo adapter de segurança.
        """
        self.consultas.append((token_hash, instante))
        return self.usuario_id


class ResultadoExecucaoDouble:
    """Simula o resultado escalar de uma consulta SQLAlchemy.

    O objeto devolve um UUID ou `None` sem banco. Ele existe para exercitar a
    conversão da linha persistida para identidade de domínio.
    """

    def __init__(self, valor) -> None:
        """Armazena valor escalar que a consulta deve devolver.

        Nenhuma conexão é aberta. O construtor existe para controlar o resultado.
        """
        self.valor = valor

    def scalar_one_or_none(self):
        """Devolve a linha escalar opcional simulada.

        A operação corresponde ao método consumido pelo repositório. Ela existe
        para manter o teste isolado de SQL real.
        """
        return self.valor


class AsyncSessionConsultaDouble:
    """Captura expressão SELECT e devolve resultado escalar configurado.

    O double implementa somente `execute`, sem transação ou conexão real. Ele
    existe para verificar os filtros gerados pelo repositório.
    """

    def __init__(self, valor) -> None:
        """Prepara retorno da consulta e espaço para capturar o comando.

        O estado é local ao teste. Ele existe para inspecionar a expressão SQL.
        """
        self.valor = valor
        self.comando = None

    async def execute(self, comando):
        """Captura SELECT e retorna um resultado SQLAlchemy simulado.

        Não há I/O de banco. O método existe para observar os critérios da
        consulta e validar a conversão do resultado.
        """
        self.comando = comando
        return ResultadoExecucaoDouble(self.valor)


class AutenticadorSessaoPersistidaTestCase(unittest.IsolatedAsyncioTestCase):
    """Protege o resumo SHA-256 e o encaminhamento da identidade de sessão."""

    async def test_resume_token_e_retorna_identidade_com_instante_utc(self) -> None:
        """Consulta somente o hash e preserva a identidade retornada.

        A porta em memória registra os argumentos usados pelo adapter. O teste
        existe para garantir que o token em claro não chegue à persistência.
        """
        usuario_id = UsuarioId(UUID("00000000-0000-0000-0000-000000000001"))
        consulta = ConsultaSessaoStub(usuario_id)
        token = "token-opaco"

        resultado = await AutenticadorSessaoPersistida(consulta).autenticar(token)

        resumo, instante = consulta.consultas[0]
        self.assertEqual(resultado, usuario_id)
        self.assertEqual(resumo, hashlib.sha256(token.encode("utf-8")).hexdigest())
        self.assertNotEqual(resumo, token)
        self.assertEqual(instante.utcoffset().total_seconds(), 0)

    async def test_retorna_none_quando_sessao_nao_esta_ativa(self) -> None:
        """Propaga ausência de identidade para sessão desconhecida ou inativa.

        A porta retorna `None` e o adapter não fabrica identidade. O teste
        existe para garantir rejeição de sessão sem registro ativo.
        """
        consulta = ConsultaSessaoStub(None)

        resultado = await AutenticadorSessaoPersistida(consulta).autenticar("token-invalido")

        self.assertIsNone(resultado)


class RepositorioConsultaSessaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica os filtros de validade e revogação da consulta SQLAlchemy."""

    async def test_consulta_aplica_hash_expiracao_e_revogacao(self) -> None:
        """Retorna UsuarioId apenas pela linha correspondente a sessão ativa.

        O resultado SQL é simulado e a expressão compilada é inspecionada. O
        teste existe para prevenir aceitação de sessão expirada ou revogada.
        """
        uuid_usuario = UUID("00000000-0000-0000-0000-000000000001")
        session = AsyncSessionConsultaDouble(uuid_usuario)
        instante = datetime(2026, 10, 12, tzinfo=timezone.utc)

        resultado = await RepositorioSessaoSqlAlchemy(session).obter_usuario_ativo("a" * 64, instante)

        compilado = session.comando.compile()
        sql = str(compilado)
        self.assertEqual(resultado, UsuarioId(uuid_usuario))
        self.assertEqual(compilado.params["token_hash_1"], "a" * 64)
        self.assertEqual(compilado.params["expira_em_1"], instante)
        self.assertIn("revogada_em IS NULL", sql)
        self.assertIn("token_hash", sql)
        self.assertIn("expira_em", sql)

    async def test_consulta_retorna_none_sem_registro_ativo(self) -> None:
        """Não produz identidade se a consulta não encontrar sessão elegível.

        O resultado escalar simulado é nulo. O teste existe para manter sessão
        desconhecida, expirada ou revogada fora das requisições autenticadas.
        """
        session = AsyncSessionConsultaDouble(None)

        resultado = await RepositorioSessaoSqlAlchemy(session).obter_usuario_ativo(
            "b" * 64, datetime.now(timezone.utc)
        )

        self.assertIsNone(resultado)
