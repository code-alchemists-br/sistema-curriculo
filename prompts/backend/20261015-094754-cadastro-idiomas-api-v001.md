---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: "2026-10-15T09:47:54-03:00"
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
      locator: "entidade Idioma, linhas 289–302"
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "IdiomaId (linha 174) e UsuarioId"
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "protocolos de repositório e gerador de ID"
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
    - path: src/backend/application/cadastro_competencia.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
    - path: src/backend/api/competencia.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/competencia.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/repositorio_competencia.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
    - path: src/backend/infrastructure/identificadores/geradores.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/metadata.py
      relationship: supporting
      representation: source-code
      function: configuration
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: mermaid-markdown
      analysis_scope: selected-section
      locator: "entidade IDIOMA e relações com USUARIO e CURRICULO_IDIOMA"
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF01–RF03"
      content_state: working-tree
      revision: "working-tree based on 2286d034836b9d135c1d494cf364746823b4e08d"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos]
  confidence: high
  rationale: "A decisão delimita arquitetura, regras de domínio, portas, orquestração, persistência relacional Code First e router HTTP de backend para o cadastro de idioma."
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

# Análise de decisão — Cadastro de idioma e nível de proficiência pela API

## Solicitação original

> Issue #97: Expor cadastro de idioma. Tarefa da fatia vertical atribuída a @mariacarolinayamamoto. Inclua os testes unitários pertinentes.
> Plano executivo aprovado: Implementar o endpoint de cadastro de idioma do backend respeitando rigorosamente a Clean Architecture, DDD, AGENTS.md e o fluxo de skills ($decision-analysis-v4 -> $backend-domain-orchestration-v2 -> $backend-adapters-drivers-v2).

## Informações complementares

