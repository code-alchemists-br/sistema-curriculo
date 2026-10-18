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
from backend.infrastructure.persistence.sqlalchemy.curriculo import (
    CurriculoRegistro,  # noqa: F401
)
from backend.infrastructure.persistence.sqlalchemy.usuario import Base

# Proveniência: decision-analysis prompts/backend/20260916-estrutura-alembic-code-first-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
metadata = Base.metadata
