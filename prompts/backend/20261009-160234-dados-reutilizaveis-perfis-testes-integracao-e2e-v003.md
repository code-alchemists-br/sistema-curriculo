---
artifact: decision-analysis
schema_version: "4.0"
artifact_version: "v003"
status: proposed
created_at: "2026-10-09T16:02:34-03:00"
lineage:
  mode: revision
  root: prompts/backend/20261009-153458-dados-reutilizaveis-perfis-testes-integracao-e2e-v001.md
  supersedes: prompts/backend/20261009-154428-dados-reutilizaveis-perfis-testes-integracao-e2e-v002.md
  change_type: enrichment
  secondary_change_types: [scope-change]
  decision_impact: revised
subjects:
  kind: mixed
  files:
    - path: prompts/backend/20261009-154428-dados-reutilizaveis-perfis-testes-integracao-e2e-v002.md
      relationship: primary
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/requisitos_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RF01–RF04, RF13–RF15 e detalhamentos pendentes"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/requisitos_nao_funcionais.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "RNF04–RNF05 e critérios de verificação"
      content_state: working-tree
      revision: null
      availability: available
    - path: docs/matriz_testes.md
      relationship: supporting
      representation: prose
      function: documentation
      format: markdown
      analysis_scope: selected-section
      locator: "CT-RF01, CT-RF02, CT-RF03, CT-RF08, CT-RF13, CT-RF14 e CT-RF15"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/AGENTS.md
      relationship: context
      representation: prose
      function: prompt-instruction
      format: markdown
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/itens_perfil.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "FormacaoAcademica e ExperienciaProfissional"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/domain/curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/cadastro_acesso.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "DTOs/endpoints e ausência de criação de sessão no acesso"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/api/versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: production
      format: python
      analysis_scope: selected-section
      locator: "Contratos de criação/edição e nota sobre identidade/autorização"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/usuario.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/curriculo.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/sqlalchemy/metadata.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20260916_0001_criar_usuarios.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/infrastructure/persistence/alembic/versions/20261005_0002_criar_curriculos.py
      relationship: supporting
      representation: source-code
      function: schema-contract
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_infrastructure_usuario_mapping.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_infrastructure_curriculo_mapping.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_domain_experiencia_profissional.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/test_api_criar_versao_curriculo.py
      relationship: supporting
      representation: source-code
      function: test
      format: python
      analysis_scope: selected-section
      locator: "Contrato de criação e validações da requisição"
      content_state: working-tree
      revision: null
      availability: available
    - path: src/backend/tests/fixtures/curriculo_exportacao.py
      relationship: context
      representation: source-code
      function: data-fixture
      format: python
      analysis_scope: whole-file
      locator: null
      content_state: working-tree
      revision: null
      availability: available
routing:
  root: prompts
  selected_directory: prompts/backend
  considered_directories: [prompts/backend, prompts/requisitos, prompts/revisao]
  confidence: high
  rationale: "Continuidade da linhagem e foco em fixture, domínio e persistência do backend; alternativa C delimita a fatia técnica atual."
classification:
  sphere: engineering
  concerns: [data, integration, reliability]
  decision_kind: design
  scope: component
  lifecycle: design
  urgency: normal
  uncertainty: medium
  reversibility: easy
  risk: low
---

# Análise de decisão — Dados reutilizáveis de perfis para testes de integração e E2E

## Solicitação original

```text
$decision-analysis-v4 Issue #148 Crie dados reutilizáveis de estudante, formação, experiência e currículo para testes de integração e E2E. Devem ser criados perfis fakes para teste utilizando SQLite e uma função para ler do SQLite e injetar nesses testes de integração de E2E.
```

## Informações complementares

```text
$decision-analysis-v4 Revise 20261009-154428-dados-reutilizaveis-perfis-testes-integracao-e2e-v002.md. Escolha a alternativa C (objetos em memória para o resto) e, para a decisão 2, handoffs.
```

## Mudanças desde a versão anterior

