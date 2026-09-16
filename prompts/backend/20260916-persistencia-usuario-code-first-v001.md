---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v001"
status: proposed
created_at: 2026-09-16
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
    - path: src/backend/application/ports.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: src/backend/domain/entities.py
      relationship: primary
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: markdown-mermaid
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: prompts/backend/20260916-cadastro-acesso-estudante-v002.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: prompts/ambientes/20260916-fundamentos-backend-nix-v002.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/ambientes]
  confidence: high
  rationale: "A decisão cria um adapter de persistência para contrato interno do backend; o ambiente é dependência de apoio."
classification:
  sphere: engineering
  concerns: [architecture, data, implementation]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — persistência Code First do usuário

## Solicitação original

`$decision-analysis-v4 crie uma análise com referenci as portas de repositório e mapeamentos SQLAlchemy/Alembic na infraestrutura Code First.`

## Informações complementares

- `RepositorioUsuario` já define `existe_por_email` e `salvar` como operações assíncronas.
- A pilha aprovada é SQLAlchemy assíncrono, Psycopg assíncrono e Alembic; `asyncpg` não é necessário.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem | Nenhum identificado | v001 inicial | Não há análise anterior de persistência | Nenhum histórico a preservar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `src/backend/application/ports.py` | Principal | Código | Produção | Python | Completo | Working tree baseado em `1188723` |
| `src/backend/domain/entities.py` | Principal | Código | Produção | Python | Completo | Commit `1188723` |
| `docs/modelagem_der.md` | Apoio | Modelo | Contrato de schema | Mermaid | Completo | Commit `1188723` |
| `prompts/backend/20260916-cadastro-acesso-estudante-v002.md` | Apoio | Prosa | Documentação | Markdown | Completo | Working tree baseado em `1188723` |
| `prompts/ambientes/20260916-fundamentos-backend-nix-v002.md` | Apoio | Prosa | Documentação | Markdown | Completo | Working tree baseado em `1188723` |

### Limites da evidência dos artefatos

Não foram criados banco, URL, credenciais, pool nem migration. O DER não decide
políticas de remoção, sessão ou todos os agregados; a decisão limita-se à tabela
e ao repositório de `Usuario` necessários para o cadastro.

## Problema enriquecido

### Resultado desejado

Implementar na infraestrutura um mapeamento Code First de `Usuario`, migration
Alembic versionada e repositório assíncrono que satisfaça `RepositorioUsuario`.

### Atores e interesses

- Application precisa persistir sem importar ORM ou driver.
- Infraestrutura precisa garantir unicidade de e-mail também sob concorrência.
- Operação precisa schema reproduzível por migrations.

### Evidências e fatos observados

- `Usuario` possui UUID, nome, e-mail e hash de senha.
- A porta precisa consultar e salvar assincronamente.
- Os fundamentos proíbem criação automática de tabelas no startup.

### Hipóteses

- Uma tabela `usuarios` com `id` UUID como chave primária e `email` único cobre
  a fatia atual; nome e hash são campos textuais não nulos.
- O adapter converterá explicitamente colunas e value objects, sem tornar o
  domínio um modelo ORM.

### Perguntas em aberto

- URL, pool, timeout, gestão de `AsyncSession` e tradução de violação única para
  erro de aplicação ainda exigem composição externa e integração.

### Escopo

- Criar metadata e mapeamento SQLAlchemy de `Usuario` na infraestrutura.
- Criar migration Alembic inicial correspondente.
- Criar repositório com `AsyncSession` que implemente as duas operações da porta.
- Criar apenas testes unitários isolados do adapter; integração fica posterior.

### Fora do escopo

- Alterar domínio, portas, caso de uso, API ou autenticação.
- Mapear currículos, itens de perfil, sessões, tokens ou integrações.
- Executar migration contra banco real ou configurar serviço PostgreSQL.

### Critérios de sucesso

- Mapeamento externo preserva `Usuario` e seus value objects.
- Migration cria `usuarios` com PK UUID e unicidade de e-mail.
- Repositório usa `AsyncSession` e satisfaz `RepositorioUsuario` sem ORM no núcleo.

## Restrições aplicáveis

