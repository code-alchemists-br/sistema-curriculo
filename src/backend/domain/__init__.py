"""Expõe o núcleo de domínio independente da aplicação de currículos.

O módulo reúne a API pública de entidades, agregados e value objects sem
importar frameworks, persistência ou transporte. Ele existe para que camadas
internas possam trabalhar com regras de negócio estáveis e para que adapters
futuros dependam do domínio, e não o contrário.
"""

# Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
from backend.domain.associacao_curriculo_vaga import (
    AssociacaoCurriculoVaga,
    ClassificacaoAssociacao,
)

# Proveniência: decision-analysis prompts/backend/20260914-camada-dominio-v001.md#v001
from backend.domain.curriculo import Curriculo

# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
from backend.domain.decisao_recomendacao import (
    DecisaoEstudante,
    DecisaoRecomendacao,
)

# Proveniência: decision-analysis prompts/backend/20261017-120000-propriedade-referencia-curriculo-v001.md#v001
from backend.domain.exceptions import (
    ReferenciaDeOutroProprietario,
    RegraDeDominioViolada,
)

# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.itens_perfil import (
    CARGA_HORARIA_MAXIMA_CURSO,
    CARGA_HORARIA_MINIMA_CURSO,
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    ESQUEMAS_URL_PERMITIDOS,
    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    TAMANHO_MAXIMO_DESCRICAO_PROJETO,
    # Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
    TAMANHO_MAXIMO_DOCUMENTO_BYTES,
    TAMANHO_MAXIMO_ROTULO_LINK,
    TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO,
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    TAMANHO_MAXIMO_TEXTO_CERTIFICACAO,
    TAMANHO_MAXIMO_TEXTO_CURSO,
    TAMANHO_MAXIMO_TEXTO_FORMACAO,
    TAMANHO_MAXIMO_TITULO_PROJETO,
    TAMANHO_MAXIMO_URL_LINK,
    TAMANHO_MINIMO_ROTULO_LINK,
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    TAMANHO_MINIMO_TEXTO_CERTIFICACAO,
    TAMANHO_MINIMO_TEXTO_CURSO,
    TAMANHO_MINIMO_TEXTO_FORMACAO,
    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    TAMANHO_MINIMO_TEXTO_PROJETO,
    TIPOS_ARQUIVO_PERMITIDOS,
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    CategoriaCompetencia,
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    Certificacao,
    Competencia,
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    Curso,
    Documento,
    ExperienciaProfissional,
    FormacaoAcademica,
    Idioma,
    LinkProfissional,
    # Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
    NivelFormacaoAcademica,
    ProjetoAcademico,
    StatusFormacaoAcademica,
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    normalizar_chave_certificacao,
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    normalizar_chave_curso,
    normalizar_chave_rotulo_link,
    normalizar_chave_url,
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    normalizar_idioma,
    normalizar_rotulo_link,
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    normalizar_texto_certificacao,
    normalizar_texto_curso,
    # Proveniência: decision-analysis prompts/backend/20261016-140000-ordenacao-experiencias-profissionais-v001.md#v001
    ordenar_experiencias,
    # Proveniência: decision-analysis prompts/backend/20261015-150000-ordenacao-formacoes-academicas-v001.md#v001
    ordenar_formacoes,
    validar_e_normalizar_url_link,
)

# Proveniência: decision-analysis prompts/backend/20261017-140000-modelo-curriculo-edicao-versao-v001.md#v001
from backend.domain.modelo_curriculo import ModeloCurriculo

# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
from backend.domain.revisao_curriculo import (
    PendenciaRevisao,
    ResultadoRevisao,
    SecaoRevisao,
    SeveridadePendencia,
    revisar_curriculo,
)

# Proveniência: decision-analysis prompts/backend/20261017-100000-secoes-curriculo-ordem-padrao-v001.md#v001
from backend.domain.secao_curriculo import (
    ORDEM_PADRAO_SECOES,
    SecaoCurriculo,
)

# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.usuario import Usuario
from backend.domain.value_objects import (
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    CertificacaoId,
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    Cidade,
    CompetenciaId,
    CurriculoId,
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    CursoId,
    # Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
    DadosContato,
    DocumentoId,
    Email,
    # Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
    Endereco,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    HashSenha,
    IdiomaId,
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    LinkProfissionalId,
    Nome,
    Periodo,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    # Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
    Telefone,
    UsuarioId,
    # Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
    VagaId,
)

