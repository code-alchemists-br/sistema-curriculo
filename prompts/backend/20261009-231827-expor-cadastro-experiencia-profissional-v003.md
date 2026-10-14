---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v003"
status: pending
created_at: "2026-10-09T23:18:27-03:00"
lineage:
  mode: revision
  root: prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md
  supersedes: prompts/backend/20261009-231117-expor-cadastro-experiencia-profissional-v002.md
  change_type: reassessment
  secondary_change_types: [enrichment, correction]
  decision_impact: strengthened
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: prompts/backend/20261009-231117-expor-cadastro-experiencia-profissional-v002.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: "working-tree based on 388fa9e; untracked"
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/application/acesso_estudante.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "AcessarEstudante.executar"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/api/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "criar_router e nota sobre identidade de rota"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/api/projeto_academico.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/api/factory.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/application/cadastro_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/domain/itens_perfil.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ExperienciaProfissional e __post_init__"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/domain/value_objects.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: selected-section
      locator: "ExperienciaProfissionalId, UsuarioId e Periodo"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/tests/test_api_projeto_academico.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/tests/test_application_cadastro_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/tests/test_domain_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: test
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF01, RF02, RF03 e RF13"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: docs/requisitos-seguranca.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "visão geral e planejamento de autenticação"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: docs/mapeamento_jornadas.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "seção 6.5 / UC04"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: docs/modelagem_der.md
      relationship: supporting
      representation: diagram-model
      function: schema-contract
      format: markdown/mermaid
      analysis_scope: selected-section
      locator: "EXPERIENCIA_PROFISSIONAL"
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261005_0002_criar_curriculos.py
      relationship: supporting
      representation: source-code
      function: production
      format: Python
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: commit
      revision: "388fa9e"
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/frontend]
  confidence: high
  rationale: "A linhagem trata da exposição de um caso de uso por API do backend; autenticação e requisitos são evidências de apoio."
classification:
  sphere: engineering
  concerns: [integration, security, implementation]
  decision_kind: design
  scope: component
  lifecycle: delivery
  urgency: normal
  uncertainty: high
  reversibility: moderate
  risk: high
---

# Análise de decisão — expor cadastro de experiência profissional no backend

## Solicitação original

Versão v001: “$decision-analysis-v4 Implementar cadastro de experiências profissionais com relação às camadas de casos de uso e domain. Use doubles de teste apropriados para testes unitários.”

## Informações complementares

**v002:** “$decision-analysis-v4 Fa;a uma analise para o card Expor cadastro de experiência profissional no backend. Inclua os testes unitarios adequados”

**v003:** “$decision-analysis-v4 Revise prompts/backend/20261009-231117-expor-cadastro-experiencia-profissional-v002.md”

