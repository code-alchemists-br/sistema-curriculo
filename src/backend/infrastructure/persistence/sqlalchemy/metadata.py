"""Centraliza a metadata SQLAlchemy descoberta pelo Alembic.

O módulo expõe a metadata dos modelos externos, carregados explicitamente. Ele
existe para tornar autogenerate determinístico e manter ORM fora do núcleo do
backend.
"""

# A importação abaixo registra as tabelas de currículos e de seleção de itens em
# ``Base.metadata``; ela é explícita porque cada módulo de modelo é importado à
# parte do módulo da base.
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
from backend.infrastructure.persistence.sqlalchemy.sessao import (
    SessaoRegistro,  # noqa: F401
)
from backend.infrastructure.persistence.sqlalchemy.usuario import Base

# Proveniência: decision-analysis prompts/backend/20260916-estrutura-alembic-code-first-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
metadata = Base.metadata
