"""Expõe os casos de uso internos da aplicação de currículos.

O pacote organiza a orquestração entre agregados do domínio e portas internas,
sem importar API, ORM ou adaptadores concretos. Ele existe para preservar as
dependências apontadas para dentro e permitir que interfaces externas componham
os casos de uso posteriormente.
"""

# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
from backend.application.cadastro_estudante import (
    CadastrarEstudante,
    CadastrarEstudanteEntrada,
    EmailJaCadastrado,
)
from backend.application.ports import GeradorUsuarioId, RepositorioUsuario

__all__ = [
    "CadastrarEstudante",
    "CadastrarEstudanteEntrada",
    "EmailJaCadastrado",
    "GeradorUsuarioId",
    "RepositorioUsuario",
]
