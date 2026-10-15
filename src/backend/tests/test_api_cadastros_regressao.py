"""Protege os contratos das issues #31/#32 com executores AsyncMock isolados.

Os testes exercitam handlers e DTOs atuais, sem banco ou servidor, para
complementar a cobertura sem reintroduzir as rotas antigas do patch.
"""

import unittest
from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID

from fastapi import HTTPException
from pydantic import ValidationError
from starlette.requests import Request

from backend.api.experiencia_profissional import (
    CadastroExperienciaProfissionalExecutor,
    CadastroExperienciaProfissionalRequisicao,
    ExperienciaProfissionalResposta,
)
from backend.api.experiencia_profissional import criar_router as router_experiencia
from backend.api.formacao_academica import (
    CadastroFormacaoAcademicaExecutor,
    CadastroFormacaoAcademicaRequisicao,
    FormacaoAcademicaResposta,
)
from backend.api.formacao_academica import criar_router as router_formacao
from backend.application.cadastro_experiencia_profissional import (
    CadastrarExperienciaProfissionalEntrada,
)
from backend.application.perfil_estudante import CadastrarFormacaoAcademicaEntrada
from backend.domain import (
    ExperienciaProfissional,
    ExperienciaProfissionalId,
    FormacaoAcademica,
    FormacaoAcademicaId,
    NivelFormacaoAcademica,
    Periodo,
    RegraDeDominioViolada,
    StatusFormacaoAcademica,
    UsuarioId,
)

USUARIO = UUID("00000000-0000-0000-0000-000000000001")
ITEM = UUID("00000000-0000-0000-0000-000000000002")


class CadastrosRegressaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Compara as duas fronteiras com doubles assíncronos de contrato explícito.

    Cada cenário cria mocks com spec e entradas fixas para verificar comandos,
    respostas e ausência de efeitos em falhas, sem executar casos de uso reais.
    """

    def preparar(self, tipo, fim=None):
        """Monta um cadastro válido e seu executor controlado para um cenário.

        Seleciona DTO, entidade e router por tipo, usando IDs e datas fixos para
        permitir asserções exatas e independentes de relógio ou persistência.
        """
        if tipo == "formacao":
            textos = {
                "instituicao": "FATEC",
                "curso": "ADS",
                "nivel": NivelFormacaoAcademica.TECNOLOGO,
                "status": StatusFormacaoAcademica.EM_ANDAMENTO,
            }
            dto = CadastroFormacaoAcademicaRequisicao
            executor = AsyncMock(spec=CadastroFormacaoAcademicaExecutor)
            entidade = FormacaoAcademica
            identificador = FormacaoAcademicaId(ITEM)
            router = router_formacao
            comando = CadastrarFormacaoAcademicaEntrada
            resposta = FormacaoAcademicaResposta
        else:
            textos = {
                "empresa": "Empresa exemplo",
                "cargo": "Desenvolvedora",
                "descricao": "Desenvolvimento de sistemas.",
            }
            dto = CadastroExperienciaProfissionalRequisicao
            executor = AsyncMock(spec=CadastroExperienciaProfissionalExecutor)
            entidade = ExperienciaProfissional
            identificador = ExperienciaProfissionalId(ITEM)
            router = router_experiencia
            comando = CadastrarExperienciaProfissionalEntrada
            resposta = ExperienciaProfissionalResposta
        dados = {**textos, "data_inicio": "2024-01-01", "data_fim": fim}
        periodo = Periodo(date(2024, 1, 1), date.fromisoformat(fim) if fim else None)
        executor.executar.return_value = entidade(
            id=identificador, usuario_id=UsuarioId(USUARIO), periodo=periodo, **textos
        )
        rota = router(executor).routes[0]
        request = Request(
            {"type": "http", "method": "POST", "path": rota.path, "headers": []}
        )
        request.state.usuario_id = USUARIO
        return executor, rota, request, dto, dados, comando, resposta, periodo, textos

    async def test_comando_e_resposta_exatos_com_periodo_aberto_e_fechado(self):
        """Verifica todos os campos enviados e devolvidos nos dois cadastros.

        Usa AsyncMock e compara dataclasses/DTOs completos com datas fixas para
        detectar perda de campos ou mudanças no contrato público de criação.
        """
        for tipo in ("formacao", "experiencia"):
            for fim in (None, "2025-01-01"):
                with self.subTest(tipo=tipo, fim=fim):
                    (
                        executor,
                        rota,
                        request,
                        dto,
                        dados,
                        comando,
                        resposta,
                        periodo,
                        textos,
                    ) = self.preparar(tipo, fim)
                    resultado = await rota.endpoint(dto.model_validate(dados), request)
                    executor.executar.assert_awaited_once_with(
                        comando(
                            usuario_id=UsuarioId(USUARIO), periodo=periodo, **textos
                        )
                    )
                    self.assertEqual(
                        resultado,
                        resposta(
                            id=ITEM,
                            usuario_id=USUARIO,
                            data_inicio=periodo.inicio,
                            data_fim=periodo.fim,
                            **textos,
                        ),
                    )
                    self.assertEqual(rota.status_code, 201)
                    self.assertEqual(rota.methods, {"POST"})
                    self.assertIs(rota.response_model, resposta)

    async def test_cronologia_invalida_nao_executa_cadastro(self):
        """Exige rejeição do período invertido antes de chamar o executor.

        Altera apenas a data final e observa HTTPException e histórico do mock
        para impedir efeitos quando o value object rejeita a cronologia.
        """
        for tipo in ("formacao", "experiencia"):
            with self.subTest(tipo=tipo):
                executor, rota, request, dto, dados, *_ = self.preparar(tipo)
                dados["data_fim"] = "2023-01-01"
                with self.assertRaises(HTTPException) as erro:
                    await rota.endpoint(dto.model_validate(dados), request)
                self.assertEqual(erro.exception.status_code, 422)
                executor.executar.assert_not_awaited()

    async def test_falha_interna_nao_e_mascarada_como_validacao(self):
        """Preserva falhas inesperadas em vez de classificá-las como entrada ruim.

        Injeta RuntimeError no executor e exige sua propagação para que defeitos
        internos permaneçam distinguíveis de erros de validação do usuário.
        """
        for tipo in ("formacao", "experiencia"):
            with self.subTest(tipo=tipo):
                executor, rota, request, dto, dados, *_ = self.preparar(tipo)
                executor.executar.side_effect = RuntimeError("Falha controlada")
                with self.assertRaisesRegex(RuntimeError, "Falha controlada"):
                    await rota.endpoint(dto.model_validate(dados), request)
                executor.executar.assert_awaited_once()

    async def test_violacao_de_dominio_retorna_422(self):
        """Traduz a exceção de domínio sem depender de validação do double.

        O mock lança a falha explicitamente para verificar o tratamento do
        handler, isolando transporte das regras executadas na Application.
        """
        for tipo in ("formacao", "experiencia"):
            with self.subTest(tipo=tipo):
                executor, rota, request, dto, dados, *_ = self.preparar(tipo)
                executor.executar.side_effect = RegraDeDominioViolada("Dados inválidos")
                with self.assertRaises(HTTPException) as erro:
                    await rota.endpoint(dto.model_validate(dados), request)
                self.assertEqual(erro.exception.status_code, 422)
                executor.executar.assert_awaited_once()

    async def test_identidade_textual_nao_e_aceita_como_sessao(self):
        """Rejeita um principal não tipado antes de produzir efeitos.

        Substitui o UUID do estado por texto para confirmar que a identidade
        precisa vir do contrato autenticado, não de entrada arbitrária.
        """
        for tipo in ("formacao", "experiencia"):
            with self.subTest(tipo=tipo):
                executor, rota, request, dto, dados, *_ = self.preparar(tipo)
                request.state.usuario_id = str(USUARIO)
                with self.assertRaises(HTTPException) as erro:
                    await rota.endpoint(dto.model_validate(dados), request)
                self.assertEqual(erro.exception.status_code, 401)
                executor.executar.assert_not_awaited()

    async def test_executor_ausente_retorna_503(self):
        """Confirma indisponibilidade explícita quando falta composição.

        Constrói ambos os routers sem executor e chama seus handlers com dados
        válidos para impedir respostas de sucesso sem um caso de uso real.
        """
        for tipo, router in (
            ("formacao", router_formacao),
            ("experiencia", router_experiencia),
        ):
            with self.subTest(tipo=tipo):
                _, _, request, dto, dados, *_ = self.preparar(tipo)
                with self.assertRaises(HTTPException) as erro:
                    await (
                        router(None)
                        .routes[0]
                        .endpoint(dto.model_validate(dados), request)
                    )
                self.assertEqual(erro.exception.status_code, 503)

    def test_campos_ausentes_e_datas_invalidas_rejeitados_pelo_dto(self):
        """Valida entradas obrigatórias e datas antes de invocar os handlers.

        Remove cada campo obrigatório e fornece datas impossíveis para proteger
        a desserialização dos dois contratos sem depender de persistência.
        """
        for tipo in ("formacao", "experiencia"):
            executor, _, _, dto, dados, *_ = self.preparar(tipo)
            for campo in dados:
                if campo == "data_fim":
                    continue
                with self.subTest(tipo=tipo, ausente=campo):
                    incompleto = dict(dados)
                    del incompleto[campo]
                    with self.assertRaises(ValidationError):
                        dto.model_validate(incompleto)
            for campo in ("data_inicio", "data_fim"):
                with self.subTest(tipo=tipo, data=campo):
                    with self.assertRaises(ValidationError):
                        dto.model_validate({**dados, campo: "2024-02-30"})
            executor.executar.assert_not_called()
