---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-15T15:28:03-03:00"
lineage:
  mode: initial
  root: null
  supersedes: null
  change_type: initial
  secondary_change_types: []
  decision_impact: initial
subjects:
  kind: mixed
  files:
    - path: src/backend/domain/itens_perfil.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "entidades de itens complementares de perfil e funções de normalização"
      content_state: working-tree
      revision: "working-tree based on b25ba7c3a0ee74bdb3431a6bc3864ef5dcf6561a"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "value objects tipados de identidade (UsuarioId, etc.)"
      content_state: working-tree
      revision: "working-tree based on b25ba7c3a0ee74bdb3431a6bc3864ef5dcf6561a"
      availability: available
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "protocolos de repositório e geradores de ID"
      content_state: working-tree
      revision: "working-tree based on b25ba7c3a0ee74bdb3431a6bc3864ef5dcf6561a"
      availability: available
    - path: src/backend/application/cadastro_curso.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on b25ba7c3a0ee74bdb3431a6bc3864ef5dcf6561a"
      availability: available
    - path: src/backend/api/curso.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on b25ba7c3a0ee74bdb3431a6bc3864ef5dcf6561a"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on b25ba7c3a0ee74bdb3431a6bc3864ef5dcf6561a"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/metadata.py
      relationship: supporting
      representation: source-code
      function: configuration
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on b25ba7c3a0ee74bdb3431a6bc3864ef5dcf6561a"
      availability: available
    - path: docs/wireframes/06-informacoes-complementares.md
      relationship: supporting
      representation: specification
      function: user-journey
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on b25ba7c3a0ee74bdb3431a6bc3864ef5dcf6561a"
      availability: available
    - path: docs/mapeamento_jornadas.md
      relationship: supporting
      representation: specification
      function: user-journey
      format: markdown
      analysis_scope: selected-section
      locator: "seção 6.6 Informações complementares"
      content_state: working-tree
      revision: "working-tree based on b25ba7c3a0ee74bdb3431a6bc3864ef5dcf6561a"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "A decisão delimita arquitetura, regras de domínio, portas, orquestração, persistência relacional Code First e router HTTP de backend para o cadastro de links profissionais."
classification:
  sphere: engineering
  concerns: [domain, architecture, data, security]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: high
  uncertainty: low
  reversibility: moderate
  risk: medium
---

# Análise de decisão — Cadastro de link profissional pela API

## Solicitação original

> Issue #104: Expor cadastro de link profissional. Tarefa da fatia vertical atribuída a @mariacarolinayamamoto, executada por @minoruhaga. Inclua os testes unitários pertinentes.
> Subtarefas decompostas da fatia:
> - #195: [F4.5] Definir o modelo de domínio de link profissional e validar esquema/URL permitidos.
> - #196: [F4.6] Criar caso de uso e persistência para link profissional; cobrir duplicidade por usuário.
> - #197: [F4.7] Expor o cadastro de link profissional na API e cobrir a resposta pública.
> Plano executivo aprovado: Implementar o endpoint de cadastro de link profissional do backend respeitando rigorosamente Clean Architecture, DDD, AGENTS.md e o fluxo de skills ($decision-analysis-v4 -> $backend-domain-orchestration-v2 -> $backend-adapters-drivers-v2).

## Informações complementares

