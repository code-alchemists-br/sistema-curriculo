---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: proposed
created_at: 2026-09-16
lineage:
  mode: revision
  root: prompts/backend/20260914-cadastro-acesso-estudante-v001.md
  supersedes: prompts/backend/20260914-cadastro-acesso-estudante-v001.md
  change_type: reassessment
  secondary_change_types: [scope-change]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20260914-cadastro-acesso-estudante-v001.md
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
    - path: prompts/backend/20260916-fundamentos-fastapi-v002.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: src/backend/application/cadastro_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "1188723bf24c178599dd126ac69e7b85ee0ec5ab"
      availability: available
    - path: src/backend/application/ports.py
      relationship: supporting
      representation: source-code
      function: production
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
  rationale: "A linhagem descreve um caso de uso e suas portas; ambiente é somente a dependência técnica da decisão."
classification:
  sphere: engineering
  concerns: [architecture, implementation, performance]
  decision_kind: change
  scope: component
  lifecycle: evolution
  urgency: normal
  uncertainty: medium
  reversibility: moderate
  risk: medium
---

# Análise de decisão — cadastro de estudante com portas assíncronas

## Solicitação original

`$decision-analysis-v4 Analise os requisitos de cadastro e acesso de estudante e crie uma base de domínio e aplicação sem API, banco ou autenticação.`

## Informações complementares

