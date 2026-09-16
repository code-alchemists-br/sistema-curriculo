---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v002"
status: proposed
created_at: 2026-09-16
lineage:
  mode: revision
  root: prompts/ambientes/20260913-fundamentos-backend-nix-v001.md
  supersedes: prompts/ambientes/20260913-fundamentos-backend-nix-v001.md
  change_type: reassessment
  secondary_change_types: [scope-change]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: prompts/ambientes/20260913-fundamentos-backend-nix-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 3a5451ee04748cf69aca2f9e73116cfe6c6767c6"
      availability: available
    - path: docs/fundamentos-backend.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 3a5451ee04748cf69aca2f9e73116cfe6c6767c6"
      availability: available
    - path: nix/backend.nix
      relationship: supporting
      representation: source-code
      function: configuration
      format: nix
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 3a5451ee04748cf69aca2f9e73116cfe6c6767c6"
      availability: available
    - path: flake.nix
      relationship: supporting
      representation: source-code
      function: configuration
      format: nix
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 3a5451ee04748cf69aca2f9e73116cfe6c6767c6"
      availability: available
    - path: prompts/README.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 3a5451ee04748cf69aca2f9e73116cfe6c6767c6"
      availability: available
    - path: docs/configuracao-ambiente.md
      relationship: context
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 3a5451ee04748cf69aca2f9e73116cfe6c6767c6"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 3a5451ee04748cf69aca2f9e73116cfe6c6767c6"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/ambientes
  considered_directories: [prompts/ambientes, prompts/backend]
  confidence: high
  rationale: "A revisão mantém como objeto principal o ambiente Nix do backend; a mudança de modelo de I/O não altera esse propósito."
classification:
  sphere: engineering
  concerns: [architecture, implementation, performance]
  decision_kind: change
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: low
  reversibility: moderate
  risk: medium
---

# Análise de decisão — ambiente Nix para fundamentos assíncronos do backend

## Solicitação original

`$decision-analysis-v4 analise o documento 'docs\fundamentos-backend.md'. Crie uma análise para ser usada com skill 'nix-environment-implementation-v1'. Essa análise deve observar as decisões técnicas do documento e adicionar as libs e/ou frameworks adequados sob o controle do nix a serem usadas com o ambiente de backend.`

## Informações complementares

- Da solicitação desta revisão, literalmente: `Precisa rever o documento 'prompts\ambientes\20260913-fundamentos-backend-nix-v001.md' para usar API assíncrona. Ela será I/O concorrente e terá pouco trabalho intensivo de CPU.`
- A verificação pontual em `nix develop .#backend` importou as seis dependências do shell atual e observou `psycopg` na versão `3.3.4` com `AsyncConnection` disponível.
- `docs/fundamentos-backend.md` ainda recomenda explicitamente endpoints e banco síncronos; essa evidência é anterior e conflitante com a nova decisão do usuário, não uma autorização para ignorá-la silenciosamente.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Modelo de I/O | API e banco síncronos como início | API e acesso a banco assíncronos | A carga será predominantemente I/O concorrente e pouco intensiva em CPU | A implementação futura deve propagar `async`/`await` pelas fronteiras de I/O. |
| Justificativa para driver assíncrono | Ausente; driver assíncrono fora do escopo | Presente e observável | Nova informação do usuário | A escolha de `psycopg` deve usar sua interface assíncrona. |
| Dependências Nix | `psycopg` era suficiente somente para a opção síncrona documentada | `psycopg` permanece suficiente para a opção assíncrona | O shell confirmou `AsyncConnection` no pacote existente | Não adicionar `asyncpg` sem requisito de interoperabilidade ou desempenho que o diferencie. |
| Documento de fundamentos | Recomendava síncrono | Ainda não foi atualizado nesta atividade | Esta skill só permite nova análise, não alterar documentação | Há um handoff obrigatório para alinhar a fonte técnica de verdade. |
| Escopo da próxima implementação Nix | Alterar `nix/backend.nix` para incluir seis pacotes | Nenhuma alteração Nix adicional é justificada pelos dados atuais | O shell já contém e validou o driver apto ao modelo assíncrono | A implementação Nix deve validar a composição atual e registrar a ausência de diff, não incluir dependências especulativas. |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/ambientes/20260913-fundamentos-backend-nix-v001.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `3a5451e` |
| `docs/fundamentos-backend.md` | Apoio | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `3a5451e` |
| `nix/backend.nix` | Apoio | Código-fonte | Configuração | Nix | Arquivo completo | Working tree baseado em `3a5451e` |
| `flake.nix` | Apoio | Código-fonte | Configuração | Nix | Arquivo completo | Working tree baseado em `3a5451e` |
| `prompts/README.md` | Contexto | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `3a5451e` |
| `docs/configuracao-ambiente.md` | Contexto | Prosa | Documentação | Markdown | Arquivo completo | Working tree baseado em `3a5451e` |
| `AGENTS.md` | Contexto | Prosa | Instrução para agentes | Markdown | Arquivo completo | Working tree baseado em `3a5451e` |

