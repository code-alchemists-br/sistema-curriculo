"""Expõe os casos de uso internos da aplicação de currículos.

O pacote organiza a orquestração entre agregados do domínio e portas internas,
sem importar API, ORM ou adaptadores concretos. Ele existe para preservar as
dependências apontadas para dentro e permitir que interfaces externas componham
os casos de uso posteriormente.
"""

# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
from backend.application.acesso_estudante import (
    AcessarEstudante,
    AcessarEstudanteEntrada,
    CredenciaisInvalidas,
)

# Proveniência: decision-analysis prompts/backend/20261018-133100-contrato-assistente-descricao-projeto-v001.md#v001
from backend.application.assistente_descricao_projeto import (
    AssistenteDescricaoProjeto,
    AssistenteDescricaoProjetoAusente,
    AssistenteDescricaoProjetoEntrada,
    AssistenteDescricaoProjetoIndisponivel,
    AssistenteDescricaoProjetoSaida,
)
from backend.application.assistente_descricao_projeto_deterministico import (
    AssistenteDescricaoProjetoDeterministico,
)

# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
from backend.application.associacao_curriculo_vaga import (
    AdicionarClassificacaoAssociacaoCurriculoVaga,
    AlterarClassificacaoAssociacaoCurriculoVagaEntrada,
    AssociacaoCurriculoVagaJaExiste,
    AssociacaoCurriculoVagaNaoEncontrada,
    CriarAssociacaoCurriculoVaga,
    CriarAssociacaoCurriculoVagaEntrada,
    RemoverClassificacaoAssociacaoCurriculoVaga,
)

# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
from backend.application.cadastro_certificacao import (
    CadastrarCertificacao,
    CadastrarCertificacaoEntrada,
    CertificacaoJaCadastrada,
)

# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
from backend.application.cadastro_competencia import (
    CadastrarCompetencia,
    CadastrarCompetenciaEntrada,
    CompetenciaJaCadastrada,
)

# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
from backend.application.cadastro_curso import (
    CadastrarCurso,
    CadastrarCursoEntrada,
    CursoJaCadastrado,
)

# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
from backend.application.cadastro_documento import (
    ArmazenarDocumento,
    ArmazenarDocumentoEntrada,
)
from backend.application.cadastro_estudante import (
    CadastrarEstudante,
    CadastrarEstudanteEntrada,
    EmailJaCadastrado,
)

# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from backend.application.cadastro_experiencia_profissional import (
    CadastrarExperienciaProfissional,
    CadastrarExperienciaProfissionalEntrada,
)

# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
from backend.application.cadastro_idioma import (
    CadastrarIdioma,
    CadastrarIdiomaEntrada,
    IdiomaJaCadastrado,
)

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.application.cadastro_link_profissional import (
    CadastrarLinkProfissional,
    CadastrarLinkProfissionalEntrada,
    LinkProfissionalJaCadastrado,
)

# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
from backend.application.cadastro_projeto_academico import (
    CadastrarProjetoAcademico,
    CadastrarProjetoAcademicoEntrada,
)

# Proveniência: decision-analysis prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md#v001
from backend.application.consulta_associacao_curriculo_vaga import (
    ListarAssociacoesCurriculoVaga,
    ListarAssociacoesCurriculoVagaEntrada,
)

# Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
from backend.application.dados_contato import (
    AtualizarDadosContato,
    AtualizarDadosContatoEntrada,
)
from backend.application.documento_renderizado import (
    BlocoDocumento,
    CabecalhoDocumento,
    DocumentoCurriculoRenderizado,
    RenderizadorDocumentoCurriculo,
    SecaoDocumento,
    montar_documento_renderizado,
)

# Proveniência: decision-analysis prompts/backend/20261019-110000-download-documento-complementar-v001.md#v001
from backend.application.download_documento import (
    BaixarDocumento,
    BaixarDocumentoEntrada,
    ConteudoDocumento,
)
from backend.application.edicao_experiencia_profissional import (
    EditarExperienciaProfissional,
    EditarExperienciaProfissionalEntrada,
    ExperienciaProfissionalNaoEncontrada,
)

# Proveniência: decision-analysis prompts/backend/20261016-102843-exclusao-documento-complementar-v001.md#v001
from backend.application.exclusao_documento import (
    DocumentoNaoEncontrado,
    ExcluirDocumento,
    ExcluirDocumentoEntrada,
)
from backend.application.exclusao_experiencia_profissional import (
    ExcluirExperienciaProfissional,
    ExcluirExperienciaProfissionalEntrada,
)

# Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
from backend.application.exclusao_versao_curriculo import (
    ExcluirVersaoCurriculo,
    ExcluirVersaoCurriculoEntrada,
)
from backend.application.exportacao_curriculo import (
    FORMATO_DOCX,
    ArquivoCurriculoExportado,
    ExportarCurriculo,
    ExportarCurriculoEntrada,
    FalhaGeracaoArquivoCurriculo,
    FormatoExportacao,
)

# Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
from backend.application.listagem_versoes_curriculo import (
    ListarVersoesCurriculo,
    ListarVersoesCurriculoEntrada,
)
from backend.application.perfil_completo import (
    AtualizarPerfilCompleto,
    AtualizarPerfilCompletoEntrada,
)

# Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
from backend.application.perfil_estudante import (
    CadastrarFormacaoAcademica,
    CadastrarFormacaoAcademicaEntrada,
    # Proveniência: decision-analysis prompts/backend/20261012-233648-expor-consulta-dados-pessoais-estudante-v005.md#v005
    ConsultarPerfilEstudante,
    ConsultarPerfilEstudanteEntrada,
    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    EditarFormacaoAcademica,
    EditarFormacaoAcademicaEntrada,
    EditarPerfil,
    EditarPerfilEntrada,
    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    ExcluirFormacaoAcademica,
    ExcluirFormacaoAcademicaEntrada,
    ExcluirPerfil,
    ExcluirPerfilEntrada,
    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    FormacaoAcademicaNaoEncontrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)

# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
from backend.application.ports import (
    # Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
    ArmazenadorDocumentos,
    # Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
    ConsultaItemPerfil,
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    ConsultaProprietarioItem,
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    GeradorCertificacaoId,
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    GeradorCompetenciaId,
    GeradorCurriculoId,
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    GeradorCursoId,
    # Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
    GeradorDocumentoId,
    GeradorExperienciaProfissionalId,
    GeradorFormacaoAcademicaId,
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    GeradorIdiomaId,
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    GeradorLinkProfissionalId,
    GeradorProjetoAcademicoId,
    GeradorUsuarioId,
    Relogio,
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    RepositorioCertificacao,
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    RepositorioCompetencia,
    RepositorioCurriculo,
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    RepositorioCurso,
    # Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
    RepositorioDocumento,
    RepositorioExperienciaProfissional,
    RepositorioFormacaoAcademica,
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    RepositorioIdioma,
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    RepositorioLinkProfissional,
    RepositorioProjetoAcademico,
    RepositorioUsuario,
    VerificadorSenha,
)

# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
from backend.application.previa_versao_curriculo import (
    GerarPreviaVersaoCurriculo,
    GerarPreviaVersaoCurriculoEntrada,
    PreviaVersaoCurriculo,
)

# Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
from backend.application.revisao_versao_curriculo import (
    RevisarVersaoCurriculo,
    RevisarVersaoCurriculoEntrada,
)

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
from backend.application.selecao_itens_versao_curriculo import (
    DesselecionarItemVersaoCurriculo,
    DesselecionarItemVersaoCurriculoEntrada,
    ItemNaoEncontrado,
    SelecionarItemVersaoCurriculo,
    SelecionarItemVersaoCurriculoEntrada,
)

# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
from backend.application.versao_curriculo import (
    AtualizarOrdemSecoesCurriculo,
    AtualizarOrdemSecoesCurriculoEntrada,
    CriarVersaoCurriculo,
    CriarVersaoCurriculoEntrada,
    CurriculoNaoEncontrado,
    EditarVersaoCurriculo,
    EditarVersaoCurriculoEntrada,
)

