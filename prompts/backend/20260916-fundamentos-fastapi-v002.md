---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: proposed
created_at: 2026-09-16
lineage:
  mode: revision
  root: prompts/backend/20260913-fundamentos-fastapi-v001.md
  supersedes: prompts/backend/20260913-fundamentos-fastapi-v001.md
  change_type: enrichment
  secondary_change_types: [scope-change]
  decision_impact: strengthened
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20260913-fundamentos-fastapi-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723bf24c178599dd126ac69e7b85ee0ec5ab"
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
    - path: docs/fundamentos-backend.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: nix/backend.nix
      relationship: supporting
      representation: source-code
      function: configuration
      format: nix
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: src/backend/main.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: src/backend/tests/test_fastapi_foundation.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: prompts/README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/ambientes]
  confidence: high
  rationale: "A linhagem e o objeto principal são a fundação da interface HTTP; a análise de ambiente é uma dependência de decisão."
classification:
  sphere: engineering
  concerns: [architecture, implementation, performance]
  decision_kind: change
  scope: component
  lifecycle: evolution
  urgency: normal
  uncertainty: low
  reversibility: easy
  risk: medium
---

# Análise de decisão — fundamentos assíncronos da interface FastAPI

## Solicitação original

`$decision-analysis-v4 Agora com base no documento 'docs\fundamentos-backend.md', faça uma análise para implementação de um base mínina FastApi. Não quero domain, use case, nem rota. Quero apenas o fundamento inicial FastApi onde depois serão adicionados de forma composável os outros componentes.`

## Informações complementares

- Da solicitação desta revisão, literalmente: `Vamos fazer uma revisão do 'prompts\backend\20260913-fundamentos-fastapi-v001.md' para referenciar o 'prompts\ambientes\20260916-fundamentos-backend-nix-v002.md' e o uso de libs e APIs assíncrona.`
- A análise de ambiente v002 estabelece API e persistência assíncronas para I/O concorrente, mantém `psycopg` como driver único e confirma sua interface `AsyncConnection` no shell Nix.
- `docs/fundamentos-backend.md` foi atualizado no working tree para prescrever handlers de I/O assíncronos, `AsyncEngine`, `AsyncSession` e Psycopg assíncrono.
- A fundação v001 já está implementada: `create_app()` constrói uma `FastAPI` vazia e `main.py` expõe a instância ASGI, sem I/O, rotas ou recursos externos.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Referência de ambiente | Disponibilidade genérica de FastAPI e Uvicorn | Referência explícita à análise Nix v002 | A decisão de ambiente define a pilha assíncrona | Implementações futuras rastrearão ambas as análises. |
| Modelo de I/O | Não especificado | Assíncrono nas fronteiras de I/O | API terá I/O concorrente e pouca carga CPU | Handlers, dependências e adapters futuros usarão `async`/`await`. |
| Fábrica | Fábrica síncrona sem efeitos externos | Mantida síncrona | Construir `FastAPI()` não faz I/O | Não converter `create_app` em coroutine. |
| APIs futuras | Persistência e Psycopg fora do escopo | `AsyncEngine`, `AsyncSession` e Psycopg assíncrono referenciados | Alinhamento técnico | A fundação permanece preparada para composição posterior. |
| Estado do backend | Pressupunha ausência de código | Fábrica, entrada ASGI e teste existem | `dev` foi integrada | Não reimplementar nem ampliar a fundação nesta revisão. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20260913-fundamentos-fastapi-v001.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Commit `1188723` |
| `prompts/ambientes/20260916-fundamentos-backend-nix-v002.md` | Apoio | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `1188723` |
| `docs/fundamentos-backend.md` | Apoio | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `1188723` |
| `nix/backend.nix` | Apoio | Código-fonte | Configuração | Nix | Arquivo completo | Commit `1188723` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `1188723` |
| `src/backend/main.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `1188723` |
| `src/backend/tests/test_fastapi_foundation.py` | Apoio | Código-fonte | Teste | Python | Arquivo completo | Commit `1188723` |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Commit `1188723` |
| `prompts/README.md` | Contexto | Prosa | Documentação | Markdown | Arquivo completo | Commit `1188723` |
| `AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Commit `1188723` |

