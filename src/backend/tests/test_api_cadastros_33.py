"""Protege as interfaces existentes com doubles para evitar regressões da #33."""

import unittest
from unittest.mock import AsyncMock
from uuid import UUID

from fastapi import HTTPException
from pydantic import ValidationError
from starlette.requests import Request

from backend.api import certificacao, curso, idioma
from backend.domain import (
    Certificacao,
    CertificacaoId,
    Curso,
    CursoId,
    Idioma,
    IdiomaId,
)
from backend.domain.value_objects import UsuarioId

DONO = UUID(int=1)
ITEM = UUID(int=2)
CASOS = (
    (
        curso,
        curso.CadastroCursoRequisicao,
        curso.CadastroCursoExecutor,
        Curso(CursoId(ITEM), UsuarioId(DONO), "Python", "Escola", 10),
        {"nome": "Python", "instituicao": "Escola", "carga_horaria": 10},
    ),
    (
        certificacao,
        certificacao.CadastroCertificacaoRequisicao,
        certificacao.CadastroCertificacaoExecutor,
        Certificacao(CertificacaoId(ITEM), UsuarioId(DONO), "Python", "Escola"),
        {"nome": "Python", "organizacao_emissora": "Escola"},
    ),
    (
        idioma,
        idioma.CadastroIdiomaRequisicao,
        idioma.CadastroIdiomaExecutor,
        Idioma(IdiomaId(ITEM), UsuarioId(DONO), "Inglês", "Avançado"),
        {"idioma": "Inglês", "nivel": "Avançado"},
    ),
)


class InterfacesCadastro33TestCase(unittest.IsolatedAsyncioTestCase):
    """Exercita contratos por handlers isolados para preservar cadastro e titularidade."""

    def test_carga_horaria_nao_converte_booleano_ou_real_em_inteiro(self):
        """Recusa coerção no DTO com valores não inteiros para preservar a regra do curso."""
        for valor in (True, False, 1.0, "10"):
            with self.subTest(valor=valor), self.assertRaises(ValidationError):
                curso.CadastroCursoRequisicao(
                    nome="Python", instituicao="Escola", carga_horaria=valor
                )

    async def test_resposta_e_comando_preservam_dono_da_sessao(self):
        """Compara resposta e comando com doubles tipados para impedir troca de dono pelo corpo."""
        for modulo, dto, protocolo, entidade, dados in CASOS:
            with self.subTest(interface=modulo.__name__):
                executor = AsyncMock(spec=protocolo)
                executor.executar.return_value = entidade
                handler = modulo.criar_router(executor).routes[0].endpoint
                request = Request({"type": "http", "headers": []})
                request.state.usuario_id = DONO
                resposta = await handler(dto(**dados, usuario_id=UUID(int=99)), request)
                self.assertEqual(
                    resposta.model_dump(), dict(dados, id=ITEM, usuario_id=DONO)
                )
                comando = executor.executar.call_args.args[0]
                self.assertEqual(comando.usuario_id, UsuarioId(DONO))
                executor.executar.assert_awaited_once()

    async def test_identidade_invalida_nao_invoca_executor(self):
        """Recusa ausência ou UUID textual em handlers isolados para evitar efeitos anônimos."""
        for modulo, dto, protocolo, _, dados in CASOS:
            for principal in (None, str(DONO)):
                with self.subTest(interface=modulo.__name__, principal=principal):
                    executor = AsyncMock(spec=protocolo)
                    request = Request({"type": "http", "headers": []})
                    request.state.usuario_id = principal
                    with self.assertRaises(HTTPException) as erro:
                        await (
                            modulo.criar_router(executor)
                            .routes[0]
                            .endpoint(dto(**dados), request)
                        )
                    self.assertEqual(erro.exception.status_code, 401)
                    executor.executar.assert_not_awaited()
