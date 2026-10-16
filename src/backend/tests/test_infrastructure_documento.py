"""Testes unitários para o adaptador de persistência SQLAlchemy de Documento."""

import unittest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from backend.domain import Documento, DocumentoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.documento import (
    DocumentoRegistro,
    para_documento,
    para_registro,
)
from backend.infrastructure.persistence.sqlalchemy.repositorio_documento import (
    RepositorioDocumentoSqlAlchemy,
)


# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
class TestInfrastructureDocumento(unittest.IsolatedAsyncioTestCase):
    """Testes unitários dos mappers e do repositório SQLAlchemy de Documento.

    A classe verifica a integridade das conversões bidirecionais entre a entidade
    e o modelo ORM, e assegura que as chamadas do repositório interajam corretamente
    com a sessão assíncrona. Ela existe para validar a camada de persistência isoladamente.
    """

    def setUp(self) -> None:
        """Inicializa mocks e instâncias para os cenários de teste.

        O método cria uma AsyncSession mockada e entidades com dados válidos.
        Ele existe para isolar os testes de infraestrutura sem acesso a banco real.
        """
        self.session = AsyncMock()
        self.session.add = MagicMock()
        self.repo = RepositorioDocumentoSqlAlchemy(self.session)
        self.documento_id = DocumentoId(uuid4())
        self.usuario_id = UsuarioId(uuid4())
        self.documento = Documento(
            id=self.documento_id,
            usuario_id=self.usuario_id,
            nome_arquivo="historico.pdf",
            tipo_arquivo="application/pdf",
            url_armazenamento="https://storage.local/historico.pdf",
        )

    def test_conversao_bidirecional_entre_entidade_e_registro(self) -> None:
        """Verifica a equivalência de dados entre Documento e DocumentoRegistro.

        O teste converte a entidade para registro e depois de volta para entidade,
        validando a preservação de todos os atributos. Ele existe para garantir
        fidelidade na serialização e deserialização ORM.
        """
        registro = para_registro(self.documento)
        self.assertEqual(registro.id, self.documento.id.valor)
        self.assertEqual(registro.usuario_id, self.documento.usuario_id.valor)
        self.assertEqual(registro.nome_arquivo, self.documento.nome_arquivo)
        self.assertEqual(registro.tipo_arquivo, self.documento.tipo_arquivo)
        self.assertEqual(registro.url_armazenamento, self.documento.url_armazenamento)

        registro.created_at = datetime.now(timezone.utc)
        entidade_reconstruida = para_documento(registro)
        self.assertEqual(entidade_reconstruida.id, self.documento.id)
        self.assertEqual(entidade_reconstruida.usuario_id, self.documento.usuario_id)
        self.assertEqual(
            entidade_reconstruida.nome_arquivo, self.documento.nome_arquivo
        )
        self.assertEqual(
            entidade_reconstruida.tipo_arquivo, self.documento.tipo_arquivo
        )
        self.assertEqual(
            entidade_reconstruida.url_armazenamento,
            self.documento.url_armazenamento,
        )

    async def test_obter_por_id_retorna_documento_quando_encontrado(self) -> None:
        """Verifica a recuperação bem-sucedida do documento a partir da sessão.

        O teste configura o retorno do scalar da sessão com um registro válido
        e confirma que o método devolve a entidade correspondente. Ele existe
        para certificar o mapeamento da consulta.
        """
        registro_mock = MagicMock(spec=DocumentoRegistro)
        registro_mock.id = self.documento_id.valor
        registro_mock.usuario_id = self.usuario_id.valor
        registro_mock.nome_arquivo = "comprovante.pdf"
        registro_mock.tipo_arquivo = "application/pdf"
        registro_mock.url_armazenamento = "https://storage.local/1.pdf"
        self.session.scalar.return_value = registro_mock

        resultado = await self.repo.obter_por_id(self.documento_id)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, self.documento_id)  # type: ignore[union-attr]
        self.session.scalar.assert_called_once()

    async def test_obter_por_id_retorna_none_quando_inexistente(self) -> None:
        """Verifica que obter_por_id devolve None caso o scalar retorne None.

        O teste configura scalar para None e valida o tratamento neutro de ausência.
        Ele existe para validar o contrato quando o registro não existe ou foi excluído.
        """
        self.session.scalar.return_value = None

        resultado = await self.repo.obter_por_id(self.documento_id)

        self.assertIsNone(resultado)
        self.session.scalar.assert_called_once()

    async def test_excluir_executa_update_e_flush(self) -> None:
        """Verifica que o método excluir envia UPDATE e flush para a sessão.

        O teste invoca excluir e confere as interações com a sessão assíncrona.
        Ele existe para confirmar o disparo correto da mutação no banco.
        """
        await self.repo.excluir(self.documento)

        self.session.execute.assert_called_once()
        self.session.flush.assert_called_once()

    async def test_salvar_adiciona_registro_e_chama_flush(self) -> None:
        """Verifica que o método salvar adiciona o registro e chama flush.

        O teste invoca salvar e valida que session.add e session.flush foram acionados.
        Ele existe para assegurar a persistência de novos documentos.
        """
        await self.repo.salvar(self.documento)

        self.session.add.assert_called_once()
        self.session.flush.assert_called_once()


if __name__ == "__main__":
    unittest.main()
