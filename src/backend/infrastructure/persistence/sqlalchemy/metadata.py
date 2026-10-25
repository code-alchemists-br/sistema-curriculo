"""Centraliza a metadata SQLAlchemy descoberta pelo Alembic.

O módulo importa explicitamente os modelos externos de usuário, currículo e
associação currículo-vaga antes de expor a metadata. Ele existe para tornar
Alembic determinístico e manter ORM fora do núcleo do backend.
"""

# A importação abaixo registra as tabelas de currículos e de seleção de itens em
# ``Base.metadata``; ela é explícita porque cada módulo de modelo é importado à
# parte do módulo da base.
# Proveniência: decision-analysis prompts/backend/20261017-184313-associacao-curriculo-vaga-v004.md#v004
from backend.infrastructure.persistence.sqlalchemy.associacao_curriculo_vaga import (
    AssociacaoCurriculoVagaRegistro,  # noqa: F401
    ClassificacaoAssociacaoRegistro,  # noqa: F401
)

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
from backend.infrastructure.persistence.sqlalchemy.certificacao import (
    CertificacaoRegistro,  # noqa: F401
)
from backend.infrastructure.persistence.sqlalchemy.competencia import (
    CompetenciaRegistro,  # noqa: F401
)
from backend.infrastructure.persistence.sqlalchemy.curriculo import (
    CurriculoRegistro,  # noqa: F401
)

# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
from backend.infrastructure.persistence.sqlalchemy.curso import (
    CursoRegistro,  # noqa: F401
)

# Proveniência: decision-analysis prompts/backend/20261023-170000-persistir-decisao-recomendacao-v001.md#v001
from backend.infrastructure.persistence.sqlalchemy.decisao_recomendacao import (
    DecisaoRecomendacaoRegistro,  # noqa: F401
)

# Proveniência: decision-analysis prompts/backend/20261016-074803-armazenamento-documento-complementar-v001.md#v001
from backend.infrastructure.persistence.sqlalchemy.documento import (
    DocumentoRegistro,  # noqa: F401
)
from backend.infrastructure.persistence.sqlalchemy.experiencia_profissional import (
    ExperienciaProfissionalRegistro,  # noqa: F401
)

# Proveniência: decision-analysis prompts/backend/20261014-195233-expor-cadastro-formacao-academica-v003.md#v003
from backend.infrastructure.persistence.sqlalchemy.formacao_academica import (
    FormacaoAcademicaRegistro,  # noqa: F401
)

# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
from backend.infrastructure.persistence.sqlalchemy.idioma import (
    IdiomaRegistro,  # noqa: F401
)

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.infrastructure.persistence.sqlalchemy.link_profissional import (
    LinkProfissionalRegistro,  # noqa: F401
)

# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
from backend.infrastructure.persistence.sqlalchemy.projeto_academico import (
    ProjetoAcademicoRegistro,  # noqa: F401
)
from backend.infrastructure.persistence.sqlalchemy.sessao import (
    SessaoRegistro,  # noqa: F401
)
from backend.infrastructure.persistence.sqlalchemy.usuario import Base

# Proveniência: decision-analysis prompts/backend/20260916-estrutura-alembic-code-first-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
metadata = Base.metadata
