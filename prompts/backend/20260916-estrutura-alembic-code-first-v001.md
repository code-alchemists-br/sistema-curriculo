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
    - path: prompts/backend/20260916-persistencia-usuario-code-first-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 1188723"
      availability: available
    - path: docs/fundamentos-backend.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 1188723"
      availability: available
    - path: nix/backend.nix
      relationship: supporting
      representation: source-code
      function: configuration
      format: nix
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/ambientes]
  confidence: high
  rationale: "Alembic materializa a persistência Code First do backend; o ambiente Nix é somente apoio."
classification:
  sphere: engineering
  concerns: [architecture, data, delivery]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — estrutura Alembic Code First

## Solicitação original

`$decision-analysis-v4 Faça uma análise para definir estrutura Alembic no projeto, diretório de versões, decisão para a configuração de metadata e descoberta de migrations.`

## Informações complementares

- Ainda não há `alembic.ini`, `env.py` ou diretório de versões.
- A persistência de `Usuario` requer migration Code First, SQLAlchemy assíncrono e Psycopg.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Linhagem | Nenhum identificado | v001 inicial | Estrutura Alembic ainda não foi decidida | Nenhum histórico a preservar |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20260916-persistencia-usuario-code-first-v001.md` | Principal | Prosa | Documentação | Markdown | Completo | Working tree baseado em `1188723` |
| `docs/fundamentos-backend.md` | Apoio | Prosa | Documentação | Markdown | Completo | Working tree baseado em `1188723` |
| `nix/backend.nix` | Apoio | Código | Configuração | Nix | Completo | Commit `1188723` |

### Limites da evidência dos artefatos

Não há URL de banco, serviço PostgreSQL ou configuração de produção; esta decisão
não autoriza executá-los nem gerar migration funcional contra um banco.

## Problema enriquecido

### Resultado desejado

Definir uma estrutura Alembic versionada e descoberta determinística da metadata
SQLAlchemy, para que migrations Code First possam ser criadas e executadas fora
do startup da API.

### Atores e interesses

- Infraestrutura precisa de migrations reproduzíveis.
- Backend precisa concentrar metadata e mapeamentos fora do domínio.
- Operação precisa fornecer URL somente no momento de executar Alembic.

### Evidências e fatos observados

- Alembic é obrigatório para evolução de schema.
- Não há estrutura Alembic atual.
- A primeira metadata será a de `Usuario`; outros agregados continuam fora do corte.

### Hipóteses

- `alembic.ini` na raiz e `src/backend/infrastructure/persistence/alembic/` com
  `env.py`, `script.py.mako` e `versions/` permitem versionamento próximo à infraestrutura.
- Um módulo `metadata.py` será a única fonte de `MetaData`; `env.py` o importará
  explicitamente como `target_metadata`, sem varrer pacotes por reflexão.

### Perguntas em aberto

- A injeção de URL, pool e credenciais será decidida na composição externa; não
  deve ser fixada em arquivo versionado.

### Escopo

- Criar configuração Alembic, ambiente, template e diretório `versions/`.
- Definir `target_metadata` por import explícito do módulo de infraestrutura.
- Suportar migrations online assíncronas e offline sem iniciar a API.

### Fora do escopo

- Criar tabela, migration de `Usuario`, engine da aplicação, banco ou serviço.
- Alterar domínio, Application, API, Nix ou instalar dependências.

### Critérios de sucesso

- `alembic upgrade`, `revision` e `autogenerate` descobrem uma única metadata.
- Migrations ficam em diretório versionado e não dependem de startup FastAPI.
- URL é recebida por variável de ambiente/argumento operacional, não hardcoded.

## Restrições aplicáveis

- Code First e Alembic são fonte de verdade; não usar scripts SQL manuais.
- Metadata, ORM e Alembic ficam em Infrastructure; domínio e Application não os importam.
- Configuração não deve iniciar banco ou criar tabelas no startup.

## Classificação comentada

Decisão de engenharia de dados e delivery: define mecanismo de evolução de
schema, preservando fronteiras e reprodutibilidade.

## Decisão de roteamento

`prompts/backend` é mais específico para infraestrutura do backend; `ambientes`
foi considerada apenas pela dependência Nix.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Reprodutibilidade | Alta | Maximizar | Migrations devem acompanhar código. |
| Separação arquitetural | Alta | Satisfazer | ORM não entra no núcleo. |
| Operabilidade | Alta | Satisfazer | Alembic deve descobrir metadata sem API. |

## Alternativas consideradas

### Alternativa A — Criar schema no startup

Viola a regra de migrations e é inviável.

### Alternativa B — Alembic dedicado com metadata explícita

Centraliza metadata, usa `versions/` versionado e adapta a conexão assíncrona no
`env.py`. É recomendada.

### Alternativa C — Metadata espalhada e descoberta dinâmica

Oculta imports e torna autogenerate não determinístico; não é recomendada.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Reprodutibilidade | Alta | -2 | +2 | 0 | Alta | Alembic versionado. |
| Separação arquitetural | Alta | -2 | +2 | +1 | Alta | Metadata em Infrastructure. |
| Operabilidade | Alta | -1 | +2 | 0 | Média | Import explícito. |

## Histórico e decisão atual

### Decisão da versão anterior

Nenhum identificado.

### Decisão recomendada nesta versão

Adotar a Alternativa B. Implementar `alembic.ini` na raiz, ambiente Alembic em
`src/backend/infrastructure/persistence/alembic/` e migrations em `versions/`.
Criar `metadata.py` como ponto único de descoberta e fazê-lo importar todos os
mapeamentos aprovados antes de expor `target_metadata`. `env.py` deve adaptar o
engine assíncrono para a execução Alembic e ler URL apenas de configuração
operacional. A primeira migration será criada pela análise de persistência de
`Usuario`, não por esta estrutura.

### Impacto da revisão

Análise inicial; nenhum impacto de revisão.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Reprodutibilidade | maximized | Histórico de schema versionado. | Alembic. |
| Separação arquitetural | prioritized | Descoberta fica na infraestrutura. | Metadata explícita. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Operabilidade | Comandos não iniciam a API | `env.py` usa metadata e configuração próprias. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Reprodutibilidade | Schema diverge entre ambientes. | Alta | Equipe e operação. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Reprodutibilidade | Mais arquivos de configuração. | Simplicidade local | Aceitável. |

## Riscos e efeitos de segunda ordem

- Mapeamento não importado por `metadata.py` não será detectado.
- Autogenerate produz proposta que deve ser revisada, não schema definitivo.
- Migration assíncrona exige validação posterior contra PostgreSQL.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Metadata é descoberta | `target_metadata` contém tabelas aprovadas | Avaliação unitária/estática | Tabela ausente. |
| Estrutura é executável | Alembic carrega configuração | Comando no `.#backend` | Import ou configuração falha. |
| Migration real funciona | PostgreSQL controlado | Integração em `.#tests` | Falha de conexão ou upgrade. |

## Handoffs e atividades posteriores

- `$backend-adapters-drivers-v2`: criar estrutura Alembic, metadata, mapeamento e migration de `Usuario`.
- `$integration-system-testing-v1`: validar upgrade/downgrade contra PostgreSQL.
- `$cross-cutting-implementation-v1`: definir URL, engine, pool e ciclo de sessão da aplicação.

## Síntese

Alembic deve ter ambiente próprio na infraestrutura, `versions/` versionado e
metadata única importada explicitamente. Essa estrutura permite migrations Code
First assíncronas sem acoplar domínio ou startup da API ao schema.

## Configuração operacional decidida posteriormente

O `alembic.ini` deve declarar `prepend_sys_path = src`, para que comandos
executados na raiz do repositório possam importar o pacote `backend` de forma
determinística. O `env.py` deve obter a URL exclusivamente da variável de
ambiente `DATABASE_URL` e falhar com mensagem clara quando ela não estiver
definida. A URL não deve ser versionada, inferida da aplicação nem gravada em
arquivos de configuração do projeto.