| Elemento | Versão anterior | Versão atual | Motivo | Impacto |
|---|---|---|---|---|
| Alternativa escolhida | C era possível somente após aprovação explícita | C escolhida: SQLite para usuário e currículo, objetos de domínio em memória para formação e experiência | Instrução literal do usuário | Fecha a escolha de escopo desta issue |
| Status | `pending` por falta de schema e autorização | `proposed`; schema adicional e autorização viram handoffs de decisões separadas | O usuário selecionou o recorte parcial e pediu handoffs para a decisão 2 | Autoriza revisão/implementação da fatia fixture definida, sem autorizar mudança de produto |
| Perfis | Completo/negativo definidos conceitualmente | Perfil combinado especificado com fronteira explícita entre persistido e memória; cenários negativos mantêm dados válidos | Tornar a decisão executável e não sugerir persistência que o schema não oferece | Evita cobertura fictícia de integração para formação/experiência |
| Impacto | Decisão reaberta | Decisão revisada e delimitada | Lacuna de schema removida do escopo desta implementação por escolha explícita | Handoffs preservam a evolução futura |

## Artefatos analisados

| Caminho | Relação | Representação | Função | Formato | Recorte | Estado/revisão |
|---|---|---|---|---|---|---|
| `prompts/backend/20261009-154428-dados-reutilizaveis-perfis-testes-integracao-e2e-v002.md` | Principal | Prosa | Documentação | Markdown | Arquivo completo e decisão anterior | Working tree; sem commit registrado |
| `docs/requisitos_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RF01–RF04, RF13–RF15 e detalhamentos | Working tree |
| `docs/requisitos_nao_funcionais.md` | Apoio | Prosa | Documentação | Markdown | RNF04–RNF05 e critérios de verificação | Working tree |
| `docs/matriz_testes.md` | Apoio | Prosa | Documentação | Markdown | Casos CT-RF01, 02, 03, 08, 13, 14 e 15 | Working tree |
| `src/backend/AGENTS.md` | Contexto | Prosa | Instrução de agente | Markdown | Arquivo completo | Working tree |
| `src/backend/domain/itens_perfil.py`, `curriculo.py` | Apoio | Código-fonte | Produção | Python | Entidades de formação/experiência e aggregate Curriculo | Working tree |
| `src/backend/api/cadastro_acesso.py`, `versao_curriculo.py` | Apoio | Código-fonte | Produção | Python | DTOs, endpoints e limitações de sessão/autorização | Working tree |
| `src/backend/infrastructure/persistence/sqlalchemy/usuario.py`, `curriculo.py`, `metadata.py` | Apoio | Código-fonte | Contrato de schema | Python | Mappings e metadata | Working tree |
| `src/backend/infrastructure/persistence/alembic/versions/20260916_0001_criar_usuarios.py`, `20261005_0002_criar_curriculos.py` | Apoio | Código-fonte | Contrato de schema | Python | Migrations existentes | Working tree |
| `src/backend/tests/test_infrastructure_usuario_mapping.py`, `test_infrastructure_curriculo_mapping.py`, `test_domain_experiencia_profissional.py`, `test_api_criar_versao_curriculo.py` | Apoio | Código-fonte | Teste | Python | Contratos, invariantes e validação de entrada relevantes | Working tree |
| `src/backend/tests/fixtures/curriculo_exportacao.py` | Contexto | Código-fonte | Fixture de dados | Python | Fixture existente de objetos de domínio sem banco | Working tree |

### Limites da evidência dos artefatos

Os mappings/migrations atuais cobrem `usuarios` e `curriculos`, com FK do currículo para usuário; formação e experiência são entidades de domínio sem mapping persistente, e referências do currículo aos itens não são persistidas. O escopo desta versão aceita explicitamente esse limite e não apresenta os objetos em memória como cobertura SQLite.

A matriz é de aceitação, não exaustiva. Os negativos de isolamento/autorização permanecem cenários para os quais a fixture pode preparar dados, mas os endpoints examinados não implementam sessão/autorização suficiente para executá-los como E2E hoje. Fixtures existentes usam domínio diretamente; não demonstram o acesso SQLite proposto. Não foi consultado conteúdo remoto da Issue #148.

## Problema enriquecido

### Resultado desejado

Disponibilizar cenário reutilizável de estudante e currículo persistido em SQLite, combinado com formação e experiência válidas como objetos de domínio em memória, além de estados de borda e dados para cenários negativos. Uma função de teste deve consultar o banco para a parte persistida e compor o cenário completo sem declarar que as partes em memória foram armazenadas.

### Atores e interesses

- Autores de testes de integração precisam validar a leitura real de usuário/currículo no adapter SQLite e reutilizar objetos de domínio para os itens sem mapping.
- Autores de testes de sistema/E2E precisam de massa consistente para pré-condições e jornadas que já tenham suporte de produto.
- QA precisa de rastreabilidade dos estados negativos à matriz e de separação entre preparação de estado e ação rejeitada.

### Evidências e fatos observados

- RF01–RF03 cobrem dados de estudante, formação e experiência; CT-RF03-03 descreve isolamento entre dois estudantes.
- CT-RF02-04 cobre item removido; CT-RF08-02 aceita currículo incompleto para orientação; CT-RF15-03 representa currículos sem seleção atual.
- CT-RF13-02/03, CT-RF09-04, CT-RF14-05 e CT-RF15-04 descrevem não autenticado ou tentativa de acesso cruzado.
- O schema atual tem usuários com UUID, nome, e-mail único e hash; currículos têm UUID, owner obrigatório por FK, título, layout e visibilidade não nulos.
- Formação e experiência existem no domínio, mas não são mapeadas no schema atual. O agregado Curriculo mantém referências localmente, sem persistência das referências no mapping atual.
- Os contratos de cadastro/versão restringem formatos e tamanhos; invariantes de domínio rejeitam dados essenciais vazios e períodos inválidos.
- A rota de acesso não estabelece sessão; rotas de currículo recebem `usuario_id` do caminho. Autorização é uma pendência do produto, não da fixture.

### Hipóteses

- “Objetos em memória para o resto” significa que formação e experiência serão instanciadas como entidades válidas do domínio no mesmo cenário de teste, sem SQLite.
- Cenários negativos de propriedade podem reutilizar usuários/currículos persistidos válidos, enquanto o teste executa a tentativa; ausência de sessão é um estado do cliente/harness, não uma conta falsa.
- IDs e valores fixos dão determinismo, desde que cada execução use banco isolado/limpo.

### Perguntas em aberto

- Nenhuma necessária para implementar a decisão delimitada nesta versão. Ciclo de vida do SQLite deve seguir a configuração de teste existente.
- Autenticação/autorização real para os cenários protegidos permanece encaminhada como decisão separada.

### Escopo

- SQLite de teste para registros de estudante e currículo, usando schema/mappings existentes.
- Formação e experiência como entidades válidas, determinísticas e em memória, associadas ao mesmo `usuario_id` do cenário.
- Uma função reutilizável que lê estudante/currículo do SQLite e compõe/retorna os dados em memória do perfil combinado.
- Cenários nomeados: perfil completo; segundo estudante/currículo para preparar isolamento; perfil com currículo incompleto para revisão; estudante com currículos sem seleção; objetos/payloads inválidos produzidos no ponto de teste e nunca persistidos.
- Testes integrados que comprovem leitura SQLite e composição da fixture, sem implementar autenticação/autorização no produto.

### Fora do escopo

- Criar mappings, migrations, constraints ou repositórios de formação/experiência/referências.
- Implementar ou corrigir sessão, autenticação, autorização ou APIs protegidas.
- Afirmar que testes E2E de acesso cruzado passarão antes da implementação correspondente no produto.
- Persistir entradas negativas em violação de constraints ou invariantes.

### Critérios de sucesso

- O usuário e currículo retornados foram lidos do SQLite e têm relação de proprietário válida conforme schema.
- Formação/experiência são objetos de domínio válidos em memória, determinísticos e com `usuario_id` coerente; a fixture deixa explícito que não vieram do banco.
- Perfil completo e variações válidas de borda são fáceis de obter sem duplicar setup.
- Cenários negativos de isolamento usam dois proprietários e dados válidos; o catálogo entrega estado preparatório, sem mascarar a ausência de suporte de autorização.
- Dados/payloads inválidos não são inseridos no SQLite.
- A execução e cleanup mantêm isolamento, sem estado vazando entre testes.

## Restrições aplicáveis

- Manter regras arquiteturais do backend: ORM na infraestrutura; domínio sem dependência de banco; fixtures exclusivamente na área de testes.
- Não alterar produto/schema ou requisitos nesta decisão.
- Usar ambientes Nix prescritos para implementação e validação; testes de integração/E2E usam `tests`.
- Toda classe/função nova deve ter docstring completa conforme AGENTS.
- A análise autoriza a fatia definida, não os handoffs nem mudanças de produto.

## Classificação comentada

- Esfera `engineering`, preocupações `data`, `integration`, `reliability`, decisão `design`, escopo `component`.
- Incerteza média: o contrato da fixture fica definido, mas o modo de isolamento SQLite deve seguir configuração existente e autorização futura não está disponível.
- Risco baixo e reversibilidade fácil, pois o artefato é dado exclusivamente de teste e não muda schema nem produto.

## Decisão de roteamento

Continua em `prompts/backend`: mesma linhagem, fixture e persistência do backend. `requisitos` e `revisao` não representam o propósito principal desta análise.

## Dimensões de decisão

| Dimensão | Prioridade | Limiar ou direção | Por que importa |
|---|---|---|---|
| `correctness` | Alta | Persistir somente o que o schema suporta; objetos restantes respeitam domínio | Evita alegações falsas sobre cobertura de persistência |
| `reliability` | Alta | IDs determinísticos e estado isolado | Previne flakiness e contaminação |
| `interoperability` | Média | Função comum de composição para consumidores elegíveis | Reduz duplicação entre suites sem ocultar fronteiras |
| `simplicity` | Média | Um cenário combinado com proveniência explícita de cada parte | Mantém a fixture compreensível |

## Alternativas consideradas

- **A — Persistir todos os dados no SQLite:** oferece integração relacional completa, mas exige schema/migrations ainda inexistentes para formação/experiência e referências; ultrapassa a decisão escolhida e requer handoff.
- **B — Apenas objetos em memória:** simples e cobre domínio, mas não atende ao requisito de leitura do SQLite para estudante/currículo.
- **C — SQLite para estudante/currículo e objetos em memória para formação/experiência (escolhida):** usa mappings existentes, satisfaz a necessidade imediata de leitura/injeção parcial e conserva objetos válidos. Não prova persistência relacional dos itens em memória; explicitar esse limite evita sobreinterpretação.

## Perfil de pagamento comparativo

| Dimensão | Prioridade | Alternativa A | Alternativa B | Alternativa C | Confiança | Base |
|---|---:|---:|---:|---:|---|---|
| `correctness` | Alta | +2 | 0 | +1 | Alta | A cobre tudo se schema existir; C descreve fielmente fronteiras atuais; B não valida SQLite. |
| `reliability` | Alta | +2 | +1 | +1 | Média | Todas podem ser determinísticas; C exige compor duas fontes controladas. |
| `interoperability` | Média | +2 | 0 | +1 | Média | C fornece objeto comum aos consumidores sem fingir persistência integral. |
| `simplicity` | Média | -1 | +2 | 0 | Média | A demanda schema; B tem uma fonte; C mantém composição híbrida, porém pequena e explícita. |

## Histórico e decisão atual

### Decisão da versão anterior

A v002 manteve `pending`, pois formação/experiência não têm mappings e autorização está incompleta. A v001 originalmente recomendava persistência de todos os perfis no SQLite.

### Decisão recomendada nesta versão

Escolher a alternativa C. Persistir no SQLite de teste os registros `UsuarioRegistro` e `CurriculoRegistro` conforme as tabelas/migrations atuais. Ler esses registros pela função fixture e compor o cenário com objetos de domínio `FormacaoAcademica` e `ExperienciaProfissional` em memória, usando IDs estáveis e o mesmo proprietário. A função deve tornar distinguível o que veio do banco e o que foi construído em memória. Preparar dados de dois estudantes/currículos para cenários de isolamento, mas deixar a execução de expectativas de autorização para quando o produto oferecer identidade de solicitante e proteção correspondentes.

### Impacto da revisão

Decisão revisada: a alternativa C foi escolhida explicitamente pelo usuário, removendo a necessidade de schema de formação/experiência como bloqueio desta fatia. A decisão fica `proposed`; não aprova mudanças de produto, schema ou autorização.

### Dimensões maximizadas ou priorizadas

| Dimensão | Estado | Ganho esperado | Evidência ou hipótese |
|---|---|---|---|
| `correctness` | prioritized | Fronteira entre dados persistidos e objetos em memória permanece explícita | Mappings existentes e escolha explícita da alternativa C. |
| `reliability` | prioritized | Cenários determinísticos com isolamento do banco | Hipótese apoiada na fixture atual; validar no runner. |

### Dimensões satisfeitas por limiar

| Dimensão | Limiar aceito | Como a decisão atende |
|---|---|---|
| `interoperability` | Um objeto de cenário utilizável por suites sem afirmar origem uniforme dos dados | Composição única pela função de teste. |
| `simplicity` | Um perfil combinado e variações nomeadas, sem novo schema | Uso dos mappings atuais e construtores de domínio existentes. |

## Perdas e trade-offs

### Perdas se as prioridades não forem atendidas

| Dimensão | Perda esperada | Severidade | Afetados |
|---|---|---|---|
| `correctness` | Consumidores podem supor incorretamente que formação/experiência foram persistidas | Moderada | Autores de testes e QA |
| `reliability` | Banco compartilhado pode vazar estado entre cenários | Moderada | CI e equipe backend |
| `interoperability` | Suites podem recriar composição de modo divergente | Baixa | QA e manutenção |

### Custos aceitos para priorizá-las

| Dimensão favorecida | Custo ou oportunidade | Dimensão prejudicada | Aceitabilidade |
|---|---|---|---|
| `time-to-value` com schema existente | Parte dos dados do perfil não exercita persistência | `interoperability`/cobertura de integração | Aceitável como limite deliberado e documentado; reavaliar após decisão de persistência completa. |
| `correctness` sobre negativos | Cenários inválidos são gerados como ação/payload e não como seed | `simplicity` | Aceitável para preservar constraints e invariantes. |

## Riscos e efeitos de segunda ordem

- A fixture híbrida pode ser confundida com um agregado integralmente persistido; separar campos/retorno ou documentar claramente a origem.
- CurriculoRegistro não persiste referências aos itens; não usar a fixture para afirmar leitura relacional do currículo completo.
- A existência de dados de proprietário B não prova que A será impedido de acessar B; esse comportamento requer produto com identidade/autorização.
- A alternativa C pode virar solução permanente por inércia; handoff da decisão 2 deve reavaliar schema sem ampliar esta issue.

## Validação da decisão

| Hipótese ou resultado | Evidência necessária | Método | Sinal para revisar |
|---|---|---|---|
| Usuário e currículo são efetivamente lidos do SQLite | Instância isolada e rows criadas pelas migrations/mappings atuais | Teste de integração de fixture contra SQLite descartável | Retorno criado somente em memória ou constraint/FK não observada |
| Objetos em memória são válidos e pertencem ao mesmo estudante | Invariantes de domínio e igualdade de `usuario_id` | Asserções na composição do cenário | IDs de proprietário inconsistentes ou período inválido |
| Fixture é determinística e isolada | Valores fixos e banco limpo por execução | Executar caso isolado e em sequência na suite de integração | Ordem afeta resultado ou banco deixa estado residual |
| Casos negativos não contaminam seed | Persistência contém somente estados válidos; ação/payload fica no teste consumidor | Inspecionar estado antes/depois da tentativa | Fixture exige desativar constraints ou inserir registro inválido |
| Handoff de autorização é realmente separado | Contrato futuro identifica ator autenticado e oráculo de acesso cruzado | Nova análise antes de testes E2E de autorização | Implementação da fixture passa a pressupor guard inexistente |

## Handoffs e atividades posteriores

- **Decisão 2 — persistência integral de dados do perfil:** abrir análise separada para decidir mappings Code First, migrations e relações de formação/experiência e referências no currículo; considerar impactos em repositórios, contratos e cobertura de integração. Não incluir essas mudanças nesta issue/decisão.
- **Decisão de produto separada — sessão e autorização:** definir identidade do ator, sessão e proteção dos endpoints necessários a CT-RF13-02/03, CT-RF09-04, CT-RF14-05 e CT-RF15-04. Até lá, a fixture pode fornecer os dois proprietários e dados preparatórios, mas não se deve implementar teste E2E de autorização como se o mecanismo existisse.
- Handoff de implementação desta análise: fixture e testes integrados permitidos devem usar somente `src/backend/tests`, sem alterar aplicação, mappings ou migrations; rastrear o código à versão v003 e validar em ambiente Nix de testes.

## Síntese

A alternativa C foi escolhida: usuário e currículo vêm do SQLite usando o schema existente; formação e experiência completam o cenário como objetos de domínio em memória. Dados de borda/negativos devem preservar registros válidos e representar a violação na ação ou payload. A decisão está proposta para implementação dessa fixture híbrida; persistência completa e autorização ficam como handoffs separados, sem bloquear a fatia atual.
