"""Testa DTOs, handlers e tradução local de validação sem servidor ou banco.

Usa executores e handler de framework substituídos para conferir normalização,
metadados e mensagens seguras sem integrar Application ou persistência.
"""

# Proveniência: decision-analysis prompts/backend/20261107-175712-validar-datas-textos-experiencias-profissionais-v001.md#v001
import unittest
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from pydantic import ValidationError

from backend.api.experiencia_profissional import (
    CadastroExperienciaProfissionalRequisicao,
    EdicaoExperienciaProfissionalRequisicao,
    ExperienciaProfissionalResposta,
    _resposta,
    criar_router,
)
from backend.api.rota_gravacao_experiencia import RotaGravacaoExperiencia
from backend.application.edicao_experiencia_profissional import (
    ExperienciaProfissionalNaoEncontrada,
)
from backend.domain.exceptions import RegraDeDominioViolada
from backend.domain.itens_perfil import ExperienciaProfissional
from backend.domain.value_objects import ExperienciaProfissionalId, Periodo, UsuarioId

DONO = UUID(int=101)
ITEM = UUID(int=1)
DTO_POR_METODO = {"POST": CadastroExperienciaProfissionalRequisicao,
                  "PUT": EdicaoExperienciaProfissionalRequisicao}


def payload(**alteracoes):
    """Fornece corpo sintético fixo com alterações isoladas por cenário.

    Mantém datas estáveis e permite variar textos para testar somente a
    representação de entrada sem depender do dia atual ou do fuso do ambiente.
    """
    return {
        "empresa": "Empresa Local", "cargo": "Desenvolvedor",
        "descricao": "Desenvolvimento de aplicações.",
        "data_inicio": "2024-01-01", "data_fim": None,
        **alteracoes,
    }


def preparar_handler(metodo, erro=None):
    """Monta o handler isolado e seu executor double para observar tradução.

    Cria somente o router declarativo e um estado autenticado sintético para
    testar cadastro/edição sem iniciar framework ou usar caso de uso real.
    """
    entidade = ExperienciaProfissional(
        id=ExperienciaProfissionalId(ITEM), usuario_id=UsuarioId(DONO),
        empresa="Empresa Local", cargo="Desenvolvedor", descricao="Descrição",
        periodo=Periodo(date(2024, 1, 1)),
    )
    executor = Mock(executar=AsyncMock(return_value=entidade, side_effect=erro))
    router = criar_router(executor if metodo == "POST" else None,
                          executor if metodo == "PUT" else None)
    handler = next(rota.endpoint for rota in router.routes if metodo in rota.methods)
    request = Mock(state=SimpleNamespace(usuario_id=DONO))
    return handler, executor, request


async def chamar_handler(metodo, handler, dto, request):
    """Invoca diretamente uma das assinaturas do handler para isolar a unidade.

    Fornece o ID somente à edição e mantém a requisição como double para
    observar transporte sem atravessar middleware ou HTTP real.
    """
    if metodo == "POST":
        return await handler(dto, request)
    return await handler(ITEM, dto, request)