__all__ = [
    # Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
    "AssociacaoCurriculoVaga",
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    "CARGA_HORARIA_MAXIMA_CURSO",
    "CARGA_HORARIA_MINIMA_CURSO",
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    "CategoriaCompetencia",
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    "Certificacao",
    "CertificacaoId",
    "ClassificacaoAssociacao",
    "Competencia",
    "CompetenciaId",
    "Curriculo",
    "CurriculoId",
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    "Curso",
    "CursoId",
    "Cidade",
    "DadosContato",
    "Documento",
    "DocumentoId",
    "Email",
    "Endereco",
    "ExperienciaProfissional",
    "ExperienciaProfissionalId",
    "FormacaoAcademica",
    "FormacaoAcademicaId",
    "HashSenha",
    "Idioma",
    "IdiomaId",
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    "ESQUEMAS_URL_PERMITIDOS",
    "LinkProfissional",
    "LinkProfissionalId",
    # Proveniência: decision-analysis prompts/backend/20261017-140000-modelo-curriculo-edicao-versao-v001.md#v001
    "ModeloCurriculo",
    "Nome",
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    "normalizar_chave_curso",
    "normalizar_texto_curso",
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    "normalizar_chave_rotulo_link",
    "normalizar_chave_url",
    "normalizar_rotulo_link",
    "validar_e_normalizar_url_link",
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    "normalizar_chave_certificacao",
    "normalizar_texto_certificacao",
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    "normalizar_idioma",
    # Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
    "NivelFormacaoAcademica",
    # Proveniência: decision-analysis prompts/backend/20261016-140000-ordenacao-experiencias-profissionais-v001.md#v001
    "ordenar_experiencias",
    # Proveniência: decision-analysis prompts/backend/20261015-150000-ordenacao-formacoes-academicas-v001.md#v001
    "ordenar_formacoes",
    "Periodo",
    "ProjetoAcademico",
    "ProjetoAcademicoId",
    "ReferenciaCurriculo",
    # Proveniência: decision-analysis prompts/backend/20261017-120000-propriedade-referencia-curriculo-v001.md#v001
    "ReferenciaDeOutroProprietario",
    "RegraDeDominioViolada",
    "StatusFormacaoAcademica",
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    "TAMANHO_MAXIMO_ROTULO_LINK",
    "TAMANHO_MAXIMO_URL_LINK",
    "TAMANHO_MINIMO_ROTULO_LINK",
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    "TAMANHO_MAXIMO_TEXTO_CURSO",
    "TAMANHO_MINIMO_TEXTO_CURSO",
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    "TAMANHO_MAXIMO_TEXTO_CERTIFICACAO",
    "TAMANHO_MINIMO_TEXTO_CERTIFICACAO",
    "TAMANHO_MAXIMO_TEXTO_FORMACAO",
    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    "TAMANHO_MAXIMO_DESCRICAO_PROJETO",
    "TAMANHO_MAXIMO_TECNOLOGIAS_PROJETO",
    "TAMANHO_MAXIMO_TITULO_PROJETO",
    "TAMANHO_MINIMO_TEXTO_FORMACAO",
    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    "TAMANHO_MINIMO_TEXTO_PROJETO",
    # Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
    "TAMANHO_MAXIMO_DOCUMENTO_BYTES",
    "TIPOS_ARQUIVO_PERMITIDOS",
    "Telefone",
    "Usuario",
    "UsuarioId",
    # Proveniência: decision-analysis prompts/backend/20261011-023511-associacao-curriculo-vaga-v002.md#v002
    "VagaId",
    # Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
    "PendenciaRevisao",
    "ResultadoRevisao",
    "SecaoRevisao",
    "SeveridadePendencia",
    "revisar_curriculo",
    # Proveniência: decision-analysis prompts/backend/20261017-100000-secoes-curriculo-ordem-padrao-v001.md#v001
    "ORDEM_PADRAO_SECOES",
    "SecaoCurriculo",
    # Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
    "DecisaoEstudante",
    "DecisaoRecomendacao",
]
