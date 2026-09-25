"""Testa unitariamente o caso de uso de cadastro de certificação."""

import unittest
from uuid import uuid4

from backend.application.cadastro_certificacao import (
    CadastrarCertificacao,
    CadastrarCertificacaoEntrada,
)
from backend.domain.itens_perfil import Certificacao
from backend.domain.value_objects import CertificacaoId, UsuarioId


class RepositorioCertificacaoSpy:
    """Substitui assincronamente a porta e regista as certificações persistidas."""

    def __init__(self) -> None:
        self.certificacoes_salvas: list[Certificacao] = []

    async def salvar(self, certificacao: Certificacao) -> None:
        self.certificacoes_salvas.append(certificacao)


class GeradorCertificacaoIdStub:
    """Substitui a geração de ID por uma identidade determinística."""

    def __init__(self, certificacao_id: CertificacaoId) -> None:
        self._certificacao_id = certificacao_id
        self.chamadas = 0

    def gerar(self) -> CertificacaoId:
        self.chamadas += 1
        return self._certificacao_id


class CadastrarCertificacaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a orquestração do cadastro de certificação."""

    async def test_cadastra_certificacao_e_solicita_salvamento_com_sucesso(self) -> None:
        certificacao_id = CertificacaoId(uuid4())
        usuario_id = UsuarioId(uuid4())
        repositorio = RepositorioCertificacaoSpy()
        gerador = GeradorCertificacaoIdStub(certificacao_id)
        caso_de_uso = CadastrarCertificacao(repositorio, gerador)

        entrada = CadastrarCertificacaoEntrada(
            usuario_id=usuario_id,
            nome="AWS Certified Cloud Practitioner",
            organizacao_emissora="Amazon Web Services",
        )

        certificacao = await caso_de_uso.executar(entrada)

        self.assertEqual(certificacao.id, certificacao_id)
        self.assertEqual(certificacao.usuario_id, usuario_id)
        self.assertEqual(certificacao.nome, "AWS Certified Cloud Practitioner")
        self.assertEqual(certificacao.organizacao_emissora, "Amazon Web Services")
        self.assertEqual(repositorio.certificacoes_salvas, [certificacao])
        self.assertEqual(gerador.chamadas, 1)