"""Testa a construção unitária das entidades independentes do perfil."""

from datetime import date
import unittest
from uuid import uuid4

from backend.domain import (
    Email,
    FormacaoAcademica,
    FormacaoAcademicaId,
    HashSenha,
    Nome,
    Periodo,
    Usuario,
    UsuarioId,
)


# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
class EntidadesDoDominioTestCase(unittest.TestCase):
    """Verifica entidades com identidade e proprietário explícitos.

    A classe constrói agregados e itens de perfil somente com value objects em
    memória. Ela existe para confirmar que esses conceitos são reutilizáveis sem
    FastAPI, ORM, persistência ou recursos externos.
    """

    def test_usuario_reune_identidade_e_dados_de_conta_tipados(self) -> None:
        """Confirma que o aggregate root de usuário preserva seus value objects.

        O teste monta uma conta válida e compara os objetos recebidos pela
        entidade. Ele existe para assegurar que a primeira fatia não reduz dados
        de conta a DTOs ou strings sem significado de domínio.
        """
        usuario_id = UsuarioId(uuid4())
        usuario = Usuario(
            id=usuario_id,
            nome=Nome("Ana Silva"),
            email=Email("ana.silva@fatec.sp.gov.br"),
            hash_senha=HashSenha("hash-ja-derivado"),
        )

        self.assertIs(usuario.id, usuario_id)
        self.assertEqual(usuario.nome.valor, "Ana Silva")

    def test_formacao_e_item_reutilizavel_com_proprietario_e_periodo(self) -> None:
        """Confirma que uma formação mantém proprietário e intervalo válidos.

        O teste constrói a entidade de perfil separadamente de qualquer currículo
        e inspeciona suas identidades. Ele existe para proteger a decisão de que
        formações podem ser reutilizadas entre versões de currículo.
        """
        usuario_id = UsuarioId(uuid4())
        formacao = FormacaoAcademica(
            id=FormacaoAcademicaId(uuid4()),
            usuario_id=usuario_id,
            instituicao="FATEC",
            curso="Análise e Desenvolvimento de Sistemas",
            nivel="tecnologo",
            periodo=Periodo(date(2024, 2, 1)),
            status="em_andamento",
        )

        self.assertIs(formacao.usuario_id, usuario_id)
        self.assertIsNone(formacao.periodo.fim)