__all__ = [
    # Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
    "AssociacaoCurriculoVagaJaExiste",
    "AssociacaoCurriculoVagaNaoEncontrada",
    "AlterarClassificacaoAssociacaoCurriculoVagaEntrada",
    "AdicionarClassificacaoAssociacaoCurriculoVaga",
    "CriarAssociacaoCurriculoVaga",
    "CriarAssociacaoCurriculoVagaEntrada",
    "RemoverClassificacaoAssociacaoCurriculoVaga",
    "CadastrarEstudante",
    "CadastrarEstudanteEntrada",
    # Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
    "ArmazenarDocumento",
    "ArmazenarDocumentoEntrada",
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    "CadastrarCertificacao",
    "CadastrarCertificacaoEntrada",
    "CertificacaoJaCadastrada",
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    "CadastrarCompetencia",
    "CadastrarCompetenciaEntrada",
    "CompetenciaJaCadastrada",
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    "CadastrarCurso",
    "CadastrarCursoEntrada",
    "CursoJaCadastrado",
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    "CadastrarIdioma",
    "CadastrarIdiomaEntrada",
    "IdiomaJaCadastrado",
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    "CadastrarLinkProfissional",
    "CadastrarLinkProfissionalEntrada",
    "LinkProfissionalJaCadastrado",
    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    "CadastrarExperienciaProfissional",
    "CadastrarExperienciaProfissionalEntrada",
    "EditarExperienciaProfissional",
    "EditarExperienciaProfissionalEntrada",
    "ExperienciaProfissionalNaoEncontrada",
    "ExcluirExperienciaProfissional",
    "ExcluirExperienciaProfissionalEntrada",
    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    "CadastrarProjetoAcademico",
    "CadastrarProjetoAcademicoEntrada",
    # Proveniência: decision-analysis prompts/backend/20261018-133100-contrato-assistente-descricao-projeto-v001.md#v001
    "AssistenteDescricaoProjeto",
    "AssistenteDescricaoProjetoAusente",
    "AssistenteDescricaoProjetoDeterministico",
    "AssistenteDescricaoProjetoEntrada",
    "AssistenteDescricaoProjetoIndisponivel",
    "AssistenteDescricaoProjetoSaida",
    "AcessarEstudante",
    "AcessarEstudanteEntrada",
    # Proveniência: decision-analysis prompts/backend/20260924-cadastro-dados-pessoais-contato-v001.md#v001
    "AtualizarDadosContato",
    "AtualizarDadosContatoEntrada",
    "AtualizarPerfilCompleto",
    "AtualizarPerfilCompletoEntrada",
    "CredenciaisInvalidas",
    "EmailJaCadastrado",
    # Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
    "CadastrarFormacaoAcademica",
    "CadastrarFormacaoAcademicaEntrada",
    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    "EditarFormacaoAcademica",
    "EditarFormacaoAcademicaEntrada",
    "FormacaoAcademicaNaoEncontrada",
    "ConsultarPerfilEstudante",
    "ConsultarPerfilEstudanteEntrada",
    # Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001
    "EditarPerfil",
    "EditarPerfilEntrada",
    # Proveniência: decision-analysis prompts/backend/20261015-205307-expor-exclusao-formacao-academica-v002.md#v002
    "ExcluirFormacaoAcademica",
    "ExcluirFormacaoAcademicaEntrada",
    "ExcluirPerfil",
    "ExcluirPerfilEntrada",
    # Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
    "ArmazenadorDocumentos",
    # Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
    "GeradorDocumentoId",
    "GeradorFormacaoAcademicaId",
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    "GeradorCertificacaoId",
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    "GeradorCompetenciaId",
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    "GeradorCursoId",
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    "GeradorIdiomaId",
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    "GeradorLinkProfissionalId",
    "GeradorUsuarioId",
    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    "GeradorExperienciaProfissionalId",
    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    "GeradorProjetoAcademicoId",
    "PerfilExcluido",
    "PerfilNaoEncontrado",
    "Relogio",
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    "RepositorioCertificacao",
    "RepositorioFormacaoAcademica",
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    "RepositorioCompetencia",
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    "RepositorioCurso",
    # Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
    "RepositorioDocumento",
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    "RepositorioIdioma",
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    "RepositorioLinkProfissional",
    "RepositorioUsuario",
    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    "RepositorioExperienciaProfissional",
    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    "RepositorioProjetoAcademico",
    "VerificadorSenha",
    # Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
    "CurriculoNaoEncontrado",
    "AtualizarOrdemSecoesCurriculo",
    "AtualizarOrdemSecoesCurriculoEntrada",
    "EditarVersaoCurriculo",
    "EditarVersaoCurriculoEntrada",
    "RepositorioCurriculo",
    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    "CriarVersaoCurriculo",
    "CriarVersaoCurriculoEntrada",
    "GeradorCurriculoId",
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    "ConsultaProprietarioItem",
    "DesselecionarItemVersaoCurriculo",
    "DesselecionarItemVersaoCurriculoEntrada",
    "ItemNaoEncontrado",
    "SelecionarItemVersaoCurriculo",
    "SelecionarItemVersaoCurriculoEntrada",
    # Proveniência: decision-analysis prompts/backend/20261019-182907-consulta-paginada-associacoes-estudante-v001.md#v001
    "ListarAssociacoesCurriculoVaga",
    "ListarAssociacoesCurriculoVagaEntrada",
    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    "ListarVersoesCurriculo",
    "ListarVersoesCurriculoEntrada",
    # Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
    "ExcluirVersaoCurriculo",
    "ExcluirVersaoCurriculoEntrada",
    "DocumentoNaoEncontrado",
    "ExcluirDocumento",
    "ExcluirDocumentoEntrada",
    # Proveniência: decision-analysis prompts/backend/20261019-110000-download-documento-complementar-v001.md#v001
    "BaixarDocumento",
    "BaixarDocumentoEntrada",
    "ConteudoDocumento",
    # Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
    "ConsultaItemPerfil",
    "GerarPreviaVersaoCurriculo",
    "GerarPreviaVersaoCurriculoEntrada",
    "PreviaVersaoCurriculo",
    "BlocoDocumento",
    "CabecalhoDocumento",
    "DocumentoCurriculoRenderizado",
    "RenderizadorDocumentoCurriculo",
    "FORMATO_DOCX",
    "ArquivoCurriculoExportado",
    "ExportarCurriculo",
    "ExportarCurriculoEntrada",
    "FalhaGeracaoArquivoCurriculo",
    "FormatoExportacao",
    "SecaoDocumento",
    "montar_documento_renderizado",
    # Proveniência: decision-analysis prompts/backend/20261015-165611-revisao-campos-obrigatorios-curriculo-v001.md#v001
    "RevisarVersaoCurriculo",
    "RevisarVersaoCurriculoEntrada",
]
