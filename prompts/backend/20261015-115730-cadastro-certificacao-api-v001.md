---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-15T11:57:30-03:00"
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
      locator: "itens reutilizáveis de perfil e funções de normalização"
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "value objects tipados de identidade (UsuarioId, etc.)"
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "protocolos de repositório e geradores de ID"
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
    - path: src/backend/application/cadastro_idioma.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
    - path: src/backend/api/idioma.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/idioma.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_idioma.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
    - path: src/backend/infrastructure/identificadores/geradores.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/metadata.py
      relationship: supporting
      representation: source-code
      function: configuration
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261015_0009_criar_idiomas.py
      relationship: supporting
      representation: source-code
      function: database-migration
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: mermaid-markdown
      analysis_scope: selected-section
      locator: "modelagem de itens reutilizáveis do perfil"
      content_state: working-tree
      revision: "working-tree based on fe383e4776100ca4beea11bc40e70e4e75c6ebce"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "A decisão delimita arquitetura, regras de domínio, portas, orquestração, persistência relacional Code First e router HTTP de backend para o cadastro de certificação."
classification:
  sphere: engineering
  concerns: [domain, architecture, data]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: time-critical
  uncertainty: low
  reversibility: moderate
  risk: medium
---

# Análise de decisão — Cadastro de certificação pela API

## Solicitação original