### Limites da evidência dos artefatos

A confirmação foi limitada à composição do shell e à presença da interface
`psycopg.AsyncConnection`; não criou conexão PostgreSQL, não implementou engine
ou sessão SQLAlchemy assíncronos e não mediu throughput. A afirmação sobre o
perfil de carga vem do usuário e é tratada como requisito da decisão. Os
documentos e fontes examinados pertencem ao working tree; não foi alegada
identidade com um commit limpo.

## Problema enriquecido

### Resultado desejado

Manter no dev shell `.#backend` um único interpretador Python reprodutível que
suporte uma API REST assíncrona, com concorrência de operações de I/O e pouca
carga CPU, preservando FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL, Psycopg e
Pydantic Settings sob controle do Nix.

### Atores e interesses

- Desenvolvedores de backend precisam implementar e testar I/O concorrente sem
  instalar drivers globalmente ou manter dois drivers PostgreSQL.
- A equipe de arquitetura precisa preservar DDD, Clean Architecture, Code
  First e a separação entre domínio, aplicação, infraestrutura e API.
- A equipe de ambientes precisa manter dependências declaradas, mínimas e
  compatíveis com o interpretador selecionado.

### Evidências e fatos observados

- O shell `backend` já compõe `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`,
  `psycopg` e `pydantic-settings` via `pkgs.python3.withPackages`.
- O shell atual importa essas dependências e expõe `psycopg 3.3.4` com
  `AsyncConnection`.
- FastAPI e Uvicorn já formam uma base ASGI adequada; não requerem um pacote
  adicional apenas para declarar handlers `async`.
- SQLAlchemy 2.x pode ser usado com `AsyncEngine` e `AsyncSession`; essa é uma
  adaptação futura de código de infraestrutura, não uma propriedade obtida pela
  mera presença do pacote.
- Alembic continua sendo o mecanismo de migrations versionadas. A aplicação
  não deve criar tabelas automaticamente no startup.
- O documento de fundamentos ainda registra a decisão síncrona e deve ser
  atualizado por atividade autorizada posteriormente.

### Hipóteses

- A implementação futura usará `create_async_engine` e `AsyncSession`, com
  repositórios concretos que aguardam somente operações de I/O.
- A URL PostgreSQL será configurada na forma compatível com o dialeto assíncrono
  de SQLAlchemy e Psycopg, por exemplo `postgresql+psycopg://...`, e será
  verificada contra as versões efetivas do ambiente.
- Trabalho CPU intensivo continuará fora do caminho assíncrono ou será
  encaminhado a mecanismo específico se surgir; `async` não o acelera.

### Perguntas em aberto

- A política concreta de concorrência, pool de conexões, timeouts e limites de
  conexões ainda não foi definida; ela depende de cenários de carga e do banco
  disponível.