class EntradasExperienciaTestCase(unittest.TestCase):
    """Confere os DTOs e schemas puros sem executar políticas de negócio.

    Parametriza limites, Unicode e tipos para garantir o mesmo contrato estático
    de entrada em POST e PUT, preservando uma resposta sem limites retroativos.
    """

    def test_limites_inclusivos_apos_strip_nos_dois_dtos(self):
        """Aceita mínimo/máximo após strip e rejeita branco ou máximo mais um.

        Usa caracteres Unicode e variação de cada campo para conferir os limites
        expostos pelo transporte sem truncar ou restringir espaços internos.
        """
        for metodo, dto in DTO_POR_METODO.items():
            for campo, maximo in (("empresa", 200), ("cargo", 200), ("descricao", 5000)):
                for tamanho in (1, maximo):
                    with self.subTest(metodo=metodo, campo=campo, tamanho=tamanho):
                        texto = "é" * tamanho
                        entrada = dto.model_validate(payload(**{campo: " \t" + texto + "\n "}))
                        self.assertEqual(getattr(entrada, campo), texto)
                for texto in ("", " \t\n ", " " + "é" * (maximo + 1) + " "):
                    with self.subTest(metodo=metodo, campo=campo, invalido=len(texto)):
                        with self.assertRaises(ValidationError):
                            dto.model_validate(payload(**{campo: texto}))

    def test_textos_sao_estritos_e_unicode_e_linhas_internas_sao_preservados(self):
        """Rejeita coerção de tipos e conserva descrição multilinha e Unicode.

        Confere len por pontos de código com texto composto e não permite bytes,
        números ou coleções para manter o transporte fiel às strings fornecidas.
        """
        for metodo, dto in DTO_POR_METODO.items():
            descricao = "Primeira  linha\nSegunda\tlinha 👩🏽‍💻"
            entrada = dto.model_validate(payload(empresa="e\u0301" * 100, descricao=" \n" + descricao + "\n "))
            self.assertEqual(len(entrada.empresa), 200)
            self.assertEqual(entrada.descricao, descricao)
            with self.assertRaises(ValidationError):
                dto.model_validate(payload(cargo="e\u0301" * 101))
            for campo in ("empresa", "cargo", "descricao"):
                for valor in (None, 42, 1.5, True, b"texto", [], {}):
                    with self.subTest(metodo=metodo, campo=campo, tipo=type(valor)):
                        with self.assertRaises(ValidationError):
                            dto.model_validate(payload(**{campo: valor}))

    def test_datas_mantem_opcionalidade_e_delegam_regra_temporal(self):
        """Confere ausência/null de término sem congelar hoje no DTO.

        Aceita formato de uma data futura para delegar sua regra à Application
        e ignora controles extras do cliente sem transformá-los em entrada interna.
        """
        dados = payload(data_inicio="2100-01-01", hoje="2200-01-01", fuso="UTC")
        del dados["data_fim"]
        self.assertIsNone(CadastroExperienciaProfissionalRequisicao.model_validate(dados).data_fim)
        with self.assertRaises(ValidationError):
            EdicaoExperienciaProfissionalRequisicao.model_validate(dados)
        for dto in DTO_POR_METODO.values():
            entrada = dto.model_validate({**dados, "data_fim": None})
            self.assertNotIn("hoje", entrada.model_dump())
            self.assertNotIn("fuso", entrada.model_dump())

    def test_schemas_das_rotas_documentam_limites_e_datas_sem_maximo_estatico(self):
        """Gera schema a partir das rotas declaradas sem aplicação iniciada.

        Inspeciona schemas referenciados pelos corpos para conferir min/maxLength,
        obrigatoriedade e descrições temporais dinâmicas nos dois métodos.
        """
        documento = get_openapi(title="Teste", version="1", routes=criar_router(None).routes)
        schemas = documento["components"]["schemas"]
        for metodo, dto in DTO_POR_METODO.items():
            caminho = "/experiencias-profissionais" if metodo == "POST" else "/experiencias-profissionais/{experiencia_id}"
            operacao = documento["paths"][caminho][metodo.lower()]
            ref = operacao["requestBody"]["content"]["application/json"]["schema"]["$ref"]
            self.assertEqual(ref.rsplit("/", 1)[1], dto.__name__)
            schema = schemas[dto.__name__]
            for campo, maximo in (("empresa", 200), ("cargo", 200), ("descricao", 5000)):
                self.assertEqual(schema["properties"][campo]["minLength"], 1)
                self.assertEqual(schema["properties"][campo]["maxLength"], maximo)
            for campo in ("data_inicio", "data_fim"):
                propriedade = schema["properties"][campo]
                self.assertIn("America/Sao_Paulo", propriedade["description"])
                self.assertNotIn("maximum", str(propriedade))
            self.assertEqual("data_fim" in schema["required"], metodo == "PUT")
            self.assertIn("422", operacao["responses"])
            erro_ref = operacao["responses"]["422"]["content"]["application/json"]["schema"]["$ref"]
            self.assertEqual(schemas[erro_ref.rsplit("/", 1)[1]]["properties"]["detail"]["type"], "string")

    def test_resposta_e_mapper_aceitam_legado_sem_aplicar_limites_de_entrada(self):
        """Converte entidade legada com textos extensos e datas futuras em DTO.

        Compara sete campos e schema sem limites para impedir que a correção das
        gravações restrinja a representação de leitura de dados existentes.
        """
        legado = ExperienciaProfissional(
            id=ExperienciaProfissionalId(ITEM), usuario_id=UsuarioId(DONO),
            empresa="e" * 201, cargo="c" * 201, descricao="d" * 5001,
            periodo=Periodo(date(2100, 1, 1), date(2101, 1, 1)),
        )
        resposta = _resposta(legado)
        self.assertEqual(set(resposta.model_dump()), {
            "id", "usuario_id", "empresa", "cargo", "descricao", "data_inicio", "data_fim"
        })
        self.assertEqual(resposta.descricao, legado.descricao)
        self.assertEqual(resposta.data_fim, date(2101, 1, 1))
        for campo in ("empresa", "cargo", "descricao"):
            self.assertNotIn("maxLength", ExperienciaProfissionalResposta.model_json_schema()["properties"][campo])