Interpretação da v002: ampliar a análise do núcleo Domain/Application para a exposição do cadastro por API e especificar testes unitários adequados. Interpretação desta revisão: reavaliar a decisão, a evidência e a qualidade do plano de testes sem alterar o escopo por inferência.

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Evidência de autenticação | Mecanismo de identidade confiável não estava confirmado | Login existente verifica credenciais, mas não cria sessão/token nem política de autorização | Leitura de `api/cadastro_acesso.py` e `application/acesso_estudante.py` | Confirma que a identidade autenticada não está implementada no backend examinado |
| Identidade em APIs existentes | Havia padrão de `usuario_id` no caminho e alerta de lacuna | Rota de edição de currículo documenta explicitamente que o ID do path não prova identidade | Reexame da nota de `api/versao_curriculo.py` | Reforça a restrição; não é seguro copiar a convenção como autenticação |
| Persistência de experiência | Não havia adapter/migration encontrados | Busca atual confirma que as migrations e adapters presentes cobrem usuário/currículo, sem experiência | Reavaliação da árvore de persistência no mesmo commit | Persistência continua dependência não atendida localmente |
| Testes unitários da API | Plano dizia testar status de sucesso/erro junto do handler | Separação explícita entre teste unitário direto do handler e verificação HTTP via ASGI | Chamada direta não executa serialização, parsing de rota ou resposta HTTP completa | Evita declarar cobertura de transporte que o unitário não oferece |
| Decisão | Pendente por falta de confirmação de escopo e identidade | Continua pendente; a necessidade de autenticação fica mais bem evidenciada | Não foi fornecido aceite do card nem mecanismo de sessão | `decision_impact: strengthened`; nenhum caminho de entrega fica aprovado |
| Linhagem e pasta | v002 em `prompts/backend` | v003 em `prompts/backend` | Revisão solicitada para o mesmo card | Mantidas |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md` | Principal | Prosa | Documentação | Markdown | Análise inicial completa | Commit `388fa9e` |
| `prompts/backend/20261009-231117-expor-cadastro-experiencia-profissional-v002.md` | Principal | Prosa | Documentação | Markdown | Análise anterior completa, incluindo classificação, decisão e testes | Working tree, arquivo não rastreado baseado em `388fa9e` |
| `src/backend/api/cadastro_acesso.py` | Apoio | Código-fonte | Produção | Python | Arquivo completo; endpoint de login e resposta | Commit `388fa9e` |
| `src/backend/application/acesso_estudante.py` | Apoio | Código-fonte | Produção | Python | `AcessarEstudante.executar` | Commit `388fa9e` |
| `src/backend/api/versao_curriculo.py` | Apoio | Código-fonte | Produção | Python | Nota e construção de identidade pelo ID no caminho | Commit `388fa9e` |
| `src/backend/api/projeto_academico.py` | Apoio | Código-fonte | Produção | Python | Router, DTOs, tratamento de erro e executor injetado | Commit `388fa9e` |
| `src/backend/api/factory.py` | Apoio | Código-fonte | Produção | Python | Registro de rotas e injeção de executores | Commit `388fa9e` |
| `src/backend/application/cadastro_experiencia_profissional.py` | Apoio | Código-fonte | Produção | Python | Entrada e execução do caso de uso | Commit `388fa9e` |
| `src/backend/domain/itens_perfil.py` | Apoio | Código-fonte | Produção | Python | Entidade e validação de experiência | Commit `388fa9e` |
| `src/backend/domain/value_objects.py` | Apoio | Código-fonte | Produção | Python | IDs tipados e `Periodo` | Commit `388fa9e` |
| `src/backend/tests/test_api_projeto_academico.py` | Apoio | Código-fonte | Teste | Python | Testes diretos do handler com doubles | Commit `388fa9e` |
| `src/backend/tests/test_application_cadastro_experiencia_profissional.py` | Apoio | Código-fonte | Teste | Python | Sucesso e falha antes de salvar | Commit `388fa9e` |
| `src/backend/tests/test_domain_experiencia_profissional.py` | Apoio | Código-fonte | Teste | Python | Textos obrigatórios e período cronológico | Commit `388fa9e` |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF01, RF02, RF03 e RF13 | Commit `388fa9e` |
| `docs/requisitos-seguranca.md` | Apoio | Prosa | Documentação | Markdown | Visão geral e planejamento de autenticação | Commit `388fa9e` |
| `docs/mapeamento_jornadas.md` | Apoio | Prosa | Documentação | Markdown | Seção 6.5 / UC04 | Commit `388fa9e` |
| `docs/modelagem_der.md` | Apoio | Diagrama/modelo | Contrato de schema | Markdown/Mermaid | `EXPERIENCIA_PROFISSIONAL` | Commit `388fa9e` |
| `src/backend/infrastructure/persistence/sqlalchemy/curriculo.py` | Apoio | Código-fonte | Produção | Python | Modelo ORM que serve de referência | Commit `388fa9e` |
| `src/backend/infrastructure/persistence/alembic/versions/20261005_0002_criar_curriculos.py` | Apoio | Código-fonte | Produção | Python | Migration de referência | Commit `388fa9e` |
| `AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Regras gerais, Nix e testes | Commit `388fa9e` |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução | Markdown | Arquitetura e testes de backend | Commit `388fa9e` |

### Limites da evidência dos artefatos

O código fonte rastreado permanece no commit `388fa9e`; na revisão, o working tree tinha apenas as análises v002 não rastreada como mudança. A árvore de APIs e migrations foi pesquisada para localizar implementação de autenticação e persistência. O login implementado confirma credenciais, mas declara não criar sessão ou token; não foi encontrada uma dependência que derive o estudante autenticado. A ausência de adapter de experiência decorre da busca na árvore atual, não de uma auditoria de serviços externos. Os critérios de aceite do card e decisões de produto não foram fornecidos.

## Problema enriquecido

### Resultado desejado

Expor por API o cadastro de experiências profissionais, reutilizando o caso de uso existente, com contrato HTTP claro, identidade autenticada do estudante, persistência conforme o aceite e testes unitários da fronteira.

### Atores e interesses