### Limites da evidência dos artefatos

Esta análise não abriu conexão PostgreSQL, não criou `AsyncEngine` ou
`AsyncSession`, nem mediu concorrência. A confirmação da capacidade do Psycopg
vem da análise de ambiente v002. O documento de fundamentos e a análise de
ambiente v002 ainda pertencem ao working tree.

## Problema enriquecido

### Resultado desejado

Manter uma fundação FastAPI mínima, importável e sem I/O, explicitamente
compatível com API assíncrona. Ela deve permitir composição futura de
FastAPI/ASGI, SQLAlchemy assíncrono e Psycopg assíncrono, sem antecipar banco,
rota, domínio, caso de uso ou lifecycle.

### Atores e interesses

- Desenvolvedores precisam distinguir a construção pura da aplicação das
  futuras operações concorrentes de I/O.
- A arquitetura deve manter FastAPI na borda e domínio independente de
  FastAPI, SQLAlchemy, Psycopg e `asyncio`.
- Ambientes devem fornecer somente as bibliotecas declaradas e verificadas pelo
  Nix.
- Testes precisam preservar a fábrica isolada e adicionar assincronia somente
  com comportamento de I/O observável.

### Evidências e fatos observados

- A análise v002 recomenda FastAPI/Uvicorn em ASGI, SQLAlchemy `AsyncEngine` e
  `AsyncSession`, e Psycopg assíncrono, sem adicionar `asyncpg`.
- `nix/backend.nix` já declara `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`,
  `psycopg` e `pydantic-settings` no mesmo interpretador.
- A fábrica atual retorna somente `FastAPI()` e a entrada ASGI somente expõe a
  instância; nenhuma executa I/O que exija `await`.
- Os fundamentos atuais atribuem `async`/`await` às fronteiras de I/O e mantêm
  Code First com migrations Alembic.
- As regras locais exigem dependências apontando para dentro e composição na
  camada externa.

### Hipóteses

- Routers futuros usarão `async def` quando realizarem I/O ou chamarem portas
  aguardáveis; handlers locais não precisam ser artificialmente assíncronos.
- Dependências de infraestrutura serão compostas na borda quando existir
  contrato aprovado.
- Startup e shutdown permanecerão ausentes até existir recurso externo a gerir.

### Perguntas em aberto

- Não há contrato HTTP, porta assíncrona, adapter de persistência, URL de banco,
  pool, timeout ou requisito de lifecycle definido.
- A necessidade de uma porta ou caso de uso assíncrono depende de cada futuro
  comportamento de negócio.

### Escopo

- Revisar a decisão da fundação FastAPI e registrar a dependência explícita da
  análise de ambiente v002.
- Definir a composição futura das APIs assíncronas nas fronteiras de I/O.
- Preservar a fábrica e entrada ASGI atuais, síncronas, importáveis e sem efeitos
  externos.

### Fora do escopo

- Alterar código, testes, Nix, fundamentos ou análise de ambiente nesta
  atividade.
- Tornar `create_app` assíncrona, adicionar `lifespan`, routers, endpoints,
  middleware, CORS, DTOs, autenticação ou observabilidade.
- Criar engine, sessão, repositório, migration, conexão ou teste de integração.
- Adicionar `asyncpg`, dependências extras ou instalação imperativa.

### Critérios de sucesso

- A revisão referencia explicitamente
  `prompts/ambientes/20260916-fundamentos-backend-nix-v002.md`.
- A recomendação separa fábrica síncrona e pura de operações futuras de I/O
  assíncronas.
- FastAPI/ASGI, `AsyncEngine`, `AsyncSession` e Psycopg assíncrono são
  tecnologias de composição futura, sem alegar que já existem no código.
- A decisão preserva Clean Architecture e a ausência de contratos HTTP.

## Restrições aplicáveis

- FastAPI fica na Interface/API; domínio e Application não dependem de FastAPI,
  SQLAlchemy, Psycopg ou infraestrutura concreta.
- Composição e injeção de dependências ocorrem na camada externa.
- Dependências são providas pelo Nix; `pip`, virtualenv e instalação global são
  proibidos.
