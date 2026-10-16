"""Testa o contrato interno do assistente de descrição de projeto."""

import unittest
from dataclasses import FrozenInstanceError, fields
from inspect import iscoroutinefunction, signature
from typing import get_type_hints

from backend.application.assistente_descricao_projeto import (
    AssistenteDescricaoProjeto,
    AssistenteDescricaoProjetoAusente,
    AssistenteDescricaoProjetoEntrada,
    AssistenteDescricaoProjetoIndisponivel,
    AssistenteDescricaoProjetoSaida,
)


class ContratoAssistenteDescricaoProjetoTestCase(
    unittest.IsolatedAsyncioTestCase
):
    """Verifica entrada, saída, porta, erro e implementação ausente.

    Os testes exercitam somente o contrato do assistente, sem acessar rede,
    banco ou serviços externos. A classe existe para tornar a issue #198
    verificável isoladamente.
    """

    def test_entrada_preserva_campos_e_tipos(self) -> None:
        """Confirma os campos e tipos definidos para a entrada.

        O teste inspeciona a dataclass sem depender de implementação externa.
        Ele existe para proteger o contrato contra alterações acidentais.
        """
        self.assertEqual(
            [campo.name for campo in fields(AssistenteDescricaoProjetoEntrada)],
            ["titulo", "tecnologias"],
        )

        self.assertEqual(
            get_type_hints(AssistenteDescricaoProjetoEntrada),
            {
                "titulo": str,
                "tecnologias": str,
            },
        )

    def test_saida_preserva_campo_e_tipo(self) -> None:
        """Confirma o campo e o tipo definidos para a saída.

        O teste verifica somente o contrato de retorno. Ele existe para manter
        o consumidor independente da estratégia utilizada.
        """
        self.assertEqual(
            [campo.name for campo in fields(AssistenteDescricaoProjetoSaida)],
            ["descricao"],
        )

        self.assertEqual(
            get_type_hints(AssistenteDescricaoProjetoSaida),
            {
                "descricao": str,
            },
        )

    def test_entrada_e_saida_sao_imutaveis(self) -> None:
        """Confirma que entrada e saída permanecem imutáveis.

        O teste tenta alterar os atributos após a construção. Ele existe para
        manter o transporte de dados previsível entre implementações.
        """
        entrada = AssistenteDescricaoProjetoEntrada(
            titulo="Sistema Currículo",
            tecnologias="Python, FastAPI",
        )

        saida = AssistenteDescricaoProjetoSaida(
            descricao="Projeto para organização de currículos."
        )

        with self.assertRaises(FrozenInstanceError):
            entrada.titulo = "Outro título"

        with self.assertRaises(FrozenInstanceError):
            saida.descricao = "Outra descrição"

    def test_porta_preserva_assinatura_assincrona(self) -> None:
        """Confirma método, entrada e retorno definidos pela porta.

        O teste inspeciona o Protocol sem executar uma implementação concreta.
        Ele existe para manter estável a interface do assistente.
        """
        metodo = AssistenteDescricaoProjeto.sugerir_descricao
        assinatura = signature(metodo)
        anotacoes = get_type_hints(metodo)

        self.assertTrue(iscoroutinefunction(metodo))

        self.assertEqual(
            list(assinatura.parameters),
            ["self", "entrada"],
        )

        self.assertEqual(
            anotacoes,
            {
                "entrada": AssistenteDescricaoProjetoEntrada,
                "return": AssistenteDescricaoProjetoSaida,
            },
        )

    async def test_implementacao_ausente_falha_de_forma_controlada(
        self,
    ) -> None:
        """Confirma a falha específica quando o assistente está ausente.

        O teste utiliza somente a implementação vazia definida no contrato.
        Ele existe para garantir comportamento previsível sem estratégia ativa.
        """
        assistente = AssistenteDescricaoProjetoAusente()

        entrada = AssistenteDescricaoProjetoEntrada(
            titulo="Sistema Currículo",
            tecnologias="Python, FastAPI",
        )

        with self.assertRaises(AssistenteDescricaoProjetoIndisponivel):
            await assistente.sugerir_descricao(entrada)
