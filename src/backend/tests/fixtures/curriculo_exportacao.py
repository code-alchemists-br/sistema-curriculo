"""Fornece fixture determinística de currículo para testes de exportação e download.

O módulo disponibiliza um cenário rico e estável com todos os dados de estudante,
formação, experiência profissional, projetos, competências e idiomas. Ele existe
para servir de base consistente para os futuros testes de geração de arquivos PDF
e DOCX (RF09) sem depender de banco de dados ou valores aleatórios.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261006-215500-fixture-teste-exportacao-curriculo-v001.md#v001
from backend.domain.curriculo import Curriculo
from backend.domain.itens_perfil import (
    Competencia,
    ExperienciaProfissional,
    FormacaoAcademica,
    Idioma,
    ProjetoAcademico,
)
from backend.domain.usuario import Usuario
from backend.domain.value_objects import (
    CompetenciaId,
    CurriculoId,
    DadosContato,
    Email,
    Endereco,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    HashSenha,
    IdiomaId,
    Nome,
    Periodo,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    Telefone,
    UsuarioId,
)

# Identificadores determinísticos estáveis para testes repetíveis
ID_USUARIO_ESTAVEL = UsuarioId(UUID("11111111-1111-4111-8111-111111111111"))
ID_CURRICULO_ESTAVEL = CurriculoId(UUID("22222222-2222-4222-8222-222222222222"))
ID_FORMACAO_ESTAVEL = FormacaoAcademicaId(UUID("33333333-3333-4333-8333-333333333333"))
ID_EXPERIENCIA_ESTAVEL = ExperienciaProfissionalId(UUID("44444444-4444-4444-8444-444444444444"))
ID_PROJETO_ESTAVEL = ProjetoAcademicoId(UUID("55555555-5555-4555-8555-555555555555"))
ID_COMPETENCIA_PYTHON_ESTAVEL = CompetenciaId(UUID("66666666-6666-4666-8666-666666666661"))
ID_COMPETENCIA_FASTAPI_ESTAVEL = CompetenciaId(UUID("66666666-6666-4666-8666-666666666662"))
ID_IDIOMA_INGLES_ESTAVEL = IdiomaId(UUID("77777777-7777-4777-8777-777777777771"))
ID_IDIOMA_ESPANHOL_ESTAVEL = IdiomaId(UUID("77777777-7777-4777-8777-777777777772"))


# Proveniência: decision-analysis prompts/backend/20261006-215500-fixture-teste-exportacao-curriculo-v001.md#v001
@dataclass(frozen=True, slots=True)
class CurriculoExportacaoFixture:
    """Consolida todos os dados de domínio e perfil para testes de exportação.

    O DTO agrupa a entidade ``Usuario`` com contato completo, a versão de ``Curriculo``
    com todas as referências tipadas e os itens de perfil correspondentes desreferenciados.
    Ele existe para fornecer uma visão integrada e imutável que motores de exportação
    (PDF/DOCX) necessitam para renderizar documentos sem acoplar a infraestrutura.
    """

    usuario: Usuario
    curriculo: Curriculo
    formacao_academica: FormacaoAcademica
    experiencia_profissional: ExperienciaProfissional
    projeto_academico: ProjetoAcademico
    competencias: tuple[Competencia, ...]
    idiomas: tuple[Idioma, ...]

    def para_dicionario(self) -> dict[str, Any]:
        """Converte a estrutura completa da fixture em um dicionário serializável.

        O método percorre os atributos da fixture, extraindo valores primitivos e
        formatando datas e identificadores em cadeias de texto padronizadas. Ele existe
        para facilitar asserções de snapshot, validações de payload JSON e testes de
        motores de template nos formatos PDF e DOCX.
        """
        contato = self.usuario.dados_contato
        return {
            "usuario": {
                "id": str(self.usuario.id.valor),
                "nome": self.usuario.nome.valor,
                "email": self.usuario.email.valor,
                "dados_contato": {
                    "endereco": contato.endereco.valor if contato else "",
                    "telefones": [t.valor for t in contato.telefones] if contato else [],
                    "linkedin": contato.linkedin if contato else None,
                    "curriculo_lattes": contato.curriculo_lattes if contato else None,
                },
            },
            "curriculo": {
                "id": str(self.curriculo.id.valor),
                "usuario_id": str(self.curriculo.usuario_id.valor),
                "titulo_versao": self.curriculo.titulo_versao,
                "layout": self.curriculo.layout,
                "is_public": self.curriculo.is_public,
                "total_referencias": len(self.curriculo.referencias),
            },
            "formacao_academica": {
                "id": str(self.formacao_academica.id.valor),
                "instituicao": self.formacao_academica.instituicao,
                "curso": self.formacao_academica.curso,
                "nivel": self.formacao_academica.nivel,
                "status": self.formacao_academica.status,
                "periodo": {
                    "inicio": self.formacao_academica.periodo.inicio.isoformat(),
                    "fim": (
                        self.formacao_academica.periodo.fim.isoformat()
                        if self.formacao_academica.periodo.fim
                        else None
                    ),
                },
            },
            "experiencia_profissional": {
                "id": str(self.experiencia_profissional.id.valor),
                "empresa": self.experiencia_profissional.empresa,
                "cargo": self.experiencia_profissional.cargo,
                "descricao": self.experiencia_profissional.descricao,
                "periodo": {
                    "inicio": self.experiencia_profissional.periodo.inicio.isoformat(),
                    "fim": (
                        self.experiencia_profissional.periodo.fim.isoformat()
                        if self.experiencia_profissional.periodo.fim
                        else None
                    ),
                },
            },
            "projeto_academico": {
                "id": str(self.projeto_academico.id.valor),
                "titulo": self.projeto_academico.titulo,
                "descricao": self.projeto_academico.descricao,
                "tecnologias": self.projeto_academico.tecnologias,
            },
            "competencias": [
                {
                    "id": str(c.id.valor),
                    "descricao": c.descricao,
                    "nivel": c.nivel,
                }
                for c in self.competencias
            ],
            "idiomas": [
                {
                    "id": str(i.id.valor),
                    "idioma": i.idioma,
                    "nivel": i.nivel,
                }
                for i in self.idiomas
            ],
        }


# Proveniência: decision-analysis prompts/backend/20261006-215500-fixture-teste-exportacao-curriculo-v001.md#v001
def obter_curriculo_exportacao_fixture() -> CurriculoExportacaoFixture:
    """Cria uma instância completa e estável de dados de currículo para testes de exportação.

    A função instancia entidades válidas com identificadores fixos, dados realistas de
    um estudante da FATEC e associa todas as referências ao agregado ``Curriculo``.
    Ela existe para fornecer massa de dados determinística para suítes de testes sem
    gerar valores aleatórios que possam causar oscilação (flakiness) em asserções de layout.
    """
    contato = DadosContato(
        endereco=Endereco("Avenida Tiradentes, 615 - Bom Retiro, São Paulo - SP"),
        telefones=(Telefone("(11) 98765-4321"), Telefone("(11) 3322-1100")),
        linkedin="https://linkedin.com/in/estudante-fatec",
        curriculo_lattes="http://lattes.cnpq.br/1234567890123456",
    )

    usuario = Usuario(
        id=ID_USUARIO_ESTAVEL,
        nome=Nome("Ana Carolina da Silva"),
        email=Email("ana.silva@fatec.sp.gov.br"),
        hash_senha=HashSenha("$scrypt$ln=16,r=8,p=1$fakehashparaestudantedeteste"),
        dados_contato=contato,
    )

    formacao = FormacaoAcademica(
        id=ID_FORMACAO_ESTAVEL,
        usuario_id=ID_USUARIO_ESTAVEL,
        instituicao="Faculdade de Tecnologia de São Paulo (FATEC-SP)",
        curso="Tecnologia em Análise e Desenvolvimento de Sistemas",
        nivel="Graduação Tecnológica",
        periodo=Periodo(inicio=date(2023, 2, 1), fim=date(2025, 12, 20)),
        status="Em andamento",
    )

    experiencia = ExperienciaProfissional(
        id=ID_EXPERIENCIA_ESTAVEL,
        usuario_id=ID_USUARIO_ESTAVEL,
        empresa="Empresa de Soluções Tecnológicas Ltda",
        cargo="Estagiária de Desenvolvimento de Software",
        descricao=(
            "Atuação no desenvolvimento de APIs RESTful utilizando Python e FastAPI, "
            "modelagem de banco de dados relacional e criação de suítes de testes "
            "automatizados para controle de qualidade de software."
        ),
        periodo=Periodo(inicio=date(2024, 1, 15), fim=None),
    )

    projeto = ProjetoAcademico(
        id=ID_PROJETO_ESTAVEL,
        usuario_id=ID_USUARIO_ESTAVEL,
        titulo="Sistema de Apoio Curricular Profissional",
        descricao=(
            "Plataforma completa para centralização de perfil estudantil, assistência "
            "na redação de trajetórias acadêmicas e exportação automatizada de currículos."
        ),
        tecnologias="Python, FastAPI, TypeScript, React, PostgreSQL, Nix",
    )

    competencia_python = Competencia(
        id=ID_COMPETENCIA_PYTHON_ESTAVEL,
        usuario_id=ID_USUARIO_ESTAVEL,
        descricao="Python e Clean Architecture",
        nivel="Avançado",
    )

    competencia_fastapi = Competencia(
        id=ID_COMPETENCIA_FASTAPI_ESTAVEL,
        usuario_id=ID_USUARIO_ESTAVEL,
        descricao="FastAPI e APIs RESTful",
        nivel="Intermediário",
    )

    idioma_ingles = Idioma(
        id=ID_IDIOMA_INGLES_ESTAVEL,
        usuario_id=ID_USUARIO_ESTAVEL,
        idioma="Inglês",
        nivel="Avançado",
    )

    idioma_espanhol = Idioma(
        id=ID_IDIOMA_ESPANHOL_ESTAVEL,
        usuario_id=ID_USUARIO_ESTAVEL,
        idioma="Espanhol",
        nivel="Intermediário",
    )

    curriculo = Curriculo(
        id=ID_CURRICULO_ESTAVEL,
        usuario_id=ID_USUARIO_ESTAVEL,
        titulo_versao="Currículo de Estágio - Engenharia de Software",
        layout="padrao_fatec",
        is_public=True,
    )

    # Inclusão determinística das referências tipadas no agregado
    curriculo.incluir_referencia(ReferenciaCurriculo(ID_FORMACAO_ESTAVEL))
    curriculo.incluir_referencia(ReferenciaCurriculo(ID_EXPERIENCIA_ESTAVEL))
    curriculo.incluir_referencia(ReferenciaCurriculo(ID_PROJETO_ESTAVEL))
    curriculo.incluir_referencia(ReferenciaCurriculo(ID_COMPETENCIA_PYTHON_ESTAVEL))
    curriculo.incluir_referencia(ReferenciaCurriculo(ID_COMPETENCIA_FASTAPI_ESTAVEL))
    curriculo.incluir_referencia(ReferenciaCurriculo(ID_IDIOMA_INGLES_ESTAVEL))
    curriculo.incluir_referencia(ReferenciaCurriculo(ID_IDIOMA_ESPANHOL_ESTAVEL))

    return CurriculoExportacaoFixture(
        usuario=usuario,
        curriculo=curriculo,
        formacao_academica=formacao,
        experiencia_profissional=experiencia,
        projeto_academico=projeto,
        competencias=(competencia_python, competencia_fastapi),
        idiomas=(idioma_ingles, idioma_espanhol),
    )