- Estudante: cadastrar dados profissionais vinculados à própria conta.
- API: validar transporte, obter a identidade autenticada e mapear resultado/erros sem expor a entidade.
- Application: executar o caso de uso e persistir pela porta existente.
- Infraestrutura: fornecer adapter e schema relacional caso o aceite demande persistência operacional.
- Equipe: definir uma entrega que não simule segurança nem declare persistência que a composição não fornece.

### Evidências e fatos observados

- UC04 descreve experiências com organização, cargo, período e descrição.
- RF01 exige cadastro; RF02 menciona consulta, edição e exclusão; RF03 prevê dados centralizados; RF13 exige autenticação para informações pessoais e currículos.
- A entidade, value objects, caso de uso, porta e testes unitários de Domain/Application já existem no commit examinado.
- A API de projeto oferece convenção de DTO, router, executor injetado e teste direto do handler com doubles.
- `create_app` registra executores opcionais e não constrói adapter de experiência.
- A rota `/acessos` confirma credenciais e retorna 204, sem sessão/token. O caso `AcessarEstudante` também afirma não criar sessão, token ou política de autorização.
- Outras rotas usam `usuario_id` no path; a API de edição de currículo documenta que isso não deriva de uma sessão autenticada.
- A árvore de persistência examinada contém modelos/migrations para usuário e currículo; não há modelo, adapter ou migration de experiência.

### Hipóteses

- O card trata somente de criação; listagem, edição e remoção serão tratadas separadamente, apesar de RF02.
- Os campos são `empresa`, `cargo`, `descricao`, `data_inicio` e `data_fim` opcional, conforme modelo existente.
- Não se deve introduzir mecanismo de sessão/token ou limites de texto sem requisitos/decisão de arquitetura.
- O teste unitário do handler é direto, como o teste de projeto; ele não substitui teste que passa pelo protocolo ASGI.

### Perguntas em aberto

- O aceite inclui criar mecanismo autenticado que derive `UsuarioId`, ou esse mecanismo será entregue por outro card? O código atual não fornece essa dependência.
- O card inclui persistência relacional funcional (modelo Code First, migration, adapter e composição) ou dependerá de infraestrutura existente? O backend examinado não tem adapter de experiência.
- Há limites de tamanho aprovados para os três textos?
- O aceite exige resposta HTTP realmente exercitada por cliente ASGI ou apenas testes unitários de DTO/handler?

### Escopo

Proposta condicional:

- Criar DTOs de requisição/resposta, router POST e registro na fábrica, invocando `CadastrarExperienciaProfissional`.
- Converter os campos de data para `Periodo`, preservar erros de domínio e devolver apenas campos públicos.
- Derivar o `UsuarioId` da dependência autenticada; não confiar no path ou body como prova de identidade.
- Especificar testes unitários de DTO e handler. Se o aceite exigir fluxo operacional, incluir também mecanismo autenticado, persistência Code First/Alembic, adapter e composição.
- Manter os testes Domain/Application existentes, sem duplicar neles a responsabilidade de transporte.

### Fora do escopo

- Consulta, listagem, edição e remoção sem aceite explícito.
- Escolha não aprovada de mecanismo de sessão/token ou de limites para textos.
- Acesso direto a ORM ou banco pelo handler.
- Considerar uma chamada direta ao handler como prova de comportamento HTTP fim a fim.
- Usar `usuario_id` arbitrário em URL ou JSON como identidade autenticada.

### Critérios de sucesso

- A rota registrada invoca o caso de uso existente e converte a resposta para DTO público.
- A identidade de proprietário vem de uma fronteira autenticada verificável, conforme RF13.
- As datas são tipadas na API e cronologia validada por `Periodo`.
- Os testes unitários cobrem DTO/validação, sucesso e campos devolvidos, identidade passada ao caso de uso, erro de domínio convertido em 422 e nenhuma chamada à porta de repositório após falha; executor ausente é tratado conforme contrato definido.
- O teste direto do handler é descrito como unitário. Caso se precise verificar serialização, validação automática do FastAPI, roteamento e códigos HTTP efetivamente emitidos, adicionar teste HTTP/ASGI separado no ambiente `tests`.
- Se o escopo incluir persistência operacional, a experiência é gravada por adapter Code First e composição não deixa o executor ausente na aplicação alvo.

## Restrições aplicáveis

- RF13 exige autenticação para acessar informações pessoais; credenciais verificadas sem sessão/token não bastam para autenticar requisições subsequentes.
- O backend deve respeitar Clean Architecture e DDD: API valida transporte, domínio guarda invariantes, Application usa portas e adapters ficam na infraestrutura.
- Entidade de domínio não é resposta HTTP.
- Persistência relacional segue Code First e migrations Alembic.
- Toda função, classe e DTO criado ou alterado precisa documentar o que faz, como faz e sua finalidade.
- Testes unitários backend rodam em `nix develop .#backend`; teste de integração/HTTP de nível superior usa `nix develop .#tests`.
- Esta revisão produz somente análise; não implementa nem executa testes.