- Tarefa com prazo ultrapassado (11/10/2026), identificada como prioridade máxima de atuação conforme alinhamento com o PM.
- Reatribuída a `minoruhaga` no GitHub.
- Padrão arquitetural já consolidado no repositório em `competencia.py`, `formacao_academica.py` e `experiencia_profissional.py`.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem | Nenhuma | v001 | Análise inicial | Não há versão anterior a comparar. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/domain/itens_perfil.py` | Principal | Código-fonte | Produção | Python | Entidade `Idioma` (L289–L302) | Working tree baseado em `2286d03` |
| `src/backend/domain/value_objects.py` | Principal | Código-fonte | Produção | Python | `IdiomaId` e `UsuarioId` | Working tree baseado em `2286d03` |
| `src/backend/application/ports.py` | Principal | Código-fonte | Produção | Python | Protocolos de repositório e ID | Working tree baseado em `2286d03` |
| `src/backend/application/cadastro_competencia.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree baseado em `2286d03` |
| `src/backend/api/competencia.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree baseado em `2286d03` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Registro de rotas e injeção | Working tree baseado em `2286d03` |
| `src/backend/infrastructure/persistence/sqlalchemy/competencia.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree baseado em `2286d03` |
| `src/backend/infrastructure/persistence/sqlalchemy/repositorio_competencia.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Working tree baseado em `2286d03` |
| `src/backend/infrastructure/identificadores/geradores.py` | Apoio | Código-fonte | Produção | Python | Geradores de UUID4 | Working tree baseado em `2286d03` |
| `src/backend/infrastructure/persistence/sqlalchemy/metadata.py` | Apoio | Código/configuração | Configuração | Python | Registro de modelos | Working tree baseado em `2286d03` |
| `docs/modelagem_der.md` | Apoio | Modelo de diagrama | Contrato de schema | Mermaid/Markdown | Entidade `IDIOMA` | Working tree baseado em `2286d03` |
| `docs/requisitos_funcionais.md` | Contexto | Prosa | Documentação | Markdown | RF01–RF03 | Working tree baseado em `2286d03` |

### Limites da evidência dos artefatos

O DER define os atributos de `IDIOMA` como `uuid id PK`, `uuid usuario_id FK`, `string idioma` e `string nivel`. Não há especificação no DER ou nos requisitos funcionais de um vocabulário fechado (enum) para `nivel` de idioma (ex.: "Básico", "Intermediário", "Avançado", "Fluente", "Nativo", A1-C2) ou lista pré-aprovada de idiomas. Assim como decidido para `Competencia`, o domínio deve tratar `idioma` e `nivel` como textos não vazios com espaços aparados, enquanto uma taxonomia controlada não for formalizada pelo produto.

## Problema enriquecido

### Resultado desejado

Disponibilizar endpoint autenticado `POST /idiomas` que permita ao estudante autenticado registrar um idioma com respectivo nível de proficiência, persistindo-o de forma independente em tabela relacional `idiomas` (Code First com SQLAlchemy e Alembic) e retornando o recurso público criado (HTTP 201), garantindo isolamento de dados entre estudantes, rejeição de payloads inválidos (HTTP 422), prevenção de duplicidades lógicas (HTTP 409) e cobertura unitária com doubles.

### Atores e interesses

- **Estudante:** Deseja cadastrar idiomas conhecidos e seus níveis de proficiência para compor versões futuras de currículos.
- **Camada de API (FastAPI):** Deve proteger o endpoint, extraindo a identidade do estudante exclusivamente de `request.state.usuario_id` (sessão autenticada) e rejeitando requisições anônimas com HTTP 401, sem permitir que o cliente forneça o `usuario_id` no corpo da requisição.
- **Camada de Aplicação (Use Case):** Deve orquestrar a geração de ID via porta tipada, validação de invariantes, checagem assíncrona de duplicidade e delegação de persistência.
- **Camada de Domínio:** Deve manter a entidade `Idioma` válida e imutável desde a criação, garantindo que textos obrigatórios estejam preenchidos e fornecendo chave canônica de normalização (`idioma_normalizado`).
- **Camada de Infraestrutura:** Deve implementar `RepositorioIdiomaSqlAlchemy` e `GeradorIdiomaIdUuid4`, mapear a tabela `idiomas` no SQLAlchemy com constraint de unicidade `uq_idiomas_usuario_idioma_normalizado` e gerar a migration correspondente no Alembic.

### Evidências e fatos observados

- `Idioma` e `IdiomaId` já existem em `src/backend/domain/itens_perfil.py` e `src/backend/domain/value_objects.py`, criados em refatoração anterior, mas sem método `__post_init__` ou propriedade de normalização.
- Todos os endpoints de itens de perfil (competência, formação acadêmica, experiência profissional) adotam padrão REST estrito com verbos HTTP, DTOs Pydantic de entrada/saída, validação de sessão em `request.state` e tratamento padronizado de códigos de status (201, 401, 409, 422, 503).
- O repositório impõe teste unitário rigoroso via ambiente Nix `.#backend`, e linter via `.#quality`.

### Hipóteses

1. A duplicidade de idioma para um mesmo estudante deve ser verificada pelo nome do idioma normalizado (colapso de espaços internos e `casefold()`). Um estudante não deve cadastrar "Inglês" duas vezes com níveis diferentes; caso queira atualizar o nível, isso pertence a um caso de uso futuro de edição (`PUT`/`PATCH`).
2. O campo `nivel` não deve possuir enum fechado nesta fase para manter compatibilidade com a modelagem do DER (`string nivel`) e a entidade existente em `itens_perfil.py`.
3. A rota pública de cadastro deve ser `POST /idiomas`, padronizada com as rotas autenticadas (`POST /competencias`, `POST /experiencias-profissionais`, `POST /formacoes-academicas`).

### Perguntas em aberto

Nenhum identificado. O padrão do repositório já resolveu todas as ambiguidades estruturais em casos análogos anteriores.

### Escopo