class HandlersGravacaoExperienciaTestCase(unittest.IsolatedAsyncioTestCase):
    """Confere handlers com casos de uso double para isolar a tradução HTTP.

    Testa a entrada normalizada, erros de domínio e de formato sem reimplementar
    ou integrar a política temporal e sem acessar banco ou relógio reais.
    """

    async def test_normalizacao_chega_a_application_sem_dono_ou_hoje_do_cliente(self):
        """Passa os DTOs normalizados ao handler e inspeciona os comandos enviados.

        Usa dados de cliente conflitantes para garantir que a identidade venha
        do estado e nenhum parâmetro temporal externo alcance a Application.
        """
        for metodo, dto in DTO_POR_METODO.items():
            handler, executor, request = preparar_handler(metodo)
            entrada = dto.model_validate(payload(
                empresa=" Empresa  Local ", cargo=" Cargo ", descricao="\n A  B\nC \n",
                usuario_id=str(UUID(int=999)), hoje="2200-01-01", fuso="UTC",
            ))
            await chamar_handler(metodo, handler, entrada, request)
            executor.executar.assert_awaited_once()
            comando = executor.executar.call_args.args[0]
            self.assertEqual((comando.empresa, comando.cargo, comando.descricao), ("Empresa  Local", "Cargo", "A  B\nC"))
            self.assertEqual(comando.usuario_id, UsuarioId(DONO))
            self.assertFalse(hasattr(comando, "hoje"))
            self.assertFalse(hasattr(comando, "fuso"))

    async def test_dominio_retorna_422_generico_sem_vazamento_ou_logs(self):
        """Injeta falha com dados extensos no executor e confere erro público.

        Observa somente a tradução HTTP para provar que a mensagem original não
        é refletida ou logada pelo handler, preservando o status de validação.
        """
        segredo = "TEXTO_PRIVADO_" * 500
        for metodo, dto in DTO_POR_METODO.items():
            handler, _, request = preparar_handler(metodo, RegraDeDominioViolada(segredo))
            with patch("logging.Logger._log") as log:
                with self.assertRaises(HTTPException) as contexto:
                    await chamar_handler(metodo, handler, dto.model_validate(payload()), request)
                log.assert_not_called()
            self.assertEqual(contexto.exception.status_code, 422)
            self.assertNotIn(segredo, contexto.exception.detail)
            self.assertEqual(contexto.exception.detail, f"A experiência informada viola as regras de {'cadastro' if metodo == 'POST' else 'edição'}.")

    async def test_entrada_invalida_nao_invoca_executor(self):
        """Confere bloqueio de formato antes da invocação direta do handler.

        Valida DTO inválido e inspeciona o executor double para impedir passagem
        de textos fora dos limites ao fluxo de gravação da Application.
        """
        for metodo, dto in DTO_POR_METODO.items():
            handler, executor, request = preparar_handler(metodo)
            with self.assertRaises(ValidationError):
                entrada = dto.model_validate(payload(descricao="d" * 5001))
                await chamar_handler(metodo, handler, entrada, request)
            executor.executar.assert_not_called()

    async def test_erro_de_formato_e_sanitizado_so_em_post_e_put(self):
        """Isola o wrapper de rota substituindo o handler de framework por double.

        Simula RequestValidationError com input e corpo confidenciais e confere
        HTTP 422 constante sem logs, sem iniciar contexto ASGI ou testar HTTP real.
        """
        segredo = "DADO_PRIVADO_" * 500
        for metodo in ("POST", "PUT"):
            rota = object.__new__(RotaGravacaoExperiencia)
            rota.methods = {metodo}
            erro = RequestValidationError([
                {"type": "string_too_long", "loc": ("body", "descricao"),
                 "msg": "Texto longo", "input": segredo}
            ], body={"descricao": segredo})
            handler = AsyncMock(side_effect=erro)
            with patch.object(APIRoute, "get_route_handler", return_value=handler):
                executar = rota.get_route_handler()
            with patch("logging.Logger._log") as log:
                with self.assertRaises(HTTPException) as contexto:
                    await executar(Mock())
                log.assert_not_called()
            self.assertEqual(contexto.exception.status_code, 422)
            self.assertEqual(contexto.exception.detail, "Dados da experiência inválidos.")
            self.assertTrue(contexto.exception.__suppress_context__)
        for metodo in ("GET", "DELETE"):
            rota = object.__new__(RotaGravacaoExperiencia)
            rota.methods = {metodo}
            handler = AsyncMock()
            with patch.object(APIRoute, "get_route_handler", return_value=handler):
                self.assertIs(rota.get_route_handler(), handler)

    async def test_erro_inesperado_e_404_nao_sao_reclassificados(self):
        """Confere propagação de erro interno e tradução de ausência na edição.

        Usa falhas configuradas no executor double para preservar semânticas
        anteriores sem mascarar defeitos como validação de entrada.
        """
        for metodo, dto in DTO_POR_METODO.items():
            handler, _, request = preparar_handler(metodo, RuntimeError("falha controlada"))
            with self.assertRaises(RuntimeError):
                await chamar_handler(metodo, handler, dto.model_validate(payload()), request)
        handler, _, request = preparar_handler("PUT", ExperienciaProfissionalNaoEncontrada())
        with self.assertRaises(HTTPException) as contexto:
            await chamar_handler("PUT", handler, EdicaoExperienciaProfissionalRequisicao.model_validate(payload()), request)
        self.assertEqual(contexto.exception.status_code, 404)