- Persistência futura é Code First e requer migrations Alembic; startup não cria
  nem evolui schema.
- Esta skill autoriza somente escrever esta análise Markdown.

## Classificação comentada

É uma mudança de engenharia no componente de interface. Preserva a estrutura
da v001, mas estabelece que `async` ocorre onde há espera por I/O, enquanto a
fábrica permanece simples e síncrona. Arquitetura, implementação e performance
diferenciam as alternativas: uma coroutine sem I/O dificulta composição, e uma
fronteira bloqueante elimina o benefício da concorrência requerida.

## Decisão de roteamento

Foram inventariadas `ambientes`, `backend`, `frontend`, `requisitos`,
`revisao` e `templates`. A revisão permanece em `prompts/backend`, pasta da
linhagem e mais específica para a fundação HTTP. `prompts/ambientes` foi
considerada porque fornece a decisão de dependências, mas não é o objeto
principal. Não há `AGENTS.md` adicional sob `prompts` ou `prompts/backend`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Simplicidade | Alta | Priorizar | A fundação não deve ganhar coroutine ou lifecycle sem I/O. |
| Modificabilidade | Alta | Maximizar | Adapters assíncronos devem compor sem reestruturar a entrada. |
| Separação arquitetural | Alta | Satisfazer | ORM e driver permanecem fora do domínio e Application. |
| Performance | Média | Satisfazer | I/O futuro não pode bloquear handlers ou o loop de eventos. |
| Operabilidade | Média | Satisfazer | APIs futuras existem no shell Nix oficial. |

## Alternativas consideradas

### Alternativa A — Manter a análise sem decisão explícita sobre I/O

Preserva a v001. É incompatível com os fundamentos e a análise de ambiente
posteriores, pois permite introduzir APIs síncronas ou assíncronas sem critério.

### Alternativa B — Fábrica síncrona e assincronia nas fronteiras de I/O

Mantém `create_app()` e a entrada ASGI sem efeitos externos. Determina que
handlers e dependências futuras de I/O usem FastAPI/ASGI, `AsyncEngine`,
`AsyncSession` e Psycopg assíncrono conforme a análise v002. É recomendada.

### Alternativa C — Fábrica `async def` com recursos assíncronos agora

Adiciona coroutine, `lifespan`, sessão ou rota apenas para demonstrar
assincronia. Não há I/O atual que a justifique e viola o escopo mínimo.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Simplicidade | Alta | +1 | +2 | -2 | Alta | A fábrica não realiza I/O. |
| Modificabilidade | Alta | 0 | +2 | 0 | Alta | B separa construção atual e composição futura. |
| Separação arquitetural | Alta | 0 | +2 | -1 | Alta | Regras locais e composição externa. |
| Performance | Média | -1 | +2 | 0 | Média | Perfil de I/O concorrente, sem benchmark. |
| Operabilidade | Média | 0 | +2 | +1 | Alta | Análise de ambiente v002. |

## Histórico e decisão atual

### Decisão da versão anterior

Criar uma fábrica `create_app` sem efeitos externos, entrada ASGI com
`app = create_app()` e teste unitário. Persistência, Psycopg e rotas ficaram
fora do escopo, sem decisão sobre sincronia ou assincronia.

### Decisão recomendada nesta versão

Adotar a Alternativa B. A fundação existente permanece síncrona e pura porque
criar `FastAPI()` não requer I/O. Ela compõe uma API assíncrona: quando houver
contratos e adapters aprovados, handlers e dependências que realizem I/O devem
usar `async`/`await`, SQLAlchemy `AsyncEngine`/`AsyncSession` e a interface
assíncrona do Psycopg.

`prompts/ambientes/20260916-fundamentos-backend-nix-v002.md#v002` é dependência
explícita. Arquivos futuros alterados para essa composição devem registrar a
proveniência da v001 e desta v002; não se alteram comentários existentes sem
mudança comportamental.

### Impacto da revisão