- Adição de invariantes (`__post_init__`) e chave canônica (`idioma_normalizado`) na entidade `Idioma` em `src/backend/domain/itens_perfil.py`.
- Definição das portas `RepositorioIdioma` e `GeradorIdiomaId` em `src/backend/application/ports.py`.
- Criação do caso de uso `CadastrarIdioma`, DTO `CadastrarIdiomaEntrada` e exceção `IdiomaJaCadastrado` em `src/backend/application/cadastro_idioma.py`.
- Implementação de `GeradorIdiomaIdUuid4` em `src/backend/infrastructure/identificadores/geradores.py`.
- Implementação de `IdiomaRegistro`, funções de conversão `para_registro` e `para_idioma` em `src/backend/infrastructure/persistence/sqlalchemy/idioma.py`.
- Implementação de `RepositorioIdiomaSqlAlchemy` em `src/backend/infrastructure/persistence/sqlalchemy/repositorio_idioma.py`.
- Registro de `IdiomaRegistro` em `src/backend/infrastructure/persistence/sqlalchemy/metadata.py`.
- Criação de migration Alembic para a tabela `idiomas`.
- Criação do router `POST /idiomas` e DTOs em `src/backend/api/idioma.py`.
- Injeção e registro de rota em `src/backend/api/factory.py`.
- Testes unitários completos para domínio, aplicação, infraestrutura e API.

### Fora do escopo

- Edição (`PUT`/`PATCH`) ou exclusão (`DELETE`) de idioma (pertencem a outras issues do backlog).
- Seleção e ordenação de idiomas em versões de currículo (`CURRICULO_IDIOMA`).
- Telas ou componentes de frontend.
- Testes integrados ou end-to-end com banco de dados real (devem ser tratados via `$integration-system-testing-v1`).
- Alterações em mecanismos globais de autenticação, sessão ou middlewares.

### Critérios de sucesso

1. Testes unitários de domínio cobrindo criação válida, rejeição de campos vazios ou somente espaços e normalização da chave de idioma.
2. Testes unitários de aplicação cobrindo sucesso, geração de ID, consulta de duplicidade e emissão de `IdiomaJaCadastrado`.
3. Testes unitários de infraestrutura cobrindo conversão bidirecional domínio-ORM e detecção de violação de unicidade (`IntegrityError`).
4. Testes unitários de API cobrindo respostas 201 Created, 401 Unauthorized, 409 Conflict, 422 Unprocessable Content e 503 Service Unavailable.
5. 100% de aprovação na suíte de testes em `nix develop .#backend`.
6. Zero inconformidades no linter em `nix develop .#quality --command ruff check src/backend`.
7. Docstrings completas com os três tópicos obrigatórios em todas as funções, métodos, classes e DTOs.

## Restrições aplicáveis

- **AGENTS.md (Raiz):** Uso obrigatório do ambiente Nix para ferramentas de desenvolvimento (`backend` para testes unitários; `quality` para ruff). Operações Git/GitHub fora do Nix. Docstrings com *o que faz*, *como faz* e *qual finalidade atende*.
- **src/backend/AGENTS.md:** Princípios da Clean Architecture: dependências apontando para dentro. Domínio e Application sem dependências de infraestrutura, FastAPI ou SQLAlchemy. Code First para persistência relacional. DDD: linguagem ubíqua e proteção de invariantes.
- **GUIA-DE-USO-DAS-SKILLS-v001.md:** Divisão estrita de papéis: `$backend-domain-orchestration-v2` apenas para núcleo e seus testes unitários; `$backend-adapters-drivers-v2` para adapters e drivers e seus testes unitários.

## Classificação comentada

- **sphere: engineering:** Trata-se da implementação arquitetural e desenvolvimento do componente de backend.
- **concerns: [domain, architecture, data]:** Abrange a camada de domínio (entidade e invariantes), arquitetura em camadas (Clean Architecture) e persistência relacional com migração Code First.
- **decision_kind: design:** Define contratos de portas, DTOs de fronteira e mapeamento relacional.
- **scope: component:** Restrito ao componente backend e suas subpastas `domain`, `application`, `infrastructure` e `api`.
- **lifecycle: design:** Fase de especificação de design que antecede as alterações de código.
- **urgency: time-critical:** Demanda com prazo de entrega vencido (Fatia Vertical, 11/10/2026).
- **uncertainty: low:** Padrões idênticos já foram estabelecidos para competências e formações acadêmicas.
- **reversibility: moderate:** Envolve migration de banco e contratos de API, reversíveis por migrations de downgrade e versionamento de rotas.
- **risk: medium:** Risco contido em caso de falha de unicidade ou quebra de regressão de rotas existentes, mitigado pela suíte de testes.

