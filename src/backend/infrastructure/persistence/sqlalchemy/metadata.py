"""Centraliza a metadata SQLAlchemy descoberta pelo Alembic.

O módulo expõe a metadata do modelo externo de usuário, carregado explicitamente.
Ele existe para tornar autogenerate determinístico e
manter ORM fora do núcleo do backend.
"""

from backend.infrastructure.persistence.sqlalchemy.usuario import Base


# Proveniência: decision-analysis prompts/backend/20260916-estrutura-alembic-code-first-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260916-persistencia-usuario-code-first-v001.md#v001
metadata = Base.metadata
