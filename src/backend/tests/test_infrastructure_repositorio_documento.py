"""Testa o repositório de documentos complementares com sessão substituída."""

import unittest
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

# Proveniência: decision-analysis prompts/backend/20261026-150000-testes-exclusao-logica-documento-v001.md#v001
from backend.domain.itens_perfil import Documento
from backend.domain.value_objects import DocumentoId, UsuarioId
from backend.infrastructure.persistence.sqlalchemy.documento import DocumentoRegistro
from backend.infrastructure.persistence.sqlalchemy.repositorio_documento import (
    RepositorioDocumentoSqlAlchemy,
)


def _documento(**alteracoes) -> Documento:
    """Cria um documento complementar válido, aceitando alterações pontuais.

    A função monta a entidade com valores determinísticos e sobrescreve só o que
    o teste pedir. Ela existe para que cada teste destaque um único campo.
    """
    campos = {
        "id": DocumentoId(uuid4()),
        "usuario_id": UsuarioId(uuid4()),
        "nome_arquivo": "historico.pdf",
        "tipo_arquivo": "application/pdf",
        "url_armazenamento": "https://storage.local/documentos/" + "a" * 32,
    }
    campos.update(alteracoes)
    return Documento(**campos)


def _registro(documento: Documento) -> SimpleNamespace:
    """Cria um registro ORM simulado com os valores do documento informado.

    A função expõe as colunas que o mapeador lê, sem sessão ou tabela. Ela existe
    para controlar o que a consulta devolve em cada cenário.
    """
    return SimpleNamespace(
        id=documento.id.valor,
        usuario_id=documento.usuario_id.valor,
        nome_arquivo=documento.nome_arquivo,
        tipo_arquivo=documento.tipo_arquivo,
        url_armazenamento=documento.url_armazenamento,
        deleted_at=documento.deleted_at,
    )


def _sessao(registro: SimpleNamespace | None = None) -> MagicMock:
    """Cria uma sessão assíncrona substituída que devolve o registro informado.

    A função devolve um mock com a interface de ``AsyncSession`` cujo
    ``execute`` entrega o registro (ou nenhum) como resultado escalar. Ela existe
    para observar o que o repositório pede à sessão sem I/O.
    """
    sessao = MagicMock(spec=AsyncSession)
    resultado = MagicMock(scalar_one_or_none=MagicMock(return_value=registro))
    sessao.execute = AsyncMock(return_value=resultado)
    sessao.flush = AsyncMock()
    return sessao


class RepositorioDocumentoSqlAlchemyTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a gravação, a leitura e a exclusão lógica pelo adapter.

    A sessão é substituída por doubles, e os testes observam as chamadas, o SQL
    gerado e o resultado. A classe existe para proteger a regra de que documento
    excluído deixa de ser encontrado e de que a exclusão não apaga o registro.
    """

    async def test_salva_o_documento_adicionando_o_registro_e_aguardando_flush(self) -> None:
        """Confirma que salvar adiciona o registro convertido e envia o flush.

        O teste salva um documento e confere o registro adicionado. Ele existe
        para o caminho de inserção.
        """
        sessao = _sessao()
        documento = _documento()

        await RepositorioDocumentoSqlAlchemy(sessao).salvar(documento)

        sessao.add.assert_called_once()
        registro = sessao.add.call_args.args[0]
        self.assertIsInstance(registro, DocumentoRegistro)
        self.assertEqual(registro.id, documento.id.valor)
        self.assertEqual(registro.usuario_id, documento.usuario_id.valor)
        sessao.flush.assert_awaited_once()

    async def test_obtem_o_documento_ativo_pelo_identificador(self) -> None:
        """Confirma que a leitura devolve o documento do registro encontrado.

        O teste faz a sessão devolver um registro e confere a conversão para o
        domínio e o filtro da consulta por identificador e por documento ativo.
        """
        documento = _documento()
        sessao = _sessao(_registro(documento))

        resultado = await RepositorioDocumentoSqlAlchemy(sessao).obter_por_id(documento.id)

        self.assertEqual(resultado, documento)
        consulta = sessao.execute.await_args.args[0]
        sql = str(consulta)
        self.assertIn("documentos.id", sql)
        self.assertIn("documentos.deleted_at IS NULL", sql)
        self.assertIn(documento.id.valor, set(consulta.compile().params.values()))

    async def test_devolve_none_quando_nao_ha_documento_ativo(self) -> None:
        """Confirma que a leitura devolve ``None`` sem registro ativo.

        O teste faz a consulta não encontrar nada, como ocorre com um documento
        excluído logicamente. Ele existe para que o excluído não seja devolvido.
        """
        resultado = await RepositorioDocumentoSqlAlchemy(_sessao(None)).obter_por_id(
            DocumentoId(uuid4())
        )

        self.assertIsNone(resultado)

    async def test_exclusao_marca_deleted_at_sem_apagar_o_registro(self) -> None:
        """Confirma que excluir faz UPDATE de ``deleted_at``, e não DELETE.

        O teste inspeciona a instrução enviada e o instante gravado. Ele existe
        para garantir a exclusão lógica: o registro permanece, marcado, com um
        instante com fuso.
        """
        sessao = _sessao()
        documento = _documento()

        await RepositorioDocumentoSqlAlchemy(sessao).excluir(documento)

        instrucao = sessao.execute.await_args.args[0]
        sql = str(instrucao)
        self.assertTrue(sql.startswith("UPDATE documentos SET deleted_at"))
        self.assertNotIn("DELETE", sql)
        parametros = instrucao.compile().params
        instante = parametros["deleted_at"]
        self.assertIsInstance(instante, datetime)
        self.assertIsNotNone(instante.tzinfo)
        self.assertIn(documento.id.valor, parametros.values())
        sessao.flush.assert_awaited_once()

    async def test_exclusao_atinge_somente_o_registro_ainda_ativo(self) -> None:
        """Confirma que o UPDATE filtra o documento e só afeta quem não foi excluído.

        O teste lê as condições da instrução. Ele existe para que excluir de novo
        não sobrescreva o instante da primeira exclusão.
        """
        sessao = _sessao()

        await RepositorioDocumentoSqlAlchemy(sessao).excluir(_documento())

        sql = str(sessao.execute.await_args.args[0])
        self.assertIn("documentos.id = :id_1", sql)
        self.assertIn("documentos.deleted_at IS NULL", sql)

    async def test_documento_excluido_mantem_o_instante_na_conversao(self) -> None:
        """Confirma que um registro já excluído preserva o instante ao voltar ao domínio.

        O teste converte um registro com ``deleted_at`` preenchido. Ele existe
        para que quem receber o documento possa recusar um excluído.
        """
        excluido = _documento(deleted_at=datetime(2026, 10, 26, 12, 0, tzinfo=UTC))
        sessao = _sessao(_registro(excluido))

        resultado = await RepositorioDocumentoSqlAlchemy(sessao).obter_por_id(excluido.id)

        self.assertEqual(resultado.deleted_at, excluido.deleted_at)