A decisão estrutural é fortalecida: fábrica e entrada ASGI continuam corretas.
O novo impacto é orientar a composição futura como assíncrona e vinculada ao
ambiente v002. Não há autorização para alterar a fundação apenas para inserir
`async`.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Modificabilidade | maximized | Adapters assíncronos compõem na borda sem refatorar a entrada. | Fábrica isolada e decisão v002. |
| Simplicidade | prioritized | Evita coroutine e lifecycle sem operação aguardável. | `create_app()` só instancia FastAPI. |
| Performance | prioritized | I/O futuro não bloqueia o fluxo ASGI. | Requisito de I/O concorrente. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Separação arquitetural | Persistência fora do domínio e Application | APIs de SQLAlchemy/Psycopg ficam em adapters e composição externa. |
| Operabilidade | Bibliotecas no ambiente oficial | `fastapi`, `uvicorn`, `sqlalchemy` e `psycopg` estão no shell Nix. |
| Testabilidade | Fundação sem recursos externos | Fábrica e entrada continuam sem I/O. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Performance | I/O síncrono em handlers bloqueia a concorrência esperada. | Alta | Usuários e backend. |
| Simplicidade | Coroutines e recursos sem necessidade complicam importação e testes. | Média | Desenvolvimento e testes. |
| Separação arquitetural | ORM ou driver vaza para domínio ou Application. | Alta | Manutenibilidade. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Performance | I/O futuro propaga `async`/`await` por handlers, portas e adapters. | Simplicidade local | Aceitável pelo requisito. |
| Simplicidade | Não demonstrar assincronia com endpoint ou lifecycle prematuro. | Time-to-value | Aceitável até haver contrato. |
| Operabilidade | Não adotar `asyncpg` especulativamente. | Optionality | Aceitável até evidência objetiva. |

## Riscos e efeitos de segunda ordem

- Uma fábrica `async` sem I/O cria problema de ciclo de eventos, sem ganho.
- Handler `async` que chama biblioteca bloqueante ainda bloqueia o loop.
- Sessão assíncrona compartilhada entre requisições pode violar isolamento
  transacional; seu ciclo será definido com o adapter.
- `lifespan` antecipado cria política de startup e shutdown não aprovada.
- Esta referência não substitui testes de integração PostgreSQL posteriores.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Fábrica serve ASGI | Import e teste unitário sem I/O | Executar no `nix develop .#backend` | Exige coroutine ou recurso externo. |
| APIs assíncronas existem | Imports e `AsyncConnection` | Verificação no shell `.#backend` | Módulo ou interface indisponível. |
| Persistência funciona | Engine, sessão e transação PostgreSQL | Teste de integração em `.#tests` | Falha de dialeto, rollback ou concorrência. |
| Fronteiras são preservadas | Imports e testes de domínio | Teste unitário e revisão | FastAPI, SQLAlchemy ou Psycopg no domínio. |
| Concorrência é necessária | Cenários de I/O e limites de conexão | Teste de carga aprovado | Carga não é I/O ou banco satura. |

## Handoffs e atividades posteriores

- `$backend-adapters-drivers-v2`: compor routers, dependências assíncronas,
  `AsyncEngine`, `AsyncSession`, Psycopg e ciclo de vida externo quando houver
  requisitos aprovados.
- `$backend-domain-orchestration-v2`: decidir por comportamento quais portas e
  casos de uso precisam ser aguardáveis, sem levar dependência técnica ao domínio.
- `$integration-system-testing-v1`: definir testes PostgreSQL para sessões,
  transações, migrations Alembic, timeouts e concorrência.
- `$cross-cutting-implementation-v1`: decidir observabilidade, cancelamento e
  resiliência antes de introduzi-los na API.

## Síntese

A fundação v001 permanece correta: criar `FastAPI()` é síncrono e não faz I/O.
Esta v002 esclarece que ela compõe uma API assíncrona. Com contratos e adapters
aprovados, fronteiras de I/O usarão FastAPI/ASGI, SQLAlchemy `AsyncEngine` e
`AsyncSession`, e Psycopg assíncrono, conforme
`prompts/ambientes/20260916-fundamentos-backend-nix-v002.md`. Não há motivo
para converter a fábrica, inserir recursos ou duplicar drivers agora.
