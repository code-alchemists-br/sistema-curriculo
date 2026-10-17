"""Verifica a configuração ambiental do nível de logging."""

import logging
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch

from backend.configuracao_logging import (
    FiltroMascaramentoDadosPessoais,
    configurar_logging,
    pseudonimizar_identificador_ator,
)


class ConfiguracaoLoggingTestCase(unittest.TestCase):
    """Configura o nível global de logs conforme o ambiente da aplicação."""

    def setUp(self) -> None:
        """Guarda o nível anterior para isolar a configuração do teste.

        O teste altera o logger raiz como faria a inicialização do backend. A
        restauração evita que a configuração de um cenário afete outros testes.
        """
        self.nivel_original = logging.getLogger().level

    def tearDown(self) -> None:
        """Restaura o nível global de logging anterior ao cenário.

        O logger raiz recupera o valor salvo em `setUp`; isso mantém os testes
        independentes e evita efeitos colaterais no processo de unittest.
        """
        logging.getLogger().setLevel(self.nivel_original)

    def test_mascara_dados_pessoais_em_mensagem_argumentos_e_campos_extras(self) -> None:
        """Mascarar dados pessoais antes de liberar um registro ao handler.

        O teste sanitiza mensagem, argumento posicional e campos estruturados
        contendo e-mail, CPF, telefone e ID de ator. Ele existe para garantir
        que dados pessoais usados acidentalmente em logs não sejam persistidos.
        """
        registro = logging.LogRecord(
            "teste",
            logging.WARNING,
            __file__,
            1,
            "email=%s telefone=11988887777",
            ("ana@example.com",),
            None,
        )
        registro.cpf = "123.456.789-00"
        registro.ator_id = "usuario-123"
        registro.correlation_id = "08c855d2-6331-40f5-a0f4-b"

        self.assertTrue(FiltroMascaramentoDadosPessoais().filter(registro))

        mensagem = registro.getMessage()
        self.assertNotIn("ana@example.com", mensagem)
        self.assertNotIn("11988887777", mensagem)
        self.assertNotIn("123.456.789-00", str(registro.cpf))
        self.assertEqual(registro.cpf, "[REDACTED]")
        self.assertEqual(registro.ator_id, "[REDACTED]")
        self.assertEqual(registro.correlation_id, "08c855d2-6331-40f5-a0f4-b")

    def test_mascara_id_de_ator_no_texto_sem_alterar_correlacao(self) -> None:
        """Redige IDs de ator em texto e preserva IDs técnicos de correlação.

        O teste verifica os limites dos padrões numéricos e do nome de campo
        sensível. Ele existe para proteger dados de usuário sem quebrar a
        capacidade de correlacionar eventos da mesma requisição.
        """
        correlation_id = "08c855d2-6331-40f5-a0f4-b"
        registro = logging.LogRecord(
            "teste",
            logging.INFO,
            __file__,
            1,
            "ator_id=12345678 correlation_id=%s",
            (correlation_id,),
            None,
        )

        FiltroMascaramentoDadosPessoais().filter(registro)

        self.assertEqual(
            registro.getMessage(),
            f"ator_id=[REDACTED] correlation_id={correlation_id}",
        )

        registro_autorizacao = logging.LogRecord(
            "teste",
            logging.INFO,
            __file__,
            1,
            "authorization=Bearer segredo privado",
            (),
            None,
        )
        FiltroMascaramentoDadosPessoais().filter(registro_autorizacao)
        self.assertEqual(registro_autorizacao.getMessage(), "authorization=[REDACTED]")

        for cabecalho in (
            "Authorization: Bearer segredo-super-secreto",
            "Set-Cookie: __Host-sessao=token-super-secreto; Path=/; Secure",
            "email=ana%40example.com&access_token=token-super-secreto",
        ):
            with self.subTest(cabecalho=cabecalho):
                registro_cabecalho = logging.LogRecord(
                    "teste", logging.INFO, __file__, 1, cabecalho, (), None
                )
                FiltroMascaramentoDadosPessoais().filter(registro_cabecalho)
                mensagem = registro_cabecalho.getMessage()
                self.assertNotIn("segredo-super-secreto", mensagem)
                self.assertNotIn("token-super-secreto", mensagem)
                self.assertNotIn("ana%40example.com", mensagem)

    def test_mascara_campos_sensiveis_em_extras_aninhados(self) -> None:
        """Protege chaves sensíveis mesmo dentro de estruturas extras.

        O cenário cria um campo estruturado com e-mail e senha e verifica a
        substituição dos dois valores. Ele existe para cobrir formatos de log
        JSON ou eventos com dados pessoais aninhados.
        """
        registro = logging.LogRecord(
            "teste", logging.INFO, __file__, 1, "evento", (), None
        )
        registro.dados = {
            "email": "ana@example.com",
            "detalhes": {"senha": "secreta", "nota": "contato ana@example.com"},
        }

        FiltroMascaramentoDadosPessoais().filter(registro)

        self.assertEqual(registro.dados["email"], "[REDACTED]")
        self.assertEqual(registro.dados["detalhes"]["senha"], "[REDACTED]")
        self.assertNotIn("ana@example.com", registro.dados["detalhes"]["nota"])

    def test_mascara_dados_pessoais_em_excecoes(self) -> None:
        """Remove dados pessoais da representação de exceções registradas.

        O cenário formata uma exceção que inclui um endereço de e-mail e
        verifica o texto anexado ao log. Ele existe para evitar vazamentos por
        meio de stack traces, além da mensagem principal.
        """
        try:
            raise ValueError("falha para ana@example.com")
        except ValueError:
            registro = logging.LogRecord(
                "teste",
                logging.ERROR,
                __file__,
                1,
                "falha",
                (),
                sys.exc_info(),
            )

        FiltroMascaramentoDadosPessoais().filter(registro)

        self.assertIsNone(registro.exc_info)
        self.assertNotIn("ana@example.com", registro.exc_text)

    def test_configuracao_instala_filtro_em_handlers_nomeados_e_raiz(self) -> None:
        """Instala a sanitização nos handlers raiz e de loggers nomeados.

        O teste cria handlers temporários nos dois níveis e consulta seus
        filtros após a configuração. Ele existe para proteger também logs de
        servidores ASGI que usam handlers próprios, como o access logger.
        """
        logger_raiz = logging.getLogger()
        logger_nomeado = logging.getLogger("uvicorn.access")
        handler_raiz = logging.NullHandler()
        saida = StringIO()
        handler_nomeado = logging.StreamHandler(saida)
        nivel_original = logger_nomeado.level
        propagacao_original = logger_nomeado.propagate
        logger_nomeado.setLevel(logging.WARNING)
        logger_nomeado.propagate = False
        logger_raiz.addHandler(handler_raiz)
        logger_nomeado.addHandler(handler_nomeado)
        try:
            with (
                patch.dict(os.environ, {"LOG_LEVEL": "INFO"}),
                patch("backend.configuracao_logging.logging.basicConfig"),
            ):
                configurar_logging()

            self.assertTrue(
                any(
                    isinstance(filtro, FiltroMascaramentoDadosPessoais)
                    for filtro in handler_raiz.filters
                )
            )
            self.assertTrue(
                any(
                    isinstance(filtro, FiltroMascaramentoDadosPessoais)
                    for filtro in handler_nomeado.filters
                )
            )
            logger_nomeado.warning("Authorization: Bearer segredo-super-secreto")
            self.assertIn("Authorization: [REDACTED]", saida.getvalue())
            self.assertNotIn("segredo-super-secreto", saida.getvalue())
        finally:
            logger_raiz.removeHandler(handler_raiz)
            logger_nomeado.removeHandler(handler_nomeado)
            logger_nomeado.setLevel(nivel_original)
            logger_nomeado.propagate = propagacao_original
            handler_raiz.close()
            handler_nomeado.close()

    def test_pseudonimiza_identificador_de_ator_de_forma_estavel(self) -> None:
        """Produz referência estável sem reproduzir o identificador original.

        O cenário transforma duas vezes o mesmo identificador técnico e
        compara forma e estabilidade do HMAC. Ele existe para manter vínculo de
        auditoria sem registrar diretamente a identidade da conta.
        """
        identificador = "00000000-0000-0000-0000-000000000001"

        referencia = pseudonimizar_identificador_ator(identificador)

        self.assertEqual(
            pseudonimizar_identificador_ator(identificador), referencia
        )
        self.assertRegex(referencia, r"^[0-9a-f]{24}$")
        self.assertNotEqual(referencia, identificador)

    def test_usa_info_quando_log_level_nao_esta_definida(self) -> None:
        """Aplica INFO como padrão quando não há configuração no ambiente.

        O teste remove `LOG_LEVEL`, intercepta a criação do handler padrão e
        verifica o nível aplicado ao logger raiz. Ele existe para definir uma
        inicialização previsível sem exigir variável de ambiente.
        """
        with (
            patch.dict(os.environ, {}, clear=True),
            patch("backend.configuracao_logging.logging.basicConfig") as basic_config,
        ):
            configurar_logging()

        basic_config.assert_called_once_with(level=logging.INFO)
        self.assertEqual(logging.getLogger().level, logging.INFO)

    def test_aplica_todos_os_niveis_permitidos_sem_diferenciar_caixa(self) -> None:
        """Aceita os níveis documentados mesmo quando escritos em minúsculas.

        O cenário percorre cada nível permitido e verifica a configuração do
        logger raiz e do logging padrão. Ele existe para proteger o contrato
        público da variável de ambiente `LOG_LEVEL`.
        """
        for nome, nivel in (
            ("DEBUG", logging.DEBUG),
            ("INFO", logging.INFO),
            ("WARNING", logging.WARNING),
            ("ERROR", logging.ERROR),
            ("CRITICAL", logging.CRITICAL),
        ):
            with self.subTest(nivel=nome):
                with (
                    patch.dict(os.environ, {"LOG_LEVEL": f" {nome.lower()} "}),
                    patch(
                        "backend.configuracao_logging.logging.basicConfig"
                    ) as basic_config,
                ):
                    configurar_logging()

                basic_config.assert_called_once_with(level=nivel)
                self.assertEqual(logging.getLogger().level, nivel)

    def test_rejeita_nivel_nao_permitido_com_mensagem_explicativa(self) -> None:
        """Interrompe a inicialização quando `LOG_LEVEL` é desconhecido.

        O cenário fornece um valor fora da lista aceita e confere que a exceção
        enumera as opções válidas. Ele existe para evitar configurações
        silenciosamente ignoradas em produção.
        """
        with (
            patch.dict(os.environ, {"LOG_LEVEL": "TRACE"}),
            patch("backend.configuracao_logging.logging.basicConfig") as basic_config,
        ):
            with self.assertRaisesRegex(
                ValueError,
                r"LOG_LEVEL inválido: 'TRACE'.*CRITICAL, DEBUG, ERROR, INFO, WARNING",
            ):
                configurar_logging()

        basic_config.assert_not_called()
