"""Testa o contrato interno de busca de vagas da Application."""

import unittest
from dataclasses import FrozenInstanceError, fields
from inspect import iscoroutinefunction, signature
from typing import Any, get_type_hints

from backend.application.ports import BuscadorVagas, VagaExternaDto


# Proveniência: decision-analysis prompts/backend/20261009-110249-contrato-adaptador-busca-vagas-v002.md#v002
class ContratoBuscaVagasTestCase(unittest.TestCase):
    """Verifica a forma tipada e imutavel do contrato interno de busca.

    Os testes inspecionam o DTO e a assinatura da porta sem instanciar adapter,
    acessar rede ou importar o pacote de doubles. A classe existe para evitar
    deriva do contrato aprovado para a issue #124.
    """

    def test_dto_preserva_campos_e_tipos_aprovados(self) -> None:
        """Confirma os oito campos e tipos definidos para o DTO de vaga.

        O teste compara a ordem dos campos e suas anotações com a baseline da
        decisão. Ele existe para detectar alterações não aprovadas no contrato.
        """
        self.assertEqual(
            [campo.name for campo in fields(VagaExternaDto)],
            [
                "id",
                "titulo",
                "empresa",
                "descricao",
                "requisitos",
                "localizacao",
                "modalidade",
                "url_candidatura",
            ],
        )
        self.assertEqual(
            get_type_hints(VagaExternaDto),
            {
                "id": str,
                "titulo": str,
                "empresa": str,
                "descricao": str,
                "requisitos": tuple[str, ...],
                "localizacao": str,
                "modalidade": str,
                "url_candidatura": str,
            },
        )

    def test_dto_e_imutavel(self) -> None:
        """Confirma que os campos de uma vaga nao podem ser alterados.

        O teste cria o DTO com todos os campos obrigatorios e tenta substituir
        um atributo. Ele existe para preservar a imutabilidade da referencia.
        """
        vaga = VagaExternaDto(
            id="vaga-1",
            titulo="Desenvolvedor",
            empresa="Empresa",
            descricao="Descricao",
            requisitos=("Python",),
            localizacao="Remoto",
            modalidade="Remoto",
            url_candidatura="https://example.test/vagas/1",
        )

        with self.assertRaises(FrozenInstanceError):
            vaga.titulo = "Outro titulo"

    def test_porta_preserva_assinatura_assincrona_aprovada(self) -> None:
        """Confirma metodo, argumentos, defaults e tipo de retorno da porta.

        O teste inspeciona o Protocol sem chamar qualquer implementação. Ele
        existe para garantir que a porta permaneca alinhada ao modelo aprovado.
        """
        metodo = BuscadorVagas.buscar_vagas
        assinatura = signature(metodo)
        anotacoes = get_type_hints(metodo)

        self.assertTrue(iscoroutinefunction(metodo))
        self.assertEqual(list(assinatura.parameters), ["self", "termo", "filtros"])
        self.assertEqual(assinatura.parameters["termo"].default, "")
        self.assertIsNone(assinatura.parameters["filtros"].default)
        self.assertEqual(
            anotacoes,
            {
                "termo": str,
                "filtros": dict[str, Any] | None,
                "return": list[VagaExternaDto],
            },
        )