- Domínio e Application não importam SQLAlchemy, Psycopg ou Alembic.
- Code First e Alembic são a fonte de verdade; scripts SQL manuais não são.
- Dependências são usadas somente pelo ambiente Nix.

## Classificação comentada

É uma decisão de engenharia de dados e infraestrutura: materializa contrato
interno em persistência externa, preservando Clean Architecture e I/O assíncrono.

## Decisão de roteamento

`prompts/backend` é a pasta mais específica para adapter e mapeamento do
backend; `prompts/ambientes` é candidata somente pela dependência Nix.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Correção | Alta | Satisfazer | E-mail único deve resistir a concorrência. |
| Separação arquitetural | Alta | Satisfazer | ORM fica na infraestrutura. |
| Reprodutibilidade | Alta | Maximizar | Schema evolui por Alembic. |
| Performance | Média | Satisfazer | Repositório não bloqueia I/O. |

## Alternativas consideradas

### Alternativa A — Repositório em memória ou SQL manual

Não fornece persistência Code First nem restrição de banco; é inviável.

### Alternativa B — SQLAlchemy 2.x assíncrono, mapeamento externo e Alembic

Mapeia somente `Usuario`, usa `AsyncSession`, Psycopg e migration versionada.
É a alternativa recomendada.

### Alternativa C — ORM no domínio ou criação de schema no startup

Viola Clean Architecture e a regra de migrations; é inviável.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Correção | Alta | -2 | +2 | 0 | Alta | Restrição única no banco. |
| Separação arquitetural | Alta | +1 | +2 | -2 | Alta | Regras do backend. |
| Reprodutibilidade | Alta | -2 | +2 | -2 | Alta | Code First e Alembic. |
| Performance | Média | -1 | +2 | 0 | Alta | Porta assíncrona existente. |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### Decisão recomendada nesta versão

Adotar a Alternativa B: criar infraestrutura `persistence/sqlalchemy` com
metadata e mapeamento imperativo ou equivalente externo de `Usuario`; criar uma
migration Alembic que defina `usuarios(id UUID PK, nome, email UNIQUE,
hash_senha)`; implementar `RepositorioUsuarioSqlAlchemy` com `AsyncSession`.
A consulta deve retornar existência por e-mail; o salvamento deve persistir o
agregado, deixando commit e ciclo de transação para a composição externa.

### Impacto da revisão

Análise inicial; nenhum impacto de revisão.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Reprodutibilidade | maximized | Schema versionado acompanha o código. | Alembic. |
| Separação arquitetural | prioritized | ORM não contamina o domínio. | Mapeamento externo. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Correção | Unicidade garantida pelo banco | Coluna `email` possui restrição única. |
| Performance | I/O aguardável | Adapter depende de `AsyncSession`. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Correção | Cadastros concorrentes duplicam e-mail. | Alta | Usuários. |
| Reprodutibilidade | Schema diverge entre ambientes. | Alta | Equipe e operação. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Reprodutibilidade | Criar metadata e migration explícitas. | Time-to-value | Aceitável. |
| Separação arquitetural | Converter entidade e value objects no adapter. | Simplicidade local | Aceitável. |

## Riscos e efeitos de segunda ordem

- A checagem prévia de e-mail não substitui a constraint única.
- Uma `AsyncSession` compartilhada entre requisições compromete transações.
- Conflito de constraint deve ser traduzido por decisão posterior de aplicação/API.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Adapter cumpre porta | Teste unitário com sessão simulada | `nix develop .#backend` | Método não aguardável. |
| Schema corresponde ao código | Revision Alembic e metadata | Revisão estática | Coluna ou constraint ausente. |
| Persistência real funciona | PostgreSQL e migration | Integração em `.#tests` | Falha de dialeto ou transação. |

## Handoffs e atividades posteriores

- `$backend-adapters-drivers-v2`: implementar mapeamento, migration, adapter e testes unitários.
- `$integration-system-testing-v1`: executar migration e validar concorrência em PostgreSQL.
- `$cross-cutting-implementation-v1`: compor engine, sessão, URL, pool e transação por requisição.

## Síntese

A primeira fatia Code First deve persistir somente `Usuario`, com e-mail único,
SQLAlchemy assíncrono, Psycopg e migration Alembic. Ela atende a porta existente
sem alterar o núcleo e deixa configuração e integração real para etapas próprias.
