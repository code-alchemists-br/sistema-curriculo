"""Centraliza a metadata SQLAlchemy descoberta pelo Alembic.

O módulo expõe a metadata dos modelos externos de usuário e de currículo,
carregados explicitamente. Ele existe para tornar autogenerate determinístico e
manter ORM fora do núcleo do backend.
"""

# A importação abaixo registra a tabela de currículos em ``Base.metadata``; ela é
# explícita porque cada modelo vive em seu próprio módulo.
from backend.infrastructure.persistence.sqlalchemy.curriculo import CurriculoRegistro  # noqa: F401
from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20260916-estrutura-alembic-code-first-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20261005-191458-edicao-versao-curriculo-v001.md#v001
metadata = Base.metadata