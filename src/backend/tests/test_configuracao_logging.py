"""Verifica a configuração ambiental do nível de logging."""

import logging
import os
import unittest
from unittest.mock import patch

from backend.configuracao_logging import configurar_logging


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