> Issue #100: Expor cadastro de certificação. Tarefa da fatia vertical atribuída a @mariacarolinayamamoto. Inclua os testes unitários pertinentes.
> Subtarefas correlatas:
> - [F4.1] (#271): Definir o modelo de domínio de certificação e suas invariantes mínimas.
> - [F4.2] (#272): Criar porta e caso de uso para cadastrar certificação; cobrir regra de domínio.
> - [F4.3] (#273): Implementar adaptador de persistência de certificação e teste de mapeamento.
> - [F4.4] (#275): Expor o cadastro de certificação na API e validar a requisição.
> Refinamentos acordados:
> - Explicitar fora de escopo a vinculação a currículos (CURRICULO_CERTIFICACAO), preservando IdItemPerfil e ReferenciaCurriculo.
> - Alinhar o down_revision do Alembic rigorosamente com os heads ativos de dev.
> - Garantir a execução de testes e linters exclusivamente nos ambientes Nix (.#backend e .#quality).

## Informações complementares

- Tarefa com prazo ultrapassado (11/10/2026), prioridade máxima alinhada com o PM.
- Reatribuída a `minoruhaga` no GitHub.
- Padrão arquitetural já consolidado no repositório em `idioma.py`, `competencia.py`, `formacao_academica.py` e `experiencia_profissional.py`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem | Nenhuma | v001 | Análise inicial | Não há versão anterior a comparar. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/itens_perfil.py` | Principal | Código-fonte | Produção | Python | Itens do perfil e normalização | Working tree baseado em `fe383e4` |
| `src/backend/domain/value_objects.py` | Principal | Código-fonte | Produção | Python | Value objects tipados | Working tree baseado em `fe383e4` |
| `src/backend/application/ports.py` | Principal | Código-fonte | Produção | Python | Protocolos de repositório e ID | Working tree baseado em `fe383e4` |
| `src/backend/application/cadastro_idioma.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree baseado em `fe383e4` |
| `src/backend/api/idioma.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree baseado em `fe383e4` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Registro de rotas e injeção | Working tree baseado em `fe383e4` |
| `src/backend/infrastructure/persistence/sqlalchemy/idioma.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree baseado em `fe383e4` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_idioma.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree baseado em `fe383e4` |
| `src/backend/infrastructure/identificadores/geradores.py` | Apoio | Código-fonte | Produção | Python | Geradores de UUID4 | Working tree baseado em `fe383e4` |
| `src/backend/infrastructure/persistence/sqlalchemy/metadata.py` | Apoio | Código/configuração | Configuração | Python | Registro de modelos | Working tree baseado em `fe383e4` |
| `src/backend/infrastructure/persistence/alembic/versions/20261015_0009_criar_idiomas.py` | Apoio | Código-fonte | Migração | Python | Arquivo completo | Working tree baseado em `fe383e4` |
| `docs/modelagem_der.md` | Apoio | Modelo de diagrama | Contrato de schema | Mermaid/Markdown | Itens do perfil | Working tree baseado em `fe383e4` |

### Limites da evidência dos artefatos

O `modelagem_der.md` modela itens reutilizáveis do perfil profissional do estudante vinculados diretamente ao usuário. A certificação possui os campos essenciais: `id` (UUID), `usuario_id` (UUID), `nome` (Text) e `organizacao_emissora` (Text). A vinculação a versões de currículo (`CURRICULO_CERTIFICACAO`) não existia na modelagem inicial e sua introdução prematura ampliaria desnecessariamente o escopo da fatia vertical. A integridade textual requer aparo de espaços e validação de não-vazio, além de normalização de espaços e caixa (`casefold`) para a prevenção determinística de duplicidades.

## Problema enriquecido

### Resultado desejado

Disponibilizar endpoint autenticado `POST /certificacoes` que permita ao estudante autenticado registrar uma certificação (com nome e organização emissora), persistindo-a de forma independente em tabela relacional `certificacoes` (Code First com SQLAlchemy e Alembic) e retornando o recurso público criado (HTTP 201), garantindo isolamento de dados entre estudantes, rejeição de payloads inválidos (HTTP 422), prevenção de duplicidades lógicas (HTTP 409) e cobertura unitária com test doubles.

### Atores e beneficiários

- **Estudante autenticado:** Pode enriquecer seu perfil profissional adicionando suas certificações e instituições emissoras.
- **Camadas do Backend (Clean Architecture):** Núcleo de domínio e orquestração isolados de banco de dados e transporte web, respeitando a inversão de dependências.

### Fatos observados

1. O backend já possui entidades de perfil análogas (`Competencia`, `Idioma`, `FormacaoAcademica`, `ExperienciaProfissional`).
2. A branch de trabalho deriva de `dev` atualizada, contendo a migração `20261015_0009_criar_idiomas.py`.
3. As subtarefas [F4.1] a [F4.4] foram planejadas para estruturar a criação em 4 etapas: domínio, portas/caso de uso, persistência e API.
4. O repositório exige docstrings nos 3 tópicos obrigatórios (*o que faz*, *como faz*, *qual finalidade atende*) e execução em shells Nix.

### Hipóteses adotadas

1. **Campos Obrigatórios:** A certificação exige obrigatoriamente `nome` e `organizacao_emissora`. Não há necessidade de data de emissão ou validade nesta fatia vertical (mantendo paridade estrita com o frontend existente em `FormularioCursos.tsx` e o histórico de domínio).
2. **Critério de Duplicidade:** Uma certificação é considerada duplicada para um mesmo estudante se houver equivalência de `(usuario_id, nome_normalizado, organizacao_emissora_normalizada)`, colapsando espaços intermediários e aplicando `casefold()`.
3. **Escopo Estrito de Perfil:** Não vincular neste momento a certificação a versões de currículo, preservando os agregados de currículo intactos.

### Restrições duras

1. **Clean Architecture e DDD:** Proibido acoplar `Domain` e `Application` a SQLAlchemy, FastAPI ou Pydantic.
2. **Autenticação:** O `usuario_id` deve ser extraído do estado seguro da requisição (`request.state.usuario_id`); nunca recebido do payload externo.
3. **Persistência Code First:** O schema relacional deve ser definido por modelos SQLAlchemy registrados em `metadata.py` e migrados via Alembic.
4. **Governança Nix:** Todos os testes unitários rodam em `nix develop .#backend` e o linter em `nix develop .#quality`.

## Comparação de alternativas

### Alternativa A: Abordagem Alinhada com a Clean Architecture, DDD e Padrão dos Itens de Perfil (Recomendada)

- **Descrição:**
  1. No Domínio: Criar `CertificacaoId` (Value Object validando UUID) e entidade `Certificacao(id, usuario_id, nome, organizacao_emissora)` com normalização canônica (`split()` e `casefold()`) e propriedades `nome_normalizado` e `organizacao_emissora_normalizada`.
  2. Na Application: Definir portas `RepositorioCertificacao` e `GeradorCertificacaoId`. Criar interactor `CadastrarCertificacao`, DTO de entrada e exceção `CertificacaoJaCadastrada`.
  3. Na Infraestrutura: Mapeamento `CertificacaoRegistro`, migração Alembic criando tabela `certificacoes` com constraint única composta, e repositório `RepositorioCertificacaoSqlAlchemy`.
  4. Na API: Router FastAPI `POST /certificacoes` consumindo protocolo de executor e respondendo HTTP 201 Created com tratamento de 401, 409, 422 e 503.
- **Vantagens:**
  - 100% aderente ao padrão estabelecido em `idioma.py` e `competencia.py`.
  - Separação cristalina de responsabilidades e testabilidade pura por camadas.
  - Zero dependência externa no núcleo de domínio.
- **Desvantagens:**
  - Exige criação de múltiplos arquivos pequenos e focados.

### Alternativa B: Acoplamento Direto ou Inclusão Prematura de Associação a Currículo

- **Descrição:** Adicionar `Certificacao` diretamente aos enums de currículo (`IdItemPerfil`, `ReferenciaCurriculo`, `ConsultaItemPerfil`) ou manipular o banco sem entidades ricas de domínio.
- **Por que é inviável:**
  - Viola a delimitação de escopo e não-objetivos aprovados pelo usuário.
  - Altera regras centrais de currículo que não foram solicitadas na Issue #100.
  - Aumenta o risco de regressão em testes já consolidados de prévia de currículo.

## Decisão

Adotar a **Alternativa A**, dividindo a execução entre as skills especializadas conforme aprovado no plano:
- Etapa 2 via `$backend-domain-orchestration-v2`.
- Etapa 3 via `$backend-adapters-drivers-v2`.

## Alinhamento da Migração Alembic (Linearidade do Schema)

Para garantir um grafo de migrações limpo e linear:
- Revisão: `20261015_0010` (arquivo `20261015_0010_criar_certificacoes.py`).
- Como a branch `dev` atual contém dois heads (`20261014_0009` e `20261015_0009`), esta nova migração dependerá de ambos:
  `down_revision = ("20261014_0009", "20261015_0009")`
- Isso unifica o histórico de migrações do repositório em um único head consistente (`20261015_0010`), eliminando heads paralelos e garantindo estabilidade nas execuções de testes e deploy.

## Plano de Handoffs

1. **Handoff 1 -> Etapa 2 ($backend-domain-orchestration-v2):**
   - Criar `CertificacaoId` em `src/backend/domain/value_objects.py`.
   - Criar função de normalização e entidade `Certificacao` em `src/backend/domain/itens_perfil.py`.
   - Exportar em `src/backend/domain/__init__.py`.
   - Criar protocolos `RepositorioCertificacao` e `GeradorCertificacaoId` em `src/backend/application/ports.py`.
   - Criar `src/backend/application/cadastro_certificacao.py`.
   - Exportar em `src/backend/application/__init__.py`.
   - Implementar testes unitários em `src/backend/tests/test_domain_certificacao.py` e `src/backend/tests/test_application_cadastro_certificacao.py`.
   - Validar testes em `nix develop .#backend`.

2. **Handoff 2 -> Etapa 3 ($backend-adapters-drivers-v2):**
   - Implementar `GeradorCertificacaoIdUuid4` em `src/backend/infrastructure/identificadores/geradores.py`.
   - Criar modelo `CertificacaoRegistro` e funções de conversão em `src/backend/infrastructure/persistence/sqlalchemy/certificacao.py`.
   - Registrar em `src/backend/infrastructure/persistence/sqlalchemy/metadata.py`.
   - Implementar `RepositorioCertificacaoSqlAlchemy` em `src/backend/infrastructure/persistence/sqlalchemy/repositorio_certificacao.py`.
   - Criar migração Alembic `20261015_0010_criar_certificacoes.py`.
   - Criar router `POST /certificacoes` em `src/backend/api/certificacao.py`.
   - Integrar router na fábrica central `src/backend/api/factory.py`.
   - Implementar testes unitários em `src/backend/tests/test_infrastructure_certificacao.py` e `src/backend/tests/test_api_certificacao.py`.
   - Validar testes em `nix develop .#backend`.

3. **Handoff 3 -> Validação dos Gates Nix:**
   - Rodar suíte completa em `nix develop .#backend`.
   - Rodar `ruff check src/backend` em `nix develop .#quality`.
   - Auditar docstrings completas (o que faz, como faz, qual finalidade atende).