## Classificação comentada

`engineering` permanece a esfera dominante, com `integration`, `security` e `implementation` como preocupações. O objeto é o contrato de uma nova fronteira de backend, não apenas texto de requisitos. A incerteza segue alta porque o aceite e a estratégia de autenticação não existem no material examinado. O risco permanece alto: a rota tratará dados profissionais pessoais e o sistema ainda não associa credenciais verificadas a uma sessão autorizada.

## Decisão de roteamento

Destino: `prompts/backend`, seguindo a linhagem anterior. As subpastas imediatas continuam incluindo backend, requisitos e frontend entre as candidatas. `backend` é a mais específica para endpoint, composição e testes; segurança/requisitos são apoio. Não há `AGENTS.md` ou `AGENTS.override.md` em `prompts/backend`; valem as instruções da raiz.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---:|---|---|
| Security | Muito alta | Obrigatório satisfazer RF13 | O login não cria sessão/token e o identificador do path é controlado pelo cliente |
| Correctness | Alta | Priorizar | Propriedade e intervalo de datas devem chegar corretos ao caso de uso |
| Interoperability | Alta | Priorizar | Handler deve integrar executor existente e configuração real |
| Simplicity | Média | Satisfazer | Reutilizar Domain/Application, sem duplicar regra |
| Delivery-speed | Média | Após segurança e operação | Uma rota isolada não produz cadastro acessível de forma segura |

## Alternativas consideradas

### A — Somente API, assumindo autenticação e persistência entregues externamente

Criar DTO/router/factory e testes unitários. É a menor entrega se as duas dependências já existirem em outro trabalho. No código examinado, ambas faltam: o login não emite sessão/token e não há adapter/migration de experiência. A alternativa não pode ser aprovada com base apenas no estado atual.

### B — Completar a fatia operacional do cadastro

Adicionar API, mecanismo autenticado escolhido conforme decisão arquitetural, persistência Code First/Alembic, adapter e composição, além de unitários e verificações de integração apropriadas. Satisfaz melhor um card entendido como cadastro funcional, mas é escopo materialmente maior e ainda requer escolher política/mecanismo de autenticação.

### C — Expor rota com `usuario_id` livre no caminho

Replica rotas existentes, mas não autentica nem autoriza o solicitante. É inviável diante de RF13.

### D — Manter pendente até definir dependências e aceite

Não liberar endpoint ainda. Obter aceite sobre autenticação e persistência, ou referências aos cards que as fornecerão; então decidir entre A e B. É a escolha provisória de menor risco, mas adia entrega.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | A | B | C | D | Confiança | Base |
|---|---:|---:|---:|---:|---:|---|---|
| Security | Muito alta | +1* | +2* | -2 | +2 | Alta | RF13 e ausência confirmada de sessão; *depende de mecanismo confiável |
| Correctness | Alta | +1* | +2 | 0 | 0 | Média | Caso de uso pronto; adapter não existe |
| Interoperability | Alta | +1* | +2 | +1 | 0 | Média | Router e executor devem ser compostos |
| Simplicity | Média | +2 | -2 | +2 | +1 | Alta | B adiciona autenticação, ORM, migration e composition |
| Delivery-speed | Média | +2* | -2 | +2 | -2 | Média | A só se dependências já existirem fora do backend analisado |

`*` A é condicional a pré-requisitos externos comprovados. Não se somam os valores ordinais.

## Histórico e decisão atual

### Decisão da versão anterior

v001 recomendou implementar domínio/Application e deixar API, autenticação e persistência concreta para handoffs. v002 identificou que domínio/Application e os unitários já existem, mas manteve pendente a exposição por falta de confirmação de autenticação e armazenamento.

### Decisão recomendada nesta versão

`status: pending`. A nova evidência confirma que não há sessão/token após o login nem adapter/migration para experiência na árvore examinada. Portanto, A não é executável apenas com as dependências atuais: ela exige prova de que esses componentes serão fornecidos externamente. C continua inviável. D permanece a decisão provisória até que o aceite do card diga se inclui autenticação e persistência ou aponte atividades que entreguem ambas. Se o card exige cadastro funcional e não há pré-requisitos externos, B é a direção necessária, mas o mecanismo autenticado deve ser definido antes da implementação.