- Padrão arquitetural consolidado no repositório em `competencia.py`, `idioma.py`, `certificacao.py` e `curso.py`.
- O usuário forneceu 2 refinamentos técnicos mandatórios incorporados a esta análise:
  1. Utilizar explicitamente `status.HTTP_422_UNPROCESSABLE_CONTENT` (da biblioteca `starlette.status` / `fastapi.status`), evitando o aviso de depreciação `StarletteDeprecationWarning` emitido pelo termo legado `HTTP_422_UNPROCESSABLE_ENTITY`.
  2. Validação da linearidade do grafo Alembic: para garantir encadeamento linear e unificado das migrações (`0009` -> `0010` -> `0011` -> `0012`), a branch de trabalho baseia-se na sequência que já contém cursos (PR #481, revisão `20261015_0011`), definindo `down_revision = "20261015_0011"`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem | Nenhuma | v001 | Análise inicial | Não há versão anterior a comparar. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/itens_perfil.py` | Principal | Código-fonte | Produção | Python | Itens reutilizáveis de perfil | Working tree baseado em `b25ba7c` |
| `src/backend/domain/value_objects.py` | Principal | Código-fonte | Produção | Python | Value objects de identidade | Working tree baseado em `b25ba7c` |
| `src/backend/application/ports.py` | Principal | Código-fonte | Produção | Python | Protocolos de repositório e gerador de ID | Working tree baseado em `b25ba7c` |
| `src/backend/application/cadastro_curso.py` | Apoio | Código-fonte | Produção | Python | Estrutura de caso de uso | Working tree baseado em `b25ba7c` |
| `src/backend/api/curso.py` | Apoio | Código-fonte | Produção | Python | Router HTTP com tratamento HTTP 422 moderno | Working tree baseado em `b25ba7c` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Registro de rotas e injeção | Working tree baseado em `b25ba7c` |
| `src/backend/infrastructure/persistence/sqlalchemy/metadata.py` | Apoio | Código/configuração | Configuração | Python | Registro global de tabelas ORM | Working tree baseado em `b25ba7c` |
| `docs/wireframes/06-informacoes-complementares.md` | Apoio | Especificação | Jornada de tela | Markdown | Grupo "Links profissionais" | Working tree baseado em `b25ba7c` |
| `docs/mapeamento_jornadas.md` | Apoio | Especificação | Jornada do usuário | Markdown | Seção 6.6 "Informações complementares" | Working tree baseado em `b25ba7c` |

### Limites da evidência dos artefatos

Os artefatos demonstram que:
1. `LinkProfissional` é um item autônomo pertencente à seção de informações complementares do perfil do estudante (`docs/mapeamento_jornadas.md:155` e `docs/wireframes/06-informacoes-complementares.md:8`).
2. Não deve ser confundido com os campos fixos de `DadosContato` (`linkedin` e `curriculo_lattes`), os quais residem diretamente na tabela de usuários.
3. Diferentemente de experiências ou formações, não há datas de início/fim nem períodos. A estrutura é focada em rótulo/título e URL web.
4. Por lidar diretamente com URLs externas, impõe-se validação estrita de segurança de esquemas no domínio para mitigar riscos de injeção XSS e esquemas arbitrários (`javascript:`, `data:`, `file:`).

## Problema enriquecido

### Resultado desejado

Disponibilizar endpoint autenticado `POST /links-profissionais` que permita ao estudante autenticado cadastrar um link profissional com rótulo (`rotulo`) e endereço web (`url`), validando no domínio os esquemas permitidos (`http` e `https`), a presença de domínio/host (`netloc`), ausência de caracteres de controle e restrições de tamanho, persistindo-o de forma independente na tabela relacional `links_profissionais` (Code First com SQLAlchemy e Alembic) e retornando o recurso público criado (HTTP 201), garantindo isolamento entre estudantes, rejeição de payloads inválidos com `status.HTTP_422_UNPROCESSABLE_CONTENT`, prevenção de duplicidades lógicas por `(usuario_id, url_normalizada)` (HTTP 409) e cobertura unitária ampla com doubles.

### Atores e interesses

- **Estudante:** Deseja cadastrar links profissionais relevantes (GitHub, portfólio pessoal, Behance, Medium, etc.) para enriquecer seu perfil.
- **Camada de API (FastAPI):** Deve proteger o endpoint, extraindo a identidade do estudante exclusivamente de `request.state.usuario_id` (sessão autenticada) e rejeitando requisições anônimas com HTTP 401, sem permitir que o cliente injete `usuario_id` no corpo da requisição. Mapeia exceções com códigos HTTP modernos (`HTTP_422_UNPROCESSABLE_CONTENT`).
- **Camada de Aplicação (Use Case):** Deve orquestrar a geração de ID via porta tipada, validação de invariantes, checagem assíncrona de duplicidade e delegação de persistência.
- **Camada de Domínio:** Deve manter a entidade `LinkProfissional` válida desde a criação, garantindo que o rótulo tenha entre 1 e 100 caracteres, que a URL pertença aos esquemas permitidos (`http`, `https`), que possua host válido, limite de 2048 caracteres, ausência de caracteres de controle, e produza a chave canônica `url_normalizada`.
- **Camada de Infraestrutura:** Deve implementar `RepositorioLinkProfissionalSqlAlchemy` e `GeradorLinkProfissionalIdUuid4`, mapear a tabela `links_profissionais` no SQLAlchemy com constraint de unicidade `uq_links_profissionais_usuario_url_normalizada`, tratar concorrência via `flush()` relançando `IntegrityError` como `LinkProfissionalJaCadastrado` e gerar a migration correspondente no Alembic com encadeamento linear (`20261015_0012`).

### Evidências e fatos observados

- O Value Object `LinkProfissionalId` e a Entidade `LinkProfissional` não constam atualmente no domínio, demandando criação.
- Subtarefa #195 exige explicitamente: "Definir o modelo de domínio de link profissional e validar esquema/URL permitidos."
- Subtarefa #196 exige explicitamente: "Criar caso de uso e persistência para link profissional; cobrir duplicidade por usuário."
- Subtarefa #197 exige explicitamente: "Expor o cadastro de link profissional na API e cobrir a resposta pública."
- Todo o código deve rodar em Nix (`.#backend` e `.#quality`) e possuir docstrings triplas obrigatórias.

### Hipóteses

1. A duplicidade de link profissional para um mesmo estudante deve ser verificada pela chave `(usuario_id, url_normalizada)` (esquema e host em minúsculas, remoção de barra final redundante na raiz). Um mesmo estudante não deve cadastrar o mesmo destino web duas vezes.
2. A rota pública de cadastro deve ser `POST /links-profissionais`, mantendo plural e simetria com as demais entidades complementares (`/idiomas`, `/certificacoes`, `/cursos`).
3. O encadeamento do Alembic deve utilizar linearidade estrita: a migração de links profissionais terá revisão `20261015_0012` e `down_revision = "20261015_0011"`.

### Perguntas em aberto

Nenhuma identificada. Os pontos de atenção e sugestões foram integralmente alinhados com o usuário.

### Escopo

- Criação do Value Object imutável `LinkProfissionalId` em `src/backend/domain/value_objects.py`.
- Criação das funções puras de validação e normalização (`normalizar_rotulo_link`, `validar_e_normalizar_url_link`, `normalizar_chave_url`), constantes dimensionais e da entidade `LinkProfissional` em `src/backend/domain/itens_perfil.py`.
- Exportação de símbolos no módulo `src/backend/domain/__init__.py`.
- Definição das portas `RepositorioLinkProfissional` e `GeradorLinkProfissionalId` em `src/backend/application/ports.py`.
- Criação do caso de uso `CadastrarLinkProfissional`, DTO `CadastrarLinkProfissionalEntrada` e exceção `LinkProfissionalJaCadastrado` em `src/backend/application/cadastro_link_profissional.py`.
- Exportação de símbolos no módulo `src/backend/application/__init__.py`.
- Implementação de `GeradorLinkProfissionalIdUuid4` em `src/backend/infrastructure/identificadores/geradores.py`.
- Implementação de `LinkProfissionalRegistro`, funções de conversão `para_registro` e `para_link_profissional` em `src/backend/infrastructure/persistence/sqlalchemy/link_profissional.py`.
- Implementação de `RepositorioLinkProfissionalSqlAlchemy` com tratamento de concorrência em `src/backend/infrastructure/persistence/sqlalchemy/repositorio_link_profissional.py`.
- Registro de `LinkProfissionalRegistro` em `src/backend/infrastructure/persistence/sqlalchemy/metadata.py`.
- Criação de migration Alembic `20261015_0012_criar_links_profissionais.py` para a tabela `links_profissionais`.
- Criação do router `POST /links-profissionais` e DTOs em `src/backend/api/link_profissional.py`.
- Injeção e registro de rota em `src/backend/api/factory.py`.
- Testes unitários completos para domínio, aplicação, infraestrutura e API.

### Fora do escopo

- Vinculação de links a versões de currículo (`CURRICULO_LINK`). O modelo relacional inicial não prevê essa relação direta, preservando `IdItemPerfil`, `ReferenciaCurriculo` e `ConsultaItemPerfil`.
- Edição (`PUT`/`PATCH`), listagem (`GET`) ou exclusão (`DELETE`) de links (objeto de issues subsequentes).
- Alterações no frontend.
- Modificação de arquivos fora do ecossistema de backend.

## Critérios de sucesso

1. **Aderência Arquitetural:** Separação estrita de camadas da Clean Architecture sem vazamento de ORM, FastAPI ou SQL para o domínio ou aplicação.
2. **Segurança de URLs:** Rejeição comprovada por testes de esquemas perigosos (`javascript:`, `data:`, `file:`) e URLs malformadas.
3. **Qualidade dos Testes:** 100% de aprovação nos testes unitários das 4 camadas (`test_domain_link_profissional.py`, `test_application_cadastro_link_profissional.py`, `test_infrastructure_link_profissional.py`, `test_api_link_profissional.py`), executando com sucesso em `nix develop .#backend`.
4. **Ausência de Regressões:** Zero falhas na suíte de testes existente do backend.
5. **Conformidade Estática:** Aprovação total em `nix develop .#quality --command ruff check src/backend` e sem warnings de depreciação do Starlette.
6. **Documentação:** Presença das 3 seções obrigatórias nas docstrings de todas as funções, métodos, classes e DTOs adicionados.

## Comparação de alternativas

### Alternativa 1: Implementação desacoplada com Clean Architecture, DDD, validação estrita de URL e Alembic linear (Recomendada)
- **Descrição:** Implementa a entidade `LinkProfissional` com validação de esquema/host puros no domínio, `LinkProfissionalId`, portas desacopladas, interactor na Application, persistência com `flush()` e captura de `IntegrityError`, router FastAPI com HTTP 422 moderno e migração linear no Alembic.
- **Vantagens:** Total aderência às regras do projeto, isolamento de regras de negócio, mitigação de vulnerabilidades XSS por esquemas perigosos, testabilidade determinística com test doubles puros sem necessidade de banco real nos testes unitários, prevenção de concorrência.
- **Desvantagens:** Maior número de classes e arquivos em comparação com endpoints acoplados (custo inerente e desejável de Clean Architecture).

### Alternativa 2: Exposição direta da rota no FastAPI acoplada ao SQLAlchemy (Rejeitada)
- **Descrição:** Manipular o modelo SQLAlchemy diretamente na função de rota da API sem passar por entidades de domínio ou casos de uso da Application.
- **Vantagens:** Menos arquivos criados.
- **Desvantagens:** Viola gravemente a Clean Architecture e as regras de `AGENTS.md`, acopla detalhes de framework à regra de negócio e impede testes unitários isolados.

### Alternativa 3: Permissão irrestrita de qualquer esquema de URL (Rejeitada)
- **Descrição:** Aceitar qualquer string como URL sem validar o esquema (`parsed.scheme`).
- **Vantagens:** Nenhuma sanitização necessária.
- **Desvantagens:** Violação crítica de segurança; permite o armazenamento de payloads maliciosos (`javascript:alert(1)`, `data:text/html,...`) que expõem consumidores e visualizadores de currículo a falhas de segurança.

## Decisão recomendada

Adotar a **Alternativa 1**. A modelagem em Clean Architecture segue o padrão maduro e comprovado do repositório, garantindo conformidade rigorosa com `AGENTS.md`, qualidade de testes, segurança de domínio e proteção de integridade relacional.

Arquivo criado em prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md. Avalie se o local escolhido é de fato o mais adequado.