## Decisão de roteamento

- **Raiz:** `prompts`
- **Diretório selecionado:** `prompts/backend`
- **Diretórios considerados:** `prompts/backend`, `prompts/requisitos`
- **Confiança:** high
- **Justificativa:** O artefato define uma decisão estritamente técnica de backend (Clean Architecture, DDD, FastAPI, SQLAlchemy e Alembic).

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | 1 | Maximizada (+2) | Garantir que dados inválidos ou duplicados sejam rejeitados e invariantes protegidas. |
| `security` | 2 | Maximizada (+2) | Garantir que o estudante não possa cadastrar idiomas para outro usuário (isolamento de conta). |
| `simplicity` | 3 | Satisfeita por limiar (+1) | Seguir o design existente de competências sem criar abstrações desnecessárias. |
| `modifiability` | 4 | Satisfeita por limiar (+1) | Preservar a Clean Architecture para permitir futuras evoluções (ex.: enumeração de níveis ou vínculo a currículos). |
| `time-to-value` | 5 | Maximizada (+2) | Permitir implementação célere e segura da issue atrasada da fatia vertical. |

## Alternativas consideradas

### Alternativa A: Espelhar o padrão de `Competencia` (Recomendada)
- Endpoint `POST /idiomas` com autenticação por sessão (`request.state.usuario_id`).
- Entidade `Idioma` com validação de textos não vazios e normalização via `idioma_normalizado` (colapso de espaços e `casefold`).
- Porta `RepositorioIdioma` com verificação de duplicidade e salvamento.
- Mapeamento `IdiomaRegistro` em SQLAlchemy com `UniqueConstraint("usuario_id", "idioma_normalizado")`.
- Casos de uso e adapters independentes, testados unitariamente com doubles.

### Alternativa B: Rota aninhada sob estudantes (`POST /estudantes/{usuario_id}/idiomas`)
- Rota recebendo o ID do usuário no path, como feito em `dados_contato.py`.
- Exige validação explícita de correspondência entre o `usuario_id` da rota e o `usuario_id` da sessão autenticada.
- Adiciona redundância desnecessária na rota e complexidade de validação de permissão.

### Alternativa C: Fechar os níveis de proficiência em Enum no Domínio
- Criar um `Enum` (ex.: BASICO, INTERMEDIARIO, AVANCADO, FLUENTE).
- Quebra compatibilidade com o DER e exige aprovação de produto, além de restringir termos como "Nativo", classificações CEFR (A1, A2, B1, etc.) ou descrições flexíveis.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | 1 | +2 | +1 | +1 | High | Invariantes no domínio e unicidade composta no banco. |
| `security` | 2 | +2 | +1 | +2 | High | Alternativa A elimina risco de ID spoofing no path. |
| `simplicity` | 3 | +2 | 0 | -1 | High | Alternativa A reutiliza arquitetura idêntica já testada. |
| `modifiability` | 4 | +2 | +1 | 0 | High | Facilidade de evolução sem acoplamento a enums precoces. |
| `time-to-value` | 5 | +2 | +1 | 0 | High | Execução direta e segura. |

## Histórico e decisão atual

### Decisão da versão anterior
Nenhuma (versão inicial `v001`).

### Decisão recomendada nesta versão
Adotar a **Alternativa A**:
1. Entidade de domínio `Idioma` enriquecida com `__post_init__` e `idioma_normalizado`.
2. Caso de uso `CadastrarIdioma` com portas `RepositorioIdioma` e `GeradorIdiomaId`.
3. Persistência `IdiomaRegistro` com constraint `uq_idiomas_usuario_idioma_normalizado`.
4. Router `POST /idiomas` extraindo usuário da autenticação e devolvendo 201 Created.
5. Testes unitários com doubles em todas as camadas.