A menor investigação para destravar é obter os critérios do card e identificar, por referência concreta, quem fornece identidade autenticada e persistência operacional.

### Impacto da revisão

`strengthened`: a decisão permanece pendente, mas a justificativa deixa de ser apenas ausência de especificação e passa a ter evidência direta de que o login não estabelece sessão/token e de que o caminho atual não possui adapter de experiência. O escopo anterior de Domain/Application permanece válido.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| Security | prioritized | Impedir cadastro sob identidade apenas declarada pelo cliente | RF13; login explicitamente não cria sessão/token |
| Correctness | prioritized | Preservar proprietário e datas válidas | Caso de uso e `Periodo` existentes |
| Interoperability | prioritized | Garantir que rota e executor estejam ligados na aplicação alvo | `create_app` recebe executores opcionais |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| Simplicity | Reutilizar código existente | Não recriar invariantes nem caso de uso |
| Testability | Unitários isolados de banco e rede | Doubles para ID, autenticação e repositório; teste direto de handler |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| Security | Usuário pode gravar em perfil alheio; dados pessoais ficam expostos | Alta | Estudantes e operação |
| Correctness | Data ou proprietário divergente do pedido autenticado | Alta | Estudantes e currículos |
| Interoperability | Endpoint registrado sem executor ou sem persistência durável | Média | Clientes da API e equipe |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| Security | Definir e compor sessão/identidade autorizada | Delivery-speed | Necessário por RF13 |
| Correctness | Validar datas e testar vínculo do principal | Simplicity | Aceitável usando `Periodo` e caso existente |
| Interoperability | Adapter, migration e composição se não houver entrega externa | Delivery-speed | Aceitável somente se o card pedir persistência funcional |

## Riscos e efeitos de segunda ordem

- Login que só responde sucesso não permite distinguir chamadas autenticadas posteriores.
- Usar o UUID do path como identidade mantém a possibilidade de cadastro em perfil de terceiros.
- A rota com executor opcional pode responder 503 na aplicação sem composição concreta.
- Um adapter novo sem política de transação externa pode criar inconsistência entre sucesso HTTP e flush/commit.
- Teste direto do handler pode passar mesmo com erro de registro, parsing ou serialização do router.
- Copiar limites de campos de outro endpoint sem decisão de produto cristaliza políticas não aprovadas.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Auth será fornecida fora do card | Dependência concreta e card responsável por emitir/validar sessão | Revisar composição e aceite | Sem dono ou mecanismo, manter D ou incluir em B |
| Persistência será fornecida fora do card | Adapter, migration e composição identificados | Revisão de código/planejamento | Nenhum adapter utilizável implica B para fluxo funcional |
| Handler passa o usuário autenticado | Principal injetado e conversão para `UsuarioId` | Unitário com principal controlado | `usuario_id` do cliente substitui principal |
| Erros de domínio não salvam | Repositório spy permanece vazio após violação | Unitário direto do handler com caso real | Persistência chamada após falha |
| DTO e datas respeitam contrato | Campos, ausência/presença e `Periodo` | Unitários do DTO/handler | Período invertido ou campo requerido tratado incorretamente |
| Transporte real emite códigos e corpo esperados | Aplicação ASGI com dependências substituídas | Teste HTTP de integração separado | Código/serialização divergem do contrato |

## Handoffs e atividades posteriores

- Gestão do card: fornecer aceite e apontar cards que entregam identidade autenticada e armazenamento.
- Arquitetura/segurança: definir como `/acessos` estabelece sessão e como handlers obtêm o principal; não inventar token nesta análise.
- Backend: após decisão, implementar API e unitários; se não houver dependências externas, incluir auth/composição e adapter/migration no escopo ou criar cards dependentes explícitos.
- Produto: aprovar limites de texto e confirmar se edição/consulta/remoção pertencem a outras entregas.
- Qualidade: manter unitários no ambiente backend e usar ambiente tests apenas para prova HTTP/integrada de nível superior.

## Síntese

Esta terceira versão reavalia a análise pendente e confirma diretamente que a verificação de credenciais não cria sessão/token; o `usuario_id` nas rotas existentes não equivale a autenticação e a experiência ainda não tem adapter/migration. O card pode reutilizar domínio, Application e testes existentes, acrescentando DTO/router e unitários diretos do handler, mas ainda não pode ser delimitado como uma rota segura e operacional sem critérios de aceite e donos concretos para identidade autenticada e persistência. A decisão permanece pendente; se esses recursos não forem entregues fora do card, a fatia precisa incluí-los.