- Não há requisito que demonstre vantagem de manter `asyncpg` além de
  `psycopg`; a necessidade deve ser reavaliada somente se compatibilidade ou
  benchmark a justificar.

### Escopo

- Revisar a decisão da linhagem para estabelecer acesso assíncrono a I/O como
  base técnica futura.
- Confirmar se a dependência PostgreSQL já declarada no Nix suporta essa
  decisão.
- Registrar requisitos para uma futura implementação de API, persistência,
  documentação de fundamentos e validação.

### Fora do escopo

- Alterar `docs/fundamentos-backend.md`, `nix/backend.nix`, `flake.nix` ou
  qualquer código da aplicação nesta atividade.
- Criar endpoints, engines, sessões, repositórios, migrations, banco local ou
  conexões externas.
- Adicionar `asyncpg`, bibliotecas de teste, linters ou serviços PostgreSQL
  sem uma decisão posterior baseada em requisito verificável.
- Alterar o domínio, DTOs ou a separação DDD/Clean Architecture.

### Critérios de sucesso

- A análise diferencia claramente o requisito assíncrono da antiga decisão
  síncrona e recomenda uma composição de dependências mínima.
- A recomendação usa evidência do shell Nix atual para não duplicar drivers.
- Uma implementação posterior pode saber que deve usar FastAPI/ASGI,
  SQLAlchemy `AsyncEngine`/`AsyncSession` e interface assíncrona do Psycopg.
- A divergência de `docs/fundamentos-backend.md` é explícita e encaminhada.

## Restrições aplicáveis

- Ferramentas de desenvolvimento do backend devem usar `nix develop .#backend`.
- Dependências devem permanecer declaradas no Nix; `pip install`, virtualenv e
  instalação global são proibidos.
- SQLModel não deve se tornar o modelo central; DTOs, entidades de domínio e
  persistência permanecem separados.
- Schema continua Code First com migrations Alembic; não são autorizados
  scripts SQL manuais como fonte de verdade nem criação de tabelas no startup.
- Esta atividade pode escrever somente esta nova análise Markdown.

## Classificação comentada

É uma decisão de engenharia que muda um componente de ambiente e a base de
implementação do backend. Arquitetura importa porque a assincronia deve ficar
nas fronteiras de I/O, implementação porque exige APIs assíncronas de
SQLAlchemy/Psycopg, e performance porque a motivação é concorrência de I/O —
não otimização de CPU. O risco é médio: uma mistura inadvertida de interfaces
síncronas e assíncronas pode bloquear requisições ou quebrar transações, embora
a decisão seja reversível com alteração de adaptadores e configuração.

## Decisão de roteamento

Foram inventariadas as subpastas `ambientes`, `backend`, `frontend`,
`requisitos`, `revisao` e `templates`. `prompts/backend` é candidata porque a
decisão orienta a API, mas `prompts/ambientes` preserva a linhagem e é mais
específica ao objeto principal: a composição do dev shell Nix. Não há
`AGENTS.md` adicional sob `prompts` ou `prompts/ambientes`.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Operabilidade | Alta | Satisfazer | O shell deve conter um driver efetivamente utilizável pelo caminho assíncrono. |
| Simplicidade | Alta | Priorizar | Um driver PostgreSQL evita configurações, URLs e diagnósticos duplicados. |
| Confiabilidade | Alta | Satisfazer | Sessões e transações devem poder usar APIs assíncronas coerentes. |
| Performance | Média | Priorizar | I/O concorrente é requisito; não se presume benefício para CPU. |
| Reprodutibilidade | Alta | Maximizar | Todo desenvolvedor deve obter a mesma composição pelo Nix. |

## Alternativas consideradas

### Alternativa A — Manter implementação síncrona

Mantém o documento de fundamentos e o uso síncrono de Psycopg. É inviável
porque contradiz o requisito explícito de I/O concorrente e pode ocupar uma
thread por operação bloqueante.

