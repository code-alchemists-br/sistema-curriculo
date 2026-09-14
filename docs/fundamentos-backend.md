# Fundamentos do backend

## Direção recomendada

O backend deve ser construído como uma API REST com **FastAPI**,
**SQLAlchemy 2.x**, **Alembic** e **PostgreSQL**.

- O FastAPI fornece a interface HTTP, validação de entradas e composição de
  dependências.
- O SQLAlchemy fornece o mapeamento objeto-relacional, as sessões, transações e
  acesso ao PostgreSQL.
- O Alembic mantém migrations versionadas para criar e evoluir o schema a partir
  dos modelos e mapeamentos do backend.

## Fronteiras arquiteturais

A organização mínima deve preservar Domain-Driven Design e Clean Architecture:

```text
domain/          entidades, value objects e portas de repositório
application/     casos de uso
infrastructure/
  persistence/
    sqlalchemy/  mapeamentos, sessão, repositórios concretos e migrations
api/             routers FastAPI e DTOs Pydantic
```

Entidades, value objects e casos de uso devem permanecer independentes de
FastAPI, SQLAlchemy, Pydantic e PostgreSQL. Os mapeamentos do ORM e os
repositórios concretos pertencem à infraestrutura. Quando necessário para
manter essa separação, use o mapeamento imperativo do SQLAlchemy para associar
entidades de domínio existentes às tabelas.

Os DTOs de entrada e saída da API devem ser definidos separadamente das
entidades de domínio e dos modelos de persistência.

## Persistência e migrations

O modelo e os mapeamentos mantidos no backend são a fonte de verdade do schema.
Cada mudança de schema deve gerar uma migration Alembic versionada, revisada e
executada pelo fluxo de implantação. Scripts SQL manuais não devem definir ou
evoluir o schema como fonte de verdade.

Não use criação automática de tabelas no startup da aplicação como mecanismo de
evolução do banco em ambientes persistentes; use migrations.

## Escolhas iniciais

Comece com endpoints e acesso ao banco síncronos, usando `psycopg`. Adote
acesso assíncrono apenas quando uma necessidade observável justificar a
complexidade adicional.

As dependências iniciais esperadas são:

- `fastapi`;
- `uvicorn`;
- `sqlalchemy`;
- `alembic`;
- `psycopg`;
- `pydantic-settings`.

## SQLModel

SQLModel é uma opção válida para aplicações CRUD simples e combina SQLAlchemy
com Pydantic. Contudo, não deve ser o modelo central deste backend, pois a
separação entre DTOs de API, entidades de domínio e modelos de persistência é
mais importante para as fronteiras DDD e Clean Architecture adotadas pelo
projeto.

## Referências

- [FastAPI — bancos de dados relacionais](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [SQLAlchemy ORM 2.0](https://docs.sqlalchemy.org/en/20/orm/)
- [Estilos de mapeamento do SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