### Impacto da revisão
Decisão inicial que destrava a implementação direta das Etapas 2 e 3 do plano de execução.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | Maximized | Invariantes protegidas antes de persistir; garantia contra duplicações. | Testes unitários e constraint de banco. |
| `security` | Maximized | Impossibilidade de cadastrar dados em nome de outro estudante. | Usuário injetado pelo middleware de sessão. |
| `time-to-value` | Maximized | Redução do tempo de entrega da issue atrasada #97. | Reutilização de blueprint testado e consolidado. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `simplicity` | Código limpo e idiomático sem overengineering. | Mantém campos de texto validados sem enum prematuro. |
| `modifiability` | Clean Architecture estrita. | Camadas desacopladas via portas e DTOs dedicados. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Inconsistência de dados ou duplicações no perfil do estudante. | Alta | Estudantes e recrutadores. |
| `security` | Vulnerabilidade de autorização caso o ID viesse do payload do cliente. | Crítica | Todo o sistema. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `correctness` | Criação de tabelas, DTOs e mapeamentos adicionais. | Esforço de código inicial | Perfeitamente aceitável pelo ganho em robustez. |
| `simplicity` | Deixar níveis como texto livre nesta fase. | Padronização formal de vocabulário | Aceitável até definição formal de produto. |

## Riscos e efeitos de segunda ordem

- **Risco de colisão de migração Alembic:** Verificado que a branch atual possui cabeças reconciliadas; a nova migration dependerá explicitamente do head atual (`20261014_0007`).
- **Risco de concorrência:** Duas requisições paralelas para o mesmo idioma podem passar pela checagem em memória do repositório; o banco protegerá com `UniqueConstraint`, e o adapter traduzirá o `IntegrityError` em `IdiomaJaCadastrado` (HTTP 409).

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Invariantes e normalização | Testes unitários de domínio passando. | `python -m unittest test_domain_idioma.py` | Aceitação de idioma vazio ou falha na normalização. |
| Bloqueio de duplicidade | Teste unitário de use case e repositório. | `python -m unittest test_application_cadastro_idioma.py` | Criação repetida de idiomas equivalentes. |
| Segurança de rota | Teste unitário de API sem autenticação. | `python -m unittest test_api_idioma.py` | Resposta diferente de 401 Unauthorized. |
| Integridade de estilo | Zero avisos do Ruff. | `ruff check src/backend` | Violações de estilo ou tipagem. |

## Handoffs e atividades posteriores

1. **Handoff para `$backend-domain-orchestration-v2`:**
   - Implementar regras de domínio em `src/backend/domain/itens_perfil.py`.
   - Implementar portas em `src/backend/application/ports.py`.
   - Implementar caso de uso em `src/backend/application/cadastro_idioma.py`.
   - Implementar testes unitários em `src/backend/tests/test_domain_idioma.py` e `src/backend/tests/test_application_cadastro_idioma.py`.
2. **Handoff para `$backend-adapters-drivers-v2`:**
   - Implementar gerador de ID em `src/backend/infrastructure/identificadores/geradores.py`.
   - Implementar mapeamento SQLAlchemy e repositório em `src/backend/infrastructure/persistence/sqlalchemy/`.
   - Criar migration Alembic.
   - Implementar router FastAPI em `src/backend/api/idioma.py` e registrar em `src/backend/api/factory.py`.
   - Implementar testes unitários em `src/backend/tests/test_infrastructure_idioma.py` e `src/backend/tests/test_api_idioma.py`.

## Síntese

A análise estabelece a especificação completa para o cadastro de idiomas do estudante na API, garantindo respeito às fronteiras de Clean Architecture, proteção de invariantes e testes unitários com test doubles, viabilizando a entrega segura e rápida da Issue atrasada #97.

Arquivo criado em prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md. Avalie se o local escolhido é de fato o mais adequado.