### Alternativa B — Usar SQLAlchemy assíncrono com o Psycopg já declarado

Mantém um único driver, usa FastAPI/Uvicorn como ASGI e direciona a futura
infraestrutura para `AsyncEngine`, `AsyncSession` e operações aguardáveis do
Psycopg. A interface assíncrona foi confirmada no shell Nix. É a alternativa
recomendada.

### Alternativa C — Adicionar `asyncpg` e substituir ou duplicar Psycopg

Também permite acesso assíncrono, mas amplia o ambiente com um driver que não é
necessário para satisfazer o requisito atual. Pode ser reconsiderada diante de
benchmark, requisito de biblioteca externa ou incompatibilidade demonstrada,
mas não há essa evidência agora.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| Operabilidade | Alta | -2 | +2 | +2 | Alta | `AsyncConnection` foi observado no shell oficial. |
| Simplicidade | Alta | +1 | +2 | -1 | Alta | B mantém o pacote PostgreSQL já declarado; C introduz outro driver. |
| Confiabilidade | Alta | -1 | +2 | +1 | Média | B permite uma pilha assíncrona coerente; a gestão concreta de sessão será validada na implementação. |
| Performance | Média | -2 | +2 | +2 | Média | O perfil de I/O concorrente foi declarado pelo usuário; não há benchmark comparativo. |
| Reprodutibilidade | Alta | +1 | +2 | +1 | Alta | B preserva a composição Nix existente e suficiente. |

## Histórico e decisão atual

### Decisão da versão anterior

Usar `python3.withPackages` com FastAPI, Uvicorn, SQLAlchemy, Alembic, Psycopg
e Pydantic Settings para iniciar uma API REST síncrona. Drivers assíncronos não
eram justificados e ficaram fora do escopo.

### Decisão recomendada nesta versão

Adotar API e persistência assíncronas para I/O concorrente, mantendo o
`psycopg` já declarado no ambiente Nix como único driver PostgreSQL. A futura
implementação deve usar o suporte assíncrono de Psycopg com SQLAlchemy 2.x,
por meio de `AsyncEngine` e `AsyncSession`, e endpoints FastAPI `async` que
aguardem operações de I/O.

Não é recomendada nenhuma inclusão adicional em `nix/backend.nix` a partir
desta revisão: o shell oficial já contém e confirmou o requisito específico do
driver. Antes de implementar, uma atividade autorizada deve atualizar
`docs/fundamentos-backend.md` para substituir sua orientação síncrona pela
decisão desta análise.

### Impacto da revisão

A decisão foi revisada, não apenas fortalecida: a versão anterior preferia
sincronia e excluía a necessidade de driver assíncrono; esta versão recomenda
assincronia e estabelece que a capacidade já existe em Psycopg. O escopo de
alteração Nix diminuiu para nenhum diff adicional, enquanto aumentou o escopo
de implementação futura de adaptadores e documentação.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Reprodutibilidade | maximized | Um único pacote controlado pelo Nix atende o driver. | Shell atual e regra de ambiente Nix. |
| Simplicidade | prioritized | Evita dois drivers, URLs e caminhos de diagnóstico. | Psycopg já oferece `AsyncConnection`. |
| Performance | prioritized | Permite liberar o fluxo durante espera por I/O. | Perfil de carga declarado pelo usuário. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Operabilidade | Driver assíncrono importável no shell oficial | `psycopg 3.3.4` e `AsyncConnection` foram confirmados. |
| Confiabilidade | Uma abstração coerente de engine, sessão e transação | A implementação futura adotará as interfaces assíncronas de SQLAlchemy e Psycopg. |
| Separação arquitetural | Domínio não depende de framework ou driver | A assincronia fica em API, aplicação quando necessário e adaptadores de infraestrutura. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Performance | Operações de I/O bloqueiam fluxos que poderiam progredir concorrentemente. | Alta | Usuários e equipe de backend. |
| Operabilidade | O código mistura interfaces síncronas e assíncronas ou requer driver não disponível. | Alta | Desenvolvedores de backend. |
| Simplicidade | Drivers duplicados tornam configuração e suporte mais complexos. | Média | Equipe de ambientes e backend. |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Performance | Propagação de `async`/`await`, sessões assíncronas e testes específicos. | Simplicidade local | Aceitável porque o requisito de I/O é explícito. |
| Simplicidade | Não adotar `asyncpg` sem evidência comparativa. | Optionality | Aceitável; a decisão pode ser revisada com benchmark. |
| Reprodutibilidade | Manter dependências exclusivamente no Nix. | Time-to-value | Aceitável para impedir instalações imperativas divergentes. |

