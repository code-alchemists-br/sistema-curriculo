"""Testes unitários para a entidade Documento e suas invariantes de domínio."""

import unittest
from uuid import uuid4

from backend.domain import Documento, DocumentoId, RegraDeDominioViolada, UsuarioId


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
class TestDomainDocumento(unittest.TestCase):
    """Conjunto de testes das regras e invariantes da entidade Documento.

    A classe verifica a criação válida, aparamento de textos e rejeição de
    valores nulos, vazios ou com tipos incompatíveis. Ela existe para garantir que
    instâncias de Documento respeitem sempre os limites e garantias do domínio.
    """

    def setUp(self) -> None:
        """Prepara identificadores válidos para os cenários de teste.

        O método inicializa IDs únicos para usuário e documento. Ele existe para
        fornecer insumos válidos e isolados para cada método de teste.
        """
        self.usuario_id = UsuarioId(uuid4())
        self.documento_id = DocumentoId(uuid4())

    def test_documento_valido_e_instanciado_com_sucesso(self) -> None:
        """Verifica a criação correta com dados válidos e aparamento de espaços.

        O teste instancia Documento com espaços laterais nos campos textuais e
        assegura que os atributos sejam preservados devidamente aparados. Ele existe
        para validar a construção padrão esperada pelo domínio.
        """
        doc = Documento(
            id=self.documento_id,
            usuario_id=self.usuario_id,
            nome_arquivo="  diploma_graduacao.pdf  ",
            tipo_arquivo="  application/pdf  ",
            url_armazenamento="  https://storage.empresa.com/docs/123.pdf  ",
        )
        self.assertEqual(doc.id, self.documento_id)
        self.assertEqual(doc.usuario_id, self.usuario_id)
        self.assertEqual(doc.nome_arquivo, "diploma_graduacao.pdf")
        self.assertEqual(doc.tipo_arquivo, "application/pdf")
        self.assertEqual(
            doc.url_armazenamento, "https://storage.empresa.com/docs/123.pdf"
        )

    def test_rejeita_identificador_documento_invalido(self) -> None:
        """Verifica que identificador de documento não tipado é rejeitado.

        O teste passa uma string em vez de DocumentoId e confirma a exceção
        RegraDeDominioViolada. Ele existe para impedir desvios de tipagem rica.
        """
        with self.assertRaises(RegraDeDominioViolada) as ctx:
            Documento(
                id="invalido",  # type: ignore[arg-type]
                usuario_id=self.usuario_id,
                nome_arquivo="arquivo.pdf",
                tipo_arquivo="application/pdf",
                url_armazenamento="https://storage.empresa.com/1.pdf",
            )
        self.assertIn("Identificador de documento inválido", str(ctx.exception))

    def test_rejeita_identificador_usuario_invalido(self) -> None:
        """Verifica que identificador de usuário não tipado é rejeitado.

        O teste passa None no lugar de UsuarioId e confirma o lançamento de
        RegraDeDominioViolada. Ele existe para proteger a integridade da posse.
        """
        with self.assertRaises(RegraDeDominioViolada) as ctx:
            Documento(
                id=self.documento_id,
                usuario_id=None,  # type: ignore[arg-type]
                nome_arquivo="arquivo.pdf",
                tipo_arquivo="application/pdf",
                url_armazenamento="https://storage.empresa.com/1.pdf",
            )
        self.assertIn("Identificador de usuário inválido", str(ctx.exception))

    def test_rejeita_nome_arquivo_vazio_ou_invalido(self) -> None:
        """Verifica a obrigatoriedade e validação textual de nome_arquivo.

        O teste testa valores vazios, compostos por espaços e tipos não textuais,
        esperando RegraDeDominioViolada. Ele existe para garantir que todo documento tenha nome.
        """
        for invalido in ["", "   ", None, 123]:
            with self.subTest(nome=invalido):
                with self.assertRaises(RegraDeDominioViolada) as ctx:
                    Documento(
                        id=self.documento_id,
                        usuario_id=self.usuario_id,
                        nome_arquivo=invalido,  # type: ignore[arg-type]
                        tipo_arquivo="application/pdf",
                        url_armazenamento="https://storage.empresa.com/1.pdf",
                    )
                self.assertIn("nome do arquivo", str(ctx.exception))

    def test_rejeita_tipo_arquivo_vazio_ou_invalido(self) -> None:
        """Verifica a obrigatoriedade de tipo_arquivo não vazio.

        O teste testa strings vazias e tipos incorretos para o tipo de arquivo.
        Ele existe para assegurar integridade no formato do documento.
        """
        for invalido in ["", "   ", None, 456]:
            with self.subTest(tipo=invalido):
                with self.assertRaises(RegraDeDominioViolada) as ctx:
                    Documento(
                        id=self.documento_id,
                        usuario_id=self.usuario_id,
                        nome_arquivo="comprovante.png",
                        tipo_arquivo=invalido,  # type: ignore[arg-type]
                        url_armazenamento="https://storage.empresa.com/1.png",
                    )
                self.assertIn("tipo do arquivo", str(ctx.exception))

    def test_rejeita_url_armazenamento_vazia_ou_invalida(self) -> None:
        """Verifica que url_armazenamento não pode ser vazia ou não textual.

        O teste valida que URLs nulas, vazias ou não-strings disparam erro.
        Ele existe para garantir rastreabilidade física do documento armazenado.
        """
        for invalido in ["", "   ", None, 789]:
            with self.subTest(url=invalido):
                with self.assertRaises(RegraDeDominioViolada) as ctx:
                    Documento(
                        id=self.documento_id,
                        usuario_id=self.usuario_id,
                        nome_arquivo="comprovante.png",
                        tipo_arquivo="image/png",
                        url_armazenamento=invalido,  # type: ignore[arg-type]
                    )
                self.assertIn("URL de armazenamento", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