- Da solicitação desta revisão, literalmente: `vamos fazer uma revisão de 'prompts\backend\20260914-cadastro-acesso-estudante-v001.md' com relação ao uso de libs e APIs assíncronas.`
- A análise de ambiente v002 determina I/O concorrente, SQLAlchemy assíncrono e Psycopg assíncrono, sem `asyncpg` adicional.
- A revisão FastAPI v002 determina que I/O futuro ocorre em handlers e dependências assíncronas, mantendo a fundação ASGI pura.
- O caso de uso e `RepositorioUsuario` atuais são síncronos; o gerador de UUID é local e não realiza I/O.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Repositório | Métodos síncronos | Métodos aguardáveis | Persistência será I/O concorrente | Portas e doubles usam `async def`. |
| Caso de uso | `executar()` síncrono | `executar()` assíncrono | Deve aguardar consulta e salvamento | Chamadores usam `await`. |
| Gerador de ID | Porta síncrona | Mantida síncrona | Geração local não é I/O | Não introduzir coroutine artificial. |
| Infraestrutura | Ainda não implementada | APIs-alvo explícitas | Decisão de ambiente | Adapter futuro usa `AsyncSession` e Psycopg assíncrono. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20260914-cadastro-acesso-estudante-v001.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Commit `1188723` |
| `prompts/ambientes/20260916-fundamentos-backend-nix-v002.md` | Apoio | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `1188723` |
| `prompts/backend/20260916-fundamentos-fastapi-v002.md` | Apoio | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `1188723` |
| `src/backend/application/cadastro_estudante.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `1188723` |
| `src/backend/application/ports.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo | Commit `1188723` |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Commit `1188723` |
| `AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Commit `1188723` |

### Limites da evidência dos artefatos

Não foi criado adapter, conexão PostgreSQL, sessão SQLAlchemy ou teste de
integração. A necessidade de I/O concorrente vem das análises v002 e o contrato
de repositório ainda não define pool, timeout, isolamento ou política de erro.

## Problema enriquecido

### Resultado desejado

Evoluir o cadastro de estudante para aguardar somente suas operações de
persistência, preservando regras de domínio, entrada tipada e geração local de
identidade independentes de framework, ORM e driver.

### Atores e interesses

- Backend precisa atender I/O concorrente sem bloquear o fluxo ASGI.
- Arquitetura precisa manter Application dependente de portas, não de SQLAlchemy
  ou Psycopg.
- Testes precisam usar doubles assíncronos determinísticos.

### Evidências e fatos observados

- O caso atual consulta `existe_por_email`, gera UUID, constrói `Usuario` e
  chama `salvar`.
- Somente consulta e salvamento representam I/O futuro; domínio e UUID são
  computação local.
- O ambiente já contém SQLAlchemy, Psycopg, FastAPI e Uvicorn; Psycopg expõe
  `AsyncConnection` conforme a análise v002.

### Hipóteses

- O adapter de repositório implementará as duas operações com `AsyncSession` e
  Psycopg assíncrono.
- O chamador HTTP aguardará o caso de uso, sem expor entidade de domínio.

### Perguntas em aberto

- A estratégia de unicidade no banco, tradução de erro de concorrência e limite
  de conexões exigem decisão de persistência e integração posterior.

### Escopo

- Revisar o contrato de I/O do caso de uso e do repositório.
- Referenciar as decisões assíncronas de ambiente e FastAPI.
- Definir requisitos de testes unitários assíncronos e handoff de adapter.

### Fora do escopo

- Alterar código, testes, schema, migrations, Nix, API HTTP ou autenticação.
- Tornar domínio, value objects ou `GeradorUsuarioId` assíncronos.
- Criar `AsyncSession`, repository concreto, banco ou adicionar `asyncpg`.

### Critérios de sucesso

- A análise especifica `async def` e `await` somente para repositório e caso de
  uso.
- SQLAlchemy e Psycopg aparecem somente como tecnologias do adapter externo.
- Domínio e geração local permanecem síncronos e independentes.

## Restrições aplicáveis

- Application não depende de Infrastructure ou API; domínio não depende de
  frameworks, banco, serialização ou serviços externos.
- Migrations seguem Code First e Alembic; startup não cria schema.
- Dependências permanecem sob Nix e esta skill pode escrever apenas esta análise.

## Classificação comentada

É uma revisão de engenharia do componente Application. A decisão muda contratos
de I/O e exige adaptação de chamadores e testes, mas preserva regras de negócio
e Clean Architecture. O risco é médio porque interfaces síncronas e assíncronas
misturadas causariam chamadas não aguardadas ou bloqueio.

## Decisão de roteamento

As subpastas existentes são `ambientes`, `backend`, `frontend`, `requisitos`,
`revisao` e `templates`. A revisão permanece em `prompts/backend` pela
linhagem e pelo propósito de caso de uso; `ambientes` é somente apoio técnico.
Não há `AGENTS.md` adicional sob o destino.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Performance | Alta | Satisfazer | I/O de repositório não bloqueia fluxo concorrente. |
| Separação arquitetural | Alta | Satisfazer | Driver e ORM ficam no adapter. |
| Simplicidade | Alta | Priorizar | Apenas I/O recebe assincronia. |
| Testabilidade | Média | Satisfazer | Doubles exercitam o contrato aguardável. |

## Alternativas consideradas

### Alternativa A — Manter o caso de uso e portas síncronos

Contradiz a decisão de persistência assíncrona e pode bloquear o caminho ASGI.

### Alternativa B — Caso de uso e repositório assíncronos; domínio e UUID síncronos

Propaga `await` somente por consulta e salvamento, preservando as fronteiras.
É a alternativa recomendada.

### Alternativa C — Tornar todas as portas e domínio assíncronos

Amplia a complexidade sem I/O em geração de UUID ou regras de negócio e é
incompatível com a simplicidade requerida.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Performance | Alta | -2 | +2 | +2 | Alta | I/O concorrente decidido. |
| Separação arquitetural | Alta | 0 | +2 | 0 | Alta | Ports isolam infraestrutura. |
| Simplicidade | Alta | +1 | +2 | -2 | Alta | UUID e domínio não fazem I/O. |
| Testabilidade | Média | +1 | +2 | -1 | Média | Doubles assíncronos controlam chamadas. |

## Histórico e decisão atual

### Decisão da versão anterior

O cadastro usava portas síncronas para verificar e salvar usuário, e um gerador
síncrono de ID, sem adapter, API ou banco.

### Decisão recomendada nesta versão

Adotar a Alternativa B. `RepositorioUsuario.existe_por_email` e `salvar` devem
ser aguardáveis; `CadastrarEstudante.executar` deve ser `async` e aguardar cada
operação do repositório. `GeradorUsuarioId.gerar`, entidades, value objects e
regras permanecem síncronos. O adapter futuro usa SQLAlchemy `AsyncSession` e
Psycopg assíncrono segundo `prompts/ambientes/20260916-fundamentos-backend-nix-v002.md`.

### Impacto da revisão

A decisão é revisada: contratos existentes e testes precisam mudar para APIs
assíncronas, mas o comportamento de cadastro, sua regra de duplicidade e as
fronteiras arquiteturais permanecem inalterados.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Simplicidade | prioritized | Apenas I/O usa `async`/`await`. | UUID e domínio são locais. |
| Performance | prioritized | Esperas de persistência liberam o fluxo concorrente. | Requisito técnico v002. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Separação arquitetural | Application não importa ORM/driver | Portas aguardáveis mantêm a abstração. |
| Testabilidade | Fluxo verificável sem banco | Doubles implementam coroutines em memória. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Performance | Cadastro bloqueia enquanto espera o armazenamento. | Alta | Usuários e backend. |
| Correctness | Chamada assíncrona sem `await` perde consulta ou salvamento. | Alta | Dados e equipe. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Performance | Assinatura, chamadores e testes passam a usar `await`. | Simplicidade local | Aceitável por I/O concorrente. |
| Simplicidade | UUID não adota coroutine. | Optionality | Aceitável sem fonte externa. |

## Riscos e efeitos de segunda ordem

- Um adapter síncrono sob porta assíncrona ainda bloqueia o loop de eventos.
- A verificação prévia não elimina a necessidade de restrição única no banco.
- Sessão compartilhada entre requisições pode comprometer transações; o adapter
  futuro deve definir ciclo de vida por unidade de trabalho.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Caso aguarda repositório | Testes unitários com doubles assíncronos | Executar no `nix develop .#backend` | Coroutine não aguardada. |
| Adapter é compatível | Engine, sessão e transação PostgreSQL | Integração no `nix develop .#tests` | Falha de dialeto ou rollback. |
| Domínio fica isolado | Revisão de imports | Testes e revisão arquitetural | ORM/driver no domínio. |
| Unicidade é segura | Conflito concorrente reproduzido | Teste integração | Cadastro duplicado passa. |

## Handoffs e atividades posteriores

- `$backend-domain-orchestration-v2`: atualizar portas, caso de uso e testes
  unitários para o contrato assíncrono, preservando domínio síncrono.
- `$backend-adapters-drivers-v2`: implementar repositório SQLAlchemy assíncrono,
  sessão Psycopg e tradução de erros de persistência.
- `$integration-system-testing-v1`: validar PostgreSQL, migrations Alembic,
  transações e disputa concorrente de e-mail.

## Síntese

O cadastro deve tornar assíncrono apenas o caminho de persistência: caso de uso
e repositório aguardam I/O; domínio e UUID local permanecem síncronos. A escolha
preserva Clean Architecture e usa a pilha já decidida — SQLAlchemy assíncrono e
Psycopg — sem implementar banco ou adicionar driver nesta atividade.