## Riscos e efeitos de segunda ordem

- Chamar bibliotecas bloqueantes dentro de handlers `async` pode anular a
  concorrência e degradar a capacidade percebida.
- Misturar `Session`/`Engine` síncronos com `AsyncSession`/`AsyncEngine` cria
  erros de execução e gestão de transações difícil de revisar.
- A escolha assíncrona não acelera CPU; tarefas intensivas precisam de desenho
  específico se vierem a existir.
- Pool de conexões, timeouts e cancelamento precisam respeitar a capacidade do
  PostgreSQL; aumentar concorrência da aplicação sem esses limites pode esgotar
  conexões.
- A divergência temporária entre esta análise e o documento de fundamentos
  pode induzir implementações síncronas se o handoff documental não ocorrer.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Psycopg suporta o caminho assíncrono no ambiente | Import e interface `AsyncConnection` disponíveis | Executar import no `nix develop .#backend` | Interface ausente ou incompatível com versões fixadas. |
| SQLAlchemy opera com a URL/dialeto escolhidos | Engine e conexão de teste contra PostgreSQL controlado | Teste de integração no ambiente `.#tests` | Falha de dialeto, conexão ou transação. |
| Concorrência beneficia o caso real | Cenários de I/O, latência e limites de conexões definidos | Teste de carga ou integração aprovado | Sem ganho mensurável ou saturação do banco. |
| Domínio permanece isolado | Revisão de dependências entre camadas | Testes unitários e revisão arquitetural | Tipos FastAPI, SQLAlchemy ou Psycopg no domínio. |
| Documento de fundamentos está alinhado | Decisão síncrona removida e modelo assíncrono descrito | Revisão documental autorizada | Documento continua instruindo sincronia. |

## Handoffs e atividades posteriores

- Atividade documental autorizada: atualizar `docs/fundamentos-backend.md` para
  declarar API e persistência assíncronas, o uso de Psycopg assíncrono e a
  preservação das migrations Alembic.
- `$backend-adapters-drivers-v2`: implementar endpoints ASGI, `AsyncEngine`,
  `AsyncSession`, repositórios concretos, transações e ciclo de vida de
  recursos, sem levar dependências de infraestrutura ao domínio.
- `$integration-system-testing-v1`: definir testes de integração com PostgreSQL
  para conexões, transações, concorrência de I/O, cancelamento e migrations.
- Revisar a decisão de driver somente após benchmark ou requisito objetivo que
  diferencie `asyncpg` de Psycopg.

## Síntese

O novo requisito de I/O concorrente e pouca carga CPU invalida a preferência
inicial por acesso síncrono. O ambiente Nix já oferece a capacidade necessária:
`psycopg 3.3.4` expõe `AsyncConnection`, além de FastAPI, Uvicorn e SQLAlchemy.
A decisão revisada é implementar o caminho assíncrono com Psycopg, sem adicionar
`asyncpg` especulativamente, e primeiro alinhar o documento de fundamentos que
ainda recomenda sincronia. Esta atividade produziu somente a análise; não
alterou configuração, documentação técnica nem aplicação.
