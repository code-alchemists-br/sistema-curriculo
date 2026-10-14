"""Verifica a persistência integrada dos campos pessoais em SQLite descartável.

Os cenários passam pelos mapeadores ORM e por uma base SQLite real em memória,
gravando e recarregando perfis sem acessar serviço externo. Eles existem para
validar a fatia de persistência disponível para a consulta pessoal do estudante.
"""

import unittest
from uuid import UUID

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import (
    Cidade,
    DadosContato,
    Email,
    Endereco,
    HashSenha,
    Nome,
    Telefone,
    Usuario,
    UsuarioId,
)
from backend.infrastructure.persistence.sqlalchemy.usuario import (
    Base,
    UsuarioRegistro,
    para_registro,
    para_usuario,
)

# Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005


class PersistenciaDadosPessoaisIntegracaoTestCase(unittest.TestCase):
    """Exercita mapeamento ORM e banco SQLite em memória.

    Cada caso usa uma engine descartável, persiste o registro e o lê em uma
    sessão nova. A classe existe para verificar a recuperação real dos campos
    de contato sem depender de banco compartilhado.
    """

    def setUp(self) -> None:
        """Cria o schema e uma fábrica de sessões isoladas para o cenário.

        A engine SQLite mantém o banco somente em memória durante o teste e
        compartilha sua conexão no pool local. Ela existe para exercitar o ORM
        sem criar recursos persistentes fora da suíte.
        """
        self.engine = create_engine(
            "sqlite+pysqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.criar_sessao = sessionmaker(
            bind=self.engine,
            class_=Session,
            expire_on_commit=False,
        )

    def tearDown(self) -> None:
        """Descarta a conexão SQLite após cada cenário.

        O descarte fecha os recursos locais da engine ao terminar o teste. Ele
        existe para impedir compartilhamento de estado entre cenários.
        """
        self.engine.dispose()

    def test_recarrega_campos_pessoais_persistidos_em_nova_sessao(self) -> None:
        """Confirma que contato e perfil sobrevivem à gravação e leitura ORM.

        O cenário converte o agregado em registro, grava no SQLite, consulta o
        registro em outra sessão e remapeia para domínio. Ele existe para
        validar a persistência durável dos campos usados pela consulta.
        """
        usuario = _usuario_com_contato()

        with self.criar_sessao() as sessao:
            sessao.add(para_registro(usuario))
            sessao.commit()

        with self.criar_sessao() as sessao:
            registro = sessao.scalar(
                select(UsuarioRegistro).where(UsuarioRegistro.id == usuario.id.valor)
            )

        self.assertIsNotNone(registro)
        assert registro is not None
        self.assertEqual(registro.nome, "Ana Exemplo")
        self.assertEqual(registro.email, "ana@example.test")
        self.assertEqual(registro.telefones, ["+55 11 99999-0001", "+55 11 3333-0001"])
        self.assertEqual(registro.cidade, "São Paulo")
        self.assertEqual(registro.linkedin, "https://www.linkedin.com/in/ana-exemplo")
        self.assertEqual(registro.curriculo_lattes, "http://lattes.cnpq.br/123456789")

        recuperado = para_usuario(registro)
        self.assertEqual(recuperado.id, usuario.id)
        self.assertEqual(recuperado.nome, usuario.nome)
        self.assertEqual(recuperado.email, usuario.email)
        self.assertIsNotNone(recuperado.dados_contato)
        assert recuperado.dados_contato is not None
        self.assertEqual(
            [telefone.valor for telefone in recuperado.dados_contato.telefones],
            ["+55 11 99999-0001", "+55 11 3333-0001"],
        )
        self.assertEqual(recuperado.dados_contato.cidade, Cidade("São Paulo"))
        self.assertEqual(
            recuperado.dados_contato.linkedin,
            "https://www.linkedin.com/in/ana-exemplo",
        )
        self.assertEqual(
            recuperado.dados_contato.curriculo_lattes,
            "http://lattes.cnpq.br/123456789",
        )

    def test_recarrega_perfil_antigo_sem_dados_de_contato(self) -> None:
        """Preserva contas anteriores à inclusão dos campos de contato.

        O cenário grava um usuário sem dados opcionais, relê suas colunas nulas
        e remapeia o agregado sem contato. Ele existe para verificar
        compatibilidade dos registros que precedem a consulta pessoal.
        """
        usuario = Usuario(
            id=UsuarioId(UUID("10000000-0000-4000-8000-000000000002")),
            nome=Nome("Bruno Exemplo"),
            email=Email("bruno@example.test"),
            hash_senha=HashSenha("hash-sintetico-de-teste"),
        )

        with self.criar_sessao() as sessao:
            sessao.add(para_registro(usuario))
            sessao.commit()

        with self.criar_sessao() as sessao:
            registro = sessao.scalar(
                select(UsuarioRegistro).where(UsuarioRegistro.id == usuario.id.valor)
            )

        self.assertIsNotNone(registro)
        assert registro is not None
        self.assertIsNone(registro.telefones)
        self.assertIsNone(registro.cidade)
        self.assertIsNone(registro.linkedin)
        self.assertIsNone(registro.curriculo_lattes)
        self.assertIsNone(para_usuario(registro).dados_contato)


def _usuario_com_contato() -> Usuario:
    """Monta um perfil sintético com todos os campos consultáveis persistidos.

    A função usa IDs e valores determinísticos, incluindo dois telefones e os
    dois links profissionais. Ela existe para tornar o round trip reproduzível.
    """
    contato = DadosContato(
        endereco=Endereco("Rua de Teste, 10"),
        telefones=(Telefone("+55 11 99999-0001"), Telefone("+55 11 3333-0001")),
        cidade=Cidade("São Paulo"),
        linkedin="https://www.linkedin.com/in/ana-exemplo",
        curriculo_lattes="http://lattes.cnpq.br/123456789",
    )
    return Usuario(
        id=UsuarioId(UUID("10000000-0000-4000-8000-000000000001")),
        nome=Nome("Ana Exemplo"),
        email=Email("ana@example.test"),
        hash_senha=HashSenha("hash-sintetico-de-teste"),
        dados_contato=contato,
    )
